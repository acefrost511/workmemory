# Agent Spawn SOP（临时Agent + SOUL.md注入方案）
> 版本：1.0 | 日期：2026-03-29 | 确立依据：实测intel_01可正常spawn

## 核心原则

**所有Agent必须从 AGENT_SPAWN_MANIFEST.json 白名单中查找，不得凭空指定agentId。**

每次Spawn流程：
1. 查清单 → 读SOUL.md → 拼接任务 → Spawn → 等结果 → 汇报

---

## 标准化Spawn函数模板

```
【角色设定 - 请严格遵循】
$(cat /workspace/agents/{agentId}/SOUL.md)

【本次任务】
{task}

【输出要求】
{output_format}
```

---

## 并发策略（重要）

**绝对禁止同时Spawn超过3个Agent。** 原因：每次spawn都是独立HTTP请求，并发太多会导致部分超时或OOM。

**正确的批量Spawn方式：**
- 每次最多3个并行
- 每个Agent任务独立（各自读自己的SOUL.md）
- 所有Agent都完成后，主Agent再汇总

** intel团队 标准并发模式：**
```
第一批（并行3个）：intel_01 + intel_04 + intel_07
第二批（并行3个）：intel_02 + intel_05 + intel_08
第三批（并行3个）：intel_03 + intel_06 + intel_09
第四批（并行3个）：intel_10 + intel_11 + intel_12
```

---

## 超时策略

| Agent类型 | 超时时间 | 超时处理 |
|-----------|---------|---------|
| intel_01~12（搜索） | 5分钟 | 超时后重新spawn 1次，失败则记录"超时未完成" |
| intel_reviewer_*（审核） | 3分钟 | 超时后记录原始输出，标记"未完成审核" |
| edu_writer（写作） | 10分钟 | 超时后重新spawn 1次 |
| reader_*（读者） | 3分钟 | 超时后记录原始输出 |
| edu_lead（主编） | 15分钟 | 超时后继续执行（主编可以跑更久） |
| info_officer（情报官） | 10分钟 | 超时后继续执行（协调工作可以跑更久） |

**超时重试规则：**
- 第一次超时 → 等30秒 → 重新spawn同一Agent
- 第二次超时 → 等1分钟 → 再次spawn
- 第三次超时 → 放弃，汇报陛下"该Agent连续超时"

---

## intel团队 完整工作流

```
1. 读取 intel_SOP.md 了解情报搜索标准流程
2. 按领域分配任务给 intel_01~12（每批3个并行）
3. 各Agent独立搜索，写入 /workspace/knowledge/原文库/
4. 汇总DOI列表，spawn intel_reviewer_* 审核
5. 审核通过后，通知陛下结果
```

---

## IP内容团队 完整工作流

```
1. 主编 edu_lead 接收任务
2. edu_lead spawn edu_writer（写作）
3. edu_writer完成后，edu_lead并行spawn 5个reader_*审核
4. edu_lead汇总评分，≥9.0则推送，不达标则重写
5. 推送飞书消息卡片
```

---

## 禁止事项

1. **禁止不读SOUL.md就直接spawn** —— 那样Agent是空的，没有角色设定
2. **禁止一次性spawn超过3个** —— 会导致并发过高，部分任务饿死
3. **禁止不设置超时时间就spawn** —— 无超时会导致任务挂起
4. **禁止在任务描述里写角色扮演指令** —— 角色在SOUL.md里，不要在task参数里重复

---

## 验证记录

- 2026-03-29：实测 intel_01 可以正常spawn（runtime=subagent），SOUL.md注入有效
