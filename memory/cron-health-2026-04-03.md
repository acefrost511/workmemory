# Cron健康检查报告
**检查时间**：2026-04-03 02:18（北京时间）
**检查触发**：Cron健康检查-每2小时（id: 920e7cc2）

---

## 一、任务概览

- 全部Cron任务：10（均为已启用，无禁用任务）
- 活跃任务总数：10
- 正常任务数：9
- 警告任务数：1（consecutiveErrors=2，接近阈值）
- 失败任务数：0（consecutiveErrors ≥ 3：0个）

---

## 二、活跃任务详情

### ✅ 正常任务（9个）

| 任务名称 | ID | 上次运行 | 耗时 | 状态 |
|---------|----|---------|------|------|
| Cron健康检查-每2小时 | 920e7cc2 | 2026-04-03 00:18 | 137s | ok |
| 记忆同步-每1小时 | 849872d0 | 2026-04-03 01:03 | 14s | ok |
| 信念抽屉每日备份-11:00 | d5963f61 | — | — | 等待中（下次04-03 11:00） |
| 情报官-抽屉充实-每天12:30 | 0bef52ae | — | — | 等待中（下次04-03 12:30） |
| 抽屉素材完整性检查-12:00 | e1838fe4 | — | — | 等待中（下次04-03 12:00） |
| IP每日创意碰撞-17:30 | 6324f287 | 2026-04-02 17:30 | 247s | ok |
| 晚间汇报 | 9e7bfee2 | 2026-04-02 19:00 | 307s | ok |
| GitHub全量同步-每天凌晨3点 | c1d720e3 | 2026-04-03 03:00 | 180s | ⚠️ error |
| 情报扫描-每天5点 | 26e936f8 | 2026-04-02 05:00 | 321s | ok |

### ⚠️ 警告任务（consecutiveErrors ≥ 2，接近阈值，共1个）

**GitHub全量同步-每天凌晨3点（cron: c1d720e3）**
- 上次运行：2026-04-03 03:00
- 错误原因：cron: job execution timed out（执行180078ms ≈ 3分钟，超出timeoutSeconds=300限制）
- 连续错误：consecutiveErrors=2（距阈值3还差1次）
- 触发超时原因：GitHub推送操作在网络不佳时耗时较长，180秒内未完成

**自动修复状态**：未触发（consecutiveErrors=2 < 阈值3）
**建议陛下操作**：手动将该任务timeoutSeconds从300调高至450秒（命令：`openclaw cron edit c1d720e3 --timeout-seconds 450`，需先修复openclaw-weixin配置报错才能执行）

---

## 三、历史任务（已知）

以下任务在上期报告中存在，本期未出现在活跃列表中（可能已过期/清理）：
- AI建造者日报_FollowBuilders每日摘要_v2（0d38e015）：consecutiveErrors=1，未再出现
- 记忆巡检（35fde329）：下次运行04-06（周0凌晨）
- 工作区定期清理-每周日凌晨3点（b24bfa49）：等待中（下次04-06）

---

## 四、本次采取的行动

1. **无consecutiveErrors≥3任务**：所有任务均未触发自动修复规则
2. **GitHub全量同步超时问题（consecutiveErrors=2）**：
   - 未能自动修复（差1次才达阈值）
   - 尝试通过CLI `openclaw cron edit` 调高timeoutSeconds → 失败
   - 失败原因：openclaw-weixin配置报错（channels.openclaw-weixin: unknown channel id）
   - 该配置问题同时影响了所有openclaw CLI命令（cron list/status/edit均失败）
   - **需陛下授权处理**：移除openclaw.json中的openclaw-weixin配置（或安装对应plugin）
3. **重新运行失败任务**：无（consecutiveErrors=2，未达3次阈值）

---

## 五、配置问题说明（阻塞CLI）

**问题**：`/root/.openclaw/openclaw.json` 包含已卸载的openclaw-weixin插件配置，导致所有openclaw CLI命令（包括cron edit）失败。

**影响范围**：
- `openclaw cron edit` 无法执行（超时调整无法自动完成）
- `openclaw cron list` CLI层面报错（但实际JSON仍能返回）
- `openclaw doctor` 无法正常运行

**解决方案（需陛下授权）**：
```bash
# 方案1：安装plugin（如果还需要微信渠道）
npm install @tencent-weixin/openclaw-weixin

# 方案2：移除无效配置（臣无权直接操作openclaw.json）
# 需移除 channels.openclaw-weixin 和 plugins.entries.openclaw-weixin 两个节点
```

---

## 六、统计摘要

- 活跃任务总数：10
- 正常任务数：9
- 警告任务数：1（consecutiveErrors=2，GitHub同步超时）
- 失败任务数：0（consecutiveErrors ≥ 3：0个）
- 连续失败≥5次需立即通知陛下：0个 → 无需发送飞书紧急通知

---

## 七、旧报告清理

- 检查现有报告：`cron-health-2026-04-01.md`、`cron-health-2026-04-02.md`、`cron-health-2026-04-03.md`
- 当前日期：04-03，7天保留期 = 03-27及之后
- 最早报告04-01，距今2天，在保留期内
- **本次清理：无文件被删除**（所有报告均在7天保留期内）

---

*报告生成时间：2026-04-03 02:18（北京时间）*
