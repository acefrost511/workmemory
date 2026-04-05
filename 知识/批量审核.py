#!/usr/bin/env python3
"""
批量审核脚本：一次性对.pending目录下所有文件执行review，节省启动开销
"""
import os, sys, time
from pathlib import Path

PENDING = Path("/workspace/knowledge/原文库/.pending")
REVIEWER = Path("/workspace/.review.py")
RESULT_FILE = Path("/workspace/.review_batch_log.txt")

log_lines = []

def log(msg):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    log_lines.append(line)

def run_review(filepath):
    """同步调用review.py，返回码0=通过，1=失败"""
    import subprocess
    result = subprocess.run(
        ["python3", str(REVIEWER), str(filepath)],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode, result.stdout, result.stderr

def main():
    pending = sorted(PENDING.glob("*.md"))
    if not pending:
        log("pending目录为空，无文件待审核")
        return
    
    log(f"发现{len(pending)}个待审核文件")
    
    passed = 0
    deleted = 0
    
    for f in pending:
        log(f"审核: {f.name}")
        try:
            code, out, err = run_review(f)
            if code == 0:
                passed += 1
                log(f"  PASS")
            else:
                deleted += 1
                log(f"  FAIL")
        except Exception as e:
            log(f"  ERROR: {e}")
            deleted += 1
    
    log(f"\n审核完成: 通过{passed} 删除{deleted}")
    
    # 写入日志
    with open(RESULT_FILE, "w") as f:
        f.write("\n".join(log_lines))
    log(f"日志: {RESULT_FILE}")

if __name__ == "__main__":
    main()
