#!/usr/bin/env python3
"""
研究观点聚类器 v1.0
对研究观点池JSON进行主题聚类，然后与信念库比对
"""
import json
from pathlib import Path
from collections import defaultdict

POOL_FILE = Path("/workspace/knowledge/研究观点池_全量.json")
BELIEF_DIR = Path("/workspace/knowledge/beliefs")
OUTPUT_FILE = Path("/workspace/knowledge/研究观点聚类结果.json")

# 主题关键词体系（自下而上归纳）
THEME_KEYWORDS = {
    "教师工作量与备课": ["备课", "planning", "workload", "时间", "节省", "减少", "效率", "负担", "教师时间"],
    "学生学业成绩": ["成绩", "achievement", "performance", "分数", "提高", "提升", "学习效果", "学业"],
    "学习态度与动机": ["动机", "engagement", "态度", "兴趣", "参与", "情感", "情绪", "自我效能"],
    "批判性思维与高阶思维": ["批判性思维", "critical thinking", "问题解决", "高阶思维", "deep learning", "创造力"],
    "个性化与自适应学习": ["个性化", "adaptive", "年级", "年龄", "匹配", "差异", "精准"],
    "教师角色转变": ["教师角色", "角色", "转变", "转型", "从.*到", "teacher role"],
    "AI辅助工具有效性": ["有效", "无效", "AI工具", "辅助", "效果", "对比"],
    "伦理风险与隐私": ["伦理", "风险", "隐私", "bias", "公平", "偏见", "弱势"],
    "协作与互动学习": ["协作", "collaboration", "互动", "讨论", "同伴", "合作"],
    "元认知与反思": ["元认知", "metacognition", "反思", "自我评估", "self-regulation"],
    "即时反馈与评价": ["反馈", "评价", "即时", "过程性", "assessment"],
    "迁移与长期效果": ["迁移", "transfer", "长期", "保持", "retention", "持久"],
    "教师培训与专业发展": ["培训", "training", "教师发展", "professional", "专业发展"],
    "政策与框架": ["政策", "policy", "框架", "framework", "UNESCO", "OECD", "标准"],
    "技术接受与采纳": ["采纳", "adoption", "接受", "意愿", "使用", "resistance", "障碍"],
    "情感支持与社会连接": ["情感", "社会连接", "社会性", "social", "孤独", "归属"],
    "计算思维与编程": ["计算思维", "computational thinking", "编程", "coding", "STEM"],
}

def read_beliefs():
    """读取所有信念抽屉的核心表述"""
    beliefs = {}
    for f in BELIEF_DIR.glob("*.md"):
        num = f.stem  # e.g. "信念1-AI教育观"
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        # 提取核心表述
        core = ""
        match = search(r'核心表述[：:]\s*(.{10,200})', content)
        if match:
            core = match.group(1)
        beliefs[num] = {
            "核心表述": core,
            "文件": f.name
        }
    return beliefs

def classify_article(article):
    """判断一篇文章属于哪个主题"""
    text = (
        article.get("英文标题", "") +
        article.get("中文标题", "") +
        article.get("核心发现", "") +
        " ".join(article.get("数字指标", []))
    text_lower = text.lower()

    matched_themes = []
    for theme, keywords in THEME_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw.lower() in text_lower:
                score += 1
        if score >= 1:
            matched_themes.append((theme, score))

    matched_themes.sort(key=lambda x: -x[1])
    return matched_themes[:3] if matched_themes else [("其他", 0)]

def main():
    with open(POOL_FILE, 'r', encoding='utf-8') as f:
        pool = json.load(f)

    articles = pool["文章列表"]

    # 主题聚类
    theme_articles = defaultdict(list)
    for art in articles:
        themes = classify_article(art)
        primary_theme = themes[0][0] if themes else "其他"
        art["主题分类"] = primary_theme
        art["主题得分"] = themes
        theme_articles[primary_theme].append(art)

    # 输出主题分布
    theme_summary = {}
    for theme, arts in sorted(theme_articles.items(), key=lambda x: -len(x[1])):
        theme_summary[theme] = len(arts)

    print("=== 主题分布 ===")
    for theme, count in sorted(theme_summary.items(), key=lambda x: -x[1]):
        print(f"  {theme}: {count}篇")

    # 数字指标提取亮点
    print("\n=== 高价值数字指标（TOP50）===")
    all_numbers = []
    for art in articles:
        for num in art.get("数字指标", []):
            if any(kw in art.get("核心发现", "") for kw in ["提高", "提升", "减少", "增加", "下降", "降低"]):
                all_numbers.append({
                    "数字": num,
                    "标题": art.get("中文标题") or art.get("英文标题", "")[:40],
                    "DOI": art.get("DOI", "")
                })

    # 按数字大小排序（如果有可比较的数字）
    unique_numbers = []
    seen = set()
    for n in all_numbers:
        key = n["数字"][:20]
        if key not in seen:
            seen.add(key)
            unique_numbers.append(n)

    print(f"高价值指标共: {len(unique_numbers)} 条")

    # 按研究类型分布
    print("\n=== 研究类型分布 ===")
    type_count = defaultdict(int)
    for art in articles:
        type_count[art.get("研究类型", "未知")] += 1
    for t, c in sorted(type_count.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}篇")

    # 保存聚类结果
    result = {
        "聚类时间": "2026-04-05",
        "有效文章数": len(articles),
        "主题分布": theme_summary,
        "高价值数字指标": unique_numbers[:50],
        "研究类型分布": dict(type_count),
        "聚类后文章列表": articles
    }
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n已保存: {OUTPUT_FILE}")
    print(f"有效文章: {len(articles)} 篇")
    print(f"主题数: {len(theme_summary)} 个")

if __name__ == "__main__":
    import re
    main()
