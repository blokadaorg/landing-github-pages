#!/usr/bin/env python3
"""Gate G4 — per-list size delta thresholds.

For every modified file under mirror/v5/ or blocklists/, compare line count
in HEAD (the pre-sync state) vs the current working copy. Trips the gate if
the file vanished, emptied, or moved far enough to look like a broken
upstream feed rather than ordinary churn.

Large lists get the percentage rule: the big mirrors move within a few
percent weekly, so a 20% drop there means a truncated download. Small
lists are exempt from it — a 2k-line feed expiring a normal batch of
entries is a double-digit percentage, and the percentage swings grow as
the list shrinks. They trip only on a collapse.

Thresholds are intentionally public: the strength of this gate comes from
enforcement, not from hiding the rules.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

DROP_RATIO = 0.8          # large lists: post must be >= 80% of pre
COLLAPSE_RATIO = 0.25     # any list: post must be >= 25% of pre
GROWTH_RATIO = 2          # post must be <= 2x pre
PERCENT_RULE_MIN_LINES = 10000  # below this, only the collapse rule applies
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

        if post == 0:
            failures.append(f"{path}: emptied (was {pre} lines)")
        elif post < pre * COLLAPSE_RATIO:
            failures.append(
                f"{path}: line count collapsed from {pre} to {post} "
                f"({100*(1-post/pre):.0f}% drop, threshold "
                f"{100*(1-COLLAPSE_RATIO):.0f}%)"
            )
        elif pre >= PERCENT_RULE_MIN_LINES and post < pre * DROP_RATIO:
            failures.append(
                f"{path}: line count dropped from {pre} to {post} "
                f"({100*(1-post/pre):.0f}% drop, threshold {100*(1-DROP_RATIO):.0f}%)"
            )
        elif post > pre * GROWTH_RATIO:
            failures.append(
                f"{path}: line count grew from {pre} to {post} "
                f"({post/pre:.1f}x, threshold {GROWTH_RATIO}x)"
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
