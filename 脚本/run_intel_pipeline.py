#!/usr/bin/env python3
"""
情报官全流程执行脚本
执行12路情报搜索 → 存储结果 → 输出摘要
"""
import subprocess
import json
import time
import os
import re
from datetime import datetime

OUT_DIR = "/workspace/knowledge/原文库"
os.makedirs(OUT_DIR, exist_ok=True)

LOG_FILE = "/workspace/logs/intel_pipeline.log"
os.makedirs("/workspace/logs", exist_ok=True)

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def run_search(query, num_results=10):
    """用curl调用内部搜索API"""
    import urllib.request, urllib.parse
    
    # 尝试调用 OpenClaw 的 batch_web_search via internal API
    # 实际上用 subprocess + curl 模拟搜索
    cmd = [
        "curl", "-s", "-X", "POST", 
        "http://127.0.0.1:8080/api/search/batch",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"queries": [{"query": query, "num_results": num_results}]})
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout)
    except:
        pass
    return None

def save_result(filename, content):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w") as f:
        f.write(content)
    return path

# ============================================================
# 第一批搜索 (intel_01, intel_02, intel_03)
# ============================================================
log("===== 第一批搜索启动 (intel_01/02/03) =====")

# intel_01: Computers & Education, Education and Information Technologies, BJET
search_01 = {
    "name": "intel_01",
    "journal": "Computers & Education / Education and Information Technologies / BJET",
    "queries": [
        "Computers and Education AI K-12 education site:sciencedirect.com",
        "Education and Information Technologies AI K-12 site:mdpi.com",
        "British Journal Educational Technology AI K-12 site:tandfonline.com",
    ]
}

# intel_02: Interactive Learning Environments, CALL, ETRD, iJET
search_02 = {
    "name": "intel_02", 
    "journal": "Interactive Learning Environments / CALL / ETRD / iJET",
    "queries": [
        "Interactive Learning Environments AI K-12 site:tandfonline.com",
        "Computer Assisted Language Learning AI K-12 site:tandfonline.com",
        "Educational Technology Research Development AI K-12 site:link.springer.com",
        "International Journal Emerging Technologies Learning iJET AI K-12 site:doaj.org",
    ]
}

# intel_03: arXiv cs.AI/cs.EDU, ERIC
search_03 = {
    "name": "intel_03",
    "journal": "arXiv cs.AI/cs.EDU / ERIC",
    "queries": [
        "arXiv K-12 AI education cs.AI cs.EDU",
        "ERIC artificial intelligence K-12 education site:eric.ed.gov",
    ]
}

log("第一批搜索任务已定义，等待父进程并行执行...")

# 写入任务清单供父进程使用
task_manifest = {
    "timestamp": datetime.now().isoformat(),
    "batches": [
        {"batch": 1, "agents": ["intel_01", "intel_02", "intel_03"]},
        {"batch": 2, "agents": ["intel_04", "intel_05", "intel_06"]},
        {"batch": 3, "agents": ["intel_07", "intel_08", "intel_09"]},
        {"batch": 4, "agents": ["intel_10", "intel_11", "intel_12"]},
    ]
}
with open("/workspace/logs/intel_manifest.json", "w") as f:
    json.dump(task_manifest, f, indent=2)

log("===== 脚本就绪，manifest已写入 =====")
print("READY")
