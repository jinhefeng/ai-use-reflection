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
    knowledge = page_cards(root, "knowledge", "知识")
    trends = page_cards(root, "trends", "趋势")
    key_points = review.get("key_points", [])
    human = review.get("human_contribution", [])
    open_questions = review.get("open_questions", [])

    def list_markup(items, empty="暂无记录"):
        if not items:
            return f"<p class=\"muted\">{empty}</p>"
        return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"

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
    .eyebrow,.date {{ color:var(--accent); font-size:12px; text-transform:uppercase; letter-spacing:.08em; font-weight:700; }} .eyebrow {{ margin-bottom:8px; }} .muted {{ color:var(--muted); }} ul {{ margin:8px 0 0; padding-left:20px; }}
    .timeline {{ list-style:none; padding:0; margin:0; }} .timeline li {{ display:grid; grid-template-columns:120px 200px 1fr; gap:12px; padding:11px 0; border-bottom:1px solid var(--line); }} .timeline li:last-child {{ border-bottom:0; }}
    footer {{ margin-top:36px; padding-top:18px; border-top:1px solid var(--line); color:var(--muted); font-size:13px; }}
    @media (max-width:760px) {{ header,.hero-grid {{ display:block; }} .stamp {{ text-align:left; margin-top:14px; }} .grid {{ grid-template-columns:1fr; }} .timeline li {{ grid-template-columns:1fr; gap:2px; }} }}
  </style>
</head>
<body>
<main>
  <header><div><div class="eyebrow">Human–AI learning loop</div><h1>AI 使用复盘</h1><p class="sub">把会话中的判断、协作和知识变化，沉淀成可追溯的 Wiki。</p></div><div class="stamp">维护者：{esc(AUTHOR)}<br><a href="{GITHUB}">{GITHUB}</a></div></header>
  <section class="hero"><div class="hero-grid"><div><div class="eyebrow">Latest review</div><h2>{esc(review.get("title", "尚未生成本次复盘"))}</h2>{list_markup(key_points, "完成一次确认后的复盘，这里会显示本次重点。")}</div><div><div class="eyebrow">Human contribution</div>{list_markup(human, "暂无已确认的长期结论。")}</div></div></section>
  <h2>开放问题</h2><section class="panel">{list_markup(open_questions, "暂无开放问题。")}</section>
  <h2>AI 协作能力</h2><section class="grid">{''.join(card_markup(card) for card in capabilities) or '<p class="muted">暂无能力页面。</p>'}</section>
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
