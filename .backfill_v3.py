#!/usr/bin/env python3
"""真正有效的发表时间补录脚本"""
import os, re, time

FORMAL_DIR = '/workspace/knowledge/原文库'
COMMIT_MSG = "fix: 发表时间补录（backfill_v3，从正文+文件名全面提取）"

def find_date_in_content(content):
    """从文章正文各种格式中提取年月"""
    # 2026年3月 / 2026年4月
    m = re.search(r'(\d{4})年(\d{1,2})月', content)
    if m: return f"{m.group(1)}-{int(m.group(2)):02d}"
    # 2026-03 / 2026-04
    m = re.search(r'\b(\d{4})-(\d{2})\b', content)
    if m and 2020 <= int(m.group(1)) <= 2027:
        return f"{m.group(1)}-{m.group(2)}"
    # March 2026 / June 2026
    months = {'January':'01','February':'02','March':'03','April':'04','May':'05','June':'06',
              'July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}
    for mon, num in months.items():
        m = re.search(rf'{mon}\s+(\d{{4}})', content)
        if m: return f"{m.group(1)}-{num}"
    return None

def find_date_in_filename(fname):
    """从DOI文件名提取年份"""
    # 10.1016.j.compedu.2026.105563
    m = re.search(r'\.(\d{4})\.\d{5}', fname)
    if m:
        y = int(m.group(1))
        if 2020 <= y <= 2027: return f"{y}-01"
    # 2026-01格式
    m = re.search(r'-(\d{4})-(\d{2})', fname)
    if m:
        y = int(m.group(1))
        if 2020 <= y <= 2027: return f"{y}-{m.group(2)}"
    # 单独2026
    m = re.search(r'(?<!\d)(\d{4})(?!\d)', fname)
    if m:
        y = int(m.group(1))
        if 2020 <= y <= 2027: return f"{y}-01"
    return None

def already_has(content):
    return bool(re.search(r'发表[时年月：: ]*\d{4}', content))

def write_date(content, pub_date):
    """在正文最前面插入发表年月（不重复）"""
    marker = f"**发表年月**：{pub_date}年\n"
    if '# 论文信息' in content:
        return content.replace('# 论文信息', marker + '# 论文信息', 1)
    if '# 基本信息' in content:
        return content.replace('# 基本信息', marker + '# 基本信息', 1)
    if content.startswith('---'):
        return marker + content
    return marker + content

count = 0
fixed_files = []

files = [f for f in os.listdir(FORMAL_DIR) if f.endswith('.md')]
for fname in files:
    fpath = os.path.join(FORMAL_DIR, fname)
    with open(fpath, encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if already_has(content):
        continue
    
    # 排除作者占位符
    am = re.search(r'作者[\*\#]*[：:]\s*(.+?)(?:\n|$)', content)
    if am and any(p in am.group(1) for p in ['待确认','待查','待补充','待补','未知']):
        continue
    
    pub_date = find_date_in_content(content)
    if not pub_date:
        pub_date = find_date_in_filename(fname)
    
    if pub_date:
        new_content = write_date(content, pub_date)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed_files.append((fname, pub_date))
        count += 1
        if count % 50 == 0:
            print(f'已处理 {count} 篇...')

print(f'✅ 补录完成：{count} 篇')
if fixed_files[:3]:
    for f, d in fixed_files[:3]:
        print(f'  {f}: {d}')
