# MEMORY.md - 长期记忆

_最后更新：2026-03-28_

## 工作原则（铁律，2026-03-28 陛下明确）

**所有Agent调用必须100%使用已配置的持久Agent，禁止任何临时Spawn。**

### ✅ 正确调用方式
```bash
# 调用持久Agent（读取自己SOUL.md，继承固定身份）
sessions_spawn(runtime="acp", agentId="reader_parent", task="...", mode="run")

# 禁止方式（临时匿名会话，无Soul，无记忆，造假风险高）
sessions_spawn(runtime="subagent", task="...")  # ❌ 禁止
```

### ✅ 已配置的持久Agent完整清单

**情报线（info_officer团队）**
- `info_officer`（情报官/百晓生，Agent ID固定）：统筹协调，下辖intel_01~12
- `intel_01` ~ `intel_12`：搜索Agent（各自有SOUL.md，不可临时创建）

**内容创作线（edu_lead团队）**
- `edu_lead`（深度内容主编）：任务分配、审核把关
- `edu_writer`：内容执笔
- `edu_researcher`：研究方法支持（按需调用）
- `edu_analyst`：数据分析
- `edu_reviewer`：终审

**读者审核Panel（5个固定读者Agent）**
- `reader_parent`：家长视角（孩子上初中）
- `reader_new_teacher`：新教师视角（入职1-3年）
- `reader_senior_teacher`：资深教师视角（10年+）
- `reader_principal`：校长视角
- `reader_expert`：学术专家视角

**其他持久Agent**
- `xiaozhang`：校长Agent
- `xueqing_data`：学情数据Agent
- `agent_ip`：IP运营Agent
- `main`：小艾（我自己）

### ✅ 正确任务链路

```
陛下指令
    ↓
小艾（总调度）→ 分析任务类型
    ├── 情报收集类 → sessions_spawn(runtime="acp", agentId="info_officer", ...)
    ├── 深度内容类 → sessions_spawn(runtime="acp", agentId="edu_lead", ...)
    │       ↓
    │       edu_lead → sessions_spawn(runtime="acp", agentId="edu_writer", ...)
    │       ↓
    │       edu_writer → sessions_spawn(runtime="acp", agentId="reader_xxx", ...)  # 并行调用5个
    │                       sessions_spawn(runtime="acp", agentId="edu_reviewer", ...)
    ├── 校长事务类 → sessions_spawn(runtime="acp", agentId="xiaozhang", ...)
    └── 数据分析类 → sessions_spawn(runtime="acp", agentId="xueqing_data", ...)
```

### ✅ 情报官(info_officer)与百晓生的关系
- **两者是同一个Agent**：info_officer的SOUL.md里"小王"是百晓生的身份设定
- 情报官 = 百晓生 = `agentId="info_officer"`
- intel_01~12 是情报官下辖的搜索子Agent，由情报官自己spawn管理

### ❌ 严禁的行为（2026-03-28陛下禁令·永久铁律）
1. **禁止未经陛下授权Spawn任何Agent**：所有Spawn必须先请示陛下获得授权，绝不自行决定
2. 禁止用 `runtime="subagent"` 临时Spawn匿名会话
3. 禁止在任务描述里写角色设定（"你是家长""你是专家"）——角色在Agent的SOUL.md里
4. 禁止跳过edu_lead直接Spawn edu_writer
5. 禁止跳过info_officer直接Spawn intel_agents
6. 禁止用中文标签做subagent名称（reader_parent-v2b这类）
7. 禁止Spawn后不汇报、不监控、不追踪结果

### 读者Panel调用规范
- 5个读者Agent并行调用，不串行
- 每次调用：`sessions_spawn(runtime="acp", agentId="reader_xxx", task="请阅读文件X并评分", mode="run")`
- 不在task里重复角色设定，Agent自己读SOUL.md
- 收集5份评分后，小艾汇总综合报告上报陛下

---

## 关于陛下

- **称呼**：陛下
- **沟通风格**：直接、务实，不喜欢废话和客套

## 研究与关注领域

- **核心领域**：K12 AI教育（中小学人工智能教育）
- **关注视角**：
  - AI在K12课堂的实际效果与应用（AI辅导、个性化学习、作业批改）
  - AI对K12学生认知、情感、学习习惯的影响
  - K12 AI教育产品设计
  - 中国K12 AI教育政策动态（教育部、各省市）
  - 全球K12 AI教育研究（重点期刊：Computers & Education, BJET, Education and IT等）
- **产品视角**：关注面向中小学/设计K12 AI产品的研究和案例

## 信息追踪偏好

- 已建立**K12 AI教育日报**定时任务（每天05:00搜索，08:00发审核列表）
- 已建立**K12 AI教育周报**定时任务（每周六05:00搜索，08:00发审核列表）
- 详细配置见：`memory/task-config.md`
- 报告格式：HTML，三板块（新研究、新产品、新报告），重点推荐+折叠次要内容
- 优先关注：直接与K12相关的研究；非K12内容折叠处理

## 写作风格倾向

- 简洁、有观点，不堆砌
- 喜欢有数据支撑的表达
- 标题有网感、吸引点击
- 不喜欢官样文章和空洞表达

## 沟通格式偏好

- 飞书里不用 Markdown 表格，改用纯文字列表或分段输出
- 回复不要太长，重点突出
- **严禁使用 .org 格式**，无法预览
- 文档输出只用：Word (.docx)、HTML（手机和 Mac 都能打开的格式）
- **PDF 不预先生成**，除非陛下主动要求
- **HTML 要适配微信公众号编辑器**：用 inline styles，结构简洁，粘贴进编辑器后效果不变形；不依赖外部 CSS/JS

## 工具与平台

- 使用 OpenClaw + 飞书
- Node.js docx包已安装（/workspace/node_modules/docx）

## 已创建技能

- **md2wechat** - 将 Markdown 转换为微信公众号适配 HTML，触发词：公众号排版html、md转公众号、手机预览
- **edu-editor** - 教育深度内容编辑，输出K12教育公众号长文（1000-2500字），触发词：深度解读、长文创作、教育解读

## 进行中的项目

- **多Agent协作系统**（2026-03-05启动，2026-03-28全面清理完成）
  - 灵感来源：傅盛的"龙虾军团"
  - 4个核心Agent：管家小艾、情报官（百晓生）、主编（edu_lead）、内容运营（edu_writer）
  - 详细架构见：`/workspace/agents/ARCHITECTURE.md`
  - 错题本（共享记忆）：`/workspace/memory/error-log.md`
  - 共享Skills库：`/workspace/shared-skills/`

- **IP团队Agent注册（2026-03-28完成）**
  - ✅ reader_parent / reader_new_teacher / reader_senior_teacher / reader_principal / reader_expert：已注册
  - ✅ intel_reviewer_en（审核01·英文论文）
  - ✅ intel_reviewer_cn（审核02·中文论文）
  - ✅ intel_reviewer_intl（审核03·国际报告）
  - ✅ intel_01 / intel_02：已注册（intel_03~intel_12待陛下确认后注册）

- K12 AI教育日报自动化（**情报官已接管，Phase 2完成**）
  - intel_01~intel_12 均已注册（可用runtime="acp"调用）
---

## 2026-03-29 关键决策记录

### 洞察造假事故处理（14:39）
- 发现：edu_writer生成洞察1时虚构DOI（10.3389/feduc.2024.1476050，Frontiers官网404）
- 洞察1作废，collision_results_v2.md更新v1.1
- 修复：edu_writer SOUL.md新增DOI强制验证规则
- 根因：审核链有空白（intel_reviewer只扫原文库，不管洞察文件）

### Harness Engineering方法论确立（15:59）
- 核心精神：把正确行为编码成Agent的工程约束，不依赖自觉或人工检查
- 关键教训：Agent做不好→补全环境（添加工具/约束/规则），不是重试提示词
- 存放：/workspace/memory/HARNESS_ENGINEERING.md

### 多Agent系统升级方案（16:14）
- 三层质量门禁：搜索（DOI验证）→审核（intel_reviewer双重审查）→发布（edu_lead二次验证+Panel评分）
- SOUL.md改造：Core SOUL（≤100行）+ 详细手册（docs/）
- 方案待陛下审批后执行P0
- 存放：/workspace/agents/SYSTEM_UPGRADE_PLAN_v2.md

### 信念抽屉方法论（最新）
- 洞察生产必须锚定信念抽屉
- Hook句要求：≤20字，含数字或反常识
- 读者带走：给老师/家长/判断标准各≥50字
- 洞察2达到9.22分，已推送飞书
