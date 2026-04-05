#!/usr/bin/env python3
"""标记文章为已推送"""
from pathlib import Path

推送列表 = [
    "10.3390_systems13100840.md",
    "10.3390_computers15010049_AI_K12_teacher_PD_MDPI.md",
    "10.3389_feduc.2025.1671306_teacher_training_AI_literacy_Germany.md",
    "10.1007_s11423-025-10568-w.md",
    "10.1007_s10639-025-13429-4.md",
    "10.1007_s10639-025-13699-y.md",
    "10.3390_educsci15091186.md",
    "10.3390_educsci16010136.md",
    "10.1007_s11423-025-10566-y.md",
    "10.1080_10494820_2026_2647984.md",
]

lib = Path("/workspace/knowledge/原文库")
marked = []
already = []

for fn in 推送列表:
    f = lib / fn
    if not f.exists():
        print(f"不存在: {fn}")
        continue
    c = f.read_text(errors="ignore")
    marker = "**状态：已推送 | 推送日期：2026-04-05**"
    if marker in c:
        already.append(fn)
    else:
        with open(f, "a", encoding="utf-8") as fh:
            fh.write(f"\n\n{marker}")
        marked.append(fn)

print(f"新增标记: {len(marked)}")
print(f"已有标记: {len(already)}")
