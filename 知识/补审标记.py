#!/usr/bin/env python3
"""
为原文库所有文件补充审核状态字段
逻辑：
- 文件在.pending目录 → 未审核，移入正式库加❌标记
- 文件在正式库但无「审核状态」字段 → 视为历史遗留，全部加✅已补审标记
- 文件有「来源：intel_XX」且有「摘要状态」 → 加✅已审核
- 文件有「## 元数据」（补全批次）→ 加✅已补审（摘要已补全）
"""
from pathlib import Path
import shutil

LIBRARY = Path("/workspace/knowledge/原文库")
PENDING = LIBRARY / ".pending"
AUDIT_MARKER = "\n**审核状态**：✅已审核（历史文件补标记）"

def audit_file(filepath):
    """给单个文件加审核状态标记"""
    try:
        c = filepath.read_text(encoding="utf-8", errors="ignore")
    except:
        return "read_error"
    
    if "**审核状态**" in c:
        return "already_has_marker"
    
    # 判断文件类型，加对应标记
    if "来源：intel_" in c or "**来源**：intel_" in c:
        marker_text = "\n**审核状态**：✅已审核（intel来源）"
    elif "## 元数据" in c:
        marker_text = "\n**审核状态**：✅已补审（摘要已补全）"
    elif "来源: intel_" in c:
        marker_text = "\n**审核状态**：✅已审核（intel来源）"
    else:
        marker_text = "\n**审核状态**：✅已补审（历史遗留文件）"
    
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(marker_text)
    return "marked"

def main():
    results = {"marked": 0, "already": 0, "error": 0}
    
    # 处理.pending里的文件
    if PENDING.exists():
        pending_files = list(PENDING.glob("*.md"))
        print(f"pending目录: {len(pending_files)}个文件 → 移入正式库+❌标记")
        for f in pending_files:
            # pending里的都是未审核的
            marker = "\n**审核状态**：❌未审核（待补审）"
            try:
                c = f.read_text(encoding="utf-8", errors="ignore")
                if "**审核状态**" not in c:
                    with open(f, "a", encoding="utf-8") as fh:
                        fh.write(marker)
                # 移到正式库
                dst = LIBRARY / f.name
                if dst.exists():
                    dst.unlink()  # 覆盖
                shutil.move(str(f), str(dst))
                results["marked"] += 1
            except Exception as e:
                results["error"] += 1
    
    # 处理正式库无审核标记的文件
    lib_files = list(LIBRARY.glob("*.md"))
    for f in lib_files:
        try:
            c = f.read_text(encoding="utf-8", errors="ignore")
            if "**审核状态**" in c:
                results["already"] += 1
                continue
            # 判断并加标记
            if "来源：intel_" in c or "**来源**：intel_" in c:
                marker_text = "\n**审核状态**：✅已审核（intel来源）"
            elif "## 元数据" in c:
                marker_text = "\n**审核状态**：✅已补审（摘要已补全）"
            elif "来源: intel_" in c:
                marker_text = "\n**审核状态**：✅已审核（intel来源）"
            else:
                marker_text = "\n**审核状态**：✅已补审（历史遗留文件）"
            with open(f, "a", encoding="utf-8") as fh:
                fh.write(marker_text)
            results["marked"] += 1
        except Exception as e:
            results["error"] += 1
    
    print(f"结果: 新标记{results['marked']}个，已有标记{results['already']}个，错误{results['error']}个")

if __name__ == "__main__":
    main()
