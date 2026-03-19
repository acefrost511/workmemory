#!/bin/bash
# 每日自我反思执行脚本 每天凌晨3点自动运行
cd /root/.openclaw/workspace

# 步骤1：获取过去24小时的聊天记录和操作日志
echo "### $(date +%Y-%m-%d) 自我反思报告" > daily_reflection_$(date +%Y%m%d).md
echo "" >> daily_reflection_$(date +%Y%m%d).md
echo "#### 📌 今日问题梳理" >> daily_reflection_$(date +%Y%m%d).md
# 从历史记录提取陛下提出的不满意点、修正要求
grep -r "错误\|问题\|教训\|不满意\|改进" memory/$(date +%Y-%m-%d).md >> daily_reflection_$(date +%Y%m%d).md 2>/dev/null || echo "无显性问题" >> daily_reflection_$(date +%Y%m%d).md

echo "" >> daily_reflection_$(date +%Y%m%d).md
echo "#### 🔧 规则优化更新" >> daily_reflection_$(date +%Y%m%d).md
# 提取今日修改的SOUL.md内容
git diff SOUL.md $(git log -1 --format=%H -- SOUL.md) | grep "+[^+]" | tail -n +2 >> daily_reflection_$(date +%Y%m%d).md 2>/dev/null || echo "无规则更新" >> daily_reflection_$(date +%Y%m%d).md

echo "" >> daily_reflection_$(date +%Y%m%d).md
echo "#### 📚 今日学习收获" >> daily_reflection_$(date +%Y%m%d).md
# 提取今日经验教训
grep -r "经验\|收获\|学到" memory/$(date +%Y-%m-%d).md >> daily_reflection_$(date +%Y%m%d).md 2>/dev/null || echo "无新增经验" >> daily_reflection_$(date +%Y%m%d).md

# 步骤2：自动同步到GitHub
git add SOUL.md USER.md memory/ daily_reflection_$(date +%Y%m%d).md
git commit -m "daily reflection: $(date +%Y-%m-%d) 自动更新规则和反思报告"
git push origin main

# 步骤3：调用自我提升技能完成自我进化
openclaw skills run self-improvement --context daily_reflection_$(date +%Y%m%d).md

# 步骤4：调用消息接口发送报告给陛下（后续完善发送逻辑）
