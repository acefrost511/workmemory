#!/usr/bin/env python3
"""
修复原文库中作者占位符文章：
- 有DOI的文章：从DOI补充作者
- 无DOI的文章：标记删除
"""
import os
import re
import urllib.request
import json

FORMAL_DIR = "/workspace/knowledge/原文库"
PLACEHOLDER_PATTERNS = ['待确认', '待查', '待补充', '待补', '作者.*待']

def extract_doi(content):
    m = re.search(r'10\.\d{4,}/[^\s，,。；;]+', content)
    if m:
        return m.group(0).rstrip('.,;，。；））')
    return None

def fetch_crossref_authors(doi):
    """通过CrossRef API获取论文作者"""
    url = f"https://api.crossref.org/works/{doi}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw/1.0 (mailto:admin@example.com)"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        authors = data.get("message", {}).get("author", [])
        if not authors:
            return None
        # 构造作者字符串
        names = []
        for a in authors[:3]:
            given = a.get("given", "")
            family = a.get("family", "")
            name = f"{family} {given}".strip()
            if name:
                names.append(name)
        if len(authors) > 3:
            return f"{', '.join(names)}, et al."
        return f"{', '.join(names)}"
    except Exception as e:
        return None

def fix_file(filepath):
    filename = os.path.basename(filepath)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        return "skip", "无法读取"

    # 检查是否有占位符
    has_placeholder = False
    for pat in PLACEHOLDER_PATTERNS:
        if re.search(pat, content):
            has_placeholder = True
            break
    if not has_placeholder:
        return "skip", "无需修复"

    # 提取DOI
    doi = extract_doi(content)
    if not doi:
        return "delete", "无DOI，无法补充作者"

    # 尝试从DOI获取作者
    authors = fetch_crossref_authors(doi)
    if not authors:
        return "delete", f"DOI {doi} 无法获取作者"

    # 替换作者字段
    # 匹配多种作者字段格式
    new_content = re.sub(
        r'(\*?\*?作者[：:]\s*).+?(\n)',
        rf'\1{authors}\2',
        content,
        flags=re.IGNORECASE
    )
    if new_content == content:
        # 尝试追加到摘要前的位置
        new_content = content.replace("## 摘要", f"**作者**：{authors}\n\n## 摘要", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return "fix", f"已替换为：{authors}"

def main():
    files = [f for f in os.listdir(FORMAL_DIR) if f.endswith(".md")]
    results = {"fix": [], "delete": [], "skip": []}

    for filename in files:
        filepath = os.path.join(FORMAL_DIR, filename)
        action, detail = fix_file(filepath)
        results[action].append((filename, detail))

    print(f"✅ 修复：{len(results['fix'])} 篇")
    for fname, detail in results['fix'][:5]:
        print(f"   {fname}: {detail}")
    if len(results['fix']) > 5:
        print(f"   ...还有{len(results['fix'])-5}篇")

    print(f"\n🗑 删除：{len(results['delete'])} 篇")
    for fname, detail in results['delete']:
        print(f"   {fname}: {detail}")

    print(f"\n⏭ 跳过：{len(results['skip'])} 篇（无需修复）")

if __name__ == "__main__":
    main()
