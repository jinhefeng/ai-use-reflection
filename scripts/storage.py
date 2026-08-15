#!/usr/bin/env python3
"""Resolve portable AI Use Reflection storage roots at runtime."""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


ENV_HOME = "AI_USE_REFLECTION_HOME"
PROJECT_DIR = ".ai-use-reflection"
APP_DIR = "ai-use-reflection"


@dataclass(frozen=True)
class StorageRoot:
    path: Path
    scope: str
    source: str

    def as_dict(self) -> dict[str, str]:
        values = asdict(self)
        values["path"] = str(self.path)
        return values


def _expanded(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def _platform_root() -> tuple[Path, str]:
    """Return the standard per-user data directory for the host platform."""
    if os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return _expanded(Path(appdata) / APP_DIR), "platform:APPDATA"
        return _expanded(Path.home() / "AppData" / "Roaming" / APP_DIR), "platform:windows-default"

    if sys.platform == "darwin":
        return _expanded(Path.home() / "Library" / "Application Support" / APP_DIR), "platform:macOS"

    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        return _expanded(Path(xdg_data_home) / APP_DIR), "platform:XDG_DATA_HOME"
    return _expanded(Path.home() / ".local" / "share" / APP_DIR), "platform:XDG-default"


def add_storage_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--store",
        default=None,
        help="Explicit storage root; overrides --scope and AI_USE_REFLECTION_HOME.",
    )
    parser.add_argument(
        "--scope",
        choices=("global", "project"),
        default="global",
        help="Use the shared per-user store (default) or an explicit project-local store.",
    )
    parser.add_argument(
        "--project-root",
        default=None,
        help="Project root used with --scope project; defaults to the current directory.",
    )


def resolve_store(args: argparse.Namespace) -> StorageRoot:
    if args.store:
        return StorageRoot(_expanded(args.store), "explicit", "--store")

    if args.scope == "project":
        project_root = _expanded(args.project_root or Path.cwd())
        return StorageRoot(project_root / PROJECT_DIR, "project", "project-root")

    configured = os.environ.get(ENV_HOME)
    if configured:
        return StorageRoot(_expanded(configured), "global", f"env:{ENV_HOME}")

    path, source = _platform_root()
    return StorageRoot(path, "global", source)
