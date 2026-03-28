#!/bin/bash
# 功能：检测今日素材库是否有新增，若有则标记触发
# 被触发后：IP归档团队会读取 .archive_trigger_pending 文件执行归档

TODAY=$(date +%Y-%m-%d)
MATERIAL_FILE="/workspace/knowledge/素材库/素材库_${TODAY}.md"
TRIGGER_FILE="/workspace/.archive_trigger_pending"
LOG_FILE="/workspace/logs/archive_trigger.log"

mkdir -p /workspace/logs

if [ -f "$MATERIAL_FILE" ]; then
    LINES=$(wc -l < "$MATERIAL_FILE")
    LAST_COUNT_FILE="/workspace/.last_archive_line_count"
    LAST_COUNT=$(cat "$LAST_COUNT_FILE" 2>/dev/null || echo "0")
    
    if [ "$LINES" -gt "$LAST_COUNT" ]; then
        echo "$LINES" > "$LAST_COUNT_FILE"
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        echo "${TIMESTAMP} 触发归档：今日素材库${LINES}行（上次${LAST_COUNT}行）" >> "$LOG_FILE"
        echo "${TIMESTAMP} 行数=${LINES}" >> "$TRIGGER_FILE"
        echo "✅ 归档触发标记已写入（行数：${LINES}）"
    else
        echo "今日素材库无新增，继续监控"
    fi
else
    echo "今日素材库文件不存在（${MATERIAL_FILE}）"
fi
