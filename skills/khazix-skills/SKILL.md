---
name: khazix-skills
description: AI技能库生命周期管理工具集
---

# Khazix-Skills 技能库

管理AI技能生命周期的工具集合。

## 包含技能

| 技能 | 功能 |
|------|------|
| github-to-skills | 将GitHub仓库转换为AI技能 |
| skill-manager | 技能生命周期管理 |
| skill-evolution-manager | 基于反馈持续改进技能 |

## 使用方法

### 1. 创建新技能
/github-to-skills <仓库地址>

### 2. 管理技能
/skill-manager check   # 检查更新
/skill-manager list    # 列出技能

### 3. 演进技能
/evolve                # 保存经验到技能

## 完整工作流
```
github-to-skills → skill-manager → skill-evolution-manager
   创建              维护              演进
```

详见各子技能SKILL.md
