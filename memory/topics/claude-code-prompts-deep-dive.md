# Claude Code 记忆与Agent系统 — 完整提示词拆解

> 目的：逐条拆解Claude Code的记忆体系、做梦机制、会话记忆、记忆抽取等核心提示词，
> 评估哪些可直接引用、哪些需调整后用于我们的架构。

---

## 一、记忆系统核心配置（teamMemPrompts.ts — 25条提示词）

### 1.1 记忆文件格式（frontmatter）

```
每条记忆单独存为一个文件，使用 frontmatter 格式：
---
name:       记忆名称
description: 一句话描述
type:       类型（如 fact/preference/convention）
---

记忆正文内容...
```

**关键规则**：
- `name`、`description`、`type` 必须始终与内容保持一致
- 记忆按**主题语义**组织，而非时间顺序
- 错误或过时的记忆要**主动更新或删除**
- 不写重复记忆——先查已有再决定新建还是更新

### 1.2 两步保存流程

**步骤1**：写记忆文件（如 `user_role.md`）
**步骤2**：在 `MEMORY.md` 中加索引条目

索引格式：
```
- [Title](file.md) — one-line hook
```

约束：
- 每条索引 ≤ 150 字符
- MEMORY.md 是**索引**，不是内容堆放区
- 超过 200 行会被截断
- 不带 frontmatter

### 1.3 记忆系统定位

> 你拥有一个持久化、基于文件的记忆系统。你应随着时间不断建设它，
> 以便未来的对话能够完整了解用户是谁、他们希望如何与你协作、
> 哪些行为应避免或重复，以及他们交给你的工作背后的上下文。

### 1.4 两个作用域层级

| 层级 | 作用域 | 持续性 |
|------|--------|--------|
| **private** | 仅你和当前用户之间 | 跨对话持续 |
| **team** | 项目内所有用户共享 | 每次会话开始同步 |

⚠️ 禁止在团队记忆中保存敏感数据（API密钥、凭证等）

### 1.5 何时访问记忆

- 记忆与当前事项相关
- 用户提到之前做过的工作
- 用户明确要求检查、回忆或记住
- 如果用户说"ignore memory"，按MEMORY.md为空处理

### 1.6 记忆 vs 其他持久化机制

| 机制 | 适用场景 |
|------|---------|
| **记忆** | 跨对话、未来仍有价值的信息 |
| **计划(Plan)** | 当前对话的实现方案，需要与用户对齐 |
| **任务(Tasks)** | 当前对话的工作拆分和进度跟踪 |

> 记忆不应保存只在当前对话范围内有用的信息。

---

## 二、记忆抽取子Agent（extractMemories/prompts.ts — 20条提示词）

### 2.1 身份定义

```
You are now acting as the memory extraction subagent.
Analyze the most recent ~N messages above and use them 
to update your persistent memory systems.
```

### 2.2 可用工具限制

- ✅ Read（读取文件）
- ✅ Write（写入文件，仅限记忆目录）
- ✅ Edit（编辑文件，仅限记忆目录）
- ✅ 只读 Bash（ls/find/cat/stat/wc/head/tail）
- ❌ rm 不允许
- ❌ MCP工具不允许
- ❌ Agent工具不允许
- ❌ 可写 Bash 不允许

### 2.3 回合预算与效率策略

```
Turn 1: 并行发出所有 Read 调用（可能需要更新的文件）
Turn 2: 并行发出所有 Write/Edit 调用
不要交替读写！
```

### 2.4 内容来源限制

```
你只能使用最近 ~N 条消息的内容。
不要浪费回合去调查或验证：
- 不要 grep 源文件
- 不要读代码确认模式
- 不要执行 git 命令
```

### 2.5 写入规则

1. 先检查已有文件 → 更新而非重复
2. 步骤1：写记忆文件（frontmatter格式）
3. 步骤2：更新MEMORY.md索引
4. 用户明确要求记住 → 立即保存
5. 用户要求忘记 → 找到并删除

---

## 三、做梦/记忆整合机制（autoDream/consolidationPrompt.ts — 1条长提示词）

### 3.1 核心定位

```
你正在执行一次 dream，也就是对记忆文件进行一轮反思式梳理。
请将你最近学到的内容综合整理成持久、结构良好的记忆，
以便未来会话能够快速建立方向感。
```

### 3.2 输入

- 记忆目录路径
- MEMORY.md 索引
- 会话转录（大型JSONL文件）

### 3.3 四阶段流程（完整原文）

#### 阶段1：建立方向感
```
- 使用 ls 查看记忆目录中已经有哪些内容
- 阅读 MEMORY.md 以理解当前索引
- 快速浏览已有主题文件，目标是改进已有内容，而不是制造重复条目
- 如果存在 logs/ 或 sessions/ 子目录，查看其中最近的条目
```

#### 阶段2：收集近期信号
```
1. Daily logs（YYYY-MM-DD.md）— 只追加的流水记录，优先级最高
2. 已经漂移的现有记忆 — 与当前事实矛盾的内容
3. 转录搜索 — 用窄关键词 grep：
   grep -rn "<narrow term>" --include="*.jsonl" | tail -50
   不要穷尽式通读转录！只查找已怀疑重要的内容。
```

#### 阶段3：整合
```
- 把新信号并入已有主题文件，而不是创建近似重复的新文件
- 将相对日期（"昨天""上周"）转换成绝对日期
- 删除被证伪的事实；如果今天的调查推翻了一条旧记忆，要在源头上修正它
```

#### 阶段4：修剪与索引
```
更新 MEMORY.md：
- 保持在 N 行以内，总大小不超过约 25KB
- 它是一个索引，不是内容堆放区
- 每条一行，约 150 字符，格式：- [Title](file.md) — one-line hook
- 绝不要把记忆内容直接写进去

修剪规则：
- 删除过时、错误或被替代的索引
- 缩短过长的索引行（>200字符说明承载了太多内容）
- 为新近重要的记忆添加索引
- 解决矛盾：两个文件不一致就修正错误的那个
```

### 3.4 输出

```
返回一段简短总结，说明你整合、更新或修剪了什么。
如果没有变化，也要直接说明。
```

---

## 四、会话记忆（SessionMemory/prompts.ts — 4条提示词）

### 4.1 会话记忆模板（10个固定板块）

```markdown
# Session Title
_A short and distinctive 5-10 word descriptive title for the session. Super info dense, no filler_

# Current State
_What is actively being worked on right now? Pending tasks not yet completed. Immediate next steps._

# Task specification
_What did the user ask to build? Any design decisions or other explanatory context_

# Files and Functions
_What are the important files? In short, what do they contain and why are they relevant?_

# Workflow
_What bash commands are usually run and in what order? How to interpret their output if not obvious?_

# Errors & Corrections
_Errors encountered and how they were fixed. What did the user correct? What approaches failed and should not be tried again?_

# Codebase and System Documentation
_What are the important system components? How do they work/fit together?_

# Learnings
_What has worked well? What has not? What to avoid? Do not duplicate items from other sections_

# Key results
_If the user asked a specific output such as an answer to a question, a table, or other document, repeat the exact result here_

# Worklog
_Step by step, what was attempted, done? Very terse summary for each step_
```

### 4.2 编辑规则

- 每个section有两部分必须保持不变：
  1. `# Section Header`（标题行）
  2. `_italic description_`（斜体模板说明）
- 只更新这两部分之下的实际内容
- 不要添加新section
- 不要引用"笔记记录"过程本身
- 没有实质新内容时跳过更新，不写"No info yet"
- 每个section控制在 ~N tokens/words 以内

### 4.3 压缩规则

```
当会话记忆超过最大token限制时：
1. 积极压缩过大section
2. 移除次要细节
3. 合并相关条目
4. 总结旧条目
5. 优先保留 "Current State" 和 "Errors & Corrections"
```

### 4.4 结构保护机制

```
STRUCTURE PRESERVATION REMINDER:
Each section has TWO parts that must be preserved exactly:
1. The section header (line starting with #)
2. The italic description line

You ONLY update the actual content that comes AFTER these two preserved lines.
```

这个设计极其精妙——模板说明永不被内容覆盖。

---

## 五、上下文压缩（compact/prompt.ts — 14条提示词）

### 5.1 核心约束

```
CRITICAL: Respond with TEXT ONLY. Do NOT call any tools.
Tool calls will be REJECTED and will waste your only turn.
```

### 5.2 输出格式

```
<analysis>
[按时间顺序分析每条消息...]
</analysis>

<summary>
1. Primary Request and Intent: ...
2. Key Technical Concepts: ...
3. Files and Code Sections: ...
4. Errors and fixes: ...
5. Problem Solving: ...
6. All user messages: ...
7. Pending Tasks: ...
8. Current Work: ...
9. Optional Next Step: ...
</summary>
```

### 5.3 分析要求

1. 按时间顺序分析每条消息和每个section
2. 识别：用户请求、你的方法、关键决策、技术概念、代码模式
3. 特别注意用户反馈（尤其是要求你做不同方式的）
4. 双重检查技术准确性和完整性

---

## 六、对我们架构的适配方案

### 6.1 可直接引用的部分

| Claude Code 组件 | 我们可直接采用 | 说明 |
|------------------|---------------|------|
| 两步保存流程 | ✅ 直接引用 | 步骤1写文件 → 步骤2更新索引 |
| MEMORY.md索引格式 | ✅ 直接引用 | `- [Title](file.md) — one-line hook` |
| 做梦四阶段流程 | ✅ 调整后引用 | 增加"创意碰撞"阶段 |
| 会话记忆10板块模板 | ⚠️ 调整后引用 | 简化为我们的场景 |
| 记忆抽取子Agent设计 | ✅ 直接引用 | 有限回合、并行读写 |
| 结构保护机制 | ✅ 直接引用 | 模板说明不被覆盖 |

### 6.2 需要调整的部分

| 调整点 | 原因 | 调整方案 |
|--------|------|---------|
| 做梦阶段增加"创意碰撞" | 大人特别要求 | 新增阶段5：关联不同主题，生成新洞察 |
| 会话记忆简化 | 我们不主要做编程 | 减少代码相关板块，增加"讨论要点""创意灵感" |
| 每日日志格式 | 我们需要快速检索 | 使用结构化格式（时间戳+标签+内容） |
| 记忆类型 | 丰富记忆维度 | 增加 `insight`（洞察）、`idea`（灵感）等类型 |

### 6.3 需要新建的部分

| 新组件 | 说明 |
|--------|------|
| 每日对话日志 | 记录每天的所有对话要点 |
| 做梦记录 | 记录每次做梦的结果和产出 |
| 创意碰撞机制 | 关联不同记忆，产生新想法 |
| 快速检索 | 支持按日期/主题/关键词检索 |

---

## 七、建议的记忆文件目录结构

```
.workbuddy/memory/
├── MEMORY.md                    ← 纯索引（≤200行，≤25KB）
├── topics/                      ← 按主题组织的持久记忆
│   ├── core-principles.md       ← 核心原则（如"实事求是"）
│   ├── claude-code-study.md     ← 学习笔记
│   ├── book-instructional-illusions.md  ← 读书笔记
│   └── ...                      ← 随时间增长
├── logs/                        ← 每日对话日志（只追加）
│   └── 2026/
│       ├── 2026-04-04.md        ← 今天
│       └── YYYY-MM-DD.md        ← 以后每天
├── dreams/                      ← 做梦记录
│   ├── 2026-04-04.md            ← 今天做梦的产出
│   └── YYYY-MM-DD.md
└── sessions/                    ← 会话级记忆（可选）
    └── session-xxx.md
```

### MEMORY.md 索引示例

```markdown
# MEMORY.md - 长期记忆索引

## 核心要求
- [最高准则](topics/core-principles.md) — 实事求是，绝不编造欺骗

## 角色设定
- [身份与称呼](topics/core-principles.md) — 总管/在下，大人

## 学习笔记
- [Claude Code架构](topics/claude-code-study.md) — 记忆体系/做梦/多Agent架构
- [教学幻觉](topics/book-instructional-illusions.md) — 10种教学幻觉详解

## 创意与洞察
- [创意碰撞-待补充](dreams/2026-04-04.md) — 做梦机制产生的关联洞察
```

### 每日日志格式

```markdown
# 2026-04-04 对话日志

## 09:25 身份确立 #角色 #设定
- 大人设定称呼...
- 更新SOUL.md/IDENTITY.md/USER.md

## 09:31 最高准则 #核心 #原则
- 实事求是原则写入...

## 10:04 教学幻觉 #读书 #学习
- 学习《教学幻觉》10种幻觉...

## 10:57 Claude Code架构 #架构 #学习
- 深度学习Claude Code记忆体系...
```

### 做梦记录格式

```markdown
# 2026-04-04 Dream Report

## 整合结果
- 将"教学幻觉-表现幻觉"与"AI幻觉"做了关联
- 更新了claude-code-study.md中的记忆抽取部分

## 创意碰撞 🔥
- 《教学幻觉》中的"创新幻觉"可以类比到AI领域...
- 做梦机制中的"修剪"思路可以用于信息整理...

## 修正
- 无
```
