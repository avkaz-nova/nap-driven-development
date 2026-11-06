#!/usr/bin/env bash
# Hash the Markdown body, independent of lifecycle metadata and host line endings.
set -euo pipefail
[[ $# -eq 1 && -f "$1" ]] || { echo 'Usage: bash spec-digest.sh path/to/spec.md' >&2; exit 1; }
if command -v shasum >/dev/null 2>&1; then
  hash() { shasum -a 256 | awk '{print $1}'; }
else
  hash() { sha256sum | awk '{print $1}'; }
fi
LC_ALL=C awk '
  { sub(/\r$/, "") }
  NR == 1 { sub(/^\357\273\277/, ""); if ($0 != "---") exit 1; next }
  !body && $0 == "---" { body=1; next }
  body { lines[++n]=$0 }
  END {
    if (!body) exit 1
    while (n > 0 && lines[n] == "") n--
    if (n == 0) exit 1
    for (i=1; i<=n; i++) print lines[i]
  }
' "$1" | hash
