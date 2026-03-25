# 飞书互动卡片配置指南

**最后更新：2026-03-06 18:03**

---

## 目的
将周报/日报通过飞书互动卡片推送给王老师，提供更好的视觉体验。

---

## 卡片消息格式

### 完整结构
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "📊 K12 AI教育周报"
      }
    },
    "elements": [
      {
        "tag": "markdown",
        "content": "**时间范围**: 2026-02-27 至 2026-03-06\n\n**新研究**: 9篇\n**新产品**: 2个\n**新报告**: 10项\n\n**总计**: 21条资讯"
      }
    ]
  }
}
```

### 支持的 tag 类型

| tag | 用途 | 示例 |
|------|--------|------|
| `plain_text` | 标题、描述 | "📊 K12 AI教育周报" |
| `markdown` | 富文本内容 | "**时间范围**: 2026-02-27..." |

---

## 适用场景

✅ **适合使用卡片的消息**：
- 📊 日报/周报（数据展示）
- 📈 销售统计（表格）
- ✅ 任务完成通知
- 📋 审批流程

⚠️ **适合纯文本的消息**：
- 💬 对话问答
- 🔍 搜索结果
- 📝 一般通知

---

## 配置步骤

### 第一步：创建飞书企业自建应用

1. 登录飞书开放平台：https://open.feishu.cn/
2. 创建「企业自建应用」
3. 应用名称：AI Assistant（随意）
4. 应用描述：基于 OpenClaw 的智能助手

### 第二步：记录凭证信息

在「凭证与基础信息」页面记录：

| 字段 | 说明 |
|------|------|
| **App ID** | cli_xxxxxxxxxx（自动生成） |
| **App Secret** | 应用密钥（保密） |
| **Encrypt Key** | 加密密钥（保密） |

### 第三步：配置权限

在「权限管理」中开启以下权限：

| 权限 | 说明 |
|------|------|
| `im:message:send_as_bot` | 以机器人身份发消息 |
| `im:message:receive` | 接收消息 |
| `im:chat:readonly` | 读取群信息 |
| `wiki:wiki:readonly` | 读取知识库（如需要 RAG） |

### 第四步：配置 OpenClaw

在 `openclaw.json` 中添加飞书通道：

```json
{
  "channels": {
    "feishu": {
      "type": "feishu",
      "appId": "cli_xxxxxxxxxx",
      "appSecret": "your-app-secret",
      "verificationToken": "your-verification-token",
      "encryptKey": "your-encrypt-key"
    }
  }
}
```

### 第五步：启动 Gateway

```bash
openclaw gateway start
```

---

## 代码示例：周报卡片

```javascript
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "📊 K12 AI教育周报"
      }
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "**时间范围**: 2026-02-27 至 2026-03-06\n\n---\n\n## 📊 数据统计\n- **新研究**: 9篇\n- **新产品**: 2个\n- **新报告**: 10项\n- **总计**: 21条资讯\n\n---\n\n## 🔥 建议深度解读\n1. [研究] AI在K12课堂的实际效果（高优先）\n2. [产品] Khan Academy新AI功能\n3. [报告] UNESCO AI教育政策更新"
        }
      }
    }
  ]
}
```

---

## 注意事项

### ⚠️ Token 过期
- 飞书 `tenant_access_token` 有效期：2小时
- OpenClaw 内置了自动刷新逻辑
- 如果自己封装，需手动处理

### ⚠️ 消息去重
- 飞书偶尔会重复推送事件
- 建议用 `message_id` 做幂等性处理
- 避免回复重复消息

### ⚠️ 大群优化
- 超过500人的群，消息量大时响应变慢
- 建议对大群设置消息过滤规则
- 只处理 `@mention` 触发的消息

---

## 成本估算

| 项目 | 月费用 |
|------|--------|
| OpenClaw 运行时 | 免费（开源） |
| LLM API 调用 | ¥200-500（取决于消息量） |
| 飞书开放平台 | 免费（企业自建） |
| **合计** | ¥200-500/月 |

---

## 下一步

**需要王老师提供的信息**：
- [ ] 是否需要我帮助创建飞书应用
- [ ] App ID
- [ ] App Secret
- [ ] Verification Token
- [ ] Encrypt Key

---

*配置人: 管家小艾*
*来源: 飞书开放平台技术文档 + OpenClaw 集成指南*
