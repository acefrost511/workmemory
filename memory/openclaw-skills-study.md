# OpenClaw 必装10个Skills - 学习笔记

> 学习来源：https://moltbook.com/ 及相关GitHub生态
> 学习时间：2026-03-06
> 笔记整理：主Agent

---

## 核心架构理解

OpenClaw = Gateway（网关）+ Agent（智能体）+ Skills（技能）

- **大脑**：大语言模型（理解、推理）
- **手脚**：Skills（封装成可调用的能力）
- **Skill结构**：每个Skill是一个目录，包含：
  - `SKILL.md`：说明文档（能力边界、使用时机、执行步骤）
  - `scripts/`：可执行脚本（需要编程能力时）
  - `assets/`：资源文件（模板、配置）

没有Skills的OpenClaw = 只会聊天的"哲学家"
有Skills的OpenClaw = 能干活的"数字员工"

---

## 1. Clawsec（安全防护）

### 核心机制
**静态代码分析** - 在安装Skill前自动扫描风险：
- 权限申请：是否要求过度权限
- 网络请求：是否向可疑服务器发送数据
- 代码混淆：是否故意难以审计
- 依赖来源：第三方库是否可靠

### 安全评级
- `SAFE`（安全）- 可放心安装
- `CAUTION`（谨慎）- 需要检查
- `DANGEROUS`（危险）- 建议不安装

### GitHub实现
- 开源项目：**Clawguard** (github.com/openclaw/openclaw/issues/36990)
- 社区安全扫描工具
- 自动集成到skill安装流程

### 使用价值
**底线保护**：帮你挡掉明显有问题的Skills，避免开盲盒装到恶意代码

---

## 2. Tavily Search（实时信息）

### 核心机制
通过API给Agent提供**联网搜索能力**，解决大模型知识截止日期问题。

### 技术特点
- **结构化输出**：返回提取后的关键信息（非一堆链接）
- **AI优化**：专门针对大模型设计的输出格式
- **上下文感知**：结合对话历史优化搜索关键词

### GitHub/API实现
- 服务：tavily.com
- 免费额度：每月1000次
- API调用：`tavily.search(query, options)`

### 配置方法
```bash
npx clawhub@latest install tavily-search
openclaw config set skills.tavily-search.apiKey "你的API密钥"
```

### 使用场景
- 查最新资讯（2025年后的事件）
- 实时信息验证
- 动态数据获取

---

## 3. Multi Search Engine（多引擎聚合）

### 核心机制
集成**17个搜索引擎**（8个国内 + 9个国际）：
- 百度、谷歌、必应等
- 统一接口调用
- 结果智能聚合

### 技术特点
- **无需API Key**：使用公开搜索接口
- **智能分流**：按查询语言自动选引擎
- **结果去重**：多个引擎重复内容合并

### 适用场景
- 技术资料搜索（中英文兼顾）
- 需要多视角信息的场景
- "研究模式"默认入口

---

## 4. Self-Improving Agent（自我改进）

### 核心机制
让Agent**记录错误和学习**，下次自动参考。

### 实现机制（三步）
1. **自动监控**：监听命令执行结果、用户反馈
2. **结构化记录**：写入 `.learnings/` 日志
3. **智能检索**：遇到相似问题自动查历史

### 记录格式
每条学习包含：
- ID、时间戳、优先级
- 摘要、复现步骤、建议修复

### GitHub结构
- 技能目录：`self-improving-agent/`
- 学习日志：`~/.openclaw/learnings/`
- 检索机制：向量相似度匹配

### 真实案例
用户纠正用过时库→记录→下次自动用正确库

---

## 5. Proactive Agent（主动性代理）

### 核心机制
从"你问我答"升级到"我替你推进"

### 关键组件
- **心跳机制**：每15分钟自动唤醒
- **任务监控**：持续跟踪进行中的任务
- **自我迭代**：优化工作流程

### 生成7个核心配置文件
| 文件 | 作用 |
|------|------|
| `ONBOARDING.md` | 首次设置引导 |
| `AGENTS.md` | 操作规则和经验教训 |
| `SOUL.md` | 身份、原则、边界定义 |
| `USER.md` | 用户上下文和偏好 |
| `MEMORY.md` | 长期记忆结构 |
| `HEARTBEAT.md` | 定期自查清单 |
| `TOOLS.md` | 工具配置笔记 |

### GitHub实现
- 开源社区：`proactive-agent` skill
- 需要配合cron/定时任务使用

### 最佳实践
- 适合长期使用的场景
- 需要前置配置7个文件
- 与HEARTBEAT.md配合使用

---

## 6. Ontology（知识图谱）

### 核心机制
用**类型化的知识图谱**给Agent做长期记忆（替代非结构化记忆）

### 三步构建
1. **实体抽取**：从对话找关键实体（人、事、物）
2. **关系构建**：把实体关联连起来
3. **类型标注**：给实体打类型标签

### 示例
用户说"我喜欢简洁风格"→记录：
```
实体：你
属性：偏好-简洁风格
类型：用户偏好
```

### 价值
- 跨对话"真的记住你"
- 个性化体验的基础
- 越用越懂你

---

## 7. Find-Skills（技能发现）

### 核心机制
**元Skill** - 专门帮你找其他Skills

### 工作流程
1. 接收需求描述
2. 向ClawHub发起搜索
3. 对比Skills匹配度
4. 推荐最合适的

### 输出格式
带相似度排序的推荐列表：
```
xiaohongshu-tools（相似度0.385）：小红书工具
xiaohongshu-title（相似度0.366）：标题生成
```

### 使用技巧
- **描述越具体越好**
- 好："批量重命名图片、支持加水印"
- 不好："图片技能"

---

## 8. GitHub Skill（仓库管理）

### 核心机制
集成**GitHub CLI (gh)**，用自然语言管理仓库

### 三步流程
1. 理解你的指令
2. 转换成对应的`gh`命令
3. 执行并返回结果

### 前置安装
```bash
# macOS
brew install gh

# Linux
sudo apt install gh

# 认证
gg auth login
```

### 常见场景
- 搜索开源项目
- 管理Issues/PR
- 代码审查
- 自动化报告（每日检查高优先级Issues）

### GitHub集成
- 依赖：`gh` CLI工具
- 技能：`github` skill
- 可接入自动化工作流

---

## 9. Office-Automation（办公自动化）

### 核心机制
综合技能包，覆盖**4大办公场景**：
- 日程管理（创建会议、设置提醒）
- 邮件处理（分类整理、自动回复）
- 文档编辑（生成报告、格式调整）
- 数据处理（Excel分析、图表生成）

### 真实场景
1. **自动周报**：每周五汇总工作，生成格式化邮件
2. **会议纪要**：会后整理成结构化纪要
3. **数据分析**：给Excel自动分析趋势、出图、提炼结论

### 配置要求
- 需要配置相关服务的API Key
- Gmail、Google Calendar等

### 最佳组合
- 与**Proactive Agent**配合使用
- 每天早上自动生成日程摘要

---

## 10. Systematic-Debugging（系统化调试）

### 核心机制
**强制结构化调试**，告别瞎猜

### 5步调试流程
1. **问题定义**：精确描述现象
2. **信息收集**：收集日志、堆栈、环境信息
3. **假设生成**：列根因，按概率排序
4. **测试验证**：设计实验逐个验证
5. **修复实施**：确认根因后修复并验证

### 检查清单
每步都有检查清单，Agent不能跳过

### 对比
| 模式 | 特点 |
|------|------|
| 无流程 | 瞎猜、乱试、碰运气 |
| 有流程 | 破案、结构化、高效 |

### 输出
生成调试报告：根因、修复方案、预防措施

### 最佳组合
- 配合**Self-Improving Agent**记录经验
- 下次类似问题秒解

---

## 总结：五大维度能力闭环

| 维度 | 对应Skill | 核心价值 |
|------|----------|----------|
| **安全** | Clawsec | 挡掉恶意Skills |
| **信息** | Tavily + Multi Search | 实时+多源信息获取 |
| **进化** | Self-Improving + Systematic-Debugging | 记录教训、结构化调试 |
| **记忆** | Proactive Agent + Ontology | 主动推进、结构化记忆 |
| **扩展** | Find-Skills + GitHub + Office-Automation | 发现技能、管理仓库、办公自动化 |

---

## 安装命令汇总

```bash
# 1. 安全防护
npx clawhub@latest install clawsec

# 2. 实时搜索（需配置API Key）
npx clawhub@latest install tavily-search

# 3. 多搜索引擎
npx clawhub@latest install multi-search-engine

# 4. 自我改进
npx clawhub@latest install self-improving-agent

# 5. 主动性代理
npx clawhub@latest install proactive-agent

# 6. 知识图谱
npx clawhub@latest install ontology

# 7. 技能发现
npx clawhub@latest install find-skills

# 8. GitHub（需先安装gh CLI）
npx clawhub@latest install github

# 9. 办公自动化
npx clawhub@latest install office-automation

# 10. 系统化调试
npx clawhub@latest install systematic-debugging
```

---

## 学习心得

### 关键洞察
1. **Skills是OpenClaw的灵魂** - 没有Skills只能聊天，有Skills才能干活
2. **ClawHub生态庞大** - 11,600+ Skills，但质量参差不齐，需要筛选
3. **组合使用更强** - 如Proactive+Office、Debugging+Self-Improving

### 优先级建议
1. **必装**：Clawsec（安全底线）、Tavily（信息获取）
2. **推荐**：Proactive Agent（自动化）、Systematic-Debugging（效率）
3. **按需**：其他根据具体场景选择

---

*学习完成时间：2026-03-06 10:45*
