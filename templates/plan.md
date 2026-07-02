# Plan: [Feature Name]

## Must-Haves

### Observable Truths
[How we know the plan is complete - what's observable and testable]
- [Truth 1: e.g., "User can log in and see dashboard"]
- [Truth 2: e.g., "Invalid credentials show error"]

### Required Artifacts
[Files that must exist or be modified]
- `src/auth/login.ts` - [what it does]
- `src/auth/login.test.ts` - [what it tests]

### Key Links
[Relevant docs, issues, PRs]
- Spec: `.factory/artifacts/<slug>/spec.md`
- [Issue/PR links if any]

## Dependency Graph

```
W0 (prefactor) ---> T1 (wave 1) ---> T3 (wave 2)
                   T2 (wave 1) ---> T3 (wave 2)
                   T3 (wave 2) ---> T4 (wave 3)
```

## Tasks

### Wave 0 (prefactoring, optional — must complete before feature work)

- **[P1]** [Preparatory refactor that makes the feature easier]
  - Files: `src/path/to/refactor.ts`
  - Depends on: none
  - Verify: `[command]`
  - TDD: write failing test -> implement -> refactor

### Wave 1 (no dependencies)

- **[T1]** [Description — a vertical slice cutting through all layers]
  - Files: `src/path/to/file.ts`
  - Depends on: [P1 if applicable, else none]
  - Verify: `[command]`
  - TDD: write failing test -> implement -> refactor

- **[T2]** [Description]
  - Files: `src/path/to/other.ts`
  - Depends on: none
  - Verify: `[command]`
  - TDD: write failing test -> implement -> refactor

### Wave 2 (depends on Wave 1)

- **[T3]** [Description]
  - Files: `src/path/to/file3.ts`
  - Depends on: [T1, T2]
  - Verify: `[command]`

### Wave 3 (depends on Wave 2)

- **[T4]** [Description]
  - Files: `src/path/to/file4.ts`
  - Depends on: [T3]
  - Verify: `[command]`

## Constitutional Compliance

- [ ] Every task has a verification command.
- [ ] No task exceeds ~5 minutes of work.
- [ ] Dependencies are acyclic.
- [ ] Plan delivers all spec success criteria.
- [ ] No task touches more than 5 files.
