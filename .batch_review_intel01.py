#!/usr/bin/env python3
import subprocess, glob, os

pending_dir = "/workspace/knowledge/原文库/.pending"
results = []

for f in sorted(glob.glob(os.path.join(pending_dir, "intel01_*.md"))):
    fname = os.path.basename(f)
    try:
        r = subprocess.run(
            ["python3", "/workspace/.review.py", f],
            capture_output=True, text=True, timeout=30
        )
        results.append(f"✅ {fname}: {r.stdout.strip()} | {r.stderr.strip()}")
    except Exception as e:
        results.append(f"❌ {fname}: ERROR {e}")

for r in results:
    print(r)
