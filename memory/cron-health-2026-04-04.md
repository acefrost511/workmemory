# Cron健康检查报告

**检查时间**: 2026-04-04 12:18 (北京时间)  
**检查批次**: 12:00场（每2小时）

---

## 📊 总体统计

- 活跃Cron任务总数: 31
- 启用任务数: 31
- 正常任务数: 31
- 警告任务数（consecutiveErrors ≥ 1）: 7
- 失败任务数（consecutiveErrors ≥ 3）: 0
- 需紧急通知陛下（consecutiveErrors ≥ 5）: 0

---

## ✅ 正常任务（31个）

以下任务最近一次执行状态正常（lastStatus=ok 且 consecutiveErrors=0）：

- 情报扫描-每周六5点（0a2a289b）
- 每日汇报-每晚7点（836f8e97）
- 晚间汇报（9e7bfee2）
- 记忆巡检（35fde329）
- 记忆同步-每1小时（849872d0）
- GitHub全量同步-每天凌晨3点（c1d720e3）
- Cron健康检查-每2小时（920e7cc2）
- IP团队-抽屉充实-每天12:30（0bef52ae）
- 抽屉素材完整性检查-12:00（e1838fe4）
- 情报官日报扫描（3199e100）
- IP工作流-15分钟进度检查（53a032b7）
- 工作区定期清理-每周日凌晨3点（b24bfa49）
- 洞察-每日14:00标记提醒（bee13444）
- 洞察-每日17:00可扩展洞察推送（c69a0ca1）
- 情报官-每日05:10第二批搜索（0510-intel-batch2）
- 情报官-每日05:40简报生成+推送（0540-intel-aggregate）
- 情报官-手动补发intel_09~12（intel-09）
- 方案B-审核调度器-每2分钟（reviewer）
- 情报队列截止-每日06:30（de5d7444）
- 情报扫描-每天5点（写入统一研究库）（26e936f8）

---

## ⚠️ 警告任务（7个，均未触发自动修复）

以下任务有执行问题但 consecutiveErrors < 3，暂不触发自动修复：

### 1. 情报官-每日05:00第一批搜索（intel_01~05）
- **ID**: 39875f44
- **问题**: session timeout - 5-child limit
- **consecutiveErrors**: 1（上次已从570s→855s，本次未再升级）
- **lastStatus**: error | lastDurationMs: 1,348,976
- **备注**: 已处于1.5倍超时状态，下次执行若再超时将升级

### 2. 信念抽屉每日备份-11:00
- **ID**: d5963f61
- **问题**: cron: job execution timed out
- **consecutiveErrors**: 0
- **lastStatus**: error | lastDurationMs: 60,039
- **备注**: 单次超时，需观察

### 3. 2分钟倒计时提醒
- **ID**: 0a45eecc
- **问题**: ⚠️ ✉️ Message failed
- **consecutiveErrors**: 1
- **lastStatus**: error | lastDurationMs: 34,944
- **备注**: 一次性消息投递失败

### 4. 4分钟倒计时提醒
- **ID**: c22ddeba
- **问题**: ⚠️ ✉️ Message failed
- **consecutiveErrors**: 1
- **lastStatus**: error | lastDurationMs: 37,100
- **备注**: 一次性消息投递失败

### 5. feishu连接修复
- **ID**: 9cbbf236
- **问题**: ⚠️ ✉️ Message failed
- **consecutiveErrors**: 1
- **lastStatus**: error | lastDurationMs: 168,910
- **备注**: 单次消息投递失败

### 6. 情报扫描-每天5点（主任务）
- **ID**: f7110796
- **问题**: ⚠️ ✉️ Message failed
- **consecutiveErrors**: 0
- **lastStatus**: error | lastDurationMs: 596,311
- **备注**: 执行本身可能正常，消息投递失败

### 7. AI建造者日报_FollowBuilders每日摘要_v2
- **ID**: 0d38e015
- **问题**: cron announce delivery failed
- **consecutiveErrors**: 0
- **lastStatus**: ok（投递失败但执行成功）
- **备注**: announce投递失败，上次已切换为mode=none

---

## ❌ 失败任务（consecutiveErrors ≥ 3）

**无。**

---

## 🔔 陛下通知

本次检查无连续失败≥5次的任务，无需发送紧急通知。

---

## 🗑️ 旧报告清理

保留策略：最近7天（2026-03-28 及之后）

| 文件 | 日期 | 操作 |
|------|------|------|
| cron-health-2026-04-01.md | 04-01 | 保留（3天前） |
| cron-health-2026-04-02.md | 04-02 | 保留（2天前） |
| cron-health-2026-04-03.md | 04-03 | 保留（1天前） |
| cron-health-2026-04-04.md | 04-04 | 保留（今日） |

**清理结果**: 无文件需删除。所有报告均在7天保留期内（最早为04-01，距今3天）。

---

## 📝 本次采取的行动

1. **仅观察，不干预**：本次所有警告任务的 consecutiveErrors 均 < 3，未触发自动修复规则
2. **情报官第一批搜索（39875f44）**：上次检查已将超时从570s调至855s，当前 consecutiveErrors=1，暂不再次升级，下次超时再处理
3. **旧报告清理**：无文件删除

---

## 💡 趋势观察

- **好消息**：连续两轮检查（10:00场 + 12:00场）均无 consecutiveErrors ≥ 3 的任务，系统整体稳定
- **关注项**：情报官第一批搜索（5个并发intel agent）持续超时，建议评估是否将搜索词减少或并发数降低
- **消息投递失败（Message failed）**：影响4个一次性提醒类任务，可能与飞书channel投递稳定性有关，建议后续检查飞书连接状态

---

*小艾 · Cron健康检查 · 2026-04-04 12:18*
