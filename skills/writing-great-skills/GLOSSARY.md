# Glossary — Building Great Skills

The domain model for what makes a skill great. A skill exists to wrangle determinism out of a stochastic system; the root virtue is **Predictability**, and every term below is a lever on it. This is the disclosed reference for [`writing-great-skills`](SKILL.md).

The terms are grouped by axis: **Invocation** (how a skill is reached), **Information Hierarchy** (how its content is arranged), **Steering** (how the agent's runtime behaviour is shaped), and **Pruning** (how it is kept lean). Each **failure mode** lives beside the lever that cures it.

**Bold terms** in any definition are themselves defined in this glossary; find them by their heading.

## Predictability

The degree to which a skill makes the agent behave the same *way* on every run — the same process, not the same output (a brainstorming skill should *predictably* diverge; its tokens vary, its behaviour doesn't). The root virtue every other term serves — cost and maintainability are symptoms of it, not rivals.

_Avoid:_ consistency, reliability, robustness, output-determinism

## Invocation

How a skill is reached — and the two loads you pay for the choice.

### Model-Invoked

A skill that keeps its **description** field, so the agent can see it and fire it autonomously — and the human can still type its name, so model-invocation always *includes* user reach. Pays a permanent **context load** on every turn in exchange for that discoverability. Reachable by other skills. Pick model-invocation only when the agent must reach the skill on its own; if it never fires except by hand, drop the description and pay no context load.

_Avoid:_ ability, tool, capability

### User-Invoked

A skill with its **description** stripped — invisible to the agent and reachable only by the human typing its name. Trades agent-discoverability for zero **context load**. Because it has no description, nothing but the human can reach it: no other skill can fire it.

_Avoid:_ procedure, workflow, command

### Description

The skill's machine-readable trigger, and the one **context pointer** a **model-invoked** skill is forced to keep loaded at all times. Its mere presence *is* the invocation axis: keep it and the skill is model-invoked; delete it and the skill is **user-invoked**. The source of a model-invoked skill's **context load**.

_Avoid:_ frontmatter, summary

### Context Pointer

A reference held in the agent's context that names some out-of-context material and encodes the condition for reaching it. The **description** is the top-level context pointer (context window -> skill); pointers to disclosed files are the same object one level down. Its wording, not the target, decides *when* the agent reaches — and *how reliably*. A must-have target behind a weakly worded pointer is a variance bug: fix the wording first, and inline the material only if sharpening fails.

_Avoid:_ link, reference, import

### Context Load

The cost a **model-invoked** skill imposes on the agent's context window — its **description**, always loaded, spending both tokens and attention. What **user-invoked** skills escape by having no description, and the brake on splitting into more model-invoked skills.

_Avoid:_ token cost, context bloat

### Cognitive Load

The cost a **user-invoked** skill imposes on the human — what they must hold in their head: which skills exist and when to reach for each. What **model-invocation** removes by being agent-discoverable. Not a cost to minimise: it is the price of human agency. Spend it where human judgement matters; remove it where it does not.

_Avoid:_ human index, burden, overhead

### Router Skill

A **user-invoked** skill whose job is to point at your other user-invoked skills — naming each and when to reach for it — so the human has one skill to remember instead of many. It can only hint, never fire them. The cure for **cognitive load** when user-invoked skills multiply.

_Avoid:_ dispatcher, menu, registry

### Granularity

How finely you divide skills. Finer division spends one of the two loads: more **model-invoked** skills spend **context load**; more **user-invoked** skills spend **cognitive load**. Two cuts guide the division. By **invocation**, split off a model-invoked skill where you have a distinct **leading word** to trigger it. By **sequence**, split a run of **steps** where a step's **post-completion steps** need hiding.

_Avoid:_ chunking, modularity

## Information Hierarchy

How a skill's content is arranged, and how far down the ladder each piece sits.

### Information Hierarchy

A skill's content ranked by how immediately the agent needs it — a single ladder, produced by two cuts: in-file or behind a pointer, and step or reference. The rungs:

- **Steps** — in-file, primary
- **Reference**, in-file — secondary
- **Reference**, disclosed — behind a **context pointer**

A skill with no **steps** uses just the bottom two rungs — often a legitimately flat peer-set, which is a fine arrangement, not a smell. When a skill has steps, in-file reference that should be disclosed buries them and turns attending to them into a coin-flip. Keep the top of the ladder legible; push down it whatever you can.

_Avoid:_ structure, organization, layout

### Steps

The ordered actions the agent performs — when a skill has them, the primary tier of its content. Not every skill has steps: a skill can be all steps, all **reference**, or both. Every step ends on a **completion criterion**.

_Avoid:_ workflow, instructions, choreography

### Reference

Material the agent refers to on demand — definitions, facts, parameters, examples, conditional instructions. Reached via **context pointers**, and the prime candidate for **progressive disclosure**.

_Avoid:_ supporting material, docs, background

### External Reference

**Reference** that lives outside the skill system — a plain file, no description, no steps, not invocable — that any skill can point at. The home for shared reference that needn't fire on its own, and the only shared home two **user-invoked** skills can use, since neither has a description and so neither can fire the other.

_Avoid:_ doc, resource, knowledge base

### Progressive Disclosure

Moving **reference** down the ladder — out of SKILL.md and behind a **context pointer** — so the top stays legible. Not primarily a token optimisation; it is how the **information hierarchy** is protected. Licensed by **branching**: disclose what only some branches need, inline what every path needs.

_Avoid:_ lazy loading, chunking

### Co-location

Keeping the material an agent needs at once in one place — a concept's definition, rules, and caveats under a single heading — so reading one part brings its neighbours with it. Distinct from **Duplication**: that repeats one meaning in two places, where scattering fragments a single meaning across many.

_Avoid:_ grouping, clustering, cohesion

### Sprawl

_Failure mode._ A skill that is simply too long — too many lines in SKILL.md — independent of whether they are stale or repeated. The cure is the **information hierarchy**: push **reference** down behind **context pointers**, and split by **branch** or sequence so each path carries only what it needs. Distinct from **sediment** (length from stale accumulation) and **duplication** (length from repeated meaning) — sprawl is length itself.

_Avoid:_ bloat, length, size, verbosity

## Steering

The levers that shape the agent's runtime behaviour toward **Predictability**.

### Branch

A distinct way a skill can be invoked — a case the skill handles — so different runs take different paths through it.

_Avoid:_ path, case, fork

### Leading Word

A compact concept already living in the model's pretraining, that the agent thinks with while running the skill. It encodes a behavioural principle in the fewest possible tokens by invoking priors the model already holds (e.g. *tight* loop, *deep module*, *seam*, *tracer bullet*, *red*). Repeated as a token, never as a sentence, it accumulates a distributed definition across the skill and anchors a whole region of behaviour. Coining your own works if you define it clearly, but a made-up word recruits no priors — you pay in definition tokens what a pretrained word gives free. Reach for an existing word first.

A leading word serves **predictability** twice. In the body it anchors *execution* — the agent reaches for the same behaviour every time the concept appears. In the **description** it anchors *invocation* — when the same word lives in your prompts, docs, and codebase, the agent links that shared language to the skill and fires it more reliably.

_Avoid:_ keyword, term, motif

### Completion Criterion

The condition that tells the agent a unit of work is done. Two properties make it a lever. Its **clarity** (can the agent tell done from not-done?) resists **premature completion** — a vague bound lets the agent declare done and slip to the next step. Its **demand** (how much it requires) sets **legwork** — "every modified model accounted for" forces thorough work where "produce a change list" does not. The strongest criteria are both checkable and exhaustive.

_Avoid:_ done condition, exit condition, stopping rule

### Legwork

The work an agent does behind the scenes within a single step — reading files, exploring the codebase, making changes. It lives below the step structure: never written as its own step, latent in the wording, controlled by the agent. Raised by a **leading word** (*comprehensive*, *thorough*) or a **completion criterion** that demands exhaustive work. Goes thin when that demand is missing or when **premature completion** cuts the step short.

_Avoid:_ scope, effort, diligence, coverage

### Post-Completion Steps

The **steps** that follow the current step. Visible, they pull the agent forward into **premature completion** — the more it sees, the stronger the tug; the defence is to hide them by splitting the sequence of steps into two.

_Avoid:_ horizon, fog of war, lookahead

### Premature Completion

_Failure mode._ Ending the current step before it is genuinely done, because the agent's attention slips to being done rather than to the work. A tug-of-war between visible **post-completion steps** (the pull forward) and the **completion criterion**'s clarity (the resistance). Two levers hold a step that does, but reach for them in order: **sharpen the bound first** — it is local and cheap. Only when the criterion is irreducibly fuzzy *and* you actually observe the rush do you **hide the later steps** — and hiding only works across a real context boundary (a user-invoked hand-off or a subagent dispatch).

_Avoid:_ premature closure, the rush, rushing, shortcutting

## Pruning

Keeping a skill lean — each remedy paired with the failure it cures.

### Single Source of Truth

The desired state where each meaning lives in exactly one authoritative place, so a change to the skill's behaviour is a change in one place. **Duplication** is its violation.

_Avoid:_ home, canonical location

### Duplication

_Failure mode._ The same meaning given more than one **single source of truth**. It costs maintenance, costs tokens, and inflates prominence — repeating a meaning weights it on the ladder past its real rank. The accidental inverse of a **leading word**, which raises attention on purpose by repeating a token, never the meaning.

_Avoid:_ repetition, redundancy

### Relevance

Whether a line still bears on what the skill does — the lens for what to keep. A line loses relevance either by never bearing on the task or by going stale. Shorter skills are easier to keep relevant, because each line is cheaper to check. Distinct from **no-op**: relevance asks whether a line bears on the task, not whether it changes behaviour.

_Avoid:_ load-bearing, staleness, freshness

### Sediment

_Failure mode._ Layers of old content that settle in a skill and are never cleared, because adding feels safe and removing feels risky. The default fate of any skill without a pruning discipline; the slow erosion of **relevance**.

_Avoid:_ accretion, bloat, cruft, rot

### No-Op

_Failure mode._ An instruction that changes nothing because the model already does it by default — you pay load to tell the agent what it would do anyway. The test: does a line change behaviour versus the default? A line can be perfectly **relevant** and still be a no-op.

A leading word is a *technique*; No-Op is a *verdict* on a line — and they cross. A leading word too weak to beat the default is a no-op (*be thorough* when the agent is already thorough-ish), and the fix is a stronger word that passes the verdict (*relentless*), not a different technique. So the No-Op test is also how you grade whether a leading word is earning its repetitions. **This is model-relative**, not reader-relative: two people disagreeing over whether a line is a no-op disagree about the default, and settle it by running the skill, not by debate. mdroid targets `model: inherit` and may run models other than Claude — verify each leading word against the model actually in use before committing to it.

_Avoid:_ redundant instruction, restating the obvious, belaboring
