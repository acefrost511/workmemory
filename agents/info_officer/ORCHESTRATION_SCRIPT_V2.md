# 情报官协调员启动脚本
> 版本：v2.0 | 日期：2026-03-28 | 完整流水线执行

## 执行前提

协调员在启动前先读取以下文件了解架构：
- /workspace/agents/info_officer/TEAM_COORDINATOR_V2.md（主架构）
- /workspace/agents/info_officer/SEARCH_AGENTS_V2.md（12个搜索Agent的详细来源）
- /workspace/agents/info_officer/VERIFY_AGENTS_V2.md（3个审核Agent的审核标准）

## 启动脚本（按顺序执行）

### Phase 1：并发启动12个搜索子Agent

使用sessions_spawn并发启动以下12个Agent（全部同时，不等待）：

**情报01** — Computers & Education / BJET / JRTE
```
sessions_spawn:
  task: "你是情报官团队·搜索子Agent（情报01）。指定来源：site:sciencedirect.com 'Computers and Education' K-12 AI；site:tandfonline.com 'British Journal of Educational Technology' AI K-12。搜索K12 AI教育论文，找到后验证DOI，写入原文库。完成后sessions_send通知协调员：搜到X篇/验证通过X篇/DOI列表。详见/workspace/agents/info_officer/SEARCH_AGENTS_V2.md"
  label: "情报01_Computers_BJET_JRTE"
  runtime: "subagent"
  runTimeoutSeconds: 1200
```

**情报02** — Frontiers in Education / Interactive Learning Environments
```
sessions_spawn:
  task: "你是情报官团队·搜索子Agent（情报02）。指定来源：site:frontiersin.org 'Education' AI K-12；site:tandfonline.com 'Interactive Learning Environments' AI。搜索K12 AI教育论文，找到后验证DOI，写入原文库。完成后sessions_send通知协调员。详见/workspace/agents/info_officer/SEARCH_AGENTS_V2.md"
  label: "情报02_Frontiers_ILE"
  runtime: "subagent"
  runTimeoutSeconds: 1200
```

**情报03** — Springer / Wiley教育期刊
```
sessions_spawn:
  task: "你是情报官团队·搜索子Agent（情报03）。指定来源：site:link.springer.com 教育学期刊 AI K-12；site:onlinelibrary.wiley.com 'Journal of Computer Assisted Learning' AI。搜索K12 AI教育论文，找到后验证DOI，写入原文库。完成后sessions_send通知协调员。详见/workspace/agents/info_officer/SEARCH_AGENTS_V2.md"
  label: "情报03_Springer_Wiley"
  runtime: "subagent"
  runTimeoutSeconds: 1200
```

**情报04** — Nature npj / ScienceDirect
```
sessions_spawn:
  task: "你是情报官团队·搜索子Agent（情报04）。指定来源：site:nature.com/npjjsci AI learning K-12；site:sciencedirect.com 'Computers and Education: Artificial Intelligence'。搜索K12 AI教育论文，找到后验证DOI，写入原文库。完成后sessions_send通知协调员。详见/workspace/agents/info_officer/SEARCH_AGENTS_V2.md"
  label: "情报04_Nature_SD"
  runtime: "subagent"
  runTimeoutSeconds: 1200
```

**情报05** — MDPI / DOAJ开放获取
```
sessions_spawn:
  task: "你是情报官团队·搜索子Agent（情报05）。指定来源：site:mdpi.com AI education K-12；site:doaj.org 'K-12' 'artificial intelligence'。搜索K12 AI教育论文，找到后验证DOI，写入原文库。完成后sessions_send通知协调员。详见/workspace/agents/info_officer/SEARCH_AGENTS_V2.md"
  label: "情报05_MDPI_DOAJ"
  runtime: "subagent"
  runTimeoutSeconds: 1200
```

**情报06** — arXiv预印本
```
sessions_spawn:
  task: "你是情报官团队·搜索子Agent（情报06）。指定来源：site:arxiv.org 'cs.AI' OR 'cs.EDU' K-12。搜索K12 AI教育arXiv预印本，找到后验证arXiv编号，写入原文库（标注preprint）。完成后sessions_send通知协调员。详见/workspace/agents/info_officer/SEARCH_AGENTS_V2.md"
  label: "情报06_arXiv"
  runtime: "subagent"
  runTimeoutSeconds: 1200
```

**情报07** — 中国知网/万方
```
sessions_spawn:
  task: "你是情报官团队·搜索子Agent（情报07）。指定来源：site:cnki.net 人工智能教育 K-12 基础教育；site:wanfangdata.com.cn 人工智能教育 研究。搜索K12 AI教育中文论文，找到后尝试验证DOI，写入原文库。完成后sessions_send通知协调员。详见/workspace/agents/info_officer/SEARCH_AGENTS_V2.md"
  label: "情报07_知网_万方"
  runtime: "subagent"
  runTimeoutSeconds: 1200
```

**情报08** — 开放教育研究/电化教育研究/现代教育技术
```
sessions_spawn:
  task: "你是情报官团队·搜索子Agent（情报08）。指定来源：site:cnki.net 开放教育研究 人工智能；site:cnki.net 电化教育研究 人工智能；site:cnki.net 现代教育技术 AI。搜索K12 AI教育中文论文，写入原文库。完成后sessions_send通知协调员。详见/workspace/agents/info_officer/SEARCH_AGENTS_V2.md"
  label: "情报08_开放教育_电化教育"
  runtime: "subagent"
  runTimeoutSeconds: 1200
```

**情报09** — 中国远程教育/课程教材教法/教育发展研究
```
sessions_spawn:
  task: "你是情报官团队·搜索子Agent（情报09）。指定来源：site:cnki.net 中国远程教育 人工智能；site:cnki.net 课程教材教法 人工智能；site:cnki.net 教育发展研究 AI。搜索K12 AI教育中文论文，写入原文库。完成后sessions_send通知协调员。详见/workspace/agents/info_officer/SEARCH_AGENTS_V2.md"
  label: "情报09_远程教育_课程教材"
  runtime: "subagent"
  runTimeoutSeconds: 1200
```

**情报10** — UNESCO/OECD/WorldBank/Stanford SCALE
```
sessions_spawn:
  task: "你是情报官团队·搜索子Agent（情报10）。指定来源：site:unesco.org AI education K-12；site:oecd.org AI education policy；site:worldbank.org AI education；Stanford SCALE官网。搜索K12 AI教育国际报告，找到后验证来源，写入原文库（标注来源机构）。完成后sessions_send通知协调员。详见/workspace/agents/info_officer/SEARCH_AGENTS_V2.md"
  label: "情报10_国际报告"
  runtime: "subagent"
  runTimeoutSeconds: 1200
```

**情报11** — K12 AI各国政策
```
sessions_spawn:
  task: "你是情报官团队·搜索子Agent（情报11）。指定来源：site:moe.gov.cn 人工智能 教育 政策；site:gov.uk AI education policy schools；site:ed.gov AI education K-12；site:mext.go.jp AI education Japan。搜索各国K12 AI教育政策文件，写入原文库。完成后sessions_send通知协调员。详见/workspace/agents/info_officer/SEARCH_AGENTS_V2.md"
  label: "情报11_各国政策"
  runtime: "subagent"
  runTimeoutSeconds: 1200
```

**情报12** — Semantic Scholar / CrossRef补充
```
sessions_spawn:
  task: "你是情报官团队·搜索子Agent（情报12）。指定来源：site:semanticscholar.org 'K-12' 'AI education'。补充搜索前面11个Agent可能遗漏的K12 AI教育论文，找到后验证DOI，写入原文库。完成后sessions_send通知协调员。详见/workspace/agents/info_officer/SEARCH_AGENTS_V2.md"
  label: "情报12_SemanticScholar"
  runtime: "subagent"
  runTimeoutSeconds: 1200
```

### Phase 2：并发启动3个审核子Agent（与Phase 1同时进行）

**审核01** — 英文论文审核
```
sessions_spawn:
  task: "你是情报官团队·审核子Agent（审核01）。实时扫描/workspace/knowledge/原文库/，对英文论文执行DOI验证和数据核实。发现造假立即sessions_send通知协调员（打回通知）。每10分钟向协调员汇报审核进度。详见/workspace/agents/info_officer/VERIFY_AGENTS_V2.md"
  label: "审核01_英文论文"
  runtime: "subagent"
  runTimeoutSeconds: 1800
```

**审核02** — 中文论文审核
```
sessions_spawn:
  task: "你是情报官团队·审核子Agent（审核02）。实时扫描/workspace/knowledge/原文库/，对中文论文执行DOI验证和机构核实。注意：中国大陆访问DOI可能有网络限制，以综合判断为主。发现造假立即sessions_send通知协调员（打回通知）。详见/workspace/agents/info_officer/VERIFY_AGENTS_V2.md"
  label: "审核02_中文论文"
  runtime: "subagent"
  runTimeoutSeconds: 1800
```

**审核03** — 国际报告/政策文件审核
```
sessions_spawn:
  task: "你是情报官团队·审核子Agent（审核03）。实时扫描/workspace/knowledge/原文库/，对UNESCO/OECD/WorldBank/各国政府发布的报告和政策文件验证来源权威性。无DOI的报告需验证官网链接可访问。发现造假立即sessions_send通知协调员（打回通知）。详见/workspace/agents/info_officer/VERIFY_AGENTS_V2.md"
  label: "审核03_国际报告"
  runtime: "subagent"
  runTimeoutSeconds: 1800
```

### Phase 3：协调员监控与子Agent管理

在spawn完所有Agent后，协调员持续执行：

1. **接收搜索Agent回报**：每收到一个sessions_send通知，记录其搜到/验证通过的数量
2. **接收审核Agent回报**：记录审核进度和打回通知
3. **处理打回（关键！要分析原因并调整提示词）：**
   - 收到打回通知后，分析造假原因：
     - 是Agent提示词描述不清晰？→ 调整明确指令
     - 是Agent对"真实"理解有偏差？→ 强化"真实是唯一成功标准"指令
     - 是Agent搜索压力大导致凑数？→ 移除数量压力，强调宁可少不要假
   - 调整该Agent提示词后，重新spawn它重搜同一主题
   - 不要简单重启，用改进后的提示词重新训练
   - 若同一Agent被打回2次 → 再次调整提示词+加入单独验证步骤
   - 若同一Agent被打回3次 → 暂停该Agent，改造提示词完成后重新启动重试同一主题
   - 若同一Agent被打回4次及以上 → 彻底暂停该Agent，向陛下汇报，等待陛下指示如何处理
4. **接收协调员自身状态**：监控各Agent运行情况，如有问题及时处理

### Phase 4：汇总与向陛下汇报

所有搜索Agent完成 + 主要审核完成后：

1. 扫描 /workspace/knowledge/原文库/ 统计：
   - ✅已验证总数
   - ❌已删除总数
   - 英文/中文各多少篇

2. 生成 /workspace/knowledge/素材库/素材库_YYYY-MM-DD.md：
   - 从✅已验证的原文库文件中提取信息
   - 按标准格式生成摘要（研究背景≥400字/研究发现≥400字/对教育价值≥200字）

3. 向陛下推送标准汇报

## 关键约束

- 12个搜索Agent + 3个审核Agent全部并发启动，不串行等待
- 搜索过程中实时汇报，不等全部完成再汇报
- 收到打回通知后立即处理，不积压
- 真实是唯一成功标准，绝不捏造
- 每篇论文可溯源（来源Agent标注在原文库文件中）
