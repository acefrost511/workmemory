#!/usr/bin/env python3
"""检查剩余文件并分类"""
import glob, os, re

files = glob.glob('/workspace/knowledge/原文库/*.md')
todo_files = []

for f in files:
    name = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if '## 摘要' not in content and '## 摘要\n' not in content:
        # Check type
        has_doi = bool(re.search(r'10\.\d{4,}/[\w\.\-\+/]+', content))
        has_arxiv = 'arxiv' in name.lower()
        if has_doi:
            dois = re.findall(r'10\.\d{4,}/[\w\.\-\+/]+', content)
            todo_files.append(('DOI', dois[0] if dois else '', name))
        elif has_arxiv:
            todo_files.append(('arXiv', name, name))
        else:
            # Check if has 内容摘要
            if '内容摘要' in content:
                todo_files.append(('HAS_内容摘要', name, name))
            else:
                todo_files.append(('OTHER', name, name))

print(f"Total remaining: {len(todo_files)}")
from collections import Counter
types = Counter(t[0] for t in todo_files)
for t, c in types.items():
    print(f"  {t}: {c}")

print("\nSample DOI files (first 5):")
for t, key, name in [x for x in todo_files if x[0] == 'DOI'][:5]:
    print(f"  {name} | DOI: {key[:50]}")

print("\nSample HAS_内容摘要 files (first 5):")
for t, key, name in [x for x in todo_files if x[0] == 'HAS_内容摘要'][:5]:
    print(f"  {name}")

print("\nSample OTHER files (first 10):")
for t, key, name in [x for x in todo_files if x[0] == 'OTHER'][:10]:
    print(f"  {name}")
