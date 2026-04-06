#!/usr/bin/env python3
"""重置历史推送标记，只保留今日推送，恢复候选池"""
import os, re

FORMAL_DIR = '/workspace/knowledge/原文库'
TODAY = '2026-04-06'

# Skill规定：只有当日推送才排除
# 04-04和04-05的标记全部清除，让这些文章重新进入候选池

removed = 0
for fname in os.listdir(FORMAL_DIR):
    if not fname.endswith('.md'): continue
    fpath = os.path.join(FORMAL_DIR, fname)
    with open(fpath, encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    new_c = c
    # 清除04-04的推送状态（但保留已触动/已无触动标记）
    new_c = re.sub(r'\n状态：已推送 \| 推送日期：2026-04-04[^\n]*', '', new_c)
    new_c = re.sub(r'\n状态：已推送 \| 推送日期：2026-04-05[^\n]*', '', new_c)
    # 清除04-06的重复标记（保留一个）
    matches = re.findall(r'\n状态：已推送 \| 推送日期：2026-04-06[^\n]*', new_c)
    if len(matches) > 1:
        # 只保留第一个，其余删除
        parts = new_c.split('\n状态：已推送 | 推送日期：2026-04-06')
        first = matches[0]
        rest = ''.join(matches[1:])
        new_c = parts[0] + first + parts[0].join(parts[1:]) if len(parts) > 1 else new_c
        new_c = re.sub(r'\n状态：已推送 \| 推送日期：2026-04-06[^\n]*', '\n'.join(matches[1:]), new_c, count=0)
    
    if new_c != c:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_c)
        removed += 1

print(f'处理文件：{removed} 篇')
print('重置完成，候选池已恢复')
