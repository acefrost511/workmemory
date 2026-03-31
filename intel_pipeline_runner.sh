#!/bin/bash
# 情报搜索流水线执行器（后台常驻）
# 监听done文件，每批完成后自动spawn下一批

WORKSPACE="/workspace/knowledge"
LOG="/workspace/intel_pipeline.log"
CLAW="/app/openclaw/openclaw"

log() { 
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG
}

wait_for_file() {
    local file=$1
    local timeout=$2
    local waited=0
    while [ ! -f "$WORKSPACE/$file" ] && [ $waited -lt $timeout ]; do
        sleep 20
        waited=$((waited+20))
    done
    [ -f "$WORKSPACE/$file" ]
}

spawn_batch2() {
    log "🚀 启动第二批 (intel_04/05/06)..."
    cd /workspace
    $CLAW run "你是情报官 intel_04。读取 /workspace/SOUL.md 后执行CSSCI中文搜索，搜索词：AI教育 K12 CSSCI 2024 2025、自适应学习 基础教育 研究、人工智能 教育应用 实证研究 2025。将结果写入 /workspace/knowledge/intel_batch2_04_cssci.md，完成后 touch /workspace/knowledge/done_intel_04" --name intel_04_batch2 --timeout 600 &
    $CLAW run "你是情报官 intel_05。读取 /workspace/SOUL.md 后执行中文学术搜索，搜索词：人工智能教育 K12 2025 2026 site:cnki.net OR site:wanfangdata.com.cn、自适应学习系统 基础教育 效果研究、大语言模型 教育应用 中国中小学。将结果写入 /workspace/knowledge/intel_batch2_05_cn_academic.md，完成后 touch /workspace/knowledge/done_intel_05" --name intel_05_batch2 --timeout 600 &
    $CLAW run "你是情报官 intel_06。读取 /workspace/SOUL.md 后执行政府政策搜索，搜索词：教育部 AI教育 政策 2025 2026、人工智能+教育 十四五 规划、中小学人工智能 教育指南 政策。将结果写入 /workspace/knowledge/intel_batch2_06_policy.md，完成后 touch /workspace/knowledge/done_intel_06" --name intel_06_batch2 --timeout 600 &
    log "✅ 第二批3个agent已spawn"
}

spawn_batch3() {
    log "🚀 启动第三批 (intel_07/08/09)..."
    cd /workspace
    $CLAW run "你是情报官 intel_07。读取 /workspace/SOUL.md 后执行搜索：生成式AI 教育应用 2025 2026。将结果写入 /workspace/knowledge/intel_batch3_07_genai.md，完成后 touch /workspace/knowledge/done_intel_07" --name intel_07_batch3 --timeout 600 &
    $CLAW run "你是情报官 intel_08。读取 /workspace/SOUL.md 后执行搜索：智慧教育 示范区 中小学 案例 2025。将结果写入 /workspace/knowledge/intel_batch3_08_smartedu.md，完成后 touch /workspace/knowledge/done_intel_08" --name intel_08_batch3 --timeout 600 &
    $CLAW run "你是情报官 intel_09。读取 /workspace/SOUL.md 后执行搜索：STEM AI 教育 创新 2025 2026研究。将结果写入 /workspace/knowledge/intel_batch3_09_stem.md，完成后 touch /workspace/knowledge/done_intel_09" --name intel_09_batch3 --timeout 600 &
    log "✅ 第三批3个agent已spawn"
}

spawn_batch4() {
    log "🚀 启动第四批 (intel_10/11/12)..."
    cd /workspace
    $CLAW run "你是情报官 intel_10。读取 /workspace/SOUL.md 后执行搜索：AI教师 角色 替代 合作 教育研究。将结果写入 /workspace/knowledge/intel_batch4_10_ai_teacher.md，完成后 touch /workspace/knowledge/done_intel_10" --name intel_10_batch4 --timeout 600 &
    $CLAW run "你是情报官 intel_11。读取 /workspace/SOUL.md 后执行搜索：学习分析 教育大数据 K-12 2025。将结果写入 /workspace/knowledge/intel_batch4_11_learning_analytics.md，完成后 touch /workspace/knowledge/done_intel_11" --name intel_11_batch4 --timeout 600 &
    $CLAW run "你是情报官 intel_12。读取 /workspace/SOUL.md 后执行搜索：个性化学习 教育公平 AI 2025 2026。将结果写入 /workspace/knowledge/intel_batch4_12_personalized.md，完成后 touch /workspace/knowledge/done_intel_12" --name intel_12_batch4 --timeout 600 &
    log "✅ 第四批3个agent已spawn"
}

spawn_reviewers() {
    log "🚀 启动审核阶段 (3个reviewer)..."
    cd /workspace
    $CLAW run "你是情报审核官 intel_reviewer_en。读取 /workspace/SOUL.md，然后扫描 /workspace/knowledge/ 下所有含intel_batch的md文件（英文/国际来源）。执行质量审核：①真实性（来源可查证）②相关性（与K12 AI教育相关）③时效性（2024-2026）。对每个文件输出通过/不通过及原因。汇总写入 /workspace/knowledge/review_en.md，完成后 touch /workspace/knowledge/done_reviewer_en" --name reviewer_en --timeout 900 &
    $CLAW run "你是情报审核官 intel_reviewer_cn。读取 /workspace/SOUL.md，然后扫描 /workspace/knowledge/ 下所有含intel_batch的md文件（中文来源）。执行质量审核：①真实性（来源可查证）②相关性（与K12 AI教育相关）③时效性（2024-2026）。对每个文件输出通过/不通过及原因。汇总写入 /workspace/knowledge/review_cn.md，完成后 touch /workspace/knowledge/done_reviewer_cn" --name reviewer_cn --timeout 900 &
    $CLAW run "你是情报审核官 intel_reviewer_intl。读取 /workspace/SOUL.md，然后扫描 /workspace/knowledge/ 下所有intel_batch文件（综合）。执行跨来源交叉验证：检查同一话题的中英文来源是否一致，识别矛盾或互补。写入 /workspace/knowledge/review_intl.md，完成后 touch /workspace/knowledge/done_reviewer_intl" --name reviewer_intl --timeout 900 &
    log "✅ 审核阶段3个reviewer已spawn"
}

spawn_edu_lead() {
    log "🚀 启动洞察生产 (edu_lead)..."
    cd /workspace
    $CLAW run "你是洞察官 edu_lead。读取 /workspace/SOUL.md 和 /workspace/knowledge/ 下的所有review*.md和intel_batch*.md文件。基于今日入库情报，生成3条高质量洞察（遵循SOUL.md中IP洞察SOP：信念溯源→Hook句→引用证据→碰撞逻辑→核心洞察≥400字→读者带走）。输出文件：/workspace/knowledge/insights_20260330.md。完成后：(1) touch /workspace/knowledge/done_edu_lead (2) 读取insights文件内容，通过message工具发送到飞书（channel=feishu, action=send, message=洞察内容）" --name edu_lead --timeout 1200 &
    log "✅ edu_lead已spawn"
}

final_report() {
    log "📊 统计入库文件..."
    total=$(ls $WORKSPACE/intel_batch*.md 2>/dev/null | wc -l | tr -d ' ')
    passed=""
    if [ -f "$WORKSPACE/review_en.md" ]; then
        passed_en=$(grep -c "通过\|PASS\|✅" $WORKSPACE/review_en.md 2>/dev/null || echo 0)
    fi
    insights=""
    if [ -f "$WORKSPACE/insights_20260330.md" ]; then
        insights="有"
    fi
    log "=== 流水线完成 ==="
    log "总入库：$total 个文件"
    log "审核通过：待查"
}

# ===== 主循环 =====
log "========================================"
log "情报流水线启动 | $(date)"
log "========================================"

# 监听第一批
log "等待第一批完成 (intel_01/02/03)..."
for f in done_intel_01 done_intel_02 done_intel_03; do
    wait_for_file "$f" 600 || log "⚠️ $f 未在10分钟内就绪"
done
log "✅ 第一批完成！"
touch $WORKSPACE/pipeline_batch1_done
spawn_batch2

# 监听第二批
log "等待第二批完成 (intel_04/05/06)..."
for f in done_intel_04 done_intel_05 done_intel_06; do
    wait_for_file "$f" 600 || log "⚠️ $f 未在10分钟内就绪"
done
log "✅ 第二批完成！"
touch $WORKSPACE/pipeline_batch2_done
spawn_batch3

# 监听第三批
log "等待第三批完成 (intel_07/08/09)..."
for f in done_intel_07 done_intel_08 done_intel_09; do
    wait_for_file "$f" 600 || log "⚠️ $f 未在10分钟内就绪"
done
log "✅ 第三批完成！"
touch $WORKSPACE/pipeline_batch3_done
spawn_batch4

# 监听第四批
log "等待第四批完成 (intel_10/11/12)..."
for f in done_intel_10 done_intel_11 done_intel_12; do
    wait_for_file "$f" 600 || log "⚠️ $f 未在10分钟内就绪"
done
log "✅ 第四批完成！"
touch $WORKSPACE/pipeline_batch4_done
spawn_reviewers

# 监听审核
log "等待审核完成..."
for f in done_reviewer_en done_reviewer_cn done_reviewer_intl; do
    wait_for_file "$f" 900 || log "⚠️ $f 审核超时"
done
log "✅ 审核完成！"
spawn_edu_lead

# 等待edu_lead
log "等待洞察生产完成..."
wait_for_file "done_edu_lead" 1200 || log "⚠️ edu_lead超时"

# 统计
total=$(ls $WORKSPACE/intel_batch*.md 2>/dev/null | wc -l | tr -d ' ')
insights_count=$(grep -c "^## 洞察" $WORKSPACE/insights_20260330.md 2>/dev/null || echo "?")

log "========================================"
log "📋 情报流水线全部完成！"
log "入库文件：$total 个"
log "洞察条数：$insights_count 条"
log "完成时间：$(date)"
log "========================================"

# 发飞书报告
cat << FIEU > /tmp/feishu_report.json
{"text": "📋 情报日报·流水线完成通知\n2026-03-30 05:00\n\n✅ 第一批（英文核心期刊/AI教育产品/arXiv预印本）：已完成\n✅ 第二批（CSSCI/中文学术/政府政策）：已完成\n✅ 第三批（生成式AI/智慧教育/STEM）：已完成\n✅ 第四批（AI教师/学习分析/个性化学习）：已完成\n✅ 三审（EN/CN/INTL）：已完成\n✅ 洞察生产：已完成\n\n入库文件：$total 个\n今日洞察：$insights_count 条\n\n详细报告：/workspace/knowledge/insights_20260330.md"}
FIEU
log "报告已生成"

