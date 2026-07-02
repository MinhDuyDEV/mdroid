---
name: mission-prep
description: Prepare a repository for Factory Missions. Checks readiness, ensures AGENTS.md, sets up QA scripting, and recommends mission model settings. Use before running /missions for multi-feature projects.
user-invocable: true
disable-model-invocation: true
---

# /mission-prep - Prepare for Missions

Prepare your repository so Factory Missions can plan, execute, and validate work reliably.

## When to use

- Before running `/missions` for the first time on a project.
- When a mission fails validation repeatedly (QA cannot run).
- When starting a large multi-feature project that needs orchestration.

## Phase 1: Readiness check

1. Run `/readiness-report` to evaluate the repo's AI-readiness level (1-5).
2. Missions need **Level 4 (Optimized) or above** for best results.
3. If below Level 4, run `/readiness-fix` to close gaps.
4. Key criteria to verify:
   - [ ] Linter configured (catches errors immediately, no debugging cycles).
   - [ ] Type checker configured (prevents runtime errors).
   - [ ] Unit tests runnable (verification in same turn).
   - [ ] AGENTS.md exists (context upfront, less exploration).
   - [ ] Build command documented (no guessing).
   - [ ] Dependencies pinned (reproducible builds).

If any high-impact criteria are missing, fix them before proceeding.

## Phase 2: AGENTS.md

1. Read `AGENTS.md` (or run `/init` if it doesn't exist).
2. Verify it contains:
   - Build, test, lint, typecheck commands.
   - Project structure map.
   - Coding conventions.
   - Testing strategy.
3. If missing sections, update AGENTS.md.

## Phase 3: .factory/rules/ setup

1. Check if `.factory/rules/` exists.
2. If not, create it with stub files for the project's languages:
   - `typescript.md` or `python.md` or `go.md` etc.
   - `testing.md`
   - `security.md`
3. Reference rules in AGENTS.md:
   ```
   ## Coding Standards
   Follow `.factory/rules/` conventions.
   ```
4. See the rules-conventions guide for rule file templates.

## Phase 4: QA scripting (critical for mission validation)

Missions validate their own work by exercising your running application. Without reliable QA scripting, validators fail repeatedly.

### Checklist

- [ ] **One command to start the app.** Provide a single script that starts all services (backend, frontend, dependencies).
  ```bash
  # Example: scripts/dev.sh
  #!/bin/bash
  docker compose up -d db redis
  npm run dev:server &
  npm run dev:client
  ```
- [ ] **Route logs to the filesystem.** Send application logs to files so Droid can read and inspect them.
  ```
  # In AGENTS.md
  ## Logs
  - App logs: ./logs/app.log
  - Server logs: ./logs/server.log
  - Error logs: ./logs/error.log
  ```
  **Security**: Redact secrets, PII, tokens from file logs. Restrict file permissions. Add log files to `.gitignore`.
- [ ] **Keep resource usage modest.** Ensure the app doesn't consume too much RAM/CPU/disk. Workers run alongside the app.
- [ ] **Provide a way to send input.** Give Droid a programmatic way to drive the app.
  - Web app: `tuistory` and `agent-browser` skills are available by default.
  - Terminal app: `tuistory` skill.
  - API: provide a test client script or curl examples.
  - Other: build a custom toolchain for driving the app.

### If QA is not needed

If the project doesn't need QA-style validation (e.g., library, CLI tool, data pipeline):
- Document this in AGENTS.md: "This project does not require user-facing QA validation."
- During mission planning, disable user-testing validation in Mission Control settings.

## Phase 5: Mission model settings

Recommend optimal model configuration for the project. Add to project `.factory/settings.json`:

```json
{
  "missionModelSettings": {
    "workerModel": "<fast model for implementation>",
    "workerReasoningEffort": "low",
    "validationWorkerModel": "<strong model for validation>",
    "validationWorkerReasoningEffort": "high"
  },
  "missionOrchestratorModel": "<strongest model for planning>",
  "missionOrchestratorReasoningEffort": "high"
}
```

### Recommendations

| Role | Model strategy | Reasoning |
|---|---|---|
| Orchestrator | Strongest available (e.g., Opus) | high |
| Worker | Fast, capable (e.g., Sonnet, Codex) | low/medium |
| Validator | Strong (e.g., Opus, Sonnet) | high |

Pairing a strong orchestrator with a faster worker model is the standard cost-quality tradeoff: planning and validation benefit most from extra reasoning, while routine worker tasks can use a lighter model.

### Headless missions

For CI/scheduled missions:
```bash
droid exec --mission \
  --worker-model <model> \
  --worker-reasoning-effort medium \
  --validator-model <model> \
  --validator-reasoning-effort high \
  -f mission.md
```

## Phase 6: Autonomy level

Missions require **High autonomy**. Verify:
1. Current autonomy level: press `Ctrl+L` to cycle, or check `/settings`.
2. If org policy caps autonomy below High, Missions may be restricted.
3. For headless: `droid exec --mission --auto high`.

## Phase 7: Memory and hooks check

1. Verify `.factory/memories.md` exists (or will be created by mdroid hooks).
2. Verify hooks are enabled: `/hooks` should show mdroid's 5-layer memory system.
3. Hooks fire during missions automatically - no extra config needed.
4. Cross-mission learning: decisions from mission 1 are captured by Stop hooks and injected into mission 2 via SessionStart.

## Phase 8: Final verification

Run through this checklist before starting the mission:

- [ ] Readiness Level >= 4 (or gaps documented and accepted).
- [ ] AGENTS.md complete with commands, structure, conventions.
- [ ] `.factory/rules/` created with language-specific standards.
- [ ] QA scripting: one-command startup, filesystem logs, input mechanism.
- [ ] Mission model settings configured (orchestrator=strong, worker=fast, validator=strong).
- [ ] Autonomy level set to High.
- [ ] Hooks enabled (mdroid memory system active).
- [ ] `.gitignore` excludes logs, `.factory/memory/`, `.factory/memories.md`.

## Phase 9: Launch

Once all checks pass:
1. Run `/missions` to start collaborative planning.
2. Describe the multi-feature goal.
3. Droid builds a plan: features, milestones, skills.
4. Approve the plan -> Mission Control begins execution.
5. Monitor progress, intervene when needed (pause orchestrator, redirect).

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "The repo is fine, I'll skip readiness" | Missions at Level <4 produce unreliable results. Check it. |
| "QA scripting is too much setup" | Without it, validators fail repeatedly and waste tokens. Set it up. |
| "I'll use the default models" | Default models may not optimize cost vs quality. Configure worker/validator split. |
| "Autonomy High is dangerous" | Missions require it. Use sandbox or denylist for safety. |
| "Logs to filesystem is overkill" | Terminal-only logs are invisible to workers. File logs are inspectable. |

## Red Flags

- Starting a mission without readiness check.
- No QA scripting (validators will fail).
- No AGENTS.md (workers explore blindly, wasting tokens).
- No .gitignore for logs (secrets leak into git).
- Using the same model for orchestrator and workers (wastes cost or sacrifices quality).
- No filesystem logs (workers can't debug failures).
