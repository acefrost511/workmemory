#!/usr/bin/env python3
import subprocess
import json
import sys
import re

def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r

# 1. 检查现有cron
r = run(['openclaw', 'cron', 'list', '--json'])
# 提取JSON（跳过banner）
text = r.stdout
idx = text.find('{')
if idx >= 0:
    text = text[idx:]
else:
    print("无JSON输出:", r.stdout[:200])
    sys.exit(1)

try:
    data = json.loads(text)
    crons = data.get('jobs', [])
    info_crons = [c for c in crons if '情报官' in c.get('name','')]
    print(f"现有情报官cron: {len(info_crons)}个")
    for c in info_crons:
        print(f"  {c.get('id','?')} | {c.get('name')} | status={c.get('state',{}).get('status')} | next={c.get('state',{}).get('nextRunAtMs','?')}")
except Exception as e:
    print(f"解析失败: {e}")
    print("原始输出:", text[:500])
    sys.exit(1)

# 2. 读取任务消息
with open('/workspace/agents/info_officer/CRON_TASK_V3.txt') as f:
    msg = f.read()

# 3. 删除已有的情报官cron
for c in info_crons:
    cid = c.get('id')
    if cid:
        print(f"\n删除旧cron: {cid}")
        run(['openclaw', 'cron', 'remove', cid])
        print("  已删除")

# 4. 创建新cron
print("\n创建新的情报官cron（8分钟intel超时，60分钟总预算）...")
r = run(['openclaw', 'cron', 'add',
    '--name', '情报官日报_每日05:00扫描v3',
    '--cron', '0 5 * * *',
    '--tz', 'Asia/Shanghai',
    '--session', 'isolated',
    '--agent', 'info_officer',
    '--timeout-seconds', '3600',
    '--announce',
    '--json'])

idx = r.stdout.find('{')
if idx < 0:
    print("创建失败，无JSON:", r.stdout[:300])
    sys.exit(1)

try:
    d = json.loads(r.stdout[idx:])
    cid = d.get('id','?')
    nxt = d.get('state',{}).get('nextRunAtMs','?')
    print(f"✓ 创建成功! ID: {cid}")
    print(f"  下次运行时间戳: {nxt}")
    if nxt:
        from datetime import datetime
        dt = datetime.fromtimestamp(nxt/1000)
        print(f"  = {dt.strftime('%Y-%m-%d %H:%M:%S')} 北京时间")
    print("\n完成!")
except Exception as e:
    print(f"解析失败: {e}")
    print("输出:", r.stdout[:500])
