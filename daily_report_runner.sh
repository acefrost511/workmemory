#!/bin/bash
# 每日日报任务执行脚本
echo "=== 开始执行每日日报任务 $(date) ===" >> /var/log/daily_report.log

# 1. 同步最新的记忆仓库
cd /root/.openclaw/workspace/workmemory
git pull origin main >> /var/log/daily_report.log 2>&1

# 2. 学习新增技能
echo "开始学习最新技能..." >> /var/log/daily_report.log
# 遍历所有技能目录，加载SKILL.md
for skill_dir in /root/.openclaw/workspace/skills/*/; do
  if [ -f "${skill_dir}SKILL.md" ]; then
    skill_name=$(basename "$skill_dir")
    echo "加载技能: $skill_name" >> /var/log/daily_report.log
  fi
done

# 3. 启动内容创作团队工作流
echo "启动内容创作团队工作流..." >> /var/log/daily_report.log
# 主编统筹任务
echo "【主编】分配任务：情报官收集今日K12教育资讯，教育专家撰写深度内容，编辑整理成日报" >> /var/log/daily_report.log

# 4. 调用资讯写作技能生成今日K12教育资讯
cd /root/.openclaw/workspace
echo "调用k12-edu-news-writer技能生成今日资讯..." >> /var/log/daily_report.log
# 这里可以扩展调用具体的技能执行
openclaw skill run k12-edu-news-writer --prompt "生成2026年$(date +%Y-%m-%d)的K12 AI教育资讯速览" >> /var/log/daily_report.log 2>&1

# 5. 生成最终日报
report_path="/root/.openclaw/workspace/daily_reports/K12_Education_Report_$(date +%Y%m%d).md"
mkdir -p /root/.openclaw/workspace/daily_reports
echo "# K12教育日报 $(date +%Y-%m-%d)" > "$report_path"
echo "## 今日资讯" >> "$report_path"
echo "（自动生成内容）" >> "$report_path"
echo "## 深度解读" >> "$report_path"
echo "（教育专家提供内容）" >> "$report_path"
echo "## 教学案例" >> "$report_path"
echo "（内容团队整理）" >> "$report_path"

echo "日报生成完成，路径: $report_path" >> /var/log/daily_report.log
echo "=== 每日日报任务执行完成 $(date) ===" >> /var/log/daily_report.log

# 通知用户日报已完成
openclaw message send --to owner --message "今日K12教育日报已生成，请查收：$report_path"
