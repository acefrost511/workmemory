# SOUL.md - intel_11
> 版本：v1.0 | 日期：2026-04-06 | 中文期刊版

## 基础信息
- **Agent**：intel_11
- **期刊**：课程·教材·教法（CNKI）
- **超时上限**：180秒

## 执行步骤
1. extract_content_from_websites访问知网期刊页面
2. 提取最新发表的文章：标题+DOI
3. 过滤（中文关键词）：
   第一步：AI词（人工智能/AI/LLM/大语言模型/生成式AI/ChatGPT）
   第二步：K-12（中小学/课堂/教学/学校/学生/教师）
   第三步：无K-12但含高教（大学/高校）→ 兜底入库
4. 抓摘要：知网页面提取
5. 写入：/workspace/knowledge/原文库/.pending/
