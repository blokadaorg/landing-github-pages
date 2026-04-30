#!/usr/bin/env bash
# Gate G3 — new-file detector.
# mirror.py cannot add new lists without a code change; ddg.py and exodus.py
# can produce new files when upstream metadata changes. Either way, a new
# list deserves a deliberate human look — fail the gate so the PR stays
# open for review rather than auto-merging a structural addition.

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

untracked=$(git ls-files --others --exclude-standard | sed '/^[[:space:]]*$/d')

if [ -z "$untracked" ]; then
  echo "G3 OK: no new files"
  exit 0
fi

echo "G3 FAIL: new file(s) added (require human review):" >&2
printf '%s\n' "$untracked" | sed 's/^/  /' >&2
exit 3
