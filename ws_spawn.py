#!/usr/bin/env python3
"""
Connect to OpenClaw gateway WebSocket and spawn intel agents
"""
import json, threading, time, base64, hashlib, asyncio, http.client, urllib.request, urllib.error

HOST = '127.0.0.1'
PORT = 18789
TOKEN = 'minimax-agent'

class WsClient:
    def __init__(self):
        self.conn = http.client.HTTPConnection(HOST, PORT, timeout=10)
        self.ws = None
        self.msg_id = 1
        self.responses = {}
        self._lock = threading.Lock()
    
    def connect(self):
        """Establish WebSocket connection"""
        import websocket  # Need to find this
        
        # Check if websocket-client is available
        try:
            import importlib
            ws = importlib.import_module('websocket')
            self._use_websocket = True
        except ImportError:
            # Use built-in http.client for WebSocket
            self._use_websocket = False
            return self._ws_connect_manual()
    
    def _ws_connect_manual(self):
        """Manual WebSocket handshake"""
        key = base64.b64encode(b'randomkey12345678').decode()
        headers = [
            f'GET /api/v1 HTTP/1.1',
            f'Host: {HOST}:{PORT}',
            'Upgrade: websocket',
            'Connection: Upgrade',
            f'Sec-WebSocket-Key: {key}',
            'Sec-WebSocket-Version: 13',
            f'X-API-Key: {TOKEN}',
            '',
            '',
        ]
        # This is complex - let's use a different approach
        pass

    def call(self, method, params=None):
        """Make a JSON-RPC call over WebSocket"""
        msg_id = self.msg_id
        self.msg_id += 1
        
        # Use Node.js for WebSocket - it has 'ws' package
        script = f"""
const {{ WebSocket }} = require('ws');
const ws = new WebSocket('ws://{HOST}:{PORT}/api/v1', {{
    headers: {{ 'X-API-Key': '{TOKEN}' }}
}});

let msgId = {self.msg_id - 1};
let resolved = false;

ws.on('open', () => {{
    const req = {{
        jsonrpc: '2.0',
        id: msgId,
        method: '{method}',
        params: {json.dumps(params or {{}})}
    }};
    console.log('SENDING:', JSON.stringify(req));
    ws.send(JSON.stringify(req));
}});

ws.on('message', (data) => {{
    if (resolved) return;
    try {{
        const resp = JSON.parse(data.toString());
        console.log('GOT:', JSON.stringify(resp));
        resolved = true;
        ws.close();
        process.exit(0);
    }} catch(e) {{
        console.log('RAW:', data.toString().slice(0, 500));
    }}
}});

ws.on('error', (e) => {{
    console.error('WS ERROR:', e.message);
    resolved = true;
    process.exit(1);
}});

setTimeout(() => {{ 
    if (!resolved) {{ 
        console.log('TIMEOUT'); 
        ws.close(); 
        process.exit(1);
    }}
}}, 10000);
"""
        import subprocess
        result = subprocess.run(['node', '-e', script], capture_output=True, text=True, timeout=15)
        return result.stdout, result.stderr

# Try using the ws package from openclaw
import os, glob

# Find ws package
ws_paths = glob.glob('/app/openclaw/node_modules/ws/**/*.js', recursive=True)
print(f"Found {len(ws_paths)} ws files")
if ws_paths:
    print("First few:", ws_paths[:3])

# Use node directly
script_v2 = """
const wsPath = require.resolve('/app/openclaw/node_modules/ws');
console.log('ws found at:', wsPath);
"""

result = subprocess.run(['node', '-e', script_v2], capture_output=True, text=True, timeout=5)
print("WS resolution:", result.stdout, result.stderr)

# Now run the actual spawn call
spawn_script = """
const WebSocket = require('/app/openclaw/node_modules/ws');

const ws = new WebSocket('ws://127.0.0.1:18789/api/v1', {
    headers: { 'X-API-Key': 'minimax-agent' }
});

let resolved = false;
const msgId = Date.now();

ws.on('open', () => {
    console.error('WS OPENED');
    const req = {
        jsonrpc: '2.0',
        id: msgId,
        method: 'sessions_spawn',
        params: {
            task: 'test subagent spawn',
            runtime: 'subagent',
            runTimeoutSeconds: 60,
            mode: 'run'
        }
    };
    console.error('SENDING:', JSON.stringify(req));
    ws.send(JSON.stringify(req));
});

ws.on('message', (data) => {
    if (resolved) return;
    try {
        const resp = JSON.parse(data.toString());
        console.log(JSON.stringify(resp));
        resolved = true;
    } catch(e) {
        console.error('RAW MSG:', data.toString().slice(0, 300));
    }
    ws.close();
});

ws.on('error', (e) => {
    console.error('WS ERROR:', e.message);
    ws.close();
});

setTimeout(() => {
    if (!resolved) {
        console.error('TIMEOUT');
        ws.close();
    }
    process.exit(0);
}, 15000);
"""

result2 = subprocess.run(['node', '-e', spawn_script], capture_output=True, text=True, timeout=20)
print("STDOUT:", result2.stdout[:500])
print("STDERR:", result2.stderr[:500])
