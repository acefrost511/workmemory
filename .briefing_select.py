#!/usr/bin/env python3
"""精准选文脚本：按v4.0规则严格选10篇"""
import os, re

FORMAL_DIR = "/workspace/knowledge/原文库"
PUSH_DATE = "2026-04-06"
PLACEHOLDERS = ['待确认','待查','待补充','待补','未知','TBD','pending','null','none']
EXCLUDED_STATES = ['已触动','已无触动']
EXCLUDED_DATE = PUSH_DATE  # 排除今日已推送

def has_placeholder_author(content):
    m = re.search(r'作者[\*\#]*[：:]\s*(.+?)(?:\n|$)', content)
    if not m:
        return True  # 无作者字段 → 过滤
    author = m.group(1).strip()
    return any(p in author for p in PLACEHOLDERS)

def is_excluded_state(content):
    for state in EXCLUDED_STATES:
        if state in content:
            return True
    # 检查是否今日已推送
    if f'推送日期：{PUSH_DATE}' in content or f'推送日期：{PUSH_DATE}' in content:
        return True
    return False

def get_pub_date(content):
    """优先读取「发表年月」，其次「出版年份」"""
    # 发表年月：2026年4月 / 2026-04
    m = re.search(r'发表[时年月：: ]*(\d{4})[年-](\d{1,2})[月]?', content)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}"
    # 出版年份
    m = re.search(r'出版年份[：: ]*(\d{4})', content)
    if m:
        return f"{m.group(1)}-12"
    return None

def extract_en_title(content):
    """提取英文标题"""
    patterns = [
        r'\*\*原标题\*\*[：:]\s*(.+?)(?:\n)',
        r'\*\*标题\*\*[（(]英文[）)][：:]\s*(.+?)(?:\n)',
        r'原标题[：:]\s*(.+?)(?:\n)',
    ]
    for pat in patterns:
        m = re.search(pat, content)
        if m:
            t = m.group(1).strip().lstrip('*# ')
            if t and not any(p in t for p in ['待补充','待查','TBD','pending']):
                return t
    return None

def extract_cn_title(content):
    patterns = [
        r'\*\*标题\*\*[：:]\s*(.+?)(?:\n)',
        r'^#\s+(.+?)(?:\n)',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.MULTILINE)
        if m:
            t = m.group(1).strip().lstrip('*# ')
            if t and not any(p in t for p in ['待补充','待查','TBD','pending']):
                return t
    return None

def extract_author(content):
    m = re.search(r'作者[\*\#]*[：:]\s*(.+?)(?:\n|$)', content)
    if m:
        return m.group(1).strip().lstrip('*# ')
    return None

files = [f for f in os.listdir(FORMAL_DIR) if f.endswith('.md')]
print(f"总文件数：{len(files)}")

candidates = []
skipped_placeholders = []
skipped_pushed = []
skipped_no_date = []
skipped_no_author = []

for fname in files:
    fpath = os.path.join(FORMAL_DIR, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 过滤：已推送/已触动/已无触动
    if is_excluded_state(content):
        skipped_pushed.append(fname)
        continue

    # 过滤：作者占位符
    if has_placeholder_author(content):
        skipped_placeholders.append(fname)
        continue

    # 提取发表时间
    pub_date = get_pub_date(content)
    if not pub_date:
        skipped_no_date.append(fname)
        continue

    # 提取标题
    en_title = extract_en_title(content)
    cn_title = extract_cn_title(content)
    author = extract_author(content)

    # 判断中英文
    is_chinese = 'cnki' in fname or '中国' in fname or any(cn in fname for cn in ['教育研究','电化教育','课程教材'])

    candidates.append({
        'file': fname,
        'pub_date': pub_date,
        'en_title': en_title,
        'cn_title': cn_title,
        'author': author,
        'is_chinese': is_chinese,
    })

print(f"\n可候选：{len(candidates)} 篇")
print(f"跳过（已推送/已触动）：{len(skipped_pushed)} 篇")
print(f"跳过（作者占位符）：{len(skipped_placeholders)} 篇")
print(f"跳过（无发表时间）：{len(skipped_no_date)} 篇")

# 按时间倒序
candidates.sort(key=lambda x: x['pub_date'], reverse=True)

# 选10篇：9英文+1中文
en_list = [c for c in candidates if not c['is_chinese']][:9]
cn_list = [c for c in candidates if c['is_chinese']][:1]
selected = en_list + cn_list

print(f"\n选出：{len(selected)} 篇（{len(en_list)}英文+{len(cn_list)}中文）")
for i, c in enumerate(selected):
    print(f"  [{i+1:02d}] {c['pub_date']} | {c['author']} | {c['en_title'] or c['cn_title']}")

# 写文件
with open('/workspace/.daily_briefing.md', 'w', encoding='utf-8') as f:
    f.write(f"# 每日简报 · {PUSH_DATE}\n\n")
    f.write(f"> 简报版本：v4.0 | 执行时间：自动生成\n\n")
    for i, c in enumerate(selected):
        title = c['en_title'] or c['cn_title'] or '原文库缺失'
        f.write(f"---\n\n")
        f.write(f"【{i+1:02d}】{c['cn_title'] or title}\n")
        if c['en_title']:
            f.write(f"原标题：{c['en_title']}\n")
        f.write(f"作者：{c['author']}\n")
        f.write(f"来源：原文库编号：{c['file']}\n")
        f.write(f"发表时间：{c['pub_date']}\n")
        f.write(f"[完整内容需读取原文库文件]\n\n")

print("\n✅ 已写入 /workspace/.daily_briefing.md")
