#!/usr/bin/env python3
"""处理中文论文摘要：将'## 内容摘要'转换为'## 摘要'"""
import glob, os, re

files = glob.glob('/workspace/knowledge/原文库/*.md')
updated = []

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Skip if already has ## 摘要
    if '## 摘要\n' in content or content.count('## 摘要') > 0:
        continue
    
    # Look for 内容摘要 or abstract section
    abstract = ''
    
    # Pattern 1: ## 内容摘要
    m = re.search(r'^## 内容摘要\s*\n+(.+?)(?=^##|\Z)', content, re.MULTILINE | re.DOTALL)
    if m:
        abstract = m.group(1).strip()
    
    # Pattern 2: 摘要[:：]
    if not abstract:
        m = re.search(r'摘要[：:]\s*\n*(.+?)(?=^##|\Z)', content, re.MULTILINE | re.DOTALL)
        if m:
            abstract = m.group(1).strip()
    
    if abstract and len(abstract) > 30:
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

print(f"Updated: {len(updated)}")
for x in updated[:10]:
    print(f"  ✅ {x}")
if len(updated) > 10:
    print(f"  ... and {len(updated)-10} more")
