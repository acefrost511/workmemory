#!/bin/bash
echo "=== Spawn Intel Agents v4 Test ==="
echo "Start: $(date '+%Y-%m-%d %H:%M:%S')"
START_TS=$(date '+%s')

# List agents directory
echo "=== Agents dir ==="
ls /workspace/agents/ 2>&1 | head -20

echo "=== Intel_01 dir ==="
ls /workspace/agents/intel_01/ 2>&1 | head -10

echo "=== SOUL.md check ==="
head -5 /workspace/agents/intel_01/SOUL.md 2>&1 || echo "no SOUL.md"

echo "=== Gateway token check ==="
# Check for token in environment
env | grep -i "CLAW\|GATEWAY\|TOKEN" 2>&1 | head -5

echo "=== End time: $(date '+%Y-%m-%d %H:%M:%S') ==="
END_TS=$(date '+%s')
echo "Duration: $((END_TS - START_TS))s"
