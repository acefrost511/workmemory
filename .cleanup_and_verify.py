#!/usr/bin/env python3
"""清理非授权文件，移动可疑文件到pending审核区"""
import os, shutil

base = '/workspace/knowledge/原文库/'
pending = base + '.pending/'
os.makedirs(pending, exist_ok=True)

# 1. 删除各国教育部政策文件（非授权）
policy_files = [
    '日本_K-12人工智能教育政策.md',
    '美国_K-12人工智能教育政策.md',
    '英国_K-12人工智能教育政策.md',
    '中国_K-12人工智能教育政策.md',
    'K-12人工智能教育政策汇编_2026-04-04.md',
    '各国_K12_AI教育政策文件_20260404_intel09.md',
]
for f in policy_files:
    fp = base + f
    if os.path.exists(fp):
        os.remove(fp)
        print(f'删除政策文件: {f}')
    else:
        print(f'不存在（已删?）: {f}')

# 2. 移动可疑中文文件到.pending/待审核
questionable = [
    '中国远程教育_2025_人工智能基础教育论文.md',
    '中国远程教育_美国K12自适应学习工具的应用与启示.md',
    '中国教育学刊_2025_第4期_人工智能基础教育论文.md',
    '中国教育学刊_人工智能视域下教师信息素养内涵解析及提升策略研究.md',
    '现代教育技术_AI_K12_2025_2026.md',
    '现代教育技术_K12人工智能教育逻辑思考_周邵锦王帆.md',
    '现代教育技术_中小学阶段人工智能教育研究.md',
    '电化教育研究_AI_K12_2025_2026.md',
    '课程教材教法_2025_人工智能基础教育论文.md',
    '课程教材教法_中小学人工智能课程教师胜任力现状与对策研究.md',
    '课程教材教法_具身模拟人工智能赋能的学习变革.md',
    '课程教材教法_创意人工智能与学生创造创新能力的培养与发展.md',
    '课程教材教法_智能教育的挑战与教师的应对策略.md',
]
for f in questionable:
    src = base + f
    dst = pending + f
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f'移入pending审核: {f}')
    else:
        print(f'不存在: {f}')

# 3. 删除已明确的非期刊内容
non_journal = [
    'intel_08_搜索报告_20260404.md',
    'intel_10_搜索报告_20260404.md',
    'intel_11_搜索报告_20260404.md',
    'intel_03_搜索报告_20260404.md',
    'intel_04_搜索报告_20260404.md',
    'intel_05_搜索报告_20260404.md',
    'intel_06_搜索报告_20260404.md',
    '情报06_搜索报告_20260404.md',
    '情报11_2026-04-04_K12AI教育产品搜索.md',
    'intel_07_国际K12AI教育产品_20260404.md',
    'ED676683.md',
    'ED676035.md',
    'INDEX.md',
]
for f in non_journal:
    fp = base + f
    if os.path.exists(fp):
        os.remove(fp)
        print(f'删除非期刊: {f}')

# 4. 统计最终文件数
all_files = [f for f in os.listdir(base) if f.endswith('.md')]
pending_files = [f for f in os.listdir(pending) if f.endswith('.md')]
print(f'\n原文库剩余: {len(all_files)} 个文件')
print(f'待审核区: {len(pending_files)} 个文件')
print('清理完成')
