# 完整流程追踪表
> 日期：2026-03-29 | 执行模式：subagent+SOUL注入

## 情报官搜索阶段

| 批次 | Agent | 状态 | 启动时间 | 预计完成 |
|------|-------|------|---------|---------|
| 批次1 | intel_01（英文期刊） | 🔄 进行中 | 09:53 | 09:58 |
| 批次1 | intel_04（国际组织） | 🔄 进行中 | 09:53 | 09:58 |
| 批次1 | intel_07（中文期刊） | 🔄 进行中 | 09:53 | 09:58 |
| 批次2 | intel_02 | ⏳ 待启动 | - | - |
| 批次2 | intel_05 | ⏳ 待启动 | - | - |
| 批次2 | intel_08 | ⏳ 待启动 | - | - |
| 批次3 | intel_03 | ⏳ 待启动 | - | - |
| 批次3 | intel_06 | ⏳ 待启动 | - | - |
| 批次3 | intel_09 | ⏳ 待启动 | - | - |
| 批次4 | intel_10 | ⏳ 待启动 | - | - |
| 批次4 | intel_11 | ⏳ 待启动 | - | - |
| 批次4 | intel_12 | ⏳ 待启动 | - | - |

## IP内容团队阶段

| 步骤 | Agent | 状态 | 触发条件 |
|------|-------|------|---------|
| 洞察生成 | edu_writer | ⏳ 待启动 | intel批次1-4全部完成 |
| 5视角并行评分 | reader_* | ⏳ 待启动 | edu_writer完成 |
| 汇总推送 | edu_lead | ⏳ 待启动 | reader评分完成 |

## SOP文档

- 清单：/workspace/agents/AGENT_SPAWN_MANIFEST.json
- Spawn规范：/workspace/agents/SPAWN_SOP.md
- 情报官SOP：/workspace/agents/INTEL_SOP.md
- IP团队SOP：/workspace/agents/IP_SOP.md
