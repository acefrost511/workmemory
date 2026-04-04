#!/bin/bash
set -e
cd /workspace

echo "=== INTEL v4.0 PARALLEL SPAWN TEST ==="
echo "MASTER_START: $(date '+%Y-%m-%d %H:%M:%S')"
MASTER_START=$(date '+%s')

# Check if ws npm module exists
WS_PATH=$(find /app/openclaw/node_modules -maxdepth 1 -name "ws" -type d 2>/dev/null | head -1)
echo "WS module: $WS_PATH"

# Check for openclaw's internal RPC mechanism
ls /app/openclaw/dist/rpc 2>/dev/null || ls /app/openclaw/src/rpc 2>/dev/null | head -5 || echo "no rpc dir"

# Try spawning via cron add for agent intel_01 as test
echo "---"
echo "Testing cron spawn for intel_01..."
RESULT=$(openclaw cron add \
  --agent intel_01 \
  --message "读取 /workspace/agents/intel_01/SOUL.md 并完整执行其搜索任务" \
  --at "+1s" \
  --json 2>/dev/null | grep -v "Config" | grep -v "duplicate" | grep -v "ELIFECYCLE")
echo "Cron add result: $RESULT"

# Wait a moment for spawn
sleep 3

# Check if session was created
openclaw sessions --active 5 --agent intel_01 --json 2>/dev/null | grep -v "Config" | grep -v "duplicate" | grep -v "ELIFECYCLE" | head -20

MASTER_END=$(date '+%s')
echo "MASTER_END: $(date '+%Y-%m-%d %H:%M:%S')"
echo "TOTAL_DURATION: $((MASTER_END - MASTER_START))s"
