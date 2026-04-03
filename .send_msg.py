#!/usr/bin/env python3
import urllib.request, json

APP_ID = "cli_a93fe76e9a781bc2"
APP_SECRET = "Kmo5JuCjzusvVQBQv674VbRVK7GDn74v"
OPEN_ID = "ou_b60e71d5307978b7ac0151f377cdd512"

# Get token
req = urllib.request.Request(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    data=json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode(),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req, timeout=10) as r:
    resp = json.loads(r.read())
token = resp["tenant_access_token"]
print(f"token ok: {token[:15]}...")

# Send text card
card = {
    "msg_type": "interactive",
    "card": {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "📋 今日简报 2026-04-03"},
            "template": "blue"
        },
        "elements": [
            {"tag": "div", "text": {"tag": "lark_md", "content": "**推送测试成功！**\n\n小艾已成功重新连接飞书。\n\n今日简报已推送，格式：10篇（9英文+1中文），请陛下逐篇标记✅触动/❌不触动。"}}
        ]
    }
}
msg_req = urllib.request.Request(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    data=json.dumps({"receive_id": OPEN_ID, "msg_type": "interactive", "content": json.dumps(card)}).encode("utf-8"),
    headers={"Content-Type": "application/json; charset=utf-8", "Authorization": f"Bearer {token}"}
)
try:
    with urllib.request.urlopen(msg_req, timeout=10) as r:
        result = json.loads(r.read())
    print(f"result: code={result.get('code')}, msg={result.get('msg')}")
except urllib.error.HTTPError as e:
    print(f"http error {e.code}: {e.read().decode()}")
except Exception as e:
    print(f"error: {e}")
