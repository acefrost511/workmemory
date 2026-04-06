#!/usr/bin/env python3
"""读取选中文章的实际内容，提取真实标题"""
import json, re, os

os.chdir('/workspace/knowledge/原文库')
with open('/workspace/.papers_selected.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

def extract_real_title(content):
    """按优先级提取真实标题"""
    # Priority 1: **标题** or **原标题**
    for pat in [r'\*\*标题\*\*[：:]\s*(.+?)(?:\n|$)', r'\*\*原标题\*\*[：:]\s*(.+?)(?:\n|$)']:
        m = re.search(pat, content)
        if m:
            t = m.group(1).strip().strip('*').strip()
            if t and len(t) > 5 and not any(k in t for k in ['待补充', '待查', 'TBD', '暂无', '论文元数据', '论文信息', '空缺']):
                return t, '标题字段'
    # Priority 2: 标题（英文）
    m = re.search(r'标题（英文）[：:]\s*(.+?)(?:\n|$)', content)
    if m:
        t = m.group(1).strip().strip('*').strip()
        if t and len(t) > 5:
            return t, '英文标题'
    # Priority 3: 第一行标题（# 开头）
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# ') and len(line) > 10:
            t = line[2:].strip()
            if not any(k in t for k in ['论文元数据', '论文信息']):
                return t, '首行标题'
    # Fallback: scan for any line that looks like a real title
    for line in lines:
        line = line.strip()
        if len(line) > 15 and len(line) < 200 and not line.startswith('**') and not line.startswith('#') and not line.startswith('-') and not line.startswith('|'):
            if re.search(r'[\u4e00-\u9fff]', line) or re.search(r'[A-Z].*[a-z]', line):
                if not any(k in line for k in ['来源', '作者', 'DOI', '编号', '发表', '摘要', '关键词', '摘要', 'Abstract']):
                    return line, '内容首行'
    return None, '未找到'

def extract_field(content, field_name, max_len=200):
    """提取任意字段"""
    patterns = [
        rf'{re.escape(field_name)}[：:]\s*(.+?)(?:\n|$)',
        rf'\*\*{re.escape(field_name)}\*\*[：:]\s*(.+?)(?:\n|$)',
    ]
    for pat in patterns:
        m = re.search(pat, content)
        if m:
            val = m.group(1).strip().strip('*').strip()
            if val and val not in ['未知', '空缺', '暂无', '待补充', 'TBD']:
                return val[:max_len]
    return None

def is_cn_paper(content, source, fname):
    """判断是否中文期刊"""
    if any(kw in source for kw in ['中国', '中文', '教育研究', '电化教育', '课程教材', '中国教育', '北京大学', '清华大学', '北京师范', '华东师范', '华中师范', '汉斯', '原创力', '知网', '万方']):
        return True
    if re.search(r'中文[期刊文献论文]', source):
        return True
    # Chinese filename pattern
    if re.search(r'[\u4e00-\u9fff].*\.md$', fname):
        return True
    return False

for p in papers:
    fname = p['filename']
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title, title_src = extract_real_title(content)
    authors = extract_field(content, '作者', 150)
    source = extract_field(content, '来源', 150)
    doi = extract_field(content, 'DOI', 200)
    if not doi:
        doi = extract_field(content, 'doi', 200)
    drawer = extract_field(content, '关联信念抽屉', 50)
    paper_id = extract_field(content, '编号', 100)
    if not paper_id:
        paper_id = p['paper_id']
    
    is_cn = is_cn_paper(content, source or '', fname)
    
    print(f"\n=== {p['index']:02d}. {fname} ===")
    print(f"  标题来源: {title_src} | 标题: {title}")
    print(f"  作者: {authors}")
    print(f"  来源: {source}")
    print(f"  DOI: {doi}")
    print(f"  信念抽屉: {drawer}")
    print(f"  编号: {paper_id}")
    print(f"  中文: {is_cn}")
    
    # Update in papers list
    p['title'] = title
    p['title_src'] = title_src
    p['authors'] = authors
    p['source'] = source
    p['doi'] = doi
    p['drawer'] = drawer
    p['paper_id'] = paper_id
    p['is_cn'] = is_cn

# Save updated data
with open('/workspace/.papers_selected.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, ensure_ascii=False, indent=2)
print("\n已更新 /workspace/.papers_selected.json")
