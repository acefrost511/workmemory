# Learnings Log (self-improving-agent)

This file captures learnings from corrections, errors, and best practice discovery.

---

## [LRN-20260318-001] correction

**Logged**: 2026-03-18 11:19:00+08:00
**Priority**: high
**Status**: pending
**Area**: config

### Summary
`edit` tool requires **exact text match including all whitespace and newlines** - repeatedly failed to match oldText exactly.

### Details
- **What went wrong**: When using `edit` tool to update files, I didn't get the oldText exactly matching including:
  - All whitespace (spaces, tabs)
  - All newlines (line breaks)
  - Leading/trailing empty lines
- **Result**: Edit failed with "Could not find the exact text"
- **This happened repeatedly** on the same task, same error pattern

### Suggested Action
1. **Before calling `edit`**: Always read the current content of the file to get the *exact* text
2. **Copy/paste exactly**: Do not guess or reformat - copy the exact text including all whitespace and newlines
3. **If in doubt**: Use `read` to read the file again, then copy the exact text
4. **If it still fails**: Use `write` to rewrite the entire file instead of `edit`

### Metadata
- Source: user_feedback
- Related Files: `/root/.openclaw/workspace/task_plan.md`
- Tags: tool, edit, matching, whitespace
- Pattern-Key: tool.edit.oldtext-exact-match
- Recurrence-Count: 2
- First-Seen: 2026-03-17
- Last-Seen: 2026-03-18
