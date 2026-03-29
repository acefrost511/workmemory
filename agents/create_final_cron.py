#!/usr/bin/env python3
"""创建最终版情报官日报cron（8分钟intel超时，60分钟总预算）"""
import subprocess, json, re
from datetime import datetime as dt

MSG = open('/workspace/agents/info_officer/CRON_TASK_V3.txt').read()

def run(args, **kw):
    r = subprocess.run(args, capture_output=True, text=True, **kw)
    return r

def get_json(r):
    text = r.stdout
    idx = text.find('{')
    if idx < 0:
        return None
    try:
        return json.loads(text[idx:])
    except:
        return None

# 1. 清理旧的"情报官"cron
print("→ 清理旧情报官cron...")
r = run(['openclaw', 'cron', 'list', '--json'], timeout=15)
d = get_json(r)
if d:
    old = [c for c in d.get('jobs',[]) if '情报官' in c.get('name','')]
    for c in old:
        cid = c['id']
        run(['openclaw', 'cron', 'remove', cid], timeout=10)
        print(f"  ✓ 删除旧cron: {cid[:8]}...")
    print(f"  共删除{len(old)}个")

# 2. 创建新的cron（用测试过的正确参数组合）
print("\n→ 创建新cron...")
args = [
    'openclaw', 'cron', 'add',
    '--name', '情报官日报_每日05:00扫描',
    '--cron', '0 5 * * *',
    '--tz', 'Asia/Shanghai',
    '--session', 'isolated',
    '--agent', 'info_officer',
    '--timeout-seconds', '3600',
    '--announce',
    '--json'
]
r = run(args, timeout=20)
d = get_json(r)
if d and d.get('id'):
    cid = d['id']
    nxt = d.get('state',{}).get('nextRunAtMs',0)
    print(f"  ✅ 创建成功!")
    print(f"     ID: {cid}")
    print(f"     预算: 3600秒 (60分钟)")
    if nxt:
        print(f"     下次: {dt.fromtimestamp(nxt/1000).strftime('%Y-%m-%d %H:%M:%S')} 北京时间")
    # 验证
    r2 = run(['openclaw', 'cron', 'list', '--json'], timeout=15)
    d2 = get_json(r2)
    info = [c for c in d2.get('jobs',[]) if cid in c.get('id','')]
    if info:
        c = info[0]
        print(f"     Agent: {c.get('agentId')}")
        print(f"     Session: {c.get('sessionTarget')}")
        print(f"     Status: {c.get('state',{}).get('status')}")
    print("\n  🎉 cron创建完成!")
else:
    print(f"  ❌ 创建失败!")
    print(f"  RC: {r.returncode}")
    print(f"  OUT: {r.stdout[:400]}")
    print(f"  ERR: {r.stderr[:200]}")
