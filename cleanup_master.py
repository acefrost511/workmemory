#!/usr/bin/env python3
"""Clean up master_k12_ai_research.md - delete entries older than 180 days"""
import re
from datetime import datetime

cutoff = datetime(2025, 9, 25)

with open('/workspace/knowledge/master_k12_ai_research.md', 'r') as f:
    content = f.read()

lines = content.split('\n')

def should_keep_block(lines_block):
    text = '\n'.join(lines_block)
    if not text.strip():
        return False
    dates = re.findall(r'发布[：:]\s*(20\d{2}-\d{2}-\d{2}|20\d{2}-\d{2}|20\d{2})', text)
    if not dates:
        return True  # no date = keep
    for d in dates:
        try:
            if len(d) == 10: dt = datetime.strptime(d, '%Y-%m-%d')
            elif len(d) == 7: dt = datetime.strptime(d, '%Y-%m')
            else: dt = datetime.strptime(d, '%Y')
            if dt >= cutoff: return True
        except: return True
    return False

# Split into header + sections
# Header ends at first ## that is not the log section
header_end = 0
for i, line in enumerate(lines):
    if line.startswith('# K12 AI教育英文研究'):
        header_end = i
        break

result = lines[:header_end]
current_block = []
current_block_type = None  # 'header', 'section', 'entry'

i = header_end
while i < len(lines):
    line = lines[i]
    if line.startswith('## '):
        # Save current block
        if current_block and should_keep_block(current_block):
            result.extend(current_block)
        current_block = [line]
    elif line.startswith('**') or (current_block and current_block[0].startswith('## ')):
        current_block.append(line)
    else:
        if current_block:
            current_block.append(line)
        else:
            result.append(line)
    i += 1

if current_block and should_keep_block(current_block):
    result.extend(current_block)

# Update header with new date
new_content = '\n'.join(result)
new_content = new_content.replace(
    '最后更新：2026-03-25',
    '最后更新：2026-03-26'
)
new_content = new_content.replace(
    '2025-09-24至2026-03-24',
    '2025-09-25至2026-03-25'
)

# Count entries
entry_count = len(re.findall(r'^\([^\)]+\)$', new_content, re.MULTILINE))
header_count = len(re.findall(r'^\s*\*\*[0-9]+\.', new_content, re.MULTILINE))

print(f"Entries found: {entry_count} (title format) + {header_count} (numbered format)")
print(f"Total lines: {len(new_content.split(chr(10)))}")

# Write output
with open('/workspace/knowledge/master_k12_ai_research.md', 'w') as f:
    f.write(new_content)

print("Done! File updated.")
print(f"\nFirst 500 chars of result:")
print(new_content[:500])
