#!/usr/bin/env python3
"""检查原文库摘要状态"""
from pathlib import Path
import re

lib = Path("/workspace/knowledge/原文库")
files = list(lib.glob("*.md"))

has_abstract = 0
no_abstract = 0
has_meta = 0  # 有"摘要状态"标记的

examples_good = []
examples_bad = []

for f in files:
    c = f.read_text(errors="ignore")
    # 新版格式：有"## 摘要"或"摘要状态"
    if "## 摘要" in c or ("摘要" in c and len(c) > 2000):
        has_abstract += 1
        if len(examples_good) < 3:
            examples_good.append(f.name)
    elif "摘要状态" in c:
        has_abstract += 1
        if len(examples_good) < 3:
            examples_good.append(f.name + " [有摘要状态标记]")
    else:
        no_abstract += 1
        if len(examples_bad) < 5:
            # 读取文件前100字看是什么内容
            examples_bad.append((f.name, c[:150]))

total = len(files)
print(f"总文件: {total}")
print(f"有摘要: {has_abstract} ({100*has_abstract//total if total else 0}%)")
print(f"无摘要: {no_abstract} ({100*no_abstract//total if total else 0}%)")
print()
print("=== 有摘要样例 ===")
for n in examples_good: print(f"  {n}")
print()
print("=== 无摘要样例（前5）===")
for n, snippet in examples_bad:
    print(f"  {n}:")
    print(f"  {snippet[:100]}")
    print()
