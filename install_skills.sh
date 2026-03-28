#!/bin/bash
cd /workspace
SKILLS_DIR="skills"

# Install each skill, retry once on rate limit
install_skill() {
  slug="$1"
  name="$2"
  echo "Installing $name..."
  output=$(npx clawhub install "$slug" --dir "$SKILLS_DIR" 2>&1)
  if echo "$output" | grep -q "Rate limit"; then
    echo "Rate limited, retrying in 60s..."
    sleep 60
    output=$(npx clawhub install "$slug" --dir "$SKILLS_DIR" 2>&1)
  fi
  if echo "$output" | grep -q "Rate limit"; then
    echo "Rate limited again, retrying in 90s..."
    sleep 90
    output=$(npx clawhub install "$slug" --dir "$SKILLS_DIR" 2>&1)
  fi
  echo "$output"
  echo "---"
}

install_skill "planning-with-files" "planning-with-files"
install_skill "xiucheng-self-improving-agent" "xiucheng-self-improving-agent"
install_skill "using-superpowers" "using-superpowers"
install_skill "education" "education"
install_skill "notion" "notion"
install_skill "slack" "slack"

echo "ALL_DONE"
