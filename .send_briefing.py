#!/usr/bin/env python3
"""每日简报发送脚本 - 使用文字消息格式（稳定版）"""
import urllib.request, json, sys

APP_ID = "cli_a93fe76e9a781bc2"
APP_SECRET = "Kmo5JuCjzusvVQBQv674VbRVK7GDn74v"
USER_OPEN_ID = "ou_3738b37d4ed758b00067bbe8feddaeec"

def get_token():
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())["tenant_access_token"]

def send(token, text):
    payload = {
        "receive_id": USER_OPEN_ID,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8", "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        result = json.loads(r.read())
    return result

# 简报内容
msg = """📋 今日简报 2026-04-03 | 9英文+1中文

━━━━━━━━━━━━━━━━━━

【01】对话式教学智能体促进中学生编程学习表现实证研究
作者：傅骞，赵亚宁，甘甜甜，郑娅峰 | 电化教育研究 2026年第3期

这篇在说什么：初中生分三组——仅用AI出题、AI出题+追问、AI出题+追问+引导。一学期后，第三组编程测验和开放性问题显著优于前两组，题目越复杂差距越大。追问+引导才是最优解，不是增加练习量。

为什么值得注意：AI是在老师顾不过来的追问和引导上补位，不是在替代老师。教老师用AI设计追问，比教老师用AI出题有价值十倍。

记住一句话：AI追问加引导一起用效果最好，别把AI只当成答题批改工具。

━━━━━━━━━━━━━━━━━━

【02】生成式AI技术与教育成果：元分析
原标题：Generative AI Technologies and Educational Outcomes: A Meta-Analysis
作者：Ying Dong | Humanities and Social Sciences 2026年3月

这篇在说什么：元分析综合多项实证研究，GAI在四个维度优于传统方法：学业成绩、高阶思维能力（Higher-Order Thinking Skills）、写作能力、反馈质量。

为什么值得注意：这是目前最系统回答"AI教育有没有用"的研究，结论是肯定。高阶思维和写作能力效果最显著——AI辅助不只是更快，而是更深。

记住一句话：元分析最系统回答：AI教育确实有效，尤其在高阶思维和写作上，不是替代思考而是扩展思考。

━━━━━━━━━━━━━━━━━━

请回复「标记完毕」或逐篇标记触动/不触动。"""

token = get_token()
result = send(token, msg)
print(f"发送结果: code={result.get('code')}, msg={result.get('msg')}")
