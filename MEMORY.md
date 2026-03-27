# MEMORY.md - 主索引

_最后更新：2026-03-26_

> 本文件是主索引，每次启动时读取。识别话题后调取对应topics原文文件。

---

## Agent架构（最终版·2026-03-27）

- 【架构】平行双团队 | edu_lead（深度内容主编）+ zhubian（资讯快讯主编）| 共享知识库
- 【edu_lead】合并原agent_ip职能 | 深度洞察（每日17:30）+ 深度文章创作 | HKRR四要素
- 【zhubian】保留不变 | 精选资讯速览（每周六早5点）| 不碰深度内容
- 【共享知识库】/workspace/knowledge/beliefs/ + research_cache/ + creative_sparks.md | 所有Agent可读
- 【共享规则】详见 /workspace/knowledge/SHARED_KNOWLEDGE_RULES.md
- 【质量标准】/workspace/agents/edu_lead/QUALITY_STANDARD.md | 8维度打分 | 否决红线5条

## 教育内容创作

- 【方法论】HAMD创作四步法确立 | 2026-03-26 | Hook→Anchor→MindMap→Different四步创作框架 | 原文：memory/topics/education.md#HAMD
- 【方法论】HKRR定位法则 | 2026-03-26 | Happy快乐+Knowledge知识+Resonance共鸣+Rhythm节奏 | 原文：memory/topics/education.md#HKRR
- 【原则】"门优先"原则 | 2026-03-26 | 标题/封面=门，先把门做对 | 原文：memory/topics/education.md#门优先
- 【原则】差异即生存原则 | 2026-03-26 | 没有差异化就没有点击，每篇必须有"这篇的不同是什么"自检答案 | 原文：memory/topics/education.md#差异即生存
- 【原则】锚点即记忆原则 | 2026-03-26 | 没有锚点都是噪音，每篇必须有一个"读者能记住的那个瞬间" | 原文：memory/topics/education.md#锚点即记忆
- 【IP定位】K12课堂门童 | 2026-03-26 | 面向K12老师的AI课堂实用指南，专注K12老师的AI内容IP蓝海 | 原文：memory/topics/education.md#IP定位
- 【IP用户】三层目标用户 | 2026-03-26 | 核心-信息科技老师/扩量-学科老师/影响-教研员 | 原文：memory/topics/education.md#目标用户
- 【IP内容模型】三层内容结构 | 2026-03-26 | 工具实操40%+课例展示40%+认知升级20% | 原文：memory/topics/education.md#内容模型
- 【IP更新节奏】周二工具稿/周五课例稿/热点+1 | 2026-03-26 | 固定节奏建立读者预期 | 原文：memory/topics/education.md#更新节奏
- 【SOP】4阶段创作SOP | 2026-03-26 | Pre-production→Production→Post-production→Review | 原文：memory/topics/education.md#创作SOP
- 【数据追踪】article_tracker.md | 2026-03-26 | 三指标追踪（转发/点赞/爱心），每5篇做阶段性复盘 | 原文：memory/topics/education.md#数据追踪
- 【日报编号】全局顺序编号规则 | 2026-03-26 | 每日编号按顺序延续，不从1重新开始 | 原文：memory/topics/education.md#日报编号
- 【日报审核格式】7字段审核列表 | 2026-03-26 | 序号/标题/时间/简介/来源/优先级/是否深度解读 | 原文：memory/topics/education.md#日报审核格式
- 【研究领域】K12 AI教育五大关注方向 | 2026-03-05 | AI应用效果/认知影响/产品设计/中国政策/全球研究 | 原文：memory/topics/education.md#研究领域
- 【日报自动化】百晓生日报cron | 持续 | 每天05:00搜索，08:00发审核列表 | 原文：memory/topics/education.md#日报自动化
- 【记忆体系】动态标签索引架构 | 2026-03-26 | 索引驱动+实时写入+原文保留 | 原文：memory/topics/education.md#记忆体系

---

## 其他

- 【工作原则】事事有回音 | 2026-03-05 | 通知不是等待，完成后通知然后继续推进 | 原文：memory/topics/other.md#事事有回音
- 【工作原则】100%成功率 | 2026-03-06 | 所有任务必须100%成功，多重备用机制 | 原文：memory/topics/other.md#100%成功率
- 【工作原则】失败问题解决三步骤 | 2026-03-06 | 协作分析→GitHub学习→学以致用攻克 | 原文：memory/topics/other.md#失败解决
- 【陛下信息】沟通风格直接务实 | 2026-03-05 | 不喜欢废话和客套 | 原文：memory/topics/other.md#陛下信息
- 【平台】OpenClaw+飞书接入 | 2026-03-05 | 已配置飞书渠道 | 原文：memory/topics/other.md#平台
- 【多Agent系统】四层架构 | 2026-03-05 | 陛下→小艾→组长→执行agent | 原文：memory/topics/other.md#多Agent
- 【Agent】百晓生接管日报 | 持续 | Phase 2完成，05:00-08:00全自动 | 原文：memory/topics/other.md#百晓生
- 【定时任务】GitHub同步01:00 | 持续 | 每天凌晨1点同步记忆文件 | 原文：memory/topics/other.md#GitHub同步
- 【教训】2026-03-03四大教训 | 2026-03-03 | cron配置错误/内容丢失/格式精简过度/被动等待 | 原文：memory/topics/other.md#历史教训
- 【记忆体系】三层索引架构 | 2026-03-26 | daily日志→MEMORY.md索引→topics原文 | 原文：memory/topics/other.md#记忆体系
- 【团队】IP团队架构确立 | 2026-03-26 | 陛下→小艾→IP主编→创作执行，复用情报官搜索 | 原文：memory/topics/education.md#IP团队架构
- 【IP洞察】三重碰撞机制 | 2026-03-26 | 研究×信念×笔记碰撞，每日17:30产出3条创意洞察推送陛下 | 原文：memory/topics/education.md#IP洞察
- 【写作手法】7种创作手法 | 2026-03-26 | 共鸣开场/正反对比/步骤拆解/比喻落地/框架工具/理念升华/数字承诺 | 原文：knowledge/writing_sop.md#7种创作手法
- 【复盘】首篇复盘文章 | 2026-03-26 | 3步搭建AI融合课堂智能体，阅读5514/转发924/传播系数0.168爆款 | 原文：knowledge/article_tracker.md
- 【复盘洞察】实用工具手册型文章 | 2026-03-26 | 收藏率8.5%+新增关注率6.1%，核心价值是"读者来拿工具"而非受教育 | 原文：knowledge/article_tracker.md
- 【官方数据】3步搭建AI智能体完整录入 | 2026-03-26 | 收藏率8.5%+新增关注率6.1%+分享率16.6%，工具手册型文章 | 原文：knowledge/article_tracker.md
- 【13抽屉系统】信念创作体系完成 | 2026-03-26 | 13个抽屉/21篇研究/碰撞引擎/4Agent打分/原文库/结果库全部就位 | 原文：knowledge/beliefs/ + collision_results.md
- 【4Agent评分体系】每日创意碰撞 | 2026-03-26 | 新教师×成熟教师×校长×K12专家，4维度并行打分选Top3，每日17:30推送陛下 | 原文：knowledge/collision_results.md
- 【情报官新任务】抽屉充实-每天12:30 | 2026-03-26 | 13个抽屉各增量检索1-2篇最新研究，持续积累 | 原文：cron ID: 0bef52ae
- 【Cron修复】announce投递bug | 2026-03-26 | announce投递有bug导致状态failed但任务执行成功，全部改为mode=none解决 | 原文：cron list
- 【创作逻辑】视角撬动素材 | 2026-03-26 | 陛下确定：创作起点是视角，13条信念是认知框架库，创作=视角+素材碰撞 | 原文：memory/daily/2026-03-26.md
