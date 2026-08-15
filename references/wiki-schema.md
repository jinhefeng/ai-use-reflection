# AI Use Reflection Wiki Schema

Maintainer: Jin Hefeng — https://github.com/jinhefeng

## Principles

- Keep pages small and focused; split a page when it becomes difficult to load selectively.
- Store durable claims as evidence-linked deltas, not an all-time narrative.
- Keep capability pages and domain knowledge pages in separate namespaces.
- Use stable slugs and session IDs so links remain valid when summaries evolve.

## Page types

### Session page

Path: `wiki/sessions/<session-id>.md`

```yaml
---
type: session-review
session_id: 2026-08-15-001
title: "Skill design"
date: 2026-08-15
topics: [skill-design, reflection]
---
```

Required sections: `Objective`, `Key Points`, `Human Contribution`, `AI Contribution`, `Evidence`, `Friction`, `Proposed Updates`, and `Next Experiments`.

### Capability page

Path: `wiki/capabilities/<capability-slug>.md`

```yaml
---
type: capability
slug: result-verification
title: "结果验证"
status: improving
confidence: medium
updated: 2026-08-15
---
```

Keep a short current statement followed by an `Evidence Log` table. Each row must link to a session page.

### Knowledge page

Path: `wiki/knowledge/<domain>/<topic-slug>.md`

```yaml
---
type: knowledge
domain: ai-skill-design
topic: "Session reflection"
status: emerging
confidence: medium
updated: 2026-08-15
---
```

Use sections for `Working Understanding`, `Verified`, `Open Questions`, `Artifacts`, and `Sources`. A working understanding is not a verified fact.

### Trend page

Path: `wiki/trends/<period>.md`

Use a period such as `2026-08` or `2026-Q3`. Summarize changes across sessions and link to the capability, knowledge, and session pages that support the summary.

## Compact indexes

`data/session-index.jsonl` contains one JSON object per eligible session. Keep summaries short and do not store transcripts there.

`data/current-review.json` contains the most recent review payload used by the dashboard. It may be replaced after a later confirmed review.

`data/link-index.json` can map topics and slugs to relative files. It is an optimization layer; Wiki pages remain authoritative.

## Evidence rules

Use three labels in analysis:

- `evidence`: directly observable from the session or artifact;
- `interpretation`: a cautious explanation of why the evidence mattered;
- `recommendation`: a future behavior to try.

Do not merge these into one unsupported statement. Prefer “three sessions show…” to an invented global score.
