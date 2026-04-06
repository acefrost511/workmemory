#!/usr/bin/env python3
"""简报生成脚本 - 一次性完成选文+撰写+写入"""
import os, re, json
from datetime import datetime

os.chdir('/workspace/knowledge/原文库')
all_files = [f for f in os.listdir('.') if f.endswith('.md')]

# ===== Step 1: 选文 =====
def get_date_and_content(f):
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            c = fh.read()
        if '已触动' in c or '已无触动' in c or '已推送' in c:
            return None
        for line in c.split('\n'):
            for field in ['发表时间', '发表年月']:
                if field in line:
                    m = re.search(r'(\d{4})[年/-](\d{1,2})', line)
                    if m:
                        y, mo = int(m.group(1)), int(m.group(2))
                        if 1 <= mo <= 12 and 2000 <= y <= 2026:
                            if y == 2026 and mo > 4:
                                return None
                            return (y, mo, f, c)
            if '出版年份' in line:
                m = re.search(r'(\d{4})', line)
                if m:
                    y = int(m.group(1))
                    if 2000 <= y <= 2026:
                        return (y, 12, f, c)
    except:
        pass
    return None

candidates = []
for f in all_files:
    r = get_date_and_content(f)
    if r:
        candidates.append(r)

candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)

# 选10篇：英文优先，中文补充
selected = []
en_count = 0
cn_count = 0
for (y, mo, f, content) in candidates:
    is_cn = bool(re.search(r'来源[：:].*(?:中国|中文|教育研究|电化教育|课程教材教法|中国教育|北京大学|清华大学|北京师范大学|华东师范大学|华中师范大学)', content))
    if is_cn and cn_count >= 1:
        continue
    if not is_cn and en_count >= 9:
        continue
    selected.append((y, mo, f, content, is_cn))
    en_count += (0 if is_cn else 1)
    cn_count += (1 if is_cn else 0)
    if len(selected) == 10:
        break

print(f"选定10篇：EN={sum(1 for s in selected if not s[4])}, CN={sum(1 for s in selected if s[4])}")
for i, s in enumerate(selected):
    print(f"{i+1:02d}. {s[0]}-{s[1]:02d} [{'CN' if s[4] else 'EN'}] | {s[2]}")

# ===== Step 2: 提取标题 =====
def extract_title(content, is_cn):
    """按SKILL.md优先级提取标题"""
    for pat in [r'\*\*标题\*\*[：:]\s*(.+)', r'\*\*原标题\*\*[：:]\s*(.+)',
                r'标题（英文）[：:]\s*(.+)', r'Original Title[：:]\s*(.+)',
                r'^#\s+(.+)', r'^标题[：:]\s*(.+)']:
        m = re.search(pat, content, re.MULTILINE)
        if m:
            t = m.group(1).strip().strip('*').strip()
            if t and not any(k in t for k in ['待补充', '待查', 'TBD', '暂无']):
                return t
    return None

# ===== Step 3: 读取每篇文章 =====
papers_data = []
for i, (y, mo, fname, content, is_cn) in enumerate(selected):
    title = extract_title(content, is_cn)
    # Extract authors
    author_m = re.search(r'作者[：:]\s*(.+)', content)
    authors = author_m.group(1).strip() if author_m else '未知'
    # Extract source
    source_m = re.search(r'来源[：:]\s*(.+)', content)
    source = source_m.group(1).strip() if source_m else '未知来源'
    # Extract DOI
    doi_m = re.search(r'(?:DOI|doi)[：:\s]*(https?://\S+)', content)
    doi = doi_m.group(1) if doi_m else '见原文库'
    # Extract 关联信念抽屉
    drawer_m = re.search(r'关联信念抽屉[：:]\s*(#\d+)', content)
    drawer = drawer_m.group(1) if drawer_m else '#待定'
    # Extract 编号
    id_m = re.search(r'编号[：:]\s*(\S+)', content)
    paper_id = id_m.group(1) if id_m else fname.replace('.md','')
    
    papers_data.append({
        'index': i+1,
        'year': y, 'month': mo,
        'filename': fname,
        'is_cn': is_cn,
        'title': title,
        'authors': authors,
        'source': source,
        'doi': doi,
        'drawer': drawer,
        'paper_id': paper_id,
        'content': content
    })

# 输出JSON供后续处理
with open('/workspace/.papers_selected.json', 'w', encoding='utf-8') as f:
    json.dump(papers_data, f, ensure_ascii=False, indent=2)

print(f"\n已写入 /workspace/.papers_selected.json，共{len(papers_data)}篇")
