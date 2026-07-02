---
name: context-engineering
description: Feed agents the right information at the right time. Token budgets, context selection, and progressive disclosure. Use when preparing context for Task tool delegation or when sessions get long.
user-invocable: false
---

# Context Engineering

Feed agents the right information at the right time. Too much context wastes tokens; too little causes errors.

## Principle

An agent's output quality is bounded by its input context. Engineering the context is as important as engineering the prompt.

## Context layers

### Layer 1: Always-on context (cheap, high-value)
- `AGENTS.md`: project conventions, build/test commands.
- `.factory/memories.md`: past decisions (injected by the memory hook at SessionStart).
- Current task description.

### Layer 2: On-demand context (loaded when relevant)
- Relevant source files (Read when the task touches them).
- Spec/plan/progress artifacts (Read when working on a feature).
- Reference checklists (loaded by skills when needed).

### Layer 3: Research context (fetched externally)
- WebSearch / FetchUrl results (when the task needs external info).
- Documentation (when the task needs API or library details).

## Token budget rules

1. **Prefer specific files over broad searches.** Reading 2 relevant files beats Grep across 100 files.
2. **Prefer summaries over raw dumps.** If delegating via Task tool, summarize what the subagent needs to know.
3. **Prefer progressive disclosure.** Start with a summary. Let the agent Read details only when needed.
4. **Avoid re-reading.** If you've read a file in this session, reference the content. Don't Read it again.

## Task tool delegation context

When delegating via Task tool, provide:
- **Goal**: what the subagent should accomplish.
- **Context**: the specific files/sections relevant (not the whole codebase).
- **Constraints**: what to avoid, what to preserve.
- **Expected output**: the format and content of the return.

Bad: "Review this code." (vague, subagent reads everything)
Good: "Review `src/auth/login.ts:30-80` for input validation. The function receives a raw password string. Check: null handling, length validation, injection risks. Report findings with line citations."

## Long session management

- **Use context compression**: Droid compresses automatically. The memory hook saves an anchored summary before compression.
- **Split work into subagents**: Long tasks bloat context. Delegate subtasks to fresh-context subagents.
- **Write artifacts, not context**: If you need info later, write it to an artifact file. Don't hold it in context.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "More context is always better" | No. Too much context dilutes signal and wastes tokens. |
| "I'll just pass the whole file" | Pass the relevant section. Large files waste tokens. |
| "The subagent can search itself" | Tell it where to look. Searching wastes its token budget. |
| "I'll re-read to be sure" | You read it this session. Reference it. Don't re-read. |
| "Context doesn't matter, the model is smart" | Smart models with bad context produce bad output. |

## Verification

- [ ] Subagent prompts include specific file paths and line ranges.
- [ ] No unnecessary file reads (re-reading files already in context).
- [ ] Artifacts used for cross-session info (not held in context).
- [ ] Token-heavy operations delegated to fresh-context subagents.

## Factory-native token efficiency patterns

### Spec Mode prevents false starts
Use Specification Mode (Shift+Tab) before complex work. Planning is cheaper than undoing:
- Without Spec Mode: Turn 1 wrong approach -> Turn 2 undo -> Turn 3 fix = 3x tokens.
- With Spec Mode: Turn 1 plan -> Turn 2 implement = 2x tokens, correct first time.

### IDE plugin eliminates context reads
With the Factory IDE plugin connected, Droid sees open files, errors, and selections immediately.
- Without IDE: Read file A -> Read file B -> Read file C -> work (4 tool calls).
- With IDE: work directly (0 extra tool calls).
- Always install the IDE plugin in VSCode/Cursor for maximum efficiency.

### Batch similar work
- Bad: 3 separate turns for similar tasks (context rebuilt each time).
- Good: 1 turn with all tasks + the pattern to follow.

### Specific prompts reduce exploration
- Bad: "Fix the bug in the auth module" (Droid reads 5 files to find it).
- Good: "Fix the timeout bug in src/auth/session.ts:45 where session expires after 5min instead of 24h" (direct fix).

### Model matching
Match model to task complexity:
- Simple edit -> Haiku/Droid Core (0.4x cost).
- Feature implementation -> Codex/Sonnet (0.7-1.2x).
- Architecture planning -> Opus (2x) with high reasoning.
- Bulk file processing -> Droid Core (0.12x).

### Monitor token usage
- Run `/cost` periodically to check session usage.
- Red flags: high read count (exploring too much), repeated grep calls (unclear target), repeated similar edits (failed attempts).
- Token budget guidelines: quick edit 5-15k, feature 30-80k, debugging 50-150k, planning 20-50k.

## Red Flags

- Passing entire large files to subagents instead of relevant sections.
- Re-reading files already read in the session.
- Holding reference info in context instead of writing to artifacts.
- Vague delegation prompts ("review this", "fix the bug").
- Not using progressive disclosure (loading everything upfront).
