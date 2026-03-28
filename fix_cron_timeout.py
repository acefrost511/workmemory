#!/usr/bin/env python3
import json, shutil, sys

path = '/root/.openclaw/cron/jobs.json'
shutil.copy(path, path + '.bak3')

with open(path) as f:
    data = json.load(f)

targets = {
    'c1d720e3-0373-4fb0-804f-b9104e5273d4': 270,
    '6324f287-baa7-4ca5-b8b2-4dd62dbe012f': 2250,
    '0bef52ae-ce66-4f65-a266-fd4ae8ed94e7': 1800,
}

changed = []
for job in data['jobs']:
    if job['id'] in targets and 'payload' in job:
        old = job['payload'].get('timeoutSeconds', 'N/A')
        new = targets[job['id']]
        if str(old) != str(new):
            job['payload']['timeoutSeconds'] = new
            changed.append((job['name'], old, new))
            print(f'CHANGED: {job["name"]}: timeout {old}s -> {new}s')
        else:
            print(f'SKIP: {job["name"]}: already {new}s')

with open(path, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Done. {len(changed)} jobs updated.')
for name, old, new in changed:
    print(f'  - {name}: {old}s -> {new}s')
