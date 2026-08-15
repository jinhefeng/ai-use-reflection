# Intervention Efficacy and Task Contribution Rubric

Use this rubric for the primary review, while keeping evidence, interpretation, and guidance separate.

## Intervention event types

Tag each meaningful user intervention with one or more types:

- `direction`: goal, priority, scope, or stopping decision;
- `context`: domain facts, examples, files, or audience;
- `constraint`: limits, safety, format, time, or acceptance criteria;
- `decomposition`: phases, dependencies, roles, or delegation;
- `correction`: a detected error, mismatch, or assumption repair;
- `verification`: test, source check, comparison, visual QA, or evidence request;
- `approval`: confirmation that authorizes the next action or durable write.

Do not count every user message as an intervention. Count it when it changes the AI's available decision space or the reliability of the result.

## Intervention ledger

Create a compact ledger before writing the summary. Keep the wording short and
link each row to a visible turn or artifact:

```yaml
- event_id: I-01
  turn_ref: "user correction after draft"
  type: [correction, constraint]
  signal: "The output used an absolute local path."
  mechanism: "Replaced the storage contract with runtime resolution."
  outcome: "The skill became usable across AI IDEs."
  observable_cost: "One correction turn; avoided a later portability rewrite."
  efficacy:
    leverage: high
    precision: high
    timing: medium
    economy: high
    coverage: high
    verification: medium
  confidence: high
  evidence: ["current session: storage discussion"]
```

If the outcome is not visible, leave it as `uncertain` and state what evidence
would resolve it. A strong intervention usually has a clear signal, a direct
mechanism, a visible outcome, and low avoidable cost. A weak intervention may
be correct but late, broad, repetitive, or unverified.

## Efficacy dimensions

| Dimension | Evidence to inspect | Guidance when weak |
|---|---|---|
| Leverage | The intervention changes direction, scope, risk, or rework | Move high-leverage clarification earlier |
| Precision | It addresses the root issue and produces a specific change | State the failure and desired correction together |
| Timing | It arrives before avoidable work or late rework | Add goal, constraints, and acceptance criteria up front |
| Economy | It reduces repeated explanations, turns, or revisions | Bundle related constraints and ask for a plan first |
| Coverage | It protects goal, constraints, acceptance, and risk | Use a short completion checklist |
| Verification | It creates evidence that the result is trustworthy | Ask for tests, sources, or a concrete comparison |

Use `high`, `medium`, `low`, or `uncertain` for each dimension and attach confidence. Do not calculate a global number unless the user explicitly requests one and the evidence supports the scale.

## Task contribution categories

Assess contribution to the concrete outcome, not the person as a whole:

- `decisive`: the user's judgment materially determined direction, trade-off, or acceptance;
- `enabling`: the user's context or constraints made a reliable result possible;
- `supporting`: the user's intervention improved clarity or polish without changing the core direction;
- `necessary`: the user's approval, verification, or accountability was required for safe completion;
- `uncertain`: the evidence does not establish causal contribution.

Every contribution claim needs a session evidence link and a confidence level. Avoid saying that AI “did everything” when the user supplied the objective, constraints, judgment, and final acceptance.

## Guidance format

Return guidance as an experiment, not a moral judgment:

```yaml
priority: high
behavior: "在开始执行前先给出目标、约束和完成判据。"
expected_gain: "减少后期返工，并提高 AI 第一次方案的命中率。"
test_in_next_session: true
```

Prefer one to three high-leverage experiments. Measure the next session against the same dimensions and report whether the intervention actually improved.

## Selecting guidance

Choose guidance in this order:

1. Fix a low-timing or low-coverage intervention that caused avoidable rework.
2. Preserve a high-leverage behavior that clearly improved the result.
3. Add one verification experiment when outcome reliability is uncertain.

Do not recommend "be more detailed" without naming the missing decision,
constraint, acceptance criterion, or evidence request.
