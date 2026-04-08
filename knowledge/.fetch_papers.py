#!/usr/bin/env python3
"""Crossref期刊论文抓取脚本
用法：python3 .fetch_papers.py <ISSN> <期刊名> <输出文件> [抓取篇数]
"""
import sys
import json
import urllib.request
import urllib.parse
import time

def fetch_json(url, timeout=20):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (compatible; research-bot/1.0)',
        'Accept': 'application/json'
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def extract_articles(issn, journal_name, max_articles=3):
    """从Crossref抓取论文元数据"""
    filter_str = f"type:journal-article,from-pub-date:2025-01-01"
    url = (f"https://api.crossref.org/journals/{issn}/works"
           f"?filter={urllib.parse.quote(filter_str)}"
           f"&sort=published-online&order=desc&rows={max_articles*3}")
    
    print(f"抓取中: {url[:80]}...")
    data = fetch_json(url)
    items = data['message']['items']
    
    articles = []
    for item in items:
        title_list = item.get('title', [])
        if not title_list:
            continue
        title = title_list[0]
        # 过滤Editorial Board等非研究文章
        skip_words = ['editorial', 'erratum', 'retraction', 'correction', 'author response', 'reply']
        if any(w in title.lower() for w in skip_words):
            continue
        
        # 提取作者（前10位）
        authors = []
        for a in item.get('author', [])[:10]:
            given = a.get('given', '')
            family = a.get('family', '')
            if family:
                name = f"{given} {family}".strip() if given else family
                authors.append(name)
        
        # 提取日期
        date_parts = (item.get('issued', {}) or {}).get('date-parts', [[None]])[0]
        year = date_parts[0] if date_parts[0] else 'n.d.'
        month = date_parts[1] if len(date_parts) > 1 else ''
        date_str = f"{year}-{month:02d}" if month else str(year)
        
        # 提取DOI
        doi = item.get('DOI', '')
        
        # 摘要：先尝试listing自带，再逐篇抓取
        abstract = item.get('abstract', '')
        if not abstract:
            # 单独抓取摘要
            try:
                detail = fetch_json(f"https://api.crossref.org/works/{doi}", timeout=15)
                abstract = (detail.get('message', {}) or {}).get('abstract', '')
            except Exception:
                pass
        if not abstract:
            abstract = f"（摘要见DOI：https://doi.org/{doi}）"
        # 清理HTML标签
        import re
        abstract = re.sub(r'<[^>]+>', '', abstract)
        abstract = abstract.strip()[:600]
        
        articles.append({
            'title': title,
            'authors': '; '.join(authors) if authors else '未知作者',
            'date': date_str,
            'doi': doi,
            'abstract': abstract,
            'journal': journal_name
        })
        
        if len(articles) >= max_articles:
            break
    
    return articles

def write_markdown(articles, output_path):
    """写入markdown文件"""
    lines = []
    for i, art in enumerate(articles, 1):
        lines.append(f"# 标题\n{art['title']}")
        lines.append(f"# 作者\n{art['authors']}")
        lines.append(f"# 发表时间\n{art['date']}")
        lines.append(f"# 摘要\n{art['abstract']}")
        lines.append(f"# 来源\n{art['journal']}")
        lines.append(f"# DOI\n{art['doi']}")
        if i < len(articles):
            lines.append("")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"✅ 写入 {output_path}，共 {len(articles)} 篇")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("用法：python3 .fetch_papers.py <ISSN> <期刊名> <输出文件> [篇数]")
        sys.exit(1)
    
    issn = sys.argv[1]
    journal = sys.argv[2]
    output = sys.argv[3]
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    
    try:
        articles = extract_articles(issn, journal, n)
        if articles:
            write_markdown(articles, output)
            print(f"成功抓取 {len(articles)} 篇论文")
        else:
            print("⚠️ 未找到符合条件的论文")
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
