# In-Session Review Trigger Rubric

The passive trigger has two layers:

1. **Session-level fallback**: suggest a review after the configured number of
   eligible, unreviewed sessions.
2. **In-session friction**: suggest a review when the visible conversation shows
   repeated refinement, repeated goal misses, a stalled multi-turn loop, or
   repeated verification failure.

The in-session layer must be called by the host's session wrapper or another
visible-session integration. The skill cannot observe background events by
itself. The wrapper should derive only the following compact metrics from the
visible session:

| Metric | Meaning |
|---|---|
| revision_count | Material revisions to the same goal or prompt |
| same_topic_revisions | Revisions that keep returning to the same unresolved topic |
| correction_count | User corrections that reject or repair an AI result |
| goal_miss_count | Outputs visibly failing the current goal |
| last_progress_turns | User turns since accepted or verified progress |
| verification_failures | Failed tests, checks, or comparisons |
| goal_status | unknown, in_progress, stalled, blocked, or done |

## Default trigger conditions

- revision_count >= 2 or same_topic_revisions >= 2 → repeated refinement;
- correction_count >= 3 → repeated correction;
- user_turns >= 6 and last_progress_turns >= 3 while not done →
  multi-round stall;
- goal_status is stalled or blocked with at least two turns without
  progress, or one visible goal miss → multi-round stall;
- goal_miss_count >= 2 while not done → repeated goal miss;
- verification_failures >= 2 → verification loop.

Do not trigger on a single normal clarification, a successful refinement, or
message volume alone. A trigger is a review suggestion, not a failure
judgment.

## Prompt behavior

Use a short, non-blocking prompt:

> 我注意到：同一目标正在反复调整，或者经过多轮仍没有可确认进展。现在先做一次 1 分钟复盘，确认目标、卡点和下一条提示词吗？可回复“先复盘”“继续”或“稍后”。

If the user chooses “继续”, keep working and do not repeat the same reason
within the cooldown. If the user chooses “稍后”, allow a later trigger only
when a new reason appears or the session crosses the cooldown. If the user
chooses “先复盘”, analyze the visible session immediately; do not wait for the
cross-session threshold.

The default cooldown is four user turns when a turn number is available, or
twenty minutes when it is not. The state is operational metadata in
data/trigger-state.json, not long-term personal knowledge.

## Integration example

~~~bash
python3 scripts/evaluate_trigger.py \
  --session-id 2026-08-17-001 \
  --turn 8 \
  --user-turns 8 \
  --revision-count 2 \
  --goal-miss-count 1 \
  --last-progress-turns 3 \
  --goal-status in_progress
~~~

The command returns review_due, reason codes, evidence, a short prompt, and
the resolved state path. It does not claim to infer hidden chat history.
