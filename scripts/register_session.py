#!/usr/bin/env python3
"""Append a compact session manifest and report whether a review suggestion is due."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def read_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--store", default=".ai-reflection")
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--topics", default="")
    parser.add_argument("--summary", default="")
    parser.add_argument("--eligible", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--reviewed", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--threshold", type=int, default=3)
    args = parser.parse_args()

    root = Path(args.store)
    root.mkdir(parents=True, exist_ok=True)
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    index_path = data_dir / "session-index.jsonl"
    records = read_records(index_path)
    if any(item.get("session_id") == args.session_id for item in records):
        raise SystemExit(f"session_id already exists: {args.session_id}")

    record = {
        "session_id": args.session_id,
        "date": date.today().isoformat(),
        "title": args.title,
        "topics": [item.strip() for item in args.topics.split(",") if item.strip()],
        "summary": args.summary[:500],
        "eligible": args.eligible,
        "reviewed": args.reviewed,
    }
    with index_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    eligible_unreviewed = [
        item for item in records + [record] if item.get("eligible") and not item.get("reviewed")
    ]
    result = {
        "record": record,
        "eligible_unreviewed_count": len(eligible_unreviewed),
        "review_due": len(eligible_unreviewed) >= max(args.threshold, 1),
        "threshold": max(args.threshold, 1),
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
