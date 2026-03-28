#!/bin/bash
SKILLS=(
  "paper-parse"
  "paper-summarize-academic"
  "arxiv-paper-processor"
  "human-writing"
  "business-writing"
  "xiucheng-self-improving-agent"
  "task-review-workflow"
  "clawhub-publisher"
  "daily-review-ritual"
)

for skill in "${SKILLS[@]}"; do
  echo "Installing $skill..."
  attempt=0
  while [ $attempt -lt 10 ]; do
    if cd /workspace && npx clawhub install "$skill" --dir /workspace/skills --force 2>&1 | grep -q "Installed"; then
      echo "✅ $skill"
      break
    else
      echo "Rate limited, waiting..."
      sleep 5
      attempt=$((attempt+1))
    fi
  done
  if [ $attempt -eq 10 ]; then
    echo "❌ Failed to install $skill after 10 attempts"
  fi
  sleep 5
done
echo "ALL DONE"
ls /workspace/skills/
