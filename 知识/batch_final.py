#!/usr/bin/env python3
"""处理剩余的最后几批文件"""
import glob, os, re

files = glob.glob('/workspace/knowledge/原文库/*.md')
updated = []

for f in files:
    name = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    if '## 摘要\n' in content or '**摘要状态**：✅' in content:
        continue
    
    # Fix HAS_内容摘要
    if '## 内容摘要' in content:
        m = re.search(r'^## 内容摘要\s*\n+(.+?)(?=^##|\Z)', content, re.MULTILINE | re.DOTALL)
        if m:
            abstract = m.group(1).strip()
            section = "\n## 摘要\n" + abstract + "\n\n**摘要状态**：✅已补充\n"
            if '## 基本信息' in content:
                content = content.replace('## 基本信息', '## 基本信息' + section, 1)
            else:
                content = content + section
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(content)
            updated.append(name)
            continue
    
    # For OTHER files - try content extraction
    # Remove header info and find substantive content
    # Skip AIGC metadata, basic info sections
    lines = content.split('\n')
    content_lines = []
    skip_patterns = ['^# ', '^AIGC:', '^\*\*', '^---', '^## ', '^来源', '^URL', '^链接', '^日期', '^作者', '^发表', '^期刊', '^摘要[:：]', '^\* 摘要']
    in_skip = False
    for line in lines:
        skip = False
        for pat in skip_patterns:
            if re.match(pat, line.strip()):
                skip = True
                break
        if not skip and len(line.strip()) > 50:
            content_lines.append(line.strip())
    
    if content_lines:
        # Join first 3 substantive paragraphs
        summary = ' '.join(content_lines[:3])
        summary = summary[:500]
        for end in '。！？.!?':
            last = summary.rfind(end)
            if last > 150:
                summary = summary[:last+1]
                break
        
        if len(summary) > 100:
            section = "\n## 摘要\n" + summary + "\n\n**摘要状态**：✅已补充（内容提取）\n"
            if '## 基本信息' in content:
                content = content.replace('## 基本信息', '## 基本信息' + section, 1)
            else:
                content = content + section
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(content)
            updated.append(name)

print(f"Updated: {len(updated)}")
for x in updated:
    print(f"  ✅ {x}")
