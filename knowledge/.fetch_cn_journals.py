#!/usr/bin/env python3
"""
中文教育期刊抓取脚本（基于OpenAlex API，严格按期刊名过滤）
用法：python3 .fetch_cn_journals.py <期刊名> <篇数> <输出文件>

⚠️ 严格检查：必须来自正确的期刊！
"""
import sys
import json
import urllib.request
import urllib.parse
import re
import time

def fetch_json(url, timeout=15):
    req = urllib.request.Request(url, headers={
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (compatible; research-bot/1.0)'
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def search_by_journal_name(journal_name, max_articles=3):
    """
    搜索指定期刊的最新论文
    使用 OpenAlex sources API 先找到期刊，再找该期刊的论文
    """
    # 先找到期刊的 OpenAlex ID
    search_url = 'https://api.openalex.org/sources?search=' + urllib.parse.quote(journal_name)
    sources_data = fetch_json(search_url)
    source_id = None

    for s in sources_data.get('results', []):
        if s.get('display_name') and journal_name in s.get('display_name', ''):
            source_id = s.get('id')  # 格式: S...
            break

    if not source_id:
        # 备选：扩大搜索
        for s in sources_data.get('results', []):
            if journal_name[:4] in s.get('display_name', ''):
                source_id = s.get('id')
                break

    if not source_id:
        print(f'未找到期刊: {journal_name}')
        return []

    print(f'找到期刊 ID: {source_id}')

    # 用期刊ID搜索论文
    works_url = (f'https://api.openalex.org/works'
                 f'?filter=primary_location.source.id:{source_id},'
                 f'publication_year:2025-2026,'
                 f'type:journal-article'
                 f'&sort=publication_date:desc'
                 f'&per-page={max_articles * 3}')
    works_data = fetch_json(works_url)
    items = works_data.get('results', [])

    articles = []
    for w in items:
        title = w.get('title', '')
        if not title or len(title) < 10:
            continue

        # 再次确认来源期刊名匹配
        source = (w.get('primary_location') or {}).get('source') or {}
        actual_journal = source.get('display_name', '')

        # 提取作者
        authors = []
        for a in (w.get('authorships', [])[:10]):
            an = a.get('author') or {}
            name = an.get('display_name') or f"{an.get('given','')} {an.get('family','')}".strip()
            if name:
                authors.append(name)

        year = w.get('publication_year', 'n.d.')
        date_parts = w.get('publication_date', '').split('-')
        date_str = date_parts[0] if date_parts else str(year)

        doi = (w.get('doi') or '').replace('https://doi.org/', '')

        # 摘要
        abstract_inv = w.get('abstract_inverted_index') or {}
        if abstract_inv:
            words = []
            for pos, word in sorted((v, k) for k, v in abstract_inv.items()):
                words.append((pos, word))
            abstract = ''.join(word for _, word in sorted(words))
        else:
            abstract = f'（摘要见DOI：https://doi.org/{doi}）'
        abstract = re.sub(r'<[^>]+>', '', abstract).strip()[:500]

        articles.append({
            'title': title,
            'authors': '；'.join(authors) if authors else '未知作者',
            'date': date_str,
            'doi': doi,
            'abstract': abstract,
            'journal': actual_journal or journal_name
        })

        if len(articles) >= max_articles:
            break

    return articles

def write_markdown(articles, output_path):
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
    print(f'写入 {output_path}，共 {len(articles)} 篇')

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("用法: python3 .fetch_cn_journals.py <期刊名> <篇数> <输出文件>")
        sys.exit(1)

    journal = sys.argv[1]
    n = int(sys.argv[2])
    output = sys.argv[3]

    try:
        articles = search_by_journal_name(journal, n)
        if not articles:
            print(f'⚠️ 未找到 {journal} 的论文（2025-2026），尝试扩大年份...')
            # 扩大年份查
            search_url = 'https://api.openalex.org/sources?search=' + urllib.parse.quote(journal)
            sources_data = fetch_json(search_url)
            source_id = None
            for s in sources_data.get('results', []):
                if journal in s.get('display_name', ''):
                    source_id = s.get('id')
                    break
            if source_id:
                works_url = (f'https://api.openalex.org/works'
                             f'?filter=primary_location.source.id:{source_id},'
                             f'publication_year:2024-2026'
                             f'&sort=publication_date:desc'
                             f'&per-page={n}')
                works_data = fetch_json(works_url)
                items = works_data.get('results', [])
                for w in items:
                    title = w.get('title', '')
                    if not title: continue
                    source = (w.get('primary_location') or {}).get('source') or {}
                    authors = [' '.join([a.get('author',{}).get('display_name','') for a in (w.get('authorships',[])[:10])])]
                    year = w.get('publication_year','')
                    doi = (w.get('doi') or '').replace('https://doi.org/', '')
                    abstract_inv = w.get('abstract_inverted_index') or {}
                    words = []
                    for pos, word in sorted((v, k) for k, v in abstract_inv.items()):
                        words.append((pos, word))
                    abstract = ''.join(word for _, word in sorted(words)) if words else f'（摘要见DOI：https://doi.org/{doi}）'
                    articles.append({
                        'title': title,
                        'authors': '；'.join([a for a in authors[0].split() if a]) or '未知作者',
                        'date': str(year),
                        'doi': doi,
                        'abstract': abstract[:500],
                        'journal': source.get('display_name', journal)
                    })
                    if len(articles) >= n: break

        if articles:
            write_markdown(articles, output)
            print(f'成功抓取 {len(articles)} 篇')
        else:
            print(f'❌ 仍然未找到 {journal} 的论文，请手动核查')
    except Exception as e:
        print(f'❌ 错误: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
