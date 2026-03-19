#!/bin/bash
# 每日凌晨2点自动同步所有配置到GitHub
cd /root/.openclaw/workspace

# 拉取最新代码，自动解决冲突
git pull --rebase origin main

# 添加所有需要同步的核心文件
git add SOUL.md USER.md MEMORY.md memory/ *.sh skills/ *.md workmemory/

# 提交同步
git commit -m "daily sync: 自动同步配置与记忆文件 $(date +%Y-%m-%d)"

# 推送到远程仓库
git push origin main
