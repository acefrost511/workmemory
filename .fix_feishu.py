#!/usr/bin/env python3
"""一站式修复飞书连接+发送测试消息"""
import os, json, urllib.request, urllib.parse

APP_ID = "cli_a93fe76e9a781bc2"
APP_SECRET = "Kmo5JuCjzusvVQBQv674VbRVK7GDn74v"
USER_OPEN_ID = "ou_b60e71d5307978b7ac0151f377cdd512"
FEISHU_DIR = "/root/.openclaw/feishu"

# Step 1: 探索feishu目录结构
print("=== feishu目录内容 ===")
if os.path.exists(FEISHU_DIR):
    for f in os.listdir(FEISHU_DIR):
        print(f"  {f}")
        subpath = os.path.join(FEISHU_DIR, f)
        if os.path.isfile(subpath):
            try:
                print(f"    内容: {open(subpath).read()[:200]}")
            except:
                pass
else:
    print("  feishu目录不存在")

print("\n=== credentials目录内容 ===")
CRED_DIR = "/root/.openclaw/credentials"
if os.path.exists(CRED_DIR):
    for f in os.listdir(CRED_DIR):
        print(f"  {f}")
else:
    print("  credentials目录不存在")

# Step 2: 写feishu凭证文件
print("\n=== 写入feishu凭证 ===")
# OpenClaw飞书凭证格式：可能是accounts.json或default.json
feishu_cred_file = os.path.join(FEISHU_DIR, "accounts.json")
cred_data = {
    "default": {
        "appId": APP_ID,
        "appSecret": APP_SECRET
    }
}
try:
    with open(feishu_cred_file, 'w') as f:
        json.dump(cred_data, f, indent=2)
    print(f"  写入成功: {feishu_cred_file}")
except Exception as e:
    print(f"  写入失败: {e}")

# Step 3: 获取token并发送消息
print("\n=== 获取token ===")
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        resp = json.loads(r.read())
    token = resp.get("tenant_access_token", "")
    print(f"  Token: {token[:20]}...")
except Exception as e:
    print(f"  获取token失败: {e}")
    token = None

if token:
    print("\n=== 发送测试消息 ===")
    payload = {
        "receive_id": USER_OPEN_ID,
        "msg_type": "text",
        "content": json.dumps({"text": "小艾已重新连接飞书！消息发送测试成功。"})
    }
    msg_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    msg_data = json.dumps(payload).encode('utf-8')
    msg_req = urllib.request.Request(msg_url, data=msg_data, headers={
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {token}"
    })
    try:
        with urllib.request.urlopen(msg_req, timeout=10) as r:
            result = json.loads(r.read())
        print(f"  发送结果: {result}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  HTTP {e.code}: {body}")
    except Exception as e:
        print(f"  错误: {e}")
