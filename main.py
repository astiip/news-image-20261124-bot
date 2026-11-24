#!/usr/bin/env python3
"""news-image-20261124 v1 — copy entry.png to $MAKEFUN_OUTPUT_DIR.

Run from the repo root; the Makefile invokes it as:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR")
if not OUT:
    sys.exit("MAKEFUN_OUTPUT_DIR is not set")
os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT, "entry.png"))
print("copied entry.png ->", OUT)
