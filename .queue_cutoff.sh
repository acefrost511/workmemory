#!/bin/bash
# 情报队列截止脚本
# 执行时间：每日06:30（北京时间）
# 功能：检查.pending/队列，决定是否停止当日dispatcher

QUEUE_DIR="/workspace/.pending"
FLAG_FILE="/workspace/.reviewer_dispatcher_off.txt"
DATE=$(date +%Y-%m-%d)

# 检查队列文件数量
if [ -d "$QUEUE_DIR" ]; then
    count=$(find "$QUEUE_DIR" -name "*.md" -not -name "*.reviewed*" | wc -l)
else
    count=0
fi

if [ $count -gt 0 ]; then
    echo "[$DATE 06:30] 队列仍有 ${count} 篇待审，标记超时，停止今日dispatcher"
    echo "待审超时-${DATE}-${count}篇" > "$FLAG_FILE"
    # 为pending文件加超时标记
    for f in "$QUEUE_DIR"/*.md; do
        [ -f "$f" ] && grep -q "\[待审\]" "$f" 2>/dev/null && \
            sed -i "s/\[待审\]/[待审-超时-${DATE}]/g" "$f" 2>/dev/null
    done
else
    echo "[$DATE 06:30] 队列已清空，无需操作"
    rm -f "$FLAG_FILE"
fi

# 无论队列空与否，本次都记录执行日志
echo "[$DATE 06:30] 队列截止检查完成，待审: ${count} 篇" >> /workspace/.queue_cutoff.log
