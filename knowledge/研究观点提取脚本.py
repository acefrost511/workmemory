#!/usr/bin/env python3
"""
研究观点提取器 v1.0
功能：扫描原文库所有.md文件，提取核心数据点和研究结论
输出：结构化JSON，供后续聚类分析
"""
import os
import re
import json
from pathlib import Path

LIBRARY_DIR = Path("/workspace/knowledge/原文库")
OUTPUT_FILE = Path("/workspace/knowledge/研究观点池_全量.json")

# 提取模式
KEY_PATTERNS = [
    (r'核心发现[：:]\s*(.{10,300})', '核心发现'),
    (r'关键发现[：:]\s*(.{10,300})', '关键发现'),
    (r'主要发现[：:]\s*(.{10,300})', '主要发现'),
    (r'结论[：:]\s*(.{10,300})', '结论'),
    (r'结果[：:]\s*(.{10,300})', '结果'),
]

# 数字指标提取
NUMBER_PATTERN = re.compile(
    r'(\d+(?:\.\d+)?)\s*(%|个百分点|倍|分数|名|篇|所|万|亿|美元|英镑)'
    r'|\b(RCT|元分析|综述)\b|'
    r'(提升|提高|增加|减少|降低|下降|增长)\s*(\d+(?:\.\d+)?)\s*(%|个百分点|倍)?'
)

def extract_from_file(filepath):
    """从单篇文章提取所有发现"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []

    findings = []
    filename = filepath.name

    # 提取标题
    title_match = re.search(r'^#\s+(.{5,200})', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filename

    # 提取DOI
    doi_match = re.search(r'DOI[：:]?\s*(10\.\S+)', content)
    doi = doi_match.group(1) if doi_match else ""

    # 提取中文标题
    cn_title_match = re.search(r'中文标题[：:]\s*(.{5,100})', content)
    cn_title = cn_title_match.group(1).strip() if cn_title_match else ""

    # 提取来源/期刊
    journal_match = re.search(r'(Computers and Education|npj AI|JSTER|ETR&D|BJET|Frontiers|Educational Technology|frontrs|电化教育研究|课程教材教法|UNESCO|OECD|Nature|Science|arXiv)', content)
    journal = journal_match.group(1) if journal_match else "其他"

    # 提取核心发现段落（从"核心发现"或"摘要"开始的前500字）
    core_section = ""
    for pattern in KEY_PATTERNS:
        matches = re.findall(pattern[0], content)
        for m in matches:
            if len(m) > 20:
                core_section += m.strip() + "\n"

    # 如果没有找到，尝试从摘要部分提取
    if not core_section:
        abstract_match = re.search(r'##?\s*摘要[：:]\s*([\s\S]{50,600})', content)
        if abstract_match:
            core_section = abstract_match.group(1).strip()

    # 提取所有数字指标
    numbers = []
    for nm in NUMBER_PATTERN.finditer(content):
        num_str = nm.group(0).strip()
        if len(num_str) > 2:
            numbers.append(num_str)

    # 去重
    numbers = list(dict.fromkeys(numbers))[:20]  # 最多20个

    # 提取研究类型
    study_type = ""
    if "RCT" in content or "随机对照" in content:
        study_type = "RCT"
    elif "元分析" in content or "meta-analysis" in content.lower():
        study_type = "元分析"
    elif "综述" in content or "review" in content.lower():
        study_type = "综述"
    elif "问卷" in content or "survey" in content.lower():
        study_type = "问卷调查"
    elif "访谈" in content or "interview" in content.lower():
        study_type = "访谈"
    else:
        study_type = "实证研究"

    # 提取信念标签
    belief_tags = []
    belief_match = re.findall(r'信念(\d+)', content)
    for b in belief_match:
        if b not in belief_tags:
            belief_tags.append(f"信念{b}")

    return {
        "文件名": filename,
        "英文标题": title,
        "中文标题": cn_title,
        "DOI": doi,
        "期刊": journal,
        "研究类型": study_type,
        "信念标签": belief_tags,
        "核心发现": core_section[:500] if core_section else "",
        "数字指标": numbers,
        "全文长度": len(content)
    }

def main():
    files = list(LIBRARY_DIR.glob("*.md"))
    print(f"开始处理 {len(files)} 篇文章...")

    results = []
    for i, f in enumerate(files):
        if i % 50 == 0:
            print(f"进度: {i}/{len(files)}")
        r = extract_from_file(f)
        if r and r.get("核心发现") or r.get("数字指标"):
            results.append(r)

    print(f"提取完成: {len(results)} 篇有可分析内容")

    # 统计
    study_types = {}
    journals = {}
    for r in results:
        st = r.get("研究类型", "未知")
        study_types[st] = study_types.get(st, 0) + 1
        j = r.get("期刊", "其他")
        journals[j] = journals.get(j, 0) + 1

    output = {
        "提取时间": "2026-04-05",
        "总篇数": len(files),
        "有效提取": len(results),
        "统计": {
            "研究类型分布": study_types,
            "期刊分布": dict(sorted(journals.items(), key=lambda x: -x[1])[:20])
        },
        "文章列表": results
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"输出: {OUTPUT_FILE}")
    print(f"有效文章: {len(results)} 篇")
    print(f"研究类型: {study_types}")

if __name__ == "__main__":
    main()
