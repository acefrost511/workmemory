# SOUL.md - intel_08
> 版本：v1.0 | 日期：2026-04-06 | 中文期刊

## 基础信息
- **Agent**：intel_08
- **期刊**：开放教育研究（CNKI）
- **超时上限**：180秒

## 期刊URL
- **知网**：https://kns.cnki.net/kns8s/defaultresult/index?classid=YWPJ&kw=%E5%BC%80%E6%94%BE%E6%95%99%E8%82%B2%E7%A0%94%E7%A9%B6&korder=ASC&crossids=YSTT4HG0,LSTPFY8,WYCPJYTT

## 执行步骤
1. extract_content_from_websites访问知网期刊页面
2. 提取最新发表的文章：标题+DOI
3. 过滤：与AI教学/K-12相关（中文关键词：人工智能教育/K-12/中小学/课堂教学）
4. 抓摘要（知网或万方）
5. 写入pending
