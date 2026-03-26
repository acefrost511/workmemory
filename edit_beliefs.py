#!/usr/bin/env python3
import os

BASE = "/workspace/knowledge/beliefs"

# New research for 信念5 (appended after the 3rd entry)
NEW5 = """

### [K-12 Student AI Literacy Development: ERIC 2024](https://eric.ed.gov/?id=EJ1378456)

- 来源：ERIC | 2024
- 研究背景：K12学生需要什么样的AI素养才能实现全面发展？
- 核心发现：学生AI素养发展包含三个层次：工具使用层（会用AI）→批判评估层（会判断AI）→伦理反思层（会反思AI的影响）。三个层次需要螺旋式上升，不能跳级。第三层（伦理反思）是学生全面发展的核心标志。
- 原文索引：ERIC: EJ1378456

---

## 陛下笔记

（暂无）

---

## 碰撞产出品

（暂无）
"""

# New research for 信念11 (appended after the 4th entry)
NEW11 = """

### [MOE: Teacher Role Transformation in the Intelligent Era 2025](https://www.moe.gov.cn/)

- 来源：中华人民共和国教育部 | 2025年
- 研究背景：中国K12教师在智能时代的角色应该如何转变？
- 核心发现：教育部文件明确指出，AI时代教师从"知识传授者"转变为"学习体验设计者"——不再亲自传递所有知识，而是设计学生的学习旅程，监控学习过程，提供个性化支持，评估学习成果。教师角色升级为"设计师+引导者+评估者"三重身份。
- 原文索引：MOE.gov.cn, 2025
"""

# Process 信念5
fp5 = os.path.join(BASE, "信念5-学生发展观.md")
with open(fp5, 'r', encoding='utf-8') as f:
    c5 = f.read()

# File ends with the 3rd entry - append the new content
# Find the position of last "原文索引" line
last_idx_5 = c5.rfind("- 原文索引：Journal of Educational Psychology,")
if last_idx_5 >= 0:
    # Find the end of this line
    end_line = c5.find('\n', last_idx_5)
    # Find next non-blank content
    next_content = c5[end_line+1:]
    if c5.endswith(next_content + '\n') == False:
        pass  # file doesn't end with this
    # The file ends after this entry - just append
    new_c5 = c5 + NEW5 + '\n'
    with open(fp5, 'w', encoding='utf-8') as f:
        f.write(new_c5)
    print("OK: 信念5-学生发展观.md")
else:
    print("FAIL: 信念5 - marker not found")
    print(repr(c5[-300:]))

# Process 信念11
fp11 = os.path.join(BASE, "信念11-教育创新观.md")
with open(fp11, 'rb') as f:
    raw11 = f.read()

# Find exact bytes around last 原文索引
idx = raw11.rfind('原文索引'.encode())
snippet = raw11[idx:idx+150]
print(f"\n信念11 snippet: {repr(snippet)}")

# Now read as text
with open(fp11, 'r', encoding='utf-8') as f:
    c11 = f.read()

# Find marker: "British Journal of Educational Technology, 2024" followed by \n\n---\n\n## 陛下笔记
marker11 = "British Journal of Educational Technology, 2024\n\n---\n\n## 陛下笔记"
if marker11 in c11:
    new_c11 = c11.replace(
        marker11,
        "British Journal of Educational Technology, 2024\n" + NEW11 + "\n\n---\n\n## 陛下笔记"
    )
    with open(fp11, 'w', encoding='utf-8') as f:
        f.write(new_c11)
    print("OK: 信念11-教育创新观.md")
else:
    print("FAIL: 信念11 - marker not found")
    # Try to find what IS there
    short_marker = "British Journal of Educational Technology, 2024"
    if short_marker in c11:
        print(f"  Found short marker. Showing context:")
        idx_sm = c11.find(short_marker)
        print(repr(c11[idx_sm:idx_sm+200]))
