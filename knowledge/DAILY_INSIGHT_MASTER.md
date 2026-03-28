# 每日洞察生产工作流·主控文档
> 版本：v1.1 | 日期：2026-03-28 | 陛下确认版
> 位置：/workspace/knowledge/DAILY_INSIGHT_MASTER.md
> cron任务触发方式：读取本文件 → 按步骤执行

---

## ⚠️ 绝对禁止（违者杀）

- ❌ 编造任何具体人物/学校/场景/情节
- ❌ 在"碰撞逻辑"段落混入虚构内容
- ❌ 修改研究原文的数字
- ❌ 用"某学生""某老师""某学校"作为论证依据
- ❌ 虚构案例（未标注来源的"真实场景"）

**一律只引用原文数据，人物/场景只能来自陛下笔记（knowledge/笔记/），否则一律作为虚构处理**

---

## 各Agent职责与文件依赖

| 执行者 | 必须读取的文件 | 产出 |
|--------|--------------|------|
| edu_lead（主编） | 本文档 + IP_WORKFLOW_V1.md | 统筹协调 |
| edu_writer（洞察撰写） | INSIGHT_WRITING_RULES.md + 信念抽屉 | 3个候选洞察 |
| reader_*（评分Agent） | edu_writer产出的洞察草案 | 评分报告 |
| edu_lead（终审） | 6份评分报告 + 洞察草案 | 核实→推送/打回 |

---

## 执行步骤

### Step 1：主编读取文档（edu_lead）
读取以下文件，建立今日洞察方向：
1. /workspace/knowledge/DAILY_INSIGHT_MASTER.md（本文档）
2. /workspace/knowledge/IP_WORKFLOW_V1.md（工作流详细说明）
3. /workspace/knowledge/beliefs/目录下2-3个信念抽屉（读核心表述+金句+素材积累区）

### Step 2：主编选择碰撞主题
从信念抽屉里找2-3个碰撞点，确定今日洞察方向

### Step 3：主编spawn edu_writer
edu_writer 必须读取：
- /workspace/knowledge/INSIGHT_WRITING_RULES.md（写作规范·铁律）
- 对应信念抽屉文件

**edu_writer 产出要求：**
- 3个候选洞察
- 每篇含：Hook（≤60字）+ 引用证据（英文标题/作者/机构/期刊/年月/DOI）+ 碰撞逻辑 + 核心洞察 + 读者带走老师（≥3条）+ 读者带走家长（≥2条）

**edu_writer 自检（写完必查）：**
- [ ] 所有数字是否来自原文研究？
- [ ] 是否有未标注来源的人物/学校/场景？
- [ ] 碰撞逻辑段落是否只引用了研究数据？
- [ ] 如含虚构场景，是否在段首标注【以下为基于研究的假设性场景】？

### Step 4：主编并发spawn 6个读者Agent评分
等待 edu_writer 回报初稿后，6个评分Agent同时执行：
- reader_new_teacher / reader_senior_teacher / reader_principal / reader_parent / reader_expert
- 每个Agent在评分时，必须检查：核心洞察段落是否含有虚构内容？若有，在评分中注明并扣分（虚构内容=单维度≤4）

### Step 5：主编汇总评分
达标条件（必须同时满足）：
① 加权总分 ≥ 9.0
② 无单维度 ≤ 4
③ 社交货币指数 ≥ 6
④ 文章传播力 ≥ 6

**达标 → 进入Step 6**
**未达标 → 打回edu_writer修改，说明具体问题，最多3次迭代**
**3次迭代仍<9.0 → 放弃，换候选洞察**

### Step 6：主编终审（最重要的防线）
主编必须核查：
- [ ] 核心洞察是否含虚构内容？（最优先检查项）
- [ ] 所有引用证据是否含完整DOI？
- [ ] Hook≤60字？
- [ ] 读者带走是否≥3条/≥2条？
- [ ] 碰撞逻辑是否只引用了研究？

**发现虚构内容 → 立即打回edu_writer，不推送**
**不发现虚构内容 → 进入Step 7**

### Step 7：反哺抽屉
通过exec写入（不用edit）：
```
echo '洞察编号/日期/总分/社交货币/传播力' >> /workspace/knowledge/beliefs/信念{N}-{名}.md
```

### Step 8：永久存储
```
创建 /workspace/knowledge/insight_daily_YYYY-MM-DD.md
追加 /workspace/knowledge/collision_results_v3.md
```

### Step 9：飞书推送陛下
推送至：ou_b60e71d5307978b7ac0151f377cdd512

**推送格式：** 详细完整版（洞察全文+所有引用+评分明细+读者带走），不得简化

---

## 写作规范速查（edu_writer必读）
路径：/workspace/knowledge/INSIGHT_WRITING_RULES.md

核心要点：
- 虚构场景处理：绝对禁止出现未标注的虚构人物/学校
- 所有数字：必须来自原文研究
- 碰撞逻辑：只用A研究×B研究的逻辑关系
- 案例来源：只能来自陛下笔记（knowledge/笔记/）
- 假设性场景（如为说明研究而编）：必须标注【以下为基于研究的假设性场景】

---

## 动态权重参考（主编判断洞察类型后调整）
路径：/workspace/knowledge/IP_WORKFLOW_V1.md（第五节）

| 洞察类型 | 权重变化 |
|---------|---------|
| 教师向 | new_teacher×1.5，senior×1.5 |
| 家长向 | parent×1.5 |
| 校长向 | principal×1.5，expert×1.3 |
| 学术向 | expert×1.8 |
| 通用向 | 基准权重 |
