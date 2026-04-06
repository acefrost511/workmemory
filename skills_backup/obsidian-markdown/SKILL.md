---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: 1d7e473c592e3eb28516a9ccaad18a05
    PropagateID: 1d7e473c592e3eb28516a9ccaad18a05
    ReservedCode1: 3045022059602a845a21bab26e4944cb420a7c66c2937c918d03a507b8260a4081547e2202210086db60eb57a42b297d8d5c5191a20d942453036b544f3fd81c30271b3eb2090b
    ReservedCode2: 3045022100ca5817f9c39df2fb988253d0f2a922c646559329bb4dbcd7aa9fa6d9fbcb9f2602205462b28f9a1fbd0dc342339c8d7854a472089174df8b43b6ce6c58487d60a5c9
description: Obsidian 风格 Markdown 创建与编辑，支持双向链接、嵌入、Mermaid图表等Obsidian特有语法
name: obsidian-markdown
---

# obsidian-markdown

## 功能
创建和编辑 Obsidian 风格的 Markdown 文档。

## Obsidian 特有语法

### 双向链接
```markdown
[[页面名称]]           # 链接到其他笔记
[[页面名称|显示文本]]  # 带显示文本的链接
[[页面名称#章节]]     # 链接到章节
```

### 嵌入
```markdown
![[页面名称]]           # 嵌入其他笔记内容
![[图像.png]]          # 嵌入图像
```

### 任务列表
```markdown
- [ ] 未完成任务
- [x] 已完成任务
```

### 提示块（Callouts）
```markdown
> [!note] 标题
> 内容

类型：note, tip, warning, danger, bug, quote, example
```

### 图表（Mermaid）
````markdown
```mermaid
graph TD
    A --> B
```
````

### 表格
```markdown
| 列1 | 列2 |
|---|---|
| 内容 | 内容 |
```

### 脚注
```markdown
这里有脚注[^1]

[^1]: 脚注内容
```

### YAML前置元数据
```markdown
---
title: 标题
tags: [tag1, tag2]
date: 2026-03-14
---
```

### 内联标签
```markdown
#tag           // 标签
##tag          // 嵌套标签
```

### 高亮
```markdown
==高亮文本==
```

### 撤销线
```markdown
~~删除文本~~
```

## Obsidian Flavored Markdown 特点

1. **Wiki式链接**：`[[双链]]`
2. **嵌入语法**：`![[嵌入]]`
3. **Callout提示块**：>`[!类型]`
4. **Mermaid图表**：代码块mermaid
5. **任务列表**：`- [ ]`
6. **内联标签**：`#tag`

## 使用场景
- 创建Obsidian笔记
- 迁移内容到Obsidian
- 生成Obsidian兼容的Markdown

## 输出格式
保持标准Markdown兼容性，同时使用Obsidian扩展语法。
