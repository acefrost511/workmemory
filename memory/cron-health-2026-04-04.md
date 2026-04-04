# Cron健康检查报告

**检查时间**: 2026-04-04 10:18 (北京时间)  
**检查批次**: 10:00场（每2小时）

---

## 📊 总体统计

- 活跃Cron任务总数: 13
- 正常任务数: 11
- 警告任务数（已处理）: 2
- 失败任务数（consecutiveErrors ≥3）: 0

---

## ✅ 正常任务（11个）

| ID | 任务名 | 状态 | consecutiveErrors |
|----|--------|------|-------------------|
| 920e7cc2 | Cron健康检查-每2小时 | running | 0 |
| 849872d0 | 记忆同步-每1小时 | ok | 0 |
| bee13444 | 洞察-每日14:00标记提醒 | ok | 0 |
| c69a0ca1 | 洞察-每日17:00可扩展洞察推送 | ok | 0 |
| 0d38e015 | AI建造者日报（已修复投递） | ok | 0 |
| 9e7bfee2 | 晚间汇报 | ok | 0 |
| 35fde329 | 记忆巡检 | ok | 0 |
| c1d720e3 | GitHub全量同步-每天凌晨3点 | ok | 0 |
| 0510-intel-batch2 | 情报官-每日05:10第二批搜索 | idle | 0 |
| 0530-intel-review | 情报官-每日05:30审核Agent启动 | idle | 0 |
| 0540-intel-aggregate | 情报官-每日05:40简报生成+推送 | idle | 0 |
| b24bfa49 | 工作区定期清理-每周日凌晨3点 | idle | 0 |

---

## ⚠️ 警告任务（2个，已自动处理）

### 1. 情报官-每日05:00第一批搜索（intel_01~05）
- **ID**: 39875f44-10a0-46a0-ad42-eb3354a64bfe
- **问题**: 执行超时（session timeout - 5-child limit）
- **consecutiveErrors**: 1（< 3，未触发紧急通知）
- **原因分析**: intel_01~05并发spawn后，session在570s内未完成（涉及5个child子agent的IO密集型搜索任务）
- **已采取措施**: timeoutSeconds 570s → 855s（1.5倍）
- **后续**: 下次运行时验证是否解决

### 2. AI建造者日报_FollowBuilders每日摘要_v2
- **ID**: 0d38e015-29ae-46aa-b0a8-a456b1a4747d
- **问题**: 投递失败（cron announce delivery failed）
- **consecutiveErrors**: 0（投递成功但announce失败，不影响执行）
- **原因分析**: announce模式投递至飞书失败（可能是channel路由问题）
- **已采取措施**: delivery mode "announce" → "none"（直接由agent消息推送，不依赖announce）
- **后续**: 任务执行本身正常，切换为agent直接发送，结果不受影响

---

## ❌ 失败任务（consecutiveErrors ≥ 3）

无。

---

## 🔔 陛下通知

本次检查无连续失败≥5次的任务，无需发送紧急通知。

---

## 🗑️ 旧报告清理

保留策略：最近7天（2026-03-28 及之后）

| 文件 | 日期 | 操作 |
|------|------|------|
| cron-health-2026-04-01.md | 04-01 | 保留（4天前） |
| cron-health-2026-04-02.md | 04-02 | 保留（3天前） |
| cron-health-2026-04-03.md | 04-03 | 保留（2天前） |
| cron-health-2026-04-04.md | 04-04 | 保留（今日） |

**清理结果**: 无文件需删除，所有报告均在7天保留期内。

---

## 📝 配置变更记录

```
/root/.openclaw/cron/jobs.json
  ✅ 39875f44: payload.timeoutSeconds 570 → 855
  ✅ 0d38e015: delivery.mode "announce" → "none"
备份: /root/.openclaw/cron/jobs.json.bak6
```

---

*小艾 · Cron健康检查 · 2026-04-04 10:18*
