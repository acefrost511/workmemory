#!/usr/bin/env python3
import re, json
from collections import defaultdict
from pathlib import Path

with open('/workspace/knowledge/研究观点池_全量.json','r',encoding='utf-8') as f:
    pool = json.load(f)
arts = pool['文章列表']
print(f'总计: {len(arts)} 篇')

THEMES = {
    '教师工作量/效率/培训': ['备课','planning','workload','时间','节省','减少','负担','效率','培训','training','teacher workload'],
    '学业成绩/学习效果': ['成绩','achievement','performance','分数','提高','提升','降低','下降','学业'],
    '学习动机/参与/情感': ['动机','engagement','参与','兴趣','情感','态度','自我效能'],
    '批判性思维/高阶思维': ['批判性思维','critical thinking','问题解决','高阶思维','creativity'],
    '个性化/自适应/年级匹配': ['个性化','adaptive','年级','匹配','差异','精准'],
    'AI素养/教师能力': ['AI素养','AI literacy','教师能力'],
    '伦理风险/公平/偏见': ['伦理','风险','公平','偏见','bias','ethics','risk'],
    '协作学习/社会连接': ['协作','collaboration','互动','同伴','social'],
    '元认知/反思/自主学习': ['元认知','metacognition','反思','self-regulation'],
    '反馈/评价/过程性评价': ['反馈','评价','assessment'],
    '知识迁移/长期效果': ['迁移','transfer','长期','持久'],
    '政策/框架/标准': ['政策','policy','框架','UNESCO','OECD','标准'],
    '技术采纳/使用障碍': ['采纳','adoption','障碍','resistance'],
    '情感支持/孤独': ['情感','孤独','社会连接','lonely'],
    '计算思维/STEM/编程': ['计算思维','STEM','编程','coding'],
    'PBL/项目式学习': ['PBL','项目式','project-based'],
    '人机协作/对话式AI': ['人机','对话','conversational','chatbot'],
    '数据驱动/预测建模': ['预测','prediction','数据驱动'],
    '具身/沉浸式学习': ['具身','沉浸','embodied'],
}

theme_count = defaultdict(int)
theme_examples = defaultdict(list)
for art in arts:
    text = (art.get('英文标题','')+art.get('中文标题','')+art.get('核心发现','')).lower()
    matched = False
    for theme, kws in THEMES.items():
        for kw in kws:
            if kw.lower() in text:
                theme_count[theme] += 1
                if len(theme_examples[theme]) < 2:
                    title = art.get('中文标题') or art.get('英文标题','')[:40]
                    theme_examples[theme].append(f"  · {title}")
                matched = True
                break
    if not matched:
        theme_count['其他主题'] += 1

print()
print('=== 主题分布（366篇）===')
for theme, count in sorted(theme_count.items(), key=lambda x: -x[1]):
    print(f'  {theme}: {count}篇')
    for ex in theme_examples.get(theme, []):
        print(ex)

rich = [a for a in arts if len(a.get('核心发现',''))>80]
empty = [a for a in arts if not a.get('核心发现','')]
print(f'\n有实质内容（>80字）: {len(rich)}篇')
print(f'仅有标题/元数据: {len(empty)}篇')
