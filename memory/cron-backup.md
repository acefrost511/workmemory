# 定时任务备份配置
> 本文件用于在定时任务被清空时快速重建
> 更新时间：2026-03-22 01:26

## 任务清单

### 1. 每日汇报-每晚7点
```json
{
  "name": "每日汇报-每晚7点",
  "schedule": {"kind": "cron", "expr": "0 19 * * *", "tz": "Asia/Shanghai"},
  "payload": {"kind": "agentTurn", "message": "向陛下汇报当日全部进展"},
  "delivery": {"mode": "announce", "channel": "last"},
  "sessionTarget": "isolated",
  "agentId": "main",
  "enabled": false
}
```

### 2. 周巡检-每周日24点
```json
{
  "name": "周巡检-每周日24点",
  "schedule": {"kind": "cron", "expr": "0 0 * * 0", "tz": "Asia/Shanghai"},
  "payload": {"kind": "agentTurn", "message": "执行记忆巡检：容量统计、过期扫描、一致性校验"},
  "delivery": {"mode": "announce", "channel": "last"},
  "sessionTarget": "isolated",
  "agentId": "main",
  "enabled": false
}
```

### 3. GitHub同步-每周一2点
```json
{
  "name": "GitHub同步-每周一2点",
  "schedule": {"kind": "cron", "expr": "0 2 * * 1", "tz": "Asia/Shanghai"},
  "payload": {"kind": "agentTurn", "message": "执行GitHub全量同步：预检→差异扫描→提交→推送→确认"},
  "delivery": {"mode": "announce", "channel": "last"},
  "sessionTarget": "isolated",
  "agentId": "main",
  "enabled": false
}
```

### 4. 情报扫描-每天5点（工作日）
```json
{
  "name": "情报扫描-每天5点",
  "schedule": {"kind": "cron", "expr": "0 5 * * 1-5", "tz": "Asia/Shanghai"},
  "payload": {
    "kind": "agentTurn",
    "message": "1. 情报官搜索K12 AI教育最新资讯（调用9个子agent）；2. 更新master文档，删除超过180天的内容，保持英文研究储备≥100篇；3. K12教育专家从master中按发表时间从旧到新挑选10篇英文研究；4. 产出10篇精选资讯速览推送给陛下（教师场景80%，家庭20%），每条需包含：原文标题+中文翻译标题+来源期刊名称+发布日期+链接地址"
  },
  "delivery": {"mode": "announce", "channel": "last", "to": "ou_b60e71d5307978b7ac0151f377cdd512"},
  "sessionTarget": "isolated",
  "agentId": "info_officer",
  "enabled": false
}
```

### 5. 情报扫描-每周六5点
```json
{
  "name": "情报扫描-每周六5点",
  "schedule": {"kind": "cron", "expr": "0 5 * * 6", "tz": "Asia/Shanghai"},
  "payload": {
    "kind": "agentTurn",
    "message": "1. 情报官从本周日报搜索结果增量汇总，更新master文档，删除超过180天的内容；2. K12教育专家从master中按发表时间从旧到新挑选15篇英文研究；3. 产出15篇周资讯速览推送给陛下（教师场景80%，家庭20%），每条需包含：原文标题+中文翻译标题+来源期刊名称+发布日期+链接地址"
  },
  "delivery": {"mode": "announce", "channel": "last", "to": "ou_b60e71d5307978b7ac0151f377cdd512"},
  "sessionTarget": "isolated",
  "agentId": "info_officer",
  "enabled": false
}
```

## 状态记录
- 2026-03-22 01:26: 定时任务再次被清空，已将配置备份至此文件，等待陛下指示是否重建
