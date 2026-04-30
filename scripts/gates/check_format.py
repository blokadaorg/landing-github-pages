#!/usr/bin/env python3
"""Gate G5 — format check on changed lines.

Tampering tripwire. Each added line in a mirror/v5/ or blocklists/ file must
be either blank, a comment, or a recognised host-list entry: bounded length,
no HTML/JS markers. A compromised upstream that started serving HTML or JS
in its hosts.txt would fail here even if size deltas looked normal.

The rules are intentionally public: the strength of this gate comes from
enforcement (the workflow on main is the only writer; a fork edit cannot
bypass it), not from hiding the rules. Treat this file like any other piece
of public infrastructure code.
"""

from __future__ import annotations

import re
import subprocess
import sys

ALLOWED_PREFIXES = ("mirror/v5/", "blocklists/")
MAX_LEN = 256
MAX_FAILURES_REPORTED = 20

# Recognised host-list entry shapes. Listed broadest-first; each pattern
# anchors with ^/$ so they only match a complete line.
HOST_PATTERNS = (
    # IPv4/IPv6 prefix (with optional zone identifier) + hostname.
    # Covers `0.0.0.0 host`, `127.0.0.1 host`, `255.255.255.255 host`,
    # `::1 host`, `ff02::3 host`, `fe80::1%lo0 host` — all of which appear
    # in real upstream output (1hosts /etc/hosts boilerplate).
    re.compile(r"^[0-9a-fA-F:.]+(?:%[A-Za-z0-9]+)?\s+(?:\*\.)?[A-Za-z0-9_][A-Za-z0-9_.\-]*$"),
    # Bare hostname / wildcard (ddgtrackerradar, exodusprivacy).
    re.compile(r"^(?:\*\.)?[A-Za-z0-9_][A-Za-z0-9_.\-]*$"),
    # Adblock Plus basic syntax `||domain^` (1hosts wildcards, oisd).
    # Modifiers like `$third-party`, `domain=`, `@@||allowlist^` are
    # intentionally rejected — they don't appear in current upstream
    # output and adding them would expand the parse surface for tampering.
    re.compile(r"^\|\|[A-Za-z0-9_][A-Za-z0-9_.\-]*\^$"),
)
COMMENT_RE = re.compile(r"^\s*[#!;]")
BLANK_RE = re.compile(r"^\s*$")
TAMPER_MARKERS = (
    # Each marker contains a character that does NOT appear in any valid
    # host-list entry (no `<`, `>`, `(`, `:` in `HOST_PATTERNS`), so these
    # cannot match a benign hostname. Bare alphabetic tokens like
    # "script" or "function" are intentionally NOT listed: they collide
    # with real upstream domains (e.g. `script.example.com`,
    # `scripts.clarity.ms`, `function.tracker.com`) and would block
    # auto-merge on legitimate data. HTML/JS injection still gets
    # caught via `<` / `>` / `eval(` / `javascript:` and via the
    # HOST_PATTERNS regex rejecting any line shaped like code.
    "<", ">",
    "eval(", "javascript:",
    "<!doctype", "<html", "<?xml",
)


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True)


def main() -> int:
    # Resolve repo root so the pathspecs below match regardless of caller
    # cwd. The Makefile invokes us from `scripts/`, so a bare `git diff
    # -- mirror/v5/ blocklists/` would silently match zero files and the
    # gate would pass on everything (including tampering).
    root = run("git", "rev-parse", "--show-toplevel").strip()
    diff = run(
        "git", "-C", root, "diff", "--unified=0", "HEAD", "--",
        *ALLOWED_PREFIXES,
    )
    current_path: str | None = None
    failures: list[str] = []
    checked = 0

    for raw in diff.splitlines():
        # File header: capture the post-image path. Some git versions append
        # mode/timestamp info after a tab — strip it.
        if raw.startswith("+++ b/"):
            current_path = raw[len("+++ b/"):].split("\t", 1)[0]
            continue
        if raw.startswith("--- ") or raw.startswith("@@") or raw.startswith("diff --git"):
            continue
        if not raw.startswith("+"):
            continue

        line = raw[1:]
        if BLANK_RE.match(line) or COMMENT_RE.match(line):
            continue
        checked += 1

        if len(line) > MAX_LEN:
            failures.append(
                f"{current_path}: line >{MAX_LEN} chars: {line[:80]!r}..."
            )
            continue

        low = line.lower()
        marker_hit = next((m for m in TAMPER_MARKERS if m in low), None)
        if marker_hit:
            failures.append(
                f"{current_path}: contains tamper marker {marker_hit!r}: {line[:80]!r}"
            )
            continue

        if not any(p.match(line) for p in HOST_PATTERNS):
            failures.append(
                f"{current_path}: not a recognised host-list entry: {line[:80]!r}"
            )

    if failures:
        print("G5 FAIL: format check tripped on changed lines:", file=sys.stderr)
        for f in failures[:MAX_FAILURES_REPORTED]:
            print(f"  {f}", file=sys.stderr)
        if len(failures) > MAX_FAILURES_REPORTED:
            print(f"  ... and {len(failures)-MAX_FAILURES_REPORTED} more", file=sys.stderr)
        return 5

    print(f"G5 OK: {checked} added content lines passed format check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
