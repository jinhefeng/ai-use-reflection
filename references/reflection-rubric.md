# Reflection Rubric

Use this rubric to analyze a session consistently without turning it into a personality assessment.

## Human contribution dimensions

Review only dimensions that have visible evidence:

| Dimension | Look for | Avoid claiming |
|---|---|---|
| Goal framing | desired outcome, scope, priority | motivation or ambition |
| Context provision | relevant files, background, examples | total domain knowledge |
| Constraint setting | limits, audience, safety, format | risk tolerance as a trait |
| Decomposition | phases, dependencies, acceptance criteria | general intelligence |
| Delegation | what was assigned to AI and why | dependence on AI |
| Iteration | corrections, refinements, feedback | personality type |
| Verification | tests, source checks, visual QA | universal rigor |
| Judgment | trade-offs, approvals, stopping decisions | leadership or performance rating |

## Domain knowledge dimensions

Track these separately:

- concepts encountered;
- distinctions the user made or corrected;
- decisions grounded in evidence;
- artifacts the user can inspect or reuse;
- unresolved questions;
- claims that still need verification.

Use `emerging`, `stable`, `improving`, `needs-verification`, or `stale` instead of a numeric mastery score by default.

## Review output

The smallest useful review contains:

1. three to five current-session key points;
2. two or three human contributions tied to evidence;
3. one strength and one friction point;
4. zero to three proposed long-term updates;
5. one or two next-session experiments.

If the session has no durable signal, say so and update only the compact session index.

## Confirmation language

Present proposed updates as editable claims:

> 建议新增：你在“结果验证”上的状态为 `improving`。证据：本次主动要求验证实现结果。是否写入长期档案？

Accept corrections without argument. A user's correction takes precedence over the model's interpretation.
