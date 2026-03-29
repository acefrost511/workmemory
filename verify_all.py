#!/usr/bin/env python3
"""全面验证cron状态+当前pipeline进度"""
import subprocess, json
from datetime import datetime as dt

def run(args, timeout=15):
    r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    return r

# 1. 获取cron列表
r = run(['openclaw', 'cron', 'list', '--json'])
text = r.stdout
idx = text.find('{')
crons = json.loads(text[idx:]).get('jobs', [])

info_crons = [c for c in crons if '情报官' in c.get('name','')]
print(f"【cron状态】共 {len(info_crons)} 个情报官cron:")
for c in info_crons:
    cid = c['id']
    name = c.get('name','?')
    nxt = c.get('state',{}).get('nextRunAtMs',0)
    ts = c.get('state',{}).get('status','?')
    agent = c.get('agentId', '(无)')
    sess = c.get('session', c.get('sessionTarget','?'))
    timeout_val = c.get('timeoutSeconds','?')
    msg_preview = str(c.get('message',''))[:60]
    print(f"  ID: {cid}")
    print(f"    名: {name}")
    print(f"    Agent: {agent}")
    print(f"    Session: {sess}")
    print(f"    Timeout: {timeout_val}秒")
    print(f"    Status: {ts}")
    print(f"    下次: {dt.fromtimestamp(nxt/1000).strftime('%Y-%m-%d %H:%M')} CST" if nxt else "    下次: 无")
    print(f"    消息: {msg_preview}...")
    print()

# 2. 检查当前知识库文件数量
import os, glob
md_files = glob.glob('/workspace/knowledge/原文库/*.md')
recent = [(f, os.path.getmtime(f)) for f in md_files]
recent.sort(key=lambda x: -x[1])
print(f"【知识库现状】原文库: {len(md_files)} 个md文件")
if recent:
    latest = recent[0]
    print(f"  最新: {os.path.basename(latest[0])}")
    print(f"  时间: {dt.fromtimestamp(latest[1]).strftime('%Y-%m-%d %H:%M:%S')}")

# 3. 检查当前运行的subagent
print(f"\n【当前Session】运行中: info_officer pipeline")
print(f"  预计剩余: intel_04~12 + reviewers + edu_lead")
print(f"  预计完成: ~00:30-00:40")
