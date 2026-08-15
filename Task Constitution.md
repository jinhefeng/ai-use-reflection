# Task Constitution

## 1. Mission

Build and publish `ai-use-reflection`, a Codex skill that turns visible human–AI sessions into evidence-linked cross-session capability and knowledge growth, stored as a Wiki and presented through one generated HTML dashboard.

## 2. Success Criteria

- [ ] Skill metadata and instructions are valid and clearly trigger on session reflection, Wiki updates, and dashboard generation.
- [ ] A non-destructive Wiki store can be initialized and compact session metadata can be registered.
- [ ] A self-contained `reflection-dashboard.html` renders current review, capability, knowledge, trend, source links, and Jin Hefeng attribution.
- [ ] Scripts pass fixture-based checks and the skill passes structural validation.
- [ ] A GitHub repository is created and the project is published at `https://github.com/jinhefeng/ai-use-reflection`.

## 3. Task Tree

### T1 — Define and implement the skill package
- Status: 已完成
- Objective: Create the reusable skill, Wiki schema, deterministic helpers, and attribution.
- Acceptance: Skill folder contains valid `SKILL.md`, `agents/openai.yaml`, references, and tested scripts.

### T2 — Implement the reflection data and presentation loop
- Status: 已完成
- Objective: Support quiet session registration, review thresholds, Wiki-oriented storage, and HTML dashboard output.
- Acceptance: Fixture run creates the store, registers sessions, detects threshold, and generates a readable dashboard.

### T3 — Validate and forward-test
- Status: 进行中
- Objective: Run structural validation and realistic fixture tests; record limitations and debt.
- Acceptance: Fixture and syntax checks pass; structural validation is either passed or its dependency blocker is recorded; no unrelated workspace files are changed.

### T4 — Create and publish the GitHub project
- Status: 进行中
- Objective: Initialize Git, create the remote repository, commit the skill, and push the project.
- Acceptance: Remote repository exists under the user-confirmed visibility and contains the validated skill.
- Visibility: public, confirmed by the user.
- Remaining dependency: local `gh` authentication is invalid; use the connected browser session for repository creation if needed.

## 4. Current Focus

- Task: T1 → T2
- Objective: Finish the local skill and deterministic artifact pipeline before external publication.
- Next action: Create the public repository and push `main`.

## 5. Decision Log

| Date | Decision | Rationale | Impact |
|---|---|---|---|
| 2026-08-15 | Use `ai-use-reflection` as the skill name | Short, action-oriented, and directly describes the behavior | Folder and trigger metadata use this name |
| 2026-08-15 | Use many Markdown Wiki pages, not one long file | Keeps retrieval selective and token-efficient | Wiki is the canonical data layer |
| 2026-08-15 | Use one generated HTML file as the dashboard | Gives the user a single visual entry point without duplicating the Wiki | `reflection-dashboard.html` is generated output |
| 2026-08-15 | Attribute the project to Jin Hefeng and link only to the project repository | User clarified that the repository address, not the account homepage, should be used | Skill, references, and dashboard include `https://github.com/jinhefeng/ai-use-reflection` |

## 6. Knowledge Context

- Workspace root: `/Users/jinhefeng/Dev/skills`.
- Project root: `/Users/jinhefeng/Dev/skills/ai-use-reflection`.
- Local Git identity: `Jin Hefeng <[personal-email-removed]>`.
- GitHub connector profile nickname: `jinhefeng`.
- `gh` is installed but its local token is invalid; external repository creation may require browser login or re-authentication.
- Proactive prompts require an application/automation/session hook; the skill provides registration and decision logic but does not run in the background.

## 7. Change History

| Date | Change | Reason | Affected tasks |
|---|---|---|---|
| 2026-08-15 | Added cross-session capability and knowledge Wiki to MVP | User requested long-term analysis in the first version | T1, T2 |
| 2026-08-15 | Corrected presentation target from HTM to HTML | User correction | T1, T2 |
| 2026-08-15 | Initialized local Git repository and committed the skill | User requested a GitHub project | T4 |

## 8. Detail Pointers

- Format: v1 single-file constitution until the project grows beyond the hot-file threshold.
- Skill instructions: `SKILL.md`.
- Wiki schema: `references/wiki-schema.md`.
- Reflection rubric: `references/reflection-rubric.md`.
- Local commit: `0255bac feat: create AI use reflection skill`.
- Validation: Python syntax, fixture threshold flow, HTML content inspection, and Ruby YAML parse passed; skill-creator quick validation is blocked because the active Python lacks `PyYAML`.

## 9. Current Round

- Round: R1
- Frontier: T1, T2, T3, T4
- Granularity target: objective + output + acceptance + dependency
- Exit condition: each frontier task has a first result or explicit blocker.

## 10. Technical Debt Queue

| ID | Discovered in | Debt | Why deferred | Trigger / target round | Priority | Status |
|---|---|---|---|---|---|---|
| D-001 | T2 | Add a real Codex session-end hook for proactive prompts | The skill cannot receive background events by itself | After local MVP validation | P1 | queued |
| D-002 | T4 | Restore or replace the invalid local `gh` token | Local CLI publishing is currently unavailable | Before future automated releases | P1 | queued |
