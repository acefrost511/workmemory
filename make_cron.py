#!/usr/bin/env python3
import subprocess, json, os
from datetime import datetime as dt

msg = open('/workspace/agents/info_officer/CRON_TASK_V3.txt').read()
script = f'''#!/bin/bash
openclaw cron add \\
  --name "情报官日报_每日05:00扫描" \\
  --cron "0 5 * * *" \\
  --tz "Asia/Shanghai" \\
  --session isolated \\
  --timeout-seconds 3600 \\
  --message "{msg.replace('"', '\\\\"').replace('\n', ' ')}" \\
  --announce \\
  --json
'''
# 写入临时脚本文件
with open('/tmp/make_cron.sh', 'w') as f:
    f.write(script)
os.chmod('/tmp/make_cron.sh', 0o755)

r = subprocess.run(['bash', '/tmp/make_cron.sh'], capture_output=True, text=True, timeout=30)
print('RC:', r.returncode)
# 找JSON
text = r.stdout
idx = text.find('{{' if '{{' in text else '{')
if idx < 0:
    idx = text.find('{{')
if idx < 0:
    print('NO JSON. ERR:', r.stderr[:300])
    print('OUT:', text[:400])
else:
    # 找第二个{
    pos = text.find('{', idx+1)
    if pos > 0 and pos - idx < 5:
        idx = pos
    try:
        d = json.loads(text[idx:])
        print('ID:', d.get('id','?'))
        nxt = d.get('state',{}).get('nextRunAtMs',0)
        print('NEXT:', nxt)
        if nxt:
            print('TIME:', dt.fromtimestamp(nxt/1000).strftime('%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        print('JSON ERR:', e)
        # 打印周围上下文
        print('NEAR:', text[max(0,idx-50):idx+200])
