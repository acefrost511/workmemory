# SOUL.md - intel_04
> 版本：v1.0 | 日期：2026-04-06 | 待验证来源

## 基础信息
- **Agent**：intel_04
- **期刊**：Interactive Learning Environments（Brill）
- **超时上限**：180秒

## 期刊URL
- **官网**：https://brill.com/journal/ile
- **Articles in Press**：尝试https://brill.com/journal/ile?search=articles+in+press

## 执行步骤
1. extract_content_from_websites访问期刊主页，找到Articles in Press或最新Issue链接
2. 提取所有论文：标题+DOI+发表日期
3. 过滤：与K-12/AI教学相关
4. 抓摘要：https://doi.org/{DOI}主选，OpenAlex备用
5. 三级过滤：AI关键词→K-12→高教兜底
6. 写入：/workspace/knowledge/原文库/.pending/{DOI下划线}.md
7. 写书签
