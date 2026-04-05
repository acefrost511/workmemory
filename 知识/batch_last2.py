#!/usr/bin/env python3
"""处理最后20个文件 - 提取内容作为摘要"""
import glob, os, re

def extract_summary(content, name):
    """从文件内容中提取摘要"""
    # Try structured sections first
    sections = ['核心发现', '主要内容', '摘要', '研究结论', '核心论点', '关键发现', '研究概要']
    for section in sections:
        m = re.search(rf'{section}[：:\n]+(.+?)(?=^## |^#{1,3} |^### |^`{3}|$)', content, re.DOTALL | re.MULTILINE)
        if m:
            text = m.group(1).strip()
            text = re.sub(r'^[*\-#]+', '', text).strip()
            text = re.sub(r'\n+', ' ', text)
            if len(text) > 80:
                return text[:500]
    
    # Try to find first few paragraphs after metadata
    lines = content.split('\n')
    content_lines = []
    skip_next = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^(#{1,3} |AIGC:|^\*\*|\-\-\-|来源|URL|链接|日期|DOI|情报)', stripped):
            skip_next = 2
            continue
        if skip_next > 0:
            skip_next -= 1
            continue
        if len(stripped) > 60:
            content_lines.append(stripped)
    
    if content_lines:
        text = ' '.join(content_lines[:4])
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        text = text[:500]
        for end in ['。', '！', '？', '.', '!', '?']:
            last = text.rfind(end)
            if last > 100:
                return text[:last+1]
        return text[:300]
    return ''

files = glob.glob('/workspace/knowledge/原文库/*.md')
updated = []

for f in files:
    name = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    if '## 摘要\n' in content or '**摘要状态**：✅' in content:
        continue
    
    summary = extract_summary(content, name)
    
    if summary and len(summary) > 80:
        section = "\n## 摘要\n" + summary + "\n\n**摘要状态**：✅已补充（内容提取）\n"
        if '## 基本信息' in content:
            content = content.replace('## 基本信息', '## 基本信息' + section, 1)
        elif '## 核心发现' in content:
            content = content.replace('## 核心发现', '## 核心发现\n\n## 摘要\n' + summary + '\n\n**摘要状态**：✅已补充（内容提取）\n', 1)
        else:
            content = content + section
        
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        updated.append(name)
        print("  ✅ " + name)
    else:
        print("  ⚠️  No summary for: " + name)

print("\nTotal updated: " + str(len(updated)))
