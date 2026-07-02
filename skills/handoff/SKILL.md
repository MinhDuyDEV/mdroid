---
name: handoff
description: Compact the current conversation into a handoff document so another agent session can continue the work. Use when a context window is full or you need to branch off (e.g. into a prototype session) and want a fresh session with the current conversation preserved.
user-invocable: true
disable-model-invocation: true
---

# Handoff

Write a handoff document summarising the current conversation so a fresh agent can continue the work. This is the bridge between context windows: you don't continue in place — you open a new session and reference that file to carry the context across.

`/handoff` forks (new session, old preserved); the Droid-native `compact` continues (same session, earlier turns summarised). Use `/handoff` when you want a fresh session but need the current conversation preserved; use `compact` at intentional breaks between phases when you don't mind losing the verbatim history.

## Process

### 1. Save to the OS temp directory

Write the handoff doc to the OS temp directory, not the current workspace, so it never lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows). Write to `$TMPDIR/mdroid-handoff-<slug>-<timestamp>.md` so each handoff gets a fresh file. Tell the user the absolute path.

### 2. What to include

Capture what a fresh agent needs to continue:

- **Goal**: what we're trying to accomplish (one or two sentences).
- **Done so far**: what's already implemented, verified, committed. Reference commits/PRs by hash/URL, don't re-summarise their diffs.
- **In progress**: what was mid-flight when the session ended. Be specific about the half-finished state.
- **Next steps**: the immediate next actions, in order.
- **Suggested skills**: which mdroid skills the next session should invoke (e.g. `/build`, `/verify`, `/fix`, `/review`). This is the most valuable section — name them.

### 3. Reference, don't duplicate

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead. The handoff doc points; it does not copy.

### 4. Redact secrets

Redact any sensitive information — API keys, passwords, personally identifiable information. If a secret appeared in the conversation, strip it from the handoff and note "[REDACTED]" in its place.

### 5. Argument handling

If the user passed an argument, treat it as a description of what the next session will focus on and tailor the doc accordingly (the "In progress" and "Next steps" sections especially).

## Output

Tell the user:

- The absolute path of the handoff file.
- A one-line summary of what it captures.
- The instruction: "Open a new session and tell the agent to read this file to continue."

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "I'll just keep going in this session" | If you're hitting the smart zone, degraded reasoning costs more than a fresh start. Hand off. |
| "The next agent can re-read everything" | Re-reading the whole transcript is expensive and lossy. A handoff doc is cheaper and sharper. |
| "I'll include the full diff in the doc" | Don't. Reference the commit/PR. The diff is already in git. |
| "It's fine to leave the API key in" | Never. Redact it. A handoff file lives in tmp, not the repo, but secrets still shouldn't sit in plaintext docs. |

## Red Flags

- Writing the handoff into the repo workspace instead of the OS temp directory.
- Duplicating diffs, specs, or plans that already exist as artifacts.
- Including unredacted secrets.
- No "Suggested skills" section (the next session won't know what to reach for).
- Not giving the absolute path to the file.
