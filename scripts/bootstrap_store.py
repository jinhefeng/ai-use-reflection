#!/usr/bin/env python3
"""Create a minimal AI Use Reflection Wiki store without overwriting files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--store", default=".ai-reflection")
    args = parser.parse_args()
    root = Path(args.store)
    created = []

    for directory in (
        root / "wiki" / "sessions",
        root / "wiki" / "capabilities",
        root / "wiki" / "knowledge",
        root / "wiki" / "trends",
        root / "data",
    ):
        directory.mkdir(parents=True, exist_ok=True)

    files = {
        root / "wiki" / "index.md": """# AI Use Reflection Wiki\n\nMaintainer: [Jin Hefeng](https://github.com/jinhefeng/ai-use-reflection)\n\n## Sections\n\n- [Sessions](sessions/)\n- [Capabilities](capabilities/)\n- [Knowledge](knowledge/)\n- [Trends](trends/)\n""",
        root / "data" / "session-index.jsonl": "",
        root / "data" / "current-review.json": json.dumps({"key_points": [], "human_contribution": [], "open_questions": [], "capabilities": [], "knowledge": []}, ensure_ascii=False, indent=2) + "\n",
        root / "data" / "link-index.json": "{}\n",
    }
    for path, content in files.items():
        if write_if_missing(path, content):
            created.append(str(path))

    print(json.dumps({"store": str(root), "created": created}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
