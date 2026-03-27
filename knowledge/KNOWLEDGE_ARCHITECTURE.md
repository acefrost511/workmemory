# 知识库三层架构

> 版本：v1.0 | 制定：2026-03-27
> 维护者：小艾（总调度）

---

## 一、三层架构

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
记忆体系          情报官研究库           IP内容库
（小艾统筹）       （情报官维护）         （IP团队维护）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MEMORY.md         /knowledge/           /workspace/
memory/*.md        research_pool/        agents/edu_lead/
                                    /knowledge/beliefs/
                                    /knowledge/creative_sparks/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
陛下笔记洞察素材    中英文研究论文          13信念抽屉
  ↓存入           搜索结果（只读）        深度洞察结果
  IP素材库           ↑↓                  反哺产出品
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 二、各层详情

### 第一层：记忆体系（唯一维护者：小艾）

**目录**：`/workspace/memory/`、`/workspace/MEMORY.md`

**内容**：陛下的笔记/洞察/素材/对话记录/个人偏好/工作安排

**写入权限**：仅小艾（主session Agent）

**读取权限**：所有Agent可读（只读陛下记忆，不得写入）

---

### 第二层：统一研究库（唯一维护者：情报官）

**目录**：`/workspace/knowledge/research_pool/`

**内容**：情报官+9路子Agent搜索的所有中英文研究论文原始结果
- 每篇包含：标题/作者/机构/时间/来源/DOI/核心发现/原文链接
- 按日期目录组织：`research_pool/2026-03/YYYY-MM-DD.md`
- 主索引文件：`research_pool/MASTER_INDEX.md`（所有研究按主题分类索引）

**写入权限**：仅情报官+子Agent（其他Agent只读）

**读取权限**：所有Agent可读

---

### 第三层：IP内容库（唯一维护者：IP团队）

**目录**：`/workspace/knowledge/beliefs/`、`/workspace/knowledge/creative_sparks/`

**来源**：IP团队（edu_lead）从统一研究库读取研究，归类到13个信念抽屉，产出深度洞察

**内容**：
- 13个信念抽屉（含素材积累+碰撞产出）
- 创意火花库（每日洞察全文）
- 洞察历史索引

**写入权限**：仅edu_lead/IP团队（通过追加写入共享目录）

**读取权限**：所有Agent可读

---

### 精选资讯团队（zhubian）

**输入来源**：从统一研究库读取，定时抽取10-15篇高质量研究

**输出**：每周精选资讯速览（每周六早5点推送）

**不维护**：不维护任何库，只从研究库读取并生成速览推送

---

## 三、存储路径汇总

```
/workspace/
  memory/                    ← 记忆体系（小艾统筹）
    MEMORY.md               ← 主索引
    YYYY-MM-DD.md           ← 每日记忆
    topics/                 ← 话题细分记忆
    conversation_buffer.md   ← 对话缓冲
  
  knowledge/
    research_pool/          ← 统一研究库（情报官维护·所有Agent可读）
      2026-03/
        2026-03-27.md       ← 每日研究结果
      MASTER_INDEX.md       ← 研究主索引
    beliefs/                ← IP内容库·13信念抽屉（IP团队维护）
      信念1-AI教育观.md
      信念2-教师角色观.md
      ...（共13个）
    creative_sparks.md       ← IP内容库·每日创意火花
    collision_results_v3.md  ← IP内容库·洞察历史索引
  
  agents/
    edu_lead/               ← IP团队主页
    edu_writer/             ← IP团队·编辑
    edu_reviewer/           ← IP团队·审核
    reader_*/               ← IP团队·多视角审核
    zhubian/                ← 精选资讯团队主页
    info_officer/           ← 情报官主页
```

---

## 四、陛下笔记/洞察/素材处理流程

1. 陛下发送笔记/洞察/素材 → 小艾接收
2. 小艾存入IP团队素材库：`/workspace/knowledge/beliefs/暂存素材.md`
3. 小艾判断归属哪个信念抽屉 → 归类追加
4. 若无法归类 → 存入暂存区（staging_area.md）→ 定期整理
5. 更新记忆体系（MEMORY.md + memory/）

---

## 五、维护规则

| 层级 | 维护者 | 可写Agent | 可读Agent |
|------|--------|---------|---------|
| 记忆体系 | 小艾 | 仅小艾 | 所有（只读） |
| 统一研究库 | 情报官+子Agent | 仅情报官系 | 所有（只读） |
| IP内容库 | edu_lead/IP团队 | edu_lead系 | 所有（只读） |

**禁止行为**：
- ❌ 非授权Agent写入任何知识库
- ❌ 精选资讯团队维护自己的研究库
- ❌ IP团队修改统一研究库已有内容
- ❌ 任何Agent删除陛下的记忆文件
