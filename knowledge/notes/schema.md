# 笔记库 · 元数据Schema规范
> 定义每条笔记的标准格式，所有笔记必须包含以下字段
> 更新：2026-03-25 陛下指示

## 存储位置
`/workspace/knowledge/notes/YYYY-MM-DD_{slug}.md`

## 文件格式（YAML Frontmatter + Markdown正文）

```yaml
---
id: notes_{uuid}
title: "笔记标题（≤50字）"
date: "YYYY-MM-DD"
source: voice | text | article | conversation | research
speaker: 陛下
raw_content: |
  原始输入原文（去除口水话和转录后的一一对应保留）
  不得删改，仅做口语词去除和基本转写
processed_content: |
  清洗后的正文内容
  去除口水话、修正口误、还原完整语义
tags:
  - 主题标签1
  - 主题标签2
matched_topics:
  - topic_title: "精选库主题名称"
    matching_score: 0.85
    match_reason: "为什么匹配"
related_notes:
  - notes_xxx_id
  - notes_yyy_id
entities:
  - 人名/机构名
  - 关键概念
keywords:
  - 关键词1
  - 关键词2
status: raw | processed | linked
summary: "一句话摘要（≤100字）"
---
正文内容（清洗后）
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| id | ✅ | 自动生成UUID |
| title | ✅ | 从内容提炼，≤50字 |
| date | ✅ | 笔记产生日期 |
| source | ✅ | 入口：录音/文本/文章/对话/研究 |
| speaker | ✅ | 固定：陛下 |
| raw_content | ✅ | 原文一字不改保存，口语词只去除不修改原意 |
| processed_content | ✅ | 清洗后正文，去除口水话+修正口误 |
| tags | ✅ | 主题标签，与精选库对齐 |
| matched_topics | ✅ | 与精选库主题的匹配结果，含匹配得分 |
| related_notes | ○ | 与其他笔记的双向关联 |
| entities | ○ | 识别的关键人名/概念 |
| keywords | ○ | 可被检索的关键词 |
| status | ✅ | raw=待处理/processed=已清洗/linked=已关联 |
| summary | ✅ | 一句话说明价值，≤100字 |

## 匹配得分标准（topic_matching_score）

每条笔记必须与精选库主题进行匹配计算，结果存入matched_topics字段：

- **matching_score 0.9-1.0**：直接命中精选库已有主题，高度匹配
- **matching_score 0.6-0.89**：部分匹配，可作为已有主题的补充素材
- **matching_score 0.3-0.59**：涉及相关领域，可作为潜在新主题候选
- **matching_score < 0.3**：与精选库无明显关联，归入通用知识库

matching_score由臣分析笔记内容与精选库各主题的核心关键词重叠度、观点契合度综合判定。

## 关联规则

- `related_notes`：笔记与笔记之间，同主题/同来源/相反观点→自动关联
- `matched_topics`：笔记与精选库之间，通过matched_topics字段记录匹配结果
- 臣每次处理笔记时，必须维护`matched_topics`和`related_notes`字段
