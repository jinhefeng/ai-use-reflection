# Task Constitution

## 1. Mission

Build and publish `ai-use-reflection`, a portable skill that evaluates the efficiency of human interventions in AI work, identifies the user's evidence-backed contribution to concrete task outcomes, turns the findings into next-use guidance, and stores cross-session capability and knowledge growth in a Wiki presented through one generated HTML dashboard.

## 2. Success Criteria

- [x] Skill metadata and instructions are valid and clearly trigger on session reflection, Wiki updates, and dashboard generation.
- [x] A non-destructive Wiki store can be initialized and compact session metadata can be registered.
- [x] A self-contained `reflection-dashboard.html` renders current review, capability, knowledge, trend, source links, and Jin Hefeng attribution.
- [x] Scripts pass fixture-based checks and structural validation has been completed with the PyYAML dependency limitation recorded.
- [x] A public GitHub repository is created and the project is published at `https://github.com/jinhefeng/ai-use-reflection`.
- [x] Runtime storage resolves to a portable shared user directory by default, supports explicit project scope, and reports the actual path after writes.
- [x] Reviews assess intervention efficacy as an evidence-backed vector, preserve a compact intervention ledger, and produce prioritized next-use guidance.
- [x] Reviews assess human contribution to the concrete task without turning it into a general personal worth or performance score.
- [x] Reviews provide one to three evidence-matched examples that rewrite weak interventions into better prompts and define a next-session test.
- [x] In-session triggers detect repeated refinement or stalled progress and suppress duplicate prompts with a cooldown.
- [x] The public project includes a bilingual README that explains the design philosophy, human value, usage boundary, and MIT License.
- [x] The public README references a reusable project icon stored inside the repository.

## 3. Task Tree

### T1 — Define and implement the skill package
- Status: 已完成
- Objective: Create the reusable skill, intervention-efficacy model, task-contribution model, prompt-improvement examples, Wiki schema, portable storage resolver, deterministic helpers, and attribution.
- Acceptance: Skill folder contains valid `SKILL.md`, `agents/openai.yaml`, references, resolver, and tested scripts.

### T2 — Implement the reflection data and presentation loop
- Status: 已完成
- Objective: Support quiet session registration, review thresholds, portable global storage, explicit project scope, intervention/contribution evidence, prompt rewrites for weak interventions, Wiki-oriented storage, and HTML dashboard output.
- Acceptance: Fixture run resolves both global and project roots, creates the selected store, registers sessions, detects threshold, and generates a readable dashboard.

### T3 — Validate and forward-test
- Status: 已完成
- Objective: Run structural validation and realistic fixture tests for storage, intervention/contribution data, and prompt-improvement examples; record limitations and debt.
- Acceptance: Resolver, fixture, syntax, and manual structural checks pass; the bundled validator remains unavailable because the active Python lacks `PyYAML`; no unrelated workspace files are changed.

### T4 — Create and publish the GitHub project
- Status: 已完成
- Objective: Initialize Git, create the remote repository, commit the skill, and push the project.
- Acceptance: Remote repository exists under the user-confirmed visibility and contains the validated skill.
- Visibility: public, confirmed by the user.
- GitHub repository: public `https://github.com/jinhefeng/ai-use-reflection`, default branch `main`.

### T5 — Optimize passive in-session review triggers
- Status: 已完成
- Objective: Detect repeated prompt refinement, repeated goal misses, stalled multi-turn work, and verification loops from compact visible-session metrics.
- Acceptance: A host-callable trigger evaluator returns reasons and a low-friction prompt, suppresses duplicate reasons with cooldown state, and does not trigger on a completed goal.

### T6 — Document the project and license it for reuse
- Status: 已完成
- Objective: Publish a Chinese/English switchable README, a reusable project icon, and an MIT License that explain the design philosophy, human task value, limits, usage, and identity of the project.
- Acceptance: README is readable on GitHub, references the repository icon, links to the core files, contains no personal email, and LICENSE is a valid MIT License.

## 4. Current Focus

- Task: Handoff
- Objective: Keep the bilingual documentation, project icon, MIT License, installed copy, and public repository synchronized.
- Next action: Commit and publish the README/icon/license update.

## 5. Decision Log

| Date | Decision | Rationale | Impact |
|---|---|---|---|
| 2026-08-15 | Use `ai-use-reflection` as the skill name | Short, action-oriented, and directly describes the behavior | Folder and trigger metadata use this name |
| 2026-08-15 | Use many Markdown Wiki pages, not one long file | Keeps retrieval selective and token-efficient | Wiki is the canonical data layer |
| 2026-08-15 | Use one generated HTML file as the dashboard | Gives the user a single visual entry point without duplicating the Wiki | `reflection-dashboard.html` is generated output |
| 2026-08-15 | Attribute the project to Jin Hefeng and link only to the project repository | User clarified that the repository address, not the account homepage, should be used | Skill, references, and dashboard include `https://github.com/jinhefeng/ai-use-reflection` |
| 2026-08-15 | Use runtime-resolved shared user storage by default | User identified that absolute paths and project-root defaults do not support cross-IDE archives | T1, T2 |
| 2026-08-17 | Combine session-count fallback with in-session friction triggers | A user can need help before three sessions accumulate, especially when a prompt is repeatedly revised or progress stalls | T5 |
| 2026-08-17 | Use a bilingual README and MIT License as the public entry point | The project needs to communicate its design philosophy and human value, not only expose implementation files | T6 |

## 6. Knowledge Context

- Project workspace: repository root containing this skill.
- Local Git identity: Jin Hefeng.
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
| 2026-08-15 | Verified global, environment-selected, project, and explicit storage modes | Fixture tests confirmed path precedence and write reporting | T1, T2, T3 |
| 2026-08-15 | Made intervention efficacy, task contribution, and next-use guidance the primary review model | User clarified the most important value of the skill | T1, T2 |
| 2026-08-15 | Added an intervention ledger and causal-evidence boundary | Efficiency must explain how a human move changed the trajectory, not just assign a label | T1, T2, T3 |
| 2026-08-15 | Added typical weak-intervention cases with improved prompt wording and next-session tests | An efficacy label must lead to an actionable change in AI use | T1, T2, T3 |
| 2026-08-17 | Added in-session friction triggers and cooldown state | One day of use showed that the session-count fallback never detected live stalls or repeated prompt revisions | T5 |
| 2026-08-17 | Added bilingual project documentation and MIT License | Make the public project understandable and reusable | T6 |
| 2026-08-17 | Added a project icon representing human judgment, AI execution, and reflection | Give the open-source project a visual identity aligned with its design philosophy | T6 |

## 8. Detail Pointers

- Public documentation: README.md.
- Project icon: assets/ai-use-reflection-icon.png.
- License: LICENSE.
- Format: v1 single-file constitution until the project grows beyond the hot-file threshold.
- Skill instructions: `SKILL.md`.
- Wiki schema: `references/wiki-schema.md`.
- Reflection rubric: `references/reflection-rubric.md`.
- Local commit: updated after the core review-model optimization.
- Validation: Python syntax, fixture threshold flow, HTML content inspection, and Ruby YAML parse passed; skill-creator quick validation is blocked because the active Python lacks `PyYAML`.
- Current optimization: complete; the bilingual README, project icon, and MIT License are validated.

## 9. Current Round

- Round: R4
- Frontier: Handoff
- Granularity target: objective + output + acceptance + dependency
- Exit condition: bilingual README, project icon, MIT License, installed copy, and public repository are synchronized.

## 10. Technical Debt Queue

| ID | Discovered in | Debt | Why deferred | Trigger / target round | Priority | Status |
|---|---|---|---|---|---|---|
| D-001 | T2 | Add a real Codex session-end hook for proactive prompts | The skill cannot receive background events by itself | After local MVP validation | P1 | queued |
| D-002 | T4 | Restore or replace the invalid local `gh` token | Resolved through GitHub CLI device login | Before future automated releases | P1 | resolved |
