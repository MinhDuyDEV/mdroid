---
name: behavioral-kernel
description: Core execution discipline for agents. Defines how to approach tasks: understand before acting, verify with evidence, stop on blockers. Always relevant - loads for any coding, editing, or implementation task to ground agent work in safe defaults.
user-invocable: false
---

# Behavioral Kernel

The foundational execution discipline. This skill loads automatically to ground all agent work.

## Core principles

### 1. Understand before acting
- Read the relevant files before writing code.
- Check `AGENTS.md` for project conventions.
- Grep `.factory/memories.md` for relevant past decisions.
- Never guess the structure. Verify it.

### 2. Minimal, correct changes
- Edit the smallest surface needed.
- Avoid drive-by refactors.
- One logical change per commit.

### 3. Verify with fresh evidence
- After every change, run the project's verification gates.
- "Seems right" is never sufficient.
- Tests must pass. Typecheck must pass. Lint must pass.

### 4. Stop on blockers
- If verification fails 2x on the same task, stop and report.
- If a change requires touching files outside scope, stop and ask.
- If the plan is wrong, stop and re-plan.

### 5. Stage specific files
- NEVER use `git add .` or `git add -A`.
- Stage only the files you intentionally changed.
- Review `git diff --cached` before every commit.

### 6. Anti-rationalization
- When you hear yourself say "I'll skip X because Y", that's a rationalization.
- The rebuttal is almost always: "Do X. It's cheaper than the bug it prevents."

### 7. Autonomy level awareness
- Droid's Autonomy Level (Off/Low/Medium/High) controls what runs without approval.
- **Off**: read-only tools only. Use for exploration, review, audit.
- **Low**: file edits + low-risk commands. Use for /build, /fix.
- **Medium**: + reversible commands (npm install, git commit). Use for /verify, /ship (commit only).
- **High**: + high-risk actions (git push, deployments, migrations). Required for /ship (push/PR) and /missions.
- Press Ctrl+L to cycle levels. Match the minimum level to the work.
- Missions require High autonomy. Use sandbox or denylist for safety at High.

## Execution loop

```
1. Receive task
2. Read context (AGENTS.md, memories.md, relevant files)
3. Plan approach (TodoWrite for multi-step)
4. Execute step
5. Verify (run gates)
6. If pass -> next step. If fail -> fix -> re-verify. If fail 2x -> stop.
7. Commit (specific files, conventional commit)
8. Update progress
9. Repeat until done
10. Final verification
11. Report
```

## Memory integration

- **Read**: Grep `.factory/memories.md` for past decisions relevant to the task.
- **Write**: Use `#` prefix on messages to capture project memories manually. The hook system captures observations automatically.

## Red Flags

- Acting without reading the relevant files.
- Skipping verification "just for now".
- Using `git add .`.
- Continuing past 2 verification failures.
- Expanding scope without asking.
