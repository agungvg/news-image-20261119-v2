#!/usr/bin/env python3
"""Entry point: draw the front page and write it to /output/entry.png.

Deterministic — the same bytes on every run, no network, no clock.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    subprocess.run([sys.executable, os.path.join(HERE, "draw.py")],
                   check=True)
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), "/output/entry.png")


if __name__ == "__main__":
    main()
