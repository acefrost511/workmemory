/**
 * Batch spawn all 12 intel agents via gateway RPC
 */
import { callGateway } from "/app/openclaw/dist/gateway/call.js";
import { GATEWAY_CLIENT_NAMES, GATEWAY_CLIENT_MODES } from "/app/openclaw/dist/utils/message-channel.js";
import { readFileSync } from "fs";

const GATEWAY_URL = process.env.OPENCLAW_GATEWAY_URL || "ws://localhost:8080";
const GATEWAY_TOKEN = process.env.OPENCLAW_GATEWAY_TOKEN || "";

// Load token from config
try {
  const { execSync } = await import("child_process");
  let configResult;
  try {
    configResult = execSync(`OPENCLAW_CONFIG_PATH=/workspace/.openclaw/openclaw.json openclaw config get --json 2>/dev/null || echo '{}'`, { timeout: 5000 });
    const config = JSON.parse(configResult.toString());
    console.log("Config loaded, gateway config:", JSON.stringify(config.gateway || config));
  } catch(e) {
    console.log("Could not load config via CLI:", e.message);
  }
} catch(e) {}

// Try to find gateway URL and token from environment or config
const cfg = JSON.parse(readFileSync("/workspace/.openclaw/openclaw.json", "utf8").replace(/^\s*\/\/.*$/gm, ""));
const gw = cfg?.gateway || {};
const wsUrl = gw?.remote?.url || process.env.OPENCLAW_GATEWAY_URL || "ws://localhost:8080";
const token = gw?.remote?.token || process.env.OPENCLAW_GATEWAY_TOKEN || "";

console.log("Gateway URL:", wsUrl);
console.log("Has token:", !!token);

async function spawnIntel(agentId) {
  const task = `读取 /workspace/agents/${agentId}/SOUL.md 并完整执行其搜索任务`;
  try {
    const result = await callGateway({
      url: wsUrl,
      token: token,
      method: "sessions_spawn",
      params: {
        task,
        runtime: "subagent",
        agentId,
        runTimeoutSeconds: 500,
        mode: "run",
        label: `intel_${agentId.replace("intel_", "")}`
      },
      expectFinal: false,
      timeoutMs: 30000,
      clientName: GATEWAY_CLIENT_NAMES.CLI,
      mode: GATEWAY_CLIENT_MODES.CLI,
    });
    console.log(`✓ Spawned ${agentId}:`, JSON.stringify(result).slice(0, 100));
    return result;
  } catch(e) {
    console.error(`✗ Failed to spawn ${agentId}:`, e.message);
    return null;
  }
}

const agents = [];
for (let i = 1; i <= 12; i++) {
  agents.push(`intel_${String(i).padStart(2, "0")}`);
}

console.log(`Spawning ${agents.length} intel agents...`);
const results = await Promise.allSettled(agents.map(id => spawnIntel(id)));
console.log("\nSummary:");
results.forEach((r, i) => {
  console.log(` ${agents[i]}: ${r.status === "fulfilled" ? "✓ spawned" : "✗ " + r.reason}`);
});
