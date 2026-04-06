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
5. 写入：/workspace/knowledge/原文库/.pending/intel08_{DOI下划线}.md


---

## 禁止入库内容类型（铁律，2026-04-06）
1. 商业咨询报告（艾瑞/IDC/Gartner/艾媒/前瞻等）→ 删除
2. 行业白皮书/市场洞察报告（2026年AI教育行业发展报告）→ 删除
3. 新闻报道（36kr/虎嗅/钛媒体/芥末堆/多鲸等）→ 删除
4. 会议通知/活动邀请/奖项公告 → 删除
5. 无DOI无期刊无作者姓名的三无文档 → 删除

入库标准：✅ 正式学术期刊（DOI优先）| ✅ 大学机构报告（BNU/OECD，有作者）| ❌ 以上禁止类型不入库
