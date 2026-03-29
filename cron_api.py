#!/usr/bin/env python3
"""通过OpenClaw Gateway API直接创建cron（绕过CLI payload冲突）"""
import subprocess, json, time
from datetime import datetime as dt

# Step 1: 通过Gateway config获取当前cron列表（包含完整字段）
r = subprocess.run(['openclaw', 'cron', 'list', '--json'], capture_output=True, text=True, timeout=15)
text = r.stdout[idx if (idx := text.find('{')) >= 0 else 0:]
crons = json.loads(text).get('jobs', [])
info_crons = [c for c in crons if '情报官' in c.get('name','')]
print(f"现有情报官cron: {[c['id'][:8] for c in info_crons]}")

# Step 2: 通过sessions_spawn API创建info_officer persistent session用于明天pipeline
print("\n通过sessions_spawn创建持久化info_officer session...")
r2 = subprocess.run([
    'openclaw', 'sessions', 'spawn',
    '--runtime', 'acp',
    '--agent', 'info_officer',
    '--mode', 'session',
    '--timeout', '7200000',
    '--json'
], capture_output=True, text=True, timeout=30)
print(f"sessions spawn RC: {r2.returncode}")
print(f"OUT: {r2.stdout[:300]}")

# Step 3: 用sessions_spawn返回的session key作为cron的session-key
text2 = r2.stdout
idx2 = text2.find('{')
if idx2 >= 0:
    try:
        d2 = json.loads(text2[idx2:])
        sess_key = d2.get('sessionKey', d2.get('key', ''))
        print(f"Session Key: {sess_key}")
    except:
        sess_key = ''
        print("无法解析session key")
else:
    sess_key = ''
    print(f"sessions spawn失败: {r2.stderr[:200]}")

# Step 4: 用session-key创建cron（--session isolated会使用指定的session）
if sess_key:
    msg = open('/workspace/agents/info_officer/CRON_TASK_V3.txt').read().strip()
    print(f"\n使用session-key={sess_key[:30]}...创建cron")
    r3 = subprocess.run([
        'openclaw', 'cron', 'add',
        '--name', '情报官日报_每日05:00扫描_final',
        '--cron', '0 5 * * *',
        '--tz', 'Asia/Shanghai',
        '--session', 'isolated',
        '--session-key', sess_key,
        '--timeout-seconds', '3600',
        '--message', msg,
        '--announce',
        '--json'
    ], capture_output=True, text=True, timeout=20)
    print(f"cron RC: {r3.returncode}")
    text3 = r3.stdout
    idx3 = text3.find('{')
    if idx3 >= 0:
        try:
            d3 = json.loads(text3[idx3:])
            print(f"✅ cron创建: {d3.get('id','?')[:8]}... OK={d3.get('ok',False)}")
        except Exception as e:
            print(f"JSON err: {e}, OUT: {text3[:400]}")
    else:
        print(f"cron失败: {r3.stderr[:200]}")
        print(f"OUT: {text3[:300]}")
else:
    print("跳过cron创建（无session key）")
