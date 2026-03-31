# 情报官团队 SOP（标准操作手册）
> 版本：1.0 | 日期：2026-03-29 | 依据：task-config.md + 实测intel_01成功经验

## 核心定位

情报官（info_officer）= 协调员，不自己做搜索
intel_01~12 = 执行搜索的12个专业Agent
intel_reviewer_* = 审核员

---

## 团队成员及职责

| Agent ID | 职责领域 | SOUL路径 |
|----------|---------|---------|
| info_officer | 总协调，汇总，分配 | /workspace/agents/info_officer/SOUL.md |
| intel_01 | 英文期刊·Computers & Education | /workspace/agents/intel_01/SOUL.md |
| intel_02 | 英文期刊·BJET等 | /workspace/agents/intel_02/SOUL.md |
| intel_03 | 英文期刊·其他 | /workspace/agents/intel_03/SOUL.md |
| intel_04 | 中文期刊·核心 | /workspace/agents/intel_04/SOUL.md |
| intel_05 | 中文期刊·其他 | /workspace/agents/intel_05/SOUL.md |
| intel_06 | 中文期刊·综合 | /workspace/agents/intel_06/SOUL.md |
| intel_07 | AI教育新产品（国外） | /workspace/agents/intel_07/SOUL.md |
| intel_08 | 国际报告（UNESCO/OECD等） | /workspace/agents/intel_08/SOUL.md |
| intel_09 | 中国政策 | /workspace/agents/intel_09/SOUL.md |
| intel_10 | 行业动态 | /workspace/agents/intel_10/SOUL.md |
| intel_11 | 补充搜索 | /workspace/agents/intel_11/SOUL.md |
| intel_12 | 补充搜索 | /workspace/agents/intel_12/SOUL.md |
| intel_reviewer_en | 英文论文审核 | /workspace/agents/intel_reviewer_en/SOUL.md |
| intel_reviewer_cn | 中文论文审核 | /workspace/agents/intel_reviewer_cn/SOUL.md |
| intel_reviewer_intl | 国际报告审核 | /workspace/agents/intel_reviewer_intl/SOUL.md |

---

## 标准化Spawn流程

**每次spawn intel_XX，必须执行以下步骤：**

```
步骤1：读取 SOUL.md 内容
       命令：read /workspace/agents/intel_XX/SOUL.md

步骤2：拼接任务
       模板：
       "【角色设定 - 请严格遵循】
       $(SOUL.md内容)

       【本次任务】
       {具体任务描述}

       【输出要求】
       搜索结果写入 /workspace/knowledge/原文库/{DOI}.md
       每篇格式：标题/作者/期刊/时间/DOI/核心发现/原文链接
       完成后报告：搜到X篇，写入X篇，列表（DOI+标题）"

步骤3：spawn
       sessions_spawn(
         runtime="subagent",
         agentId="intel_XX",
         task="{步骤2的结果}",
         runTimeoutSeconds=300,
         mode="run"
       )
```

---

## 搜索时间范围规则

| 报告类型 | 时间范围 | 硬性规定 |
|---------|---------|---------|
| 日报 | 近24小时 | 超出全部排除 |
| 周报 | 近7天 | 超出全部排除 |
| 临时搜索 | 按具体要求 | 按具体要求 |

---

## 并发规则

**每次最多并行3个Agent，超出必须分批。**

```
第一批（并行3个）：intel_01 + intel_04 + intel_07
第二批（并行3个）：intel_02 + intel_05 + intel_08
第三批（并行3个）：intel_03 + intel_06 + intel_09
第四批（并行3个）：intel_10 + intel_11 + intel_12
```

**每批完成后：**
- 等待全部3个返回（或超时）
- 处理返回结果
- 再启动下一批

---

## 超时处理

| Agent | 超时时间 | 超时处理 |
|-------|---------|---------|
| intel_01~12 | 5分钟 | 等30秒→重试1次→失败则记录"超时未完成" |
| intel_reviewer_* | 3分钟 | 记录原始输出，标记"未完成审核" |

**超时重试不超过2次。**

---

## 情报官日报标准流程（每日执行）

```
T+0:00  情报官接收任务（cron触发或陛下指令）
T+0:01  spawn intel_01, intel_04, intel_07（第一批）
T+5:00  第一批完成，spawn intel_02, intel_05, intel_08（第二批）
T+10:00 第二批完成，spawn intel_03, intel_06, intel_09（第三批）
T+15:00 第三批完成，spawn intel_10, intel_11, intel_12（第四批）
T+20:00 第四批完成，读取所有写入的原文库文件
T+21:00 生成审核列表（去重+质量过滤）
T+22:00 spawn intel_reviewer_* 审核
T+23:00 审核完成，汇总推送飞书
```

---

## 质量控制规则

1. **DOI必须验证**：找到论文后访问 doi.org 确认有效
2. **K12硬边界**：研究对象必须是K12阶段（非K12全部排除）
3. **时效性硬门槛**：超出时间范围全部排除
4. **去重**：标题相似度>85%只保留一篇

---

## 输出文件规范

写入 `/workspace/knowledge/原文库/{DOI}.md`
格式：
```markdown
# 论文标题

## 基础信息
- 标题：
- 作者：
- 期刊：
- 发表时间：
- DOI：
- 原文链接：

## 核心发现
（300字以上，说清研究发现和价值）
```
