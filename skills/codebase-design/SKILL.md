---
name: codebase-design
description: Shared vocabulary for designing deep modules — a lot of behaviour behind a small interface at a clean seam, testable through that interface. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.
user-invocable: false
---

# Codebase Design

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. Use this language and these principles wherever code is being designed or restructured. The aim is leverage for callers, locality for maintainers, and testability for everyone.

When exploring the codebase, read `CONTEXT.md` (if it exists) so module names match the project's domain language, and respect ADRs in the area you're touching.

## Glossary

Use these terms exactly — don't substitute "component," "service," "API," or "boundary." Consistent language is the whole point.

**Module** — anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package, or tier-spanning slice. *Avoid:* unit, component, service.

**Interface** — everything a caller must know to use the module correctly: the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics. *Avoid:* API, signature (too narrow).

**Implementation** — what's inside a module, its body of code. Distinct from **Adapter** below.

**Depth** — leverage at the interface: the amount of behaviour a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface, **shallow** when the interface is nearly as complex as the implementation.

**Seam** (Michael Feathers) — a place where you can alter behaviour without editing in that place; the *location* at which a module's interface lives. Where to put the seam is its own design decision, distinct from what goes behind it. *Avoid:* boundary (overloaded with DDD's bounded context).

**Adapter** — a concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance (what's inside).

**Leverage** — what callers get from depth: more capability per unit of interface they learn. One implementation pays back across N call sites and M tests.

**Locality** — what maintainers get from depth: change, bugs, knowledge, and verification concentrate in one place rather than spreading across callers.

## Deep vs shallow

**Deep module** = small interface + lots of implementation:

```
┌─────────────────────┐
│   Small Interface    │  <- Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation │  <- Complex logic hidden
│                     │
└─────────────────────┘
```

**Shallow module** = large interface + little implementation (avoid):

```
┌─────────────────────────────────┐
│       Large Interface           │  <- Many methods, complex params
├─────────────────────────────────┤
│      Thin Implementation        │  <- Just passes through
└─────────────────────────────────┘
```

When designing an interface, ask: Can I reduce the number of methods? Simplify the parameters? Hide more complexity inside?

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, mockable, swappable parts — they just aren't part of the interface. A module has **internal seams** (private to its implementation, used by its own tests) as well as the **external seam** at its interface.
- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a seam unless something actually varies across it.

## Designing for testability

Good interfaces make testing natural:

1. **Accept dependencies, don't create them.** Pass collaborators in as params; don't `new` them inside.
2. **Return results, don't produce side effects.** A pure function is trivial to test; a void that mutates a shared object is not.
3. **Small surface area.** Fewer methods = fewer tests needed. Fewer params = simpler test setup.

## Relationships

- A **Module** has exactly one **Interface** (the surface it presents to callers and tests).
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

## Rejected framings

- **Depth as ratio of implementation-lines to interface-lines** (Ousterhout): rewards padding the implementation. Use depth-as-leverage instead.
- **"Interface" as a language keyword or a class's public methods**: too narrow — interface here includes every fact a caller must know.
- **"Boundary"**: overloaded with DDD's bounded context. Say **seam** or **interface**.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "It's a thin wrapper but it might grow" | Speculative generality. Delete it; add it back when a real need shows. |
| "We need a seam for future flexibility" | One adapter = hypothetical seam. Don't add it until a second adapter exists. |
| "The interface has to expose everything" | Then the module isn't deep. Hide complexity behind fewer, simpler methods. |
| "Tests need to reach internals" | Then the interface is the wrong test surface. Redesign the seam. |

## Red Flags

- A module whose interface is nearly as large as its implementation.
- Introducing a seam/interface with only one adapter.
- Tests that reach past the interface (testing internals).
- Pass-through modules that survive the deletion test (complexity just moves, doesn't vanish).
