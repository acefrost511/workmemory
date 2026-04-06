---
name: xlsx
description: Create, edit, analyze spreadsheets (.xlsx, .xlsm, .csv). Formulas, formatting, data analysis.
---

# xlsx

## 功能
创建、编辑、分析电子表格

## 触发条件
- 处理 .xlsx、.xlsm、.csv、.tsv
- 创建带公式和格式的表格
- 数据分析和可视化

## 零公式错误
所有Excel文件必须零错误：#REF!、#DIV/0!、#VALUE!、#N/A、#NAME?

## 颜色编码（财务模型）
- 蓝色：硬编码输入
- 黑色：公式
- 绿色：同工作表链接
- 红色：外部链接
- 黄色背景：关键假设

## 数字格式
- 年份：用文本 "2024"
- 货币：$#,##0，标题写单位
- 零：显示 "-"
- 负数：括号 (123)

## 用公式，不用硬编码
```python
# ❌ 错误：硬编码
sheet['B10'] = 5000

# ✅ 正确：用公式
sheet['B10'] = '=SUM(A1:A10)'
```

## pandas（数据分析）
```python
import pandas as pd
df = pd.read_excel('file.xlsx')
df.to_excel('output.xlsx', index=False)
```

## openpyxl（公式+格式）
```python
from openpyxl import Workbook
wb = Workbook()
sheet = wb.active
sheet['A1'] = '=SUM(B1:B10)'
wb.save('output.xlsx')
```

## 公式重算（必须）
```bash
python recalc.py output.xlsx
```

## 验证检查
- 测试2-3个样本引用
- 检查列映射（列64=BL）
- 行偏移（DataFrame行5=Excel行6）
- 除零检查
