#!/bin/bash
# 信念抽屉备份脚本
# 每天11:00自动运行，在任何操作前先备份

BACKUP_DIR="/workspace/.backups/beliefs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

# 备份信念抽屉
if [ -d /workspace/knowledge/beliefs ]; then
  cp -r /workspace/knowledge/beliefs/ "$BACKUP_DIR/beliefs_${TIMESTAMP}"
  echo "[$(date)] 备份完成: beliefs_${TIMESTAMP}"
  
  # 只保留最近10个备份，删除旧的
  cd "$BACKUP_DIR" && ls -dt beliefs_* | tail -n +11 | xargs rm -rf 2>/dev/null
  echo "[$(date)] 备份数量: $(ls -1 beliefs_* 2>/dev/null | wc -l)"
else
  echo "[$(date)] 警告：抽屉目录不存在，跳过备份"
fi
