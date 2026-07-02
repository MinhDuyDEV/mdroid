# mdroid - Plugin Package Build Plan

> **Purpose:** Build a Factory Droid plugin package combining the best of OpenCodeKit, addyosmani/agent-skills, and obra/superpowers, optimized for Droid-native features.
>
> **Status:** Planning phase. This file is the single source of truth for building the plugin.
>
> **Created:** 2026-07-01
>
> **Context sources:**
> - OpenCodeKit repo: `/tmp/opencodekit-template/` (cloned from `github.com/opencodekit/opencodekit-template`)
> - Factory docs: `https://docs.factory.ai/llms.txt`
> - Factory plugins: `https://github.com/Factory-AI/factory-plugins`
> - Superpowers: `https://github.com/obra/superpowers` (243k stars)
> - agent-skills: `https://github.com/addyosmani/agent-skills` (68.2k stars)

---

## 1. What is mdroid?

**mdroid** is a Factory Droid plugin that packages a production-grade engineering workflow optimized for Droid-native features. It combines:

- **OpenCodeKit** artifacts lifecycle, multi-agent orchestration, AGENTS.md behavioral kernel
- **agent-skills** anti-rationalization tables, Red Flags, verification gates, 4 review personas, reference checklists
- **Superpowers** TDD discipline, subagent-driven development, git-worktree isolation
- **Droid native** Task tool, hooks, MCP, Missions, context compression, session navigation

The result: a lean plugin (~60 files) that delivers 80% of the value of porting all three kits combined, without the 60%+ duplication. Includes a 5-layer automated memory system that provides cross-session learning without spending LLM tokens.

---

## 2. Why not just port OpenCodeKit?

OpenCodeKit has 60+ skills, but research shows:

- **17/24 agent-skills skills share the same name** as OpenCodeKit skills (70% overlap)
- **Superpowers** already provides TDD, brainstorming, writing-plans, subagent-driven-dev, git-worktrees, systematic-debugging, verification
- **Factory plugins** already provide security-engineer (STRIDE), review + simplify (code review), droid-control (browser/QA), droid-evolved (session-nav, frontend-design)
- **MCP registry** already provides 40+ servers (figma, playwright, supabase, jira, sentry, linear, stripe, vercel)
- **Droid native** already provides context compression (replaces session-summary.ts), Spec Mode (replaces prompt-leverage.ts), BYOK (replaces copilot-auth.ts), WebSearch (replaces webclaw/context7 tools)

**Strategy: PORT only unique value, REPLACE duplicates with ecosystem, DROP what Droid has natively.**

---

## 3. Plugin Package Structure

```
mdroid/
├── .factory-plugin/
│   └── plugin.json                    # Plugin manifest
├── droids/                             # 8 custom droids (7 from OpenCodeKit + oracle convergence judge)
│   ├── build.md                        # Primary dev agent
│   ├── explore.md                      # Read-only code search
│   ├── plan.md                         # Architecture planning
│   ├── review.md                       # Code review specialist
│   ├── oracle.md                       # Convergence Judge (strong model, high reasoning)
│   ├── scout.md                        # External research
│   ├── vision.md                       # UI/UX visual analysis
│   └── general.md                      # Fast simple tasks
├── skills/                             # 10 workflow commands + ~15 unique skills
│   ├── spec/SKILL.md                   # /spec - Define what to build
│   ├── plan/SKILL.md                   # /plan - Break down implementation
│   ├── build/SKILL.md                  # /build - Implement with TDD
│   ├── verify/SKILL.md                 # /verify - Run verification gates
│   ├── review/SKILL.md                 # /review - Multi-persona review
│   ├── ship/SKILL.md                   # /ship - Commit, PR, deploy
│   ├── fix/SKILL.md                    # /fix - Debug and fix bugs
│   ├── research/SKILL.md              # /research - External research
│   ├── audit/SKILL.md                  # /audit - Codebase pattern audit
│   ├── init/SKILL.md                   # /init - Project setup
│   ├── behavioral-kernel/SKILL.md      # Core execution discipline
│   ├── defense-in-depth/SKILL.md      # Security hardening patterns
│   ├── incremental-implementation/SKILL.md  # Thin vertical slices
│   ├── development-lifecycle/SKILL.md  # Full SDLC routing
│   ├── doubt-driven-development/SKILL.md    # Adversarial review (from agent-skills)
│   ├── context-engineering/SKILL.md    # Feed agents right info (from agent-skills)
│   ├── interview-me/SKILL.md            # Structured grilling (from agent-skills)
│   ├── observability-and-instrumentation/SKILL.md  # Telemetry (from agent-skills)
│   ├── deprecation-and-migration/SKILL.md  # Code-as-liability (from agent-skills)
│   ├── api-and-interface-design/SKILL.md  # Contract-first design
│   ├── documentation-and-adrs/SKILL.md    # ADRs and docs
│   ├── ci-cd-and-automation/SKILL.md      # Pipeline automation
│   ├── shipping-and-launch/SKILL.md       # Pre-launch checklists
│   └── grill-me/SKILL.md                  # Requirement interrogation
├── hooks/
│   ├── hooks.json                      # Hook configuration (7 hooks)
│   ├── track-artifacts.py              # Layer 1: PreToolUse + PostToolUse -> session-state.json
│   ├── save-summary.py                # Layer 2: PreCompact -> session-summary.md (anchored)
│   ├── distill-session.py              # Layer 3: Stop -> TF-IDF distill -> distillations/
│   ├── curate-observations.py          # Layer 4: Stop (sau distill) -> regex -> memories.md
│   ├── inject-memory.py               # Layer 5: SessionStart -> BM25 score + inject context
│   ├── memory-capture-manual.py        # Manual: UserPromptSubmit (#/## prefix)
│   ├── structural-check.sh             # Architecture validation: PostToolUse
│   └── lib/
│       ├── tfidf.py                     # TF-IDF engine (port from OCK distill.ts)
│       ├── bm25.py                      # BM25 scoring (port from OCK inject.ts)
│       ├── patterns.py                  # Regex curator patterns (port from OCK curator.ts)
│       ├── markdown.py                  # memories.md read/write/append helpers
│       └── tokenize.py                  # Text tokenization + stop words (port from distill.ts)
├── references/                         # 7 reference checklists (from agent-skills)
│   ├── definition-of-done.md
│   ├── testing-patterns.md
│   ├── security-checklist.md
│   ├── performance-checklist.md
│   ├── accessibility-checklist.md
│   ├── observability-checklist.md
│   └── orchestration-patterns.md
├── templates/                          # Artifact templates
│   ├── spec-lite.md                    # Lite PRD template
│   ├── spec-full.md                    # Full PRD template
│   ├── plan.md                         # Implementation plan template
│   └── progress.md                     # Progress tracking template
├── mcp.json                            # MCP server configs (context7, optional others)
└── README.md                           # Plugin documentation
```

**Total: ~60 files** (vs 60+ in OpenCodeKit). No duplication with ecosystem. 5-layer memory system adds 12 hook files + 5 lib files but replaces OpenCodeKit's 20 TypeScript memory plugin files.

---

## 4. Component Breakdown

### 4.1 Plugin Manifest (`.factory-plugin/plugin.json`)

```json
{
  "name": "mdroid",
  "description": "Production-grade engineering workflow for Factory Droid - combines OpenCodeKit artifacts lifecycle, agent-skills anti-rationalization patterns, and Superpowers TDD discipline",
  "version": "0.1.0",
  "author": {
    "name": "MinhDuyDEV"
  },
  "license": "MIT",
  "homepage": "https://github.com/minhduydev/mdroid",
  "repository": "https://github.com/minhduydev/mdroid"
}
```

### 4.2 Custom Droids (7 files in `droids/`)

Port from OpenCodeKit `.opencode/agent/*.md`, converting to Droid format.

**Conversion rules:**
- OpenCode frontmatter `mode: primary|subagent` -> Droid: no equivalent, omit
- OpenCode frontmatter `temperature` -> Droid: omit (not supported)
- OpenCode frontmatter `steps` -> Droid: omit
- OpenCode frontmatter `tools:` (map of true/false) -> Droid: `tools:` array of tool IDs
- OpenCode frontmatter `permission:` -> Droid: omit (Droid handles permissions differently)
- Body content: keep mostly as-is, but replace `task()` with "Task tool", `skill()` with "Skill tool", `question()` with "AskUser tool", `memory_search` with "Grep on memories.md", `observation` with "Edit memories.md"

**Per-droid conversion:**

| Droid | OpenCode source | Droid tools | Notes |
|---|---|---|---|
| `build.md` | `.opencode/agent/build.md` | `["Read","Edit","Create","Execute","Grep","Glob","TodoWrite"]` | Primary agent, full access. Remove delegation analysis (Droid Task tool handles this) |
| `explore.md` | `.opencode/agent/explore.md` | `["Read","Grep","Glob","LS"]` (read-only) | Replace srcwalk references with Grep/Glob. Remove `websearch: false` (Droid handles) |
| `plan.md` | `.opencode/agent/plan.md` | `["Read","Grep","Glob","LS","Create","TodoWrite"]` | Remove memory_search/observation calls. Keep goal-backward methodology |
| `review.md` | `.opencode/agent/review.md` | `["Read","Grep","Glob","LS"]` (read-only) | Keep goal-backward verification, stub detection. Remove srcwalk references |
| `scout.md` | `.opencode/agent/scout.md` | `["Read","Grep","Glob","WebSearch","FetchUrl"]` | Replace context7/opensrc/grepsearch with WebSearch + FetchUrl |
| `vision.md` | `.opencode/agent/vision.md` | `["Read","Grep","Glob","LS"]` (read-only) | UI/UX analysis, multimodal |
| `general.md` | `.opencode/agent/general.md` | `["Read","Edit","Create","Execute","Grep","Glob"]` | Fast simple tasks. Keep minimal |

**Source files to read:** `/tmp/opencodekit-template/.opencode/agent/*.md` (7 files)

### 4.3 Workflow Skills/Commands (10 files in `skills/`)

These are the 10 slash commands. Each is a SKILL.md with YAML frontmatter.

**IMPORTANT: Do NOT port OpenCodeKit commands verbatim.** They reference OpenCode APIs (memory_search, observation, task(), skill(), question(), .opencode/ paths). The improved versions below are redesigned for Droid-native features and incorporate improvements from agent-skills and Superpowers.

#### Design principles for each command:

1. **Triage gate** (NEW, from our analysis): Every command starts with a triage check. Trivial tasks get rejected with "just do it directly."
2. **Progressive complexity**: Simple / Standard / Deep modes. User picks depth.
3. **Artifact-driven**: Each phase writes to `.factory/artifacts/<slug>/`.
4. **Droid-native**: Use Task tool (not `task()`), AskUser (not `question()`), Grep (not `memory_search`), Edit memories.md (not `observation()`).
5. **Anti-rationalization table** (from agent-skills): Every command has "Common Rationalizations" table with excuses + rebuttals.
6. **Red Flags** (from agent-skills): Every command has "Red Flags" section.
7. **Verification gates** (from agent-skills + OCK): Non-negotiable. "Seems right" is never sufficient.
8. **Lean**: Each command <300 lines. OCK /ship is 17k chars - too verbose.
9. **Natural chaining**: Each command knows its next step.
10. **3-way combo**: Best of OpenCodeKit (artifacts, multi-agent), agent-skills (anti-rationalization, personas), Superpowers (TDD, subagent isolation).

#### Command specifications:

##### `/init` - Project setup
- **Phase:** Setup
- **Droid:** build
- **Artifact:** AGENTS.md, tech-stack.md
- **Source:** OCK `/init` simplified
- **Changes:** Remove OCK-specific skill installation. Remove .opencode/ paths -> .factory/. Remove observation() call. Remove Mode 2/3 (planning context, user profile) -> these go in memories.md via hook.
- **Next:** `/spec` or `/research`

##### `/spec` - Define what to build (replaces OCK `/create`)
- **Phase:** Define
- **Droid:** explore + scout (research), build (write)
- **Artifact:** `.factory/artifacts/<slug>/spec.md`
- **Source:** OCK `/create` (8 phases instead of 11) + agent-skills `/spec`
- **Triage gate:** If trivial (1 file, known fix) -> reject, tell user to do directly. If bugfix (2-3 files) -> suggest `/fix`. If research needed -> suggest `/research` first.
- **Changes from OCK:** 8 phases (not 11). Task tool replaces task(). AskUser replaces question(). Lite/Full auto-detect. No memory_search dependency. No observation() dependency.
- **Next:** `/plan` (complex) or `/build --skip-plan` (simple)

##### `/plan` - Break down implementation
- **Phase:** Plan
- **Droid:** plan + explore
- **Artifact:** `.factory/artifacts/<slug>/plan.md`
- **Source:** OCK `/plan` simplified + agent-skills `/plan`
- **Changes from OCK:** Remove Phase 0 "Institutional Research" (memory_search dependency). Replace with Grep on memories.md + git log. Keep goal-backward methodology. Keep dependency graph + wave assignment. Keep constitutional compliance gate. Remove discovery level user prompt -> auto-detect from spec complexity.
- **Next:** `/build`

##### `/build` - Implement with TDD (replaces OCK `/ship` execution phases)
- **Phase:** Build
- **Droid:** general (parallel) or build (sequential)
- **Artifact:** `.factory/artifacts/<slug>/progress.md`
- **Source:** OCK `/ship` Phases 2-3 + Superpowers TDD + agent-skills `/build`
- **Modes:** `auto` (plan + implement all tasks in 1 pass, from agent-skills), `task` (specific task by ID, sequential), `--skip-plan` (simple features, convert spec -> tasks directly)
- **TDD cycle** (from Superpowers): RED (failing test) -> GREEN (minimal code) -> REFACTOR -> commit per task
- **Wave-based execution:** Tasks in same wave run parallel via Task tool if independent.
- **Changes from OCK /ship:** 8 phases (not 6 phases + 5 sub-phases + 2 review modes). No Iterative Quality Loop (too heavy, /review handles this). No UI Quality Gate inline (moved to /review). No Goal-Backward Verification inline (moved to /verify). TDD cycle added (OCK doesn't have). auto mode added (OCK doesn't have).
- **Stop conditions:** Verification fails 2x on same task -> stop, report blocker. Files outside scope -> stop, ask user.
- **Commit protocol:** Stage specific files (NEVER `git add .`). Per-task commit with type prefix (feat/fix/test/refactor).
- **Next:** `/verify`

##### `/verify` - Run verification gates
- **Phase:** Verify
- **Droid:** None (direct execution, no delegation)
- **Artifact:** `.factory/artifacts/<slug>/verify.log`
- **Source:** OCK `/verify` simplified + agent-skills verification pattern
- **Gates:** typecheck, lint, test, build (all 4 must pass). Incremental mode (changed files only) by default, full mode with `--full`.
- **Cache:** Fingerprint (commit hash + diff hash). Skip if unchanged since last verify.
- **Changes from OCK:** Remove skill() call. Remove observation() call. Keep verification cache. Keep incremental/full modes. Add Red Flags from agent-skills.
- **Next:** `/review` (if changes significant) or `/ship` (if trivial)

##### `/review` - Multi-persona parallel review (NEW standalone command)
- **Phase:** Review
- **Droid:** 4-5 review personas via Task tool (parallel)
- **Artifact:** `.factory/artifacts/<slug>/review.md`
- **Source:** agent-skills 4 personas + OCK `/ship` Phase 5 review
- **Personas:** correctness, security, performance, tests (+ architecture in `--deep` mode)
- **Modes:** `--quick` (1 reviewer, correctness only), default (4 personas), `--deep` (5 personas + cross-check)
- **Auto-fix rule:** Critical -> fix inline, re-verify. Important -> fix inline. Minor -> log to review.md.
- **Changes from OCK:** Standalone command (OCK has review inside /ship Phase 5). 4 focused personas (OCK has 5 generic reviewers). --quick and --deep modes (OCK doesn't have). Anti-rationalization table (OCK doesn't have). No Iterative Quality Loop (too heavy).
- **Next:** `/ship` (if clean) or `/fix` (if critical issues)

##### `/ship` - Commit, PR, deploy
- **Phase:** Ship
- **Droid:** build
- **Artifact:** Final commit + PR
- **Source:** OCK `/ship` Phase 6 (close) + agent-skills `/ship`
- **Pre-conditions:** /verify passed, /review passed (or user confirms skipping review).
- **Actions:** Confirm with user. Stage specific files. Commit with conventional commit format. Optionally create PR (ask user, never push without confirmation). Update progress.md with final status. Clean up .active.
- **Changes from OCK:** Lean (OCK /ship Phase 6 is part of 17k char command). No Goal-Backward Verification here (moved to /verify). No review here (moved to /review). Just commit + PR + cleanup.
- **Next:** Done

##### `/fix` - Debug and fix bugs
- **Phase:** Bugfix (standalone, not part of lifecycle)
- **Droid:** build
- **Artifact:** Optional `.factory/artifacts/<slug>/progress.md`
- **Source:** OCK `/fix` + agent-skills debugging-and-error-recovery + Superpowers systematic-debugging
- **Process:** Reproduce -> Isolate (search, trace, read 2-4 files) -> Fix (minimal, root cause) -> Verify (typecheck, lint, test)
- **Changes from OCK:** Add Red Flags. Add anti-rationalization. Remove skill() calls. Keep it lean (OCK /fix is already short, keep it).
- **Next:** Done (or `/verify` if part of larger work)

##### `/research` - External research
- **Phase:** Research (standalone, can happen at any time)
- **Droid:** scout (parallel for complex)
- **Artifact:** `.factory/artifacts/<slug>/research.md` (if active feature) or direct report
- **Source:** OCK `/research` + agent-skills source-driven-development
- **Complexity detection:** Simple (direct execution, ~30 tool calls) vs Complex (invoke deep-research pattern: fan out scout droids, cross-check, synthesize)
- **Source priority:** Codebase -> Official docs (WebSearch/FetchUrl) -> Source code -> GitHub -> Web search
- **Changes from OCK:** Replace context7/opensrc/grepsearch/codesearch with WebSearch + FetchUrl. Remove deep-research.md workflow file (use Task tool directly). Keep confidence levels. Keep stop conditions.
- **Next:** `/spec` (if feature) or done

##### `/audit` - Codebase pattern audit
- **Phase:** Audit (standalone)
- **Droid:** explore (discover) + review (audit each) + general (synthesize)
- **Artifact:** `.factory/artifacts/<slug>/audit.md`
- **Source:** OCK `/audit` + agent-skills code-review-and-quality
- **Process:** Find all occurrences -> Review each for issues -> Synthesize prioritized remediation
- **Changes from OCK:** Remove workflow file reference. Use Task tool directly. Keep it lean.
- **Next:** `/fix` (if issues) or done

### 4.4 Unique Skills (~15 files in `skills/`)

These are skills that are NOT workflow commands. They are loaded on-demand by the Droid when task context matches.

**Source priority:** If skill exists in agent-skills, port from agent-skills (better quality: anti-rationalization, Red Flags). If skill exists only in OpenCodeKit, port from OpenCodeKit. If skill exists in Superpowers, use Superpowers (install plugin instead of duplicating).

| Skill | Source | Port or Replace? | Notes |
|---|---|---|---|
| behavioral-kernel | OCK | PORT | Core execution discipline. Unique to OCK. |
| defense-in-depth | OCK | PORT | Security hardening patterns. Unique to OCK. |
| incremental-implementation | OCK | PORT | Thin vertical slices. In OCK and agent-skills, port OCK version. |
| development-lifecycle | OCK | PORT | Full SDLC routing. Unique to OCK. |
| doubt-driven-development | agent-skills | PORT | Adversarial review: CLAIM -> EXTRACT -> DOUBT -> RECONCILE -> STOP. Unique to agent-skills. |
| context-engineering | agent-skills | PORT | Feed agents right info at right time. Unique to agent-skills. |
| interview-me | agent-skills | PORT | One-question-at-a-time interview. Better than OCK grill-me. |
| observability-and-instrumentation | agent-skills | PORT | Structured logging, RED metrics, OpenTelemetry. Unique to agent-skills. |
| deprecation-and-migration | agent-skills | PORT | Code-as-liability. Better than OCK version. |
| api-and-interface-design | agent-skills | PORT | Contract-first, Hyrum's Law, One-Version Rule. Better than OCK version. |
| documentation-and-adrs | OCK/agent-skills | PORT | Both have this. Port agent-skills version (better structured). |
| ci-cd-and-automation | agent-skills | PORT | Shift Left, Faster is Safer. Port agent-skills version. |
| shipping-and-launch | agent-skills | PORT | Pre-launch checklists, staged rollouts. Port agent-skills version. |
| grill-me | OCK | PORT | Requirement interrogation. Keep OCK version (simpler). |

**Skills NOT ported (replaced by ecosystem):**
- test-driven-development -> Superpowers (install plugin)
- brainstorming -> Superpowers (install plugin)
- writing-plans -> Superpowers (install plugin)
- subagent-driven-development -> Superpowers (install plugin)
- using-git-worktrees -> Superpowers (install plugin)
- systematic-debugging -> Superpowers (install plugin)
- verification-before-completion -> agent-skills pattern embedded in /verify command
- security-and-hardening -> Factory security-engineer plugin
- code-review-and-quality -> Factory core plugin (review + simplify)
- frontend-design / design-taste-frontend -> Factory droid-evolved plugin
- figma -> MCP registry
- playwright -> MCP registry + droid-control plugin
- supabase -> MCP registry
- jira -> MCP registry
- performance-optimization -> agent-skills (could port if needed, but not critical for v0.1)
- code-cleanup / code-simplification -> agent-skills code-simplification (could port if needed)
- gemini-large-context -> DROP (Gemini CLI EOL 2026-06-18)
- srcwalk -> DROP (no Droid equivalent, use Grep/Glob)
- webclaw -> DROP (Droid has WebSearch)
- opensrc -> DROP (Droid has WebSearch + FetchUrl)
- pdf-extract -> DROP (Droid has FetchUrl for web, Read for local PDFs)
- mockup-to-code -> DROP (not core workflow)
- design-system-audit -> DROP (not core workflow)
- accessibility-audit -> agent-skills accessibility-checklist.md reference
- chrome-devtools -> droid-control plugin + agent-browser
- browser-testing-with-devtools -> droid-control plugin
- swift-concurrency / swiftui-expert-skill -> DROP (platform-specific, not core)
- react-best-practices -> DROP (framework-specific, not core)
- polar / resend / cloudflare / vercel-deploy-claimable -> DROP (platform-specific, use MCP)

**Conversion rules for skills:**
- Add YAML frontmatter: `name`, `description` (with "Use when..." trigger)
- Remove OpenCode-specific API references (skill(), task(), memory_search, observation)
- Replace `.opencode/` paths with `.factory/`
- Add anti-rationalization table if not present (from agent-skills pattern)
- Add Red Flags section if not present (from agent-skills pattern)
- Add Verification section if not present (from agent-skills pattern)
- Keep under 300 lines per skill

### 4.5 Hooks — 5-Layer Memory System (12 files in `hooks/`)

This is the core innovation of mdroid: a **5-layer automated memory system** built entirely with Droid hooks + Python scripts. It replaces OpenCodeKit's 4-tier TypeScript memory plugin (20 files, ~4500 lines) with 7 hooks + 5 Python lib modules, achieving equivalent functionality without a TypeScript runtime and without spending any LLM tokens.

**Design principles:**
- **Fully automatic**: Agent does nothing. Hooks fire deterministically on lifecycle events.
- **No LLM tokens**: All processing is heuristic (TF-IDF, BM25, regex). Python only.
- **Cross-session learning**: Memories accumulate across sessions. BM25 injects relevant context.
- **Survives compression**: Session summary is anchored before Droid compacts.
- **Progressive**: Layers 1-2 run every session. Layers 3-5 activate when enough data exists.

#### Architecture overview

```
Session Start:
  [Layer 5] inject-memory.py reads memories.md -> BM25 score -> inject relevant context

During Session:
  [Layer 1] track-artifacts.py captures every Read/Edit/Create -> session-state.json
  [Manual]  memory-capture-manual.py captures #/## messages -> memories.md
  [Guard]   structural-check.sh validates architecture on every edit

Before Compression:
  [Layer 2] save-summary.py reads session-state.json -> writes session-summary.md (anchored)

Session Stop:
  [Layer 3] distill-session.py reads transcript -> TF-IDF -> distillations/<id>.md
  [Layer 4] curate-observations.py reads distillation -> regex patterns -> memories.md (append)

Next Session:
  [Layer 5] inject-memory.py reads UPDATED memories.md -> BM25 -> inject
  (Learning loop complete: past sessions inform future sessions)
```

#### Runtime data layout (project-level, created at runtime)

```
.factory/
  memory/
    distillations/               # <session-id>.md files (TF-IDF compressed)
    session-state.json            # file trail + decisions (per session, ephemeral)
    session-summary.md            # anchored summary (survives Droid compression)
  memories.md                    # curated observations (append-only, grows over time)
  artifacts/
    <slug>/
      ... (existing artifacts)
```

#### `hooks/hooks.json`

```json
{
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "python3 ${DROID_PLUGIN_ROOT}/hooks/inject-memory.py",
          "timeout": 10
        }
      ]
    }
  ],
  "PreToolUse": [
    {
      "matcher": "Read|Edit|Create|ApplyPatch",
      "hooks": [
        {
          "type": "command",
          "command": "python3 ${DROID_PLUGIN_ROOT}/hooks/track-artifacts.py",
          "timeout": 5
        }
      ]
    }
  ],
  "PostToolUse": [
    {
      "matcher": "Read|Edit|Create|ApplyPatch",
      "hooks": [
        {
          "type": "command",
          "command": "python3 ${DROID_PLUGIN_ROOT}/hooks/track-artifacts.py",
          "timeout": 5
        }
      ]
    },
    {
      "matcher": "Create|Edit|ApplyPatch",
      "hooks": [
        {
          "type": "command",
          "command": "${DROID_PLUGIN_ROOT}/hooks/structural-check.sh",
          "timeout": 30
        }
      ]
    }
  ],
  "PreCompact": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "python3 ${DROID_PLUGIN_ROOT}/hooks/save-summary.py",
          "timeout": 10
        }
      ]
    }
  ],
  "Stop": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "python3 ${DROID_PLUGIN_ROOT}/hooks/distill-session.py",
          "timeout": 60
        },
        {
          "type": "command",
          "command": "python3 ${DROID_PLUGIN_ROOT}/hooks/curate-observations.py",
          "timeout": 30
        }
      ]
    }
  ],
  "UserPromptSubmit": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "python3 ${DROID_PLUGIN_ROOT}/hooks/memory-capture-manual.py"
        }
      ]
    }
  ]
}
```

#### Layer 1: `hooks/track-artifacts.py` (file artifact trail)

**Hook events:** PreToolUse (Read, Edit, Create, ApplyPatch) + PostToolUse (same)

**Purpose:** Automatically track every file the agent reads, modifies, or creates during a session. Replaces OpenCodeKit's session-summary.ts file-artifact tracking.

**Input:** JSON via stdin containing `session_id`, `tool_name`, `tool_input`, `tool_response`, `cwd`

**Logic:**
```python
# 1. Read .factory/memory/session-state.json (or create empty)
# 2. Based on tool_name:
#    - "Read": append file_path to files_read[] (dedup)
#    - "Edit": append file_path to files_modified[] + extract edit detail
#    - "Create": append file_path to files_created[]
# 3. If tool_input content contains decision keywords ("decided to", "chose", "went with"):
#    - Extract sentence, append to decisions[]
# 4. Enforce limits: max 100 files_read, max 50 files_modified, max 20 files_created, max 10 decisions
# 5. Write back to .factory/memory/session-state.json
```

**Session-state JSON schema:**
```json
{
  "session_id": "abc123",
  "started_at": "2026-07-01T10:00:00Z",
  "intent": "",
  "files_read": ["src/foo.ts", "README.md"],
  "files_modified": ["src/foo.ts"],
  "files_created": ["src/new-file.ts"],
  "decisions": [
    {"title": "Decided to use Zustand", "rationale": "simpler than Redux", "time": "..."}
  ]
}
```

**Output:** Exit 0 (silent). No stdout, no stderr.

**Performance:** <50ms per call. Just JSON read + append + write.

#### Layer 2: `hooks/save-summary.py` (anchored session summary)

**Hook event:** PreCompact (fires before Droid compresses context)

**Purpose:** Save a structured session summary that survives Droid's context compression. Based on Factory Research's "anchored iterative summarization" (validated as best-in-class, scoring 3.70/5 vs Anthropic 3.44 vs OpenAI 3.35).

**Input:** JSON via stdin containing `session_id`, `trigger` (manual/auto), `cwd`

**Logic:**
```python
# 1. Read .factory/memory/session-state.json (file trail + decisions from Layer 1)
# 2. Read .factory/artifacts/.active -> get current slug
# 3. If active slug: read .factory/artifacts/<slug>/progress.md (task progress)
# 4. Format structured summary:
#    ## Intent: [from session-state or first user message]
#    ## Files Read: [list]
#    ## Files Modified: [list with edit details]
#    ## Files Created: [list]
#    ## Decisions: [list with rationale]
#    ## Next Steps: [from progress.md incomplete tasks]
# 5. Write to .factory/memory/session-summary.md
```

**Output:** Exit 0 (silent). PreCompact hook stderr goes to user only.

**Performance:** <100ms. Read 1-2 JSON/MD files + write 1 MD file.

#### Layer 3: `hooks/distill-session.py` (TF-IDF distillation)

**Hook event:** Stop (fires when Droid finishes responding)

**Purpose:** Compress the full session transcript into a concise distillation using TF-IDF term extraction + key sentence selection. Replaces OpenCodeKit's distill.ts. No LLM tokens used.

**Input:** JSON via stdin containing `session_id`, `transcript_path`, `cwd`

**Logic:**
```python
# 1. Read transcript JSONL file (path from hook input transcript_path)
# 2. Extract user + assistant text messages (skip tool calls, skip system)
# 3. TF-IDF pipeline (lib/tfidf.py):
#    a. Tokenize each message (lib/tokenize.py: lowercase, strip non-alphanum, remove stop words)
#    b. Compute Term Frequency (TF) per message
#    c. Compute Inverse Document Frequency (IDF) across all messages
#    d. Extract top 20 terms by TF*IDF score
# 4. Key sentence selection:
#    a. Split messages into sentences (>10 chars, <500 chars)
#    b. Score each sentence: term_density * (1 + term_hits)
#    c. Greedy-pack top sentences up to ~2000 chars total
#    d. Re-sort by original message order for coherence
# 5. Write to .factory/memory/distillations/<session-id>.md:
#    # Distillation: <session-id> <timestamp>
#    ## Top Terms: [term1, term2, ...]
#    ## Key Content:
#    [selected sentences]
# 6. Return distillation path (for Layer 4 to read)
```

**Output:** Exit 0 (silent).

**Performance:** <2s for typical session. <5s for very long sessions. Timeout: 60s.

#### Layer 4: `hooks/curate-observations.py` (regex pattern extraction)

**Hook event:** Stop (fires AFTER distill-session.py completes)

**Purpose:** Extract structured observations (decisions, bugfixes, patterns, discoveries, warnings) from the distillation using regex pattern matching. Replaces OpenCodeKit's curator.ts. No LLM tokens used.

**Input:** JSON via stdin containing `session_id`, `cwd`

**Logic:**
```python
# 1. Find latest distillation: .factory/memory/distillations/<session-id>.md
# 2. Read distillation content
# 3. Split into sentences (>30 chars, filtered for context)
# 4. Match against patterns (lib/patterns.py):
#    TYPE_PATTERNS = [
#      ("decision", r"\b(decided to|chose to|went with|opted for|switched to|migrated to)\b"),
#      ("bugfix",   r"\b(fixed|resolved|patched|corrected|bug in|error in|crash in)\b"),
#      ("pattern",  r"\b(pattern:|convention:|best practice|standard practice|we always|we never)\b"),
#      ("discovery",r"\b(found that|discovered|noticed|learned that|turns out|realized)\b"),
#      ("warning",  r"\b(warning:|caution:|careful with|gotcha|pitfall|don't use|avoid|beware|never)\b"),
#    ]
# 5. For each matched sentence:
#    a. Extract title (truncate sentence to 80 chars)
#    b. Extract concepts (significant words, max 5)
#    c. Assign confidence: "medium" (default for regex-matched)
# 6. Deduplicate against existing memories.md entries (prefix match, first 40 chars)
# 7. Append new observations to .factory/memories.md:
#    ### [YYYY-MM-DD]: [Title]
#    **Type**: decision/bugfix/pattern/discovery/warning
#    **Confidence**: medium
#    **Content**: [sentence]
#    **Concepts**: [concept1, concept2, ...]
# 8. Log: created=N, skipped=N, patterns={decision: N, bugfix: N, ...}
```

**Output:** Exit 0 (silent).

**Performance:** <500ms. Read 1 MD + regex match + append to MD.

#### Layer 5: `hooks/inject-memory.py` (BM25 relevance injection)

**Hook event:** SessionStart (fires when Droid starts or resumes a session)

**Purpose:** Search accumulated memories for relevance to current context, score with BM25, and inject top results into Droid's context. Replaces OpenCodeKit's inject.ts. No LLM tokens used.

**Input:** JSON via stdin containing `session_id`, `cwd`, `source` (startup/resume/clear/compact)

**Logic:**
```python
# 1. Read .factory/memories.md (all accumulated observations)
# 2. Parse each observation block (### [Date]: [Title] + Type + Confidence + Content)
# 3. Read current context for query term extraction:
#    a. If .factory/artifacts/.active: read spec.md + plan.md + progress.md
#    b. Read AGENTS.md (project conventions)
#    c. Extract query terms via TF (lib/tfidf.py: tokenize + term frequency)
# 4. BM25 score each observation against query terms (lib/bm25.py):
#    score = sum over query terms: IDF(term) * (f(term, doc) * (k1+1)) / (f + k1*(1-b+b*|doc|/avgdl))
#    where k1=1.5, b=0.75 (standard BM25 params)
# 5. Apply recency boost: score *= (1.0 + 0.1 * days_since / 30) capped at 1.5x
# 6. Apply confidence boost: high=1.2x, medium=1.0x, low=0.8x
# 7. Filter: score > 0.5 (threshold), top N=5 results
# 8. Format as additionalContext:
#    <memory_context>
#    Relevant knowledge from previous sessions:
#    ### [decision] Title (relevance: 0.82)
#    [content]
#    ### [warning] Title (relevance: 0.75)
#    [content]
#    </memory_context>
# 9. Output as JSON: {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "<memory_context>..."}}
```

**Output:** JSON stdout with `hookSpecificOutput.additionalContext`. Exit 0.

**Performance:** <500ms. Read 1-3 MD files + BM25 on ~50 observations (grows over time).

**Token cost:** ~200-500 tokens per session start (top 5 observations, ~40-100 tokens each). This is the ONLY token cost of the entire memory system, and it's paid once per session, not per turn.

#### Manual: `hooks/memory-capture-manual.py`

**Hook event:** UserPromptSubmit

**Purpose:** Allow user to manually capture memories by prefixing messages with `#` (project) or `##` (personal). Complementary to the auto-capture system.

**Input:** JSON via stdin containing `prompt`, `session_id`, `cwd`

**Logic:**
```python
# 1. Read prompt from stdin JSON
# 2. If starts with "##": personal memory
#    -> append to ~/.factory/memories.md: "- [YYYY-MM-DD] <content>"
# 3. If starts with "#": project memory
#    -> append to $FACTORY_PROJECT_DIR/.factory/memories.md: "- [YYYY-MM-DD] <content>"
# 4. If no # prefix: exit 0 (no action)
# 5. Output: {"systemMessage": "Saved to <path>"}
```

**Output:** JSON stdout with `systemMessage`. Exit 0.

#### Guard: `hooks/structural-check.sh`

**Hook event:** PostToolUse (Create, Edit, ApplyPatch)

**Purpose:** Validate architecture constraints after file edits. Port from OpenCodeKit `.opencode/tool/structural-check.sh`.

**Checks:**
- Plugin/skill files <300 lines
- Command files <500 lines
- Kebab-case filenames only
- No `.env` files in changes

**Output:** Exit 2 (block) if violation found, stderr sent to Droid. Exit 0 if clean.

#### Library modules (`hooks/lib/`)

##### `lib/tokenize.py`
Port from OpenCodeKit `distill.ts` tokenize function:
- Lowercase text
- Strip non-alphanumeric (keep hyphens, underscores, slashes, dots)
- Split on whitespace
- Remove stop words (120+ English stop words + code stop words: function, const, return, import, etc.)
- Filter: length > 2 chars

**Source:** `/tmp/opencodekit-template/.opencode/plugin/memory/distill.ts` (STOP_WORDS set + tokenize function)

##### `lib/tfidf.py`
Port from OpenCodeKit `distill.ts` TF-IDF engine:
- `compute_tf(words: list) -> dict[str, float]` - term frequency normalized by total
- `compute_idf(documents: list[list[str]]) -> dict[str, float]` - inverse document frequency: log(N / df)
- `extract_top_terms(messages: list, top_n: int) -> list[str]` - top N terms by TF*IDF
- `select_key_sentences(messages: list, top_terms: list, target_length: int) -> str` - greedy-pack by term density

**Source:** `/tmp/opencodekit-template/.opencode/plugin/memory/distill.ts` (extractTopTerms + selectKeySentences functions)

##### `lib/bm25.py`
Port BM25 scoring from OpenCodeKit `inject.ts`:
- `bm25_score(query_terms: list, doc: str, doc_stats: dict, avgdl: float, k1=1.5, b=0.75) -> float`
- `rank_documents(query_terms: list, documents: list, top_n: int) -> list[tuple[str, float]]`

**Source:** `/tmp/opencodekit-template/.opencode/plugin/memory/inject.ts` (extractQueryTerms + buildInjection logic)

##### `lib/patterns.py`
Port regex patterns from OpenCodeKit `curator.ts`:
- `CURATOR_PATTERNS`: list of (type, regex, title_extractor) tuples
- `match_patterns(sentence: str) -> tuple[str, str] | None` - returns (type, title) or None
- `extract_concepts(sentence: str) -> list[str]` - significant words, max 5

**Source:** `/tmp/opencodekit-template/.opencode/plugin/memory/curator.ts` (CURATOR_PATTERNS array)

##### `lib/markdown.py`
Memory file helpers:
- `read_memories(path: str) -> list[dict]` - parse memories.md into list of {type, title, content, date, confidence}
- `append_observation(path: str, observation: dict)` - append formatted block to memories.md
- `is_duplicate(title: str, existing_titles: set) -> bool` - fuzzy dedup (prefix match, first 40 chars)

### 4.6 References (7 files in `references/`)

Port from agent-skills `references/` directory. These are supplementary checklists that skills pull in when needed.

| Reference | Source | Content |
|---|---|---|
| definition-of-done.md | agent-skills | Project-wide standing bar: Correctness, Quality, Integration, Docs, Ship-readiness |
| testing-patterns.md | agent-skills | Test structure, naming, mocking, React/API/E2E examples, anti-patterns |
| security-checklist.md | agent-skills | Pre-commit checks, auth, input validation, headers, CORS, OWASP Top 10 |
| performance-checklist.md | agent-skills | Core Web Vitals targets, frontend/backend checklists, measurement commands |
| accessibility-checklist.md | agent-skills | Keyboard nav, screen readers, ARIA, testing tools |
| observability-checklist.md | agent-skills | On-call questions, RED/USE metrics, tracing, symptom-based alerting |
| orchestration-patterns.md | agent-skills | Multi-persona orchestration patterns, anti-patterns, personas-dont-invoke-personas rule |

**Source:** `https://github.com/addyosmani/agent-skills/tree/main/references/`

### 4.7 Templates (4 files in `templates/`)

#### `templates/spec-lite.md`

For simple, well-scoped work (bugs, small tasks). ~20 lines max.

```markdown
# [Title]

## Problem
[1-2 sentences: what's wrong or what's needed]

## Solution
[1-2 sentences: what to do]

## Affected Files
- `src/path/to/file.ts`

## Tasks
- [ ] [Task description] -> Verify: `[command]`

## Success Criteria
- Verify: `npm run typecheck && npm run lint`
- Verify: `[specific test or check]`
```

#### `templates/spec-full.md`

For features and complex work. Port from OpenCodeKit `.opencode/templates/` PRD template, adapted:
- Replace `.opencode/artifacts/` with `.factory/artifacts/`
- Remove OpenCode-specific references
- Add anti-rationalization section
- Add Red Flags section

**Source:** Read `/tmp/opencodekit-template/.opencode/templates/` for the full template.

#### `templates/plan.md`

Implementation plan template. Port the plan header structure from OCK `/plan` Phase 7:
- Must-Haves: Observable Truths, Required Artifacts, Key Links
- Dependency Graph: Task A -> Task B -> Task C (waves)
- Tasks: exact file paths, TDD order, 2-5 min steps, verification per task

#### `templates/progress.md`

Progress tracking template:
```markdown
# Progress: [Feature Name]

## Tasks
| # | Task | Status | Commit | Notes |
|---|------|--------|--------|-------|
| 1 | [desc] | [x]/[ ] | [hash] | [notes] |

## Blockers
- (none)

## Deviations
- (none)
```

### 4.8 MCP Config (`mcp.json`)

```json
{
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp",
      "disabled": true
    }
  }
}
```

Keep minimal. Users add their own MCP servers via `droid mcp add` or `/mcp` registry. context7 disabled by default (Droid has WebSearch built-in).

### 4.9 README.md

Document:
- What mdroid does
- Installation: `droid plugin marketplace add https://github.com/minhduydev/mdroid` + `droid plugin install mdroid@mdroid`
- Recommended companion plugins: Superpowers, security-engineer, droid-control, droid-evolved
- Recommended MCP servers: figma, playwright, supabase, sentry, linear (via `/mcp` registry)
- All 10 commands with usage
- All 7 droids with when to use
- Artifacts lifecycle explanation
- Hooks explanation

---

## 5. Workflow Design (Improved)

### 5.1 Triage Gate

Every user request passes through a mental triage gate before entering the workflow:

| Request type | Route | Artifacts? |
|---|---|---|
| Trivial (1 file, known fix) | Do directly | No |
| Bugfix (2-3 files) | `/fix` | Optional |
| Feature small (3-5 files) | `/spec` -> `/build --skip-plan` -> `/verify` -> `/ship` | Yes |
| Feature large (5+ files, multi-system) | `/spec` -> `/plan` -> `/build` -> `/verify` -> `/review` -> `/ship` | Yes |
| Research | `/research` | If active feature |
| Audit | `/audit` | Yes |
| Init project | `/init` | AGENTS.md + tech-stack.md |

### 5.2 Lifecycle Flow

```
User Request
     |
     v
[TRIAGE GATE]
     |
     +-- Trivial? -----> Do directly (no artifacts)
     |
     +-- Bugfix? ------> /fix ----> /verify ----> done
     |
     +-- Research? ----> /research ----> /spec (if feature) or done
     |
     +-- Audit? -------> /audit ----> /fix (if issues) or done
     |
     +-- Feature? -----> /spec
                            |
                            v
                         /plan (optional for simple)
                            |
                            v
                    /build (auto or task mode, TDD)
                            |
                            v
                    /verify (gates: typecheck, lint, test, build)
                            |
                            v
                    /review (4 personas parallel)
                            |
                            +-- Critical issues? -> /fix -> /verify -> /review
                            |
                            v
                    /ship (commit, PR, deploy)
                            |
                            v
                         DONE
     |
     +-- Init? --------> /init ----> /spec or /research
```

### 5.3 Artifacts & Memory Lifecycle

```
.factory/
  artifacts/
    .active                    # current slug (text file with slug name)
    <slug>/
      spec.md                   # PRD (from /spec)
      plan.md                   # Implementation plan (from /plan)
      progress.md               # Progress tracking (from /build)
      research.md               # Research findings (from /research)
      review.md                 # Review findings (from /review)
      verify.log                # Verification cache (from /verify)
      audit.md                  # Audit findings (from /audit)
    todo.md                    # Flat todo across all features
  memory/
    distillations/              # <session-id>.md files (TF-IDF compressed, one per session)
    session-state.json          # file trail + decisions (per session, ephemeral, Layer 1)
    session-summary.md          # anchored summary (survives Droid compression, Layer 2)
  memories.md                   # curated observations (append-only, grows over time, Layers 4+5)
```

**Memory flow per session:**
1. **SessionStart** → inject-memory.py reads memories.md → BM25 → injects relevant observations into context
2. **During session** → track-artifacts.py builds session-state.json (file trail + decisions)
3. **PreCompact** → save-summary.py writes session-summary.md (anchored, survives compression)
4. **Stop** → distill-session.py compresses transcript → distillations/<id>.md
5. **Stop** → curate-observations.py extracts patterns from distillation → appends to memories.md
6. **Next SessionStart** → inject-memory.py reads UPDATED memories.md → learning loop complete

### 5.4 Design Principles (applied to every command)

1. **Triage first** - Not every request needs full lifecycle
2. **Progressive complexity** - Simple / Standard / Deep modes
3. **Artifact-driven** - Each phase writes to .factory/artifacts/
4. **Droid-native** - Task tool, AskUser, Grep, Edit, hooks, Missions
5. **Anti-rationalization** - Common Rationalizations table in every command
6. **Red Flags** - Signs something's wrong, in every command
7. **Verification gates** - Non-negotiable, fresh evidence required
8. **Lean commands** - Each <300 lines (OCK /ship is 17k chars, too verbose)
9. **Natural chaining** - Each command knows its next step
10. **3-way combo** - Best of OpenCodeKit + agent-skills + Superpowers

---

## 6. Build Steps

### Step 1: Create directory structure

```bash
mkdir -p ~/workspace/mdroid/{.factory-plugin,droids,skills,hooks,references,templates}
```

### Step 2: Write plugin manifest

Create `.factory-plugin/plugin.json` (see section 4.1 above).

### Step 3: Port 8 custom droids

Read each file from `/tmp/opencodekit-template/.opencode/agent/`:
- `build.md`, `explore.md`, `plan.md`, `review.md`, `scout.md`, `vision.md`, `general.md`

Apply conversion rules (section 4.2). Write to `droids/`.

### Step 4: Write 10 workflow command skills

Write each SKILL.md following the command specifications (section 4.3). These are NOT verbatim ports - they are redesigned for Droid.

Key files to reference:
- OCK commands: `/tmp/opencodekit-template/.opencode/command/*.md` (source patterns)
- agent-skills SKILL.md format: `https://github.com/addyosmani/agent-skills/tree/main/skills` (anti-rationalization, Red Flags pattern)
- Superpowers TDD: `https://github.com/obra/superpowers/tree/main/skills/test-driven-development` (TDD cycle)

Each command must have:
- YAML frontmatter: `name`, `description` (with "Use when..." trigger)
- Triage gate (if applicable)
- Phases (numbered, lean)
- Anti-rationalization table
- Red Flags section
- Next step
- Related commands

### Step 5: Port ~15 unique skills

Port from the best source for each skill (section 4.4). Apply conversion rules. Write to `skills/<name>/SKILL.md`.

### Step 6: Build 5-layer memory system (hooks + lib)

This is the most complex step. Build in order:

**6a. Create hook configuration:**
- `hooks/hooks.json` (section 4.5 - 7 hooks across 5 events)

**6b. Build library modules first (hooks/lib/):**
- `lib/tokenize.py` - Port from OCK distill.ts: STOP_WORDS set + tokenize function. Source: `/tmp/opencodekit-template/.opencode/plugin/memory/distill.ts`
- `lib/tfidf.py` - Port from OCK distill.ts: compute_tf, compute_idf, extract_top_terms, select_key_sentences. Source: same file
- `lib/bm25.py` - Port BM25 scoring from OCK inject.ts. Source: `/tmp/opencodekit-template/.opencode/plugin/memory/inject.ts`
- `lib/patterns.py` - Port regex patterns from OCK curator.ts: CURATOR_PATTERNS + match_patterns. Source: `/tmp/opencodekit-template/.opencode/plugin/memory/curator.ts`
- `lib/markdown.py` - Memory file parser + append helpers (new, no OCK equivalent)

**6c. Build hook scripts in dependency order:**
- `hooks/track-artifacts.py` (Layer 1) - PreToolUse/PostToolUse → session-state.json
- `hooks/save-summary.py` (Layer 2) - PreCompact → session-summary.md
- `hooks/memory-capture-manual.py` (Manual) - UserPromptSubmit → memories.md (#/## prefix)
- `hooks/structural-check.sh` (Guard) - PostToolUse → validate architecture. Source: OCK `.opencode/tool/structural-check.sh`
- `hooks/distill-session.py` (Layer 3) - Stop → TF-IDF → distillations/. Depends on: lib/tfidf.py, lib/tokenize.py
- `hooks/curate-observations.py` (Layer 4) - Stop → regex → memories.md. Depends on: lib/patterns.py, lib/markdown.py
- `hooks/inject-memory.py` (Layer 5) - SessionStart → BM25 → inject context. Depends on: lib/bm25.py, lib/tfidf.py, lib/markdown.py

**6d. Test the memory system:**
```bash
# Test Layer 1: simulate hook input
echo '{"session_id":"test","tool_name":"Read","tool_input":{"file_path":"/tmp/test.txt"},"cwd":"/tmp"}' | python3 hooks/track-artifacts.py
cat .factory/memory/session-state.json  # verify file trail

# Test Layer 3: simulate Stop with a short transcript
echo '{"session_id":"test","transcript_path":"/tmp/test-transcript.jsonl","cwd":"/tmp"}' | python3 hooks/distill-session.py
ls .factory/memory/distillations/  # verify distillation created

# Test Layer 4: run after Layer 3
echo '{"session_id":"test","cwd":"/tmp"}' | python3 hooks/curate-observations.py
cat .factory/memories.md  # verify observation appended

# Test Layer 5: simulate SessionStart
echo '{"session_id":"test2","cwd":"/tmp","source":"startup"}' | python3 hooks/inject-memory.py
# verify JSON output with additionalContext field
```

**Key OCK source files to read for porting:**
- `/tmp/opencodekit-template/.opencode/plugin/memory/distill.ts` - TF-IDF engine + tokenize
- `/tmp/opencodekit-template/.opencode/plugin/memory/inject.ts` - BM25 scoring + query extraction
- `/tmp/opencodekit-template/.opencode/plugin/memory/curator.ts` - Regex patterns
- `/tmp/opencodekit-template/.opencode/plugin/memory/capture.ts` - Message capture patterns
- `/tmp/opencodekit-template/.opencode/plugin/memory/db.ts` - SQLite schema (adapt to JSON files)
- `/tmp/opencodekit-template/.opencode/plugin/session-summary.ts` - Structured summary format
- `/tmp/opencodekit-template/.opencode/tool/structural-check.sh` - Architecture validation

**Important:** The Python scripts must be executable and use `#!/usr/bin/env python3` shebang. Install no external dependencies (stdlib only: json, re, math, os, sys, datetime, pathlib, collections).

### Step 7: Port 7 reference checklists

Fetch from `https://github.com/addyosmani/agent-skills/tree/main/references/` and port to `references/`.

### Step 8: Write 4 templates

- `templates/spec-lite.md` (section 4.7)
- `templates/spec-full.md` (port from OCK `.opencode/templates/`)
- `templates/plan.md` (port plan header from OCK `/plan` Phase 7)
- `templates/progress.md` (section 4.7)

### Step 9: Write mcp.json

Minimal config (section 4.8).

### Step 10: Write README.md

Document everything (section 4.9).

### Step 11: Test locally

```bash
droid plugin marketplace add ~/workspace/mdroid
droid plugin install mdroid@mdroid
```

Verify:
- `/init` works
- `/spec "test feature"` creates artifacts
- `/build` reads spec and implements
- `/verify` runs gates
- `/review` spawns personas
- `/ship` commits
- Hooks fire on `#` messages
- Droids available via Task tool

### Step 12: Publish to GitHub

```bash
cd ~/workspace/mdroid
git init
git add .
git commit -m "feat: initial mdroid plugin v0.1.0"
# Create GitHub repo: minhduydev/mdroid
git remote add origin git@github.com:minhduydev/mdroid.git
git push -u origin main
```

### Step 13: Test installation from marketplace

```bash
droid plugin marketplace add https://github.com/minhduydev/mdroid
droid plugin install mdroid@mdroid
```

---

## 7. Recommended Companion Setup

For users installing mdroid, recommend these companion plugins and MCP servers:

### Companion plugins

```bash
# Official Factory plugins
droid plugin marketplace add https://github.com/Factory-AI/factory-plugins
droid plugin install droid-evolved@factory-plugins --scope user
droid plugin install security-engineer@factory-plugins --scope user
droid plugin install droid-control@factory-plugins --scope user

# Superpowers (community, 243k stars)
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

### Project-level setup (per project)

```bash
# In project root:
# 1. AGENTS.md (project conventions, build/test commands)
# 2. .factory/memories.md (project decisions, architecture history)
# 3. .factory/rules/ (coding standards per language)
# 4. Run /init to bootstrap AGENTS.md
```

---

## 8. Key Decisions Log

| Decision | Rationale | Date |
|---|---|---|
| Use Superpowers as primary router (not agent-skills) | Superpowers has Droid native install, 243k stars, subagent isolation. agent-skills warns against stacking 2 meta-routers. | 2026-07-01 |
| Port 7 droids from OpenCodeKit (not agent-skills personas) | OCK droids are more specialized (7 roles vs 4 personas). OCK droids have permission models. | 2026-07-01 |
| Port anti-rationalization + Red Flags pattern from agent-skills | Unique to agent-skills, not in OCK or Superpowers. High value for preventing agent deviation. | 2026-07-01 |
| Port 7 reference checklists from agent-skills | Supplementary material, progressive disclosure. Unique to agent-skills. | 2026-07-01 |
| Drop 60+ OCK skills, keep only ~15 unique | 70% overlap with agent-skills. Replaced by Superpowers + Factory plugins + MCP registry. | 2026-07-01 |
| Memory: 5-layer hook-based system | Replaces OCK 4-tier TypeScript plugin. Uses 7 Droid hooks + 5 Python scripts. Fully automatic, no LLM tokens (heuristic only: TF-IDF, BM25, regex). Cross-session learning via BM25 injection at SessionStart. Survives compression via anchored summary at PreCompact. | 2026-07-02 |
| Workflows -> Missions + Task tool (not workflow files) | Droid has Missions natively. Task tool replaces task(). No need for .md workflow files. | 2026-07-01 |
| Artifacts at .factory/artifacts/ (not .opencode/artifacts/) | Droid-native path convention. | 2026-07-01 |
| Commands as SKILL.md (not .factory/commands/) | Droid merged commands into skills. SKILL.md supports both user-invoked and model-invoked. | 2026-07-01 |
| Each command <300 lines | OCK /ship is 17k chars (too verbose). Lean commands = better token efficiency. | 2026-07-01 |
| Triage gate in every command | NEW concept. Prevents over-process for trivial tasks. Saves tokens + time. | 2026-07-01 |
| /build has auto mode (from agent-skills) | Plan + implement in 1 pass. Pauses on failures. OCK doesn't have this. | 2026-07-01 |
| /review as standalone command (not inside /ship) | Separation of concerns. OCK has review buried in /ship Phase 5. | 2026-07-01 |
| TDD cycle in /build (from Superpowers) | OCK doesn't have TDD. Superpowers has strict TDD. Use flexible TDD. | 2026-07-01 |
| No Iterative Quality Loop | Too heavy for most work. /verify + /review chain handles quality. | 2026-07-01 |

---

## 9. Session Continuation Guide

If you are resuming this work in a new session, follow these steps:

### Quick start

1. **Read this file:** `~/workspace/mdroid/BUILD_PLAN.md` (you are here)
2. **Check progress:** `ls ~/workspace/mdroid/` - what files exist already?
3. **Read OpenCodeKit source:** Files in `/tmp/opencodekit-template/.opencode/` (if still cloned)
4. **Re-clone if needed:** `git clone git@github.com:opencodekit/opencodekit-template.git /tmp/opencodekit-template`
5. **Fetch agent-skills references:** `https://github.com/addyosmani/agent-skills/tree/main/references/`
6. **Continue from Step X:** Check the build steps (section 6) and continue from where you left off

### What to read for context

| File/URL | Purpose |
|---|---|
| This file | Master plan, all decisions, all specs |
| `/tmp/opencodekit-template/.opencode/agent/*.md` | Source for 7 droids |
| `/tmp/opencodekit-template/.opencode/command/*.md` | Source patterns for 10 commands |
| `/tmp/opencodekit-template/.opencode/AGENTS.md` | Source for behavioral kernel |
| `/tmp/opencodekit-template/.opencode/templates/` | Source for spec/plan templates |
| `/tmp/opencodekit-template/.opencode/tool/structural-check.sh` | Source for structural-check hook |
| `/tmp/opencodekit-template/.opencode/plugin/memory/distill.ts` | Source for lib/tfidf.py + lib/tokenize.py |
| `/tmp/opencodekit-template/.opencode/plugin/memory/inject.ts` | Source for lib/bm25.py |
| `/tmp/opencodekit-template/.opencode/plugin/memory/curator.ts` | Source for lib/patterns.py |
| `/tmp/opencodekit-template/.opencode/plugin/memory/capture.ts` | Source for track-artifacts.py capture patterns |
| `/tmp/opencodekit-template/.opencode/plugin/session-summary.ts` | Source for save-summary.py format |
| `https://github.com/addyosmani/agent-skills/tree/main/skills` | Anti-rationalization + Red Flags pattern |
| `https://github.com/addyosmani/agent-skills/tree/main/references` | 7 reference checklists |
| `https://github.com/addyosmani/agent-skills/tree/main/agents` | 4 persona definitions (for review droid reference) |
| `https://github.com/obra/superpowers/tree/main/skills` | TDD cycle, subagent patterns |
| `https://docs.factory.ai/cli/configuration/custom-droids.md` | Droid format spec |
| `https://docs.factory.ai/cli/configuration/skills.md` | SKILL.md format spec |
| `https://docs.factory.ai/cli/configuration/plugins.md` | Plugin system spec |
| `https://docs.factory.ai/cli/configuration/hooks-guide.md` | Hooks format spec |
| `https://docs.factory.ai/cli/configuration/hooks-reference.md` | Hook event schemas (input JSON, output format) |
| `https://docs.factory.ai/evaluation/context-compression/` | Anchored iterative summarization research |
| `https://docs.factory.ai/guides/power-user/memory-management.md` | Memory hook pattern |
| `https://docs.factory.ai/guides/building/building-plugins.md` | Plugin build guide |

### Conversion cheat sheet (OpenCode -> Droid)

| OpenCode API | Droid equivalent |
|---|---|
| `task({ subagent_type: "X" })` | Task tool with `subagent_type: "X"` |
| `skill({ name: "X" })` | Skill tool with `skill: "X"` |
| `question({ questions: [...] })` | AskUser tool with `questionnaire: "..."` |
| `memory_search({ query: "X" })` | Grep tool on `.factory/memories.md` |
| `observation({ type: "X", ... })` | Edit tool on `.factory/memories.md` (append) |
| `.opencode/artifacts/` | `.factory/artifacts/` |
| `.opencode/agent/` | `.factory/droids/` (different format) |
| `.opencode/command/` | `.factory/skills/<name>/SKILL.md` |
| `.opencode/skill/` | `.factory/skills/<name>/SKILL.md` |
| `.opencode/plugin/` | Hooks + MCP (no TypeScript runtime) |
| `.opencode/tool/` | Hooks (shell scripts) or MCP servers |
| `.opencode/workflows/` | Missions or Task tool chaining (no workflow files) |
| `.opencode/opencode.json` | `.factory/settings.json` + `.factory/mcp.json` |
| `opencode/deepseek-v4-flash` | Use `inherit` or specific model ID |

### Common pitfalls

1. **Don't port OpenCode commands verbatim.** They reference OpenCode APIs that don't exist on Droid. Redesign following section 4.3.
2. **Don't duplicate ecosystem skills.** Check section 4.4 for what to port vs replace vs drop.
3. **Don't create workflow files.** Droid has Missions + Task tool. Use them directly in commands.
4. **Don't create a CLI.** Droid plugin system replaces the need for `ock` CLI.
5. **Don't forget anti-rationalization tables.** This is the key value-add from agent-skills.
6. **Don't exceed 300 lines per command.** Lean is critical for token efficiency.
7. **Don't use .opencode/ paths.** Use .factory/ paths everywhere.
8. **Don't reference memory_search or observation.** Use Grep + Edit on memories.md.
9. **Don't stack meta-routers.** Superpowers is the primary router. mdroid commands are lifecycle entry points, not a competing router.
10. **Don't forget the triage gate.** First thing in every command. Reject trivial tasks.

---

## 10. File Checklist

Track progress here. Mark `[x]` when each file is created and verified.

### Core
- [ ] `.factory-plugin/plugin.json`
- [ ] `mcp.json`
- [ ] `README.md`

### Droids (7)
- [ ] `droids/build.md`
- [ ] `droids/explore.md`
- [ ] `droids/plan.md`
- [ ] `droids/review.md`
- [ ] `droids/scout.md`
- [ ] `droids/vision.md`
- [ ] `droids/general.md`

### Workflow Commands (10)
- [ ] `skills/init/SKILL.md`
- [ ] `skills/spec/SKILL.md`
- [ ] `skills/plan/SKILL.md`
- [ ] `skills/build/SKILL.md`
- [ ] `skills/verify/SKILL.md`
- [ ] `skills/review/SKILL.md`
- [ ] `skills/ship/SKILL.md`
- [ ] `skills/fix/SKILL.md`
- [ ] `skills/research/SKILL.md`
- [ ] `skills/audit/SKILL.md`

### Unique Skills (~15)
- [ ] `skills/behavioral-kernel/SKILL.md`
- [ ] `skills/defense-in-depth/SKILL.md`
- [ ] `skills/incremental-implementation/SKILL.md`
- [ ] `skills/development-lifecycle/SKILL.md`
- [ ] `skills/doubt-driven-development/SKILL.md`
- [ ] `skills/context-engineering/SKILL.md`
- [ ] `skills/interview-me/SKILL.md`
- [ ] `skills/observability-and-instrumentation/SKILL.md`
- [ ] `skills/deprecation-and-migration/SKILL.md`
- [ ] `skills/api-and-interface-design/SKILL.md`
- [ ] `skills/documentation-and-adrs/SKILL.md`
- [ ] `skills/ci-cd-and-automation/SKILL.md`
- [ ] `skills/shipping-and-launch/SKILL.md`
- [ ] `skills/grill-me/SKILL.md`

### Hooks (12)
- [ ] `hooks/hooks.json`
- [ ] `hooks/track-artifacts.py` (Layer 1: file trail)
- [ ] `hooks/save-summary.py` (Layer 2: anchored summary)
- [ ] `hooks/distill-session.py` (Layer 3: TF-IDF distill)
- [ ] `hooks/curate-observations.py` (Layer 4: regex curate)
- [ ] `hooks/inject-memory.py` (Layer 5: BM25 inject)
- [ ] `hooks/memory-capture-manual.py` (Manual: #/## capture)
- [ ] `hooks/structural-check.sh` (Guard: architecture validation)
- [ ] `hooks/lib/tokenize.py` (Tokenization + stop words)
- [ ] `hooks/lib/tfidf.py` (TF-IDF engine)
- [ ] `hooks/lib/bm25.py` (BM25 scoring)
- [ ] `hooks/lib/patterns.py` (Regex curator patterns)
- [ ] `hooks/lib/markdown.py` (Memory file read/write helpers)

### References (7)
- [ ] `references/definition-of-done.md`
- [ ] `references/testing-patterns.md`
- [ ] `references/security-checklist.md`
- [ ] `references/performance-checklist.md`
- [ ] `references/accessibility-checklist.md`
- [ ] `references/observability-checklist.md`
- [ ] `references/orchestration-patterns.md`

### Templates (4)
- [ ] `templates/spec-lite.md`
- [ ] `templates/spec-full.md`
- [ ] `templates/plan.md`
- [ ] `templates/progress.md`

**Total: ~60 files**

---

## 11. Quality Gates for This Plugin

Before publishing, verify:

- [ ] All droids have valid YAML frontmatter (`name`, `description`, `model`, `tools`)
- [ ] All skills have valid YAML frontmatter (`name`, `description` with "Use when...")
- [ ] No file exceeds 300 lines (commands, skills) or 500 lines (droids)
- [ ] No `.opencode/` paths remain (all converted to `.factory/`)
- [ ] No OpenCode API calls remain (`task()`, `skill()`, `question()`, `memory_search`, `observation`)
- [ ] Every command has anti-rationalization table + Red Flags
- [ ] Every command has triage gate (if applicable)
- [ ] Every command has "Next:" step
- [ ] Plugin installs successfully: `droid plugin install mdroid@mdroid`
- [ ] `/init` works end-to-end
- [ ] `/spec "test"` creates artifacts
- [ ] `/build` reads spec and implements
- [ ] `/verify` runs gates
- [ ] `/review` spawns personas via Task tool
- [ ] `/ship` commits with user confirmation
- [ ] Memory hook fires on `#` prefix messages
- [ ] Structural-check hook fires on file edits
- [ ] Layer 1: track-artifacts.py captures file trail to session-state.json
- [ ] Layer 2: save-summary.py writes anchored session-summary.md on PreCompact
- [ ] Layer 3: distill-session.py creates distillations/<id>.md on Stop
- [ ] Layer 4: curate-observations.py appends observations to memories.md on Stop
- [ ] Layer 5: inject-memory.py outputs JSON with additionalContext on SessionStart
- [ ] Cross-session learning: observations from session 1 appear in session 2 context
- [ ] All Python scripts use stdlib only (no pip install needed)
- [ ] All Python scripts have `#!/usr/bin/env python3` shebang
- [ ] lib/tfidf.py TF-IDF scores match expected output on test data
- [ ] lib/bm25.py BM25 scores match expected output on test data
- [ ] lib/patterns.py regex patterns match expected types on test sentences
- [ ] All 7 droids available via Task tool
- [ ] README documents all commands and droids
