#!/usr/bin/env python3
"""重建情报官cron：使用session-key方式（正确！）"""
import subprocess, json, os
from datetime import datetime as dt

msg = open('/workspace/agents/info_officer/CRON_TASK_V3.txt').read()

# Step 1: 创建一个一次性的 info_officer session
print("【1/3】创建info_officer isolated session...")
r1 = subprocess.run([
    'openclaw', 'cron', 'add',
    '--name', '_temp_info_session',
    '--at', '+1h',
    '--session', 'isolated',
    '--agent', 'info_officer',
    '--timeout-seconds', '7200',
    '--no-deliver',
    '--json'
], capture_output=True, text=True, timeout=20)

# 提取session key
text1 = r1.stdout
idx1 = text1.find('{')
d1 = json.loads(text1[idx1:]) if idx1 >= 0 else {}
tmp_id = d1.get('id', '')
print(f"  临时cron ID: {tmp_id}")

# Step 2: 用 session-key + message 重建真正的cron
# 关键：--session-key 指定会话，--message 传递任务，两者不冲突
print("\n【2/3】用session-key创建真正的情报官cron...")
session_key = f'agent:info_officer:cron:{tmp_id}' if tmp_id else ''

r2 = subprocess.run([
    'openclaw', 'cron', 'add',
    '--name', '情报官日报_每日05:00扫描',
    '--cron', '0 5 * * *',
    '--tz', 'Asia/Shanghai',
    '--session', 'isolated',
    '--session-key', session_key,
    '--timeout-seconds', '3600',
    '--message', msg,
    '--announce',
    '--json'
], capture_output=True, text=True, timeout=25)

text2 = r2.stdout
idx2 = text2.find('{')
if idx2 < 0:
    print(f"  ❌ 创建失败! RC={r2.returncode}")
    print(f"  ERR: {r2.stderr[:200]}")
    # 备用：只用message
    print("\n  尝试备用方案（无session-key）...")
    r3 = subprocess.run([
        'openclaw', 'cron', 'add',
        '--name', '情报官日报_每日05:00扫描',
        '--cron', '0 5 * * *',
        '--tz', 'Asia/Shanghai',
        '--session', 'isolated',
        '--timeout-seconds', '3600',
        '--message', msg,
        '--announce',
        '--json'
    ], capture_output=True, text=True, timeout=25)
    text3 = r3.stdout
    idx3 = text3.find('{')
    if idx3 >= 0:
        d3 = json.loads(text3[idx3:])
        cid3 = d3.get('id','?')
        nxt3 = d3.get('state',{}).get('nextRunAtMs',0)
        print(f"  ✅ 备用cron创建成功! ID: {cid3}")
        print(f"     下次: {dt.fromtimestamp(nxt3/1000).strftime('%Y-%m-%d %H:%M')} CST")
    else:
        print(f"  备用也失败: {r3.stderr[:200]}")
else:
    d2 = json.loads(text2[idx2:])
    cid2 = d2.get('id','?')
    nxt2 = d2.get('state',{}).get('nextRunAtMs',0)
    print(f"  ✅ cron创建成功! ID: {cid2}")
    print(f"     Session: {session_key}")
    print(f"     下次: {dt.fromtimestamp(nxt2/1000).strftime('%Y-%m-%d %H:%M')} CST")

# Step 3: 删除临时cron
print("\n【3/3】清理临时cron...")
if tmp_id:
    subprocess.run(['openclaw', 'cron', 'remove', tmp_id], timeout=10)
    print(f"  ✓ 已删除临时cron")

print("\n完成!")
