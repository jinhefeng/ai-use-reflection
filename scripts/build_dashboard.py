#!/usr/bin/env python3
"""Build a dependency-free HTML dashboard from an AI Use Reflection store."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

from storage import add_storage_args, resolve_store


AUTHOR = "Jin Hefeng"
GITHUB = "https://github.com/jinhefeng/ai-use-reflection"


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default
    except json.JSONDecodeError:
        return default


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def page_cards(root: Path, subdir: str, kind: str) -> list[dict]:
    directory = root / "wiki" / subdir
    cards = []
    if not directory.exists():
        return cards
    for path in sorted(directory.rglob("*.md")):
        if path.name == "index.md":
            continue
        text = path.read_text(encoding="utf-8")
        title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), path.stem)
        excerpt = " ".join(line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#") and not line.startswith("---"))[:240]
        cards.append({"title": title, "excerpt": excerpt, "path": path.relative_to(root).as_posix(), "kind": kind})
    return cards


def esc(value) -> str:
    return html.escape(str(value or ""), quote=True)


def card_markup(card: dict) -> str:
    return f'''<article class="card"><div class="eyebrow">{esc(card["kind"])}</div><h3>{esc(card["title"])}</h3><p>{esc(card["excerpt"])}</p><a href="{esc(card["path"])}">打开 Wiki 页面 →</a></article>'''


def build(root: Path) -> str:
    review = load_json(root / "data" / "current-review.json", {})
    sessions = read_jsonl(root / "data" / "session-index.jsonl")[-12:][::-1]
    capabilities = page_cards(root, "capabilities", "能力")
    interventions = page_cards(root, "interventions", "干预效能")
    contributions = page_cards(root, "contributions", "任务贡献")
    knowledge = page_cards(root, "knowledge", "知识")
    trends = page_cards(root, "trends", "趋势")
    key_points = review.get("key_points", [])
    interventions_current = review.get("interventions", []) or []
    human = review.get("human_contribution", [])
    task_contribution = review.get("human_task_contribution", []) or human
    efficacy = review.get("intervention_efficacy", {}) or {}
    guidance_examples = review.get("guidance_examples", []) or []
    open_questions = review.get("open_questions", [])

    def item_markup(item):
        if isinstance(item, dict):
            label = item.get("category") or item.get("dimension") or item.get("priority") or "记录"
            note = item.get("note") or item.get("behavior") or item.get("summary") or item.get("expected_gain") or ""
            confidence = item.get("confidence")
            suffix = f"（置信度：{esc(confidence)}）" if confidence else ""
            return f"<li><strong>{esc(label)}</strong>：{esc(note)}{suffix}</li>"
        return f"<li>{esc(item)}</li>"

    def list_markup(items, empty="暂无记录"):
        if not items:
            return f"<p class=\"muted\">{empty}</p>"
        return "<ul>" + "".join(item_markup(item) for item in items) + "</ul>"

    def intervention_markup(items):
        if not items:
            return '<p class="muted">暂无本次复盘的干预账本。</p>'
        rows = []
        for item in items:
            if not isinstance(item, dict):
                rows.append(f"<li>{esc(item)}</li>")
                continue
            event_id = item.get("event_id", "干预")
            event_type = item.get("type", [])
            if isinstance(event_type, list):
                event_type = " / ".join(str(value) for value in event_type)
            efficacy = item.get("efficacy", {}) or {}
            dimensions = ", ".join(f"{key}: {value}" for key, value in efficacy.items())
            rows.append(
                f'<li><strong>{esc(event_id)}</strong> · {esc(event_type)}：{esc(item.get("signal", ""))}'
                f'<br><span class="muted">机制：{esc(item.get("mechanism", ""))}；结果：{esc(item.get("outcome", ""))}；成本：{esc(item.get("observable_cost", ""))}</span>'
                f'<br><span class="metric">{esc(dimensions or "效能待评估")}</span> <span class="muted">置信度：{esc(item.get("confidence", "暂无"))}</span></li>'
            )
        return "<ol class=\"ledger\">" + "".join(rows) + "</ol>"

    def example_markup(items):
        if not items:
            return '<p class="muted">暂无针对弱干预的提示词改写示例。</p>'
        cards = []
        for item in items:
            if not isinstance(item, dict):
                cards.append(f'<article class="example"><p>{esc(item)}</p></article>')
                continue
            cards.append(
                f'<article class="example"><div class="eyebrow">{esc(item.get("scenario", "典型案例"))}</div>'
                f'<p><strong>原提示词</strong><br><span class="prompt">{esc(item.get("original_prompt", ""))}</span></p>'
                f'<p><strong>失效原因</strong><br>{esc(item.get("diagnosis", ""))}</p>'
                f'<p><strong>改进提示词</strong><br><span class="prompt improved">{esc(item.get("improved_prompt", ""))}</span></p>'
                f'<p><strong>预期收益</strong>：{esc(item.get("expected_gain", ""))}</p>'
                f'<p class="muted"><strong>下一轮验证</strong>：{esc(item.get("test_in_next_session", ""))}</p></article>'
            )
        return '<div class="example-grid">' + "".join(cards) + "</div>"

    dimensions = efficacy.get("dimensions", {}) or {}
    dimension_markup = " ".join(f'<span class="metric"><strong>{esc(key)}</strong> {esc(value)}</span>' for key, value in dimensions.items())
    efficacy_markup = f'''<div class="metric-row"><span class="metric"><strong>总体</strong> {esc(efficacy.get("overall", "暂无"))}</span><span class="metric"><strong>置信度</strong> {esc(efficacy.get("confidence", "暂无"))}</span>{dimension_markup}</div><p>{esc(efficacy.get("summary", "干预效能将在确认复盘后显示。"))}</p>{list_markup(efficacy.get("guidance", []), "暂无下一步指导。" )}'''

    session_markup = "".join(
        f'<li><span class="date">{esc(item.get("date"))}</span><strong>{esc(item.get("title"))}</strong><span class="muted">{esc(item.get("summary"))}</span></li>'
        for item in sessions
    ) or '<li class="muted">暂无会话记录</li>'

    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>AI 使用复盘 · {esc(AUTHOR)}</title>
  <style>
    :root {{ color-scheme: light; --ink:#172033; --muted:#657086; --line:#dfe5ee; --wash:#f6f8fb; --accent:#2857d8; --accent-soft:#eaf0ff; }}
    * {{ box-sizing:border-box; }} body {{ margin:0; color:var(--ink); background:var(--wash); font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    main {{ max-width:1100px; margin:0 auto; padding:42px 24px 70px; }} header {{ display:flex; justify-content:space-between; gap:24px; align-items:end; margin-bottom:28px; }}
    h1,h2,h3 {{ line-height:1.2; margin:0 0 10px; }} h1 {{ font-size:34px; letter-spacing:-.03em; }} h2 {{ font-size:21px; margin-top:34px; }} h3 {{ font-size:17px; }} p {{ margin:8px 0; }} a {{ color:var(--accent); text-decoration:none; }} a:hover {{ text-decoration:underline; }}
    .sub {{ color:var(--muted); }} .stamp {{ color:var(--muted); text-align:right; }} .hero,.panel,.card {{ background:white; border:1px solid var(--line); border-radius:16px; box-shadow:0 8px 24px rgba(33,47,79,.05); }}
    .hero {{ padding:24px; background:linear-gradient(135deg,#fff,#f1f5ff); }} .hero-grid {{ display:grid; grid-template-columns:1.2fr .8fr; gap:18px; }}
    .panel {{ padding:20px; }} .grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }} .card {{ padding:16px; }} .card p {{ color:var(--muted); font-size:14px; }}
    .metric-row {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:12px; }} .metric {{ display:inline-block; padding:5px 9px; background:#eef3ff; border-radius:999px; color:#29447f; font-size:13px; }}
    .eyebrow,.date {{ color:var(--accent); font-size:12px; text-transform:uppercase; letter-spacing:.08em; font-weight:700; }} .eyebrow {{ margin-bottom:8px; }} .muted {{ color:var(--muted); }} ul {{ margin:8px 0 0; padding-left:20px; }}
    .timeline {{ list-style:none; padding:0; margin:0; }} .timeline li {{ display:grid; grid-template-columns:120px 200px 1fr; gap:12px; padding:11px 0; border-bottom:1px solid var(--line); }} .timeline li:last-child {{ border-bottom:0; }}
    .ledger {{ margin:0; padding-left:24px; }} .ledger li {{ padding:12px 0; border-bottom:1px solid var(--line); }} .ledger li:last-child {{ border-bottom:0; }}
    .example-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:14px; }} .example {{ padding:16px; border:1px solid var(--line); border-radius:12px; background:#fbfcff; }} .example p {{ margin:10px 0; }} .prompt {{ display:block; padding:9px 11px; margin-top:4px; background:#f2f4f8; border-radius:8px; white-space:pre-wrap; }} .prompt.improved {{ background:#edf7f0; }}
    footer {{ margin-top:36px; padding-top:18px; border-top:1px solid var(--line); color:var(--muted); font-size:13px; }}
    @media (max-width:760px) {{ header,.hero-grid {{ display:block; }} .stamp {{ text-align:left; margin-top:14px; }} .grid,.example-grid {{ grid-template-columns:1fr; }} .timeline li {{ grid-template-columns:1fr; gap:2px; }} }}
  </style>
</head>
<body>
<main>
  <header><div><div class="eyebrow">Human–AI learning loop</div><h1>AI 使用复盘</h1><p class="sub">把会话中的判断、协作和知识变化，沉淀成可追溯的 Wiki。</p></div><div class="stamp">维护者：{esc(AUTHOR)}<br><a href="{GITHUB}">{GITHUB}</a></div></header>
  <section class="hero"><div class="hero-grid"><div><div class="eyebrow">Latest review</div><h2>{esc(review.get("title", "尚未生成本次复盘"))}</h2>{list_markup(key_points, "完成一次确认后的复盘，这里会显示本次重点。")}</div><div><div class="eyebrow">Human contribution</div>{list_markup(human, "暂无已确认的长期结论。")}</div></div></section>
  <h2>干预账本</h2><section class="panel">{intervention_markup(interventions_current)}</section>
  <h2>干预效能</h2><section class="panel">{efficacy_markup}</section>
  <h2>典型提示词改进</h2><section class="panel">{example_markup(guidance_examples)}</section>
  <h2>人类任务贡献</h2><section class="panel">{list_markup(task_contribution, "暂无已确认的任务贡献证据。")}</section>
  <h2>开放问题</h2><section class="panel">{list_markup(open_questions, "暂无开放问题。")}</section>
  <h2>AI 协作能力</h2><section class="grid">{''.join(card_markup(card) for card in capabilities) or '<p class="muted">暂无能力页面。</p>'}</section>
  <h2>干预 Wiki</h2><section class="grid">{''.join(card_markup(card) for card in interventions) or '<p class="muted">暂无干预页面。</p>'}</section>
  <h2>任务贡献 Wiki</h2><section class="grid">{''.join(card_markup(card) for card in contributions) or '<p class="muted">暂无任务贡献页面。</p>'}</section>
  <h2>知识 Wiki</h2><section class="grid">{''.join(card_markup(card) for card in knowledge) or '<p class="muted">暂无知识页面。</p>'}</section>
  <h2>趋势</h2><section class="grid">{''.join(card_markup(card) for card in trends) or '<p class="muted">暂无趋势页面。</p>'}</section>
  <h2>最近会话</h2><section class="panel"><ul class="timeline">{session_markup}</ul></section>
  <footer>本页面由 <code>ai-use-reflection</code> 生成。HTML 是展示层，Wiki Markdown 才是长期档案的来源。</footer>
</main>
</body>
</html>
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    add_storage_args(parser)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    storage = resolve_store(args)
    root = storage.path
    output = Path(args.output) if args.output else root / "reflection-dashboard.html"
    if not output.is_absolute():
        output = Path.cwd() / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build(root), encoding="utf-8")
    print(json.dumps({**storage.as_dict(), "output": str(output), "bytes": output.stat().st_size}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
