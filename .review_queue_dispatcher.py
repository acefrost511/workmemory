#!/usr/bin/env python3
"""
方案B：轻量级审核调度器
读取 .pending/.queue 文件，非空则spawn reviewer处理，清空队列
"""
import os, json, subprocess, time

QUEUE_FILE = '/workspace/knowledge/原文库/.pending/.queue'
PENDING_DIR = '/workspace/knowledge/原文库/.pending/'

def log(msg):
    ts = time.strftime('%H:%M:%S')
    print(f'[{ts}] {msg}')

def read_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def write_queue(files):
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        for fn in files:
            f.write(fn + '\n')

def spawn_reviewer(filename):
    """生成并执行spawn reviewer的命令"""
    filepath = PENDING_DIR + filename
    
    # 根据文件类型判断用哪个reviewer
    is_en = any(d in filename for d in [
        '10.1016', '10.1007', '10.1080', '10.3390', '10.48550',
        '10.1111', '10.1186', '10.3389', '10.1038', '2502.', '2503.',
        '2504.', '2505.', '2506.', '2507.', '2508.', '2509.', '2510.',
        '2512.', '2601.', '2602.', '2603.', '2604.', 'iJET'
    ])
    
    reviewer_id = 'reviewer_en_01' if is_en else 'reviewer_cn_02'
    
    task = (
        f'审核单篇文件：{filepath}\n'
        f'按 reviewer_en_01 或 reviewer_cn_02 SOUL.md 标准执行审核。\n'
        f'通过则移到原文库，失败则标记删除。\n'
        f'只审核这1篇，审核完立即退出。'
    )
    
    cmd = [
        'node', '-e',
        f'''
const {{ spawn }} = require("child_process");
const j = JSON.stringify({{
    task: `{task}`,
    runtime: "subagent",
    agentId: "{reviewer_id}",
    runTimeoutSeconds: 120,
    mode: "run"
}});
process.stdout.write(j);
'''
    ]
    return cmd, reviewer_id

def main():
    files = read_queue()
    if not files:
        log('队列为空，无待审核文件')
        return
    
    log(f'队列有 {len(files)} 个文件，开始spawn reviewer')
    
    # 清空队列（防止重复处理）
    write_queue([])
    
    # 对每个文件spawn reviewer（最多同时5个，超出则分批）
    batch_size = 5
    spawned = []
    for i, fn in enumerate(files):
        log(f'Spawn reviewer {i+1}/{len(files)}: {fn}')
        pid = subprocess.Popen(
            ['node', '/app/agents/sessions_spawn_tool.js',
             json.dumps({
                 'task': f'审核文件：{PENDING_DIR}{fn}，按SOUL.md标准验证，通过移到原文库，失败删除。只审1篇。',
                 'runtime': 'subagent',
                 'agentId': 'reviewer_en_01' if any(d in fn for d in ['10.','2502','2503','2504','2505','2506','2507','2508','2509','2510','2512','2601','2602','2603','2604','iJET','intel_03_','intel_08_','intel_09_','intel_10_','intel_11_']) else 'reviewer_cn_02',
                 'runTimeoutSeconds': 120,
                 'mode': 'run'
             })],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        spawned.append(pid)
        if len(spawned) >= batch_size:
            log(f'已达5并发上限，等待...')
            for p in spawned:
                p.wait()
            spawned = []
        time.sleep(1)
    
    # 等待剩余spawn完成
    for p in spawned:
        p.wait()
    
    log(f'全部 {len(files)} 个文件已spawn完成')

if __name__ == '__main__':
    main()
