"""Ensure Quarto-rendered notebooks can import the local package."""
from __future__ import annotations

import sys
from pathlib import Path


def ensure_src_on_path() -> None:
    """Add the repo's src directory to sys.path if missing."""
    repo_root = Path(__file__).resolve().parents[1]
    src_dir = repo_root / "src"
    src_str = str(src_dir)

    if src_dir.exists() and src_str not in sys.path:
        sys.path.insert(0, src_str)


ensure_src_on_path()
