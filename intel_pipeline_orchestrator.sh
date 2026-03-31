#!/bin/bash
# 情报搜索流水线协调器
# 监听done文件，每批完成后自动触发下一批

WORKSPACE="/workspace/knowledge"

log() { echo "[$(date '+%H:%M:%S')] $1"; }

wait_for_done() {
    local file=$1
    local timeout=$2
    local waited=0
    while [ ! -f "$WORKSPACE/$file" ] && [ $waited -lt $timeout ]; do
        sleep 30
        waited=$((waited+30))
        log "等待 $file ... (已等${waited}s)"
    done
    if [ -f "$WORKSPACE/$file" ]; then
        log "✅ $file 已就绪"
        return 0
    else
        log "⏰ 等待 $file 超时"
        return 1
    fi
}

# ===== 监听第一批完成 =====
log "监听第一批 (intel_01/02/03)..."
wait_for_done "done_intel_01" 600
wait_for_done "done_intel_02" 600  
wait_for_done "done_intel_03" 600
log "🎉 第一批全部完成！启动第二批..."

# 写入总协调文件
echo "$(date)" > $WORKSPACE/pipeline_batch1_done

# ===== 第二批完成后监听 =====
wait_for_done "pipeline_batch2_done" 900 || log "第二批未检测到信号，继续监听..."
log "流水线第一阶段完成"
