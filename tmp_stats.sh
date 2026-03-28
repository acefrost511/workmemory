#!/bin/bash
echo "=== 各抽屉素材数量统计 ==="
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13; do
  case $i in
    1) f="信念1-AI教育观.md" ;;
    2) f="信念2-教师角色观.md" ;;
    3) f="信念3-学习本质观.md" ;;
    4) f="信念4-教育公平观.md" ;;
    5) f="信念5-学生发展观.md" ;;
    6) f="信念6-课堂教学观.md" ;;
    7) f="信念7-教育评价观.md" ;;
    8) f="信念8-家校协同观.md" ;;
    9) f="信念9-教育伦理观.md" ;;
    10) f="信念10-教育技术观.md" ;;
    11) f="信念11-教育创新观.md" ;;
    12) f="信念12-教育政策观.md" ;;
    13) f="信念13-未来教育观.md" ;;
  esac
  count=$(grep -c "🔬 研究素材" "/workspace/knowledge/信念抽屉/$f" 2>/dev/null || echo 0)
  echo "信念$i: ${count}篇"
done

# Create staging area
echo "" > /workspace/knowledge/staging_area.md
echo "暂存区已创建"
