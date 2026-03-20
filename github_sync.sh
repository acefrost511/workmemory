#!/bin/bash
# 每日GitHub自动同步脚本，每日凌晨2点执行
cd /root/.openclaw/workspace
git pull --rebase origin master
git add .
git commit -m "$(date +%Y-%m-%d) 自动同步：当日配置更新、业务产出、记忆文件"
git push origin master
