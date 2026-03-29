# IP内容团队 SOP（洞察生产标准操作手册）
> 版本：1.0 | 日期：2026-03-29 | 依据：SOUL.md体系 + 实测经验

## 核心定位

edu_lead（主编）= 任务分配中枢 + 审核把关 + 推送决策
edu_writer = 内容执笔人
reader_parent/new_teacher/senior_teacher/principal/expert = 5视角读者Panel
edu_reviewer = 终审（外交学院教授视角）

---

## 团队成员及SOUL路径

| Agent ID | 角色 | SOUL路径 |
|---------|------|---------|
| edu_lead | 主编/组长 | /workspace/agents/edu_lead/SOUL.md |
| edu_writer | 内容执笔 | /workspace/agents/edu_writer/SOUL.md |
| reader_parent | 读者Panel·家长 | /workspace/agents/reader_parent/SOUL.md |
| reader_new_teacher | 读者Panel·新教师 | /workspace/agents/reader_new_teacher/SOUL.md |
| reader_senior_teacher | 读者Panel·资深教师 | /workspace/agents/reader_senior_teacher/SOUL.md |
| reader_principal | 读者Panel·校长 | /workspace/agents/reader_principal/SOUL.md |
| reader_expert | 读者Panel·学术专家 | /workspace/agents/reader_expert/SOUL.md |
| edu_reviewer | 终审 | /workspace/agents/edu_reviewer/SOUL.md |

---

## 洞察生产标准流程（IP洞察SOP）

### 阶段1：情报输入
- 情报来源：intel团队搜索结果（原文库文件）
- 输入判断：读信念抽屉 → 判断哪些论文/产品/报告值得生产洞察

### 阶段2：洞察生成
```
主编 edu_lead 收到任务
  ↓
edu_lead spawn edu_writer（注入SOUL.md + 任务）
  ↓
edu_writer 读取原文库 + 信念抽屉
  ↓
edu_writer 生成3个候选洞察
  ↓
edu_writer 写入 /workspace/knowledge/collision_results_v2.md
```

**洞察质量标准（每条必须包含6个部分）：**
1. 信念溯源：信念编号+核心表述（必须出现）
2. Hook句（≤20字，含数字或反常识）
3. 引用证据A/B（标题+机构+≥100字通俗描述）
4. 碰撞逻辑（2-3句，说明信念如何被新证据改变）
5. 核心洞察（≥400字，含具体场景）
6. 读者带走（给老师/家长/判断标准各≥50字）

### 阶段3：4 Agent并行评分

**注意：5个读者并行，而非串行！**

```
edu_lead 并行 spawn（3个，分批）：
第一批：reader_parent + reader_new_teacher + reader_senior_teacher
第二批：reader_principal + reader_expert

每个读者评5个维度（0-10分）：
- 新颖性
- 真实性
- 可操作性
- 传播性
- 信念契合度（洞察是否在信念框架内运作）
```

### 阶段4：评分汇总
```
综合分 = 5维度均值
≥9.0 → 进入推送
<9.0 → 迭代重写（最多3轮）
3轮仍未达标 → 推送当前最高分，标注"本期最低分"
```

### 阶段5：反哺抽屉（必须执行）
```
Top洞察追加写入对应抽屉的「碰撞产出品区」
若挑战了抽屉原有结论 → 在「抽屉结论区」加修订说明
```

### 阶段6：飞书推送
```
格式：消息卡片（纯文本清单体，不用Markdown表格）
内容：Top3洞察综合评分+核心内容摘要
```

---

## Spawn模板

**edu_writer spawn 模板：**
```
步骤1：读 SOUL
       read /workspace/agents/edu_writer/SOUL.md

步骤2：拼接
       "【角色设定 - 请严格遵循】
       $(edu_writer的SOUL.md内容)

       【本次任务】
       读取以下文件获取原材料：
       - /workspace/knowledge/原文库/（最新论文）
       - /workspace/knowledge/belief_drawers.md（信念抽屉）

       任务：生成3个K12 AI教育洞察
       主题：[具体主题描述]

       【输出要求】
       写入 /workspace/knowledge/collision_results_v2.md
       格式必须包含6个部分（见SOUL.md）
       每条洞察≥400字"

步骤3：spawn
       sessions_spawn(
         runtime="subagent",
         agentId="edu_writer",
         task="{步骤2结果}",
         runTimeoutSeconds=600,
         mode="run"
       )
```

**reader_* 并行 spawn 模板（5个同时）：**
```
步骤1：读对应SOUL（如 reader_parent 的 SOUL.md）

步骤2：拼接
       "【角色设定 - 请严格遵循】
       $(reader_xxx的SOUL.md内容)

       【评分对象】
       文件：/workspace/knowledge/collision_results_v2.md

       【任务】
       阅读该文件中的洞察，对每个洞察从以下5维度评分（0-10分）：
       1. 新颖性：是否提供了新认知？
       2. 真实性：证据是否可靠？
       3. 可操作性：读者能否落地？
       4. 传播性：是否有传播潜力？
       5. 信念契合度：是否在信念框架内？

       【输出格式】
       对每个洞察评分并写出理由（每条≥50字）
       最终输出：综合分（5维度均值）

       【输出文件】
       /workspace/knowledge/scores/reader_xxx_scores.md"

步骤3：并行spawn（5个同时）
       sessions_spawn(runtime="subagent", agentId="reader_parent", ...)
       sessions_spawn(runtime="subagent", agentId="reader_new_teacher", ...)
       sessions_spawn(runtime="subagent", agentId="reader_senior_teacher", ...)
       sessions_spawn(runtime="subagent", agentId="reader_principal", ...)
       sessions_spawn(runtime="subagent", agentId="reader_expert", ...)
```

---

## 质量红线

1. **不得跳过"信念溯源"步骤**
2. **不得只写"研究A×研究B"，不写信念如何被改变**
3. **不得在分数低于9.0时强行推送**
4. **不得只推1个或2个洞察（必须Top3）**
5. **不得跳过反哺抽屉步骤**

---

## 超时规则

| Agent | 超时 | 处理 |
|-------|------|------|
| edu_writer | 10分钟 | 重试1次 |
| reader_*（5个并行） | 各3分钟 | 记录已评分的结果，继续汇总 |
| edu_reviewer | 5分钟 | 如超时，人工主Agent做终审 |

---

## 输出文件清单

| 文件 | 负责Agent |
|------|---------|
| /workspace/knowledge/collision_results_v2.md | edu_writer |
| /workspace/knowledge/scores/reader_parent_scores.md | reader_parent |
| /workspace/knowledge/scores/reader_new_teacher_scores.md | reader_new_teacher |
| /workspace/knowledge/scores/reader_senior_teacher_scores.md | reader_senior_teacher |
| /workspace/knowledge/scores/reader_principal_scores.md | reader_principal |
| /workspace/knowledge/scores/reader_expert_scores.md | reader_expert |
| /workspace/knowledge/scores/SUMMARY.md | edu_lead（汇总） |
