#!/usr/bin/env python3
"""使用Python列表传参（已验证work）创建cron"""
import subprocess, json, os
from datetime import datetime as dt

msg = open('/workspace/agents/info_officer/CRON_TASK_V3.txt').read()

# 分开stdout和stderr
r = subprocess.run([
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

# 从stdout提取JSON（跳过banner行）
lines = r.stdout.split('\n')
json_line = None
for i, line in enumerate(lines):
    if line.strip().startswith('{'):
        json_line = '\n'.join(lines[i:])
        break

if json_line:
    try:
        d = json.loads(json_line)
        cid = d.get('id', '?')
        nxt = d.get('state', {}).get('nextRunAtMs', 0)
        status = d.get('state', {}).get('status', '?')
        print(f"RC={r.returncode}")
        print(f"ID: {cid}")
        print(f"Status: {status}")
        print(f"Next: {nxt}")
        if nxt:
            print(f"Time: {dt.fromtimestamp(nxt/1000).strftime('%Y-%m-%d %H:%M:%S')} CST")
    except Exception as e:
        print(f"JSON解析失败: {e}")
        print("JSON内容:", json_line[:300])
else:
    print(f"RC={r.returncode}")
    print("NO JSON FOUND")
    print("STDOUT:", r.stdout[:500])
    print("STDERR:", r.stderr[:300])
