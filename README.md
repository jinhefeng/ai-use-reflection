<a id="chinese"></a>

# AI 使用复盘

[中文](#chinese) · [English](#english)

> 让人和 AI 的协作，能够被看见、被反思、被验证，并持续变得更好。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 这是什么

<code>ai-use-reflection</code> 是一个用于 AI IDE 和其他 AI 工具的可移植 Skill。
它不只记录“AI 做了什么”，更关注两个问题：

1. 用户的哪一次干预真正改变了 AI 的方向和任务结果？
2. 用户下一次应该怎样提问、约束、纠错和验证，才能更高效地完成类似任务？

它把一次会话转化为一个学习闭环：

<p align="center">
  <strong>会话证据 → 干预效能 → 人类任务贡献 → 使用指导 → 下一轮验证</strong>
</p>

## 设计哲学

### 1. 人的价值不等于打字量

在 AI 协作中，人的价值不应由提示词长度、消息数量或亲自执行了多少机械步骤来衡量。
更重要的是，用户是否：

- 定义了真正要解决的问题；
- 做出了优先级和范围判断；
- 提供了 AI 无法自行知道的背景和约束；
- 识别了错误假设并推动纠正；
- 建立了验收标准并对最终结果负责。

AI 可以完成大量执行工作，但方向、边界、取舍和最终判断仍然可能来自人。

### 2. 评价具体任务贡献，而不是评价整个人

本项目评估的是用户对某一个具体任务结果的贡献，不是人的总体价值、智力、性格、心理状态或职业表现。

贡献使用证据关联的标签表达：

- <code>decisive</code>：用户的判断决定了方向、取舍或验收边界；
- <code>enabling</code>：用户提供的背景或约束使可靠执行成为可能；
- <code>supporting</code>：用户改善了清晰度、质量或表达；
- <code>necessary</code>：用户的批准、验证或责任承担是安全完成所必需的；
- <code>uncertain</code>：现有证据不足以确认因果贡献。

### 3. 评价干预的效能，而不是给人打一个总分

一次干预是否有效，要看它如何改变了 AI 的决策空间和任务结果。Skill 会追踪：

<table>
  <tr><th>维度</th><th>要问的问题</th></tr>
  <tr><td>杠杆</td><td>是否改变了方向、范围、风险或返工？</td></tr>
  <tr><td>精准度</td><td>是否解决了根因，而不是只修补表面症状？</td></tr>
  <tr><td>时机</td><td>是否在昂贵工作发生前进入了决策空间？</td></tr>
  <tr><td>经济性</td><td>是否减少了重复解释、往返和返工？</td></tr>
  <tr><td>覆盖度</td><td>是否覆盖目标、约束、验收标准和风险？</td></tr>
  <tr><td>验证度</td><td>是否提供了足够证据来信任结果？</td></tr>
</table>

默认使用 <code>high</code>、<code>medium</code>、<code>low</code>、<code>uncertain</code> 和置信度，
不制造缺乏证据的“人机协作总分”。

### 4. 复盘必须能转化为下一次行动

当某次干预效果不佳时，复盘不会只说“提示词不够好”，而会给出：

<p align="center">
  <strong>原提示词 → 失效原因 → 改进提示词 → 下一轮验证方式</strong>
</p>

典型情况包括：目标模糊、约束出现过晚、只说“错了”却不指出根因、要求验证却没有检查清单。

## 核心能力

### 会话内复盘

Skill 分析当前可见会话，记录：

- 目标与最终结果；
- 用户改变结果的关键动作；
- AI 加速或限制工作的地方；
- 返工、摩擦和未解决的问题；
- 干预账本和下一轮实验。

它只分析当前可见内容和明确提供的文件，不声称读取隐藏或历史聊天记录。

### 会话内被动触发

除了原有的“多次未复盘会话”兜底机制，现在还支持会话内摩擦信号：

- 同一目标或提示词被实质性改写至少 2 次；
- 用户连续纠错至少 3 次；
- 至少 6 轮交互，且连续 3 轮没有确认进展；
- 目标连续未达成，或状态进入 stalled / blocked；
- 验证连续失败至少 2 次。

触发提示是非阻塞的，并有冷却机制，避免打断正常迭代。触发评估器位于
<code>scripts/evaluate_trigger.py</code>，可由 AI IDE 的会话包装器或宿主集成调用。

> 注意：Skill 本身不能在后台拦截每一轮对话。真正的被动触发需要宿主在可见会话检查点调用触发评估器。

### 跨会话 Wiki

长期档案采用多个小型 Markdown 页面，而不是一个越来越长的文件：

~~~text
<reflection-root>/
├── wiki/
│   ├── sessions/          # 会话复盘
│   ├── capabilities/      # AI 协作能力
│   ├── interventions/     # 干预效能模式
│   ├── contributions/     # 具体任务贡献
│   ├── knowledge/         # 领域知识
│   └── trends/            # 跨会话趋势
├── data/
│   ├── session-index.jsonl
│   ├── current-review.json
│   ├── link-index.json
│   └── trigger-state.json
└── reflection-dashboard.html
~~~

这种结构支持按需读取，减少长期知识库对 Token 的消耗，也允许不同 AI IDE 共享同一份个人档案。

### HTML 总览

<code>reflection-dashboard.html</code> 是展示层，不是事实来源。它将当前复盘、干预效能、任务贡献、
能力、知识、趋势和提示词改进案例放在一个自包含 HTML 文件中，Wiki Markdown 才是长期档案的来源。

## 快速开始

在 Skill 目录中运行：

~~~bash
# 解析当前主机的可移植存储路径
python3 scripts/resolve_storage.py

# 初始化 Wiki 和运行时数据
python3 scripts/bootstrap_store.py

# 分析一次会话内是否需要立即复盘
python3 scripts/evaluate_trigger.py \
  --session-id 2026-08-17-001 \
  --turn 8 \
  --user-turns 8 \
  --revision-count 2 \
  --last-progress-turns 3 \
  --goal-status in_progress

# 生成 HTML 总览
python3 scripts/build_dashboard.py
~~~

如果希望多个 AI IDE 共享同一份档案，可以在各个宿主中设置同一个
<code>AI_USE_REFLECTION_HOME</code>。也可以显式使用
<code>--store</code> 或选择项目级 <code>.ai-use-reflection/</code> 存储。

## 数据与隐私边界

- 默认使用主机的用户级数据目录，不把个人档案写入 Skill 安装目录或公开仓库；
- 支持显式选择项目级存储；
- 持久化能力、贡献和知识前，先展示建议变化并等待用户确认；
- 不复制完整聊天记录到 Wiki，只保留紧凑的证据链接和摘要；
- 不进行人格、心理、员工绩效或总体人类价值评估；
- 触发状态是运行元数据，不属于长期能力或知识档案；
- HTML 为自包含文件，不依赖外部网络资源来显示个人档案。

## 项目结构

- [SKILL.md](SKILL.md)：Skill 的工作规则和执行流程
- [references/intervention-rubric.md](references/intervention-rubric.md)：干预效能与任务贡献评价标准
- [references/intervention-examples.md](references/intervention-examples.md)：典型无效干预与提示词改写案例
- [references/trigger-rubric.md](references/trigger-rubric.md)：会话内触发条件与集成约定
- [scripts/evaluate_trigger.py](scripts/evaluate_trigger.py)：会话内触发评估器
- [scripts/build_dashboard.py](scripts/build_dashboard.py)：HTML 总览生成器

## License

本项目采用 MIT License，详见 [LICENSE](LICENSE)。

## Maintainer

Jin Hefeng  
Project repository: <https://github.com/jinhefeng/ai-use-reflection>

<a id="english"></a>

# AI Use Reflection

[中文](#chinese) · [English](#english)

> Make human–AI collaboration visible, reflectable, testable, and continuously improvable.

## What it is

<code>ai-use-reflection</code> is a portable Skill for AI IDEs and other AI tools.
It does not only record what the AI did. It asks two more useful questions:

1. Which human intervention actually changed the AI's direction and the task outcome?
2. What should the human change in the next similar session to work with AI more effectively?

It turns a session into a learning loop:

<p align="center">
  <strong>Session evidence → intervention efficacy → human task contribution → usage guidance → next-session test</strong>
</p>

## Design philosophy

### 1. Human value is not typing volume

Human value in AI collaboration should not be estimated from prompt length, message count,
or how many mechanical steps the person performed manually. The more important contributions are:

- defining the real problem;
- setting priorities and scope;
- supplying context and constraints the AI cannot know on its own;
- identifying false assumptions and driving corrections;
- defining acceptance criteria and owning the final judgment.

AI may perform most of the execution while the human still provides the direction, boundaries, trade-offs, and accountability.

### 2. Assess task contribution, not the whole person

This project evaluates a person's contribution to a concrete task outcome. It is not a rating of
overall worth, intelligence, personality, psychological state, or employment performance.

Contribution uses evidence-linked labels:

- <code>decisive</code>: the user's judgment determined direction, a trade-off, or acceptance;
- <code>enabling</code>: the user's context or constraints made reliable execution possible;
- <code>supporting</code>: the user's intervention improved clarity, quality, or polish;
- <code>necessary</code>: approval, verification, or accountability was required for safe completion;
- <code>uncertain</code>: the available evidence does not establish causal contribution.

### 3. Assess intervention efficacy instead of assigning one total score

An intervention is useful when it changes the AI's decision space and improves the task outcome.
The Skill evaluates leverage, precision, timing, economy, coverage, and verification.
It uses qualitative labels and confidence rather than inventing an unsupported collaboration score.

### 4. Reflection must become the next action

When an intervention performs poorly, the review does not stop at “the prompt was weak”.
It produces:

<p align="center">
  <strong>original prompt → diagnosis → improved prompt → next-session test</strong>
</p>

Typical cases include vague goals, late constraints, corrections that do not identify the root mismatch,
and verification requests without a concrete checklist.

## Core capabilities

### Session review

The Skill analyzes the visible session and records the objective, outcome, human actions that changed
the result, AI acceleration or friction, rework, open questions, intervention evidence, and next-session experiments.

It analyzes only visible content and explicitly available files. It never claims to read hidden or historical chat logs.

### In-session passive triggers

In addition to the original cross-session fallback, the project detects:

- two or more material revisions to the same goal or prompt;
- three or more user corrections;
- at least six user turns with three turns without accepted progress;
- repeated goal misses or a stalled / blocked goal;
- two or more failed verification attempts.

The prompt is non-blocking and protected by a cooldown. The evaluator is
<code>scripts/evaluate_trigger.py</code> and can be called by an AI IDE session wrapper or host integration.

> Important: the Skill cannot intercept every background turn by itself. A real passive trigger requires the host to call the evaluator at visible-session checkpoints.

### Cross-session Wiki

Long-term data is stored as many focused Markdown pages rather than one ever-growing file:

~~~text
<reflection-root>/
├── wiki/
│   ├── sessions/          # session reviews
│   ├── capabilities/      # AI collaboration capabilities
│   ├── interventions/     # intervention efficacy patterns
│   ├── contributions/     # concrete task contributions
│   ├── knowledge/         # domain knowledge
│   └── trends/            # cross-session trends
├── data/
│   ├── session-index.jsonl
│   ├── current-review.json
│   ├── link-index.json
│   └── trigger-state.json
└── reflection-dashboard.html
~~~

Focused pages keep retrieval selective and reduce token usage as the archive grows.
The same store can be shared across multiple AI IDEs on one machine.

### Self-contained HTML dashboard

<code>reflection-dashboard.html</code> is a presentation layer, not the source of truth.
It brings the latest review, intervention efficacy, task contribution, capabilities, knowledge,
trends, and prompt-improvement examples into one self-contained HTML file. The Markdown Wiki remains authoritative.

## Quick start

From the Skill directory:

~~~bash
# Resolve a portable runtime storage path
python3 scripts/resolve_storage.py

# Initialize the Wiki and runtime data
python3 scripts/bootstrap_store.py

# Evaluate whether the visible session needs an immediate review
python3 scripts/evaluate_trigger.py \
  --session-id 2026-08-17-001 \
  --turn 8 \
  --user-turns 8 \
  --revision-count 2 \
  --last-progress-turns 3 \
  --goal-status in_progress

# Build the HTML dashboard
python3 scripts/build_dashboard.py
~~~

To share one archive across AI IDEs, set the same
<code>AI_USE_REFLECTION_HOME</code> in each host. You can also use
<code>--store</code> explicitly or choose a project-local
<code>.ai-use-reflection/</code> store.

## Data and privacy boundaries

- The default store is a host-resolved per-user data directory, separate from the installed Skill and public repository.
- Project-local storage is available only when explicitly selected.
- Durable capability, contribution, and knowledge changes are proposed before they are written.
- The Wiki keeps compact evidence links and summaries instead of copying full transcripts.
- The project does not infer personality, psychology, employee performance, or general human worth.
- Trigger state is operational metadata, not a long-term capability or knowledge record.
- The HTML dashboard is self-contained and does not require external assets to display personal data.

## Project structure

- [SKILL.md](SKILL.md): Skill workflow and operating rules
- [references/intervention-rubric.md](references/intervention-rubric.md): intervention efficacy and task contribution rubric
- [references/intervention-examples.md](references/intervention-examples.md): typical ineffective interventions and prompt rewrites
- [references/trigger-rubric.md](references/trigger-rubric.md): in-session trigger conditions and integration contract
- [scripts/evaluate_trigger.py](scripts/evaluate_trigger.py): in-session trigger evaluator
- [scripts/build_dashboard.py](scripts/build_dashboard.py): HTML dashboard generator

## Maintainer

Jin Hefeng  
Project repository: <https://github.com/jinhefeng/ai-use-reflection>

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
