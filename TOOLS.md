# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics - the stuff that's unique to this environment.

## edit tool - Important Gotcha

### Problem
`edit` tool **requires exact text match including all whitespace and newlines**. If the oldText doesn't match _exactly_, the edit will fail.

### Solution
1. **Before calling `edit`**: Always `read` the current file content to get the *exact* text
2. **Copy/paste exactly**: Do not guess or reformat - copy the exact text including:
   - All spaces
   - All newlines (line breaks)
   - Leading/trailing empty lines
3. **If in doubt**: Use `read` to read the file again, then copy the exact text
4. **If still failing**: Use `write` to rewrite the entire file instead of `edit`

### 定时
当用户要求设置提醒或定时任务时，使用 cron.add 工具。
示例：用户说"30分钟后提醒我开会"，你应该调用 cron.add，
设置 schedule.at 为当前时间+30分钟的 ISO 8601 时间戳，
payload.kind 设为 "agentTurn"，payload.message 设为提醒内容。

## ClawHub镜像（2026-04-02新增）

**官方镜像站**：https://mirror-cn.clawhub.com

**clawhub CLI路径**：
/tmp/.tool-cache/npm/_npx/a92a6dbcf543fba6/node_modules/.bin/clawhub

**使用方式**：
clawhub search [关键词] --base-url https://mirror-cn.clawhub.com
或设置环境变量：CLAWHUB_BASE_URL=https://mirror-cn.clawhub.com

**搜索语法**：以后搜索skills用镜像站，不用原生官方站

## Cron配置关键知识（2026-04-02从定时任务可靠性计划迁移）

**isolated session硬上限：平台对isolated agent session的默认timeout = 600秒（10分钟）**
**解决方案：cron payload必须显式设置timeoutSeconds=3600，否则超过10分钟自动被kill**

来源：/workspace/agents/定时任务可靠性计划.md（保留）
