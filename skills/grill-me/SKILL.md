---
name: grill-me
description: Interrogate requirements to find gaps and contradictions. Aggressive questioning to stress-test a plan or spec before implementation. Use when a spec or plan feels too optimistic.
user-invocable: true
---

# Grill Me

Interrogate requirements and plans to find gaps before they become bugs.

## When to use

- A spec feels too optimistic or vague.
- A plan has tasks without verification.
- You're about to implement something complex and want to stress-test the approach.
- The user wants their idea challenged before committing.

## Process

Read the spec or plan, then fire questions aggressively. Don't accept "we'll figure it out later".

### Requirement grilling

1. **What happens when X fails?** For every happy-path step, ask about the error path.
2. **Who uses this and how?** Challenge assumptions about users and usage patterns.
3. **What's the scale?** Challenge assumptions about volume, concurrency, data size.
4. **What depends on this?** Challenge assumptions about isolation. What breaks if this changes?
5. **What if this is late?** Challenge schedule assumptions. What's the minimum viable version?
6. **What if this is wrong?** Challenge the core assumption. If the feature is wrong, how do we know? How do we pivot?

### Plan grilling

1. **How do you verify task T?** Every task must have a verification command. No verification = no task.
2. **What if task T takes 10x longer?** Identify the riskiest tasks. What's the fallback?
3. **What if dependency D isn't ready?** For each dependency, what's the plan if it's delayed?
4. **What's the rollback?** If the implementation goes wrong, how do we undo?
5. **What does "done" look like?** Challenge the completion criteria. Is it observable?

### Spec grilling

1. **Is this one feature or three?** Challenge scope. Split if it's multiple features.
2. **What's explicitly out of scope?** If nothing is out of scope, scope creep is guaranteed.
3. **Can this be tested?** Every success criterion must be observable and testable.
4. **What's the simplest version?** Challenge complexity. What's the MVP?
5. **What if we don't build this?** Challenge necessity. Is this actually needed?

## Output

After grilling, produce:

```
## Grill Results

### Gaps found
1. [gap] - [what's missing and why it matters]
2. [gap]

### Contradictions
1. [contradiction] - [what conflicts with what]

### Risks
1. [risk] - [likelihood] - [impact] - [mitigation]

### Recommendations
1. [what to change before proceeding]
```

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "We've thought of everything" | Then the grilling will be fast. Let's verify. |
| "Edge cases are unlikely" | Unlikely != impossible. What's the cost if they happen? |
| "We'll handle errors during implementation" | Error handling is a requirement, not an implementation detail. |
| "The plan is solid" | Then it survives grilling. Let's test it. |
| "Grilling takes too long" | Grilling is cheaper than building the wrong thing. |

## Red Flags

- Accepting "we'll figure it out later" as an answer.
- Not grilling error paths and failure modes.
- Not questioning the core assumption (what if this is wrong?).
- Not identifying the riskiest tasks.
- No gaps found (you didn't grill hard enough).
