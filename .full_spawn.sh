#!/bin/bash
set -e
echo "=== INTEL AGENTS v4.0 SPAWN TEST ==="
echo "Start: $(date '+%Y-%m-%d %H:%M:%S')"
START_TS=$(date '+%s')

# Get cron add help
openclaw cron add --help 2>/dev/null | grep -v "Config" | grep -v "duplicate" | grep -v "ELIFECYCLE" | grep -v "^$" | head -30

echo "---"
echo "Checking if agents have valid SOUL.md files..."
for i in $(seq -w 1 12); do
  f="/workspace/agents/intel_$i/SOUL.md"
  if [ -f "$f" ]; then
    lines=$(wc -l < "$f")
    echo "intel_$i: EXISTS ($lines lines)"
  else
    echo "intel_$i: MISSING"
  fi
done

echo "---"
echo "Checking gateway connectivity..."
curl -s --max-time 3 -H "Authorization: Bearer minimax-agent" "http://127.0.0.1:18789/" 2>&1 | head -3

echo "---"
END_TS=$(date '+%s')
echo "Duration: $((END_TS - START_TS))s"
echo "End: $(date '+%Y-%m-%d %H:%M:%S')"
