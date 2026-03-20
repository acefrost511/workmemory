#!/bin/bash
# 每日K12教育精选资讯生成脚本 每天凌晨5点自动运行
cd /root/.openclaw/workspace

# 1. 创建当日资讯存储文件
output_file="daily_news_$(date +%Y%m%d).md"
echo "### $(date +%Y年%m月%d日) K12 AI教育精选资讯速览" > $output_file
echo "" >> $output_file

# 2. 调用情报官Agent启动资讯搜索任务，明确要求搜索完成后调用主编协作
openclaw sessions_spawn --runtime subagent --label "情报官" --mode run --task "
【任务要求】
1. 启动10个Agent并行搜索近24小时发布的K12 AI教育相关资讯，覆盖9本英文核心期刊+10本中文核心期刊
2. 搜索结果要求：总资讯≥40篇，其中论文占比≥70%，仅保留最近90天内的北京时间内容，过滤旧内容
3. 搜索完成后，输出包含7个必填字段的资讯列表：序号、标题、时间、简介、来源、优先级、是否深度解读，保存为文件：/root/.openclaw/workspace/daily_reports/raw_news_$(date +%Y%m%d).md
4. 搜索完成后，**必须调用zhubian（主编）Agent**，将上述文件路径传递给主编，要求主编执行以下操作：
   a. 从搜索结果中筛选10-15条优质内容，严格符合70%研究/20%报告/10%产品的比例要求
   b. 按照k12-edu-news-writer技能规范生成完整的资讯速览，包含标题区、导读区、正文区
   c. 完成后将最终内容写入$output_file，并通知总调度提交给陛下
【权限说明】你已被授予subagent调用权限，可以直接调用zhubian Agent执行后续步骤
"

# 3. 等待结果生成后自动推送给陛下
sleep 1800
if [ -s "$output_file" ]; then
  openclaw message send --channel feishu --target user:ou_3738b37d4ed758b00067bbe8feddaeec --message "$(cat $output_file)"
fi

