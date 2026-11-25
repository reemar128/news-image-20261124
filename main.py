#!/usr/bin/env python3
"""Entry point for the news-image-20261124 front page.

Copies the pre-rendered entry.png next to this file into the output
directory make.fun expects. Standard library only; no network, no
randomness, deterministic.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, target)
    print("copied", source, "->", target)


if __name__ == "__main__":
    main()
