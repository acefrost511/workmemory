#!/usr/bin/env python3
"""
飞书消息发送脚本
绕过OpenClaw channel配置，直接调用飞书API发送消息
已验证可用（2026-04-03）
"""
import urllib.request, json, sys, os

# ===== 配置 =====
APP_ID = "cli_a93fe76e9a781bc2"
APP_SECRET = "Kmo5JuCjzusvVQBQv674VbRVK7GDn74v"
# 陛下的正确open_id
USER_OPEN_ID = "ou_3738b37d4ed758b00067bbe8feddaeec"
# ================

def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        resp = json.loads(r.read())
    if resp.get("code") != 0:
        print(f"获取token失败: {resp}")
        sys.exit(1)
    return resp["tenant_access_token"]

def send_text(token, text, user_open_id=None):
    uid = user_open_id or USER_OPEN_ID
    payload = {
        "receive_id": uid,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {token}"
    })
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read())
    return result

def send_card(token, title, elements, user_open_id=None):
    """发送飞书互动卡片"""
    uid = user_open_id or USER_OPEN_ID
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": "blue"
        },
        "elements": elements
    }
    payload = {
        "receive_id": uid,
        "msg_type": "interactive",
        "content": card  # 直接传dict，不要json.dumps
    }
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {token}"
    })
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read())
    return result

def send_briefing(token, title, articles):
    """发送每日简报（富文本卡片格式）"""
    uid = USER_OPEN_ID
    # 构建卡片元素
    elements = []
    for art in articles:
        art_type = art.get("type", "text")
        if art_type == "divider":
            elements.append({"tag": "hr"})
        elif art_type == "title":
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": art["text"], "lines": 1}
            })
        elif art_type == "text":
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": art["text"]}
            })
        elif art_type == "footer":
            elements.append({
                "tag": "note",
                "elements": [{"tag": "plain_text", "content": art["text"]}]
            })
    
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": "blue"
        },
        "elements": elements
    }
    payload = {
        "receive_id": uid,
        "msg_type": "interactive",
        "content": json.dumps(card)
    }
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {token}"
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        result = json.loads(r.read())
    return result

if __name__ == "__main__":
    token = get_token()
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "test":
            result = send_text(token, "🔔 飞书连接测试\n\n小艾已成功通过Python直连发送消息。")
            print(f"发送结果: code={result.get('code')}, msg={result.get('msg')}")
        elif cmd == "card":
            result = send_card(token, "📋 测试卡片", [
                {"type": "text", "text": "**测试标题**\n这是测试内容"}
            ])
            print(f"卡片发送: code={result.get('code')}, msg={result.get('msg')}")
    else:
        result = send_text(token, "🔔 飞书Python脚本测试成功！")
        print(f"发送结果: code={result.get('code')}, msg={result.get('msg')}")
