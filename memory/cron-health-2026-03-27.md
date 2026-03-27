# Cron健康检查报告
**检查时间：** 2026-03-27 10:18 AM (Asia/Shanghai)  
**执行任务：** Cron健康检查-每2小时 (920e7cc2-89cd-403b-9c00-45d9d125006b)

---

## 📊 总体概况

- 活跃任务总数：10
- 正常任务数：7（ok）
- 警告任务数：1（error，累计2次失败，<3次阈值）
- 失败任务数：0（无连续失败≥3次的任务）
- 未运行任务数：2（idle，从未触发，属正常排程）

---

## ✅ 正常任务（7个）

1. **Cron健康检查-每2小时** | lastStatus=ok | consecutiveErrors=0
2. **记忆同步-每1小时** | lastStatus=ok | consecutiveErrors=0
3. **IP每日创意碰撞-17:30** | lastStatus=ok | consecutiveErrors=0
4. **晚间汇报-19:00** | lastStatus=ok | consecutiveErrors=0
5. **情报扫描-每天5点（周一至周五）** | lastStatus=ok | consecutiveErrors=0
6. **信念抽屉每日备份-11:00** | lastStatus=unknown（未触发，属正常）
7. **抽屉素材完整性检查-12:00** | lastStatus=unknown（未触发，属正常）
8. **记忆巡检（每周日）** | lastStatus=unknown（未触发，属正常）
9. **情报官-抽屉充实-每天12:30** | lastStatus=unknown（未触发，属正常）

---

## ⚠️ 警告任务（1个）

**GitHub全量同步-每天凌晨3点**
- ID：c1d720e3-0373-4fb0-804f-b9104e5273d4
- lastStatus：error
- lastRunStatus：error
- consecutiveErrors：2（距触发阈值还差1次）
- timeoutSeconds：300
- delivery：mode=none

**分析：** 连续失败2次，尚未达到≥3次阈值，本次仅记录警告，下次健康检查时若仍未修复将触发自动修复流程。

---

## 🔧 本次采取的行动

1. **观察GitHub全量同步：** consecutiveErrors=2，暂未触发自动修复（需≥3次）
2. **无超时任务需要调整：** 所有任务timeoutSeconds设置合理
3. **无投递失败任务：** 所有delivery配置正常
4. **无需重新运行任何任务：** 无连续失败≥3次的任务

---

## 📌 后续建议

- 关注GitHub全量同步（c1d720e3-0373-4fb0-804f-b9104e5273d4）：下次触发时若再次失败，consecutiveErrors将累积至3，届时需排查具体失败原因（建议手动运行一次 `openclaw cron run c1d720e3` 提前诊断）

---

**下次健康检查：** 约2小时后（12:18左右）
