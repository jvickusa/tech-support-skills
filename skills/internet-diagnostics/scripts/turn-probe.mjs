// Native ICE allocation check only. No media or packet-loss measurement.
export const TIMEOUT_MS = 15_000;

export function configuration(url, username, credential) {
  const match = /^(turns?):(\[[0-9a-fA-F:]+\]|[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?)(?::([0-9]{1,5}))?(?:\?transport=(udp|tcp))?$/.exec(url);
  if (!match || (match[3] && (+match[3] < 1 || +match[3] > 65535))) {
    throw new Error('Enter one TURN/TURNS URL with an optional port and udp/tcp transport.');
  }
  if (!username || !credential || username.length > 1024 || credential.length > 2048) {
    throw new Error('Enter temporary username and credential within the supported length limits.');
  }
  return { iceTransportPolicy: 'relay', iceServers: [{ urls: [url], username, credential }] };
}

export function probe(config, Peer = globalThis.RTCPeerConnection) {
  const started = performance.now();
  const capturedAt = new Date().toISOString();
  const codes = new Set();
  let peer, timer, completed = false, candidates = 0, resolve;
  const promise = new Promise(r => { resolve = r; });
  function finish(status, reason) {
    if (completed) return;
    completed = true;
    clearTimeout(timer);
    if (peer) {
      peer.onicecandidate = peer.onicecandidateerror = peer.onicegatheringstatechange = null;
      peer.close();
    }
    resolve({ schema_version: 1, kind: 'turn-allocation', captured_at: capturedAt,
      status, reason, relay_candidates: candidates, ice_error_codes: [...codes],
      duration_seconds: Math.round((performance.now() - started) / 10) / 100 });
  }
  if (!Peer) {
    finish('unavailable', 'browser-unavailable');
  } else {
    try {
      peer = new Peer(config);
      peer.onicecandidate = event => {
        if (event.candidate?.type === 'relay') {
          candidates++;
          finish('observed', 'relay-candidate');
        }
      };
      peer.onicecandidateerror = event => {
        // Do not expose URL, address, error text or authentication material.
        if (Number.isInteger(event.errorCode) && event.errorCode >= 300 && event.errorCode <= 799 && codes.size < 20) {
          codes.add(event.errorCode);
        }
      };
      peer.onicegatheringstatechange = () => {
        if (peer.iceGatheringState === 'complete') finish('unavailable', 'no-relay-candidate');
      };
      timer = setTimeout(() => finish('unavailable', 'timeout'), TIMEOUT_MS);
      peer.createDataChannel('allocation-only');
      Promise.resolve(peer.createOffer()).then(offer => {
        if (!completed) return peer.setLocalDescription(offer);
      }).catch(() => finish('unavailable', 'setup-failed'));
    } catch {
      finish('unavailable', 'setup-failed');
    }
  }
  return { promise, cancel: () => finish('cancelled', 'user-cancelled') };
}
