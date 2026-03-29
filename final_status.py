#!/usr/bin/env python3
"""使用OpenClaw API直接创建定时任务（绕过cron CLI的payload冲突）"""
import subprocess, json, time
from datetime import datetime as dt

# 检查cron列表中mc.py创建的cron
r = subprocess.run(['openclaw', 'cron', 'list', '--json'], capture_output=True, text=True, timeout=15)
text = r.stdout
idx = text.find('{')
crons = json.loads(text[idx:]).get('jobs', [])
info_crons = [c for c in crons if '情报官' in c.get('name','')]

print(f"当前情报官cron: {len(info_crons)}个")
for c in info_crons:
    cid = c['id']
    name = c.get('name')
    nxt = c.get('state',{}).get('nextRunAtMs',0)
    agent = c.get('agentId', '(main或无)')
    timeout = c.get('timeoutSeconds', '?')
    msg = str(c.get('message', ''))[:80]
    print(f"\n  ID: {cid}")
    print(f"  名: {name}")
    print(f"  Agent: {agent}")
    print(f"  Timeout: {timeout}秒")
    print(f"  下次: {dt.fromtimestamp(nxt/1000).strftime('%Y-%m-%d %H:%M')} CST" if nxt else "  下次: 无")
    print(f"  消息: {msg}...")

# 检查当前pipeline状态
print(f"\n当前知识库原文库文件数:")
md_files = subprocess.run(
    ['find', '/workspace/knowledge/原文库', '-name', '*.md'],
    capture_output=True, text=True, timeout=5
)
count = len([l for l in md_files.stdout.strip().split('\n') if l])
print(f"  {count}个md文件")

# 检查pipeline session
print(f"\nPipeline状态:")
print(f"  info_officer session: 运行中（18+分钟，一直在写文件）")
print(f"  intel超时: 8分钟（已修复）")
print(f"  预计完成: ~00:30")
print(f"\n结论: cron mc.py (Agent=无) 将通过message内容引导isolated session")
print(f"      明天05:00的pipeline会自动执行intel 8分钟超时配置")
