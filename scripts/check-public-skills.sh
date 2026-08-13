#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

skill_files=$(find skills -type f -name SKILL.md | sort)

if [[ -z "$skill_files" ]]; then
  echo "No public skills found under skills/." >&2
  exit 1
fi

invalid_paths=$(printf '%s\n' "$skill_files" | awk -F/ 'NF != 4')
if [[ -n "$invalid_paths" ]]; then
  echo "Public skills must use skills/<category>/<skill>/SKILL.md:" >&2
  printf '%s\n' "$invalid_paths" >&2
  exit 1
fi

while IFS= read -r skill_file; do
  if ! grep -Eq '^name:[[:space:]]*[^[:space:]]+' "$skill_file"; then
    echo "Missing skill name: $skill_file" >&2
    exit 1
  fi

  if ! grep -Eq '^description:[[:space:]]*[^[:space:]]+' "$skill_file"; then
    echo "Missing skill description: $skill_file" >&2
    exit 1
  fi
done <<< "$skill_files"

skill_names=$(
  while IFS= read -r skill_file; do
    sed -n 's/^name:[[:space:]]*//p' "$skill_file" | head -1
  done <<< "$skill_files" | sort
)

duplicate_names=$(printf '%s\n' "$skill_names" | uniq -d)
if [[ -n "$duplicate_names" ]]; then
  echo "Duplicate public skill names:" >&2
  printf '%s\n' "$duplicate_names" >&2
  exit 1
fi

forbidden_pattern='plandb|planr|plan\.ledger|docs/plan-ledger|provider-backed ledger|ledger event|agentrig|instructa-(init|status|doctor|kit)'
if grep -RInEi \
  --include='*.md' \
  --include='*.json' \
  --include='*.toml' \
  --include='*.yaml' \
  --include='*.yml' \
  "$forbidden_pattern" skills; then
  echo "Public skills contain forbidden workflow-platform coupling." >&2
  exit 1
fi

printf 'Validated %s independent public skills.\n' "$(printf '%s\n' "$skill_names" | wc -l | tr -d ' ')"
