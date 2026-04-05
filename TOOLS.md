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

## 高频调用防护规则（2026-04-05新增）

**核心原则：先规划，再执行，禁止边想边改。**

修改多个相关配置项时（cron/gateway/文件等）：
1. 先在脑中/草稿区列出所有需要改动的项
2. 合并为一次工具调用完成，不逐个调用
3. 调用失败后等待片刻，不立即重试
4. 严禁在同一个工具上连续调用超过2次

**反面案例**：对同一个cron任务连续6次update/patch，每次只改一个字段 → 触发高频保护
**正确做法**：把payload+timeout+delivery三项合并，一次update完成

## Cron配置关键知识（2026-04-05更新）

**isolated session硬上限：平台对isolated agent session的默认timeout = 600秒（10分钟）**
**intel cron自身timeout：120秒（spawn完成即退出，不等结果）**

**Spawn超时规则（陛下2026-04-05确立，铁律）**：
- intel agent spawn：runTimeoutSeconds=600（600秒平台硬上限，留5%缓冲）
- 其他所有spawn（洞察/文章/审核等）：runTimeoutSeconds=480（8分钟，留20%缓冲）
- intel_01~05 cron(a4b3f1ed)：spawn timeout 600秒，cron自身120秒
- intel_06~12 cron(0510)：spawn timeout 600秒，cron自身120秒
- 审核调度器 dispatcher(eabfa507)：every 2分钟 × 20次空队列停止，timeout 300秒

**审核调度器重建（2026-04-05）**：
- 旧dispatcher(reviewer-plan-b-dispatcher)：anchor时间错位导致04:30批次漏审，已删除
- 新dispatcher(eabfa507)：*/2分钟 cron，全天候监控.pending/队列，连续20次空则自停
- intel写入后立即调用review.py，dispatcher作兜底防护
来源：陛下2026-04-05指令
