#!/usr/bin/env python3
import subprocess, json

result = subprocess.run(['openclaw', 'cron', 'list', '--json'], capture_output=True, text=True)
lines = result.stdout.split('\n')

json_start = -1
for i, l in enumerate(lines):
    stripped = l.strip()
    if stripped.startswith('{') and ('jobs' in stripped or '"id"' in stripped):
        json_start = i
        break
    elif stripped.startswith('{'):
        json_start = i
        break

json_text = '\n'.join(lines[json_start:])
data = json.loads(json_text)
jobs = data['jobs']

# Print detailed info for idle/unusual tasks
for j in jobs:
    s = j.get('state', {})
    ce = s.get('consecutiveErrors', 0)
    ls = s.get('lastStatus', 'NO_STATE')
    tid = j.get('id', '?')[:12]
    name = j.get('name', '?')
    
    if ls == 'NO_STATE' or ce >= 3:
        print(f"\n=== Task: {name} [{tid}] ===")
        print(f"  enabled: {j.get('enabled')}")
        print(f"  schedule: {j.get('schedule')}")
        print(f"  state: {json.dumps(s, indent=2)}")
        print(f"  delivery: {json.dumps(j.get('delivery',{}), indent=2)}")
        print(f"  payload timeout: {j.get('payload',{}).get('timeoutSeconds')}")
