#!/usr/bin/env python3
"""Mark selected session records as reviewed without changing other fields."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from storage import add_storage_args, resolve_store


def main() -> int:
    parser = argparse.ArgumentParser()
    add_storage_args(parser)
    parser.add_argument("--session-ids", required=True, help="Comma-separated session IDs")
    args = parser.parse_args()

    target_ids = {item.strip() for item in args.session_ids.split(",") if item.strip()}
    storage = resolve_store(args)
    path = storage.path / "data" / "session-index.jsonl"
    if not path.exists():
        raise SystemExit(f"missing session index: {path}")

    records = []
    changed = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("session_id") in target_ids and not record.get("reviewed"):
            record["reviewed"] = True
            changed.append(record["session_id"])
        records.append(record)

    path.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in records), encoding="utf-8")
    print(json.dumps({**storage.as_dict(), "updated": changed, "count": len(changed)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
