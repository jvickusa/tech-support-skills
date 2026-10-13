import argparse
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("collect", ROOT / "skills/internet-diagnostics/scripts/collect.py")
collect = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(collect)


class CollectorTests(unittest.TestCase):
    def test_target_validation(self):
        for value in ["example.com", "game.example.", "192.0.2.1", "2001:db8::1", "fe80::1%en0"]:
            self.assertEqual(collect.target(value), value)
        for value in ["-n", "/t", "https://example.com", "host;echo", "$(whoami)", "a b", "a\nb", "bad..name", "999.0.0.1", "fe80::1%a;bad", "a" * 254, ""]:
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                collect.target(value)

    def test_gateway_requires_literal_and_count_bounded(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            collect.gateway("example.com")
        for value in ["0", "61", "abc", "1.5"]:
            with self.assertRaises(argparse.ArgumentTypeError):
                collect.count(value)
        self.assertEqual(collect.count("60"), 60)

    def test_platform_baselines_have_no_probes(self):
        for system in ["Windows", "Darwin", "Linux"]:
            commands = collect.plan(system, collect.parser().parse_args([]))
            self.assertTrue(commands)
            self.assertFalse(any("ping" in name or "tcp" in name or "trace" in name for name, _, _ in commands))
            self.assertTrue(all(timeout <= 15 for _, _, timeout in commands))
        with self.assertRaises(ValueError):
            collect.plan("Other", collect.parser().parse_args([]))

    def test_platform_probe_flags_and_gateway_family(self):
        args = collect.parser().parse_args(["--target", "example.com", "--gateway", "192.0.2.1", "--count", "20", "--trace", "--family", "6"])
        for system in ["Windows", "Darwin", "Linux"]:
            commands = {name: (cmd, timeout) for name, cmd, timeout in collect.plan(system, args)}
            gw, timeout = commands["gateway-ping"]
            self.assertEqual(gw[-1], "192.0.2.1")
            self.assertIn("20", gw)
            self.assertEqual(timeout, 50)
            self.assertLessEqual(commands["trace"][1], 45)
            self.assertEqual(commands["tcp-443"][0][-2:], ["example.com", "6"])
            if system == "Darwin":
                self.assertEqual(commands["target-ping"][0][0], "ping6")
                self.assertIn("1000", gw)
            else:
                self.assertIn("-4", gw)
                self.assertIn("-6", commands["target-ping"][0])

    def test_optional_wifi_vpn_profiles_are_read_only_and_bounded(self):
        args = collect.parser().parse_args(["--wifi", "--vpn"])
        for system in ["Windows", "Darwin", "Linux"]:
            commands = collect.plan(system, args)
            ids = [name for name, _, _ in commands]
            self.assertTrue(any(name.startswith("wifi-") for name in ids))
            self.assertTrue(any(name.startswith("vpn-") for name in ids))
            self.assertNotIn("target-ping", ids)
            for _, argv, timeout in commands:
                self.assertLessEqual(timeout, collect.INSPECT_TIMEOUT)
                self.assertNotIn("--show-secrets", argv)
                self.assertNotIn("--rescan yes", " ".join(argv))
                self.assertNotIn("Disconnect-Vpn", " ".join(argv))
            if system == "Linux":
                cached = next(argv for name, argv, _ in commands if name == "wifi-cached")
                self.assertEqual(cached[-2:], ["--rescan", "no"])

    def test_profiles_only_when_selected(self):
        for system in ["Windows", "Darwin", "Linux"]:
            ids = [name for name, _, _ in collect.plan(system, collect.parser().parse_args([]))]
            self.assertFalse(any(name.startswith(("wifi-", "vpn-")) for name in ids))

    def test_missing_tool(self):
        with patch.object(collect.shutil, "which", return_value=None), patch.object(collect.subprocess, "run") as run:
            result = collect.run("test", ["missing"], 1)
        self.assertEqual(result["status"], "unavailable")
        self.assertIsNone(result["exit_code"])
        run.assert_not_called()

    def simulated_run(self, behavior):
        with patch.object(collect.shutil, "which", return_value="tool"), patch.object(collect.subprocess, "run", side_effect=behavior):
            return collect.run("test", ["tool", "arg"], 1)

    def test_nonzero_exit_retains_evidence(self):
        def behavior(argv, **kwargs):
            self.assertFalse(kwargs["shell"])
            self.assertEqual(kwargs["timeout"], 1)
            kwargs["stdout"].write(b"one valid reply; later unavailable")
            return subprocess.CompletedProcess(argv, 1)
        result = self.simulated_run(behavior)
        self.assertEqual(result["status"], "error")
        self.assertIn("valid reply", result["output"])
        self.assertEqual(result["exit_code"], 1)
        self.assertNotIn("loss", result)

    def test_timeout_preserves_partial(self):
        def behavior(argv, **kwargs):
            kwargs["stdout"].write(b"partial reply")
            raise subprocess.TimeoutExpired(argv, 1)
        result = self.simulated_run(behavior)
        self.assertEqual(result["status"], "timeout")
        self.assertEqual(result["output"], "partial reply")
        self.assertIsNone(result["exit_code"])

    def test_output_limit_and_decode(self):
        def behavior(argv, **kwargs):
            kwargs["stdout"].write(b"\xff" + b"x" * (collect.OUTPUT_LIMIT + 50))
            return subprocess.CompletedProcess(argv, 0)
        result = self.simulated_run(behavior)
        self.assertTrue(result["truncated"])
        self.assertLessEqual(len(result["output"]), collect.OUTPUT_LIMIT)
        self.assertEqual(result["status"], "ok")

    def test_permission_error_unavailable(self):
        result = self.simulated_run(PermissionError("denied"))
        self.assertEqual(result["status"], "unavailable")
        self.assertIn("denied", result["output"])

    def test_dry_run_does_not_execute(self):
        with contextlib.redirect_stdout(io.StringIO()) as out, patch.object(collect, "run") as run:
            self.assertEqual(collect.main(["--dry-run", "--target", "example.com"]), 0)
        self.assertTrue(json.loads(out.getvalue()))
        run.assert_not_called()

    def test_conflicting_literal_family_and_trace_without_target(self):
        for args in [["--target", "::1"], ["--trace"]]:
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                collect.main(args)
            self.assertEqual(error.exception.code, 2)

    def test_cancel_emits_partial_json(self):
        def behavior(argv, **kwargs):
            kwargs["stdout"].write(b"retained before cancel")
            raise KeyboardInterrupt
        with patch.object(collect.platform, "system", return_value="Windows"), patch.object(collect.platform, "release", return_value="test"), patch.object(collect.shutil, "which", return_value="tool"), patch.object(collect.subprocess, "run", side_effect=behavior), contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(collect.main([]), 130)
        report = json.loads(out.getvalue())
        self.assertTrue(report["cancelled"])
        self.assertEqual(len(report["observations"]), 1)
        self.assertIn("retained", report["observations"][0]["output"])
        self.assertNotIn("interrupted", report["observations"][0])

    def test_markdown_keeps_untrusted_fences_in_code(self):
        item = {"id": "test", "command": ["tool"], "output": "```\n<script>evil</script>\n\x1b", "status": "ok", "started_at": "now", "duration_seconds": 1, "truncated": False}
        result = collect.markdown({"captured_at": "now", "os": "Linux", "observations": [item]})
        self.assertIn("````text", result)
        self.assertIn("<script>evil</script>", result)
        self.assertNotIn("\x1b", result)

    def test_real_local_subprocess(self):
        result = collect.run("test", [collect.sys.executable, "-c", "print('local-only')"], 5)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["output"].strip(), "local-only")

    def test_real_timeout_retains_flushed_output(self):
        result = collect.run("test", [collect.sys.executable, "-c", "import time; print('partial', flush=True); time.sleep(30)"], 1)
        self.assertEqual(result["status"], "timeout")
        self.assertIn("partial", result["output"])
        self.assertLess(result["duration_seconds"], 10)


class PackagingTests(unittest.TestCase):
    def test_relative_document_links_resolve(self):
        import re
        for path in ROOT.rglob("*.md"):
            for destination in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if "://" not in destination and not destination.startswith("#"):
                    with self.subTest(path=path, destination=destination):
                        self.assertTrue((path.parent / destination.split("#")[0]).exists())

    def test_standalone_skill_preserves_mit_license(self):
        for skill in ["internet-diagnostics", "game-diagnostic", "game-optimizer"]:
            with self.subTest(skill=skill):
                self.assertEqual((ROOT / "LICENSE").read_bytes(), (ROOT / "skills" / skill / "LICENSE").read_bytes())


if __name__ == "__main__":
    unittest.main()
