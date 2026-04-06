---
name: pdf
description: PDF manipulation - extract text/tables, create, merge/split, fill forms
---

# pdf

## 功能
PDF处理：提取文本表格、创建、合并/拆分、表单填写

## 核心库

### pypdf - 基础操作
```python
from pypdf import PdfReader, PdfWriter

# 读取
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# 提取文本
text = ""
for page in reader.pages:
    text += page.extract_text()

# 合并
writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)
writer.write("merged.pdf")
```

### pdfplumber - 文本和表格提取
```python
import pdfplumber

# 提取文本
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()

# 提取表格
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
```

### reportlab - 创建PDF
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
c.drawString(100, 750, "Hello World!")
c.save()
```

## 命令行工具

### pdftotext
```bash
pdftotext -layout input.pdf output.txt  # 保持布局
```

### qpdf
```bash
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
qpdf input.pdf --rotate=+90:1 -- output.pdf
```

## 常见任务

### OCR扫描件
```python
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path('scanned.pdf')
for image in images:
    text += pytesseract.image_to_string(image)
```

### 添加水印
```python
from pypdf import PdfReader, PdfWriter
watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()
for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)
```

### 密码保护
```python
writer.encrypt("userpassword", "ownerpassword")
```

## 快速参考
| 任务 | 工具 |
|------|------|
| 合并PDF | pypdf |
| 拆分PDF | pypdf |
| 提取文本 | pdfplumber |
| 提取表格 | pdfplumber |
| 创建PDF | reportlab |
| OCR | pytesseract |
