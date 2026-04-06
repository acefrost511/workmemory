---
name: skill-evolution-manager
description: 基于用户反馈和会话洞察持续改进技能
---

# skill-evolution-manager

## 功能
基于用户反馈持续改进AI技能。

## 核心概念

1. **Session Review** - 对话后分析技能表现
2. **Experience Extraction** - 将反馈转为evolution.json
3. **Smart Stitching** - 将最佳实践持久化到SKILL.md

## 使用方法

```
/evolve
```

或自然语言："Save this experience to the skill"

## 工作流程

1. **Review（审查）**
   - Agent分析什么有效/无效
   - 识别问题和改进点

2. **Extract（提取）**
   - 创建结构化JSON
   - 包含：偏好、修复、自定义提示

3. **Persist（持久化）**
   - 合并到`evolution.json`

4. **Stitch（缝合）**
   - 用最佳实践更新`SKILL.md`

## 脚本

| 脚本 | 用途 |
|------|------|
| merge_evolution.py | 增量合并新经验数据 |
| smart_stitch.py | 生成/更新SKILL.md最佳实践 |
| align_all.py | 批量重新缝合所有技能 |

## evolution.json 结构
```json
{
  "preferences": [...],
  "fixes": [...],
  "custom_prompts": [...],
  "last_updated": "2026-03-14"
}
```
