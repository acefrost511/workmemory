# K12 AI教育资讯搜索与创作任务计划（第12周）

## 任务概述
- **任务目标**：执行情报官工作流程，搜索K12 AI教育资讯，筛选后用K12 AI教育资讯速览写作技能输出
- **时间范围**：2026年3月16日-22日（第12周）
- **开始时间**：2026-03-17
- **负责人**：臣

---

## 阶段一：资讯搜索（情报官角色）

### 📋 计划
- 调用情报官（info_officer）执行搜索
- 使用web_search工具真实搜索K12 AI教育最新资讯
- 搜索来源：
  - 英文期刊：Computers & Education、Education and Information Technologies、British Journal of Educational Technology等
  - 中文期刊：教育研究、中国电化教育、远程教育杂志等
  - 国际报告：UNESCO、OECD、世界银行
  - 国内政策：教育部、省级教育厅
  - 行业动态：教育科技企业官方发布

### 🔄 行动
**步骤1：搜索英文期刊最新研究**
📋 计划：搜索Computers & Education期刊2026年K12 AI教育相关论文
🔄 行动：使用web_search搜索"site:sciencedirect.com/journal/computers-and-education K12 artificial intelligence education 2026"
✅ 结果：等待返回...
📊 状态：进行中...

**步骤2：搜索英文期刊BJET最新研究**
📋 计划：搜索British Journal of Educational Technology期刊2026年K12 AI教育相关论文
🔄 行动：使用web_search搜索"site:onlinelibrary.wiley.com/journal/14678535 K12 artificial intelligence education 2026"
✅ 结果：等待返回...
📊 状态：待开始

**步骤3：搜索中文期刊最新研究**
📋 计划：搜索中国电化教育等期刊2026年K12 AI教育相关论文
🔄 行动：使用web_search搜索"site:cnki.net K12 人工智能 教育 2026"
✅ 结果：等待返回...
📊 状态：待开始

**步骤4：搜索国际组织最新报告**
📋 计划：搜索UNESCO、OECD、世界银行2026年K12 AI教育相关报告
🔄 行动：使用web_search搜索"UNESCO OECD world bank K12 artificial intelligence education report 2026"
✅ 结果：等待返回...
📊 状态：待开始

**步骤5：搜索国内政策最新动态**
📋 计划：搜索教育部2026年K12 AI教育相关政策
🔄 行动：使用web_search搜索"site:moe.gov.cn K12 人工智能 教育 政策 2026"
✅ 结果：等待返回...
📊 状态：待开始

### ✅ 结果（预期）
- 总资讯≥40篇
- 研究论文≥30篇（75%）
- 行业报告≤8篇（20%）
- 新政策≤2篇（5%）

### 📊 状态
- [x] 进行中

---

## 阶段二：选题筛选（K12教育专家角色）

### 📋 计划
- 调用K12教育专家（k12_jiaoyu_zhuanti）
- 精选10-15条资讯
- 场景比例：教师80%，家庭20%

### 🔄 行动
- 从搜索结果中筛选
- 标注场景：教师/家庭

### ✅ 结果（预期）
- 精选资讯清单（10-15条）
- 提交陛下决定最终选题

### 📊 状态
- [ ] 待开始

---

## 阶段三：内容创作（K12教育专家+自媒体达人）

### 📋 计划
- 调用K12教育专家+自媒体达人
- 使用 k12-edu-news-writer 技能
- 产出【精选资讯速览】

### 🔄 行动
- 基于精选资讯创作
- 使用精选资讯速览写作模板

### ✅ 结果（预期）
- 精选资讯速览（10-15条）
- 每条包含：emoji + 一句话总览 + 背景 + 关键发现 + 对K12的意义 + 来源/日期/链接

### 📊 状态
- [ ] 待开始

---

## 备注
- 使用 web_search 工具真实搜索
- 场景比例：教师80%，家庭20%
- 情报官只搜索不写报告，K12教育专家负责撰写
