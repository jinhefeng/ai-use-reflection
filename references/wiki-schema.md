# AI Use Reflection Wiki Schema

Maintainer: Jin Hefeng — https://github.com/jinhefeng/ai-use-reflection

## Principles

- Keep pages small and focused; split a page when it becomes difficult to load selectively.
- Store durable claims as evidence-linked deltas, not an all-time narrative.
- Keep capability pages and domain knowledge pages in separate namespaces.
- Keep intervention efficacy and task contribution evidence in their own namespaces.
- Use stable slugs and session IDs so links remain valid when summaries evolve.
- Keep user data outside the installed skill package and outside the public repository.

## Portable storage resolution

The skill resolves a logical `<reflection-root>` at runtime. Never hardcode a machine-specific absolute path in the skill.

Resolution order:

1. `--store <path>` supplied for the current operation;
2. `AI_USE_REFLECTION_HOME` for a user-selected shared store;
3. the host's standard per-user data directory;
4. project-local `.ai-use-reflection/` only with explicit `--scope project`.

Use `scripts/resolve_storage.py` to display the resolved path, scope, and source before writing. A user who wants several AI IDEs to share one archive should set the same `AI_USE_REFLECTION_HOME` in each host. A public skill repository must never be used as the personal archive.

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

### Intervention efficacy page

Path: `wiki/interventions/<dimension-slug>.md`

Track repeated patterns such as `early-constraints`, `correction-precision`, `verification-coverage`, or `delegation`. Store the current state, evidence links, confidence, and the next experiment. Do not store a single unexplained score.

### Task contribution page

Path: `wiki/contributions/<category-slug>.md`

Use this namespace for evidence that the user supplied direction, context, judgment, verification, or accountability that affected a concrete outcome. This is not a personal worth or performance profile.

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

The current review may include:

```json
{
  "interventions": [
    {
      "event_id": "I-01",
      "turn_ref": "user correction after draft",
      "type": ["correction", "constraint"],
      "signal": "The output used an absolute local path.",
      "mechanism": "Replaced the storage contract with runtime resolution.",
      "outcome": "The skill became usable across AI IDEs.",
      "observable_cost": "One correction turn; avoided a later portability rewrite.",
      "efficacy": {"leverage": "high", "timing": "medium", "verification": "medium"},
      "confidence": "high",
      "evidence": ["current session: storage discussion"]
    }
  ],
  "intervention_efficacy": {
    "overall": "medium",
    "confidence": "medium",
    "dimensions": {"leverage": "high", "timing": "low"},
    "guidance": ["Move acceptance criteria earlier."]
  },
  "human_task_contribution": [
    {"category": "decisive", "note": "Defined the acceptance boundary.", "confidence": "high"}
  ],
  "guidance_examples": [
    {
      "scenario": "约束出现过晚",
      "original_prompt": "这部分不能改。",
      "diagnosis": "约束有效但没有在执行前进入 AI 的决策空间。",
      "improved_prompt": "开始前先确认：保持 API 和目录结构不变；突破前先停下说明。",
      "expected_gain": "减少返工并提高风险覆盖。",
      "test_in_next_session": "记录是否发生越界和二次实现。"
    }
  ]
}
```

`data/link-index.json` can map topics and slugs to relative files. It is an optimization layer; Wiki pages remain authoritative.

## Evidence rules

Use three labels in analysis:

- `evidence`: directly observable from the session or artifact;
- `interpretation`: a cautious explanation of why the evidence mattered;
- `recommendation`: a future behavior to try.

Do not merge these into one unsupported statement. Prefer “three sessions show…” to an invented global score.
