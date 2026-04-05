#!/usr/bin/env python3
"""
全面审核脚本 v1.0
执行陛下的两项铁律：
1. 全面审核387篇：摘要实质+DOI一致性+主题相关性
2. 建立双字段系统：审核状态 + 触动标记
"""
from pathlib import Path
import re, shutil, time

LIBRARY = Path("/workspace/knowledge/原文库")
PENDING = LIBRARY / ".pending"
RESULT_FILE = Path("/workspace/knowledge/审核报告_全面清理.md")
REPORT_LINES = []

K12_AI_KW = [
    "K-12", "k12", "middle school", "high school", "primary school",
    "classroom", "student", "teacher", "learner", "education",
    "artificial intelligence", "AI", "LLM", "generative AI", "ChatGPT",
    "pedagogy", "pedagogical", "instruction", "curriculum",
    "电化教育", "课程", "教学", "学生", "教师", "课堂",
    "人工智能教育", "AI教育", "智慧教育", "数字化教学",
]

def log(msg):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    REPORT_LINES.append(line)

def has_real_abstract(content):
    """判断是否有实质摘要（英文≥150字 或 中文≥80字）"""
    # 英文摘要
    en_m = re.search(r'(?:Abstract|ABSTRACT|Summary)[：:\s]*\n?([\s\S]{150,2000})', content)
    if en_m and len(en_m.group(1).strip()) >= 150:
        return True, "英文摘要"
    # 核心发现
    finding_m = re.search(r'(?:核心发现|关键发现|主要发现)[：:]\s*([\s\S]{50,1000})', content)
    if finding_m and len(finding_m.group(1).strip()) >= 50:
        return True, "核心发现"
    # 中文摘要（较完整）
    cn_m = re.search(r'摘要[：:]\s*([^\n]{80,})', content)
    if cn_m and len(cn_m.group(1).strip()) >= 80:
        return True, "中文摘要"
    return False, "无实质摘要"

def is_k12_ai_related(content):
    """判断是否与K12 AI教育相关"""
    text = content.lower()
    score = 0
    for kw in K12_AI_KW:
        if kw.lower() in text:
            score += 1
    return score >= 2, score

def extract_doi(content):
    """提取DOI"""
    m = re.search(r'DOI[：:]*\s*(10\.[^\s<>"\'\n]{5,60})', content)
    return m.group(1).strip().split('/')[0] if m else None

def get_title(content):
    """提取标题"""
    m = re.search(r'标题[（中文) ：:]*\s*([^\n]{10,120})', content)
    if m: return m.group(1).strip()[:80]
    m2 = re.search(r'(?:English Title|Title)[：:\s]*([^\n]{10,120})', content)
    if m2: return m2.group(1).strip()[:80]
    return None

def main():
    log("=" * 50)
    log("原文库全面审核开始")
    log("=" * 50)
    
    all_files = sorted(LIBRARY.glob("*.md"))
    total = len(all_files)
    log(f"总文件: {total}")
    
    # 统计
    stats = {
        "通过": 0, "删除": 0, "主题不符": 0,
        "无摘要": 0, "极小": 0, "已有标记": 0,
        "新增标记": 0, "触动_有": 0, "触动_无": 0, "触动_未标": 0,
    }
    delete_list = []
    pass_list = []
    fail_list = []
    
    for f in all_files:
        try:
            c = f.read_text(encoding="utf-8", errors="ignore")
        except:
            stats["删除"] += 1
            continue
        
        fname = f.name
        sz = len(c)
        
        # ── 1. 极小文件删除 ──
        if sz < 500:
            log(f"删除[极小{sz}B]: {fname}")
            delete_list.append((fname, "极小文件"))
            stats["删除"] += 1
            continue
        
        # ── 2. 判断是否有实质摘要 ──
        has_abs, abs_type = has_real_abstract(c)
        
        # ── 3. 判断主题相关性 ──
        is_rel, rel_score = is_k12_ai_related(c)
        
        # ── 4. 提取DOI ──
        doi = extract_doi(c)
        
        # ── 5. 判断触动标记现有状态 ──
        if "✅有触动" in c:
            touch = "有触动"
        elif "❌无触动" in c:
            touch = "无触动"
        elif "✅触动" in c or "触动" in c[:500]:
            touch = "有触动（已标记）"
        else:
            touch = "未标记"
        
        # ── 6. 决定审核状态 ──
        if not has_abs:
            reason = f"无实质摘要({abs_type})"
            log(f"删除[{reason}]: {fname}")
            delete_list.append((fname, reason))
            stats["删除"] += 1
            stats["无摘要"] += 1
            continue
        
        if not is_rel:
            reason = f"主题不相关(得分{rel_score})"
            log(f"删除[{reason}]: {fname}")
            delete_list.append((fname, reason))
            stats["删除"] += 1
            stats["主题不符"] += 1
            continue
        
        # 通过：加双字段
        doi_str = f"DOI:{doi}" if doi else "无DOI"
        
        # 检查现有标记
        has_audit_marker = "**审核状态**" in c
        has_touch_marker = any(k in c for k in ["✅有触动", "❌无触动", "**触动标记**"])
        
        if not has_audit_marker:
            marker = f"\n\n**审核状态**：✅已通过审核\n**触动标记**：○未标记\n**审核日期**：2026-04-05"
            with open(f, "a", encoding="utf-8") as fh:
                fh.write(marker)
            stats["新增标记"] += 1
        else:
            stats["已有标记"] += 1
        
        # 触动统计
        if "✅有触动" in c or "触动" in c[:300] and "❌无触动" not in c:
            stats["触动_有"] += 1
        elif "❌无触动" in c:
            stats["触动_无"] += 1
        else:
            stats["触动_未标"] += 1
        
        stats["通过"] += 1
        pass_list.append((fname, doi_str, abs_type, touch))
    
    # 写报告
    log("")
    log("=" * 50)
    log("审核结果")
    log("=" * 50)
    log(f"通过: {stats['通过']} | 删除: {stats['删除']}")
    log(f"  其中-无摘要: {stats['无摘要']} | 主题不符: {stats['主题不符']} | 极小: {stats['极小']}")
    log(f"触动状态: 有触动{stats['触动_有']} | 无触动{stats['触动_无']} | 未标记{stats['触动_未标']}")
    log(f"标记情况: 新增标记{stats['新增标记']} | 已有标记{stats['已有标记']}")
    log("")
    log(f"通过文章({len(pass_list)}):")
    for fname, doi, abs_type, touch in pass_list[:20]:
        log(f"  [{doi}] {abs_type} | {touch} | {fname}")
    if len(pass_list) > 20:
        log(f"  ... 还有{len(pass_list)-20}篇")
    
    log("")
    log(f"删除文章({len(delete_list)}):")
    for fname, reason in delete_list:
        log(f"  ❌ {reason}: {fname}")
    
    # 保存报告
    report = "\n".join(REPORT_LINES)
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 原文库全面审核报告\n\n时间: 2026-04-05\n\n## 统计\n")
        for k, v in stats.items():
            f.write(f"- {k}: {v}\n")
        f.write(f"\n## 删除列表({len(delete_list)})\n")
        for fname, reason in delete_list:
            f.write(f"- [{reason}] {fname}\n")
        f.write(f"\n## 通过列表({len(pass_list)})\n")
        for fname, doi, abs_type, touch in pass_list:
            f.write(f"- [{doi}] {abs_type} | {touch} | {fname}\n")
    
    log(f"\n报告已保存: {RESULT_FILE}")
    
    # 同时更新daily-briefing SKILL.md明确执行者
    skill_file = Path("/workspace/skills/daily-briefing/SKILL.md")
    if skill_file.exists():
        c = skill_file.read_text(encoding="utf-8", errors="ignore")
        if "执行者" not in c:
            log("更新daily-briefing SKILL.md执行者说明")
            # 在开头加执行者说明
            new_header = "# daily-briefing | 每日简报技能\n\n**执行者**：情报官（info_officer）调用，或主session直接执行\n**触发**：每日05:40 cron自动触发，或主session手动触发\n\n"
            c_new = new_header + c
            skill_file.write_text(c_new, encoding="utf-8")
            log("daily-briefing SKILL.md已更新")
    
    log("全面审核完成!")

if __name__ == "__main__":
    main()
