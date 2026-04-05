#!/usr/bin/env python3
import subprocess, glob, os, shutil

src = "/workspace/knowledge/原文库"
dst = "/workspace/knowledge/原文库/.pending"

# Ensure .pending dir exists
os.makedirs(dst, exist_ok=True)

# Move intel01 files to .pending
moved = []
for f in glob.glob(os.path.join(src, "intel01_*.md")):
    basename = os.path.basename(f)
    dst_path = os.path.join(dst, basename)
    shutil.move(f, dst_path)
    moved.append(basename)

print(f"Moved {len(moved)} files to .pending/")
for m in moved:
    print(f"  - {m}")

# Run review on all in .pending
results = []
for f in sorted(glob.glob(os.path.join(dst, "intel01_*.md"))):
    fname = os.path.basename(f)
    try:
        r = subprocess.run(
            ["python3", "/workspace/.review.py", f],
            capture_output=True, text=True, timeout=30
        )
        out = r.stdout.strip()
        err = r.stderr.strip()
        results.append(f"REVIEW {fname}: {out} | {err}")
    except Exception as e:
        results.append(f"ERROR {fname}: {e}")

for r in results:
    print(r)

# Summary
start_ts = 1775404074
import time
elapsed = time.time() - start_ts
print(f"\n=== SUMMARY ===")
print(f"Found: 3 papers")
print(f"Moved to .pending: {len(moved)}")
print(f"Reviews run: {len(results)}")
print(f"Elapsed: {int(elapsed)}s")
