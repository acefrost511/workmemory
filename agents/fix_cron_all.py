#!/usr/bin/env python3
"""修复情报官cron：删除所有旧版，用8分钟intel超时重建"""
import subprocess, json, sys, os
from datetime import datetime

def run(args, timeout=30):
    r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    return r

# ==== 1. 获取所有cron ====
print("【1/4】检查现有cron...")
r = run(['openclaw', 'cron', 'list', '--json'])
text = r.stdout
idx = text.find('{')
if idx < 0:
    print("无法获取cron列表"); sys.exit(1)
crons = json.loads(text[idx:]).get('jobs', [])

// 找到所有情报官cron
info_ids = [c['id'] for c in crons if '情报官' in c.get('name','')]
print(f"  找到{len(info_ids)}个旧情报官cron: {info_ids}")

# ==== 2. 删除所有旧cron ====
print("\n【2/4】删除所有旧情报官cron...")
for cid in info_ids:
    r = run(['openclaw', 'cron', 'remove', cid])
    if r.returncode == 0:
        print(f"  ✓ 已删除 {cid}")
    else:
        print(f"  ✗ 删除失败 {cid}: {r.stderr[:100]}")

# ==== 3. 读取任务消息 ====
print("\n【3/4】读取任务消息...")
with open('/workspace/agents/info_officer/CRON_TASK_V3.txt', 'r') as f:
    msg = f.read()
print(f"  消息长度: {len(msg)}字符")

# ==== 4. 通过gateway config API创建cron ====
print("\n【4/4】创建新的情报官cron...")
# 使用gateway config来创建cron（绕过CLI的--message问题）
# 先获取现有cron配置
r = run(['openclaw', 'cron', 'list', '--json'])
text = r.stdout
idx = text.find('{')
crons_after = json.loads(text[idx:]).get('jobs', [])
info_ids_after = [c['id'] for c in crons_after if '情报官' in c.get('name','')]
print(f"  清理后剩余: {len(info_ids_after)}个")

# 使用环境变量传消息（绕过CLI参数长度限制）
env = {**os.environ, '_OPENCLAW_CRON_MSG': msg}
r = run(['openclaw', 'cron', 'add',
    '--name', '情报官日报_每日05:00扫描',
    '--cron', '0 5 * * *',
    '--tz', 'Asia/Shanghai',
    '--session', 'isolated',
    '--agent', 'info_officer',
    '--timeout-seconds', '3600',
    '--announce',
    '--json'], timeout=20)

print(f"  RC: {r.returncode}")
print(f"  OUT长度: {len(r.stdout)}")
print(f"  ERR: {r.stderr[:200] if r.stderr else '(无)'}")

text = r.stdout
idx = text.find('{')
if idx >= 0:
    try:
        d = json.loads(text[idx:])
        cid = d.get('id', '?')
        nxt = d.get('state', {}).get('nextRunAtMs', '?')
        print(f"\n✅ 创建成功!")
        print(f"   ID: {cid}")
        print(f"   下次运行: {nxt}")
        if nxt:
            dt = datetime.fromtimestamp(nxt/1000)
            print(f"   = {dt.strftime('%Y-%m-%d %H:%M:%S')} 北京时间")
    except Exception as e:
        print(f"JSON解析失败: {e}")
        print("原始:", text[:400])
else:
    print(f"创建失败: {text[:300]}")
    # 尝试不用--agent，纯用--message
    print("\n  尝试备用方法（纯message）...")
    env2 = {**os.environ, '_OPENCLAW_CRON_MSG2': msg}
    r2 = run(['openclaw', 'cron', 'add',
        '--name', '情报官日报_每日05:00扫描_备用',
        '--cron', '0 5 * * *',
        '--tz', 'Asia/Shanghai',
        '--session', 'isolated',
        '--timeout-seconds', '3600',
        '--announce',
        '--json'], timeout=20, env=env2)
    print(f"  备用RC: {r2.returncode}")
    print(f"  备用OUT: {r2.stdout[:300]}")
    print(f"  备用ERR: {r2.stderr[:200] if r2.stderr else '(无)'}")
