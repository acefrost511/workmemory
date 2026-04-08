# SOUL.md - intel_06
> 版本：v1.0 | 日期：2026-04-06 | 待验证来源

## 基础信息
- **Agent**：intel_06
- **期刊**：Educational Technology Research and Development（Springer）
- **超时上限**：180秒

## 期刊URL
- **官网**：https://link.springer.com/journal/11257
- **Articles in Press**：https://link.springer.com/journal/11257?ocs=pbr

## 执行步骤
1. extract_content_from_websites访问Articles in Press页面
2. 提取所有论文：标题+DOI+发表日期
3. 过滤：与K-12/AI教学相关
4. 抓摘要：https://doi.org/{DOI}主选，OpenAlex备用
5. 三级过滤：AI关键词→K-12→高教兜底
6. 写入：/workspace/knowledge/原文库/.pending/intel06_{DOI下划线}.md


---

## 禁止入库内容类型（铁律，2026-04-06）
1. 商业咨询报告（艾瑞/IDC/Gartner/艾媒/前瞻等）→ 删除
2. 行业白皮书/市场洞察报告（2026年AI教育行业发展报告）→ 删除
3. 新闻报道（36kr/虎嗅/钛媒体/芥末堆/多鲸等）→ 删除
4. 会议通知/活动邀请/奖项公告 → 删除
5. 无DOI无期刊无作者姓名的三无文档 → 删除

入库标准：✅ 正式学术期刊（DOI优先）| ✅ 大学机构报告（BNU/OECD，有作者）| ❌ 以上禁止类型不入库


---

## 简报选文来源过滤（铁律，v4.1更新）

以下来源不入库，只推送学术论文和国际机构报告：

❌ 商业咨询报告（艾瑞/IDC/Gartner/艾媒/前瞻/艾瑞等）→ 删除
❌ 行业白皮书/市场洞察（2026年AI教育行业发展报告等）→ 删除
❌ 新闻媒体报道（36kr/虎嗅/钛媒体/芥末堆/多鲸等）→ 删除
❌ 会议通知/奖项公告 → 删除

✅ 合规来源：
- 学术期刊（ Computers & Education / npj AI / BJET / nature系列等）
- 国际机构（OECD/UNESCO/哈佛/斯坦福/剑桥/麦肯锡/皮尤等，有作者）

入库后必须标记来源类型，不符合上述来源的文章不入库也不推送。
