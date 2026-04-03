#!/usr/bin/env python3
import os
import re
from datetime import datetime

src = "/workspace/knowledge/原文库"
deleted = []
kept = []

for fname in sorted(os.listdir(src)):
    if not fname.endswith('.md'):
        continue
    # Skip 2025 and 2026 by filename
    if re.search(r'[\-_]202[56][_\-]', fname) or '2025' in fname or '2026' in fname:
        kept.append(fname)
        continue

    fpath = os.path.join(src, fname)
    year = None
    try:
        with open(fpath, 'r', errors='ignore') as f:
            content = f.read(3000)
        # Look for 4-digit years in content
        years = re.findall(r'\b(20[12][0-9])\b', content)
        if years:
            # Take the most recent unambiguous year
            year = max(y for y in years if 2015 <= int(y) <= 2030)
    except:
        pass

    if year and int(year) < 2025:
        os.remove(fpath)
        deleted.append(f"{fname} ({year})")
    else:
        kept.append(fname)

print(f"✅ 保留: {len(kept)} 个")
print(f"🗑️  删除: {len(deleted)} 个")
for d in deleted:
    print(f"   {d}")
print(f"\n剩余文件: {len(os.listdir(src))} 个")
