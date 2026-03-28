#!/usr/bin/env python3
import json, sys

job_id = sys.argv[1]
new_mode = sys.argv[2] if len(sys.argv) > 2 else 'none'

with open('/root/.openclaw/cron/jobs.json', 'r') as f:
    data = json.load(f)

found = False
for job in data['jobs']:
    if job['id'] == job_id:
        old_mode = job['delivery'].get('mode', 'none')
        job['delivery']['mode'] = new_mode
        print(f"Updated job '{job['name']}' ({job_id})")
        print(f"  Delivery mode: {old_mode} -> {new_mode}")
        print(f"  Consecutive errors: {job['state'].get('consecutiveErrors', 0)}")
        print(f"  Last delivery error: {job['state'].get('lastDeliveryError', 'none')}")
        found = True
        break

if found:
    with open('/root/.openclaw/cron/jobs.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("File saved successfully.")
else:
    print(f"Job {job_id} not found.")
    sys.exit(1)
