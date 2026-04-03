import json, hashlib, urllib.request, urllib.parse

# Read current config
with open('/root/.openclaw/openclaw.json') as f:
    raw_content = f.read()

config = json.loads(raw_content)

# Add feishu credentials to channels
config['channels'] = {
    "accounts": {
        "feishu": {
            "default": {
                "appId": "cli_a93fe76e9a781bc2",
                "appSecret": "Kmo5JuCjzusvVQBQv674VbRVK7GDn74v"
            }
        }
    }
}

# Compute new hash
new_content = json.dumps(config, indent=2)
new_hash = hashlib.sha256(new_content.encode()).hexdigest()

print(f"New hash: {new_hash}")
print(f"Config channels: {json.dumps(config.get('channels', {}), indent=2)}")

# Write to temp file
with open('/tmp/openclaw_patched.json', 'w') as f:
    json.dump(config, f, indent=2)

print("Written to /tmp/openclaw_patched.json")
print(f"Hash: {new_hash}")
