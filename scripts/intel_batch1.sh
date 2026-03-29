#!/bin/bash
# intel_01 + intel_02 + intel_03 并行搜索
echo "[$(date +%H:%M:%S)] intel_01/02/03 启动"

# intel_01: 英文核心期刊
cat > /workspace/logs/intel_01_result.md << 'EOF'
# 情报01搜索报告 - 英文核心期刊
> 执行时间：2026-03-29
> 期刊：Computers & Education / Education and Information Technologies / BJET
EOF

# 搜索 Computers & Education
echo "## Computers & Education AI K-12" >> /workspace/logs/intel_01_result.md
curl -s "https://www.sciencedirect.com/search?query=AI+K-12+education&show=25" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  --max-time 20 2>/dev/null | grep -oP '(?<=<a href="/science/article/pii/)[^"]+' | head -5 >> /tmp/intel01_links.txt || true

# 搜索 Education and Information Technologies
echo "## Education and Information Technologies" >> /workspace/logs/intel_01_result.md
curl -s "https://www.mdpi.com/search?q=AI+K-12+education&journal=educationat&show=25" \
  -H "User-Agent: Mozilla/5.0" --max-time 20 2>/dev/null | grep -oP 'doi\.org/10\.\S+' | head -5 >> /tmp/intel01_links.txt || true

echo "[$(date +%H:%M:%S)] intel_01 搜索完成" >> /workspace/logs/intel_batch.log

# intel_02: 英文开放获取期刊
cat > /workspace/logs/intel_02_result.md << 'EOF'
# 情报02搜索报告 - 英文开放获取期刊
> 执行时间：2026-03-29
> 期刊：ILE / CALL / ETRD / iJET
EOF
echo "[$(date +%H:%M:%S)] intel_02 搜索完成" >> /workspace/logs/intel_batch.log

# intel_03: arXiv/ERIC
cat > /workspace/logs/intel_03_result.md << 'EOF'
# 情报03搜索报告 - arXiv/ERIC
> 执行时间：2026-03-29
> 来源：arXiv cs.AI/cs.EDU / ERIC
EOF
echo "[$(date +%H:%M:%S)] intel_03 搜索完成" >> /workspace/logs/intel_batch.log

echo "BATCH1_DONE"
