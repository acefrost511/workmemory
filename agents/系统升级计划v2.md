# 多Agent系统全面升级方案
> 制定时间：2026-03-29 | 依据：Harness Engineering + 实战教训
> 状态：待陛下审批后执行

---

## 一、现状全图诊断

### 情报团队（Intel Team）

```
[搜索阶段]                    [审核阶段]                    [洞察生产]
intel_01~12                  intel_reviewer_en              edu_lead
   ↓                            ↓                           edu_writer
   ↓                            ↓                        reader_panel (×5)
写文件→原文库                  只扫原文库，不扫洞察文件           ↓
   ↓                            ↓                        edu_reviewer
   ↓                            ↓                           ↓
   × DOI验证靠搜索者自觉        × 不验证DOI本身是否真实          × 不二次验证DOI
   × 无格式标准化               × 无内容实质审查               × 无传播力评分
```

**当前架构问题：**
- intel_01~12：质量参差不齐，靠自觉而非约束
- intel_reviewer_*：只做"事后扫描原文库"，不在关键路径上拦截问题
- edu_writer：单点信任，无交叉验证，造假成本为零
- 全链路无任何DOI真实性强制验证节点
- 没有A/B对比机制（同一话题多个视角）

### IP团队（内容创作团队）

**当前架构问题：**
- edu_writer：唯一内容生产者，单点故障
- edu_lead：既是裁判又是运动员（分配任务+审核+决定推送）
- reader_panel：评分维度混乱（严格度/传播力/相关性混在一起）
- 无"文章质量达标线"概念，分数不与推送决策挂钩
- 无"洞察选题委员会"机制，选题随机性强

---

## 二、核心重构：三层质量门禁体系

### 设计原则（Harness Engineering）

```
不依赖Agent的自觉，依赖系统的约束
不依赖人工检查，依赖自动化的门禁
不依赖事后补救，依赖事前拦截
```

### 三层门禁设计

```
第一层：搜索门禁（intel_agent）
  入口：搜索结果
  门禁：DOI/URL必须可验证，文件格式标准化
  出口：通过→原文库，拒绝→打回重搜

第二层：审核门禁（intel_reviewer_*）
  入口：原文库文件
  门禁：内容实质审查（DOI指向真实论文+内容相关性+无虚构）
  出口：通过→洞察素材库，拒绝→标记删除

第三层：发布门禁（edu_lead + edu_reviewer）
  入口：edu_writer生成的洞察草稿
  门禁：DOI二次全量验证 + 5视角Panel评分
  出口：综合分≥9.0→推送，<9.0→打回重写
```

---

## 三、情报团队改造方案

### 3.1 intel_agent搜索标准流程（所有intel_01~12通用）

```
第一步：执行搜索
第二步：对每个搜索结果DOI验证（调用 doi.org/{DOI} 或 arxiv.org/abs/{ID}）
        → 验证失败→跳过该结果，不写入文件
第三步：验证通过→写入原文库
        → 文件名格式：{DOI或arXivID}_{简短标题}_{日期}.md
        → 文件内必须包含：DOI验证URL + 验证状态
第四步：搜索完成后输出搜索报告（找到X个，验证通过X个，跳过X个）
```

### 3.2 intel_reviewer_工作升级

**现行问题**：只扫描文件是否存在于原文库，不验证内容本身

**升级方案**：
- intel_reviewer_en：英文论文 DOI真实性 + 内容实质双重审查
- intel_reviewer_cn：中文论文 期刊白名单 + 内容相关性审查
- intel_reviewer_intl：产品/报告 官网URL可访问性 + 数据可查证性审查

**新增交叉验证机制**：
- intel_reviewer_en 审核通过的文件 → intel_reviewer_intl 随机抽查10%（防漏网之鱼）
- 每季度一次：全部原文库文件DOI重新跑一遍验证

### 3.3 intel_agent分类管理

| Agent | 职责 | 核心约束 |
|-------|------|---------|
| intel_01 | 英文权威期刊（C&E/BJET/ILE） | DOI必须来自白名单期刊 |
| intel_02 | 国际教育技术期刊（ETRD/iJET/CALL） | 同上 |
| intel_03 | arXiv预印本 | arXiv ID必须在arxiv.org/abs可访问 |
| intel_04 | 中文CSSCI期刊（教育研究类） | 必须在cnki.net可查 |
| intel_05 | 中文CSSCI期刊（开放教育类） | 同上 |
| intel_06 | 中文核心教育期刊（其他） | 同上 |
| intel_07 | 国外AI教育新产品 | 官网URL必须可访问 |
| intel_08 | 国际机构报告（UNESCO/OECD/WorldBank） | 官网可下载 |
| intel_09 | 各国教育政策文件 | 官网或政府域名.gov/.cn等 |
| intel_10 | 行业媒体动态（EdSurge/EdTech Magazine） | 媒体白名单+URL可访问 |
| intel_11 | AI教育新产品（Product Hunt/Y Combinator） | 官网/官方信源 |
| intel_12 | 补充来源（Stanford HAI/Gartner等） | 信源白名单+URL可访问 |

---

## 四、IP团队改造方案

### 4.1 edu_writer强化

**核心约束（铁律写入SOUL.md）**：
- 每条引用必须包含：DOI/arXiv URL + 验证状态 + 在原文库中的文件名
- 禁止使用"我没有核实但我相信是真的"类表述
- 数据类引用：必须标注来源文件路径，非搜索结果声称
- 虚构场景用于说明逻辑 → 必须在洞察末尾声明"以下为思想实验性描述，非实证数据"

**工作流程**：
```
读取原文库文件（不是搜索结果）→ 提取数据 → 写洞察
    ↓
对洞察中每个DOI/arXiv URL调用验证
    ↓
验证全部通过 → 输出洞察v1（含验证状态说明）
    ↓
验证有失败 → 立即删除失败引用，重写相关段落
```

### 4.2 edu_lead角色重构

**拆分"裁判"和"运动员"角色**：

| 功能 | 原来 | 改造后 |
|------|------|--------|
| 任务分配 | edu_lead | edu_lead |
| 内容执笔 | edu_lead spawn edu_writer | edu_writer（独立Agent） |
| 学术质量审核 | edu_lead | edu_reviewer（独立审核） |
| 传播力评分 | reader_panel | reader_panel（独立评分） |
| 推送决策 | edu_lead | edu_lead（汇总三方意见决策） |

**edu_lead新增职责**：
- DOI二次全量验证（独立于intel_reviewer_，最后一公里拦截）
- 洞察→信念锚定映射（确保洞察真正在信念框架内运作）
- 推送决策（综合edu_reviewer学术评分 + reader_panel传播力评分）

### 4.3 edu_reviewer新增（K12 AI教育学术审核专家）

独立Agent，不隶属于edu_writer或reader_panel，定位为"K12 AI教育学术审核专家"：

```
职责：
- 学术真实性：洞察中每个引用是否真实可查（DOI/arXiv必须已验证）
- 学术规范性：研究描述是否准确（作者/期刊/年份/方法与原文一致）
- 逻辑一致性：洞察逻辑是否与原始研究一致（不夸大/不曲解）
- 适用性判断：研究发现在K12场景是否可迁移/有无重大条件限制

输出格式：
- 学术真实性：✅/❌（列出所有DOI/arXiv验证状态）
- 规范性评分：1-10分
- 主要问题：如有问题具体说明
- K12适用性：✅/⚠️/❌（研究发现在K12场景的适用性）
- 综合建议：可推送 / 需修改后推送 / 不可推送
```

### 4.4 reader_panel评分体系重构

**现行问题**：5个评委维度混在一起（严格度/传播力/相关性）

**改造方案**：5维度独立评分

| 评委 | 维度1（核心） | 维度2 | 维度3 |
|------|-------------|-------|-------|
| reader_parent | 可操作性（家长能做什么） | 真实性感知 | 情感共鸣 |
| reader_new_teacher | 可操作性（新教师能落地） | 新颖性 | 共鸣感 |
| reader_senior_teacher | 深刻性（资深教师认可） | 实用性 | 创新性 |
| reader_principal | 传播性（学校可推广） | 数据支撑 | 价值导向 |
| reader_expert | 学术严谨性 | 信念契合度 | 洞察独立性 |

**最终推送决策**：
- edu_reviewer学术评分 ≥ 8.0 → 进入reader_panel评分
- reader_panel综合分（5维度均值）≥ 9.0 → 推送
- 任一评委单项 < 6.0 → 自动打回重写

---

## 五、自动化品质保障基础设施

### 5.1 DOI实时验证工具（所有Agent共享）

创建共享验证工具，所有Agent在写入文件前必须调用：

```python
# /workspace/tools/doi_validator.py（待实现）
def verify_doi(doi):
    """调用doi.org验证DOI真实性，返回(True/False, paper_title)"""
    url = f"https://doi.org/{doi}"
    # 访问验证
    # 返回真实论文标题用于核对
    
def verify_arxiv(arXiv_id):
    """调用arxiv.org/abs验证arXiv ID真实性"""
    url = f"https://arxiv.org/abs/{arXiv_id}"
    # 访问验证
```

**强制使用规则**：
- intel_agent搜索时：每个结果调用一次验证，失败则跳过
- edu_writer写洞察时：每个引用调用一次验证，失败则删除该引用
- edu_lead推送前：洞察中所有DOI/arXiv全量验证，失败则打回edu_writer

### 5.2 洞察质量计分板（公开文件）

```markdown
# 洞察质量计分板

| 洞察ID | 信念锚定 | DOI验证状态 | edu_reviewer分 | reader_panel均分 | 最终分 | 状态 |
|--------|---------|-----------|--------------|----------------|-------|------|
| 20260329-01 | 信念2 | ❌虚构（作废）| N/A | 8.82 | N/A | ❌作废 |
| 20260329-02 | 信念6 | ✅×2通过 | 待评 | 9.22 | 待最终 | 🔄审核中 |
| 20260329-03 | 信念1 | ✅×2通过 | 待评 | 8.90 | 待最终 | 🔄审核中 |
```

### 5.3 增量验证机制（替代全量熵清理）

**触发时机**：每当新文件进入原文库时，立即触发DOI验证
- intel_agent写完文件后 → 自动调用DOI验证 → 通过才标记为"已验证"
- 发现失效DOI→标记→通知所属intel_agent重新搜索
- 发现内容质量问题→触发intel_reviewer_重新审核

**增量验证流程**：
```
新文件写入原文库
    ↓
自动触发DOI/arXiv验证（每次只验证1个文件）
    ↓
验证通过→文件标记"✅DOI已验证+时间戳"
    ↓
验证失败→文件标记"❌DOI失效+通知所属intel_agent"
    ↓
intel_agent收到通知后→删除失效文件+重新搜索
```

**Token消耗估算**：每篇新文件触发1次DOI验证，约消耗100-500 tokens/篇，按每日新增10篇计算每日最多5000 tokens，完全可接受。

---

## 六、Agent体系总览（改造后）

```
【情报团队】
info_officer（协调中枢）
    ├── intel_01（英文C&E/BJET）
    ├── intel_02（英文ILE/ETRD）
    ├── intel_03（arXiv）
    ├── intel_04（中文CSSCI-1）
    ├── intel_05（中文CSSCI-2）
    ├── intel_06（中文核心期刊）
    ├── intel_07（国际新产品）
    ├── intel_08（UNESCO/OECD/WorldBank）
    ├── intel_09（各国政策）
    ├── intel_10（行业媒体）
    ├── intel_11（YC/Product Hunt）
    ├── intel_12（补充来源）
    └── intel_reviewer_en（英文审核）→ intel_reviewer_intl（随机抽查）
        intel_reviewer_cn（中文审核）

【内容创作团队】
edu_lead（主编/决策中枢）
    ├── edu_writer（执笔）
    ├── edu_reviewer（学术审核）← 新增
    ├── edu_analyst（数据分析）
    └── reader_panel（5视角评分）
        ├── reader_parent（家长）
        ├── reader_new_teacher（新教师）
        ├── reader_senior_teacher（资深教师）
        ├── reader_principal（校长）
        └── reader_expert（学术专家）

【共享基础设施】
├── DOI验证工具（所有Agent强制使用）
├── 洞察质量计分板（公开文件）
├── 熵清理Agent（每周定时）
└── 错题本（error-log.md）
```

---

## 七、改造优先级与时间安排

### P0（立即执行，1天内）
- [ ] intel_01~12 SOUL.md添加DOI验证强制步骤（搜索时验证，失败则跳过）
- [ ] edu_writer SOUL.md添加DOI使用强制规则（已有）
- [ ] edu_lead添加DOI二次全量验证步骤
- [ ] 洞察文件更新v1.1（洞察1作废，洞察2/3保留）

### P1（3天内）
- [ ] edu_reviewer独立Agent创建（学术审核）
- [ ] reader_panel评分体系重构（5维度独立）
- [ ] 洞察质量计分板建立
- [ ] intel_reviewer_交叉抽查机制建立

### P2（1周内）
- [ ] DOI验证工具实现并内置到各Agent流程
- [ ] 熵清理机制建立（每周定时）
- [ ] intel_agent搜索报告标准化
- [ ] edu_writer→洞察输出格式标准化

### P3（长期）
- [ ] info_officer重建（ACP运行时修复后）
- [ ] A/B视角机制（同一话题多个洞察版本）
- [ ] 洞察效果追踪（阅读量/转发量/反馈收集）
