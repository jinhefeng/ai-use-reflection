---
name: ai-use-reflection
description: Analyze a visible AI IDE session and a portable cross-session Wiki to identify the human's contribution, update evidence-linked AI collaboration capabilities and domain knowledge, generate review prompts after session thresholds, and refresh a self-contained HTML dashboard. Use when the user asks to review an AI session, track cross-session collaboration growth across tools or projects, update a reflective Wiki, generate or refresh the reflection dashboard, configure session-based review reminders, or choose the runtime archive location.
---

# AI Use Reflection

Maintainer: **Jin Hefeng**<br>
Project repository: [github.com/jinhefeng/ai-use-reflection](https://github.com/jinhefeng/ai-use-reflection)

## Purpose

Use this skill to turn visible human–AI collaboration into a small, reviewable learning loop. Analyze the current session, distinguish the human's decisions from the AI's execution, propose updates to two separate long-term tracks, and present the result through a Wiki and one generated HTML dashboard.

The canonical long-term data is a set of small Markdown Wiki pages. The HTML file is a generated view, not the source of truth.

## Core model: intervention efficacy and task contribution

Make the primary question: **How efficiently did the user's intervention improve the AI's trajectory and the task outcome?**

Treat an intervention as any user action that changes direction, context, constraints, decomposition, delegation, correction, verification, approval, or stopping decisions. For each meaningful intervention, trace:

1. **Signal** — what the user added or changed;
2. **Mechanism** — how it changed the AI's plan, assumptions, output, or risk;
3. **Outcome** — what quality, scope, accuracy, rework, or risk result followed;
4. **Observable cost** — turns, revisions, delay, or repeated explanation when visible;
5. **Guidance** — how to make a similar intervention earlier, clearer, or more selective next time.

Evaluate efficacy as a vector, not an unsupported single score:

- leverage: did the intervention materially change the trajectory?
- precision: did it address the root issue rather than a symptom?
- timing: did it arrive before avoidable work?
- economy: did it reduce unnecessary turns or rework?
- coverage: did it protect the goal, constraints, acceptance criteria, and risks?
- verification: did it establish enough evidence to trust the result?

Use `high`, `medium`, `low`, or `uncertain` with confidence and evidence. Do not treat prompt length, token count, or number of messages as value by themselves.

Load [references/intervention-rubric.md](references/intervention-rubric.md) when tagging intervention events, comparing efficacy dimensions, or writing task-contribution evidence.

Assess human contribution to the concrete task in separate categories: direction and prioritization, domain context, constraints and risk judgment, decision quality, verification, and final accountability. Use labels such as `decisive`, `enabling`, `supporting`, `necessary`, or `uncertain`, and link each conclusion to evidence. This is an assessment of contribution to a task, never a rating of the person's overall worth, intelligence, personality, or employment performance.

The useful output is a loop:

```text
intervention trace → efficacy assessment → task-contribution evidence → next-use guidance → next session test
```

Use a compact intervention ledger for every substantive review. One row is one
user move that changed the AI's decision space; do not create one row per
message. At minimum record `event_id`, `turn_ref`, `type`, `signal`,
`mechanism`, `outcome`, `observable_cost`, `efficacy`, `confidence`, and
`evidence`. This ledger is the bridge between the visible conversation and
the long-term intervention Wiki.

Assess efficiency as useful outcome change relative to observable intervention
cost. Prefer comparisons such as "prevented a likely rework cycle" or
"corrected the root assumption after two late turns" over activity measures
such as prompt length, token count, or message count. Do not invent a
counterfactual; use `uncertain` when the session does not show what changed.
When summarizing human contribution, distinguish "the user supplied the
decision or constraint that enabled the result" from "the user performed the
execution." The first can be decisive even when the AI performed most of the
mechanical work.

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

Keep the skill package and user data separate. Never write personal records into the installed skill directory or the public GitHub repository.

Resolve one runtime `<reflection-root>` for the current host. Use the shared per-user store by default:

1. explicit `--store <path>`;
2. `AI_USE_REFLECTION_HOME` when set;
3. the host's standard per-user data directory;
4. only when explicitly requested, a project-local `.ai-use-reflection/` directory.

Run `scripts/resolve_storage.py` before the first write and report its `path`, `scope`, and `source` to the user. The resolver uses macOS Application Support, Linux XDG data, or Windows APPDATA conventions without hardcoding a machine-specific absolute path.

The resolved store contains:

```text
<reflection-root>/
├── wiki/
│   ├── index.md
│   ├── sessions/<session-id>.md
│   ├── capabilities/<capability-slug>.md
│   ├── interventions/<dimension-slug>.md
│   ├── contributions/<category-slug>.md
│   ├── knowledge/<domain>/<topic-slug>.md
│   └── trends/<period>.md
├── data/
│   ├── session-index.jsonl
│   ├── current-review.json
│   └── link-index.json
└── reflection-dashboard.html
```

Use `scripts/bootstrap_store.py` to create the resolved store without overwriting existing content. Use `scripts/register_session.py` to append a compact session record and determine whether a review suggestion is due. Use `scripts/mark_reviewed.py` after a confirmed review to close the reviewed batch. Use `scripts/build_dashboard.py` after a confirmed review or Wiki update.

Examples:

```bash
# Shared cross-session store; this is the default.
python3 scripts/resolve_storage.py
python3 scripts/bootstrap_store.py

# Explicit project-local store, only when the user chooses project scope.
python3 scripts/bootstrap_store.py --scope project --project-root .

# Share one store across different AI IDEs on the same machine.
AI_USE_REFLECTION_HOME="/path/selected/by/user" python3 scripts/bootstrap_store.py
```

Read only the current session, the relevant Wiki pages, and recent linked sessions. Use `data/link-index.json` or the Wiki index to avoid loading the entire knowledge base into context. After every durable write, return the resolved storage path and links to the affected files.

## Workflow

### 1. Register the session quietly

At the end of an eligible session, record only metadata: stable session ID, title, topics, completion state, review state, and a short focus summary. Treat very short or purely administrative turns as ineligible unless the user asks for a review.

Run with the resolved store options:

```bash
python3 scripts/register_session.py --session-id 2026-08-15-001 --title "Skill design" --topics "skill design,reflection" --summary "Defined cross-session Wiki and HTML dashboard requirements."
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

Add three required analysis blocks to every substantive review:

- **Intervention efficacy**: strongest and weakest interventions, vector assessment, observable cost, and confidence;
- **Human task contribution**: which decisions or judgments materially enabled the outcome, with evidence;
- **AI-use guidance**: one to three concrete changes for the next similar task, prioritized by expected leverage.

Show the intervention ledger before proposing durable updates. Rank guidance
by expected leverage and reversibility, and phrase each item as a testable
behavior for the next session. If there is no reliable signal of improvement,
say so instead of manufacturing a score.

Analyze these capability dimensions when relevant: goal framing, context provision, constraints, decomposition, delegation, prompt iteration, verification, correction, tool selection, and judgment boundaries.

For domain knowledge, record only observable changes: concepts encountered, explanations the user refined, decisions made, artifacts produced, verified facts, and open questions. Do not label a topic as mastered from one conversation. Keep knowledge growth separate from intervention efficacy and task contribution.

### 4. Update the Wiki after confirmation

Create or update the session page first. Then apply only user-confirmed deltas to capability, intervention, contribution, and knowledge pages. Prefer an evidence log over a single score:

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
- intervention efficacy vector, confidence, and guidance;
- human task contribution categories and evidence;
- current capability states and evidence counts;
- knowledge topics and open questions;
- a recent session timeline;
- trend pages and links to source Wiki pages;
- maintainer attribution to Jin Hefeng and the GitHub project link.

Keep the HTML self-contained: inline CSS, inline small summary data, and no network dependency. Do not embed the full Wiki or transcript. Use relative links from the dashboard to the Markdown pages so the dashboard remains small.

After a successful review, return clickable links to the current review, the dashboard, and the most relevant Wiki pages.

## Privacy and correction loop

Treat the Wiki as user-controlled memory. Before durable writes, state what will be added or changed. Support explicit corrections such as “删掉这条”“这不是能力提升”“把它归到另一个主题”. Preserve rejected proposals only in a pending queue when the user wants an audit trail; otherwise do not retain them.

If the shared store is missing, initialize it with the bootstrap script. If the user asks for project-local storage, confirm the project root before writing. Never silently fall back from the shared store to an arbitrary workspace directory.

## Validation

Before handing off a skill change:

1. Run `scripts/quick_validate.py` from the skill-creator package when its dependencies are available.
2. Run the local scripts against a temporary fixture store.
3. Open or inspect the generated HTML and verify that it contains current review, capability, knowledge, trend, source links, attribution, and no external asset dependency.
4. Check that existing Wiki pages and unrelated files were not overwritten.

## Maintainer

Jin Hefeng — [https://github.com/jinhefeng/ai-use-reflection](https://github.com/jinhefeng/ai-use-reflection)
