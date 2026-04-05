#!/usr/bin/env python3
"""最终统计"""
import glob, os

files = glob.glob('/workspace/knowledge/原文库/*.md')
total = len(files)
with_abstract = 0
without_abstract = 0
with_status_ok = 0
with_status_fail = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if '## 摘要' in content:
        with_abstract += 1
        if '摘要状态**：✅' in content:
            with_status_ok += 1
        elif '摘要状态**：❌' in content:
            with_status_fail += 1
    else:
        without_abstract += 1

print("=== 最终统计 ===")
print(f"原文库总文件数: {total}")
print(f"已有 ## 摘要: {with_abstract}")
print(f"无 ## 摘要: {without_abstract}")
print(f"状态✅已补充: {with_status_ok}")
print(f"状态❌待补充: {with_status_fail}")

# List files still without abstracts
print("\nStill without abstracts:")
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if '## 摘要' not in content:
        print("  " + os.path.basename(f))
