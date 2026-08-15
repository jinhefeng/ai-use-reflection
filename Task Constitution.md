# Task Constitution

## 1. Mission

Build and publish `ai-use-reflection`, a Codex skill that turns visible human–AI sessions into evidence-linked cross-session capability and knowledge growth, stored as a Wiki and presented through one generated HTML dashboard.

## 2. Success Criteria

- [x] Skill metadata and instructions are valid and clearly trigger on session reflection, Wiki updates, and dashboard generation.
- [x] A non-destructive Wiki store can be initialized and compact session metadata can be registered.
- [x] A self-contained `reflection-dashboard.html` renders current review, capability, knowledge, trend, source links, and Jin Hefeng attribution.
- [x] Scripts pass fixture-based checks and structural validation has been completed with the PyYAML dependency limitation recorded.
- [x] A public GitHub repository is created and the project is published at `https://github.com/jinhefeng/ai-use-reflection`.
- [ ] Runtime storage resolves to a portable shared user directory by default, supports explicit project scope, and reports the actual path after writes.

## 3. Task Tree

### T1 — Define and implement the skill package
- Status: 进行中
- Objective: Create the reusable skill, Wiki schema, portable storage resolver, deterministic helpers, and attribution.
- Acceptance: Skill folder contains valid `SKILL.md`, `agents/openai.yaml`, references, resolver, and tested scripts.

### T2 — Implement the reflection data and presentation loop
- Status: 进行中
- Objective: Support quiet session registration, review thresholds, portable global storage, explicit project scope, Wiki-oriented storage, and HTML dashboard output.
- Acceptance: Fixture run resolves both global and project roots, creates the selected store, registers sessions, detects threshold, and generates a readable dashboard.

### T3 — Validate and forward-test
- Status: 未开始
- Objective: Run structural validation and realistic fixture tests; record limitations and debt.
- Acceptance: Resolver, fixture, syntax, and structural checks pass; no unrelated workspace files are changed.

### T4 — Create and publish the GitHub project
- Status: 已完成
- Objective: Initialize Git, create the remote repository, commit the skill, and push the project.
- Acceptance: Remote repository exists under the user-confirmed visibility and contains the validated skill.
- Visibility: public, confirmed by the user.
- GitHub repository: public `https://github.com/jinhefeng/ai-use-reflection`, default branch `main`.

## 4. Current Focus

- Task: T1 → T2
- Objective: Replace the project-root storage default with portable shared user storage and explicit project scope.
- Next action: Test resolver precedence and update the installed skill and public repository.

## 5. Decision Log

| Date | Decision | Rationale | Impact |
|---|---|---|---|
| 2026-08-15 | Use `ai-use-reflection` as the skill name | Short, action-oriented, and directly describes the behavior | Folder and trigger metadata use this name |
| 2026-08-15 | Use many Markdown Wiki pages, not one long file | Keeps retrieval selective and token-efficient | Wiki is the canonical data layer |
| 2026-08-15 | Use one generated HTML file as the dashboard | Gives the user a single visual entry point without duplicating the Wiki | `reflection-dashboard.html` is generated output |
| 2026-08-15 | Attribute the project to Jin Hefeng and link only to the project repository | User clarified that the repository address, not the account homepage, should be used | Skill, references, and dashboard include `https://github.com/jinhefeng/ai-use-reflection` |
| 2026-08-15 | Use runtime-resolved shared user storage by default | User identified that absolute paths and project-root defaults do not support cross-IDE archives | T1, T2 |

## 6. Knowledge Context

- Project workspace: repository root containing this skill.
- Local Git identity: `Jin Hefeng <[personal-email-removed]>`.
- GitHub connector profile nickname: `jinhefeng`.
- GitHub repository: public `https://github.com/jinhefeng/ai-use-reflection`, default branch `main`.
- Proactive prompts require an application/automation/session hook; the skill provides registration and decision logic but does not run in the background.

## 7. Change History

| Date | Change | Reason | Affected tasks |
|---|---|---|---|
| 2026-08-15 | Added cross-session capability and knowledge Wiki to MVP | User requested long-term analysis in the first version | T1, T2 |
| 2026-08-15 | Corrected presentation target from HTM to HTML | User correction | T1, T2 |
| 2026-08-15 | Initialized local Git repository and committed the skill | User requested a GitHub project | T4 |
| 2026-08-15 | Created public GitHub repository and pushed `main` | User confirmed public visibility and completed CLI device login | T4 |
| 2026-08-15 | Changed runtime storage from implicit project root to portable shared user storage | User identified that absolute paths and project-root defaults do not support cross-IDE archives | T1, T2 |

## 8. Detail Pointers

- Format: v1 single-file constitution until the project grows beyond the hot-file threshold.
- Skill instructions: `SKILL.md`.
- Wiki schema: `references/wiki-schema.md`.
- Reflection rubric: `references/reflection-rubric.md`.
- Local commit: `0255bac feat: create AI use reflection skill`.
- Validation: Python syntax, fixture threshold flow, HTML content inspection, and Ruby YAML parse passed; skill-creator quick validation is blocked because the active Python lacks `PyYAML`.
- Current optimization: add `scripts/storage.py` and `scripts/resolve_storage.py`; default to platform user data, with `AI_USE_REFLECTION_HOME` and explicit project scope.

## 9. Current Round

- Round: R2
- Frontier: T1, T2, T3
- Granularity target: objective + output + acceptance + dependency
- Exit condition: portable resolver, updated skill package, and validation evidence are complete.

## 10. Technical Debt Queue

| ID | Discovered in | Debt | Why deferred | Trigger / target round | Priority | Status |
|---|---|---|---|---|---|---|
| D-001 | T2 | Add a real Codex session-end hook for proactive prompts | The skill cannot receive background events by itself | After local MVP validation | P1 | queued |
| D-002 | T4 | Restore or replace the invalid local `gh` token | Resolved through GitHub CLI device login | Before future automated releases | P1 | resolved |
