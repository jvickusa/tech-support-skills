import test from 'node:test';
import assert from 'node:assert/strict';
import { configuration, probe, TIMEOUT_MS } from '../skills/internet-diagnostics/scripts/turn-probe.mjs';

class FakePeer {
  static current;
  constructor(config) { this.config = config; FakePeer.current = this; }
  createDataChannel() {}
  async createOffer() { return { type: 'offer', sdp: 'private-sdp' }; }
  async setLocalDescription() {}
  close() { this.closed = true; }
}
const config = () => configuration('turn:relay.example:3478?transport=udp', 'temporary-user', 'temporary-secret');

test('only one explicit TURN URL; no URLs containing credentials, fragments or options', () => {
  for (const value of ['stun:relay.example', 'https://example.com', 'turn:user:password@host', 'turn:host:0', 'turn:host:65536', 'turn:host#secret', 'turn:host?transport=bad']) {
    assert.throws(() => configuration(value, 'u', 'p'));
  }
  assert.equal(config().iceTransportPolicy, 'relay');
  assert.throws(() => configuration('turn:host', '', 'p'));
  assert.equal(configuration('turns:[2001:db8::1]:5349?transport=tcp', 'u', 'p').iceServers.length, 1);
});

test('observed relay candidate closes peer and emits no credentials/addresses/SDP', async () => {
  const run = probe(config(), FakePeer);
  const peer = FakePeer.current;
  peer.onicecandidate({ candidate: { type: 'host' } });
  peer.onicecandidateerror({ errorCode: 701, errorText: 'private-secret', url: 'private-server' });
  peer.onicecandidate({ candidate: { type: 'relay', address: 'private-address' } });
  const report = await run.promise;
  assert.equal(report.status, 'observed');
  assert.equal(report.relay_candidates, 1);
  assert.deepEqual(report.ice_error_codes, [701]);
  assert.equal(peer.closed, true);
  assert.equal(peer.onicecandidate, null);
  assert.doesNotMatch(JSON.stringify(report), /temporary|private|password|packet_loss/);
});

test('no relay and browser failures are unavailable, never loss', async () => {
  const run = probe(config(), FakePeer);
  FakePeer.current.iceGatheringState = 'complete';
  FakePeer.current.onicegatheringstatechange();
  assert.equal((await run.promise).status, 'unavailable');
  assert.equal((await probe(config(), null).promise).reason, 'browser-unavailable');
  class Broken extends FakePeer { async createOffer() { throw new Error('secret'); } }
  assert.equal((await probe(config(), Broken).promise).reason, 'setup-failed');
});

test('cancel is terminal, closes peer and blocks late descriptions', async () => {
  let settle, described = false;
  class Slow extends FakePeer {
    createOffer() { return new Promise(resolve => { settle = resolve; }); }
    setLocalDescription() { described = true; }
  }
  const run = probe(config(), Slow);
  run.cancel(); run.cancel();
  settle({ type: 'offer' });
  await Promise.resolve();
  assert.equal((await run.promise).status, 'cancelled');
  assert.equal(FakePeer.current.closed, true);
  assert.equal(described, false);
});

test('timeout is bounded and closes peer', async () => {
  const originalSet = globalThis.setTimeout, originalClear = globalThis.clearTimeout;
  let expire;
  globalThis.setTimeout = (fn, delay) => { assert.equal(delay, TIMEOUT_MS); expire = fn; return 1; };
  globalThis.clearTimeout = () => {};
  try {
    const run = probe(config(), FakePeer);
    expire();
    assert.equal((await run.promise).reason, 'timeout');
    assert.equal(FakePeer.current.closed, true);
  } finally { globalThis.setTimeout = originalSet; globalThis.clearTimeout = originalClear; }
});
