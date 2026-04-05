#!/usr/bin/env python3
"""处理最后剩余的20个文件"""
import glob, os, re

files = glob.glob('/workspace/knowledge/原文库/*.md')
todo = []
for f in files:
    name = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if '## 摘要\n' not in content and '**摘要状态**：✅' not in content:
        todo.append((name, content, f))

print(f"Files remaining: {len(todo)}")
for name, content, _ in todo:
    print(f"  {name}")
