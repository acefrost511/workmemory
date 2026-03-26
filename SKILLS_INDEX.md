# 📚 技能索引与触发机制指南

## 技能触发机制原理

### 核心触发机制：description + triggers

技能通过 **YAML frontmatter** 中的两个关键字段来触发：

```yaml
---
name: skill-name
description: "这里描述技能做什么，以及**何时使用**。这是主要的触发机制！"
triggers:
  - "关键词1"
  - "关键词2"
  - "英文关键词"
---
```

### 触发优先级

1. **description（最重要）** - 描述技能的功能+触发场景
2. **triggers（关键词列表）** - 精确的触发关键词
3. **name（技能名称）** - 最后备选

---

## 🎯 如何确保正确触发技能

### 技能设计最佳实践

#### ✅ 好的 description 示例
```yaml
description: "教育专家角色技能，提供教育学专业知识和建议。当用户询问课程设计、教学方法、班级管理、教育心理学等专业教育问题时使用。触发场景：用户说'请教一个教育问题'、'从教育学角度看'、'专家建议'。"
```

#### ❌ 不好的 description 示例
```yaml
description: "教育专家技能"  # 太简单，没有说明何时使用
```

---

## 📊 技能分类索引

### 1. 教育技能组（12个）

| 技能名称 | 触发关键词 | 主要功能 |
|---------|-----------|---------|
| **edu-editor** | 深度解读、长文创作、公众号文章、教育解读、教育评论、二次创作 | 教育领域深度内容编辑 |
| **edu-article-coauthoring** | 写文章、教学心得、课堂案例、教学反思、学科分析、educational articles | K12教育文章协作写作 |
| **education-expert** | 教育专家、课程设计、教学方法、教育心理学、班级管理、教研指导、教育咨询 | 教育学专业咨询 |
| **education-learning** | 教育动画、教学动画、概念可视化、知识图解、动画讲解、可视化教学 | 教育动画原理应用 |
| **education-tutor** | 辅导老师、作业答疑、学习指导、学科辅导、错题分析、家教、一对一辅导、tutor | 私人辅导老师 |
| **educational-video-creator** | 教育视频、教学视频、视频课件、在线课程、录课指导、视频脚本 | 教育视频创作工具 |
| **new-teacher-reader** | 新手教师、新教师视角、教龄1-3年 | 新手教师读者Agent |
| **senior-teacher-reader** | 资深教师、骨干教师、教龄10年以上 | 资深教师读者Agent |
| **critical-reader** | 挑刺、逻辑漏洞、论据不足、表述含糊 | 挑刺型读者Agent |
| **k12-edu-news-writer** | 教育资讯、K12资讯、AI教育、教育新闻 | K12 AI教育资讯速览 |
| **education-tutor** | 辅导老师、作业答疑、学习指导、学科辅导 | 学科辅导与答疑 |

---

### 2. 内容创作技能组（8个）

| 技能名称 | 触发关键词 | 主要功能 |
|---------|-----------|---------|
| **ai-style-remover** | AI文风、祛除AI痕迹、自然流畅、口语化、专业化 | 识别并祛除AI生成文本痕迹 |
| **md2wechat** | 公众号排版html、公众号排版、md转公众号、生成公众号版、微信html、手机预览、公众号编辑器 | Markdown转微信公众号HTML |
| **docx** | Word文档、.docx、创建Word、编辑Word、读取Word | Word文档处理 |
| **xlsx** | Excel、电子表格、.xlsx、.csv、数据分析、公式 | 电子表格处理 |
| **pptx** | PowerPoint、演示文稿、.pptx、创建幻灯片 | PowerPoint演示文稿处理 |
| **pdf** | PDF、pdf文档、提取文本、创建PDF、合并PDF | PDF文档处理 |
| **best-minds** | 最强大脑、顶级专家、世界级、best minds、谁最懂这个 | 模拟器思维 |
| **web_search** | 搜索、web search、search the web、网络搜索 | 网络搜索（SearXNG） |

---

### 3. 设计与前端技能组（6个）

| 技能名称 | 触发关键词 | 主要功能 |
|---------|-----------|---------|
| **frontend-design** | 前端设计、React、Tailwind、UI设计、网页设计、避免AI美学 | 前端设计（Anthropic官方） |
| **ui-ux-pro-max** | UI/UX、专业设计、设计系统、UI风格、配色方案 | 专业UI/UX设计 |
| **image-generate** | 生成图片、画图、图像生成、image generation | 图片生成工具 |
| **video-generate** | 生成视频、视频生成、video generation | 视频生成工具 |
| **obsidian-markdown** | Obsidian、双向链接、Mermaid图表、嵌入 | Obsidian风格Markdown |

---

### 4. 开发工具技能组（10个）

| 技能名称 | 触发关键词 | 主要功能 |
|---------|-----------|---------|
| **skill-creator** | 创建技能、技能开发、create a skill、improve a skill、test a skill、benchmark | 技能创建元技能 |
| **find-skills** | search for、search web、find information、look up、find a skill、is there a skill、can you do、npx skills | 技能发现工具（Vercel） |
| **best-minds** | 最强大脑、顶级专家、世界级、best minds、谁最懂这个 | 模拟器思维 |
| **planning-with-files** | 任务规划、复杂任务、plan out、break down、organize | Manus风格文件规划 |
| **superpowers** | 超级能力、superpowers、软件开发、编程代理 | AI编程代理完整工作流 |
| **github** | GitHub、gh issue、gh pr、gh run、gh api | GitHub CLI工具 |
| **self-improving-agent** | 自我改进、持续改进、记录错误、captures learnings | 自我改进Agent |
| **ljg-paper** | 读论文、分析论文、paper、arxiv | 论文阅读与分析 |
| **veadk-skills** | VeADK、VeADK技能、Agents转换 | VeADK技能集合 |
| **veadk-go-skills** | VeADK-Go、Go Agent、Enio Agent | VeADK-Go技能集合 |

---

### 5. 数据与分析技能组（3个）

| 技能名称 | 触发关键词 | 主要功能 |
|---------|-----------|---------|
| **data-analyst** | 数据可视化、报告生成、SQL查询、电子表格自动化、数据分析 | 数据分析师 |
| **planning-with-files** | 任务规划、复杂任务、plan out、break down、organize | Manus风格文件规划 |

---

### 6. 配置与系统技能组（6个）

| 技能名称 | 触发关键词 | 主要功能 |
|---------|-----------|---------|
| **configure_channel** | 修改消息通道、切换消息通道、dingtalk、feishu、channel配置 | 消息通道配置 |
| **configure_model** | 修改模型配置、切换模型、更新API Key、model配置 | 模型配置修改 |
| **message_channel_mod** | 修改消息通道、channel_appId、channel_appSecret | 消息通道配置（旧版） |
| **mount-tos** | 挂载TOS、火山引擎、对象存储、s3fs、挂载网盘 | TOS对象存储挂载 |
| **workspace-netdrive** | 工作区网盘、检查挂载、持久化存储、netdrive | 工作区网盘管理 |

---

### 7. 专业阅读技能组（3个）

| 技能名称 | 触发关键词 | 主要功能 |
|---------|-----------|---------|
| **critical-reader** | 挑刺、逻辑漏洞、论据不足、表述含糊 | 挑刺型读者Agent |
| **new-teacher-reader** | 新手教师、新教师视角、教龄1-3年 | 新手教师读者Agent |
| **senior-teacher-reader** | 资深教师、骨干教师、教龄10年以上 | 资深教师读者Agent |

---

### 8. 其他技能组（6个）

| 技能名称 | 触发关键词 | 主要功能 |
|---------|-----------|---------|
| **notion** | Notion、notion page、notion database、notion blocks | Notion API工具 |
| **slack** | Slack、slack reaction、slack pin、slack channel | Slack控制工具 |
| **bluebubbles** | BlueBubbles、iMessage、外部通道、channel plugin | BlueBubbles通道插件 |
| **khazix-skills** | AI技能库、skill生命周期、skill管理 | AI技能库生命周期管理 |
| **zhubian** | 内容主编、内容统筹、公众号创作团队 | 内容主编专用 |

---

### 9. 飞书扩展技能组（4个）

| 技能名称 | 触发关键词 | 主要功能 |
|---------|-----------|---------|
| **feishu-doc** | 飞书文档、飞书云文档、Feishu doc | 飞书文档读写 |
| **feishu-drive** | 飞书云盘、飞书云空间、飞书Drive | 飞书云存储管理 |
| **feishu-perm** | 飞书权限、共享权限、collaborators | 飞书文档权限管理 |
| **feishu-wiki** | 飞书知识库、飞书wiki | 飞书知识库导航 |

---

## 🎯 技能触发检查清单

### 创建新技能时检查

- [ ] **description** 包含：技能做什么 + **何时使用**
- [ ] **triggers** 包含：中文关键词 + 英文关键词
- [ ] **description** 长度：50-200字，描述清晰
- [ ] **triggers** 数量：3-10个关键词，覆盖主要触发场景

### 技能触发测试

1. **测试关键词触发**：说trigger中的某个词，看是否触发
2. **测试场景描述触发**：描述一个使用场景，看是否触发
3. **测试误触发**：说不相关的话，看是否误触发

---

## 🔧 技能问题排查

### 技能不触发？检查：

1. **description是否明确** - 有没有说"当用户...时使用"？
2. **triggers是否包含用户用词** - 用户说的词在triggers里吗？
3. **是否有冲突技能** - 多个技能都匹配时，优先选description更具体的

### 技能误触发？检查：

1. **description是否太宽泛** - 缩小范围，增加限定条件
2. **triggers是否太通用** - 使用更具体的关键词
3. **增加否定描述** - 在description中说明"不用于..."

---

## 📊 技能统计

- **总技能数**: 47个
- **教育技能**: 12个
- **内容创作**: 8个
- **设计前端**: 6个
- **开发工具**: 10个
- **数据分析**: 3个
- **配置系统**: 6个
- **专业阅读**: 3个
- **其他**: 6个
- **飞书扩展**: 4个

---

**最后更新**: 2026-03-24
**维护者**: 首席助理
