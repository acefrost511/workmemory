# 共享知识库读取机制

> 所有Agent必须遵守此机制
> 版本：v1.0 | 制定：2026-03-27

---

## 一、共享知识库目录（只读）

以下目录和文件对所有Agent**开放读取**，但**非授权Agent不得写入**：

```
/workspace/knowledge/
  beliefs/                    ← 13个信念抽屉，所有Agent可读
    信念1-AI教育观.md
    信念2-教师角色观.md
    ...（共13个）
  research_cache/             ← 高质量研究原文库，所有Agent可读
    研究素材完整库.md
  creative_sparks.md           ← 创意火花库，所有Agent可读
  daily_intel_*.md            ← 日报资讯库，所有Agent可读
  staging_area.md             ← 暂存区，所有Agent可读
  ALL_BELIEFS_CONTENT.md     ← 全部信念汇总，所有Agent可读

/workspace/memory/           ← 记忆文件，所有Agent可读
  MEMORY.md
  topics/education.md
  topics/other.md
  conversation_buffer.md
```

---

## 二、各Agent读取权限

### zhubian（日报周报主编）·只读共享层
- 读取：beliefs/、research_cache/、daily_intel_*、memory/
- 写入：/workspace/agents/zhubian/（私有目录）
- 职责：每周六早5点推送精选资讯速览

### edu_lead（深度内容主编）·读写共享层
- 读取：beliefs/、research_cache/、creative_sparks/、daily_intel_*、memory/
- 写入：beliefs/（碰撞产出品追加区）、creative_sparks.md、collision_results_v3.md
- 职责：统筹深度洞察生产（每日17:30）和深度文章创作

### edu_writer（教育编辑）
- 读取：beliefs/、research_cache/、creative_sparks/、memory/
- 写入：/workspace/agents/edu_writer/（私有目录）
- 职责：撰写深度洞察和深度文章

### edu_reviewer（教育审核）+ reader_*（4个视角审核Agent）
- 读取：beliefs/、creative_sparks/、待审核文章
- 写入：/workspace/agents/reader_*/（私有审核结果）
- 职责：多视角终审

### info_officer（情报官）
- 读取：beliefs/、memory/
- 写入：master文档、beliefs/（素材追加）、research_cache/
- 职责：每日增量检索，充实抽屉

---

## 三、读取规则（铁律）

**禁止行为**
- ❌ 非授权Agent直接写入共享目录（只能用append追加）
- ❌ 直接修改其他Agent创建的共享文件
- ❌ 删除他人创建的共享文件

**追加写入规则（适用于共享目录）**
- 情报官追加 → beliefs/素材积累区 / research_cache/
- edu_lead追加 → beliefs/碰撞产出品区 / creative_sparks.md
- 所有Agent → collision_results_v3.md（元信息追加）

**读取优先级**
当需要创作素材时，优先从共享知识库读取已有材料：
1. 先查 creative_sparks.md（已有洞察）
2. 再查 beliefs/相关抽屉（已有研究）
3. 再查 research_cache/（完整研究）
4. 最后考虑独立检索

---

## 四、共享知识库文件结构说明

| 文件 | 内容 | 创建者 | 更新频率 |
|------|------|--------|---------|
| 信念抽屉（13个） | 核心信念+素材+碰撞产出 | 情报官+edu_lead | 每日增量 |
| 研究素材完整库.md | 所有研究原文摘要 | 情报官 | 每日增量 |
| creative_sparks.md | 每日创意火花洞察 | edu_lead | 每日17:30 |
| collision_results_v3.md | 洞察历史索引 | edu_lead | 每日17:30 |
| daily_intel_YYYY-MM-DD.md | 当日资讯清单 | 情报官 | 每日5:00 |
| staging_area.md | 待归类素材暂存 | 情报官 | 按需 |
| ALL_BELIEFS_CONTENT.md | 13抽屉全文汇总 | edu_lead | 每周六 |
