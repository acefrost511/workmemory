// Direct gateway API test via Node.js using openclaw's ws
import { createRequire } from 'module';
const require = createRequire(import.meta.url);

// Find ws in openclaw node_modules
import { readFileSync, existsSync } from 'fs';

function findWs() {
  const paths = [
    '/app/openclaw/node_modules/ws/index.js',
    '/app/openclaw/node_modules/.pnpm/ws/index.js',
  ];
  for (const p of paths) {
    if (existsSync(p)) return p.replace('/index.js', '');
  }
  return null;
}

const wsPath = findWs();
console.log('ws path:', wsPath);

// Use http instead - simpler
import http from 'http';

const TOKEN = "minimax-agent";

function httpCall(method, path, body) {
  return new Promise((resolve) => {
    const options = {
      hostname: '127.0.0.1',
      port: 8080,
      path,
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': TOKEN,
      }
    };
    
    let resolved = false;
    let timeout = setTimeout(() => {
      if (!resolved) {
        resolved = true;
        resolve({ error: 'timeout' });
      }
    }, 8000);
    
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        if (!resolved) {
          resolved = true;
          clearTimeout(timeout);
          try {
            resolve({ status: res.statusCode, body: JSON.parse(data) });
          } catch(e) {
            resolve({ status: res.statusCode, raw: data.slice(0, 500) });
          }
        }
      });
    });
    
    req.on('error', (e) => {
      if (!resolved) {
        resolved = true;
        clearTimeout(timeout);
        resolve({ error: e.message });
      }
    });
    
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

(async () => {
  const r1 = await httpCall('GET', '/api/v1/tools');
  console.log('GET /api/v1/tools:', JSON.stringify(r1).slice(0, 500));
  
  const r2 = await httpCall('GET', '/api/sessions');
  console.log('GET /api/sessions:', JSON.stringify(r2).slice(0, 500));
  
  const r3 = await httpCall('POST', '/api/sessions/spawn', {
    task: 'test spawn',
    runtime: 'subagent',
    runTimeoutSeconds: 60
  });
  console.log('POST /api/sessions/spawn:', JSON.stringify(r3).slice(0, 500));
})();
