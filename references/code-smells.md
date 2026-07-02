# Code Smells Baseline

A fixed set of Fowler code smells (_Refactoring_, ch.3) used by the **Standards axis** of `/review`. Each smell reads *what it is* -> *how to fix*; match it against the diff. These apply even when a repo documents nothing.

Two rules bind the baseline:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Skip anything tooling already enforces.

## The smells

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. -> Rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. -> Extract the shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. -> Move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). -> Bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. -> Give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. -> Replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. -> Gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. -> Split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the spec doesn't have. -> Delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. -> Hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. -> Cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. -> Drop the inheritance, use composition.

## How to apply

- Cite the smell by name and quote the hunk when reporting.
- Distinguish: documented-standard breaches can be hard violations; baseline smells are always judgement calls.
- A documented repo standard overrides the baseline (e.g. a repo that endorses pass-through adapters suppresses Middle Man).
- Skip anything the linter/formatter/type-checker already enforces; the review's job is what tooling misses.
