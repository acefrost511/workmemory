#!/usr/bin/env python3
"""最终方案：用--system-event触发主session → 主session spawn info_officer"""
import subprocess, json
from datetime import datetime as dt

msg = open('/workspace/agents/info_officer/CRON_TASK_V3.txt').read().strip()

# --system-event会被主session接收，主session收到后spawn info_officer
# 这样就绕过了--agent和--message的冲突
system_event = json.dumps({
    "type": "cron_trigger",
    "action": "spawn_info_officer",
    "task": msg,
    "reason": "情报官日报_每日05:00扫描"
})

r = subprocess.run([
    'openclaw', 'cron', 'add',
    '--name', '情报官日报_每日05:00扫描',
    '--cron', '0 5 * * *',
    '--tz', 'Asia/Shanghai',
    '--session', 'isolated',
    '--agent', 'info_officer',
    '--timeout-seconds', '3600',
    '--system-event', system_event,
    '--announce',
    '--json'
], capture_output=True, text=True, timeout=20)

text = r.stdout
idx = text.find('{')
if idx < 0:
    print(f"❌ RC={r.returncode}")
    print(f"ERR: {r.stderr[:300]}")
    print(f"OUT: {text[:200]}")
else:
    try:
        d = json.loads(text[idx:])
        print(f"RC={r.returncode} ok={d.get('ok',False)}")
        print(f"ID: {d.get('id','?')}")
        nxt = d.get('state',{}).get('nextRunAtMs',0)
        print(f"Next: {dt.fromtimestamp(nxt/1000).strftime('%Y-%m-%d %H:%M')} CST" if nxt else "Next: 无")
        print(f"State: {json.dumps(d.get('state',{}))[:100]}")
    except Exception as e:
        print(f"JSON ERR: {e}")
        print("OUT:", text[:400])
