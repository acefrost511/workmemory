#!/usr/bin/env node
/**
 * Spawn 12 intel agents via OpenClaw gateway WebSocket RPC - with challenge response
 */
const net = require('net');
const crypto = require('crypto');
const { createHmac } = require('crypto');

const GATEWAY_HOST = '127.0.0.1';
const GATEWAY_PORT = 18789;
const TOKEN = 'minimax-agent';

let socket;
let msgId = 0;
let pending = {};
let connected = false;
let receiveBuffer = Buffer.alloc(0);

function wsMask(data, key) {
  const buf = Buffer.from(data);
  for (let i = 0; i < buf.length; i++) {
    buf[i] ^= key[i % 4];
  }
  return buf;
}

function wsEncode(data) {
  const str = JSON.stringify(data);
  const len = Buffer.byteLength(str);
  const payload = Buffer.from(str);
  let header;
  if (len < 126) {
    header = Buffer.alloc(2);
    header[0] = 0x81;
    header[1] = len;
  } else {
    header = Buffer.alloc(4);
    header[0] = 0x81;
    header[1] = 0x7e;
    header.writeUInt16BE(len, 2);
  }
  return Buffer.concat([header, payload]);
}

function handleSocketData(chunk) {
  receiveBuffer = Buffer.concat([receiveBuffer, chunk]);
  while (receiveBuffer.length > 2) {
    const secondByte = receiveBuffer[1];
    let offset = 2;
    let payloadLen = secondByte & 0x7f;
    if (payloadLen === 126) {
      if (receiveBuffer.length < 4) return;
      payloadLen = receiveBuffer.readUInt16BE(2);
      offset = 4;
    } else if (payloadLen === 127) {
      if (receiveBuffer.length < 10) return;
      payloadLen = Number(receiveBuffer.readBigUInt64BE(2));
      offset = 10;
    }
    const masked = (secondByte & 0x80) !== 0;
    if (masked) offset += 4;
    const totalLen = offset + payloadLen;
    if (receiveBuffer.length < totalLen) return;
    
    const frame = receiveBuffer.slice(0, totalLen);
    receiveBuffer = receiveBuffer.slice(totalLen);
    
    const opcode = frame[0] & 0x0f;
    if (opcode === 0x8) {
      socket.end();
      return;
    }
    if (opcode === 0x1) {
      try {
        const data = JSON.parse(wsDecodeRaw(frame).toString());
        handleMessage(data);
      } catch(e) {
        console.error('Decode error:', e.message);
      }
    }
  }
}

function wsDecodeRaw(frame) {
  const secondByte = frame[1];
  let offset = 2;
  let payloadLen = secondByte & 0x7f;
  if (payloadLen === 126) { payloadLen = frame.readUInt16BE(2); offset = 4; }
  else if (payloadLen === 127) { payloadLen = Number(frame.readBigUInt64BE(2)); offset = 10; }
  const masked = (secondByte & 0x80) !== 0;
  if (masked) offset += 4;
  let payload = frame.slice(offset, offset + payloadLen);
  if (masked) {
    const key = frame.slice(offset - 4, offset);
    payload = wsMask(payload, key);
  }
  return payload;
}

function handleMessage(msg) {
  if (msg.type === 'event' && msg.event === 'connect.challenge') {
    const { nonce, ts } = msg.payload;
    // Sign: HMAC-SHA256 of nonce+ts using token
    const sig = createHmac('sha256', TOKEN)
      .update(nonce + ts)
      .digest('base64');
    console.log('Got challenge, sending response...');
    sendRaw({ type: 'auth.response', token: TOKEN, sig, nonce, ts });
    return;
  }
  if (msg.id && pending[msg.id]) {
    const resolve = pending[msg.id];
    delete pending[msg.id];
    resolve(msg.result || msg.error || msg);
  } else if (msg.type !== 'event' || !msg.event?.startsWith('connect')) {
    console.log('MSG:', JSON.stringify(msg).substring(0, 200));
  }
}

function sendRaw(data) {
  if (!socket || !connected) return;
  socket.write(wsEncode(data));
}

function sendRPC(method, params, timeout = 30000) {
  return new Promise((resolve, reject) => {
    const id = ++msgId;
    pending[id] = resolve;
    sendRaw({ jsonrpc: '2.0', id, method, params });
    setTimeout(() => {
      if (pending[id]) {
        delete pending[id];
        reject(new Error(`RPC timeout for ${method}`));
      }
    }, timeout);
  });
}

async function connect() {
  return new Promise((resolve, reject) => {
    socket = net.connect(GATEWAY_PORT, GATEWAY_HOST, () => {
      const key = crypto.randomBytes(16).toString('base64');
      const handshake = `GET / HTTP/1.1\r\n` +
        `Host: ${GATEWAY_HOST}:${GATEWAY_PORT}\r\n` +
        `Upgrade: websocket\r\n` +
        `Connection: Upgrade\r\n` +
        `Sec-WebSocket-Key: ${key}\r\n` +
        `Sec-WebSocket-Version: 13\r\n` +
        `\r\n`;
      socket.write(handshake);
    });

    let responseData = Buffer.alloc(0);
    socket.on('data', (chunk) => {
      responseData = Buffer.concat([responseData, chunk]);
      const str = responseData.toString();
      if (str.includes('\r\n\r\n')) {
        socket.removeAllListeners('data');
        socket.on('data', handleSocketData);
        connected = true;
        console.log(`[${new Date().toLocaleTimeString()}] WS connected, awaiting challenge...`);
        setTimeout(resolve, 500); // Wait for challenge
      }
    });
    socket.on('error', reject);
    socket.setTimeout(8000, () => { socket.destroy(); reject(new Error('Connect timeout')); });
  });
}

async function main() {
  const startTime = Date.now();
  console.log('=== INTEL v4.0 SPAWN TEST ===');
  console.log(`Start: ${new Date().toLocaleString()}`);

  await connect();
  
  // Wait for auth
  await new Promise(r => setTimeout(r, 1000));
  
  console.log('\n--- Exploring gateway ---');
  try {
    const status = await sendRPC('gateway.status', {});
    console.log('gateway.status:', JSON.stringify(status).substring(0, 300));
  } catch(e) {
    console.log('gateway.status failed:', e.message);
  }
  
  console.log('\n--- Spawning 12 intel agents ---');
  const spawnResults = [];
  for (let i = 1; i <= 12; i++) {
    const agentId = `intel_${String(i).padStart(2, '0')}`;
    const task = `读取 /workspace/agents/${agentId}/SOUL.md 并完整执行其搜索任务`;
    try {
      const result = await sendRPC('session.spawn', {
        agentId,
        task,
        runTimeoutSeconds: 500,
        mode: 'run',
        runtime: 'subagent'
      }, 15000);
      console.log(`✓ Spawned ${agentId}: ${JSON.stringify(result).substring(0, 100)}`);
      spawnResults.push({ agentId, status: 'spawned', result });
    } catch(e) {
      console.log(`✗ Spawn ${agentId} FAILED: ${e.message}`);
      spawnResults.push({ agentId, status: 'failed', error: e.message });
    }
  }
  
  const endTime = Date.now();
  const duration = (endTime - startTime) / 1000;
  console.log(`\nAll spawn requests sent in ${duration.toFixed(1)}s`);
  console.log('Summary:', spawnResults.map(a => `${a.agentId}:${a.status}`).join(', '));
  
  socket?.end();
}

main().catch(console.error);
