#!/bin/bash
# 工作区最终清理脚本 - 2026-03-30
cd /workspace

# 1. 清理旧日报
rm -f reports/daily/2026-03-10_*.md reports/daily/2026-03-10_*.html reports/daily/20260311_*.html
rm -f k12_ai_edu_newsletter_20260310*.html k12_ai_education_newsletter_wechat.html

# 2. 清理旧HTML日报
rm -f k12_ai_daily_20260310*.html k12_ai_daily_20260310*.json

# 3. 检查knowledge_wiki内容
if [ -f "knowledge_wiki/findings.md" ]; then
    lines=$(wc -l < "knowledge_wiki/findings.md")
    echo "knowledge_wiki/findings.md: ${lines}行"
fi

# 4. 统计各目录清理后状态
echo "=== 各目录清理后状态 ==="
for dir in extract knowledge memory reports agents scripts; do
    if [ -d "$dir" ]; then
        size=$(du -sh "$dir" 2>/dev/null | cut -f1)
        count=$(find "$dir" -type f 2>/dev/null | wc -l)
        echo "$size  $count个  $dir/"
    fi
done

# 5. 检查是否有超大文件（>10MB）
echo "=== 超大文件(>10MB) ==="
find . -type f -size +10M 2>/dev/null | while read f; do
    size=$(du -h "$f" | cut -f1)
    echo "$size  $f"
done

# 6. 检查extract/raw_content年龄分布
echo "=== extract/raw_content年龄分布 ==="
find extract/raw_content -type f -printf '%T+\n' 2>/dev/null | cut -d'+' -f1 | sort | uniq -c | sort

echo "=== 清理完成 ==="
