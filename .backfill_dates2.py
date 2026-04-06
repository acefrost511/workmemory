#!/usr/bin/env python3
"""激进补录发表时间——从多个可能位置提取日期"""
import os, re

FORMAL_DIR = "/workspace/knowledge/原文库"
PLACEHOLDERS = ['待确认','待查','待补充','待补','未知','TBD','pending']

def already_has_date(content):
    return bool(re.search(r'发表[时年月：: ]*\d{4}', content))

def year_month_from_content(content):
    """从内容正文提取年月"""
    # 模式1: 2026年3月 / 2026年4月
    m = re.search(r'(\d{4})年(\d{1,2})月', content)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}"
    # 模式2: June 2026 / Apr 2026
    months = {'January':'01','February':'02','March':'03','April':'04','May':'05','June':'06',
              'July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}
    for mon, num in months.items():
        m = re.search(rf'{mon}\s+(\d{{4}})', content)
        if m:
            return f"{m.group(1)}-{num}"
    # 模式3: Vol.10, 2026 / 2026, Vol.10
    m = re.search(r'Vol\.\d+,?\s*(\d{4})', content, re.IGNORECASE)
    if m and 2020 <= int(m.group(1)) <= 2027:
        return f"{m.group(1)}-01"
    m = re.search(r'(\d{4}),?\s*Vol\.', content)
    if m and 2020 <= int(m.group(1)) <= 2027:
        return f"{m.group(1)}-01"
    # 模式4: (2026) / 2026/
    m = re.search(r'[\(\s](\d{4})[\)\s]', content)
    if m and 2020 <= int(m.group(1)) <= 2027:
        return f"{m.group(1)}-01"
    return None

def year_from_filename(fname):
    # DOI日期: 10.1016.j.compedu.2026.105614
    m = re.search(r'\.(\d{4})\.\d{5}', fname)
    if m:
        y = int(m.group(1))
        if 2020 <= y <= 2027: return str(y)
    # 2026-01格式
    m = re.search(r'-(\d{4})-\d{2}', fname)
    if m:
        y = int(m.group(1))
        if 2020 <= y <= 2027: return str(y)
    # 单独2026
    m = re.search(r'(?<![a-zA-Z])(\d{4})(?!\d)', fname)
    if m:
        y = int(m.group(1))
        if 2020 <= y <= 2027: return str(y)
    return None

fixed = 0; skipped = 0; no_date = []

files = [f for f in os.listdir(FORMAL_DIR) if f.endswith('.md')]
for fname in files:
    fpath = os.path.join(FORMAL_DIR, fname)
    with open(fpath, encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if already_has_date(content):
        skipped += 1
        continue

    # 排除作者占位符（已有date的是合法文章）
    am = re.search(r'作者[\*\#]*[：:]\s*(.+?)(?:\n|$)', content)
    if am and any(p in am.group(1) for p in PLACEHOLDERS):
        no_date.append((fname, '作者占位符')); continue

    pub_date = year_month_from_content(content)
    if not pub_date:
        y = year_from_filename(fname)
        if y: pub_date = f"{y}-01"

    if pub_date:
        insert = f"\n**发表年月**：{pub_date}年\n"
        if '# 核心发现' in content:
            new_content = content.replace('# 核心发现', insert + '# 核心发现', 1)
        elif '## 核心发现' in content:
            new_content = content.replace('## 核心发现', insert + '## 核心发现', 1)
        else:
            new_content = content + insert
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1
    else:
        no_date.append((fname, '无法提取日期'))

print(f"✅ 补录发表时间：{fixed} 篇（已跳过={skipped}）")
print(f"❌ 仍无日期：{len(no_date)} 篇")
for fname, reason in no_date[:10]:
    print(f"   [{reason}] {fname}")
