---
name: research
description: External research with confidence levels and source citations. Searches web, fetches docs, and synthesizes findings. Supports simple (direct) and complex (fan-out via Task tool) modes. Use before /spec for unknowns or standalone for investigation.
user-invocable: true
disable-model-invocation: true
---

# /research - External Research

Gather external information with explicit confidence levels and source citations.

## Complexity detection

- **Simple**: The question can be answered with a few searches. ~30 tool calls max. Execute directly.
- **Complex**: The question requires multiple sub-questions, cross-checking, and synthesis. Fan out scout droids via Task tool.

Auto-detect: if the question has 1-2 key terms and a clear answer format -> simple. If it has multiple facets, conflicting sources likely, or needs deep synthesis -> complex.

## Phase 1: Parse the question

1. Identify the core question and key terms.
2. Identify sub-questions if complex.
3. Determine what "done" looks like: a decision? a comparison? a how-to?

## Phase 2: Source priority

Search in this order:
1. **Codebase** (Grep/Glob): Is the answer already in the project?
2. **Official docs** (WebSearch with site filters, or FetchUrl of known doc URLs).
3. **Source code** (FetchUrl of GitHub source files).
4. **GitHub** (issues, discussions, PRs via WebSearch + FetchUrl).
5. **General web** (blogs, forums, Stack Overflow).

## Phase 3: Execute (simple mode)

1. WebSearch for the key terms.
2. FetchUrl the most promising official doc URLs.
3. If conflicting info, find 2+ sources to cross-check.
4. Synthesize with confidence levels.

## Phase 3: Execute (complex mode)

1. Break the question into sub-questions.
2. Use the Task tool to spawn `scout` droids in parallel, one per sub-question.
3. Each scout returns findings with confidence levels and URLs.
4. Collect all findings.
5. Cross-check: do findings agree? Resolve conflicts by finding authoritative sources.
6. Synthesize.

## Phase 4: Confidence levels

Tag every claim:
- **HIGH**: Confirmed by official docs + source code. Unambiguous.
- **MEDIUM**: Reputable secondary source (established blog, popular GitHub repo, conference talk).
- **LOW**: Single blog post, forum answer, or unverified claim.

## Phase 5: Stop conditions

- Stop after ~30 tool calls (simple mode).
- Stop when findings converge: 3+ independent sources agree.
- Stop when official sources are exhausted and no further authoritative sources exist.
- Don't stop if key claims have only LOW confidence and higher sources might exist.

## Phase 6: Write findings

If there's an active feature (`.factory/artifacts/.active` exists):
- Write to `.factory/artifacts/<slug>/research.md`.

If standalone, report directly to the user.

## Output format

```markdown
# Research: [question]

## Summary
[1-3 sentence answer]

## Findings
1. [claim] (confidence: HIGH) - [URL]
   [supporting detail]
2. [claim] (confidence: MEDIUM) - [URL]
   [supporting detail]

## Sources
- [URL1] - [what it confirmed]
- [URL2] - [what it confirmed]

## Gaps
- [what couldn't be confirmed and why]
- [suggested follow-up research]
```

## Next

- If researching for a feature -> suggest `/spec` with these findings.
- If standalone -> done.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "One blog post said X" | One source = LOW confidence. Find more. |
| "The docs probably cover this" | Fetch them. Don't assume. |
| "I'll skip checking the source code" | Source code is HIGH confidence. Don't skip. |
| "This is common knowledge" | Cite it. Common knowledge is often wrong. |
| "I have enough sources" | If they're all LOW confidence, you don't. |

## Red Flags

- Claims without source URLs.
- HIGH confidence on a single blog post.
- Not checking official documentation first.
- Synthesizing before gathering enough sources.
- No gaps section (there are always gaps).

## Related Commands

- `/spec` - Define a feature using these research findings.
- `/audit` - Audit codebase patterns (internal research).
