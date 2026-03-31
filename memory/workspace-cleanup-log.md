# 工作区定期清理日志

> 建立时间：2026-03-30
> 清理规则：陛下定制，铁律

---

## 清理执行记录

### 2026-03-30（首次全面清理）
执行：python3脚本批量清理11类目录
结果：删除29个文件，释放175KB

**各目录清理后状态：**
- extract/raw_content/：862个文件，40MB（全部为<30天，保留）
- scores/：0个文件 ✅
- reports/weekly/temp/：0个文件 ✅
- .cron_patches/：3个文件（保留最新3个）✅
- .learnings/：10个文件（保留最新10个）✅
- education_sop/：7个文件（保留v4.0）✅
- knowledge/scores/：10个文件，71KB
- knowledge/素材库/：5个文件，51KB
- articles/：3个文件，19KB

**下次预计清理时间：2026-04-06（周日03:00）**



**本次立即清理：**
- /workspace/scores/*20260330*.md（6个旧打分文件）—— ✅ 已删除
- /workspace/reports/weekly/temp/*.json（11个临时agent json）—— ✅ 已删除

**建立定期cron：**
- cron名称：工作区定期清理-每周日凌晨3点
- cron ID：b24bfa49
- 频率：每周日03:00执行
- 11项清理规则（见上方）

---

## 永久保留目录（禁止清理）

| 目录 | 说明 |
|------|------|
| /workspace/memory/ | 记忆体系 |
| /workspace/knowledge/beliefs/ | 14个信念抽屉 |
| /workspace/knowledge/原文库/ | 情报永久库 |
| /workspace/knowledge/insights/ | 洞察最终版 |
| /workspace/agents/ | Agent定义文件 |
| /workspace/skills/ | Skill定义 |
| /workspace/SOUL.md等核心文件 | 身份/规则定义 |

---

## 定期清理目录

| 目录 | 清理周期 | 说明 |
|------|---------|------|
| /workspace/extract/raw_content/ | 30天 | 原始网页缓存（情报已入库） |
| /workspace/scores/ | 不写盘 | 洞察打分过程文件 |
| /workspace/reports/weekly/temp/ | 不写盘 | 临时agent json |
| /workspace/.cron_patches/ | 保留最新3个 | 历史cron payload |
| /workspace/.learnings/ | 30天 | 学习文件夹 |
| /workspace/education_sop/ | 保留v4.0 | 旧版SOP和测试文件 |
| /workspace/knowledge/scores/ | 30天 | 情报审核打分 |
| /workspace/knowledge/素材库/ | 30天 | 临时素材库 |
| /workspace/knowledge/笔记/ | 60天 | 临时笔记 |
| /workspace/articles/ | 30天 | 旧版复盘文章 |
| /workspace/memory/cron-health-*.md | 7天 | Cron健康报告 |
