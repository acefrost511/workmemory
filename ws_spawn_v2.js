const WebSocket = require('/app/openclaw/node_modules/ws');

const GATEWAY = 'ws://127.0.0.1:18789/api/v1';
const TOKEN = 'minimax-agent';

function spawnAgent(task, runtime, runTimeoutSeconds, agentId) {
    return new Promise((resolve, reject) => {
        const ws = new WebSocket(GATEWAY, {
            headers: { 'X-API-Key': TOKEN }
        });

        const msgId = Date.now();
        let resolved = false;
        let stderr = '';

        ws.on('open', () => {
            const params = { task, runtime, runTimeoutSeconds, mode: 'run' };
            if (agentId) params.agentId = agentId;
            
            const req = {
                jsonrpc: '2.0',
                id: msgId,
                method: 'sessions_spawn',
                params
            };
            process.stderr.write('SENDING: ' + JSON.stringify(req).slice(0, 200) + '\n');
            ws.send(JSON.stringify(req));
        });

        ws.on('message', (data) => {
            if (resolved) return;
            try {
                const resp = JSON.parse(data.toString());
                resolve(resp);
                resolved = true;
            } catch(e) {
                process.stderr.write('PARSE ERROR: ' + e.message + '\n');
            }
            ws.close();
        });

        ws.on('error', (e) => {
            if (!resolved) {
                reject(new Error('WS Error: ' + e.message));
                resolved = true;
            }
        });

        setTimeout(() => {
            if (!resolved) {
                ws.close();
                resolve({ error: 'timeout' });
                resolved = true;
            }
        }, 20000);
    });
}

// Test: spawn intel_01
(async () => {
    try {
        const result = await spawnAgent(
            '读取 /workspace/agents/intel_01/SOUL.md 并完整执行其搜索任务。今日日期：2026-04-02。搜索英文教育技术核心顶刊（Computers & Education / Education and Information Technologies / British Journal of Educational Technology），关键词：AI education + K-12。验证DOI，写入 /workspace/knowledge/原文库/ 。',
            'subagent',
            480,
            'intel_01'
        );
        console.log('RESULT:', JSON.stringify(result).slice(0, 500));
    } catch(e) {
        console.error('ERROR:', e.message);
    }
})();
