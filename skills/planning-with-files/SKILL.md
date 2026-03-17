---
name: planning-with-files
description: 实现Manus风格的持久化Markdown规划工作流
author: OthmanAdi
version: 1.0.0
homepage: https://github.com/OthmanAdi/planning-with-files
triggers:
  - "任务规划"
  - "复杂任务"
metadata: {"clawdbot":{"emoji":"📋"}}
---

# planning-with-files - Manus风格规划

## 核心理念
- 将Markdown文件作为磁盘上的"工作记忆"

## 创建的文件
- task_plan.md（追踪阶段和进度）
- findings.md（存储研究发现）
- progress.md（会话日志和测试结果）

## 适用场景
- 需要超过5次工具调用的复杂多步骤任务

## 安装
`npx skills add https://github.com/OthmanAdi/planning-with-files --skill planning-with-files`
