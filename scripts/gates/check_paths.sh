#!/usr/bin/env bash
# Gate G2 — path allowlist.
# Every changed/added file must be under mirror/v5/, blocklists/, the
# regenerated whitelist files, or the tracker-radar submodule pointer.
# Anything else (e.g. mirror.py, whitelist-manual, top-level files) trips
# the gate so a human reviews the structural change instead of letting it
# ride in on a sync PR. Rules are intentionally public: the strength of
# the gate comes from enforcement (the workflow on main is the only writer
# and squash-merges only via the App token), not from hiding them.

set -euo pipefail

ALLOW='^(mirror/v5/|blocklists/|scripts/whitelist$|scripts/whitelist-subdomains$|tracker-radar$)'

cd "$(git rev-parse --show-toplevel)"

modified=$(git diff --name-only HEAD || true)
untracked=$(git ls-files --others --exclude-standard || true)
all=$(printf '%s\n%s\n' "$modified" "$untracked" | sed '/^[[:space:]]*$/d' | sort -u)

if [ -z "$all" ]; then
  echo "G2 OK: no file changes"
  exit 0
fi

violations=$(printf '%s\n' "$all" | grep -Ev "$ALLOW" || true)
if [ -n "$violations" ]; then
  echo "G2 FAIL: changed paths outside allowlist:" >&2
  printf '%s\n' "$violations" | sed 's/^/  /' >&2
  exit 2
fi

count=$(printf '%s\n' "$all" | wc -l | tr -d ' ')
echo "G2 OK: $count changed paths within allowlist"
