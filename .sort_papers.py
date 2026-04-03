#!/usr/bin/env python3
import os, re

src = "/workspace/knowledge/原文库"
results = []

for fname in os.listdir(src):
    if not fname.endswith('.md'):
        continue
    fpath = os.path.join(src, fname)
    with open(fpath) as f:
        txt = f.read()
    
    # Skip if not verified
    if '✅已验证' not in txt:
        continue
    
    # Extract date
    date_str = None
    # Patterns: 发表时间：2026年3月 / 发表日期：2025-03-20 / 发表年: 2025 / 发布时间: 2026年
    for pat in [
        r'发表时间[：:]\s*(\d{4})年(\d{1,2})月',
        r'发表日期[：:]\s*(\d{4})[-年](\d{2})',
        r'发布时间[：:]\s*(\d{4})年(\d{1,2})月',
        r'发表年[：:]\s*(\d{4})',
    ]:
        m = re.search(pat, txt)
        if m:
            y, m2 = m.group(1), int(m.group(2))
            date_str = f"{y}-{m2:02d}"
            break
    
    # Extract title (first line starting with #)
    title_m = re.search(r'^#\s+(.+)$', txt, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else fname
    
    results.append((date_str or '0000-00', fname, title))

# Sort by date descending, then by filename
results.sort(key=lambda x: x[0], reverse=True)

for date, fname, title in results[:20]:
    print(f"{date}\t{fname}\t{title}")
