---
name: docx
description: "Create, read, edit Word documents (.docx). For reports, memos, letters, templates with formatting."
---

# docx

## 功能
创建、编辑Word文档

## 触发条件
- 提及 "Word doc"、"word document"、".docx"
- 要求生成报告、备忘录、信函、模板
- 提取或重组.docx内容
- 插入/替换图片
- 查找替换
- 追踪修订或评论

## 核心要点

### 创建新文档
```javascript
const { Document, Packer, Paragraph, TextRun } = require('docx');
const doc = new Document({ sections: [{ children: [] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### 关键规则
1. **页面尺寸**：docx-js默认A4，美帝用US Letter (12240 x 15840 DXA)
2. **Never use \n**：用独立的Paragraph元素
3. **Never use unicode bullets**：用LevelFormat.BULLET
4. **PageBreak必须在Paragraph内**
5. **表格需要dual widths**：columnWidths + cell width都用DXA
6. **图片必须指定type**：png/jpg等
7. **Shading用CLEAR不是SOLID**

### 编辑现有文档
1. **Unpack**：`python scripts/office/unpack.py doc.docx unpacked/`
2. **Edit XML**：编辑unpacked/word/下的XML
3. **Pack**：`python scripts/office/pack.py unpacked/ output.docx`

### 颜色编码（财务模型）
- 蓝色：硬编码输入
- 黑色：公式
- 绿色：同工作表链接
- 红色：外部链接
- 黄色背景：关键假设

### 数字格式
- 年份：用文本 "2024"
- 货币：$#,##0，标题要写单位
- 零：显示 "-"
- 负数：用括号 (123)
