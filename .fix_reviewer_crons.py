import json
from datetime import datetime, timezone, timedelta

bj = timezone(timedelta(hours=8))

with open('/workspace-inner/.openclaw/cron/jobs.json') as f:
    data = json.load(f)

new_jobs = []
removed = []
for j in data['jobs']:
    jid = j.get('id','')
    if jid.startswith('reviewer-05-'):
        removed.append(jid)
    else:
        new_jobs.append(j)

# Update 05:00 cron to spawn reviewer after intel agents
for j in new_jobs:
    if j.get('id') == '39875f44-10a0-46a0-ad42-eb3354a64bfe':
        old_msg = j['payload']['message']
        reviewer_append = '\n\nspawn完成后，再spawn 3个常驻reviewer（持续监控.pending/）：\nsessions_spawn(task="读取 /workspace/agents/reviewer_en_01/SOUL.md - 实时监控模式：扫描.pending/有新文件立即处理，无新文件时每2分钟重扫，持续运行8分钟后退出", runtime="subagent", agentId="reviewer_en_01", runTimeoutSeconds=480, mode="run")\nsessions_spawn(task="读取 /workspace/agents/reviewer_cn_02/SOUL.md - 实时监控模式：扫描.pending/有新文件立即处理，无新文件时每2分钟重扫，持续运行8分钟后退出", runtime="subagent", agentId="reviewer_cn_02", runTimeoutSeconds=480, mode="run")\nsessions_spawn(task="读取 /workspace/agents/reviewer_intl_03/SOUL.md - 实时监控模式：扫描.pending/有新文件立即处理，无新文件时每2分钟重扫，持续运行8分钟后退出", runtime="subagent", agentId="reviewer_intl_03", runTimeoutSeconds=480, mode="run")'
        j['payload']['message'] = old_msg + reviewer_append
        print('Updated 05:00 cron to spawn 3 reviewers')

# Persistent reviewer cron (every 10 minutes)
reviewer_msg = (
    '【常驻审核 - 每10分钟扫描.pending/】\n'
    '扫描 /workspace/knowledge/原文库/.pending/ 目录\n'
    '找到待审核文件，立即spawn 3个审核Agent处理（spawn后立即退出，不等待）：\n'
    'sessions_spawn(task="读取 /workspace/agents/reviewer_en_01/SOUL.md 并完整执行审核任务", runtime="subagent", agentId="reviewer_en_01", runTimeoutSeconds=240, mode="run")\n'
    'sessions_spawn(task="读取 /workspace/agents/reviewer_cn_02/SOUL.md 并完整执行审核任务", runtime="subagent", agentId="reviewer_cn_02", runTimeoutSeconds=240, mode="run")\n'
    'sessions_spawn(task="读取 /workspace/agents/reviewer_intl_03/SOUL.md 并完整执行审核任务", runtime="subagent", agentId="reviewer_intl_03", runTimeoutSeconds=240, mode="run")\n'
    'spawn后立即退出，不等待结果。'
)

reviewer_cron = {
    'id': 'reviewer-persistent',
    'agentId': 'main',
    'sessionKey': 'agent:main:main',
    'name': '常驻审核Agent-每10分钟唤醒',
    'enabled': True,
    'createdAtMs': int(datetime.now(tz=bj).timestamp() * 1000),
    'updatedAtMs': int(datetime.now(tz=bj).timestamp() * 1000),
    'schedule': {'kind': 'every', 'everyMs': 600000, 'tz': 'Asia/Shanghai'},
    'sessionTarget': 'isolated',
    'wakeMode': 'now',
    'payload': {
        'kind': 'agentTurn',
        'message': reviewer_msg,
        'timeoutSeconds': 20
    },
    'delivery': {'mode': 'none'},
    'state': {'nextRunAtMs': int(datetime.now(tz=bj).timestamp() * 1000)}
}
new_jobs.append(reviewer_cron)

data['jobs'] = new_jobs

with open('/workspace-inner/.openclaw/cron/jobs.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

print(f'Removed {len(removed)}定时 reviewer crons: {removed}')
print(f'Added 常驻审核Agent cron (every 10 min)')
print(f'Total jobs: {len(data["jobs"])}')
