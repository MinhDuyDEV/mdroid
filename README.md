# mdroid

> Production-grade engineering workflow for Factory Droid. Combines OpenCodeKit artifacts lifecycle, agent-skills anti-rationalization patterns, and Superpowers TDD discipline, optimized for Droid-native features. Includes a 5-layer automated memory system with cross-session learning, zero LLM tokens.

## What is mdroid?

**mdroid** is a Factory Droid plugin that packages a production-grade engineering workflow. It combines the best of three kits without duplicating what the Droid ecosystem already provides:

- **OpenCodeKit**: artifacts lifecycle, multi-agent orchestration, AGENTS.md behavioral kernel
- **agent-skills**: anti-rationalization tables, Red Flags, verification gates, review personas, reference checklists
- **Superpowers**: TDD discipline, subagent-driven development, git-worktree isolation
- **Droid native**: Task tool, hooks, MCP, Missions, context compression, session navigation

### Key innovation: 5-layer memory system

A fully automatic, cross-session memory system built with Droid hooks + Python. No LLM tokens used (heuristic only: TF-IDF, BM25, regex). Replaces OpenCodeKit's 4-tier TypeScript memory plugin (20 files) with 7 hooks + 5 Python lib modules.

```
Session Start → inject relevant memories (BM25)
During Session → track file artifacts
Before Compression → save anchored summary
Session Stop → distill transcript (TF-IDF) → extract observations (regex)
Next Session → inject updated memories (learning loop)
```

## Installation

```bash
# Add the plugin marketplace
droid plugin marketplace add https://github.com/minhduydev/mdroid

# Install mdroid
droid plugin install mdroid@mdroid
```

## Recommended companion setup

mdroid is lean by design. It delegates to the ecosystem for things other plugins do better:

### Companion plugins

```bash
# Official Factory plugins
droid plugin marketplace add https://github.com/Factory-AI/factory-plugins
droid plugin install droid-evolved@factory-plugins --scope user
droid plugin install security-engineer@factory-plugins --scope user
droid plugin install droid-control@factory-plugins --scope user

# Superpowers (TDD, brainstorming, subagent dev, git-worktrees)
droid plugin marketplace add https://github.com/obra/superpowers
droid plugin install superpowers@superpowers --scope user
```

### Companion MCP servers

```bash
droid mcp add figma https://mcp.figma.com/mcp --type http
droid mcp add playwright "npx -y @playwright/mcp@latest"
droid mcp add sentry https://mcp.sentry.dev/mcp --type http
droid mcp add linear https://mcp.linear.app/mcp --type http
```

## Commands

### Lifecycle commands

| Command | Purpose | When to use |
|---|---|---|
| `/init` | Bootstrap AGENTS.md + tech-stack.md + rules stubs | New or existing project lacking AGENTS.md |
| `/spec` | Define what to build (PRD) | Before implementing a feature (3+ files) |
| `/plan` | Break down into dependency-ordered tasks | Complex features (4+ files, multiple systems) |
| `/build` | Implement with TDD | After /spec (and optionally /plan) |
| `/verify` | Run verification gates | After /build, before /ship |
| `/review` | Multi-persona parallel review | After /verify, before /ship |
| `/ship` | Commit, PR, cleanup | After /verify + /review pass |

### Standalone commands

| Command | Purpose | When to use |
|---|---|---|
| `/fix` | Debug and fix bugs (2-3 files) | Bugfix or resolving /verify, /review issues |
| `/research` | External research with confidence levels | Unknowns before /spec, or standalone |
| `/audit` | Codebase pattern audit | Finding tech debt, anti-patterns |
| `/interview-me` | One-question-at-a-time requirements extraction | Vague requirements |
| `/grill-me` | Aggressive requirement interrogation | Specs/plans that feel too optimistic |
| `/clean` | Remove stale artifact directories | Clean up old feature artifacts |
| `/mission-prep` | Prepare repo for Factory Missions | Before /missions on multi-feature projects |
| `/interview-me` | One-question-at-a-time requirements extraction | Vague requirements |
| `/grill-me` | Aggressive requirement interrogation | Specs/plans that feel too optimistic |

### Workflow

```
User Request
     ↓
[TRIAGE GATE] → Trivial? Do directly. Bugfix? /fix. Research? /research. Audit? /audit.
     ↓
Multi-feature? → /mission-prep → /missions (agent-driven orchestration)
     ↓
Single feature → /spec → /plan (optional) → /build → /verify → /review → /ship → DONE
```

## Factory Missions integration

mdroid works seamlessly inside [Factory Missions](https://docs.factory.ai/features/missions/overview). Missions inherit all plugin config: hooks, droids, skills, AGENTS.md, MCP.

### When to use Missions vs mdroid workflow

| Criteria | Use mdroid workflow | Use Missions |
|---|---|---|
| Feature count | 1 feature | 2+ features |
| Control | User-driven (manual steps) | Agent-driven (orchestration) |
| Sessions | Single session | Multi-session, milestones |
| Validation | /verify + /review (manual) | Validator workers (automated) |
| Planning | /spec + /plan | Collaborative planning with Droid |

### How they complement

- **Missions** = orchestration layer (WHAT to do, in what order, across features).
- **mdroid** = execution discipline (HOW to do it: TDD, verify gates, review personas).
- Missions workers can use mdroid skills and droids when implementing each feature.
- mdroid's 5-layer memory system fires during missions via hooks: decisions from mission 1 are injected into mission 2.

### Preparation

Run `/mission-prep` before starting a mission. It checks:
1. Agent Readiness (Level 4+ recommended).
2. AGENTS.md completeness.
3. `.factory/rules/` coding standards.
4. QA scripting (one-command startup, filesystem logs, input mechanism).
5. Mission model settings (orchestrator=strong, worker=fast, validator=strong).
6. Autonomy level (High required for Missions).

### Mission model tuning

Add to `.factory/settings.json`:

```json
{
  "missionModelSettings": {
    "workerModel": "<fast model>",
    "workerReasoningEffort": "low",
    "validationWorkerModel": "<strong model>",
    "validationWorkerReasoningEffort": "high"
  },
  "missionOrchestratorModel": "<strongest model>",
  "missionOrchestratorReasoningEffort": "high"
}
```

Pair a strong orchestrator with a faster worker model for the best cost-quality tradeoff.

### Headless missions

```bash
droid exec --mission \
  --worker-model <model> \
  --worker-reasoning-effort medium \
  --validator-model <model> \
  --validator-reasoning-effort high \
  -f mission.md
```

## Agent Readiness

Factory evaluates repos on a 1-5 readiness scale. mdroid works best at **Level 4 (Optimized) or above**.

Run `/readiness-report` to check your repo, then `/readiness-fix` to close gaps. Key criteria:
- Linter configured (catches errors immediately).
- Type checker configured (prevents runtime errors).
- Unit tests runnable (verification in same turn).
- AGENTS.md exists (context upfront).
- Build command documented.
- Dependencies pinned.

## Custom droids

8 specialized subagents, invoked via the Task tool:

| Droid | Role | Tools |
|---|---|---|
| `build` | Primary dev agent, full edit access | Read, Edit, Create, Execute, Grep, Glob, LS |
| `explore` | Read-only code search and discovery | Read, Grep, Glob, LS |
| `plan` | Architecture planning | Read, Grep, Glob, LS, Create |
| `review` | Code review specialist (read-only) | Read, Grep, Glob, LS |
| `scout` | External research (web, docs) | Read, Grep, Glob, LS, WebSearch, FetchUrl |
| `vision` | UI/UX visual analysis | Read, Grep, Glob, LS |
| `security-audit` | Focused security review (STRIDE, OWASP) | Read, Grep, Glob, LS |
| `general` | Fast simple tasks | Read, Edit, Create, Execute, Grep, Glob, LS |

## Skills

26 skills total: 12 workflow commands (user-invoked via `/command`) and 14 background skills (auto-loaded when relevant).

### Workflow commands (12)

| Command | Purpose |
|---|---|
| `/init` | Bootstrap AGENTS.md + tech-stack.md |
| `/spec` | Define what to build (PRD) |
| `/plan` | Break down into dependency-ordered tasks |
| `/build` | Implement with TDD |
| `/verify` | Run verification gates |
| `/review` | Multi-persona parallel review |
| `/ship` | Commit, PR, cleanup |
| `/fix` | Debug and fix bugs |
| `/research` | External research with confidence levels |
| `/audit` | Codebase pattern audit |
| `/clean` | Remove stale artifact directories |

### Background skills (14, auto-loaded when relevant)

- **behavioral-kernel**: Core execution discipline
- **defense-in-depth**: Security hardening patterns
- **incremental-implementation**: Thin vertical slices
- **development-lifecycle**: SDLC routing
- **doubt-driven-development**: Adversarial review (CLAIM -> EXTRACT -> DOUBT -> RECONCILE -> STOP)
- **context-engineering**: Feed agents right info at right time
- **observability-and-instrumentation**: Structured logging, RED metrics, tracing
- **deprecation-and-migration**: Code-as-liability, safe removal
- **api-and-interface-design**: Contract-first design, Hyrum's Law
- **documentation-and-adrs**: ADRs and docs that stay useful
- **ci-cd-and-automation**: Shift Left, Faster is Safer
- **shipping-and-launch**: Pre-launch checklists, staged rollouts
- **interview-me**: One-question-at-a-time interview (user-invocable)
- **grill-me**: Requirement interrogation (user-invocable)

## Memory system

### How it works

The 5-layer memory system runs automatically via hooks. You don't need to do anything.

| Layer | Hook event | What it does |
|---|---|---|
| 1. Track | PreToolUse/PostToolUse | Records files read/modified/created in session-state.json |
| 2. Summary | PreCompact | Saves anchored summary before context compression |
| 3+4. Distill + Curate | Stop | TF-IDF distill -> regex extract observations (single script, sequential) |
| 5. Inject | SessionStart | BM25-ranks memories, injects relevant ones into context |

### Manual memory capture

Prefix a message with `#` to save a project memory, or `##` for a personal memory:

```
# We use Zustand for state management because it's simpler than Redux
## Always run tests before committing
```

### Runtime data

```
.factory/
  memory/
    distillations/          # TF-IDF compressed session transcripts
    session-state.json      # Current session file trail (ephemeral)
    session-summary.md      # Anchored summary (survives compression)
  memories.md               # Curated observations (append-only, grows over time)
  artifacts/
    <slug>/
      spec.md, plan.md, progress.md, review.md, verify.log, ...
```

## Artifacts lifecycle

Each feature gets a slug and an artifact directory:

```
/spec → creates .factory/artifacts/<slug>/spec.md
/plan → creates .factory/artifacts/<slug>/plan.md
/build → updates .factory/artifacts/<slug>/progress.md
/verify → writes .factory/artifacts/<slug>/verify.log
/review → writes .factory/artifacts/<slug>/review.md
/research → writes .factory/artifacts/<slug>/research.md
/audit → writes .factory/artifacts/<slug>/audit.md
/ship → cleans up .factory/artifacts/.active
```

## Project setup

For each project using mdroid:

```bash
# 1. Run /init to bootstrap AGENTS.md
/init

# 2. Start building
/spec "your first feature"
```

## License

MIT
