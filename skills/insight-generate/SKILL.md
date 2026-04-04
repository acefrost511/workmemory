---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
---

# insight-generate | 洞察生成技能

## 技能概述

- **版本**：v1.0
- **创建日期**：2026-04-04
- **触发方式**：主session检测到陛下「判断完毕」后调用
- **输入**：陛下的判断（碰撞卡编号+所选方向+判断原话）
- **输出**：7部分完整洞察 + 4角色读者模拟反应 → 飞书推送陛下
- **下游衔接**：陛下审核后写入INSIGHT_LIBRARY.md并反哺信念抽屉

---

## 执行流程

### Step 1：读取上下文

1. 读取 `/workspace/knowledge/素材库/MAT_YYYYMMDD_XX.md`（触动原文）
2. 读取 `/workspace/knowledge/洞察写作规范.md`（参考格式）
3. 读取对应信念抽屉（核心表述+金句+素材积累区）
4. 提取陛下判断原话（一字不改）

---

### Step 2：生成洞察（7个部分）

```markdown
# 洞察 · INSIGHT_NEW_XXX

- 批次：YYYY-MM-DD
- 触动来源：MAT_YYYYMMDD_XX
- 碰撞卡：碰撞卡 #XX

---

## 1. 信念溯源
扎根于哪个信念抽屉？引用抽屉中的哪个核心表述？

## 2. Hook句
≤20字，含数字或反常识。读者看完必须想知道"为什么"或"凭什么这么说"。

## 3. 研究发现（纯事实层）
引用1：（研究标题 + 期刊/年份 + 2-3句话核心发现）
引用2：（同上）
（只陈述事实，不加判断）

## 4. 碰撞逻辑
触动点与已有框架放在一起看，出现了什么张力、矛盾或互补？
大白话，不超过5句。

## 5. 我的判断
⚠️ 以下为陛下原话，臣展开论证，但核心观点必须忠于原话：

「陛下判断原话」

臣展开：（≥400字，大量具体场景，必须回答"信念变了没有"）

## 6. 读者带走
① 给老师：具体能做什么（≥50字）
② 给老师（另一个角度）：具体能做什么（≥50字）
③ 判断标准：遇到什么情况时用这个洞察判断（≥30字）

## 7. 刻意不写
本条洞察刻意没有涉及哪些角度？为什么？
（防止面面俱到的综述，显式声明边界）
```

---

### Step 3：并行spawn 4个读者Agent

**⚠️ spawn规则（铁律）**：
- 主Agent直接spawn，不通过子Agent代spawn
- 每个读者Agent必须设置 `runTimeoutSeconds=300`
- 所有spawn并行，同时发出，不串行等待

**4个角色**：
1. `reader_new_teacher` — 新教师（1-3年教龄）
2. `reader_senior_teacher` — 资深教师（5年以上）
3. `reader_principal` — 校长/教学管理者
4. `reader_expert` — K12教育专家

**每个角色的system prompt**（共性部分）：
```
你是[角色名]，[角色描述]。
你正在阅读一篇教育洞察。请从你的角色视角给出真实的第一反应。
回复必须包含：
1. **第一反应：**（读完后的第一句话，不超过2句）
2. **最大疑问：**（你最想追问作者的一句话，不超过2句）
3. **会不会转发：**（会/不会/看情况 + 一句话原因）

禁止：打分/评价文章质量/跳出角色说话/超过2句
```

**Spawn方式**（4个并行）：
```
sessions_spawn(
  task="[洞察全文完整内容] + [角色专属补充]",
  runtime="subagent",
  agentId="reader_new_teacher",
  runTimeoutSeconds=300,
  mode="run"
)
sessions_spawn(
  task="[洞察全文完整内容] + [角色专属补充]",
  runtime="subagent",
  agentId="reader_senior_teacher",
  runTimeoutSeconds=300,
  mode="run"
)
sessions_spawn(
  task="[洞察全文完整内容] + [角色专属补充]",
  runtime="subagent",
  agentId="reader_principal",
  runTimeoutSeconds=300,
  mode="run"
)
sessions_spawn(
  task="[洞察全文完整内容] + [角色专属补充]",
  runtime="subagent",
  agentId="reader_expert",
  runTimeoutSeconds=300,
  mode="run"
)
```

---

### Step 4：汇总读者反应

收集4个角色的输出，格式：

```markdown
## 读者模拟反应

### 新教师
**第一反应：**（1-2句）
**最大疑问：**（1-2句）
**会不会转发：**（会/不会/看情况 + 原因）

### 资深教师
（同上格式）

### 校长
（同上格式）

### K12教育专家
（同上格式）
```

---

### Step 5：推送陛下

1. 合并洞察全文 + 读者模拟反应
2. 通过 `message` 工具发送（action=send, channel=feishu, target=陛下ID）
3. 消息末尾附：「📌 请审核：回复「发布」→ 进入存储 / 回复「改，方向是：XXXX」→ 重写 / 回复「不发」→ 存入洞察库不推送」

---

## 限制条件（铁律）

1. 陛下判断原话一字不改，忠实记录在洞察第5部分
2. 第5部分"臣展开"必须≥400字，大量具体场景
3. 洞察中所有数字必须有来源，禁止捏造
4. 读者Agent不输出分数，只输出第一反应+最大疑问+转发意愿
5. 所有spawn由本skill主Agent直接管理，不委托子Agent spawn
