#!/usr/bin/env python3
import subprocess, json

result = subprocess.run(['openclaw', 'cron', 'list', '--json'], capture_output=True, text=True)
lines = result.stdout.split('\n')

# find JSON start
json_start = -1
for i, l in enumerate(lines):
    stripped = l.strip()
    if stripped.startswith('{') and ('jobs' in stripped or '"id"' in stripped):
        json_start = i
        break
    elif stripped.startswith('{'):
        json_start = i
        break

if json_start == -1:
    print("Could not find JSON start")
    exit(1)

json_text = '\n'.join(lines[json_start:])
data = json.loads(json_text)
jobs = data['jobs']

print(f"总任务数: {len(jobs)}")
print()
print(f"{'#错':>4} | {'lastStatus':6} | {'lastRun':6} | {'delivery':14} | {'enabled':7} | name")
print("-" * 120)

active_ok = 0
active_warn = 0
active_fail = 0
idle_count = 0

for j in jobs:
    s = j.get('state', {})
    ce = s.get('consecutiveErrors', 0)
    ls = s.get('lastStatus', '?')
    lrs = s.get('lastRunStatus', '?')
    lds = s.get('lastDeliveryStatus', '?')
    name = j.get('name', '?')[:45]
    tid = j.get('id', '?')[:12]
    enabled = j.get('enabled', True)
    
    if not enabled:
        continue
    
    if ls in ('ok', 'running'):
        active_ok += 1
    elif ce >= 3:
        active_warn += 1
    else:
        active_fail += 1
    
    if ls == 'idle':
        idle_count += 1
    
    marker = "⚠️" if ce >= 3 else "  "
    print(f'{marker}[{ce:2}错] {str(ls):6} | {str(lrs):6} | {str(lds):14} | enabled={enabled} | {name}')

print()
print(f"活跃任务总数: {len(jobs)}")
print(f"正常(ok/running): {active_ok}")
print(f"警告(consecutiveErrors>=3): {active_warn}")
print(f"失败/异常: {active_fail}")
print(f"idle任务: {idle_count}")
