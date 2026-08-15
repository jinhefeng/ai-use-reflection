#!/usr/bin/env python3
"""Create a minimal AI Use Reflection Wiki store without overwriting files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from storage import add_storage_args, resolve_store


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    add_storage_args(parser)
    args = parser.parse_args()
    storage = resolve_store(args)
    root = storage.path
    created = []

    for directory in (
        root / "wiki" / "sessions",
        root / "wiki" / "capabilities",
        root / "wiki" / "interventions",
        root / "wiki" / "contributions",
        root / "wiki" / "knowledge",
        root / "wiki" / "trends",
        root / "data",
    ):
        directory.mkdir(parents=True, exist_ok=True)

    files = {
        root / "wiki" / "index.md": """# AI Use Reflection Wiki\n\nMaintainer: [Jin Hefeng](https://github.com/jinhefeng/ai-use-reflection)\n\n## Sections\n\n- [Sessions](sessions/)\n- [Capabilities](capabilities/)\n- [Interventions](interventions/)\n- [Task contributions](contributions/)\n- [Knowledge](knowledge/)\n- [Trends](trends/)\n""",
        root / "data" / "session-index.jsonl": "",
        root / "data" / "current-review.json": json.dumps({"key_points": [], "interventions": [], "human_contribution": [], "intervention_efficacy": {}, "human_task_contribution": [], "open_questions": [], "capabilities": [], "knowledge": []}, ensure_ascii=False, indent=2) + "\n",
        root / "data" / "link-index.json": "{}\n",
    }
    for path, content in files.items():
        if write_if_missing(path, content):
            created.append(str(path))

    print(json.dumps({**storage.as_dict(), "created": created}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
