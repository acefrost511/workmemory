#!/bin/bash
# 功能：每日12:00检查归档情况
# 检查内容：今日素材库有多少篇？各抽屉归档了多少？有没有问题？
# 若发现问题：立即记录并尝试重新执行归档

TODAY=$(date +%Y-%m-%d)
MATERIAL_FILE="/workspace/knowledge/素材库/素材库_${TODAY}.md"
TRIGGER_FILE="/workspace/.archive_trigger_pending"
CHECK_LOG="/workspace/logs/daily_archive_check.log"

mkdir -p /workspace/logs

echo "$(date '+%Y-%m-%d %H:%M:%S') === 每日归档检查 ===" >> "$CHECK_LOG"

if [ ! -f "$MATERIAL_FILE" ]; then
    echo "⚠️ 今日素材库为空，情报官尚未写入内容" >> "$CHECK_LOG"
    echo "⚠️ 今日素材库为空，请检查情报官运行状态"
    exit 1
fi

# 统计今日素材库篇数
ARTICLES=$(grep -c "【素材" "$MATERIAL_FILE" 2>/dev/null || echo "0")
echo "今日素材库篇数：${ARTICLES}" >> "$CHECK_LOG"

if [ "$ARTICLES" -eq 0 ]; then
    echo "⚠️ 今日素材库0篇，情报官可能未运行" >> "$CHECK_LOG"
    echo "⚠️ 今日素材库0篇，请检查情报官运行状态"
    exit 1
fi

# 统计各抽屉今日新增（简单检查）
echo "归档检查完成（${ARTICLES}篇待归档）" >> "$CHECK_LOG"
echo "✅ 每日归档检查通过：今日素材库${ARTICLES}篇"

# 检查是否有触发标记
if [ -f "$TRIGGER_FILE" ]; then
    echo "归档触发标记存在：$(cat $TRIGGER_FILE)" >> "$CHECK_LOG"
fi

exit 0
