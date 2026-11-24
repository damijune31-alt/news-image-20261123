#!/usr/bin/env python3
"""news-image-20261123 entrypoint.

Stdlib-only. Copies the repo's entry.png to the output directory
(MAKEFUN_OUTPUT_DIR, default /output) as entry.png. No network,
deterministic: the output is byte-for-byte the bundled image.
"""
import hashlib
import os
import shutil
import sys


MAX_BYTES = 1048576


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
    if os.path.getsize(dst) > MAX_BYTES:
        print("ERROR: output exceeds 1 MiB", file=sys.stderr)
        return 1
    if _sha256(src) != _sha256(dst):
        print("ERROR: output digest does not match entry.png", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)" % (dst, os.path.getsize(dst), _sha256(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
