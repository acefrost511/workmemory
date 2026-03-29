# Agent SOUL.md 全面审计报告
> 审计时间：2026-03-29 | 审计人：小艾 | 状态：待陛下审批

---

## 一、审计结论总览

| 级别 | 数量 | 说明 |
|------|------|------|
| 🔴 严重矛盾 | 3处 | 流程根本性冲突 |
| 🟡 内容错误 | 5处 | 描述与事实不符 |
| 🟡 缺失项 | 3处 | 关键约束缺失 |
| 🟠 冗余过长 | 1处 | 严重降低可维护性 |
| 🟡 格式问题 | 2处 | 不影响功能但需整理 |

---

## 二、🔴 严重矛盾（必须立即修复）

### 矛盾1：info_officer 的 intel_01~12 描述 vs 实际SOUL.md 完全对不上

**问题详情**：
info_officer（568行）第51行开始描述intel_01~intel_12的分工，但这个描述是v1版本的：

| Agent | info_officer里的描述 | 实际SOUL.md（v3.0） |
|-------|---------------------|---------------------|
| intel_01 | C&E/BJET/JRTE | **Computers & Education / EIT / BJET**（✅匹配） |
| intel_02 | Frontiers/ILE | **ILE/CALL/ETRD/iJET**（⚠️不匹配） |
| intel_03 | Springer/Wiley教育期刊 | **arXiv/ERIC**（⚠️不匹配） |
| intel_04 | Nature npj/ScienceDirect | **中文CSSCI·教育研究类**（⚠️完全不匹配） |
| intel_05 | MDPI/DOAJ | **中文CSSCI·开放教育类**（⚠️不匹配） |
| intel_06 | arXiv CS.AI/CS.EDU | **中文CSSCI·其他**（⚠️不匹配） |
| intel_07 | 中文期刊A | **国外AI教育新产品**（⚠️不匹配） |
| intel_08 | 中文期刊B | **UNESCO/OECD/WorldBank报告**（⚠️不匹配） |
| intel_09 | 中文期刊C | **各国政策文件**（⚠️不匹配） |
| intel_10 | UNESCO/OECD/WorldBank | **行业媒体动态**（⚠️不匹配） |
| intel_11 | 各国政策 | **YC/Product Hunt产品**（⚠️不匹配） |
| intel_12 | 补充搜索 | **补充来源（Stanford HAI等）**（✅基本匹配） |

**危害**：info_officer协调任务分配时，给出的intel分工描述是错的。如果info_officer spawn intel_02，它会告诉intel_02去搜"Frontiers in Education"，但intel_02实际是搜"ILE/CALL/ETRD"。

**修复方案**：info_officer的"搜索方法论"章节需要对照intel_01~12的实际SOUL.md全部重写。

---

### 矛盾2：edu_lead QUALITY_STANDARD.md 的审核角色 vs 实际reader_panel不匹配

**问题详情**：
QUALITY_STANDARD.md（四、审核角色）说：
- 资深教师（reader_senior_teacher）：准确性+逻辑+读者带走
- 新手教师（reader_new_teacher）：Hook+情感+读者带走
- 校长视角（reader_principal）：准确性+知识增量+转发动机
- 家长视角（reader_parent）：Hook+情感+节奏

**实际情况**（已注册5个reader，实际分工）：
- reader_parent ✅ 有
- reader_new_teacher ✅ 有
- reader_senior_teacher ✅ 有
- reader_principal ✅ 有
- reader_expert ✅ 有（QUALITY_STANDARD.md完全没有提及！）

**修复方案**：QUALITY_STANDARD.md需要增加reader_expert的审核维度，并重新校准5个读者的评分权重。

---

### 矛盾3：edu_reviewer 通过标准 vs edu_lead QUALITY_STANDARD.md 不一致

| 标准 | edu_reviewer SOUL.md | QUALITY_STANDARD.md |
|------|---------------------|-------------------|
| 通过分数 | ≥7.0 | ≥7.0（✅一致） |
| 否决触发 | 任何维度≤4分 | 发现虚构/无来源/3秒关闭/不知道做什么/制造焦虑（⚠️不完全一致） |
| 实际执行 | 8维度打分+否决 | 应该8维度+否决，但QUALITY_STANDARD.md的否决条件不包含"任何维度≤4分" |

**修复方案**：统一两份文件的否决标准。

---

## 三、🟡 内容错误

### 错误1：edu_writer 的素材库路径描述 vs 实际路径

**问题**：
edu_writer SOUL.md写："先读取 /workspace/knowledge/素材库/ 下的所有.md文件"

**实际情况**：
- 素材库：/workspace/knowledge/素材库/（存在）
- 原文库：/workspace/knowledge/原文库/（存在）
- intel搜索结果→原文库
- edu_writer应该读取→原文库

**修复**：edu_writer的素材库访问规则改为"先读取 /workspace/knowledge/原文库/"。

---

### 错误2：edu_reviewer SOUL.md 引用不存在的外部文件

**问题**：
edu_reviewer SOUL.md写："必读文件：/workspace/agents/edu_lead/QUALITY_STANDARD.md"

实际上QUALITY_STANDARD.md存在，但edu_reviewer需要能够读到它。这个路径是可以访问的，问题不大。

**实际问题是**：QUALITY_STANDARD.md中所有打分标准已经内嵌在edu_reviewer的SOUL.md里，edu_reviewer应该直接看自己SOUL.md里的8维度，不需要额外读文件（减少依赖）。

---

### 错误3：intel_01 的文件名格式可能导致文件名冲突

**问题**：
intel_01 SOUL.md写："写入 /workspace/knowledge/原文库/{DOI}.md"

实际文件路径通常是：`/workspace/knowledge/原文库/10.1016_j.compedu.2026.105620.md`

如果intel_02也写了同一篇论文到同一路径，会覆盖。但各intel_agent实际上搜不同来源，这个问题不大。

---

## 四、🟡 缺失项

### 缺失1：intel_07（国外AI教育新产品）缺少URL验证约束

**问题**：intel_07搜索Product Hunt/Y Combinator/EdSurge，这些是URL不是DOI，但没有任何"验证URL可访问性"的约束。如果Y Combinator返回了404，intel_07可能会把假产品信息写入原文库。

**修复**：intel_07 SOUL.md添加"写入前必须验证URL可访问性（curl -I验证）"。

---

### 缺失2：edu_reviewer SOUL.md 缺少DOI验证第9维度（P1改造未完成）

**问题**：FULL_ACCURATE_PLAN里说"edu_reviewer新增DOI真实性维度"，但至今未更新。

**修复**：在8维度之前新增：
```
0. DOI/arXiv真实性（强制前置检查）：洞察中所有引用是否已在doi.org/arXiv.org验证？有未验证DOI引用→一票否决
```

---

### 缺失3：intel_reviewer_* 审核范围不覆盖洞察文件（漏洞未封堵）

**问题**：intel_reviewer_en/cn/intl的SOUL.md只写"扫描原文库"，实际上洞察文件（collision_results_v2.md等）没有经过审核员的DOI抽查。

**修复**：intel_reviewer_en/intl的SOUL.md扩展为"原文库+洞察文件双重覆盖"。

---

## 五、🟠 冗余过长

### info_officer（568行）

**问题**：
- "核心原则·情报官工作的唯一正确标准"章节有大量哲学性描述（200+字），建议精简为3行核心原则
- "情报官团队架构·流水线设计"章节描述的intel_01~12分工与实际完全不符（见矛盾1），这部分应该完全重写
- 大量历史版本注释和调试信息

**建议**：
info_officer SOUL.md应该精简为：
- 核心原则（≤20行）
- spawn intel_01~12的任务模板（各5行）
- spawn intel_reviewer的任务模板（各3行）
- 汇报格式（≤10行）

---

## 六、🟡 格式问题

### 格式1：多处重复【素材库访问规则】段落

edu_writer、edu_reviewer、intel_*的SOUL.md都有一段完全相同的【素材库访问规则】，内容一模一样。这段应该提取为共享文件，改为：
```
【素材库/原文库访问】读取 /workspace/agents/SHARED_ACCESS_RULES.md
```

### 格式2：edu_lead QUALITY_STANDARD.md 第9维度缺失

reader_expert维度在5个reader里没有定义，但实际reader_expert存在。需要补全。

---

## 七、修复优先级

### P0（立即修复）
1. info_officer：重写intel_01~12分工描述，对照实际SOUL.md
2. edu_writer：修正素材库→原文库路径
3. edu_reviewer：新增DOI真实性第0维度（前置检查）
4. edu_lead QUALITY_STANDARD.md：增加reader_expert审核维度

### P1（1天内修复）
5. intel_reviewer_en/intl：扩展审核范围到洞察文件
6. intel_07：添加URL验证约束
7. 提取共享【素材库访问规则】为独立文件

### P2（本周内修复）
8. info_officer：精简到≤100行核心内容
9. edu_reviewer QUALITY_STANDARD.md vs SOUL.md：统一否决标准
10. edu_lead QUALITY_STANDARD.md：重新校准5个reader评分权重

---

## 八、各Agent最终正确分工（已核实）

### 情报团队
| Agent | 职责 | 审核范围 |
|-------|------|---------|
| intel_01 | 英文C&E/BJET/EIT | 期刊白名单+DOI验证 |
| intel_02 | 英文ILE/CALL/ETRD/iJET | 期刊白名单+DOI验证 |
| intel_03 | arXiv预印本 | arXiv ID验证 |
| intel_04 | 中文CSSCI·教育研究类 | cnki.net白名单 |
| intel_05 | 中文CSSCI·开放教育类 | cnki.net白名单 |
| intel_06 | 中文CSSCI·其他核心期刊 | cnki.net白名单 |
| intel_07 | 国外AI教育新产品 | URL可访问性验证 |
| intel_08 | UNESCO/OECD/WorldBank报告 | 官网URL验证 |
| intel_09 | 各国教育政策 | .gov/.gov.cn/.cn/people.cn |
| intel_10 | 行业媒体（EdSurge/EdTech Magazine/THE Journal） | URL验证 |
| intel_11 | YC/Product Hunt产品 | URL验证 |
| intel_12 | 补充来源（Stanford HAI等） | 信源白名单+URL验证 |
| intel_reviewer_en | 英文论文审核 | 原文库+洞察文件抽查 |
| intel_reviewer_cn | 中文论文审核 | 原文库 |
| intel_reviewer_intl | 产品/报告/政策审核 | 原文库+洞察文件抽查 |

### 内容团队
| Agent | 职责 | 审核维度 |
|-------|------|---------|
| edu_lead | 主编/决策中枢 | 信念共鸣+碰撞逻辑+推送决策 |
| edu_writer | 内容执笔 | HKRR四要素+DOI验证清单 |
| edu_researcher | 研究支持 | （按需调用） |
| edu_analyst | 数据分析 | （按需调用） |
| edu_reviewer | 学术终审 | 0.DOI真实性+8维度质量打分 |
| reader_parent | 家长视角 | Hook+情感+节奏 |
| reader_new_teacher | 新教师视角 | Hook+情感+读者带走 |
| reader_senior_teacher | 资深教师视角 | 准确性+逻辑+读者带走 |
| reader_principal | 校长视角 | 准确性+知识增量+转发动机 |
| reader_expert | 学术专家视角 | 学术严谨性+信念契合度+洞察独立性 |
