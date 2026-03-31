# 现有Agent体系真实流程图（截至2026-03-29）

> 依据：现有Agent目录核查 + SOUL.md实际内容
> 状态：**已核实**，不是想象

---

## 一、现有Agent完整清单（37个）

### 情报团队（14个）
- info_officer（协调中枢）
- intel_01 / intel_02 / intel_03（英文期刊/arXiv）
- intel_04 / intel_05 / intel_06（中文CSSCI）
- intel_07 / intel_08 / intel_09（国际产品/报告/政策）
- intel_10 / intel_11 / intel_12（行业媒体/YC/补充来源）
- intel_reviewer_en / intel_reviewer_cn / intel_reviewer_intl（审核）

### 内容创作团队（8个）
- edu_lead（主编/协调中枢）
- edu_writer（内容执笔）
- edu_researcher（研究支持）
- edu_analyst（数据分析）
- edu_reviewer（**终审·8维度打分**）← 存在
- reader_parent / reader_new_teacher / reader_senior_teacher / reader_principal / reader_expert（5视角Panel）

### 其他Agent
- xiaozhang（校长）、xueqing_data（学情数据）、agent_ip（IP运营）、zhubian

---

## 二、现有真实流程（实测确认）

```
[第一阶段：情报搜索]
info_officer spawn intel_01~12（并行或分批）
    ↓
intel_01~12 各自写文件 → /workspace/knowledge/原文库/

[第二阶段：审核过滤]
intel_reviewer_en 扫描 原文库（英文论文）
intel_reviewer_cn 扫描 原文库（中文论文）
intel_reviewer_intl 扫描 原文库（产品/报告/政策）
    ↓
各审核结果写入 /workspace/knowledge/scores/

[第三阶段：洞察生成]
edu_lead 读取 原文库 + 审核结果
    ↓
edu_lead spawn edu_writer → 生成洞察草稿
    ↓
edu_lead spawn edu_reviewer → 8维度打分（准确性/逻辑/Hook/知识增量/情感共鸣/读者带走/节奏/转发动机）
    ↓
edu_lead spawn 5个reader_panel → 5视角评分
    ↓
edu_lead 汇总 edu_reviewer分 + reader_panel分
→ 综合分≥7.0 → edu_lead推送飞书
→ <7.0 → 打回edu_writer重写
```

---

## 三、现有流程的关键验证点

| 阶段 | 验证什么 | 谁来做 | 覆盖范围 |
|------|---------|--------|---------|
| intel搜索时 | DOI/arXiv真实性 | intel_agent自己 | 搜索结果 |
| intel审核 | 内容相关性/实质性/无虚构 | intel_reviewer_* | 原文库文件 |
| edu_writer写洞察 | 引用的DOI是否真实 | edu_writer自己 | **漏洞：没有强制约束** |
| edu_reviewer终审 | 8维度质量+虚构核查 | edu_reviewer | 洞察草稿 |
| reader_panel | 5视角传播力评分 | reader_panel | 洞察草稿 |

---

## 四、发现的核心漏洞

**漏洞只有一个：edu_writer写洞察时，没有强制DOI二次验证**

- intel_agent负责搜索 → intel_reviewer_*负责审核文件 → 都有DOI验证环节
- 但edu_writer从原文库提取内容写洞察 → 这一步的DOI引用没有强制验证
- 今天洞察1的虚构DOI就是这样漏进来的：intel_01的DOI是真的，intel_reviewer_*审的是原文库文件（也是真的），但edu_writer在写洞察时**自己编了一个假DOI**

---

## 五、edu_reviewer的准确角色

**已有的，不是新增的：**

- **角色定义**：K12教育内容团队终审Agent
- **职责**：对照QUALITY_STANDARD.md的8个维度打分 + 虚构核查
- **位置**：在edu_writer生成洞察草稿之后，edu_lead推送之前
- **输入**：洞察草稿 + 原文库
- **输出**：8维度打分 + 综合结论（通过/修改/否决）
- **否决线**：任何维度≤4分直接否决

**注意**：edu_reviewer的虚构核查是**内容层面**的（洞察中的人物/场景/数据是否有来源），**不是DOI层面**的（DOI本身是否真实）。DOI真实性应该在intel搜索和edu_writer引用时就验证完毕。

---

## 六、改造方案（最小改动，只补漏洞）

**P0（立即执行）：edu_writer写洞察时强制DOI验证**

在edu_writer的SOUL.md已有【DOI使用强制规则】，问题是执行时可能遗漏。
改造方案：在洞察输出格式里强制要求包含「DOI验证清单」，没有这个清单edu_lead视为不合格。

```
【洞察输出格式·必须包含】
1. 每条引用必须附DOI/arXiv ID + 验证URL + 验证状态
2. 附DOI验证清单：
   - DOI-1：10.XXXX/XXXXX → https://doi.org/10.XXXX → ✅通过
   - DOI-2：10.XXXX/XXXXX → https://doi.org/10.XXXX → ✅通过
3. 如有DOI验证失败：该引用立即删除，不写入洞察
```

**P1（3天内）：edu_reviewer增强「DOI核查」维度**

在edu_reviewer的QUALITY_STANDARD.md中新增第9个维度：
- **DOI真实性（新增，强 制）**：洞察中所有DOI/arXiv是否已验证？如有未验证DOI引用，一票否决。

**P2（本周内）：intel_reviewer_*增加洞察文件抽查**

 intel_reviewer_*的任务范围从"只扫原文库"扩展为"原文库+洞察文件"双重覆盖：
- intel_reviewer_en：每生成一条洞察，随机抽1-2个DOI发doi.org验证
- 验证失败→立即通知edu_lead，洞察打回重写

---

## 七、改造后的完整流程

```
[第一阶段：情报搜索]
info_officer spawn intel_01~12
    ↓
每个intel_agent搜索时强制DOI验证 → 不通过则跳过
→ 写入原文库

[第二阶段：审核过滤]
intel_reviewer_en 扫描原文库
intel_reviewer_cn 扫描原文库
intel_reviewer_intl 扫描原文库+洞察文件（新增）
    ↓
通过 → 进入素材库

[第三阶段：洞察生成]
edu_lead 读取原文库+审核结果
    ↓
edu_lead spawn edu_writer
→ edu_writer写洞察时强制DOI二次验证
→ 输出洞察v1（含DOI验证清单，无验证清单edu_lead打回）
    ↓
edu_lead spawn edu_reviewer（8维度+DOI真实性新增）
→ 任何维度≤4分 OR DOI未验证 → 否决
    ↓
edu_lead spawn 5个reader_panel（5视角评分）
    ↓
edu_lead汇总：edu_reviewer分+reader_panel分
→ edu_reviewer通过 AND 综合分≥9.0 → 推送飞书
→ 否则 → 打回edu_writer重写
```

---

## 八、不新增Agent，只补漏洞

| 问题 | 解决方案 | 改动范围 |
|------|---------|---------|
| edu_writer可能跳过DOI验证 | 在输出格式里强制要求DOI验证清单 | 修改edu_writer的SOUL.md |
| edu_reviewer不知道检查DOI | QUALITY_STANDARD.md新增DOI真实性维度 | 修改QUALITY_STANDARD.md |
| intel_reviewer_*只扫原文库 | 扩展覆盖洞察文件（增量小，每周几条洞察） | 修改intel_reviewer_*的SOUL.md |

**不新增edu_reviewer（已有，保留），不新增其他Agent。**
