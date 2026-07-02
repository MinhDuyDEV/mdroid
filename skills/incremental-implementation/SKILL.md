---
name: incremental-implementation
description: Thin vertical slices for incremental delivery. Each slice is independently shippable and verifiable. Use when planning and implementing features to avoid big-bang deliveries.
user-invocable: false
---

# Incremental Implementation

Deliver value in thin, vertical slices. Each slice is end-to-end and independently verifiable.

## Principle

A **vertical slice** cuts through all layers: UI -> API -> logic -> data. It delivers a small piece of user-visible value, end to end.

A **horizontal layer** builds one tier completely before the next (all UI, then all API, then all logic). This delays verification and integration.

**Always prefer vertical slices.**

## Why vertical slices?

1. **Early verification**: You can test the full path immediately.
2. **Early feedback**: Users/stakeholders see value sooner.
3. **Risk reduction**: Integration issues surface early, not at the end.
4. **Shippable**: Each slice can ship independently.
5. **Focused**: Each slice has a clear "done" criterion.

## How to slice

1. **Identify the core path**: What's the minimum end-to-end flow that delivers value?
2. **Cut the first slice**: That core path, with stubs for edge cases.
3. **Cut subsequent slices**: Each adds a capability or handles an edge case.
4. **Each slice ships**: Don't accumulate slices. Ship each one.

## Example

Feature: "User can search products by name, filter by category, sort by price."

- **Slice 1**: Search by name (UI input -> API query -> DB query -> results displayed). Ship.
- **Slice 2**: Filter by category. Ship.
- **Slice 3**: Sort by price. Ship.

NOT:
- All UI (search + filter + sort) -> all API -> all DB. (Horizontal. Bad.)

## Slice criteria

A good slice:
- [ ] End-to-end (touches all necessary layers).
- [ ] Independently verifiable (has its own test).
- [ ] Independently shippable (doesn't break existing functionality).
- [ ] Small (implementable in one session).
- [ ] User-visible (delivers observable value).

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "I'll build the API first, then the UI" | That's horizontal. Build the first vertical slice instead. |
| "The slice is too thin to be useful" | Thin slices ship. Thick slices stall. Ship thin. |
| "I need all features before it's useful" | Rarely true. The first slice usually has value. |
| "Integration can wait until the end" | Integration issues grow. Integrate per slice. |
| "Edge cases need to be in the first slice" | No. First slice = core path. Edge cases = later slices. |

## Verification

- [ ] Each slice has an end-to-end test.
- [ ] Each slice ships independently.
- [ ] No slice depends on a future slice to be useful.
- [ ] Slices are ordered by value (highest value first).

## Red Flags

- Building a complete layer before any end-to-end path works.
- A slice that can't be tested without the next slice.
- A slice that touches only one layer (it's horizontal, not vertical).
- Accumulating multiple slices before shipping any.
