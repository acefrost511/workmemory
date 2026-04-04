#!/usr/bin/env python3
"""Spawn 12 intel agents via OpenClaw gateway RPC."""
import json
import time
import asyncio
import websockets
import sys

GATEWAY_URL = "ws://127.0.0.1:18789"
TOKEN = "minimax-agent"

async def spawn_all_agents():
    print(f"[{time.strftime('%H:%M:%S')}] Starting 12 intel agent spawns...")
    spawn_tasks = []
    
    async with websockets.connect(f"{GATEWAY_URL}?token={TOKEN}") as ws:
        msg_id = 0
        
        async def send_rpc(method, params=None):
            nonlocal msg_id
            msg_id += 1
            msg = {"jsonrpc": "2.0", "id": msg_id, "method": method, "params": params or {}}
            await ws.send(json.dumps(msg))
            resp = await ws.recv()
            return json.loads(resp)
        
        # Test connection
        await send_rpc("status")
        print(f"[{time.strftime('%H:%M:%S')}] Gateway connected.")
        
        # Spawn all 12 agents
        for i in range(1, 13):
            agent_id = f"intel_{i:02d}"
            msg_id += 1
            task = f"读取 /workspace/agents/{agent_id}/SOUL.md 并完整执行其搜索任务"
            msg = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "method": "session.spawn",
                "params": {
                    "agentId": agent_id,
                    "task": task,
                    "runTimeoutSeconds": 500,
                    "mode": "run",
                    "runtime": "subagent"
                }
            }
            await ws.send(json.dumps(msg))
            resp = await ws.recv()
            result = json.loads(resp)
            print(f"[{time.strftime('%H:%M:%S')}] Spawned {agent_id}: {result.get('result', result.get('error', 'unknown'))[:100]}")
        
        print(f"[{time.strftime('%H:%M:%S')}] All spawn requests sent.")

if __name__ == "__main__":
    try:
        import websockets
        asyncio.run(spawn_all_agents())
    except ImportError:
        print("websockets not available, trying ws-cli approach...")
        sys.exit(1)
