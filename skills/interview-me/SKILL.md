---
name: interview-me
description: One-question-at-a-time structured interview to extract requirements and constraints. Better than batch questions for complex topics. Use when requirements are unclear or need deep exploration.
user-invocable: true
---

# Interview Me

Structured, one-question-at-a-time interview to extract requirements and constraints.

## When to use

- Requirements are vague or incomplete.
- The feature has many unknowns.
- You need to understand constraints, priorities, and edge cases.
- The user isn't sure what they want yet.

## Process

Ask ONE question at a time. Wait for the answer. Then ask the next.

### Opening
"Let me interview you to understand this better. I'll ask one question at a time."

### Question sequence

1. **Goal**: What's the outcome you want? (user-visible, measurable)
2. **Users**: Who uses this? (roles, personas)
3. **Current state**: What happens today? (workaround, manual process, nothing)
4. **Trigger**: When does this need to happen? (event, user action, schedule)
5. **Inputs**: What information goes in? (data, format, source)
6. **Outputs**: What comes out? (data, format, destination)
7. **Constraints**: What limits apply? (performance, compatibility, budget, timeline)
8. **Edge cases**: What unusual situations should we handle? (empty, null, huge, concurrent)
9. **Out of scope**: What's explicitly NOT included?
10. **Priority**: If we can only ship one thing first, what is it?
11. **Done**: How will you know this is complete? (observable, testable)

### Adapt
- Skip questions that are already answered.
- Add follow-up questions based on answers.
- Don't rigidly follow the list. Let the conversation flow.

### Closing
"Based on our conversation, here's what I understand: [summary]. Does this capture it?"

If yes -> proceed to `/spec` with the gathered info.
If no -> continue interviewing.

## Rules

1. **One question at a time.** Never batch. The answer to Q1 might change Q2.
2. **Listen.** Don't pre-plan all questions. Adapt based on answers.
3. **Probe.** If an answer is vague, ask "can you give an example?"
4. **Confirm.** Periodically summarize what you've heard.
5. **Don't lead.** Don't suggest answers. Ask open questions.
6. **Stop when done.** If you have enough to write a spec, stop interviewing.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "I'll ask all questions at once to save time" | Answers change later questions. One at a time. |
| "I know what they want" | You're guessing. Ask. |
| "The user seems unsure, I'll decide for them" | Probe deeper. "Unsure" means you haven't found the right question. |
| "This is taking too long" | Better requirements now save rework later. |
| "I have enough after 3 questions" | Maybe. Confirm with a summary before stopping. |

## Red Flags

- Batching multiple questions.
- Suggesting answers instead of asking open questions.
- Not summarizing before proceeding.
- Stopping before "done" criteria is clear.
- Ignoring vague answers (probe them).
