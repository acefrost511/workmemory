---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
---

# insight-extend | 可扩展洞察推送技能

## 技能概述

- **版本**：v1.0
- **创建日期**：2026-04-04
- **触发方式**：每日17:00自动调用（cron调度）
- **输入**：INSIGHT_LIBRARY.md
- **输出**：筛选3条可扩展洞察 → 飞书推送陛下
- **下游衔接**：陛下回复「用洞察#XX写文章」→ 触发5技能文章写作流程

---

## 执行流程

### Step 1：读取洞察库

读取 `/workspace/knowledge/insights/INSIGHT_LIBRARY.md`
（如果文件不存在，读取 `/workspace/knowledge/INSIGHT_LIBRARY.md`）

### Step 2：筛选可扩展洞察

**必须全部满足**：
1. 入库时间 ≥ 1天前（当天生成的不推）
2. 未标记「已扩展」
3. 未标记「不扩展」
4. 未被推送过3次（检查推送次数记录）

**不足3条时**：有多少推多少，不强行凑数
**库存为0时**：静默结束，不推送

### Step 3：组装推送内容

```markdown
## 今日可扩展洞察 ｜ YYYY-MM-DD

### 洞察 #INSIGHT_NEW_XXX
📅 生成于：YYYY-MM-DD
💡 当初的判断：「[判断原话，不超过50字]」
🔗 信念抽屉：#XX [抽屉名称]
📝 Hook句：[原文hook句]

（共N条）
```

### Step 4：推送

通过 `message` 工具发送（action=send, channel=feishu, target=陛下ID）

### Step 5：等待陛下回复并处理

**陛下可能的回复**：
- 「用洞察#INSIGHT_NEW_XX写文章」→ 触发5技能文章写作流程，更新该洞察标记 [已扩展-日期]
- 「这条以后也不用推了」→ 更新该洞察标记 [不扩展-日期]
- 「都不写」→ 这3条保留（推送次数+1），次日换3条

### Step 6：更新记录

每次推送后更新INSIGHT_LIBRARY.md中对应洞察的推送次数。

**沉默归档**：同一洞察被推送3次均未被选中 → 标记 [沉默归档-日期]，不再主动推送。

---

## 限制条件（铁律）

1. 当天生成的洞察不推送（入库时间<1天）
2. 推送次数独立计数，每次+1
3. 沉默归档后不再出现在可推送列表
4. 已扩展/不扩展的洞察永久排除
