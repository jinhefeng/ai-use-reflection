#!/usr/bin/env python3
"""Print the resolved AI Use Reflection storage root without creating files."""

from __future__ import annotations

import argparse
import json

from storage import add_storage_args, resolve_store


def main() -> int:
    parser = argparse.ArgumentParser()
    add_storage_args(parser)
    args = parser.parse_args()
    print(json.dumps(resolve_store(args).as_dict(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
