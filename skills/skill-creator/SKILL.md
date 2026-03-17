---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
author: Anthropic
version: 1.0.0
homepage: https://github.com/anthropics/skills/tree/main/skills/skill-creator
triggers:
  - "创建技能"
  - "技能开发"
  - "create a skill"
  - "improve a skill"
  - "test a skill"
  - "benchmark"
metadata: {"clawdbot":{"emoji":"🔧"}}
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

## At a high level

The process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
- Rewrite the skill based on feedback from the user's evaluation
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages.

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture. Extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output formats observed.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier
- **description**: When to trigger, what it does. This is the primary triggering mechanism - include both what the skill does AND specific contexts for when to use it.
- **compatibility**: Required tools, dependencies (optional)
- **the rest of the skill :)**

## Skill Writing Guide

### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited)

## Running and evaluating test cases

This section is one continuous sequence — don't stop partway through.

### Step 1: Spawn all runs (with-skill AND baseline) in the same turn

For each test case, spawn two subagents in the same turn — one with the skill, one without.

### Step 2: While runs are in progress, draft assertions

Don't just wait for the runs to finish — you can use this time productively. Draft quantitative assertions for each test case and explain them to the user.

### Step 3: As runs complete, capture timing data

When each subagent task completes, you receive a notification containing `total_tokens` and `duration_ms`. Save this data immediately.

### Step 4: Grade, aggregate, and launch the viewer

Once all runs are done:
1. Grade each run
2. Aggregate into benchmark
3. Do an analyst pass
4. Launch the viewer

---

## Improving the skill

This is the heart of the loop. You've run the test cases, the user has reviewed the results, and now you need to make the skill better based on their feedback.

### The iteration loop

After improving the skill:
1. Apply your improvements to the skill
2. Rerun all test cases into a new directory
3. Launch the reviewer
4. Wait for the user to review
5. Read the new feedback, improve again, repeat

---

## Description Optimization

The description field in SKILL.md frontmatter is the primary mechanism that determines whether Claude invokes a skill. After creating or improving a skill, offer to optimize the description for better triggering accuracy.

---

For the full, complete version of this skill (30+ pages), please refer to the original GitHub repository at https://github.com/anthropics/skills/tree/main/skills/skill-creator
