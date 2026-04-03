#!/usr/bin/env python3
"""调试版：发送飞书消息"""
import urllib.request
import json

APP_ID = "cli_a93fe76e9a781bc2"
APP_SECRET = "Kmo5JuCjzusvVQBQv674VbRVK7GDn74v"

# 获取token
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=10) as r:
    resp = json.loads(r.read())
token = resp["tenant_access_token"]
print(f"Token获取成功: {token[:20]}...")

# 发送消息（用正确格式）
# Feishu API要求content是JSON字符串
msg_content = {"text": "飞书直连测试成功！小艾已重新连接飞书。"}
payload = {
    "receive_id": "ou_b60e71d5307978b7ac0151f377cdd512",
    "msg_type": "text",
    "content": json.dumps(msg_content)  # 这里不用双重编码
}
msg_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
msg_data = json.dumps(payload).encode('utf-8')
print(f"发送payload: {payload}")

msg_req = urllib.request.Request(msg_url, data=msg_data, headers={
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": f"Bearer {token}"
})
try:
    with urllib.request.urlopen(msg_req, timeout=10) as r:
        result = json.loads(r.read())
        print(f"发送结果: {result}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"HTTP错误 {e.code}: {body}")
except Exception as e:
    print(f"错误: {e}")
