#!/usr/bin/env python3
"""Bounded read-only observations; no network diagnosis or configuration writes."""

import argparse
from datetime import datetime
import ipaddress
import json
import locale
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time

OUTPUT_LIMIT = 24_000
INSPECT_TIMEOUT = 15
TRACE_TIMEOUT = 45


def timestamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def target(value):
    """Allow literal IPs (with scope) or ASCII DNS names, never options/URLs."""
    try:
        address = ipaddress.ip_address(value)
        if "%" in value and not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", address.scope_id):
            raise ValueError("Invalid IPv6 scope")
        return value
    except ValueError:
        if len(value) <= 253 and re.fullmatch(
            r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
            r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*\.?", value
        ):
            # Malformed numeric addresses should not silently become DNS names.
            if not re.fullmatch(r"[0-9.]+", value):
                return value
        raise argparse.ArgumentTypeError("Use a literal IP or ASCII DNS name, not a URL, option, or shell expression")


def gateway(value):
    value = target(value)
    try:
        ipaddress.ip_address(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Gateway must be a literal IP from the selected route")
    return value


def count(value):
    try:
        number = int(value)
        if 1 <= number <= 60:
            return number
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("Count must be an integer from 1 to 60")


def powershell(code):
    # Only fixed internal code is accepted here. User targets are separate argv.
    return ["powershell.exe", "-NoLogo", "-NoProfile", "-NonInteractive", "-Command",
            "$ErrorActionPreference='Stop'; [Console]::OutputEncoding=[System.Text.Encoding]::UTF8; " + code]


def plan(system, args):
    if system == "Windows":
        inspections = [
            ("interfaces", powershell("Get-NetAdapter | Format-Table -AutoSize | Out-String -Width 180")),
            ("configuration", powershell("Get-NetIPConfiguration | Format-List | Out-String -Width 180")),
            ("dns-config", powershell("Get-DnsClientServerAddress | Format-Table -AutoSize | Out-String -Width 180")),
            ("routes", powershell("Get-NetRoute | Format-Table -AutoSize | Out-String -Width 180")),
            ("mtu", powershell("Get-NetIPInterface | Format-Table -AutoSize | Out-String -Width 180")),
        ]
    elif system == "Darwin":
        inspections = [("interfaces", ["ifconfig"]), ("hardware", ["networksetup", "-listallhardwareports"]),
                       ("dns-config", ["scutil", "--dns"]), ("routes", ["netstat", "-rn"]),
                       ("default-route", ["route", "-n", "get", "default"])]
    elif system == "Linux":
        inspections = [("interfaces", ["ip", "-brief", "address"]), ("link-counters", ["ip", "-s", "link"]),
                       ("routes-v4", ["ip", "route", "show"]), ("routes-v6", ["ip", "-6", "route", "show"]),
                       ("dns-config", ["resolvectl", "status"])]
    else:
        raise ValueError("Unsupported OS; use manual instructions for Windows, macOS, or Linux")

    commands = [(name, argv, INSPECT_TIMEOUT) for name, argv in inspections]
    for name, host in [("gateway-ping", args.gateway), ("target-ping", args.target)]:
        if host:
            # Literal gateways use their own family; target hostname uses explicit choice.
            family = args.family
            try:
                family = str(ipaddress.ip_address(host).version)
            except ValueError:
                pass
            if system == "Windows":
                argv = ["ping.exe", "-" + family, "-n", str(args.count), "-w", "1000", host]
            elif system == "Darwin":
                argv = ["ping6", "-c", str(args.count), host] if family == "6" else [
                    "ping", "-c", str(args.count), "-W", "1000", host]
            else:
                argv = ["ping", "-" + family, "-c", str(args.count), "-W", "1", host]
            commands.append((name, argv, args.count * 2 + 10))
    if args.target:
        # Subprocess boundary bounds DNS too, unlike an in-process socket lookup.
        code = ("import json,socket,sys; "
                "a=socket.getaddrinfo(sys.argv[1],443,socket.AF_INET if sys.argv[2]=='4' else socket.AF_INET6,socket.SOCK_STREAM); "
                "print(json.dumps(sorted({x[4][0] for x in a})))")
        commands.append(("system-dns", [sys.executable, "-c", code, args.target, args.family], 10))
        code = ("import socket,sys; "
                "a=socket.getaddrinfo(sys.argv[1],443,socket.AF_INET if sys.argv[2]=='4' else socket.AF_INET6,socket.SOCK_STREAM); "
                "s=socket.socket(a[0][0],socket.SOCK_STREAM); s.settimeout(5); "
                "s.connect(a[0][4]); s.close(); print('TCP 443 connected to first resolved address; not application validation')")
        commands.append(("tcp-443", [sys.executable, "-c", code, args.target, args.family], 10))
        if args.trace:
            if system == "Windows":
                argv = ["tracert.exe", "-" + args.family, "-d", "-h", "12", "-w", "1000", args.target]
            elif system == "Darwin":
                argv = ["traceroute6" if args.family == "6" else "traceroute", "-n", "-m", "12", "-w", "1", args.target]
            else:
                argv = ["traceroute", "-" + args.family, "-n", "-m", "12", "-w", "1", args.target]
            commands.append(("trace", argv, TRACE_TIMEOUT))
    return commands


def run(name, argv, timeout):
    started = time.monotonic()
    record = {"id": name, "started_at": timestamp(), "command": argv, "status": "unavailable",
              "exit_code": None, "output": "", "truncated": False}
    if not shutil.which(argv[0]):
        record["output"] = "Command not installed or not on PATH"
    else:
        env = dict(os.environ, LC_ALL="C", LANG="C", NO_COLOR="1", PYTHONIOENCODING="utf-8")
        # A private spool file bounds retained memory even for unusually verbose tools.
        with tempfile.TemporaryFile() as output:
            try:
                result = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=output,
                                        stderr=subprocess.STDOUT, timeout=timeout, env=env, shell=False)
                record["exit_code"] = result.returncode
                record["status"] = "ok" if result.returncode == 0 else "error"
            except subprocess.TimeoutExpired:
                record["status"] = "timeout"
            except OSError as error:
                record["output"] = str(error)
            except KeyboardInterrupt:
                record["status"] = "timeout"
                record["output"] = "Interrupted; partial output follows\n"
                # Retain this observation and let caller cancel the remaining plan.
                record["interrupted"] = True
            output.seek(0)
            raw = output.read(OUTPUT_LIMIT + 1)
            record["truncated"] = len(raw) > OUTPUT_LIMIT
            encoding = "utf-8" if name not in ("gateway-ping", "target-ping", "trace") or platform.system() != "Windows" else locale.getpreferredencoding(False)
            record["output"] += raw[:OUTPUT_LIMIT].decode(encoding, errors="replace")
    record["duration_seconds"] = round(time.monotonic() - started, 3)
    return record


def markdown(report):
    lines = ["# Internet diagnostic evidence", "", "Sensitive local evidence; review before sharing. No automatic diagnosis.",
             "", f"Captured: {report['captured_at']} | OS: {report['os']}"]
    if report.get("cancelled"):
        lines += ["", "Cancelled; remaining observations not collected."]
    for item in report["observations"]:
        # Dynamic fences keep untrusted output containing Markdown fences inside code.
        content = json.dumps(item["command"], ensure_ascii=True) + "\n\n" + item["output"]
        content = "".join(c if c in "\n\t" or ord(c) >= 32 else "�" for c in content)
        fence = "`" * max(3, 1 + max((len(x) for x in re.findall(r"`+", content)), default=0))
        lines += ["", "## " + item["id"], "", f"Status: {item['status']} | Started: {item['started_at']} | Duration: {item['duration_seconds']} s | Truncated: {item['truncated']}",
                  "", fence + "text", content, fence]
    return "\n".join(lines) + "\n"


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--target", type=target, help="Authorized hostname/IP; adds ICMP, system DNS, TCP 443")
    cli.add_argument("--gateway", type=gateway, help="Literal selected-route gateway; adds ICMP probes")
    cli.add_argument("--count", type=count, default=10, help="1–60 echo probes per target (default 10)")
    cli.add_argument("--family", choices=("4", "6"), default="4", help="Target address family (default 4)")
    cli.add_argument("--trace", action="store_true", help="Add bounded 12-hop trace; requires --target")
    cli.add_argument("--dry-run", action="store_true", help="Print command plan without executing")
    cli.add_argument("--format", choices=("json", "markdown"), default="json")
    return cli


def main(argv=None):
    cli = parser()
    args = cli.parse_args(argv)
    if args.trace and not args.target:
        cli.error("--trace requires --target")
    if args.target:
        try:
            if str(ipaddress.ip_address(args.target).version) != args.family:
                cli.error("Literal target family conflicts with --family; choose matching family")
        except ValueError:
            pass
    system = platform.system()
    try:
        commands = plan(system, args)
    except ValueError as error:
        cli.error(str(error))
    if args.dry_run:
        print(json.dumps([{"id": name, "command": cmd, "timeout_seconds": timeout}
                          for name, cmd, timeout in commands], indent=2))
        return 0
    print("Read-only collection. Output contains sensitive network data; no upload. Ctrl+C cancels.", file=sys.stderr)
    report = {"schema_version": 1, "captured_at": timestamp(), "os": system,
              "os_release": platform.release(), "observations": []}
    try:
        for name, cmd, timeout in commands:
            observation = run(name, cmd, timeout)
            report["observations"].append(observation)
            if observation.pop("interrupted", False):
                report["cancelled"] = True
                break
    except KeyboardInterrupt:
        report["cancelled"] = True
    print(markdown(report) if args.format == "markdown" else json.dumps(report, indent=2, ensure_ascii=True))
    return 130 if report.get("cancelled") else 0


if __name__ == "__main__":
    sys.exit(main())
