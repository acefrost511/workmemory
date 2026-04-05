#!/usr/bin/env python3
"""检查剩余文件"""
import glob, os, re

files = glob.glob('/workspace/knowledge/原文库/*.md')
todo = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if '## 摘要' not in content:
        todo += 1

print(f"Files still needing abstracts: {todo}")
