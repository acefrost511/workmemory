---
name: pptx
description: Create, read, edit PowerPoint presentations (.pptx)
---

# pptx

## 功能
创建、编辑PPT演示文稿

## 触发条件
提及 "deck"、"slides"、".pptx"

## 设计原则

### 配色方案
| 主题 | 主色 | 辅色 |
|------|------|------|
| Midnight | #1E2761 | #CADCFC |
| Forest | #2C5F2D | #97BC62 |
| Coral | #F96167 | #F9E795 |
| Ocean | #065A82 | #1C7293 |

### 每张幻灯片需视觉元素
- 图片、图表、图标
- 纯文本幻灯片易被遗忘

### 排版
- 标题：36-44pt
- 正文：14-16pt
- 边距：0.5"

### 禁止
- 重复布局
- 默认蓝色
- 纯文本幻灯片
- 标题下装饰线

## 质量检查
```bash
python -m markitdown output.pptx
# 转图片检查
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```
