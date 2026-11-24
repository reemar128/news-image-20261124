#!/usr/bin/env python3
"""Entry for make.fun news-image-20261124 (Python 3.13, stdlib only).

Copies the bundled entry.png — a 1024x1024 infographic summing up
Tuesday 24 November 2026 — to /output/entry.png. No network, no
randomness: two runs write identical bytes.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
# The copy is byte-for-byte, so a second run produces the same file.
assert (OUT / "entry.png").stat().st_size == (HERE / "entry.png").stat().st_size
