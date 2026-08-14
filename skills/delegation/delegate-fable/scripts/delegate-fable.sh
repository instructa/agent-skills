#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' \
    'Usage: delegate-fable.sh <review|implement> [options]' \
    '' \
    'Options:' \
    '  --task TEXT          Task text.' \
    '  --task-file PATH     Read task text from a file.' \
    '  --target TARGET      Reuse a specific Herdr agent name or pane ID.' \
    '  --target-title TITLE Reuse the Cursor pane with this exact title.' \
    '  --model MODEL        Cursor model used when starting Fable.' \
    '  --timeout MS         Prompt settlement timeout. Default: 600000.' \
    '  --dry-run            Print the generated Fable prompt without using Herdr.' \
    '  -h, --help           Show this help.' \
    '' \
    'If neither --task nor --task-file is provided, read the task from stdin.'
}

fail() {
  printf 'delegate-fable: %s\n' "$*" >&2
  exit 1
}

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
target_override="${DELEGATE_FABLE_TARGET:-}"
target_title="${DELEGATE_FABLE_TARGET_TITLE:-}"
model="${DELEGATE_FABLE_MODEL:-claude-fable-5-thinking-high}"
timeout_ms="600000"
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
[[ -z "$target_override" || -z "$target_title" ]] || fail 'use only one of --target or --target-title'

project_cwd="$(pwd -P)"

if [[ "$mode" == "review" ]]; then
  printf -v prompt '%s\n\nProject: %s\n\nTask:\n%s\n\nRules:\n%s\n%s\n%s\n%s\n%s\n\nReturn exactly these sections:\n%s\n%s\n%s\n%s' \
    'You are Fable acting as an independent read-only reviewer.' \
    "$project_cwd" \
    "$task" \
    '- Do not create, edit, rename, or delete files.' \
    '- Do not commit, check in, shelve, push, switch branches, or change workspace configuration.' \
    '- Inspect the relevant code, existing changes, and available verification evidence.' \
    '- Run tests only when already configured and when they do not require source or VCS changes.' \
    '- If permission, missing context, or ambiguity blocks a reliable review, stop and report it.' \
    'STATUS: approved | changes_requested | blocked' \
    'FINDINGS: concrete issues ordered by severity with file references' \
    'EVIDENCE: commands, tests, or observations supporting the findings' \
    'RECOMMENDATION: the smallest safe next action'
else
  printf -v prompt '%s\n\nProject: %s\n\nTask:\n%s\n\nRules:\n%s\n%s\n%s\n%s\n%s\n%s\n\nReturn exactly these sections:\n%s\n%s\n%s\n%s\n%s' \
    'You are Fable acting as the sole implementation writer for this delegated task.' \
    "$project_cwd" \
    "$task" \
    '- Preserve all unrelated and pre-existing changes.' \
    '- Modify only the requested scope and avoid speculative cleanup.' \
    '- Do not commit, check in, shelve, push, switch branches, or change workspace configuration.' \
    '- Run the relevant tests or verification after editing.' \
    '- Do not delegate editing to another agent in the same workspace.' \
    '- If permission, missing context, or ambiguity blocks a safe implementation, stop instead of guessing.' \
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
command -v cursor-agent >/dev/null 2>&1 || fail 'cursor-agent is not installed or not on PATH'
[[ "${HERDR_ENV:-}" == "1" ]] || fail 'run this skill from an agent pane inside Herdr'

workspace_id="${HERDR_WORKSPACE_ID:-}"
if [[ -z "$workspace_id" && -n "${HERDR_PANE_ID:-}" ]]; then
  workspace_id="${HERDR_PANE_ID%%:*}"
fi
[[ -n "$workspace_id" ]] || fail 'HERDR_WORKSPACE_ID is unavailable'

target="$target_override"
if [[ -z "$target" ]]; then
  agents_json="$(herdr agent list)"
  if [[ -n "$target_title" ]]; then
    candidate="$({
      jq -c --arg workspace "$workspace_id" --arg title "$target_title" '
        [.result.agents[]
          | select(.workspace_id == $workspace and .agent == "cursor")
          | select(((.terminal_title_stripped // .terminal_title // "") | ascii_downcase)
              == ($title | ascii_downcase))][0] // empty
      ' <<<"$agents_json"
    } || true)"
    [[ -n "$candidate" ]] || fail "designated Fable pane not found: $target_title"
  else
    candidate="$({
      jq -c --arg workspace "$workspace_id" --arg cwd "$project_cwd" '
      [.result.agents[] | select(.workspace_id == $workspace and .agent == "cursor")] as $agents
      | (($agents | map(select(((.terminal_title_stripped // .terminal_title // "") | ascii_downcase)
            == "fable 5 reviewer"))[0])
        // ($agents | map(select(.cwd == $cwd and (.agent_status == "idle" or .agent_status == "done")))[0])
        // ($agents | map(select(.cwd == $cwd))[0])
        // ($agents | map(select(.agent_status == "idle" or .agent_status == "done"))[0])
        // $agents[0]
        // empty)
      ' <<<"$agents_json"
    } || true)"
  fi

  if [[ -n "$candidate" ]]; then
    target="$(jq -r '.name // .pane_id' <<<"$candidate")"
  fi
fi

if [[ -z "$target" ]]; then
  split_json="$(herdr pane split --current --direction right --cwd "$project_cwd" --no-focus)"
  pane_id="$(jq -er '.result.pane.pane_id' <<<"$split_json")" || fail 'could not read the new pane ID'
  agent_name="fable-${workspace_id//[^[:alnum:]-]/-}"
  printf 'delegate-fable: starting %s in %s\n' "$agent_name" "$pane_id" >&2
  herdr agent start "$agent_name" \
    --kind cursor \
    --pane "$pane_id" \
    --timeout 120000 \
    -- --model "$model" --trust >/dev/null
  target="$agent_name"
fi

agent_json="$(herdr agent get "$target")"
agent_workspace="$(jq -er '.result.agent.workspace_id' <<<"$agent_json")" || fail "could not inspect agent: $target"
agent_status="$(jq -er '.result.agent.agent_status' <<<"$agent_json")"
before_seq="$(jq -er '.result.agent.state_change_seq' <<<"$agent_json")"

[[ "$agent_workspace" == "$workspace_id" ]] || fail "agent $target is not in the current Herdr workspace"
[[ "$agent_status" == "idle" || "$agent_status" == "done" ]] || fail "agent $target is $agent_status; wait or choose another target"

printf 'delegate-fable: sending %s task to %s\n' "$mode" "$target" >&2
set +e
prompt_result="$(herdr agent prompt "$target" "$prompt" --wait --timeout "$timeout_ms" 2>&1)"
prompt_exit=$?
set -e

if (( prompt_exit != 0 )); then
  if grep -q 'agent_prompt_stalled' <<<"$prompt_result"; then
    printf 'delegate-fable: Cursor did not submit; sending Enter fallback\n' >&2
    herdr agent send-keys "$target" enter >/dev/null

    state_changed="0"
    deadline=$((SECONDS + 10))
    while (( SECONDS < deadline )); do
      agent_json="$(herdr agent get "$target")"
      current_seq="$(jq -er '.result.agent.state_change_seq' <<<"$agent_json")"
      if [[ "$current_seq" != "$before_seq" ]]; then
        state_changed="1"
        break
      fi
      sleep 0.2
    done
    [[ "$state_changed" == "1" ]] || fail 'Cursor still showed no state change after the Enter fallback'

    agent_status="$(jq -er '.result.agent.agent_status' <<<"$agent_json")"
    if [[ "$agent_status" == "working" ]]; then
      set +e
      wait_result="$(herdr agent wait "$target" \
        --until idle \
        --until "done" \
        --until blocked \
        --timeout "$timeout_ms" 2>&1)"
      wait_exit=$?
      set -e
      if (( wait_exit != 0 )); then
        printf 'delegate-fable: settlement timed out; cancelling %s\n' "$target" >&2
        herdr agent send-keys "$target" esc >/dev/null 2>&1 || true
        herdr agent wait "$target" --until idle --until "done" --until blocked \
          --timeout 10000 >/dev/null 2>&1 || true
        printf '%s\n' "$wait_result" >&2
        fail 'Fable exceeded the settlement timeout'
      fi
    fi
  elif grep -qiE 'timed out|"code":"timeout"|code: timeout' <<<"$prompt_result"; then
    printf 'delegate-fable: prompt timed out; cancelling %s\n' "$target" >&2
    herdr agent send-keys "$target" esc >/dev/null 2>&1 || true
    herdr agent wait "$target" --until idle --until "done" --until blocked \
      --timeout 10000 >/dev/null 2>&1 || true
    printf '%s\n' "$prompt_result" >&2
    fail 'Fable exceeded the prompt timeout'
  else
    printf '%s\n' "$prompt_result" >&2
    fail 'Herdr could not submit or settle the Fable task'
  fi
fi

agent_json="$(herdr agent get "$target")"
agent_status="$(jq -er '.result.agent.agent_status' <<<"$agent_json")"

output="$(herdr agent read "$target" --source recent-unwrapped --lines 200)"
if [[ -z "${output//[[:space:]]/}" ]]; then
  output="$(herdr agent read "$target" --source visible --lines 200)"
fi
printf '%s\n' "$output"

if [[ "$agent_status" == "blocked" ]]; then
  printf 'delegate-fable: Fable is blocked; do not auto-approve the pending action\n' >&2
  exit 3
fi

[[ "$agent_status" == "idle" || "$agent_status" == "done" ]] || fail "Fable ended in unexpected state: $agent_status"

if [[ "$mode" == "review" ]]; then
  for section in STATUS FINDINGS EVIDENCE RECOMMENDATION; do
    grep -Eq "^[[:space:]]*${section}:" <<<"$output" ||
      fail "Fable returned an incomplete handoff: missing ${section}"
  done
else
  for section in STATUS CHANGED VERIFICATION BLOCKERS NEXT; do
    grep -Eq "^[[:space:]]*${section}:" <<<"$output" ||
      fail "Fable returned an incomplete handoff: missing ${section}"
  done
fi
