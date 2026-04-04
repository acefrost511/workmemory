#!/usr/bin/env python3
"""执行Cron健康检查行动：更新超时时间"""
import subprocess, json, sys, datetime

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

# 当前时间
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
print(f"检查时间: {now}")

# 1. 获取当前cron列表
out, err, rc = run(['openclaw', 'cron', 'list', '--json'])
text = out.strip()
idx = text.find('{')
if idx == -1:
    print("ERROR: Cannot find JSON in cron list output")
    sys.exit(1)
json_text = text[idx:]
data = json.loads(json_text)
jobs = data.get('jobs', [])
print(f"活跃任务总数: {len(jobs)}")

# 2. 识别警告任务
warning_jobs = []
ok_count = 0
for j in jobs:
    s = j.get('state', {})
    ce = s.get('consecutiveErrors', 0)
    ls = s.get('lastStatus', '?')
    if ls == 'ok':
        ok_count += 1
    elif ce >= 3:
        warning_jobs.append({
            'id': j['id'],
            'name': j.get('name', '')[:50],
            'ce': ce,
            'timeout': j.get('payload', {}).get('timeoutSeconds', 0),
            'error': s.get('lastError', ''),
            'delivery_mode': j.get('delivery', {}).get('mode', 'none'),
        })

print(f"正常任务数: {ok_count}")
print(f"警告任务数(consecutiveErrors>=3): {len(warning_jobs)}")
print()

actions_taken = []

# 3. 处理警告任务
for w in warning_jobs:
    print(f"处理警告: {w['name']}")
    print(f"  ID: {w['id']}")
    print(f"  consecutiveErrors: {w['ce']}")
    print(f"  error: {w['error']}")
    print(f"  timeout: {w['timeout']}")
    
    err_lower = w['error'].lower()
    
    if 'timeout' in err_lower:
        # 超时错误 → 调高1.5倍
        new_timeout = int(w['timeout'] * 1.5)
        print(f"  → 行动计划: 超时，调整 timeout {w['timeout']}s → {new_timeout}s")
        cmd = ['openclaw', 'cron', 'set', w['id'], '--timeout-seconds', str(new_timeout)]
        o, e, rc = run(cmd)
        if rc == 0:
            actions_taken.append(f"✓ {w['name']} timeout {w['timeout']}s→{new_timeout}s (超时调整)")
            print(f"  → 结果: 成功")
        else:
            actions_taken.append(f"✗ {w['name']} timeout调整失败: {e[:100]}")
            print(f"  → 结果: 失败 - {e[:100]}")
    elif 'delivery failed' in err_lower or 'message failed' in err_lower:
        # 投递失败 → 改为mode=none
        print(f"  → 行动计划: 投递失败，当前mode={w['delivery_mode']}")
        if w['delivery_mode'] != 'none':
            cmd = ['openclaw', 'cron', 'set', w['id'], '--delivery', 'none']
            o, e, rc = run(cmd)
            if rc == 0:
                actions_taken.append(f"✓ {w['name']} delivery→none (投递失败调整)")
                print(f"  → 结果: 成功")
            else:
                actions_taken.append(f"✗ {w['name']} delivery调整失败: {e[:100]}")
                print(f"  → 结果: 失败")
        else:
            actions_taken.append(f"⊘ {w['name']} delivery已为none，无需调整")
            print(f"  → 结果: 无需调整")
    else:
        # 执行错误 → 重新运行
        print(f"  → 行动计划: 执行错误，尝试重新运行")
        cmd = ['openclaw', 'cron', 'run', w['id']]
        o, e, rc = run(cmd)
        if rc == 0:
            actions_taken.append(f"✓ {w['name']} 重新运行已触发")
            print(f"  → 结果: 成功触发")
        else:
            actions_taken.append(f"✗ {w['name']} 重新运行失败: {e[:100]}")
            print(f"  → 结果: 失败 - {e[:100]}")
    print()

# 4. 检查是否有CE>=5需要通知陛下
urgent = [w for w in warning_jobs if w['ce'] >= 5]
if urgent:
    print(f"⚠️ 发现 {len(urgent)} 个连续失败>=5的任务，需要通知陛下！")
    for u in urgent:
        print(f"  - {u['name']} (CE={u['ce']})")
    # 通过飞书通知陛下的消息
    feishu_msg = f"⚠️ **Cron紧急告警**\n\n发现 {len(urgent)} 个Cron任务连续失败≥5次，请关注：\n"
    for u in urgent:
        feishu_msg += f"• **{u['name']}** (CE={u['ce']})\n  错误：{u['error']}\n"
    print("FEISHU_ALERT:" + feishu_msg)
else:
    print("✓ 无连续失败>=5的任务，无需紧急通知陛下")

# 5. 打印行动摘要
print()
print("=== 行动摘要 ===")
for a in actions_taken:
    print(a)

print()
print("DONE")
