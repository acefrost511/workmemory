# 笔记库 · 元数据Schema规范
> 定义每条笔记的标准格式，所有笔记必须包含以下字段

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
tags:
  - 主题标签1
  - 主题标签2
related_topics:
  - topic_id_1
  - topic_id_2
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
quality_score: 1-5
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
| tags | ✅ | 主题标签，与精选库对齐 |
| related_topics | ○ | 对应精选库中的主题 |
| related_notes | ○ | 与其他笔记的双向关联 |
| entities | ○ | 识别的关键人名/概念 |
| keywords | ○ | 可被检索的关键词 |
| status | ✅ | raw=待处理/processed=已清洗/linked=已关联 |
| summary | ✅ | 一句话说明价值，≤100字 |
| quality_score | ○ | 质量评分（1-5），臣评估 |

## 质量评分标准

- 5分：有独特洞察、有具体数据或案例、可直接写文章
- 4分：有观点、有逻辑、有应用场景
- 3分：有想法、结构尚可、需要补充
- 2分：碎片化想法、需要进一步加工
- 1分：口水话为主、保留价值低

## 关联规则

- `related_notes`：笔记与笔记之间，同主题/同来源/相反观点→自动关联
- `related_topics`：笔记与精选库之间，通过tags匹配
- 臣每次处理笔记时，必须维护`related_notes`和`related_topics`字段
