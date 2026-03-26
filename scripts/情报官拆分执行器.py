#!/usr/bin/env python3
"""
情报官任务拆分执行器 v3（修复版）
- 使用 utf-8-sig 读取源文件（自动去除BOM）
- 匹配规则：信念行使用 startswith 而非精确匹配
"""
import os, re, json

WORKSPACE = "/workspace"
DRAWER_DIR = f"{WORKSPACE}/knowledge/beliefs"
SOURCE_FILE = f"{DRAWER_DIR}/ALL_BELIEFS_CONTENT.md"
PROGRESS_FILE = f"{WORKSPACE}/memory/情报官进度.json"

DRAWER_NAMES = {
    1: "信念1-AI教育观.md", 2: "信念2-教师角色观.md",
    3: "信念3-学习本质观.md", 4: "信念4-教育公平观.md",
    5: "信念5-学生发展观.md", 6: "信念6-课堂教学观.md",
    7: "信念7-教育评价观.md", 8: "信念8-家校协同观.md",
    9: "信念9-教育伦理观.md", 10: "信念10-教育技术观.md",
    11: "信念11-教育创新观.md", 12: "信念12-教育政策观.md",
    13: "信念13-未来教育观.md",
}

BELIEF_LABELS = {
    1:"信念一", 2:"信念二", 3:"信念三", 4:"信念四", 5:"信念五",
    6:"信念六", 7:"信念七", 8:"信念八", 9:"信念九", 10:"信念十",
    11:"信念十一", 12:"信念十二", 13:"信念十三",
}

BATCHES = [[1,2,3,4], [5,6,7,8], [9,10,11,12,13]]

def load_source():
    with open(SOURCE_FILE, 'r', encoding='utf-8-sig') as f:  # utf-8-sig removes BOM
        return f.read()

def get_belief_section(source, belief_num):
    target = BELIEF_LABELS[belief_num]
    lines = source.split('\n')
    start = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == f'# {target}' or stripped.startswith(f'# {target}：'):
            start = i; break
    if start == -1: return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        s = lines[i].strip()
        if s.startswith('# 信念') and not s.startswith('### Collision'):
            end = i; break
    return '\n'.join(lines[start:end])

def inject_to_drawer(belief_num, new_section):
    drawer_file = f"{DRAWER_DIR}/{DRAWER_NAMES[belief_num]}"
    if not os.path.exists(drawer_file):
        return False, f"文件不存在"
    with open(drawer_file, 'r', encoding='utf-8') as f:
        content = f.read()
    marker = "## 素材积累区"
    if marker not in content:
        return False, "无素材积累区"
    marker_pos = content.index(marker)
    after_marker = marker_pos + len(marker)
    rest = content[after_marker:]
    m = re.search(r'\n## ', rest)
    section_end = after_marker + m.start() if m else len(content)
    new_content = content[:marker_pos] + marker + '\n\n' + new_section.strip() + '\n\n' + content[section_end:]
    with open(drawer_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True, "成功"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            raw = json.load(f)
        # 兼容新旧格式
        if isinstance(raw.get("done"), list):
            return raw
    return {"done": [], "batch_results": {}}

def save_progress(p):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(p, f, ensure_ascii=False, indent=2)

def run():
    os.makedirs(f"{WORKSPACE}/memory", exist_ok=True)
    p = load_progress()
    source = load_source()
    total_done = []

    for batch_idx, beliefs in enumerate(BATCHES, 1):
        batch_key = f"batch_{batch_idx}"
        print(f"\n{'='*40}")
        print(f"批次{batch_idx}：信念{beliefs} {'[已完成]' if batch_key in p.get('done',[]) else ''}")
        if batch_key in p.get('done', []):
            total_done.extend(beliefs); continue

        results = {}
        for b in beliefs:
            section = get_belief_section(source, b)
            if section is None:
                results[b] = "来源缺失"; print(f"  信念{b}：❌ 来源缺失"); continue
            ok, msg = inject_to_drawer(b, section)
            results[b] = "ok" if ok else msg
            print(f"  信念{b}：{'✅' if ok else '❌'} {msg}")

        ok_count = sum(1 for v in results.values() if v == "ok")
        rate = ok_count / len(beliefs)
        print(f"  成功率：{ok_count}/{len(beliefs)} = {rate:.0%}")
        if rate >= 0.8:
            p.setdefault("done", []).append(batch_key)
            p["batch_results"][batch_key] = results
            total_done.extend([b for b,r in results.items() if r == "ok"])
            print(f"  ✅ 批次{batch_idx}标记完成")
        else:
            p["batch_results"][batch_key] = {"status": "partial", "rate": rate, "results": results}

    save_progress(p)
    print(f"\n{'='*40}")
    print(f"📊 最终：{len(total_done)}/13 个抽屉已完成")
    if len(total_done) == 13: print("🎉 全部完成！")
    else: print(f"📋 剩余：{set(range(1,14))-set(total_done)}")

if __name__ == '__main__':
    run()
