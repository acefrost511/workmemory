#!/usr/bin/env python3
"""正确创建cron：--agent info_officer（使用SOUL.md），不用--message"""
import subprocess, json
from datetime import datetime as dt

# 创建cron，用 --agent info_officer（不用--message）
# info_officer的SOUL.md已经包含正确的pipeline（intel 8分钟超时）
r = subprocess.run([
    'openclaw', 'cron', 'add',
    '--name', '情报官日报_每日05:00扫描',
    '--cron', '0 5 * * *',
    '--tz', 'Asia/Shanghai',
    '--session', 'isolated',
    '--agent', 'info_officer',
    '--timeout-seconds', '3600',
    '--announce',
    '--json'
], capture_output=True, text=True, timeout=20)

text = r.stdout
idx = text.find('{')
if idx < 0:
    print(f"❌ 创建失败! RC={r.returncode}")
    print(f"ERR: {r.stderr[:300]}")
    print(f"OUT: {text[:300]}")
else:
    try:
        d = json.loads(text[idx:])
        cid = d.get('id','?')
        nxt = d.get('state',{}).get('nextRunAtMs',0)
        ok = d.get('ok', False)
        print(f"RC={r.returncode} ok={ok}")
        print(f"ID: {cid}")
        print(f"Next: {dt.fromtimestamp(nxt/1000).strftime('%Y-%m-%d %H:%M')} CST" if nxt else "Next: 无")
        if ok:
            print("✅ cron创建成功！info_officer将在明天05:00自动运行pipeline")
        else:
            print("⚠️ 返回ok=false，检查输出:", text[:400])
    except Exception as e:
        print(f"JSON解析失败: {e}")
        print("OUT:", text[:400])
