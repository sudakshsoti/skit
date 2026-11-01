#!/usr/bin/env bash
# Cut a release: ./scripts/release.sh 1.1.0
# Bumps .claude-plugin/plugin.json, commits, tags v<version>, pushes, and
# creates a GitHub release with generated notes. Users with auto-update on
# receive it at their next Claude Code start; everyone else on
# `/plugin marketplace update soti`.
set -euo pipefail
cd "$(dirname "$0")/.."

version="${1:-}"
[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "usage: $0 <major.minor.patch>" >&2; exit 2; }
[[ "$(git branch --show-current)" == main ]] || { echo "release from main" >&2; exit 1; }
[[ -z "$(git status --porcelain)" ]] || { echo "working tree is dirty" >&2; exit 1; }
git rev-parse -q --verify "refs/tags/v$version" >/dev/null && { echo "tag v$version exists" >&2; exit 1; }

git fetch -q origin main
[[ "$(git rev-parse HEAD)" == "$(git rev-parse origin/main)" ]] || { echo "main is not in sync with origin/main" >&2; exit 1; }

python3 scripts/lint.py
if command -v claude >/dev/null; then claude plugin validate . >/dev/null; fi

python3 - "$version" <<'PY'
import json, sys, pathlib
p = pathlib.Path(".claude-plugin/plugin.json")
d = json.loads(p.read_text())
d["version"] = sys.argv[1]
p.write_text(json.dumps(d, indent=2) + "\n")
PY

git commit -q -am "release: v$version"
git tag -a "v$version" -m "v$version"
git push -q origin main "v$version"
gh release create "v$version" --title "v$version" --generate-notes
