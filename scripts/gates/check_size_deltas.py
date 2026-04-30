#!/usr/bin/env python3
"""Gate G4 — per-list size delta thresholds.

For every modified file under mirror/v5/ or blocklists/, compare line count
in HEAD (the pre-sync state) vs the current working copy. Trips the gate if
the new file dropped more than 20% of its lines (likely a partially-broken
upstream feed) or grew to more than 10x its previous size (likely an upstream
that started spamming or got compromised).

Thresholds are intentionally public: the strength of this gate comes from
enforcement, not from hiding the rules.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

DROP_RATIO = 0.8       # post must be >= 80% of pre
GROWTH_RATIO = 10      # post must be <= 10x pre
ALLOWED_PREFIXES = ("mirror/v5/", "blocklists/")


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True)


def repo_root() -> Path:
    return Path(run("git", "rev-parse", "--show-toplevel").strip())


def main() -> int:
    root = repo_root()
    modified = run("git", "-C", str(root), "diff", "--name-only", "HEAD").splitlines()
    targets = [p for p in modified if p.startswith(ALLOWED_PREFIXES)]
    if not targets:
        print("G4 OK: no modified mirror/blocklist files")
        return 0

    failures: list[str] = []
    for path in targets:
        try:
            pre_blob = subprocess.check_output(
                ["git", "-C", str(root), "show", f"HEAD:{path}"],
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            continue
        pre = pre_blob.count(b"\n")

        full = root / path
        if not full.exists():
            failures.append(f"{path}: deleted entirely (was {pre} lines)")
            continue
        post = full.read_bytes().count(b"\n")

        if pre == 0:
            continue

        if post < pre * DROP_RATIO:
            failures.append(
                f"{path}: line count dropped from {pre} to {post} "
                f"({100*(1-post/pre):.0f}% drop, threshold 20%)"
            )
        elif post > pre * GROWTH_RATIO:
            failures.append(
                f"{path}: line count grew from {pre} to {post} "
                f"({post/pre:.1f}x, threshold 10x)"
            )

    if failures:
        print("G4 FAIL: size delta thresholds tripped:", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        return 4

    print(f"G4 OK: {len(targets)} files within size-delta thresholds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
