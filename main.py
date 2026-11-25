"""Entry point for the news-image-20261124 front page.

Copies the image built by build_image.py into the output directory
the grader provides. Standard library only.

Usage:
    python3 main.py
Environment:
    MAKEFUN_OUTPUT_DIR - directory to receive entry.png
                         (default: /output)
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        sys.stderr.write("entry.png not found next to main.py\n")
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print("wrote", target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
