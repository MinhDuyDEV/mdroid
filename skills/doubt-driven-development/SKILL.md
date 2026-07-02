---
name: doubt-driven-development
description: Adversarial review technique. CLAIM -> EXTRACT -> DOUBT -> RECONCILE -> STOP. Use to stress-test assumptions, designs, and implementations before committing.
user-invocable: false
---

# Doubt-Driven Development

Adversarial review that stress-tests assumptions before they become bugs.

## The 5-step cycle

### 1. CLAIM
State the assumption or claim explicitly.
- "This function handles null inputs safely."
- "This API endpoint validates the user's permissions."
- "This algorithm is O(n)."

### 2. EXTRACT
Extract the evidence supporting the claim.
- What code proves this?
- What test verifies this?
- What documentation states this?

### 3. DOUBT
Attack the claim. Try to break it.
- What input would violate this claim?
- What edge case did we miss?
- What assumption is the claim built on?
- Is the evidence actually sufficient?

### 4. RECONCILE
- If the doubt is unfounded: the claim stands. Move on.
- If the doubt is valid: fix the code, add the test, or revise the claim.
- If uncertain: mark as a finding for follow-up.

### 5. STOP
- Stop when you can no longer produce a valid doubt.
- Don't stop at "probably fine". Stop at "I tried to break it and couldn't."

## When to apply

- **Before commit**: Doubt your claims about correctness.
- **During review**: Doubt the author's claims about security, performance, edge cases.
- **During planning**: Doubt the plan's assumptions about dependencies and scope.
- **On bugs**: Doubt your root cause hypothesis. The first hypothesis is often wrong.

## Example

**CLAIM**: "The login function validates the password before hashing."
**EXTRACT**: `src/auth/login.ts:42` calls `validatePassword()` before `hashPassword()`.
**DOUBT**: "What if `validatePassword()` throws? Does it still reach `hashPassword()`?"
**RECONCILE**: Read the code. `validatePassword()` throws on invalid input, and the throw is uncaught -> the function exits before `hashPassword()`. But is the error handled by the caller? Check `src/auth/login.ts:38` -> the route handler catches it and returns 400. Claim stands, but add a test for the throw path.
**STOP**: Tested the throw path. Claim verified. Move on.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "The claim is obviously true" | Obvious claims hide obvious bugs. Doubt it. |
| "I already tested it" | Tests test what you thought of. Doubt tests what you didn't. |
| "Doubting takes too long" | A 2-minute doubt saves a 2-hour debug session. |
| "I can't think of a way to break it" | Try harder. Or ask someone else to doubt it. |
| "The doubt is too unlikely" | Unlikely != impossible. Note it as a finding. |

## Verification

- [ ] Every critical claim has been through the 5-step cycle.
- [ ] Doubts that found issues resulted in fixes or tests.
- [ ] Claims that survived doubt have evidence (code + test).
- [ ] No claim was accepted on "probably fine".

## Red Flags

- Accepting a claim without extracting evidence.
- Stopping doubt at "seems fine" instead of "tried to break it and couldn't".
- Skipping doubt on security claims.
- Not adding tests for doubts that revealed edge cases.
- Doubting only the happy path.
