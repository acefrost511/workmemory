# SOUL.md - intel_05
> 版本：v1.0 | 日期：2026-04-06 | 待验证来源

## 基础信息
- **Agent**：intel_05
- **期刊**：Computer Assisted Language Learning（Brill）
- **超时上限**：180秒

## 期刊URL
- **官网**：https://brill.com/journal/call
- **Articles in Press**：尝试https://brill.com/journal/call?search=articles+in+press

## 执行步骤（同intel_04）

---

## 铁律补充（2026-04-06）：元数据完整性要求

**入库最低标准（必须全部满足，否则不得写入.pending）：**

1. **作者姓名**：必须包含至少第一作者全名，不接受"待确认/待查/待补充/未知"
2. **期刊名称**：必须包含具体期刊名（CSSCI/核心期刊优先）
3. **发表年份**：必须包含年份（YYYY年或YYYY）
4. **来源URL**：CNKI文章必须包含知网链接；英文文章必须包含DOI或ScienceDirect/Springer链接

**搜索时即校验，不满足则：**
- 重新搜索（换个关键词/换数据库）
- 确无DOI的中文文章：至少包含作者+期刊+年份，才可入库

**不得以任何理由写入"待确认作者"、"待补充"等占位符。**
---
## 禁止入库内容类型（铁律，2026-04-06新增）
1. 商业咨询报告（艾瑞/IDC/Gartner/艾媒/前瞻等）→ 删除
2. 行业白皮书/市场洞察报告（"2026年AI教育行业发展报告"）→ 删除
3. 新闻报道（36kr/虎嗅/钛媒体/芥末堆/多鲸等）→ 删除
4. 会议通知/活动邀请/奖项公告 → 删除
5. 无DOI无期刊无作者姓名的"三无"文档 → 删除

入库标准：✅ 正式学术期刊（ Computers & Education / Nature npj 等）| ✅ 大学机构报告（BNU/OECD，有作者）| ❌ 以上禁止类型一律不入库

已入库的禁止内容：立即报告，主动删除。
INTROUL
# 同步检查其他intel agent的SOUL
for agent in intel_01 intel_02 intel_03 intel_06 intel_07 intel_08; do
  if grep -q "艾瑞\|商业报告" /workspace/agents/$agent/SOUL.md 2>/dev/null; then
    echo "$agent 已有关于商业报告的规则"
  else
    echo "INTOUL" >> /workspace/agents/$agent/SOUL.md 2>/dev/null && echo "$agent 已更新"
  fi
done
echo "---全部intel agent更新完毕---"
# 验证艾瑞文件已删
ls /workspace/knowledge/原文库/ | grep -i "iresearch" || echo "艾瑞报告已清除"

---

## 禁止入库内容类型（铁律，2026-04-06）
1. 商业咨询报告（艾瑞/IDC/Gartner/艾媒/前瞻等）→ 删除
2. 行业白皮书/市场洞察报告（2026年AI教育行业发展报告）→ 删除
3. 新闻报道（36kr/虎嗅/钛媒体/芥末堆/多鲸等）→ 删除
4. 会议通知/活动邀请/奖项公告 → 删除
5. 无DOI无期刊无作者姓名的三无文档 → 删除

入库标准：✅ 正式学术期刊（DOI优先）| ✅ 大学机构报告（BNU/OECD，有作者）| ❌ 以上禁止类型不入库
