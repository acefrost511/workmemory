#!/bin/bash
# intel_daily_scan.sh
# 情报官每日扫描脚本（小艾触发版）
# 使用方法：bash intel_daily_scan.sh

echo "=== 情报官每日扫描 $(date) ==="

# 1. spawn intel_01+intel_04+intel_07（第一批，3个并行）
echo "启动第一批搜索..."
sessions_spawn --runtime=subagent --agentId=intel_01 --task="..." --mode=run &
sessions_spawn --runtime=subagent --agentId=intel_04 --task="..." --mode=run &
sessions_spawn --runtime=subagent --agentId=intel_07 --task="..." --mode=run &
wait

# 2. 等待5分钟后启动第二批
sleep 300
echo "启动第二批搜索..."
sessions_spawn --runtime=subagent --agentId=intel_02 --task="..." --mode=run &
sessions_spawn --runtime=subagent --agentId=intel_05 --task="..." --mode=run &
sessions_spawn --runtime=subagent --agentId=intel_08 --task="..." --mode=run &
wait

# 3. 等待5分钟后启动第三批
sleep 300
echo "启动第三批搜索..."
sessions_spawn --runtime=subagent --agentId=intel_03 --task="..." --mode=run &
sessions_spawn --runtime=subagent --agentId=intel_06 --task="..." --mode=run &
sessions_spawn --runtime=subagent --agentId=intel_09 --task="..." --mode=run &
wait

# 4. 等待5分钟后启动第四批
sleep 300
echo "启动第四批搜索..."
sessions_spawn --runtime=subagent --agentId=intel_10 --task="..." --mode=run &
sessions_spawn --runtime=subagent --agentId=intel_11 --task="..." --mode=run &
sessions_spawn --runtime=subagent --agentId=intel_12 --task="..." --mode=run &
wait

echo "=== 12路搜索全部完成 ==="
