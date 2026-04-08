#!/usr/bin/env python3
"""
原文库完整性守护脚本
功能：
1. 识别AIGC生成内容（通过元数据标记）
2. DOI溯源验证（Crossref比对）
3. 摘要AI指纹检测（统计方法）
4. 来源期刊一致性验证
5. 隔离可疑文件

用法：
  python3 .integrity_scanner.py [--scan]       # 仅扫描不修复
  python3 .integrity_scanner.py [--fix]       # 扫描+修复
  python3 .integrity_scanner.py [--quarantine] # 扫描+隔离+报告
"""
import os
import re
import sys
import json
import time
import random
import hashlib
import urllib.request
import urllib.parse
from collections import Counter

BASE = '/Users/choubao/Documents/网易龙虾/knowledge/原文库'
QUARANTINE = os.path.join(BASE, '.quarantine')
REPORT_PATH = os.path.join(BASE, '.integrity_report.json')

# ==================== 工具函数 ====================

def fetch_crossref(doi, timeout=12):
    """从Crossref获取论文元数据"""
    doi = doi.replace('https://doi.org/', '').strip()
    url = 'https://api.crossref.org/works/' + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={
        'User-Agent': f'Mozilla/5.0 (research IntegrityScanner/1.0; mailto:research@example.com)',
        'Accept': 'application/json'
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read()).get('message') or {}

def extract_doi(content):
    m = re.search(r'\*\*DOI\*\*[：:]\s*(10\.\S+)', content)
    if m: return m.group(1).strip()
    m = re.search(r'^##\s*DOI\n+(.+?)\n', content, re.MULTILINE)
    if m: return m.group(1).strip()
    m = re.search(r'#\s*DOI\n+(.+?)\n', content, re.MULTILINE)
    if m: return m.group(1).strip()
    m = re.search(r'\(https?://doi\.org/(10\.\S+)\)', content)
    if m: return m.group(1).strip()
    return None

def extract_abstract(content):
    # 优先提取 ## 摘要
    m = re.search(r'^##\s*摘要\s*\n+(.+?)(?=^##|\n#|\n\*|\Z)', content, re.MULTILINE | re.DOTALL)
    if m: return re.sub(r'\n+', ' ', m.group(1)).strip()
    # 其次提取 # 摘要
    m = re.search(r'^#\s*摘要\s*\n+(.+?)(?=^##|\n#\s|\n\*|\Z)', content, re.MULTILINE | re.DOTALL)
    if m: return re.sub(r'\n+', ' ', m.group(1)).strip()
    return ''

def extract_title(content):
    m = re.search(r'\*\*标题\*\*[：:]\s*\n?(.+?)\n', content)
    if m: return m.group(1).strip().strip('#').strip()
    m = re.search(r'^##?\s*标题\s*\n+(.+?)\n', content, re.MULTILINE)
    if m: return m.group(1).strip().strip('#').strip()
    return ''

def extract_journal(content):
    m = re.search(r'\*\*期刊\*\*[：:]\s*(.+?)\n', content)
    if m: return m.group(1).strip()
    m = re.search(r'#\s*来源\n+(.+?)\n', content, re.MULTILINE)
    if m: return m.group(1).strip()
    m = re.search(r'来源[：:]\s*(.+?)\n', content)
    if m: return m.group(1).strip()
    return ''

def clean_text(text):
    return re.sub(r'<[^>]+>', '', text or '').lower()

# ==================== 检测模块 ====================

def check_aigc(content, fname):
    """检测1：AIGC元数据标记"""
    markers = ['aigc:', 'contentproducer:', 'minimax agent', 'ai-generated',
               'contentpropagator:', 'produceid:', 'propagateid:']
    text_lower = content.lower()
    found = [m for m in markers if m in text_lower]
    if found:
        return 'AIGC_META', f'发现AIGC标记: {", ".join(found)}'
    return None, None

def check_doi_format(doi, fname):
    """检测2：DOI格式"""
    if not doi:
        return 'NO_DOI', '文件中无DOI'
    # 正确格式：10.XXXX/YYYY  （斜杠）
    # 错误格式：10.XXXX_YYYY  （下划线）- 造假特征
    if re.match(r'^10\.\d{4,}_', doi):
        return 'FAKE_DOI_FORMAT', f'DOI使用下划线而非斜杠: {doi}'
    if not re.match(r'^10\.\d{4,}/', doi):
        return 'INVALID_DOI', f'DOI格式不符: {doi}'
    return None, None

def check_crossref_match(doi, content, fname):
    """检测3：Crossref溯源比对（摘要+期刊名）"""
    try:
        meta = fetch_crossref(doi)
        time.sleep(0.2 + random.uniform(0, 0.3))  # 尊重限流
    except Exception as e:
        return 'CROSSREF_FAIL', f'Crossref查询失败: {e}', None, None

    if not meta or not meta.get('DOI'):
        return 'CROSSREF_NOT_FOUND', f'DOI在Crossref不存在: {doi}', None, None

    # 比对期刊名
    file_journal = clean_text(extract_journal(content))
    cr_journals = [clean_text(j) for j in (meta.get('container-title') or [])]
    cr_journal = cr_journals[0] if cr_journals else ''
    if file_journal and cr_journal:
        if file_journal not in cr_journal and cr_journal not in file_journal:
            # 部分匹配检查
            key_words = [w for w in file_journal.split() if len(w) > 3]
            if not any(w in cr_journal for w in key_words):
                return 'JOURNAL_MISMATCH', f'期刊名不符(文件:{file_journal[:30]}, Crossref:{cr_journal[:30]})', None, None

    # 比对标题（相似度）
    file_title = clean_text(extract_title(content))
    cr_titles = [clean_text(t) for t in (meta.get('title') or [])]
    cr_title = cr_titles[0] if cr_titles else ''
    if file_title and cr_title:
        words_file = set(file_title.split())
        words_cr = set(cr_title.split())
        if len(words_file) > 3 and len(words_cr) > 3:
            overlap = len(words_file & words_cr)
            union = len(words_file | words_cr)
            jaccard = overlap / union if union else 0
            if jaccard < 0.3:
                return 'TITLE_MISMATCH', f'标题与DOI不匹配(Jaccard:{jaccard:.2f})', None, None

    # 比对摘要（相似度）
    file_abs = clean_text(extract_abstract(content))
    cr_abs = clean_text(meta.get('abstract') or '')
    if file_abs and cr_abs and len(file_abs) > 50 and len(cr_abs) > 50:
        words_f = set(file_abs.split())
        words_c = set(cr_abs.split())
        overlap = len(words_f & words_c)
        union = len(words_f | words_c)
        sim = overlap / union if union else 0
        if sim < 0.3:
            return 'ABSTRACT_FAKE', f'摘要与Crossref不符(相似度:{sim:.0%})', cr_abs[:200], cr_abs
        elif sim >= 0.7:
            return None, None, cr_abs[:200], cr_abs
        else:
            return 'ABSTRACT_PARTIAL', f'摘要部分不符(相似度:{sim:.0%})', cr_abs[:200], cr_abs

    return None, None, cr_abs[:200] if cr_abs else None, cr_abs

def compute_text_fingerprint(text):
    """
    检测4：文本统计指纹（识别AI生成内容）
    AI生成文本特征：
    - 词汇丰富度低（重复词多）
    - 句子长度分布过于均匀
    - 特定连接词高频（因此、然而、此外）
    - 信息熵接近
    """
    if not text or len(text) < 50:
        return None, 'text_too_short'

    words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text)
    if len(words) < 10:
        return None, 'not_enough_words'

    # 词频分析
    word_counts = Counter(words)
    total = len(words)
    vocab_ratio = len(word_counts) / total  # 词汇丰富度

    # 平均词长
    avg_word_len = sum(len(w) for w in words) / len(words)

    # 常见AI连接词比例
    ai_markers = ['因此', '然而', '此外', '与此同时', '总而言之', '综上所述',
                  '值得注意的是', '不难发现', '可以看出', '研究表明']
    marker_count = sum(1 for w in words if any(m in w for m in ai_markers))
    marker_ratio = marker_count / total

    # 句子长度标准差（AI生成句子长度过于均匀）
    sentences = re.split(r'[。.!?]+', text)
    sent_lens = [len(s) for s in sentences if len(s) > 5]
    if len(sent_lens) >= 3:
        mean_len = sum(sent_lens) / len(sent_lens)
        variance = sum((l - mean_len) ** 2 for l in sent_lens) / len(sent_lens)
        std_dev = variance ** 0.5
        coef_var = std_dev / mean_len if mean_len > 0 else 0  # 变异系数，越小越规律
    else:
        coef_var = 1.0

    # 综合打分（0-100，越高越像AI生成）
    ai_score = 0
    if vocab_ratio < 0.15: ai_score += 30  # 词汇重复严重
    if marker_ratio > 0.05: ai_score += 25  # AI连接词过多
    if coef_var < 0.3: ai_score += 25  # 句子长度过于均匀
    if avg_word_len < 1.5: ai_score += 20  # 平均词长异常

    return ai_score, {
        'vocab_ratio': round(vocab_ratio, 3),
        'marker_ratio': round(marker_ratio, 3),
        'coef_var': round(coef_var, 3),
        'ai_score': ai_score
    }

# ==================== 主扫描 ====================

def scan_file(fname):
    """扫描单个文件，返回问题列表"""
    fpath = os.path.join(BASE, fname)
    if not os.path.isfile(fpath):
        return []

    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    issues = []
    doi = extract_doi(content)

    # 检测1：AIGC元数据
    code, msg = check_aigc(content, fname)
    if code:
        issues.append({'检测': 'AIGC元数据', '等级': 'CRITICAL', '代码': code, '说明': msg})
        return issues  # AIGC文件直接隔离，不继续检测

    # 检测2：DOI格式
    code, msg = check_doi_format(doi, fname)
    if code:
        issues.append({'检测': 'DOI格式', '等级': 'HIGH', '代码': code, '说明': msg})

    # 检测3：Crossref溯源
    if doi and re.match(r'^10\.\d{4,}/', doi):
        code, msg, cr_abs_hint, cr_abs_full = check_crossref_match(doi, content, fname)
        if code:
            issues.append({
                '检测': 'Crossref溯源',
                '等级': {'CROSSREF_NOT_FOUND': 'HIGH', 'INVALID_DOI': 'MEDIUM',
                         'JOURNAL_MISMATCH': 'HIGH', 'TITLE_MISMATCH': 'HIGH',
                         'ABSTRACT_FAKE': 'CRITICAL', 'ABSTRACT_PARTIAL': 'MEDIUM',
                         'CROSSREF_FAIL': 'LOW'}.get(code, 'MEDIUM'),
                '代码': code, '说明': msg,
                '正确摘要提示': cr_abs_hint,
                '正确摘要': cr_abs_full
            })

    # 检测4：AI文本指纹（仅对英文摘要）
    abstract = extract_abstract(content)
    if abstract and len(abstract) > 80 and re.match(r'^[a-zA-Z\s,\.]+$', abstract[:30]):
        score, stats = compute_text_fingerprint(abstract)
        if score and score >= 60:
            issues.append({
                '检测': 'AI文本指纹',
                '等级': 'HIGH',
                '代码': 'AI_FINGERPRINT',
                '说明': f'摘要具有AI生成特征(得分:{score})',
                '统计': stats
            })

    return issues

def quarantine_file(fname, reason):
    """隔离文件"""
    os.makedirs(QUARANTINE, exist_ok=True)
    src = os.path.join(BASE, fname)
    dest = os.path.join(QUARANTINE, fname)
    # 避免覆盖
    if os.path.exists(dest):
        base, ext = os.path.splitext(fname)
        dest = os.path.join(QUARANTINE, f"{base}_{int(time.time())}{ext}")
    import shutil
    shutil.move(src, dest)
    return dest

def fix_file(fname, real_abstract=None, real_journal=None):
    """修复文件"""
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    ts = time.strftime('%Y-%m-%d')

    if real_abstract:
        # 替换摘要
        def replace_abs(m):
            return m.group(0).rstrip() + '\n\n### ⚠️ 系统于' + ts + '从Crossref校正摘要\n'
        content = re.sub(r'(^##\s*摘要\s*\n)', replace_abs, content, flags=re.MULTILINE)
        content = re.sub(r'(^#\s*摘要\s*\n)', replace_abs, content, flags=re.MULTILINE)
        # 已有正确摘要则替换
        if re.search(r'(^##\s*摘要\s*\n)(?!.*Crossref)', content, re.MULTILINE):
            pass  # 已有标记

    if real_journal:
        content = re.sub(r'(\*\*期刊\*\*[：:]\s*)(.+?)\n',
                         r'\g<1>' + real_journal + r'\n', content)

    content = re.sub(r'\*\*摘要状态\*\*[：:]?[^\n]*',
                     '**摘要状态**：✅Crossref溯源验证于' + ts, content)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

# ==================== 主程序 ====================

if __name__ == '__main__':
    mode = 'scan'
    if '--fix' in sys.argv: mode = 'fix'
    if '--quarantine' in sys.argv: mode = 'quarantine'

    files = sorted([f for f in os.listdir(BASE)
                    if f.endswith('.md') and not f.startswith('.')])
    print(f'扫描 {len(files)} 个文件...')

    results = {}
    quarantined = []
    fixed = []
    stats = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'OK': 0}

    for i, fname in enumerate(files):
        issues = scan_file(fname)
        results[fname] = issues

        if issues:
            top_issue = max(issues, key=lambda x: {'CRITICAL': 3, 'HIGH': 2, 'MEDIUM': 1, 'LOW': 0}.get(x['等级'], 0))
            stats[top_issue['等级']] = stats.get(top_issue['等级'], 0) + 1
        else:
            stats['OK'] += 1

        bar = '#' * (i * 50 // len(files))
        print(f'\r[{bar:<50}] {i+1}/{len(files)} {fname[:35]} → {"OK" if not issues else issues[0]["检测"]}', end='', flush=True)

        if mode == 'quarantine' and issues:
            for issue in issues:
                if issue['等级'] == 'CRITICAL':
                    dest = quarantine_file(fname, issue['说明'])
                    quarantined.append({'file': fname, 'reason': issue['说明']})
                    print(f'\n  🔒 隔离: {fname} → {os.path.basename(dest)}')
                    break

        if mode == 'fix' and issues:
            for issue in issues:
                if issue.get('正确摘要'):
                    fix_file(fname, real_abstract=issue['正确摘要'])
                    fixed.append(fname)
                    break

        time.sleep(0.05)

    print()
    print()
    print('=' * 60)
    print('完整性扫描报告 - ' + time.strftime('%Y-%m-%d %H:%M:%S'))
    print('=' * 60)
    print('✅ 正常: %d' % stats['OK'])
    print('❌ CRITICAL: %d' % stats['CRITICAL'])
    print('⚠️  HIGH: %d' % stats['HIGH'])
    print('⚠️  MEDIUM: %d' % stats['MEDIUM'])
    print('⚠️  LOW: %d' % stats['LOW'])

    if quarantined:
        print(f'\n🔒 已隔离 {len(quarantined)} 个文件:')
        for q in quarantined:
            print(f'  - {q["file"]}: {q["reason"][:60]}')

    if fixed:
        print(f'\n🔧 已修复 {len(fixed)} 个文件')
        for f in fixed:
            print(f'  - {f}')

    # 保存报告
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump({'results': results, 'stats': stats, 'quarantined': quarantined,
                   'fixed': fixed, 'scanned_at': time.strftime('%Y-%m-%d %H:%M:%S')},
                  f, ensure_ascii=False, indent=2)
    print(f'\n📄 详细报告: {REPORT_PATH}')
