#!/usr/bin/env python3
"""
Spawn intel agents and run full intelligence pipeline for 2026-04-02
"""
import subprocess
import json
import time
import os

# Gateway info - use the minimax-agent token
GATEWAY_URL = "http://127.0.0.1:8080"
TOKEN = "minimax-agent"

def api_call(method, path, data=None):
    import urllib.request, urllib.error
    req = urllib.request.Request(f"{GATEWAY_URL}{path}")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-API-Key", TOKEN)
    if data:
        req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode()[:500]}
    except Exception as e:
        return {"error": str(e)}

# First, check what's available
print("=== Checking gateway ===")
result = api_call("GET", "/api/v1/status")
print(json.dumps(result, indent=2)[:500])

# Check what tools/sessions are available
result2 = api_call("GET", "/api/v1/tools")
print("\n=== Tools ===")
print(str(result2)[:500])

# Check sessions
result3 = api_call("GET", "/api/sessions")
print("\n=== Sessions ===")
print(str(result3)[:500])
