# 情报官日报Cron可靠执行手册
> 制定时间：2026-03-29 23:35 | 依据：实测教训

## 核心发现（已验证）

### cron孤立session的硬上限
- 平台对孤立agent session的默认+最大timeout = **600秒（10分钟）**
- cron payload的timeoutSeconds=0会触发平台默认值600秒
- **必须显式设置timeoutSeconds=3600**，才能给60分钟预算

### info_officer的正确用法
- cron spawn info_officer（mode=run，超长timeout）
- info_officer立即spawn intel_0X作为background sub-agent（不等完成，立即返回）
- info_officer继续下一步，intel_0X在后台运行
- **关键是：info_officer的session本身不能被阻塞**

### 时间线估算（从info_officer被spawn开始）
```
T=0: info_officer启动
T=1: spawn intel_01~03 (并行, 3min超时)
T=4: spawn intel_04~06 (并行, 3min超时)
T=8: spawn intel_07~09 (并行, 3min超时)
T=12: spawn intel_10~12 (并行, 3min超时)
T=16: spawn intel_reviewer_* (并行, 5min超时)
T=21: spawn edu_lead (15min超时)
T=36: edu_lead推送飞书
→ 总计约40分钟，cron 60分钟预算充足
```

## Cron配置（已更新）

```json
{
  "id": "8e1507ee-130f-4d13-a941-a1c8cc9bd6c3",
  "expr": "0 5 * * *",
  "tz": "Asia/Shanghai",
  "timeoutSeconds": 3600,
  "sessionTarget": "isolated"
}
```

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| cron失败"job execution timed out" | timeoutSeconds=0触发平台默认值600s | 更新为3600 |
| intel搜索全部超时 | 来源网站慢，3分钟不够 | 缩短搜索范围或增加超时 |
| edu_lead超时 | 10分钟不够生成洞察 | 减少洞察数量（3条→1条） |
| 推送未发出 | 某步骤卡住 | edu_lead优先推送日报，再生成洞察 |

## 备用手动触发

如果明天5:10仍无推送，执行：
```
/agents/scripts/manual_trigger.sh
```
或直接spawn info_officer（臣已测试可用）。

## 验证时间线

当前info_officer（session: 0a7b065d）正在后台运行
→ 预计00:30-00:50推送
→ 明天5:00 cron会自动触发
→ cron有60分钟预算，intel超时已改为8分钟，预期成功

## 重要教训（2026-03-30 00:00+）

### cron + isolated session + payload规则
源码验证（/app/openclaw/dist/cron-cli-*.js）：
```javascript
if ([Boolean(systemEvent), Boolean(message)].filter(Boolean).length !== 1)
  throw new Error("Choose exactly one payload: --system-event or --message");
```
含义：isolated session必须有payload（system-event或message），且二选一。

### `--agent`和`--message`的关系（经验证）
- `--session isolated --agent info_officer`（无--message）：❓ 需要测试
  - v2 cron（2026-03-28）用此组合，成功创建
  - isolated session应加载agentId指定的agent的SOUL.md
- `--session isolated --message <msg>`（无--agent）：✅ mc.py用此组合
  - isolated session收到message作为任务
  - message内容告诉它读取info_officer/SOUL.md → 正确执行pipeline
- `--session isolated --agent info_officer --message <msg>`：❌ 冲突
  - `--agent`隐含设置payload，CLI报错"Choose exactly one payload"

### intel超时修复
- 原：各4分钟超时（搜索需要5-6分钟，导致大量超时）
- 改：各8分钟超时（在info_officer/SOUL.md）
- reviewer：10分钟→15分钟

### 平台timeout行为（重要新发现）
- `mode=run` subagent session：目前实测18分钟仍无压力，无固定10分钟限制
- `cron --expect-final=false`（默认）：cron立即返回，不等待agent完成
- cron的`timeoutSeconds`：控制isolated agent turn的超时，不是cron等待时间
- 结论：pipeline可以完整跑完（40-50分钟），cron会在60分钟后强制终止isolated agent

### 最终cron配置（2026-03-30 00:00）
- ID: 3b928748-02e6-4384-ab2b-f20e9e863c0b
- session: isolated
- timeoutSeconds: 3600（60分钟）
- message: 完整pipeline（intel 8分钟超时）
- 下次: 2026-03-30 05:00:00 CST
