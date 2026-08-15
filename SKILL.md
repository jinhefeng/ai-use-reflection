---
name: ai-use-reflection
description: Analyze a visible Codex session and a local cross-session Wiki to identify the human's contribution, update evidence-linked AI collaboration capabilities and domain knowledge, generate review prompts after session thresholds, and refresh a self-contained HTML dashboard. Use when the user asks to review an AI session, track cross-session collaboration growth, update a reflective Wiki, generate or refresh the reflection dashboard, or configure session-based review reminders.
---

# AI Use Reflection

Maintainer: **Jin Hefeng**<br>
Project repository: [github.com/jinhefeng/ai-use-reflection](https://github.com/jinhefeng/ai-use-reflection)

## Purpose

Use this skill to turn visible human–AI collaboration into a small, reviewable learning loop. Analyze the current session, distinguish the human's decisions from the AI's execution, propose updates to two separate long-term tracks, and present the result through a Wiki and one generated HTML dashboard.

The canonical long-term data is a set of small Markdown Wiki pages. The HTML file is a generated view, not the source of truth.

## Operating rules

- Analyze only content visible in the current session and files explicitly available in the workspace. Never claim to have read hidden or historical chat logs.
- Separate evidence, interpretation, and recommendation. Link every durable claim to a session page or other local evidence.
- Keep the AI collaboration capability track separate from the domain knowledge track. Prompting skill is not domain expertise.
- Do not infer personality, psychological traits, employee performance, intelligence, or human worth.
- Summarize the human's influence on outcomes without treating the AI as an independent owner of the result.
- Draft durable changes first. Ask the user to confirm, edit, or reject them before updating long-term capability or knowledge pages.
- Record a compact session index even when a full review is deferred. Do not copy a full transcript into the Wiki.
- Keep evidence snippets short and paraphrase by default; preserve exact wording only when it materially supports the conclusion.
- Never overwrite an existing Wiki page blindly. Append a dated evidence entry or create a focused page when a topic is new.

## Storage contract

Use `.ai-reflection/` at the project root unless the user specifies another store:

```text
.ai-reflection/
├── wiki/
│   ├── index.md
│   ├── sessions/<session-id>.md
│   ├── capabilities/<capability-slug>.md
│   ├── knowledge/<domain>/<topic-slug>.md
│   └── trends/<period>.md
├── data/
│   ├── session-index.jsonl
│   ├── current-review.json
│   └── link-index.json
└── reflection-dashboard.html
```

Use `scripts/bootstrap_store.py` to create the store without overwriting existing content. Use `scripts/register_session.py` to append a compact session record and determine whether a review suggestion is due. Use `scripts/mark_reviewed.py` after a confirmed review to close the reviewed batch. Use `scripts/build_dashboard.py` after a confirmed review or Wiki update.

Read only the current session, the relevant Wiki pages, and recent linked sessions. Use `data/link-index.json` or the Wiki index to avoid loading the entire knowledge base into context.

## Workflow

### 1. Register the session quietly

At the end of an eligible session, record only metadata: stable session ID, title, topics, completion state, review state, and a short focus summary. Treat very short or purely administrative turns as ineligible unless the user asks for a review.

Run:

```bash
python3 scripts/register_session.py --store .ai-reflection --session-id 2026-08-15-001 --title "Skill design" --topics "skill design,reflection" --summary "Defined cross-session Wiki and HTML dashboard requirements."
```

Use the script's `review_due` result to decide whether a suggestion should be shown. The default threshold is three eligible, unreviewed sessions; support a different threshold when the user configures one.

### 2. Show a low-friction review suggestion

When a review is due, show a compact preview before asking for consent:

1. Summarize three to five important points from the current session.
2. Name the likely long-term changes, if any.
3. Offer `复盘`, `稍后`, and `不再提示` as conversational choices.

Do not make the user type a fixed command. A manual request such as “复盘本次会话” remains supported as an override.

The skill itself cannot run in the background or receive an end-of-session event. If proactive prompting is requested, use an available application hook, automation, or session wrapper to invoke the registration step. Keep that trigger layer separate from the analysis and storage logic.

### 3. Analyze the current session

Build a concise session page with these sections:

- Objective and outcome
- Human actions that changed the result
- AI actions that accelerated or constrained the work
- Evidence-backed strengths
- Friction, rework, or missed opportunities
- Decisions and unresolved questions
- Proposed capability updates
- Proposed knowledge updates
- One or two next-session experiments

Analyze these capability dimensions when relevant: goal framing, context provision, constraints, decomposition, delegation, prompt iteration, verification, correction, tool selection, and judgment boundaries.

For domain knowledge, record only observable changes: concepts encountered, explanations the user refined, decisions made, artifacts produced, verified facts, and open questions. Do not label a topic as mastered from one conversation.

### 4. Update the Wiki after confirmation

Create or update the session page first. Then apply only user-confirmed deltas to capability and knowledge pages. Prefer an evidence log over a single score:

```yaml
status: improving
confidence: medium
evidence:
  - session: 2026-08-15-001
    note: "主动补充了触发策略、Wiki 拆分和 HTML 展示约束。"
next_experiment: "在任务开始时先写出验收标准。"
```

Use qualitative trend states such as `emerging`, `stable`, `improving`, `needs-verification`, and `stale`. If a quantitative score is requested, show the evidence and uncertainty beside it; never present an unsupported number as measurement.

### 5. Generate the HTML dashboard

Run `scripts/build_dashboard.py` with the store path and output path. The generated `reflection-dashboard.html` should show:

- the latest session review and key points;
- current capability states and evidence counts;
- knowledge topics and open questions;
- a recent session timeline;
- trend pages and links to source Wiki pages;
- maintainer attribution to Jin Hefeng and the GitHub project link.

Keep the HTML self-contained: inline CSS, inline small summary data, and no network dependency. Do not embed the full Wiki or transcript. Use relative links from the dashboard to the Markdown pages so the dashboard remains small.

After a successful review, return clickable links to the current review, the dashboard, and the most relevant Wiki pages.

## Privacy and correction loop

Treat the Wiki as user-controlled memory. Before durable writes, state what will be added or changed. Support explicit corrections such as “删掉这条”“这不是能力提升”“把它归到另一个主题”. Preserve rejected proposals only in a pending queue when the user wants an audit trail; otherwise do not retain them.

If the store is missing, initialize it with the bootstrap script. If the workspace contains multiple plausible project roots, ask the user to choose rather than writing to a broad directory.

## Validation

Before handing off a skill change:

1. Run `scripts/quick_validate.py` from the skill-creator package when its dependencies are available.
2. Run the local scripts against a temporary fixture store.
3. Open or inspect the generated HTML and verify that it contains current review, capability, knowledge, trend, source links, attribution, and no external asset dependency.
4. Check that existing Wiki pages and unrelated files were not overwritten.

## Maintainer

Jin Hefeng — [https://github.com/jinhefeng/ai-use-reflection](https://github.com/jinhefeng/ai-use-reflection)
