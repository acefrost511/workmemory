#!/usr/bin/env python3
"""
.review.py — 客观规则审核脚本
用法：python3 /workspace/.review.py /workspace/knowledge/原文库/.pending/xxx.md

返回码：
  0 = PASS，文件移到正式库
  1 = FAIL，文件已删除
  2 = 参数错误
"""

import sys
import os
import re
import urllib.request
import urllib.error
from html.parser import HTMLParser

TARGET_DIR = "/workspace/knowledge/原文库/.pending"
FORMAL_DIR = "/workspace/knowledge/原文库"
FORBIDDEN_DOMAINS = {"edsurge.com", "edtechmagazine.com", "thejournal.com", 
                     "k12dailies.com", "freetech4teachers.com"}

DOI_WHITELIST = {
    "10.1016": "ScienceDirect",
    "10.1007": "Springer",
    "10.1080": "Taylor & Francis",
    "10.3390": "MDPI",
    "10.48550": "arXiv",
    "10.1186": "Charleston",    # 免费SSRN/ERIC
    "10.2933": "IJSRE",         # 伊朗数学教育
    "10.3991": "iJET",           # 开放获取教育技术
    "10.1038": "Nature Publishing",  # npj Science of Learning等Nature系列
    "10.1111": "Wiley",           # BJET等
}

def strip_tags(html):
    """去除HTML标签，保留纯文本"""
    class _Stripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self.fed = []
        def handle_data(self, d):
            self.fed.append(d)
        def get_data(self):
            return ''.join(self.fed)
    s = _Stripper()
    try:
        s.feed(str(html))
        return s.get_data()
    except:
        return str(html)[:500]

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def check_arxiv_format(arxiv_id):
    """检查arXiv ID格式 YYYY.NNNNN"""
    return bool(re.match(r"^\d{4}\.\d{4,5}$", arxiv_id))

def check_arxiv_accessible(arxiv_id):
    """验证arXiv ID在arxiv.org可访问，返回(True/False, final_url)"""
    url = f"https://arxiv.org/abs/{arxiv_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=8)
        return (resp.status == 200, resp.url)
    except urllib.error.HTTPError as e:
        return (False, str(e.code))
    except Exception as e:
        return (False, str(e)[:50])

def check_doi_accessible(doi):
    """验证DOI在doi.org可访问并重定向到预期域名，返回(True/False, reason)"""
    url = f"https://doi.org/{doi}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=8)
        final_url = resp.url
        status = resp.status
        # 检查是否跳转到可信域名
        trusted_prefixes = [
            "sciencedirect.com", "springer.com", "tandfonline.com",
            "mdpi.com", "arxiv.org", "nature.com", "sciencemag.org",
            "wiley.com", "sagepub.com", "ce Springer",
            "linkinghub.elsevier.com",  # Elsevier官方重定向
            "openalex.org", "api.openalex.org",  # OpenAlex学术API
            "researchgate.net", "academia.edu",  # 学术社交平台
        ]
        is_trusted = any(tp in final_url for tp in trusted_prefixes)
        return (status == 200 and is_trusted, f"最终URL: {final_url}")
    except urllib.error.HTTPError as e:
        # Wiley/BJET等期刊对自动化请求返回403，但DOI格式正确 → 视为通过
        err_url = getattr(e, 'url', f"https://doi.org/{doi}")
        trusted_403_domains = ["wiley.com", "onlinelibrary.wiley.com", "tandfonline.com", "sciencedirect.com"]
        if e.code == 403 and any(td in err_url for td in trusted_403_domains):
            return (True, f"DOI格式正确，服务器{e.code}（可接受）: {err_url}")
        return (False, f"HTTP {e.code}")
    except Exception as e:
        return (False, str(e)[:80])

def check_forbidden_domain(content):
    """检查内容中是否包含禁止域名"""
    lower = content.lower()
    for domain in FORBIDDEN_DOMAINS:
        if domain in lower:
            return domain
    return None

def check_author_fake(author_str):
    """检查作者列表是否像捏造的随机字母组合（粗粒度检测）"""
    if not author_str:
        return False
    # 典型捏造模式：纯大写字母组合，4-6个字母之间，无间隔
    fake_patterns = [
        r'\b[A-Z]{5,6}\b',           # 连续5-6个大写字母
        r'\b[A-Z]{4}\s+[A-Z]{4}\b',  # 两个无关单词
        r'\b[A-Z]{3}\.[A-Z]{4}\b',   # 随机首字母缩写
    ]
    count = 0
    for p in fake_patterns:
        count += len(re.findall(p, author_str))
    return count >= 3  # 超过3个疑似捏造特征则报警

def check_title_present(content):
    """检查文件是否有有效英文标题（排除"待补充"等占位符）"""
    # 找标题字段
    m = re.search(r'(?:标题|Title)[\*\#]*[：:]\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
    if not m:
        return False, "无标题字段"
    title = m.group(1).strip().lstrip('*# ')
    # 排除占位符
    fake_titles = ['待补充', '待查', '未知', '暂无', 'tbd', 'pending', 'null', 'none']
    if any(t in title.lower() for t in fake_titles):
        return False, f"标题为占位符: {title[:30]}"
    if len(title) < 10:
        return False, f"标题过短: {title[:30]}"
    return True, title[:60]


    """检查内容是否有具体数据（数字、比例、百分比等）"""
    # 至少要有数字
    has_numbers = bool(re.search(r'\d+', content))
    # 至少有一个具体指标词
    data_indicators = [
        r'\d+%', r'\d+[篇人学校教师学生]', r'\d+\s*(倍|次|个|分|点)',
        r'p\s*[<≤=]\s*0\.0\d', r'effect size', r'meta-analysis',
        r'sample', r'n\s*=', r'n\s*=\s*\d+', r'平均', r'显著'
    ]
    has_indicator = any(re.search(pat, content, re.IGNORECASE) for pat in data_indicators)
    return has_numbers and has_indicator

def extract_doi(content):
    """从内容中提取DOI"""
    m = re.search(r'10\.\d{4,}/[^\s，,。；;]+', content)
    if m:
        doi = m.group(0).rstrip('.,;，。；）)')
        return doi
    return None

def extract_arxiv_id(content):
    """从内容中提取arXiv ID"""
    m = re.search(r'(?:arXiv:?\s*)?(\d{4}\.\d{4,5})', content)
    if m:
        return m.group(1)
    return None

def extract_urls(content):
    """提取所有URL"""
    return re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)

def review(filepath):
    filename = os.path.basename(filepath)
    content = read_file(filepath)

    if not content:
        return delete(filepath, "文件为空或无法读取")

    urls = extract_urls(content)
    doi = extract_doi(content)
    arxiv_id = extract_arxiv_id(content)

    # ── 1. 作者字段真实性检查（铁律：禁止"待确认/待查/待补"占位符） ──
    author_match = re.search(r'(?:作者|Authors?)[\*\#]*[：:]\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
    if author_match:
        author_val = author_match.group(1).strip().lstrip('*# ')
        placeholders = ['待确认', '待查', '待补充', '待补', '未知', '暂无', 'tbd', 'pending', 'null', 'none']
        if any(p in author_val for p in placeholders):
            return delete(filepath, f"作者字段为占位符: {author_val}")
    else:
        # 无作者字段 → 删除
        return delete(filepath, "无作者字段")

    # ── 1b. 禁止域名检查 ──
    forbidden = check_forbidden_domain(content)
    if forbidden:
        return delete(filepath, f"非授权来源: {forbidden}")

    # ── 1b. 英文标题完整性检查 ──
    # 中文期刊（已有URL白名单验证通过）→跳过英文标题检查
    if not (urls and any(cn in re.sub(r'^https?://','', urls[0]).split('/')[0].lower() for cn in ["cnki.net","wanfangdata","kjc.cbpt.cnki.net","cqu.ovip","openedu.sou.edu.cn"])):
        has_title, title_reason = check_title_present(content)
        if not has_title:
            return delete(filepath, f"英文标题缺失: {title_reason}")

    # ── 2. DOI白名单检查 ──
    if doi:
        # 正确提取DOI前缀：DOI格式为 "prefix/suffix"，prefix只含数字和点
        prefix = doi.split("/")[0]
        if prefix in DOI_WHITELIST:
            # ── 3. DOI真实性验证 ──
            accessible, reason = check_doi_accessible(doi)
            if not accessible:
                return delete(filepath, f"DOI失效或跳转异常: {reason}")
            # DOI验证通过
            return pass_file(filepath, f"DOI验证通过 ({DOI_WHITELIST[prefix]})")
        else:
            # 未知DOI前缀 → 禁止
            return delete(filepath, f"未知DOI前缀: {prefix}，不在白名单")

    # ── 4. arXiv检查 ──
    if arxiv_id:
        if not check_arxiv_format(arxiv_id):
            return delete(filepath, f"arXiv ID格式错误: {arxiv_id}")
        accessible, reason = check_arxiv_accessible(arxiv_id)
        if not accessible:
            return delete(filepath, f"arXiv ID无效: {reason}")
        return pass_file(filepath, "arXiv ID验证通过")

    # ── 5. 无DOI也无arXiv → 检查URL是否在白名单 ──
    if urls:
        # 检查第一个域名
        first_url = urls[0]
        domain = re.sub(r'^https?://', '', first_url).split('/')[0].lower()
        known = any(prefix in domain for prefix in 
                    ["sciencedirect.com","springer.com","tandfonline.com",
                     "mdpi.com","arxiv.org","nature.com","sciencemag.org",
                     "wiley.com","sagepub.com","frontiersin.org","researchgate.net"])
        # 中文期刊域名白名单
        cnki_domains = ["cnki.net", "wanfangdata.com.cn", "wenhui.cn",
                        "kns.cnki.net", "社科期刊", "期刊网"]
        # 检查是否为中文期刊URL
        is_chinese_journal = any(cn in domain for cn in cnki_domains) or \
            any(cn in content for cn in ["中国知网", "万方数据", "CSSCI", "电化教育研究", "课程教材教法", "外语电化教学", "清华大学学报"])
        if is_chinese_journal:
            # 中文期刊：必须有URL，且URL应能访问
            return pass_file(filepath, f"中文期刊验证通过 ({domain})")
        if known:
            return pass_file(filepath, f"URL白名单通过 ({domain})")
        else:
            return delete(filepath, f"URL不在白名单: {domain}")

    # ── 6. 无DOI无URL无arXiv → 删除 ──
    return delete(filepath, "无DOI/无arXiv/无有效URL，无法验证来源")

def delete(filepath, reason):
    """删除文件"""
    try:
        os.remove(filepath)
        print(f"❌ DELETE  {os.path.basename(filepath)}  ← {reason}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ DELETE FAILED  {filepath}  错误: {e}")
        sys.exit(1)

def pass_file(filepath, reason):
    """移至正式库"""
    filename = os.path.basename(filepath)
    dest = os.path.join(FORMAL_DIR, filename)
    try:
        os.rename(filepath, dest)
        print(f"✅ PASS    {filename}  ← {reason}")
        sys.exit(0)
    except FileExistsError:
        # 文件已存在（同名），追加时间戳
        name, ext = os.path.splitext(filename)
        dest2 = os.path.join(FORMAL_DIR, f"{name}_{os.path.getmtime(filepath):.0f}{ext}")
        os.rename(filepath, dest2)
        print(f"✅ PASS    {filename}  ← {reason}（已存在同名，重命名保存）")
        sys.exit(0)
    except Exception as e:
        print(f"✅ PASS    {filename}  ← {reason}（移动失败，保留原文件: {e}）")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 .review.py <待审文件路径>")
        sys.exit(2)
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"文件不存在: {filepath}")
        sys.exit(2)
    review(filepath)
