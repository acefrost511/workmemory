#!/usr/bin/env node
/**
 * Spawn 12 intel agents via OpenClaw gateway WebSocket RPC
 */
const net = require('net');
const crypto = require('crypto');

const GATEWAY_HOST = '127.0.0.1';
const GATEWAY_PORT = 18789;
const TOKEN = 'minimax-agent';

let socket;
let msgId = 0;
let pending = {};
let connected = false;

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
    header[1] = 0x7e; // 126
    header.writeUInt16BE(len, 2);
  }
  return Buffer.concat([header, payload]);
}

function wsDecode(buffer) {
  // Simple WebSocket frame decoder
  const firstByte = buffer[0];
  const secondByte = buffer[1];
  const opcode = firstByte & 0x0f;
  const masked = (secondByte & 0x80) !== 0;
  let offset = 2;
  let payloadLen = secondByte & 0x7f;
  if (payloadLen === 126) {
    payloadLen = buffer.readUInt16BE(2);
    offset = 4;
  } else if (payloadLen === 127) {
    offset = 10;
    payloadLen = Number(buffer.readBigUInt64BE(2));
  }
  let maskKey = null;
  if (masked) {
    maskKey = buffer.slice(offset, offset + 4);
    offset += 4;
  }
  let payload = buffer.slice(offset, offset + payloadLen);
  if (masked && maskKey) {
    payload = wsMask(payload, maskKey);
  }
  return JSON.parse(payload.toString());
}

function connect() {
  return new Promise((resolve, reject) => {
    socket = net.connect(GATEWAY_PORT, GATEWAY_HOST, () => {
      const key = crypto.randomBytes(16).toString('base64');
      const handshake = `GET / HTTP/1.1\r\n` +
        `Host: ${GATEWAY_HOST}:${GATEWAY_PORT}\r\n` +
        `Upgrade: websocket\r\n` +
        `Connection: Upgrade\r\n` +
        `Sec-WebSocket-Key: ${key}\r\n` +
        `Sec-WebSocket-Version: 13\r\n` +
        `Authorization: Bearer ${TOKEN}\r\n` +
        `\r\n`;
      socket.write(handshake);
    });

    let responseData = Buffer.alloc(0);
    
    socket.on('data', (chunk) => {
      responseData = Buffer.concat([responseData, chunk]);
      const str = responseData.toString();
      if (str.includes('\r\n\r\n')) {
        // Got complete HTTP response
        socket.removeAllListeners('data');
        socket.on('data', handleSocketData);
        connected = true;
        console.log(`[${new Date().toLocaleTimeString()}] Gateway WebSocket connected`);
        resolve();
      }
    });

    socket.on('error', (err) => {
      console.error('Socket error:', err.message);
      reject(err);
    });

    socket.setTimeout(5000, () => {
      socket.destroy();
      reject(new Error('Connection timeout'));
    });
  });
}

let receiveBuffer = Buffer.alloc(0);

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
      // Close frame
      console.log('Gateway closed connection');
      socket.end();
      return;
    }
    if (opcode === 0x1 || opcode === 0x2) {
      // Text or binary frame
      try {
        const data = wsDecode(frame);
        handleMessage(data);
      } catch (e) {
        console.error('Decode error:', e.message);
      }
    }
  }
}

function handleMessage(msg) {
  if (msg.id && pending[msg.id]) {
    const resolve = pending[msg.id];
    delete pending[msg.id];
    resolve(msg.result || msg.error);
  } else {
    console.log('UNSOLICITED:', JSON.stringify(msg).substring(0, 200));
  }
}

function sendRPC(method, params) {
  return new Promise((resolve, reject) => {
    const id = ++msgId;
    pending[id] = resolve;
    const frame = wsEncode({ jsonrpc: '2.0', id, method, params });
    socket.write(frame);
    // Timeout
    setTimeout(() => {
      if (pending[id]) {
        delete pending[id];
        reject(new Error(`RPC timeout for ${method}`));
      }
    }, 30000);
  });
}

async function main() {
  const startTime = Date.now();
  console.log('=== INTEL v4.0 SPAWN TEST ===');
  console.log(`Start: ${new Date().toLocaleString()}`);

  try {
    await connect();
    
    // First, let's explore available methods
    console.log('\n--- Exploring gateway ---');
    try {
      const status = await sendRPC('gateway.status', {});
      console.log('Gateway status:', JSON.stringify(status).substring(0, 200));
    } catch(e) {
      console.log('gateway.status failed:', e.message);
    }
    
    try {
      const list = await sendRPC('agent.list', {});
      console.log('Agent list:', JSON.stringify(list).substring(0, 300));
    } catch(e) {
      console.log('agent.list failed:', e.message);
    }

    // Try spawning
    console.log('\n--- Spawning agents ---');
    const agents = [];
    for (let i = 1; i <= 12; i++) {
      const agentId = `intel_${String(i).padStart(2, '0')}`;
      try {
        const result = await sendRPC('session.spawn', {
          agentId,
          task: `读取 /workspace/agents/${agentId}/SOUL.md 并完整执行其搜索任务`,
          runTimeoutSeconds: 500,
          mode: 'run',
          runtime: 'subagent'
        });
        console.log(`Spawned ${agentId}:`, JSON.stringify(result).substring(0, 100));
        agents.push({ agentId, result });
      } catch(e) {
        console.log(`Spawn ${agentId} FAILED:`, e.message);
        agents.push({ agentId, error: e.message });
      }
    }
    
    const endTime = Date.now();
    console.log(`\nAll spawns completed: ${(endTime - startTime)/1000}s`);
    console.log('Summary:', agents.map(a => `${a.agentId}: ${a.error ? 'FAIL' : 'OK'}`).join(', '));
    
  } catch(err) {
    console.error('Fatal error:', err);
  }
  
  socket?.end();
}

main().catch(console.error);
