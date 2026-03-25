# 飞书互动卡片模板

**创建时间**：2026-03-06 18:15
**创建人**：管家小艾

---

## 日报/周报卡片模板

### 日报卡片模板
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "📊 K12 AI教育日报"
      }
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "## 📋 数据统计\n\n**时间范围**：2026-03-06\n\n| 指标 | 数值 |\n|------|------|\n| 新研究 | 12篇 |\n| 新产品 | 3个 |\n| 新报告 | 8项 |\n| **总计** | 23条 |\n\n---\n\n## 🔥 高优先级内容\n\n1. [研究] AI在K12课堂的实际效果\n   - 来源：Computers & Education\n   - 发表时间：2026-03-05\n   - 摘要：一项针对120所中学的研究显示...\n\n2. [产品] Khan Academy推出新AI功能\n   - 来源：Khan Academy官网\n   - 发表时间：2026-03-05\n   - 摘要：个性化学习路径...\n\n---\n\n## 📈 全文链接\n[查看完整日报](https://your-link.com/daily-report-20260306)"
        }
      }
    ]
  }
}
```

### 周报卡片模板
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
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "## 📋 数据统计\n\n**时间范围**：2026-02-27 至 2026-03-06\n\n| 指标 | 数值 |\n|------|------|\n| 新研究 | 9篇 |\n| 新产品 | 2个 |\n| 新报告 | 10项 |\n| **总计** | 21条 |\n\n---\n\n## 🔥 高优先级内容\n\n1. [研究] AI在K12课堂的实际效果\n2. [产品] Khan Academy新AI功能\n3. [报告] UNESCO AI教育政策\n\n---\n\n## 📈 全文链接\n[查看完整周报](https://your-link.com/weekly-report-20260306)"
        }
      }
    ]
  }
}
```

---

## 任务完成卡片模板
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "✅ 任务完成"
      }
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "**任务名称**：K12 AI教育日报搜索\n\n**执行状态**：✅ 已完成\n\n**执行时间**：14:03 - 15:10\n\n**结果**：成功获取78条资讯\n\n---\n\n*微臣已记录到任务执行日志*"
        }
      }
    ]
  }
}
```

---

## 资源监控卡片模板
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "📊 资源监控"
      }
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "**检查时间**：2026-03-06 17:00\n\n| 指标 | 数值 | 状态 |\n|------|------|------|\n| 内存 | 1.16GB/2.37GB (49.1%) | ✓ 正常 |\n| 磁盘 | 155GB/228GB (68%, 剩余7.3GB) | ✓ 正常 |\n| 工作区 | 748KB | ✓ 正常 |"
        }
      }
    ]
  }
}
```

---

## 使用说明

### 什么时候使用卡片？
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

## OpenClaw 配置方式

### 方式 A：通过 openclaw.json 配置
在 `openclaw.json` 中设置：
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

### 方式 B：使用环境变量
```bash
export FEISHU_APP_ID="cli_xxxxxxxxxx"
export FEISHU_APP_SECRET="your-app-secret"
export FEISHU_VERIFICATION_TOKEN="your-verification-token"
export FEISHU_ENCRYPT_KEY="your-encrypt-key"
```

---

## 需要的信息

要配置飞书互动卡片，需要陛下提供以下信息：

### 必需信息
- [ ] **App ID**：从飞书开放平台获取
- [ ] **App Secret**：从飞书开放平台获取
- [ ] **Verification Token**：从飞书开放平台获取
- [ ] **Encrypt Key**：从飞书开放平台获取

### 可选信息
- [ ] 是否需要自定义卡片样式
- [ ] 是否需要配置按钮（如"查看详情"）
- [ ] 是否需要配置其他元素（图片、表格等）

---

## 下一步

请陛下：
1. 登录飞书开放平台：https://open.feishu.cn/
2. 创建或找到现有的"企业自建应用"
3. 在「凭证与基础信息」页面复制 App ID 和 App Secret
4. 在「事件订阅」获取 Verification Token 和 Encrypt Key
5. 将上述信息发送给微臣

收到信息后，微臣将立即：
1. 配置 `openclaw.json`
2. 重启 Gateway 服务
3. 测试发送一张示例卡片
4. 将日报/周报切换为卡片模式

---

*模板创建人: 管家小艾*
*来源: 飞书开放平台技术文档*
