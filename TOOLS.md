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

### Example
❌ **Bad**: Guess the text based on memory
✅ **Good**: `read` the file → copy exact text → `edit`

### 定时
当用户要求设置提醒或定时任务时，使用 cron.add 工具。
示例：用户说"30分钟后提醒我开会"，你应该调用 cron.add，
设置 schedule.at 为当前时间+30分钟的 ISO 8601 时间戳，
payload.kind 设为 "agentTurn"，payload.message 设为提醒内容。


