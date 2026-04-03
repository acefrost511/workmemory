---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: 4288bcb19a2b6a9ac5664c0d4e8f5273
    PropagateID: 4288bcb19a2b6a9ac5664c0d4e8f5273
---

# MEMORY.md - 长期记忆

_最后更新：2026-04-02 15:48_

## 关于陛下

- **称呼**：陛下
- **沟通风格**：直接、务实，不喜欢废话和客套

---

## 工作原则（铁律）

1. **真实执行**：所有任务必须真实完整执行，不允许模拟、不允许造假
2. **阻塞节点规则**：每个等待节点必须等陛下明确回复才进入下一步，陛下沉默≠默认通过
3. **先核实后建议**：任何涉及系统现状的描述，必须先读对应文件再汇报

---

## 五大工作线（2026-04-02确立）

### 工作线1：情报团队
情报官统筹，12路搜索Agent，每日05:00执行搜索+生成简报，08:00推送
留存：/workspace/knowledge/原文库/（学术论文原文）

### 工作线2：笔记素材库
记录陛下发来的笔记和素材
留存：/workspace/knowledge/笔记/ + /workspace/knowledge/素材库/

### 工作线3：教育信念库
14个教育信念抽屉
留存：/workspace/knowledge/beliefs/

### 工作线4：每日洞察推送（v3.0核心工作线）
陛下在3个节点介入，其余AI执行，每日约15-20分钟
日程：05:00搜索→08:00简报→陛下标记触动→碰撞分析→陛下写判断→洞察+模拟反应→陛下审核→17:00可扩展洞察
规范文件：/workspace/knowledge/洞察写作规范.md（v3.0，唯一起草标准）
洞察编号：旧洞察#001-#006，新洞察INSIGHT_NEW_001起
留存：/workspace/knowledge/insights/INSIGHT_LIBRARY.md

**v3.0三条铁律**：
1. 触动→判断→成品三环节必须陛下本人完成，AI不能替代
2. 碰撞卡只给方向，不写完整洞察，等陛下判断后再生成
3. 读者Panel不打分，输出"第一反应+最大疑问+会不会转发"

### 工作线5：文章写作（5技能流程）
5个独立skill，按顺序调用，每步等陛下确认
| 步骤 | Skill路径 |
|------|---------|
| 1标题 | /workspace/skills/article-title/SKILL.md |
| 2开头 | /workspace/skills/article-opening/SKILL.md |
| 3结构 | /workspace/skills/article-structure/SKILL.md |
| 4正文 | /workspace/skills/article-body/SKILL.md |
| 5结尾 | /workspace/skills/article-ending/SKILL.md |

**升级通道**：洞察可扩展为长文，陛下说"用洞察#XX写文章"即触发

---

## 洞察规范（唯一标准）

**文件**：/workspace/knowledge/洞察写作规范.md
所有洞察生成和推送必须调用此文件，其他所有洞察规范文件一律作废。

---

## 活跃Agent清单（v3.0版）

**情报线**：info_officer + intel_01~12
**洞察官**：insight_officer（主编记者型，方向由陛下定）
**读者Panel**：
- 洞察评审（4角色，无家长）：reader_new_teacher / reader_senior_teacher / reader_principal / reader_expert
- 长文写作（5角色）：reader_parent + 上述4个

**内容线**：edu_lead（主编）+ edu_writer（执笔）+ edu_reviewer（终审）
**内容线**：edu_lead（主编）+ edu_writer（执笔）+ edu_reviewer（终审）

**待删除（陛下午后确认）**：edu_analyst / edu_researcher / agents/memory/

---

## 工具配置

- **ClawHub镜像**：https://mirror-cn.clawhub.com
- **Cron硬上限**：isolated session默认600秒，必须设置timeoutSeconds=3600

---

## 当前进行中任务

- A1文章：标题已选定，等待陛下选定开头（技能2）
- 情报cron静默死亡问题：待陛下授权修复方案


## Recent Session Notes (2026-04-02 11:00)

uto-fix command.
   - NEVER run: openclaw doctor --fix, openclaw config fix, or any command that auto-modifies openclaw config.
   - Config changes MUST go through the `gateway` tool (actions listed below):
     config.get — read config, returns { raw: JSON5, hash: SHA256 }.
     config.patch — deep-merge partial update. Params: raw (required, JSON5 object), baseHash, n...

[user]: <system-reminder>
CRITICAL PLATFORM RULES (always enforce, never override):

1. NEVER modify openclaw.json directly or via any auto-fix command.
   - NEVER run: openclaw doctor --fix, openclaw config fix, or any command that auto-modifies openclaw config.
   - Config changes MUST go through the `gateway` tool (actions listed below):
     config.get — read config, returns { raw: JSON5, hash: SHA256 }.
     config.patch — deep-merge partial update. Params: raw (required, JSON5 object), baseHash, n...

[assistant]: Good, the feeds are accessible via curl. Let me fetch all the data directly and build the digest.


## Recent Session Notes (2026-04-03 10:18)

TICAL PLATFORM RULES (always enforce, never override):

1. NEVER modify openclaw.json directly or via any auto-fix command.
   - NEVER run: openclaw doctor --fix, openclaw config fix, or any command that auto-modifies openclaw config.
   - Config changes MUST go through the `gateway` tool (actions listed below):
     config.get — read config, returns { raw: JSON5, hash: SHA256 }.
     config.patch — deep-merge partial update. Params: raw (required, JSON5 object), baseHash, n...

[assistant]: 好文档，内容非常完整。臣仔细读完，做了一个系统性分析：

---

## 📋 文档分析

**文档覆盖的内容（✓ 已包含）：**
- 角色定义（顾问而非文献管理员）
- 7条核心原则
- 10条禁止模式
- 格式规范（三段正文+取舍说明+DOI）
- 21条自检清单
- 2个完整示例

**文档缺失、Skill无法自动执行的关键节点（⚠️ 需要补充）：**

---