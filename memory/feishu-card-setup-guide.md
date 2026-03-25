# 飞书互动卡片配置 - 详细操作手册

**创建时间**：2026-03-06 20:05
**目的**：逐步指导陛下完成飞书应用配置和卡片消息发送测试

---

## 📋 操作清单

| 步骤 | 任务 | 状态 |
|------|------|------|
| 第1步 | 创建飞书企业自建应用 | ⏳ 待执行 |
| 第2步 | 配置应用权限 | ⏳ 待执行 |
| 第3步 | 记录4个关键信息 | ⏳ 待执行 |
| 第4步 | 配置 OpenClaw 飞书通道 | ⏳ 待执行 |
| 第5步 | 重启 Gateway 服务 | ⏳ 待执行 |
| 第6步 | 测试发送卡片消息 | ⏳ 待执行 |

---

## 第1步：创建飞书企业自建应用（5分钟）

### 1.1 登录飞书开放平台
```
https://open.feishu.cn/
```

### 1.2 创建企业自建应用
1. 点击「创建企业自建应用」按钮
2. 填写应用信息：
   - **应用名称**：K12 AI Assistant（或随意填写）
   - **应用描述**：基于 OpenClaw 的智能助手，用于日报/周报推送
   - **应用图标**：上传 Logo 图片或使用默认

3. 点击「创建」按钮

### 1.3 记录应用创建成功页面
- 页面会显示「创建成功」
- 记录以下信息备用：
  - App ID（会自动显示）
  - App Secret（创建后可查看）

---

## 第2步：配置应用权限（3分钟）

### 2.1 进入权限管理
1. 在应用页面，点击左侧菜单「权限管理」
2. 你会看到权限配置列表

### 2.2 开启以下权限（必须全部开启）

| 权限名称 | 开关 | 说明 |
|----------|------|------|
| im:message:send_as_bot | ✅ 打开 | 以机器人身份发送消息 |
| im:message:receive | ✅ 打开 | 接收群消息 |
| im:chat:readonly | ✅ 打开 | 读取群信息 |
| wiki:wiki:readonly | ✅ 打开 | 读取知识库（可选，RAG场景需要） |

### 2.3 保存权限配置
1. 点击「保存」或「保存变更」按钮
2. 等待几秒钟，保存成功会有提示

---

## 第3步：记录4个关键信息（2分钟）

### 3.1 获取 App ID 和 App Secret

1. 点击左侧菜单「凭证与基础信息」
2. 记录以下信息（请复制到记事本）：

```
App ID: cli_xxxxxxxxxx  （类似这样的格式）
App Secret: ********************************  （一长串密钥）
```

**⚠️ 重要**：
- App Secret 只在创建时显示一次
- 离开页面后无法再次查看
- **必须立即记录**，否则需要重新创建应用

### 3.2 获取 Verification Token 和 Encrypt Key

1. 点击左侧菜单「事件订阅」
2. 记录以下信息：

```
Verification Token: xxxxxxx-xxxx-xxxx-xxxx  （长字符串）
Encrypt Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxx （长字符串）
```

**⚠️ 重要**：
- 这两个值每次进入页面都显示
- 但建议一起记录，避免遗漏

### 3.3 信息汇总清单

请确认已获取并记录以下4个信息：

- [ ] App ID
- [ ] App Secret
- [ ] Verification Token
- [ ] Encrypt Key

**完成后请回复："信息已记录完毕"**

---

## 第4步：配置 OpenClaw 飞书通道（5分钟）

### 4.1 检查 OpenClaw 配置文件

在终端运行以下命令：

```bash
cat ~/.easyclaw/openclaw.json
```

如果文件不存在，创建它：

```bash
mkdir -p ~/.easyclaw
touch ~/.easyclaw/openclaw.json
```

### 4.2 编辑 openclaw.json

使用你喜欢的编辑器（nano、vim、VS Code等）：

```bash
nano ~/.easyclaw/openclaw.json
```

### 4.3 添加飞书通道配置

在 `channels` 数组中添加以下配置：

```json
{
  "channels": {
    "feishu": {
      "type": "feishu",
      "appId": "cli_xxxxxxxxxx",
      "appSecret": "your-app-secret-here",
      "verificationToken": "your-verification-token-here",
      "encryptKey": "your-encrypt-key-here"
    }
  }
}
```

**完整示例**（替换为你的实际值）：

```json
{
  "version": 1,
  "agentDefaults": {
    "env": {
      "OPENAI_API_KEY": "sk-xxx",
      "ANTHROPIC_API_KEY": "sk-ant-xxx"
    }
  },
  "channels": {
    "feishu": {
      "type": "feishu",
      "appId": "cli_xxxxxxxxxx",
      "appSecret": "your-app-secret-here",
      "verificationToken": "your-verification-token-here",
      "encryptKey": "your-encrypt-key-here"
    }
  }
}
```

**⚠️ 注意**：
- 必须用第3步记录的4个实际值替换示例中的占位符
- 确保JSON格式正确，逗号、引号都要正确
- 保存前确认没有拼写错误

### 4.4 保存并退出

在 nano 编辑器中：
1. 按 `Ctrl+O` 保存
2. 按 `Ctrl+X` 退出

---

## 第5步：重启 Gateway 服务（1分钟）

### 5.1 运行重启命令

在终端运行：

```bash
easyclaw gateway restart
```

### 5.2 确认重启成功

你应该看到类似这样的输出：

```
✓ Gateway config-patch ok (config.patch)
```

如果没有看到成功提示，说明配置文件有错误，请检查：
1. JSON 语法是否正确
2. 4个飞书配置信息是否正确填写

---

## 第6步：测试发送卡片消息（2分钟）

### 6.1 准备测试消息

准备一条测试消息，使用互动卡片格式：

```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "📋 测试消息"
      }
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "**测试时间**：2026-03-06 20:00\n\n**消息类型**：互动卡片\n\n**状态**：✅ 配置完成"
        }
      }
    ]
  }
}
```

### 6.2 通过飞书发送

有两种方式：

**方式 A：通过飞书群（推荐）**
1. 打开飞书客户端
2. 找到你想要测试的群
3. 在输入框输入测试消息
4. 微臣将自动将消息通过互动卡片格式发送给你

**方式 B：通过命令行（用于调试）**
如果你想让微臣通过 OpenClaw 直接发送，可以告诉微臣发送测试消息。

### 6.3 验证卡片效果

成功发送后，你应该在飞书中看到：
- 📋 一个漂亮的卡片
- 标题："测试消息"
- 内容："**测试时间**：2026-03-06 20:00..."
- 卡片有结构化的布局，比纯文本更美观

---

## ⚠️ 常见问题排查

### 问题 1：发送失败，提示权限不足

**原因**：飞书应用权限没有正确开启

**解决**：
1. 回到飞书开放平台
2. 检查「权限管理」页面
3. 确认以下权限已开启：
   - im:message:send_as_bot
   - im:message:receive
4. 保存后重启 Gateway

---

### 问题 2：收到纯文本，不是卡片

**原因**：
1. JSON 格式有错误
2. 飞书 API 版本问题
3. 配置不完整

**解决**：
1. 检查 openclaw.json 中的配置是否完整
2. 确认 4 个飞书配置值都已正确填写
3. 查看 Gateway 日志：`tail -f /tmp/easyclaw/easyclaw-2026-03-06.log`

---

### 问题 3：发送非常慢或超时

**原因**：网络问题或飞书 API 限流

**解决**：
1. 检查网络连接
2. 等待几分钟后重试
3. 如果持续失败，联系飞书技术支持

---

## 📊 完成检查清单

完成所有步骤后，请确认：

- [ ] 飞书企业自建应用已创建
- [ ] 4个权限已开启（发送、接收、读取群聊、知识库）
- [ ] App ID 已记录
- [ ] App Secret 已记录
- [ ] Verification Token 已记录
- [ ] Encrypt Key 已记录
- [ ] openclaw.json 已更新配置
- [ ] Gateway 已重启
- [ ] 测试卡片消息已成功发送

---

## 🎯 配置完成后

一旦配置完成，微臣可以：

✅ **日报/周报通过卡片推送**
- 更美观的视觉体验
- 结构化数据展示
- 支持按钮交互（可选扩展）

✅ **任务完成通知**
- 卡片格式更专业
- 信息层次更清晰

---

## 📞 需要帮助？

如果遇到任何问题，请：

1. 截图错误信息发送给微臣
2. 描述卡在哪一步
3. 说明具体的错误提示

微臣会根据错误信息提供针对性解决方案。

---

*手册创建人: 管家小艾*
*版本: v1.0*
*最后更新: 2026-03-06 20:05*
