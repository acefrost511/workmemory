#!/bin/bash
set -e
cd /workspace

echo "=== CRON CHECK ==="
openclaw cron list --json 2>/dev/null | grep -v "Config" | grep -v "duplicate" | grep -v "ELIFECYCLE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(json.dumps(data, indent=2, ensure_ascii=False))
except:
    print('parse failed')
    sys.stdin.seek(0)
    print(sys.stdin.read()[:500])
" 2>&1 | head -50

echo "---"
echo "CRON RUNS:"
openclaw cron runs --json 2>/dev/null | grep -v "Config" | grep -v "duplicate" | grep -v "ELIFECYCLE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(json.dumps(data[:3] if isinstance(data, list) else data, indent=2, ensure_ascii=False)[:500])
except:
    print('parse failed')
" 2>&1 | head -30

echo "---"
echo "ACTIVE SESSIONS:"
openclaw sessions --active 10 --all-agents --json 2>/dev/null | grep -v "Config" | grep -v "duplicate" | grep -v "ELIFECYCLE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    sessions = data if isinstance(data, list) else data.get('sessions', [])
    for s in sessions[-5:]:
        print(f\"  {s.get('label','?')} | {s.get('status','?')} | {s.get('runtime','?')} ago\")
except Exception as e:
    print(f'error: {e}')
" 2>&1 | head -20
