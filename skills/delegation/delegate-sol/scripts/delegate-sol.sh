#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' \
    'Usage: delegate-sol.sh <review|implement> [options]' \
    '' \
    'Options:' \
    '  --task TEXT          Task text.' \
    '  --task-file PATH     Read task text from a file.' \
    '  --target TARGET      Reuse a specific Herdr agent name or pane ID.' \
    '  --target-title TITLE Reuse the Codex pane with this exact title.' \
    '  --model MODEL        Sol model used when starting Codex. Default: gpt-5.6-sol.' \
    '  --effort EFFORT      Sol reasoning effort. Default: xhigh.' \
    '  --timeout MS         Prompt settlement timeout. Default: 900000.' \
    '  --dry-run            Print the generated Sol prompt without using Herdr.' \
    '  -h, --help           Show this help.' \
    '' \
    'If neither --task nor --task-file is provided, read the task from stdin.'
}

fail() {
  printf 'delegate-sol: %s\n' "$*" >&2
  exit 1
}

task_packet=""
cleanup() {
  if [[ -n "$task_packet" && -f "$task_packet" ]]; then
    rm -f -- "$task_packet"
  fi
}
trap cleanup EXIT

mode="${1:-}"
if [[ "$mode" == "-h" || "$mode" == "--help" ]]; then
  usage
  exit 0
fi
[[ "$mode" == "review" || "$mode" == "implement" ]] || {
  usage >&2
  fail 'the first argument must be review or implement'
}
shift

task=""
task_file=""
target_override=""
target_title=""
model="${DELEGATE_SOL_MODEL:-gpt-5.6-sol}"
effort="${DELEGATE_SOL_EFFORT:-xhigh}"
timeout_ms="900000"
dry_run="0"

while (( $# > 0 )); do
  case "$1" in
    --task)
      (( $# >= 2 )) || fail '--task requires a value'
      task="$2"
      shift 2
      ;;
    --task-file)
      (( $# >= 2 )) || fail '--task-file requires a path'
      task_file="$2"
      shift 2
      ;;
    --target)
      (( $# >= 2 )) || fail '--target requires a value'
      target_override="$2"
      shift 2
      ;;
    --target-title)
      (( $# >= 2 )) || fail '--target-title requires a value'
      target_title="$2"
      shift 2
      ;;
    --model)
      (( $# >= 2 )) || fail '--model requires a value'
      model="$2"
      shift 2
      ;;
    --effort)
      (( $# >= 2 )) || fail '--effort requires a value'
      effort="$2"
      shift 2
      ;;
    --timeout)
      (( $# >= 2 )) || fail '--timeout requires milliseconds'
      timeout_ms="$2"
      shift 2
      ;;
    --dry-run)
      dry_run="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "unknown option: $1"
      ;;
  esac
done

[[ -z "$task" || -z "$task_file" ]] || fail 'use only one of --task or --task-file'
if [[ -n "$task_file" ]]; then
  [[ -f "$task_file" ]] || fail "task file not found: $task_file"
  task="$(<"$task_file")"
elif [[ -z "$task" && ! -t 0 ]]; then
  task="$(command cat)"
fi

[[ -n "${task//[[:space:]]/}" ]] || fail 'task text is required'
[[ "$timeout_ms" =~ ^[1-9][0-9]*$ ]] || fail '--timeout must be a positive integer'
if [[ -n "$target_override" ]]; then
  target_title=""
fi

project_cwd="$(pwd -P)"
if command -v uuidgen >/dev/null 2>&1; then
  handoff_token="$(uuidgen | tr -d '-' | tr '[:upper:]' '[:lower:]' | cut -c1-16)"
  handoff_id="delegate-sol-$handoff_token"
else
  handoff_id="delegate-sol-$(date +%s)-$$-$RANDOM"
fi

if [[ "$mode" == "review" ]]; then
  printf -v prompt '%s\n\nProject: %s\n\nTask:\n%s\n\nContext-gathering protocol:\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n\nReview rules:\n%s\n%s\n%s\n%s\n%s\n\nReturn exactly these sections:\n%s\n%s\n%s\n%s\n%s\n%s' \
    'You are GPT-5.6 Sol acting as the lead independent read-only reviewer.' \
    "$project_cwd" \
    "$task" \
    '- Before judging the change, use collaboration.spawn_agent to launch two or three independent context gatherers in parallel.' \
    '- Every gatherer must set model="gpt-5.6-terra", reasoning_effort="medium", and fork_turns="none".' \
    '- Give each gatherer a bounded, distinct, read-only scope derived from the task: for example contract/architecture, implementation call paths, and tests/regression evidence.' \
    '- Tell every gatherer not to create, edit, rename, or delete files and not to decide the final approval status.' \
    '- Wait for every gatherer, inspect its evidence, and resolve overlaps or contradictions yourself.' \
    '- Do not replace the Terra gatherers with local sequential inspection. If subagent tools are unavailable, return STATUS: blocked and explain why.' \
    $'- In CONTEXT, repeat this exact six-line record for each gatherer. Keep every value on its line and use a short lowercase kebab-case scope ID:\n  TERRA_GATHERER: <canonical task name>\n  MODEL: gpt-5.6-terra\n  REASONING_EFFORT: medium\n  FORK_TURNS: none\n  SCOPE_ID: <distinct-scope-id>\n  EVIDENCE_USE: used or rejected' \
    '- Do not create, edit, rename, or delete files.' \
    '- Do not commit, check in, shelve, push, switch branches, or change workspace configuration.' \
    '- Inspect the relevant code, existing changes, and available verification evidence yourself after collecting context.' \
    '- Run tests only when already configured and when they do not require source or VCS changes.' \
    '- If permission, missing context, or ambiguity blocks a reliable review, stop and report it.' \
    "HANDOFF_ID: $handoff_id" \
    'STATUS: approved | changes_requested | blocked' \
    'CONTEXT: followed by exactly two or three structured TERRA_GATHERER records' \
    'FINDINGS: concrete issues ordered by severity with file references' \
    'EVIDENCE: commands, tests, observations, and Terra evidence supporting the findings' \
    'RECOMMENDATION: the smallest safe next action'
else
  printf -v prompt '%s\n\nProject: %s\n\nTask:\n%s\n\nRules:\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n\nReturn exactly these sections:\n%s\n%s\n%s\n%s\n%s\n%s' \
    'You are GPT-5.6 Sol acting as the sole implementation writer for this delegated task.' \
    "$project_cwd" \
    "$task" \
    '- Preserve all unrelated and pre-existing changes.' \
    '- Modify only the requested scope and avoid speculative cleanup.' \
    '- Do not commit, check in, shelve, push, switch branches, or change workspace configuration.' \
    '- Run the relevant tests or verification after editing.' \
    '- Do not delegate editing to another agent in the same workspace.' \
    '- Do not spawn context-gathering subagents unless the user explicitly requested them for implementation.' \
    '- If permission, missing context, or ambiguity blocks a safe implementation, stop instead of guessing.' \
    "HANDOFF_ID: $handoff_id" \
    'STATUS: done | blocked' \
    'CHANGED: files changed and why' \
    'VERIFICATION: commands and results' \
    'BLOCKERS: unresolved issues or none' \
    'NEXT: the smallest recommended follow-up'
fi

if [[ "$dry_run" == "1" ]]; then
  printf '%s\n' "$prompt"
  exit 0
fi

command -v herdr >/dev/null 2>&1 || fail 'herdr is not installed or not on PATH'
command -v jq >/dev/null 2>&1 || fail 'jq is required but not on PATH'
command -v codex >/dev/null 2>&1 || fail 'codex is not installed or not on PATH'
[[ "${HERDR_ENV:-}" == "1" ]] || fail 'run this skill from an agent pane inside Herdr'

workspace_id="${HERDR_WORKSPACE_ID:-}"
if [[ -z "$workspace_id" && -n "${HERDR_PANE_ID:-}" ]]; then
  workspace_id="${HERDR_PANE_ID%%:*}"
fi
[[ -n "$workspace_id" ]] || fail 'HERDR_WORKSPACE_ID is unavailable'
caller_pane="${HERDR_PANE_ID:-}"
if [[ -z "$caller_pane" ]]; then
  caller_pane="$(herdr pane current | jq -er '.result.pane.pane_id')" ||
    fail 'could not resolve the calling Herdr pane'
fi

target="$target_override"
created_here="0"
if [[ -z "$target" ]]; then
  if [[ -n "$target_title" ]]; then
    agents_json="$(herdr agent list)"
    candidates="$({
      jq -c --arg workspace "$workspace_id" --arg title "$target_title" '
        [.result.agents[]
          | select(.workspace_id == $workspace and .agent == "codex")
          | select((.terminal_title_stripped // .terminal_title // "") == $title)]
      ' <<<"$agents_json"
    } || true)"
    candidate_count="$(jq -r 'length' <<<"$candidates")"
    [[ "$candidate_count" == "1" ]] || {
      if [[ "$candidate_count" == "0" ]]; then
        fail "designated Sol pane not found: $target_title"
      fi
      fail "multiple Codex panes have the exact title: $target_title"
    }
    target="$(jq -r '.[0].name // .[0].pane_id' <<<"$candidates")"
  fi
fi

if [[ -z "$target" ]]; then
  split_json="$(herdr pane split --current --direction right --cwd "$project_cwd" --no-focus)"
  pane_id="$(jq -er '.result.pane.pane_id' <<<"$split_json")" || fail 'could not read the new pane ID'
  safe_workspace="${workspace_id//[^[:alnum:]-]/-}"
  safe_workspace="$(printf '%s' "$safe_workspace" | tr '[:upper:]' '[:lower:]')"
  safe_workspace="${safe_workspace:0:6}"
  agent_name="delegate-sol-${safe_workspace}-$$"
  [[ "$agent_name" =~ ^[a-z][a-z0-9_-]{0,31}$ ]] || fail 'could not derive a valid Herdr agent name'

  shell_ready="0"
  shell_deadline=$((SECONDS + 10))
  while (( SECONDS < shell_deadline )); do
    process_json="$(herdr pane process-info --pane "$pane_id" 2>/dev/null || true)"
    if jq -e '
        .result.process_info as $process
        | ($process.foreground_processes | length) == 1
          and $process.foreground_processes[0].pid == $process.shell_pid
      ' <<<"$process_json" >/dev/null 2>&1; then
      shell_ready="1"
      break
    fi
    sleep 0.2
  done
  if [[ "$shell_ready" != "1" ]]; then
    herdr pane close "$pane_id" >/dev/null 2>&1 || true
    fail 'the new Herdr pane did not reach an available shell; closed it'
  fi

  task_packet="$(mktemp "${TMPDIR:-/tmp}/delegate-sol-task.XXXXXX")"
  chmod 600 "$task_packet"
  printf '%s\n' "$prompt" >"$task_packet"
  initial_prompt="Read the complete delegated task from $task_packet, follow it exactly, and return its required handoff."

  printf 'delegate-sol: starting %s in %s\n' "$agent_name" "$pane_id" >&2
  if ! herdr agent start "$agent_name" \
      --kind codex \
      --pane "$pane_id" \
      --timeout 120000 \
      -- \
      -m "$model" \
      -c "model_reasoning_effort=\"$effort\"" \
      -s danger-full-access \
      -a never \
      "$initial_prompt" >/dev/null; then
    herdr pane close "$pane_id" >/dev/null 2>&1 || true
    fail 'could not start Sol; closed the pane created by this delegation attempt'
  fi
  target="$agent_name"
  created_here="1"
fi

agent_json="$(herdr agent get "$target")"
agent_workspace="$(jq -er '.result.agent.workspace_id' <<<"$agent_json")" || fail "could not inspect agent: $target"
agent_kind="$(jq -er '.result.agent.agent' <<<"$agent_json")"
agent_name="$(jq -r '.result.agent.name // ""' <<<"$agent_json")"
agent_pane="$(jq -er '.result.agent.pane_id' <<<"$agent_json")"
agent_status="$(jq -er '.result.agent.agent_status' <<<"$agent_json")"

[[ "$agent_workspace" == "$workspace_id" ]] || fail "agent $target is not in the current Herdr workspace"
[[ "$agent_kind" == "codex" ]] || fail "agent $target is not a Codex/Sol pane"
[[ "$agent_pane" != "$caller_pane" ]] || fail 'refusing to delegate back into the calling Codex pane'
if [[ "$created_here" != "1" && "$agent_name" != delegate-sol-* ]]; then
  fail 'refusing to reuse a Codex pane that was not created by delegate-sol'
fi
if [[ "$created_here" == "1" ]]; then
  printf 'delegate-sol: waiting for the initial %s task in %s\n' "$mode" "$target" >&2
  if [[ "$agent_status" == "idle" || "$agent_status" == "done" ]]; then
    set +e
    start_result="$(herdr agent wait "$target" --until working --until blocked --timeout 120000 2>&1)"
    start_exit=$?
    set -e
    if (( start_exit != 0 )); then
      printf '%s\n' "$start_result" >&2
      herdr agent send-keys "$target" esc >/dev/null 2>&1 || true
      herdr pane close "$agent_pane" >/dev/null 2>&1 || true
      fail 'Sol did not begin its initial task; closed the owned pane'
    fi
    agent_json="$(herdr agent get "$target")"
    agent_status="$(jq -er '.result.agent.agent_status' <<<"$agent_json")"
  fi
  if [[ "$agent_status" == "working" ]]; then
    set +e
    wait_result="$(herdr agent wait "$target" --until idle --until "done" --until blocked --timeout "$timeout_ms" 2>&1)"
    wait_exit=$?
    set -e
    if (( wait_exit != 0 )); then
      printf '%s\n' "$wait_result" >&2
      if grep -qiE 'timed out|"code":"timeout"|code: timeout' <<<"$wait_result"; then
        printf 'delegate-sol: initial task timed out; cancelling owned pane %s\n' "$target" >&2
        herdr agent send-keys "$target" esc >/dev/null 2>&1 || true
        herdr agent wait "$target" --until idle --until "done" --until blocked --timeout 10000 >/dev/null 2>&1 || true
      fi
      fail 'Sol did not settle its initial task'
    fi
  elif [[ "$agent_status" != "idle" && "$agent_status" != "done" && "$agent_status" != "blocked" ]]; then
    fail "Sol initial task entered unexpected state: $agent_status"
  fi
else
  [[ "$agent_status" == "idle" || "$agent_status" == "done" ]] || fail "agent $target is $agent_status; wait or choose another target"
  printf 'delegate-sol: sending %s task to reused pane %s\n' "$mode" "$target" >&2
  set +e
  prompt_result="$(herdr agent prompt "$target" "$prompt" --wait --timeout "$timeout_ms" 2>&1)"
  prompt_exit=$?
  set -e
  if (( prompt_exit != 0 )); then
    printf '%s\n' "$prompt_result" >&2
    if grep -qiE 'timed out|"code":"timeout"|code: timeout' <<<"$prompt_result"; then
      fail 'the reused Sol pane timed out; left it untouched'
    fi
    fail 'the reused Sol pane did not submit or settle; left it untouched'
  fi
fi

agent_json="$(herdr agent get "$target")"
agent_status="$(jq -er '.result.agent.agent_status' <<<"$agent_json")"

output="$(herdr agent read "$target" --source recent-unwrapped --lines 400)"
if [[ -z "${output//[[:space:]]/}" ]]; then
  output="$(herdr agent read "$target" --source visible --lines 400)"
fi
printf '%s\n' "$output"

if [[ "$agent_status" == "blocked" ]]; then
  printf 'delegate-sol: Sol is blocked; do not auto-approve the pending action\n' >&2
  exit 3
fi

[[ "$agent_status" == "idle" || "$agent_status" == "done" ]] || fail "Sol ended in unexpected state: $agent_status"

handoff="$(awk -v handoff_id="$handoff_id" '
  {
    marker = $0
    sub(/^[[:space:]]*•[[:space:]]*/, "", marker)
    if ($0 ~ /^[[:space:]]*•/ && marker == "HANDOFF_ID: " handoff_id) {
      captured = ""
      in_handoff = 1
    }
  }
  in_handoff { captured = captured $0 ORS }
  END { printf "%s", captured }
' <<<"$output")"
[[ -n "${handoff//[[:space:]]/}" ]] || fail 'Sol returned no identifiable final handoff'
grep -Fq "HANDOFF_ID: $handoff_id" <<<"$handoff" || fail 'Sol returned a stale or mismatched handoff'

if [[ "$mode" == "review" ]]; then
  for section in STATUS CONTEXT FINDINGS EVIDENCE RECOMMENDATION; do
    grep -Eq "^[[:space:]•>*_#-]*(\*\*)?${section}:(\*\*)?" <<<"$handoff" ||
      fail "Sol returned an incomplete handoff: missing ${section}"
  done
  grep -Eq '^[[:space:]•>*_#-]*(\*\*)?STATUS:(\*\*)?[[:space:]]+(approved|changes_requested|blocked)[[:space:]]*$' <<<"$handoff" ||
    fail 'Sol returned an invalid review status'
  context_section="$(awk '
    /^[[:space:]•>*_#-]*(\*\*)?CONTEXT:(\*\*)?/ { in_context = 1; next }
    /^[[:space:]•>*_#-]*(\*\*)?FINDINGS:(\*\*)?/ { in_context = 0 }
    in_context
  ' <<<"$handoff")"
  gatherer_records=()
  gatherer_record=""
  while IFS= read -r context_line; do
    if [[ "$context_line" =~ ^[[:space:]]*TERRA_GATHERER: ]]; then
      if [[ -n "$gatherer_record" ]]; then
        gatherer_records+=("$gatherer_record")
      fi
      gatherer_record="$context_line"
    elif [[ -n "$gatherer_record" ]]; then
      gatherer_record+=$'\n'"$context_line"
    fi
  done <<<"$context_section"
  if [[ -n "$gatherer_record" ]]; then
    gatherer_records+=("$gatherer_record")
  fi

  gatherer_count="${#gatherer_records[@]}"
  (( gatherer_count >= 2 && gatherer_count <= 3 )) || fail 'Sol handoff must report exactly two or three Terra context gatherers'
  gatherer_names=""
  gatherer_scopes=""
  for gatherer_record in "${gatherer_records[@]}"; do
    gatherer_name="$(sed -En 's|^[[:space:]]*TERRA_GATHERER:[[:space:]]+(/[^[:space:]]+)[[:space:]]*$|\1|p' <<<"$gatherer_record")"
    [[ -n "$gatherer_name" ]] || fail 'a Terra gatherer has a missing or invalid canonical identity'
    [[ "$(grep -Ec '^[[:space:]]*MODEL:[[:space:]]+gpt-5\.6-terra[[:space:]]*$' <<<"$gatherer_record")" == "1" ]] || fail 'a Terra gatherer has the wrong or missing model'
    [[ "$(grep -Ec '^[[:space:]]*REASONING_EFFORT:[[:space:]]+medium[[:space:]]*$' <<<"$gatherer_record")" == "1" ]] || fail 'a Terra gatherer has the wrong or missing reasoning effort'
    [[ "$(grep -Ec '^[[:space:]]*FORK_TURNS:[[:space:]]+none[[:space:]]*$' <<<"$gatherer_record")" == "1" ]] || fail 'a Terra gatherer has the wrong or missing fork setting'
    gatherer_scope="$(sed -En 's/^[[:space:]]*SCOPE_ID:[[:space:]]+([a-z0-9]+(-[a-z0-9]+)*)[[:space:]]*$/\1/p' <<<"$gatherer_record")"
    [[ -n "$gatherer_scope" ]] || fail 'a Terra gatherer is missing its kebab-case scope ID'
    [[ "$(grep -Ec '^[[:space:]]*EVIDENCE_USE:[[:space:]]+(used|rejected)[[:space:]]*$' <<<"$gatherer_record")" == "1" ]] || fail 'a Terra gatherer has an invalid evidence disposition'
    record_line_count="$(sed '/^[[:space:]]*$/d' <<<"$gatherer_record" | wc -l | tr -d '[:space:]')"
    [[ "$record_line_count" == "6" ]] || fail 'a Terra gatherer record must contain exactly six non-empty lines'
    gatherer_names+="$gatherer_name"$'\n'
    gatherer_scopes+="$gatherer_scope"$'\n'
  done
  distinct_gatherers="$(sort -u <<<"$gatherer_names" | sed '/^[[:space:]]*$/d' | wc -l | tr -d '[:space:]')"
  [[ "$distinct_gatherers" == "$gatherer_count" ]] || fail 'Sol handoff contains duplicate Terra gatherer identities'
  distinct_scopes="$(sort -u <<<"$gatherer_scopes" | sed '/^[[:space:]]*$/d' | wc -l | tr -d '[:space:]')"
  [[ "$distinct_scopes" == "$gatherer_count" ]] || fail 'Sol handoff contains duplicate Terra gatherer scopes'
else
  for section in STATUS CHANGED VERIFICATION BLOCKERS NEXT; do
    grep -Eq "^[[:space:]•>*_#-]*(\*\*)?${section}:(\*\*)?" <<<"$handoff" ||
      fail "Sol returned an incomplete handoff: missing ${section}"
  done
  grep -Eq '^[[:space:]•>*_#-]*(\*\*)?STATUS:(\*\*)?[[:space:]]+(done|blocked)[[:space:]]*$' <<<"$handoff" ||
    fail 'Sol returned an invalid implementation status'
fi
