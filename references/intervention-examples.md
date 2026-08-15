# Typical Ineffective Interventions and Prompt Improvements

Use these examples when a visible session contains a weak or uncertain
intervention. Match the example to the actual failure; do not force a case or
claim that the rewritten prompt would have worked without evidence.

## 1. Vague goal with no acceptance criteria

**Ineffective intervention**

> 帮我把这个做得更好。

**Why it underperforms**

The AI must guess the audience, priority, scope, and definition of done. The
first answer may look plausible while missing the user's real objective.

**Improved prompt**

> 目标：为内部团队做一个可执行的方案。
>
> 优先级：先保证信息结构和关键决策，再优化表达。
>
> 约束：保留现有数据，不引入外部依赖。
>
> 输出：先给出方案和风险，再实施。
>
> 完成标准：我能据此判断范围、验收结果，并知道下一步行动。

**Expected improvement**: precision, timing, and coverage.

**Next-session test**: compare first-draft rework and the number of missing
acceptance criteria after the first response.

## 2. Constraint introduced after expensive work

**Ineffective intervention**

> 这部分不能改。
>
> （在 AI 已经重构完成后才补充。）

**Why it underperforms**

The constraint is valid but arrives after the AI has committed to a solution,
so the correction creates avoidable rework.

**Improved prompt**

> 开始前先确认边界：保持现有 API 和目录结构不变；只能修改实现层；
> 如果方案需要突破这两个边界，先停下来说明原因，不要直接执行。

**Expected improvement**: timing, economy, and risk coverage.

**Next-session test**: record whether the AI asks before crossing a protected
boundary and whether a second implementation pass is needed.

## 3. Correction without naming the root mismatch

**Ineffective intervention**

> 这个不对，重来。

**Why it underperforms**

The AI receives a rejection but not the failed assumption, the desired change,
or the part that should remain unchanged. It may repeat the same error in a
different form.

**Improved prompt**

> 问题不是格式，而是你把“项目级存储”当成了默认存储。默认应使用跨工具的
> 用户级目录，项目级目录只能在显式选择后启用。请保留现有 Wiki 结构，
> 只改存储解析规则，并列出你修改的文件和验证方式。

**Expected improvement**: precision, leverage, and verification.

**Next-session test**: check whether the next revision addresses the root
assumption in one pass and names a verification step.

## 4. Verification request without a test surface

**Ineffective intervention**

> 帮我检查一下有没有问题。

**Why it underperforms**

The scope of “问题” is undefined. The AI may perform a superficial review and
miss the risk that matters to the user.

**Improved prompt**

> 请按以下顺序验证：1）脚本能否运行；2）默认路径是否跨平台且不写死；
> 3）旧 Wiki 是否不会被覆盖；4）HTML 是否包含当前复盘和来源链接。
> 对每项给出证据、未验证项和阻塞原因，不要只给总体结论。

**Expected improvement**: coverage and verification.

**Next-session test**: compare the checklist coverage and the number of
undetected issues after the review.

## Required rewrite format

When showing a case in a review, use this compact structure:

```yaml
scenario: "约束出现过晚"
original_prompt: "这部分不能改。"
diagnosis: "约束有效但没有在执行前进入 AI 的决策空间。"
improved_prompt: "开始前先确认：保持 API 和目录结构不变；突破前先停下说明。"
expected_gain: "减少返工并提高风险覆盖。"
test_in_next_session: "记录是否发生越界和二次实现。"
```

Show one to three matched examples, prioritize the lowest-timing or
lowest-precision intervention, and preserve uncertainty when the session does
not reveal whether the improved wording would have changed the result.
