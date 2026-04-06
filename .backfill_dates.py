#!/usr/bin/env python3
"""从文件名反向补录发表时间（临时补丁）"""
import os, re

FORMAL_DIR = "/workspace/knowledge/原文库"

def year_from_filename(fname):
    """从文件名提取可能年份"""
    # 模式1: 10.1007_s10639-023-xxxx → 2023年
    m = re.search(r'0[56]-\d{3}-(\d{2})\d{2}-\d', fname)
    if m:
        y = int(m.group(1))
        if y <= 26:
            return f"20{y:02d}"
    # 模式2: 10.1016.j.compedu.2026.xxxxx → 2026
    m = re.search(r'\.(\d{4})\.\d', fname)
    if m:
        y = int(m.group(1))
        if 2020 <= y <= 2027:
            return str(y)
    # 模式3: 10.1016-j.caeai.2026.xxxxx → 2026
    m = re.search(r'-(\d{4})\.\d', fname)
    if m:
        y = int(m.group(1))
        if 2020 <= y <= 2027:
            return str(y)
    return None

def get_current_pub_date(content):
    """读现有发表时间字段"""
    m = re.search(r'发表[时年月：: ]*(\d{4})[年-](\d{1,2})', content)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}"
    m2 = re.search(r'出版年份[：: ]*(\d{4})', content)
    if m2:
        return f"{m2.group(1)}-12"
    return None

def add_pub_date(content, pub_date):
    """在「## 核心发现」前插入发表时间（若尚无）"""
    if '发表时间' in content or '发表年月' in content:
        return content
    insert = f"\n**发表年月**：{pub_date}年\n"
    if '## 核心发现' in content:
        return content.replace('## 核心发现', insert + '## 核心发现', 1)
    if '# 核心发现' in content:
        return content.replace('# 核心发现', insert + '# 核心发现', 1)
    return content + insert

fixed = 0
no_date = []

files = [f for f in os.listdir(FORMAL_DIR) if f.endswith('.md')]
for fname in files:
    fpath = os.path.join(FORMAL_DIR, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if get_current_pub_date(content):
        continue  # 已有时间，跳过

    year = year_from_filename(fname)
    if year:
        pub_date = f"{year}-01"  # 写标准格式 yyyy-mm，精确月待后续补
        new_content = add_pub_date(content, pub_date)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1
    else:
        no_date.append(fname)

print(f"✅ 补录发表时间：{fixed} 篇")
print(f"❌ 仍无时间：{len(no_date)} 篇")
if no_date[:10]:
    print("无时间文件样例：")
    for f in no_date[:10]:
        print(f"  {f}")
