#!/usr/bin/env python3
import subprocess, json, sys, os
from datetime import datetime as dt

MSG = open('/workspace/agents/info_officer/CRON_TASK_V3.txt').read()

# Test 1: --session isolated + --agent info_officer + --message (our main attempt)
print("测试A: --session isolated + --agent + --message")
r = subprocess.run([
    'openclaw', 'cron', 'add',
    '--name', 'testA',
    '--cron', '0 5 * * *',
    '--tz', 'Asia/Shanghai',
    '--session', 'isolated',
    '--agent', 'info_officer',
    '--timeout-seconds', '3600',
    '--message', MSG,
    '--json'
], capture_output=True, text=True, timeout=15)
print(f"RC={r.returncode} OUT={r.stdout[:100]}")
if r.returncode != 0:
    print("STDERR:", r.stderr[:200])

# Test 2: --session isolated + --message (no --agent)
print("\n测试B: --session isolated + --message (no --agent)")
r2 = subprocess.run([
    'openclaw', 'cron', 'add',
    '--name', 'testB',
    '--cron', '0 5 * * *',
    '--tz', 'Asia/Shanghai',
    '--session', 'isolated',
    '--timeout-seconds', '3600',
    '--message', MSG,
    '--json'
], capture_output=True, text=True, timeout=15)
print(f"RC={r2.returncode} OUT={r2.stdout[:100]}")
if r2.returncode != 0:
    print("STDERR:", r2.stderr[:200])
