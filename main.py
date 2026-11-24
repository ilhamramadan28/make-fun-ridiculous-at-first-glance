#!/usr/bin/env python3
"""Ridiculous at First Glance, Real by the Second.

Writes the one-sentence startup pitch to /output/entry.txt.
The pitch lives in entry.txt next to this file; this program only
validates it against the gate and copies it to /output.
"""

import os
import shutil
import stat


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.txt")
    with open(src, "r", encoding="utf-8") as f:
        text = f.read()
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 chars, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, one sentence")
    if text[-1] not in ".!?":
        raise ValueError("entry must end with a sentence terminator")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.txt")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)
    with open(src, "rb") as f:
        expected = f.read()
    with open(dst, "rb") as f:
        actual = f.read()
    if expected != actual:
        raise ValueError("output differs from entry.txt")
    mode = stat.S_IMODE(os.stat(dst).st_mode)
    if mode != 0o644:
        raise ValueError(f"output mode must be 0644, got {oct(mode)}")


if __name__ == "__main__":
    main()
