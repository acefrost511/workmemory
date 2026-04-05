#!/usr/bin/env python3
"""处理剩余文件"""
import glob, os, re

files = glob.glob('/workspace/knowledge/原文库/*.md')
updated = []

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Skip if already has ## 摘要
    if '## 摘要\n' in content:
        continue
    
    # Look for 内容摘要
    if '## 内容摘要' in content:
        m = re.search(r'^## 内容摘要\s*\n+(.+?)(?=^##|\Z)', content, re.MULTILINE | re.DOTALL)
        if m:
            abstract = m.group(1).strip()
            section = "\n## 摘要\n" + abstract + "\n\n**摘要状态**：✅已补充\n"
            if '## 基本信息' in content:
                content = content.replace('## 基本信息', '## 基本信息' + section, 1)
            elif '## 期刊信息' in content:
                content = content.replace('## 期刊信息', '## 期刊信息' + section, 1)
            else:
                content = content + section
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(content)
            updated.append(os.path.basename(f))
            continue
    
    # For OTHER files without DOI - try to find content to summarize
    name = os.path.basename(f)
    # Try to find first paragraph after header info
    # Look for 正文内容 or first long paragraph
    paragraphs = re.findall(r'[^。！？\n]{50,}', content)
    if paragraphs and len(paragraphs) > 3:
        # Use 2nd-3rd paragraph as summary (skip header info)
        summary_candidates = [p for p in paragraphs[2:5] if len(p) > 100]
        if summary_candidates:
            # Truncate to ~300 chars
            summary = summary_candidates[0][:400].strip()
            # Ensure it ends at a sentence boundary
            for end in '。！？':
                last = summary.rfind(end)
                if last > 100:
                    summary = summary[:last+1]
                    break
            section = "\n## 摘要\n" + summary + "\n\n**摘要状态**：✅已补充（内容提取）\n"
            if '## 基本信息' in content:
                content = content.replace('## 基本信息', '## 基本信息' + section, 1)
            else:
                content = content + section
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(content)
            updated.append(os.path.basename(f))

print(f"Updated: {len(updated)}")
for x in updated:
    print(f"  ✅ {x}")
