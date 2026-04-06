#!/usr/bin/env python3
import os, re

os.chdir('/workspace/knowledge/原文库')
all_files = [f for f in os.listdir('.') if f.endswith('.md')]

def get_date(f):
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            c = fh.read()
        if '已触动' in c or '已无触动' in c or '已推送' in c:
            return None, None
        for line in c.split('\n'):
            for field in ['发表时间', '发表年月', '出版年份']:
                if field in line:
                    m = re.search(r'(\d{4})[年/-](\d{1,2})', line)
                    if m:
                        y, mo = int(m.group(1)), int(m.group(2))
                        if 1 <= mo <= 12 and 2000 <= y <= 2026:
                            if y == 2026 and mo > 4:
                                return None, None
                            return (y, mo), c
                    if field == '出版年份' and m:
                        return None, None
        return None, None
    except:
        return None, None

results = []
for f in all_files:
    res, content = get_date(f)
    if res:
        results.append((res, f, content))

results.sort(key=lambda x: x[0], reverse=True)

# Pick top 10: prefer English, include Chinese
selected = []
en_count = 0
cn_count = 0
for (y, mo), f, content in results:
    is_cn = bool(re.search(r'来源[：:].*(?:中国|中文|教育研究|电化教育|课程教材教法|中国教育|北京大学|清华大学|北京师范大学|华东师范大学|华中师范大学)', content))
    lang = 'CN' if is_cn else 'EN'
    if len(selected) < 10:
        selected.append((y, mo, f, is_cn, content))
    print(f"{y}-{mo:02d} [{lang}] | {f}")

print(f"\n=== SELECTED 10 ===")
for i, s in enumerate(selected):
    print(f"{i+1:02d}. {s[0]}-{s[1]:02d} [{'CN' if s[3] else 'EN'}] | {s[2]}")
