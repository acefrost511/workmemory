#!/usr/bin/env python3
"""
原文库摘要补全脚本 v1.0
功能：读取原文库所有文件，抓DOI/arXiv摘要，更新文件
"""
import re, time, json
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

LIBRARY = Path("/workspace/knowledge/原文库")
STATE_FILE = Path("/workspace/knowledge/.abstract_progress.json")
LOG_FILE = Path("/workspace/knowledge/.abstract_fetch_log.txt")

# 加载进度
if STATE_FILE.exists():
    with open(STATE_FILE) as f:
        state = json.load(f)
else:
    state = {"done": [], "failed": [], "total": 0}

done_set = set(state["done"])
failed_set = set(state["failed"])

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")

def fetch_doi_abstract(doi):
    """从DOI抓摘要"""
    doi = doi.strip().strip('<>')
    # 优先从Semantic Scholar抓（速度快，支持CORS）
    urls = [
        f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=abstract,title,year,venue",
        f"https://api.crossref.org/works/{doi}",
    ]
    for url in urls:
        try:
            req = urlopen(url, timeout=8)
            data = json.loads(req.read())
            # Semantic Scholar格式
            if "abstract" in data and data["abstract"]:
                return data["abstract"][:800]
            # Crossref格式
            abs_m = re.search(r'"abstract"[^"]*"([^"]{100,})', str(data))
            if abs_m:
                return abs_m.group(1)[:800]
        except Exception:
            continue
    # 兜底：直接访问DOI
    try:
        import urllib.request
        req = urllib.request.urlopen(f"https://doi.org/{doi}", timeout=6)
        html = req.read().decode('utf-8', errors='ignore')
        abs_m = re.search(r'<meta[^>]+abstract[^>]*content="([^"]{100,})"', html)
        if abs_m:
            return abs_m.group(1)[:800]
    except:
        pass
    return None

def fetch_arxiv_abstract(arxiv_id):
    """从arXiv抓摘要"""
    arxiv_id = arxiv_id.strip()
    # 转换格式：2410.03017 → arxiv:2410.03017
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    try:
        req = urlopen(url, timeout=10)
        xml = req.read().decode('utf-8', errors='ignore')
        summary_m = re.search(r'<summary>([\s\S]{100,2000})</summary>', xml)
        if summary_m:
            text = re.sub(r'\s+', ' ', summary_m.group(1)).strip()
            return text[:800]
    except:
        pass
    return None

def update_file(filepath, abstract, fetch_info):
    """给文件追加摘要"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 如果已有"核心发现"且超过100字，不更新
    if '核心发现' in content and len(re.findall(r'核心发现[：:][^\n]{100,}', content)) > 0:
        existing = re.search(r'核心发现[：:]\s*([^\n]{100,})', content)
        if existing and len(existing.group(1)) > 100:
            return "已有内容"
    
    # 追加摘要
    marker = "\n\n---\n## 摘要（自动抓取）\n" + fetch_info + "\n\n" + abstract[:600] + "\n"
    
    # 找最后位置插入
    if '## 摘要' in content or '##核心发现' in content:
        return "已有摘要段"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content + marker)
    return "已更新"

def process_file(filepath):
    """处理单个文件"""
    name = filepath.name
    if name in done_set:
        return "done", "已处理"
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 提取DOI
    doi_m = re.search(r'(?:DOI|doi)[：:\s]*10\.[^\s<>"\'\n]{5,60}', content, re.I)
    doi = doi_m.group(0).split()[-1].strip('<>.,;:') if doi_m else None
    
    # 提取arXiv ID
    arxiv_m = re.search(r'arXiv:?\s*(\d{4}\.\d{4,5})', content, re.I)
    arxiv_id = arxiv_m.group(1) if arxiv_m else None
    
    # 提取中文标题
    cn_m = re.search(r'中文标题[：:]\s*[\"\']?([^\n"\']{10,100})', content)
    title = cn_m.group(1).strip() if cn_m else filepath.stem[:40]
    
    if not doi and not arxiv_id:
        return "skip", "无DOI/arXiv ID"
    
    if doi:
        src = f"来源：DOI {doi} | "
        abstract = fetch_doi_abstract(doi)
        if abstract:
            result = update_file(filepath, abstract, src)
            return "success", f"DOI {doi[:20]} → {abstract[:60]}"
        else:
            return "failed", f"DOI {doi[:20]} 抓取失败"
    
    if arxiv_id:
        src = f"来源：arXiv {arxiv_id} | "
        abstract = fetch_arxiv_abstract(arxiv_id)
        if abstract:
            result = update_file(filepath, abstract, src)
            return "success", f"arXiv {arxiv_id} → {abstract[:60]}"
        else:
            return "failed", f"arXiv {arxiv_id} 抓取失败"

def main():
    log("=== 摘要补全开始 ===")
    files = sorted(LIBRARY.glob("*.md"))
    total = len(files)
    log(f"总文件: {total} 个")
    
    stats = {"success": 0, "failed": 0, "skip": 0, "done": 0}
    
    for i, f in enumerate(files):
        if i % 20 == 0:
            log(f"进度: {i}/{total} | 成功:{stats['success']} 失败:{stats['failed']} 跳过:{stats['skip']}")
        
        status, msg = process_file(f)
        stats[status] = stats.get(status, 0) + 1
        
        if status == "success":
            done_set.add(f.name)
            state["done"].append(f.name)
        elif status == "failed":
            if f.name not in failed_set:
                failed_set.add(f.name)
                state["failed"].append(f.name)
        
        # 每10个保存一次进度
        if (i+1) % 10 == 0:
            with open(STATE_FILE, 'w') as sf:
                json.dump(state, sf)
        
        time.sleep(0.3)  # 控制速率
        
        if i == total - 1:
            log(f"完成! 成功:{stats['success']} 失败:{stats['failed']} 跳过:{stats['skip']}")
    
    with open(STATE_FILE, 'w') as sf:
        json.dump(state, sf)
    log("=== 补全结束 ===")

if __name__ == "__main__":
    main()
