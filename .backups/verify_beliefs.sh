#!/bin/bash
# 信念抽屉写后验证脚本
# 每次写入抽屉文件后，运行此脚本验证完整性

TARGET_DIR="/workspace/knowledge/beliefs"
LOG="/workspace/.backups/write_verify.log"

echo "[$(date '+%H:%M:%S')] 开始验证..." >> "$LOG"

PROBLEM_FILES=""

for f in "$TARGET_DIR"/*.md; do
  LINES=$(wc -l < "$f")
  if [ "$LINES" -lt 20 ]; then
    PROBLEM_FILES="$PROBLEM_FILES\n$(basename $f): ${LINES}行 ⚠️"
  fi
done

if [ -z "$PROBLEM_FILES" ]; then
  echo "[$(date '+%H:%M:%S')] ✅ 验证通过，所有抽屉完整" >> "$LOG"
  echo "✅ 验证通过"
else
  echo "[$(date '+%H:%M:%S')] ⚠️ 发现问题文件:$PROBLEM_FILES" >> "$LOG"
  echo -e "⚠️ 发现问题文件:$PROBLEM_FILES"
fi

# 输出抽屉行数统计
echo "--- 抽屉行数 ---" >> "$LOG"
wc -l "$TARGET_DIR"/*.md >> "$LOG"
wc -l "$TARGET_DIR"/*.md
