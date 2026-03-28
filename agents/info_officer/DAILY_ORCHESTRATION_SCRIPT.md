# 小艾每日情报启动脚本
> 版本：v1.0 | 日期：2026-03-28 | 小艾执行

## 执行时机
- 每日 05:00 AM cron触发
- 小艾立即启动情报官协调员子Agent

## 小艾执行步骤

### Step 1：小艾并发spawn以下子Agent（全部同时）

使用 sessions_spawn 一次性启动15个子Agent：

**搜索Agent × 12（情报01-12，并发）：**

情报01（英文期刊-Computers & Education）：
"你是情报官团队搜索子Agent。指定来源：site:sciencedirect.com 'Computers and Education' AI K-12。严格遵守：搜索词必须同时包含AI教育/AI教学关键词+K12关键词。找到论文后访问doi.org验证，写入/workspace/knowledge/原文库/{DOI}.md。完成后sessions_send通知协调员：搜到X篇/验证通过X篇/DOI列表（含英文原文标题+中文标题）。"

情报02（英文期刊-Frontiers/ILE）：
"你是情报官团队搜索子Agent。指定来源：site:frontiersin.org 'Education' AI K-12；site:tandfonline.com 'Interactive Learning Environments' AI。必须同时有AI教育+K12关键词。访问doi.org验证，写入原文库。完成后sessions_send通知。"

情报03（英文期刊-Springer/Wiley）：
"你是情报官团队搜索子Agent。指定来源：site:link.springer.com AI education K-12。必须同时有AI education/AI teaching+K12关键词。访问doi.org验证，写入原文库。完成后sessions_send通知。"

情报04（英文期刊-Nature npj/SD）：
"你是情报官团队搜索子Agent。指定来源：site:nature.com npj Science of Learning AI learning K-12；site:sciencedirect.com 'Computers and Education: Artificial Intelligence'。必须同时有AI education+K12关键词。访问doi.org验证，写入原文库。完成后sessions_send通知。"

情报05（MDPI/DOAJ）：
"你是情报官团队搜索子Agent。指定来源：site:mdpi.com AI education K-12；site:doaj.org 'K-12' 'artificial intelligence' education。必须同时有AI education/AI teaching+K12关键词。访问doi.org验证，写入原文库。完成后sessions_send通知。"

情报06（arXiv）：
"你是情报官团队搜索子Agent。指定来源：site:arxiv.org cs.AI OR cs.EDU K-12 education。必须同时有K-12+AI education/AI teaching关键词。arXiv编号验证，写入原文库标注preprint。完成后sessions_send通知。"

情报07（中国知网/万方）：
"你是情报官团队搜索子Agent。指定来源：site:cnki.net 人工智能教育 K-12；site:wanfangdata.com.cn 人工智能教育 研究。中文关键词：人工智能教育+中小学/基础教育。写入原文库。完成后sessions_send通知。"

情报08（中文核心-开放教育/电化教育）：
"你是情报官团队搜索子Agent。指定来源：site:cnki.net 开放教育研究 人工智能；site:cnki.net 电化教育研究 人工智能；site:cnki.net 现代教育技术 AI。中文关键词：人工智能教育+中小学/基础教育。写入原文库。完成后sessions_send通知。"

情报09（中文-远程教育/课程教材）：
"你是情报官团队搜索子Agent。指定来源：site:cnki.net 中国远程教育 人工智能；site:cnki.net 课程教材教法 人工智能；site:cnki.net 教育发展研究 AI。中文关键词：人工智能教育+中小学。写入原文库。完成后sessions_send通知。"

情报10（UNESCO/OECD/WorldBank）：
"你是情报官团队搜索子Agent。指定来源：site:unesco.org AI education K-12；site:oecd.org AI education K-12 policy；site:worldbank.org AI education。必须有K-12 AI education官方报告。验证来源，写入原文库标注机构。完成后sessions_send通知。"

情报11（各国K12 AI政策）：
"你是情报官团队搜索子Agent。指定来源：site:moe.gov.cn 人工智能 教育 K-12；site:gov.uk AI education schools；site:ed.gov AI education K-12。各国K12 AI教育政策文件。写入原文库。完成后sessions_send通知。"

情报12（Semantic Scholar补充）：
"你是情报官团队搜索子Agent。指定来源：site:semanticscholar.org 'K-12' 'AI education'。补充搜索K12 AI教育论文，必须同时有K12+AI education/AI teaching关键词。访问doi.org验证，写入原文库。完成后sessions_send通知。"

**审核Agent × 3（并发）：**

审核01（英文论文）：
"你是情报官团队审核子Agent。扫描/workspace/knowledge/原文库/所有待审核文件。必须实际访问doi.org验证每个DOI。发现造假→标记❌已删除+原因。确认真实→标记✅已验证。发现造假→sessions_send通知协调员（包含DOI+造假类型+原因）。每10分钟向协调员汇报进度。"

审核02（中文论文）：
"你是情报官团队审核子Agent。扫描/workspace/knowledge/原文库/所有待审核文件。验证中文论文DOI/机构。无DOI时验证机构官网。注意：中国大陆访问限制≠造假，以综合判断为主。造假→标记❌+sessions_send通知协调员。真实→标记✅。"

审核03（国际报告/政策）：
"你是情报官团队审核子Agent。扫描/workspace/knowledge/原文库/所有待审核报告。验证UNESCO/OECD/WorldBank/各国政府官网链接。无DOI的政府文件需验证官网可访问。造假→标记❌+sessions_send通知协调员。真实→标记✅。"

### Step 2：小艾监控（不等结果，持续在线）

- 小艾在spawn完所有Agent后，保持接收sessions_send通知
- 收到审核Agent打回通知 → 立即spawn新的搜索Agent重试（调整提示词后）
- 收到搜索Agent完成通知 → 记录结果
- 收到情报官汇总 → 立即向陛下转发（实时推送）

### Step 3：IP主编归档触发

当素材库有新内容增加时（通过监控sessions_send），小艾立即spawn edu_lead归档Agent：
- 读取素材库最新内容
- 归入13个信念抽屉
- 推送归档简报给陛下

### Step 4：向陛下实时汇报

小艾收到任何sessions_send通知后，立即向陛下推送实时进度：
- "🔄 情报01完成：搜到X篇，验证通过X篇"
- "⚠️ 审核02打回：情报07发现X篇疑似造假，正在重搜"
- "✅ 首批X篇已入库，素材库正在生成..."

---

## 质量红线

**搜索时发现以下情况，直接丢弃，不写入原文库：**
- DOI无法访问doi.org验证
- 研究对象不是K12（是高等/成人/职业教育）
- 主题不含AI教育/AI教学（是纯AI伦理/AI安全/AI心理学）
- 数据/作者/期刊无法验证

**禁止搜索词（会搜到无关内容）：**
- ❌ "artificial intelligence" alone（无education）
- ❌ "AI ethics" / "AI safety"
- ❌ "higher education AI"
- ❌ "AI psychology" / "AI cognition"
- ❌ "AI governance" / "AI policy"（无education场景）

**允许搜索词：**
- ✅ "AI education" AND "K-12"
- ✅ "artificial intelligence" AND "school" AND "teaching"
- ✅ "generative AI" AND "classroom" AND "K-12"
- ✅ "人工智能教育" AND "中小学/基础教育/K-12"
- ✅ "AI literacy" AND "K-12"
