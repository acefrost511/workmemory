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
6. 写入pending
