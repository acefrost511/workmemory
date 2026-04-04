#!/bin/bash
# Try to call gateway RPC via HTTP (gateway may have HTTP upgrade endpoint)
# Gateway is on port 8080

GATEWAY_URL="http://localhost:8080"

spawn_agent() {
  local agent_id=$1
  local task_encoded=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.stdin.read()))" << EOF
读取 /workspace/agents/${agent_id}/SOUL.md 并完整执行其搜索任务
EOF
)
  
  echo "Attempting to spawn $agent_id..."
  
  # Try HTTP POST to gateway
  curl -s -X POST "$GATEWAY_URL/rpc" \
    -H "Content-Type: application/json" \
    -d "{\"method\":\"sessions_spawn\",\"params\":{\"task\":\"读取 /workspace/agents/${agent_id}/SOUL.md 并完整执行其搜索任务\",\"runtime\":\"subagent\",\"agentId\":\"${agent_id}\",\"runTimeoutSeconds\":500,\"mode\":\"run\"}}" \
    --max-time 10 2>&1 | head -200 || echo "HTTP call failed for $agent_id"
}

for i in $(seq -w 1 12); do
  agent_id="intel_$i"
  spawn_agent "$agent_id" &
done

wait
echo "All spawn attempts completed."
