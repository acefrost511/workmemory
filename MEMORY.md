# MEMORY.md - 长期记忆索引

_最后更新：2026-04-05_
_架构：纯索引（≤200行），内容在 topics/ 文件_

---

## 不可删除的固定条目

- 【陛下】称呼"陛下"，自称"臣"，不喜欢废话和客套，直接务实
- 【时区】统一用北京时间（UTC+8），cron tz=Asia/Shanghai

---

## 工作原则（铁律）

- 真实执行，不模拟不造假
- 阻塞节点必须等陛下明确回复，沉默≠默认通过
- 先核实后建议，不凭记忆代替查文件
- 以后spawn超时统一：intel agent 600s，其他 480s
- skill的HTML是平台渲染效果，文件内容完整（2026-04-05）
- 引用模板必须先read完整内容，不能凭记忆操作（2026-04-05）
- 做完决策必须立即执行并记录，不能"记了待办就当做了"（2026-04-05）

---

## 索引（≤150字符/行）

- 【情报】情报团队12路Agent+流程 → memory/topics/情报官日报.md
- 【洞察】洞察v4.0工作线（3节点+skill） → memory/topics/洞察生产体系.md
- 【记忆】记忆系统改造（Claude Code架构） → memory/topics/记忆体系改造.md
- 【文章】文章写作5技能流程 → memory/topics/文章写作流程.md
- 【飞书】飞书文档+消息卡片配置 → memory/feishu-config.md
- 【Agents】情报官+洞察官+内容线+读者Panel → agents/info_officer/SOUL.md
- 【Skills】洞察skill/碰撞分析/简报等 → skills/collision-analysis/SKILL.md
- 【工具】ClawHub镜像/CDN/定时任务规则 → TOOLS.md
- 【规范】洞察写作唯一规范 → knowledge/洞察写作规范.md
- 【原文库】学术论文原文库（382篇+） → knowledge/原文库/
- 【信念库】14个教育信念抽屉 → knowledge/beliefs/

---

## 进行中任务（精简）

- 情报流水线v4.0已建立，今日08:00首批简报
- 洞察流程v4.0已建立，待陛下触发
- 记忆系统改造（做梦+独立抽取）2026-04-05完成部署

---

## 重大教训

- 称呼铁律：永远自称"臣"，不写"小王"/"小张"等
- skill的HTML是平台渲染效果，文件内容完整
- 引用模板必须先read完整内容，不能凭记忆操作
- 做完决策必须立即执行并记录，不能"记了待办就当做了"


## Recent Session Notes (2026-04-06 02:26)

 go through the `gateway` tool (actions listed below):
     config.get — read config, returns { raw: JSON5, hash: SHA256 }.
     config.patch — deep-merge partial update. Params: raw (required, JSON5 object), baseHash, n...

[user]: <system-reminder>
CRITICAL PLATFORM RULES (always enforce, never override):

1. NEVER modify openclaw.json directly or via any auto-fix command.
   - NEVER run: openclaw doctor --fix, openclaw config fix, or any command that auto-modifies openclaw config.
   - Config changes MUST go through the `gateway` tool (actions listed below):
     config.get — read config, returns { raw: JSON5, hash: SHA256 }.
     config.patch — deep-merge partial update. Params: raw (required, JSON5 object), baseHash, n...

[assistant]: SHA不同，执行强制推送：
推送完成（远程已是最新），更新sync记录：
✅ GitHub同步完成

- 上一轮SHA：856ae2cbd59e22969de57b6af214fbe6ea53de9c
- 本地HEAD：770b2d7a7812c9f0af954c8bc37a71477720b797
- 推送结果：Everything up-to-date（远程已是最新SHA）
- 已更新.sync_head → 770b2d7a7812c9f0af954c8bc37a71477720b797

## 工作原则补充（2026-04-06）

- 【铁律】有skill的任务，必须调用skill执行，禁止跳过skill直接手动完成任务
  - 案例：daily-briefing skill存在，臣却自己读文件写简报→违反铁律
  - 正确做法：spawn子agent + 指令"读取XX skill → 按其步骤执行"
  - skill的cron也必须更新payload为"调用skill执行"，而非重写整个流程
