#!/bin/bash
# 信念抽屉恢复脚本
# 当发现抽屉丢失时，运行此脚本从最新备份恢复

BACKUP_DIR="/workspace/.backups/beliefs"
LATEST=$(ls -dt "$BACKUP_DIR"/beliefs_* 2>/dev/null | head -1)

if [ -z "$LATEST" ]; then
  echo "没有找到备份，恢复失败"
  exit 1
fi

echo "发现最新备份: $LATEST"
echo "即将恢复信念抽屉..."

# 先检查当前抽屉状态
if [ -d /workspace/knowledge/beliefs ] && [ "$(ls /workspace/knowledge/beliefs/*.md 2>/dev/null | wc -l)" -gt 2 ]; then
  echo "当前抽屉已有内容，跳过恢复"
  ls /workspace/knowledge/beliefs/*.md | wc -l
  exit 0
fi

# 执行恢复
mkdir -p /workspace/knowledge/beliefs
cp -r "$LATEST"/* /workspace/knowledge/beliefs/ 2>/dev/null
echo "恢复完成，共恢复文件数: $(ls /workspace/knowledge/beliefs/*.md 2>/dev/null | wc -l)"
