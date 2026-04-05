#!/usr/bin/env python3
"""
全面审核脚本 v2.0
加严版：摘要必须≥200字英文或≥120字中文，且有数字/方法/RCT等实质证据词
"""
from pathlib import Path
import re

LIBRARY = Path("/workspace/knowledge/原文库")
AUDIT_KW = ["RCT", "随机对照", "meta-analysis", "元分析", "样本", "学生", "教师",
            "效果量", "p<", "显著", "实验", "研究", "数据", "分数", "percent", "%"]
K12_AI_KW = ["K-12", "k12", "classroom", "student", "teacher", "learner",
              "education", "AI", "LLM", "ChatGPT", "pedagogy", "instruction",
              "电化教育", "课程", "教学", "学生", "教师", "课堂", "人工智能教育", "AI教育"]

def has_substance(content):
    """实质摘要判断：字数+证据词双条件"""
    # 英文摘要
    en = re.search(r'(?:Abstract|ABSTRACT)[：:\s]*\n?([\s\S]{100,})', content)
    if en and len(en.group(1).strip()) >= 200:
        text = en.group(1).lower()
        if any(kw.lower() in text for kw in AUDIT_KW):
            return True, f"英文摘要{len(en.group(1))}字+证据词"
    # 中文摘要
    cn = re.search(r'摘要[：:]\s*([^\n]{50,})', content)
    if cn and len(cn.group(1).strip()) >= 120:
        text = cn.group(1).lower()
        if any(kw.lower() in text for kw in AUDIT_KW):
            return True, f"中文摘要{len(cn.group(1))}字+证据词"
    # 核心发现
    finding = re.search(r'(?:核心发现|关键发现)[：:]\s*([\s\S]{50,})', content)
    if finding and len(finding.group(1).strip()) >= 80:
        text = finding.group(1).lower()
        if any(kw.lower() in text for kw in AUDIT_KW):
            return True, f"核心发现{len(finding.group(1))}字+证据词"
    return False, None

def is_k12_related(content):
    score = sum(1 for kw in K12_AI_KW if kw.lower() in content.lower())
    return score >= 2, score

def audit_library():
    all_files = list(LIBRARY.glob("*.md"))
    print(f"开始审核: {len(all_files)} 篇")
    
    passed = []; deleted = []; reason_map = {}
    
    for f in all_files:
        try:
            c = f.read_text(encoding="utf-8", errors="ignore")
        except:
            deleted.append((f.name, "读取错误"))
            continue
        
        sz = len(c)
        if sz < 500:
            deleted.append((f.name, f"极小文件{sz}B"))
            continue
        
        substance, sub_type = has_substance(c)
        related, rel_score = is_k12_related(c)
        
        if not substance:
            deleted.append((f.name, f"无实质摘要({sub_type or 'NA'})"))
            reason_map[f.name] = f"无实质"
            continue
        if not related:
            deleted.append((f.name, f"主题不相关(得分{rel_score})"))
            reason_map[f.name] = "主题不符"
            continue
        
        # 通过：加标记（无审核状态才加）
        if "**审核状态**" not in c:
            marker = f"\n\n**审核状态**：✅已通过审核\n**触动标记**：○未标记\n**审核日期**：2026-04-05"
            with open(f, "a", encoding="utf-8") as fh:
                fh.write(marker)
        
        # 触动状态
        if "✅有触动" in c or "触动" in c[:300]:
            touch = "✅有触动"
        elif "❌无触动" in c:
            touch = "❌无触动"
        else:
            touch = "○未标记"
        
        passed.append((f.name, sub_type, touch))
    
    print(f"\n通过: {len(passed)} | 删除: {len(deleted)}")
    print("\n=== 删除列表 ===")
    for n, r in deleted:
        print(f"  ❌ [{r}] {n}")
    print("\n=== 通过列表(前30) ===")
    for n, st, tc in passed[:30]:
        print(f"  ✅ {st} | {tc} | {n}")
    print(f"\n还有{len(passed)-30}篇...")
    
    return passed, deleted, reason_map

if __name__ == "__main__":
    p, d, rm = audit_library()
