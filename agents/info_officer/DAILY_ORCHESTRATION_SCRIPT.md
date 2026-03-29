# 小艾每日情报启动脚本
> 版本：v2.0-clean | 日期：2026-03-28 | 清理spawn，恢复持久Agent调用

## 执行时机
- 每日 05:00 AM cron触发
- 小艾立即启动情报官协调员Agent

## 小艾执行步骤

### Step 1：小艾并发调用12个搜索子Agent（全部同时）

使用 sessions_spawn(runtime="acp") 并发调用12个子Agent：

**情报01（英文期刊-Computers & Education）：**
"你是情报官团队搜索子Agent。指定来源：site:sciencedirect.com 'Computers and Education' AI K-12。严格遵守：搜索词必须同时包含AI教育/AI教学关键词+K12关键词。找到论文后访问doi.org验证，写入/workspace/knowledge/原文库/{DOI}.md。完成后sessions_send通知协调员：搜到X篇/验证通过X篇/DOI列表（含英文原文标题+中文标题）。"

**情报02（英文期刊-Frontiers/ILE）：**
"你是情报官团队搜索子Agent。指定来源：site:frontiersin.org 'Education' AI K-12；site:tandfonline.com 'Interactive Learning Environments' AI。必须同时有AI教育+K12关键词。访问doi.org验证，写入原文库。完成后sessions_send通知。"

**情报03（英文期刊-Springer/Wiley）：**
"你是情报官团队搜索子Agent。指定来源：site:link.springer.com AI education K-12。必须同时有AI education/AI teaching+K12关键词。访问doi.org验证，写入原文库。完成后sessions_send通知。"

**情报04（英文期刊-Nature npj/SD）：**
"你是情报官团队搜索子Agent。指定来源：site:nature.com/npjjsci AI learning K-12；site:sciencedirect.com 'Computers and Education: AI'。必须同时有AI education+K12关键词。访问doi.org验证，写入原文库。完成后sessions_send通知。"

**情报05（开放获取-MDPI/DOAJ）：**
"你是情报官团队搜索子Agent。指定来源：site:mdpi.com AI education K-12；site:doaj.org 'K-12' 'artificial intelligence' education。必须同时有AI education+K12关键词。访问doi.org验证，写入原文库。完成后sessions_send通知。"

**情报06（arXiv预印本）：**
"你是情报官团队搜索子Agent。指定来源：site:arxiv.org 'cs.AI' OR 'cs.EDU' K-12。必须同时有AI education+K12关键词。arXiv编号作为文献标识，写入原文库（标注preprint）。完成后sessions_send通知。"

**情报07（中文-中国知网/万方）：**
"你是情报官团队搜索子Agent。指定来源：site:cnki.net 人工智能教育 K-12 基础教育；site:wanfangdata.com.cn 人工智能教育 研究。必须同时有AI教育+K12关键词。尝试验证DOI，写入原文库。完成后sessions_send通知。"

**情报08（中文-开放教育研究/电化教育研究/现代教育技术）：**
"你是情报官团队搜索子Agent。指定来源：site:cnki.net 开放教育研究 人工智能；site:cnki.net 电化教育研究 人工智能；site:cnki.net 现代教育技术 AI。必须同时有AI教育+K12关键词。写入原文库。完成后sessions_send通知。"

**情报09（中文-中国远程教育/课程教材教法/教育发展研究）：**
"你是情报官团队搜索子Agent。指定来源：site:cnki.net 中国远程教育 人工智能；site:cnki.net 课程教材教法 人工智能；site:cnki.net 教育发展研究 AI。必须同时有AI教育+K12关键词。写入原文库。完成后sessions_send通知。"

**情报10（国际组织-UNESCO/OECD/WorldBank/Stanford）：**
"你是情报官团队搜索子Agent。指定来源：site:unesco.org AI education K-12；site:oecd.org AI education policy；site:worldbank.org AI education；Stanford SCALE官网。必须同时有AI education+K12关键词。验证来源权威性，写入原文库（标注来源机构）。完成后sessions_send通知。"

**情报11（各国K12 AI政策）：**
"你是情报官团队搜索子Agent。指定来源：site:moe.gov.cn 人工智能 教育 政策；site:gov.uk AI education policy schools；site:ed.gov AI education K-12；site:mext.go.jp AI education Japan。搜索各国K12 AI教育政策文件，写入原文库。完成后sessions_send通知。"

**情报12（补充-Semantic Scholar）：**
"你是情报官团队搜索子Agent。指定来源：site:semanticscholar.org 'K-12' 'AI education'。补充搜索前面11个Agent可能遗漏的K12 AI教育论文。必须同时有AI education+K12关键词。验证DOI，写入原文库。完成后sessions_send通知。"

### Step 2：接收Agent回报（持续监控）

小艾spawn完成后保持接收sessions_send通知：
- 收到搜索完成 → 记录DOI清单
- 收到审核结果 → 统计验证通过数
- 收到情报官汇总 → 向陛下实时推送
- 收到打回通知 → 立即重新调用对应Agent重试

### Step 3：触发归档

素材库有新内容增加时，小艾立即调用 edu_lead 执行归档：
sessions_spawn(runtime="acp", agentId="edu_lead", task="执行每日归档...", mode="run")

### Step 4：向陛下实时推送

实时推送：
- 首批搜索结果（英文原文标题+中文标题+期刊+DOI）
- 审核结果（通过/删除）
- 最终完整清单

## 关键约束

- 全部使用 sessions_spawn(runtime="acp")，禁止 runtime="subagent"
- 12个搜索Agent全部并发，不串行
- 真实是唯一成功标准，绝不捏造
- 无DOI又无机构官网链接 → 不收录
- 与K12 AI教学无关 → 不收录
