#!/usr/bin/env python3
"""Entry point: copy the committed front page to the output directory.

The front page is already rendered and committed as entry.png; this
entrypoint only copies it to $MAKEFUN_OUTPUT_DIR/entry.png and verifies
the copy byte-for-byte (same size, PNG signature, identical sha256).

No rendering, no subprocess, no third-party imports -- stdlib only -- so
it runs on the grader's read-only mount, where the repository at /bot
cannot be written to.
"""
import hashlib
import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(src) != os.path.getsize(dst):
        print("copy size mismatch", file=sys.stderr)
        return 1
    with open(dst, "rb") as f:
        head = f.read(len(PNG_SIGNATURE))
    if head != PNG_SIGNATURE:
        print("copy is not a PNG file", file=sys.stderr)
        return 1
    if _sha256(src) != _sha256(dst):
        print("copy hash mismatch", file=sys.stderr)
        return 1
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
