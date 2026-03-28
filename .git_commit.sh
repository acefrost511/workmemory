#!/bin/bash
cd /workspace
git add agents/info_officer/SOUL.md
git commit -m "情报官团队：搜索方法论铁律确立+先核实后收录流程
- info_officer SOUL.md：搜索方法论v2.0（先核实后收录）
- 精准搜索策略：site:定向搜索+DOI验证流程
- 可信来源白名单：英文9个+中文9个核心期刊
- 危险信号清单：直接排除6类情况
- 执行检查清单更新：核实环节+收录环节+数量要求
- 9路子Agent共同守则：不得造假+DOI验证+结果格式规范"
SHA=$(git rev-parse HEAD)
timeout 50 git push --force origin $SHA:master && echo "DONE:$SHA"
