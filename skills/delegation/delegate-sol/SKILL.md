---
name: delegate-sol
description: Delegate a bounded task from a Codex session to GPT-5.6 Sol in the same Herdr workspace, then wait for and collect the result. In review mode, require Sol to use parallel GPT-5.6 Terra subagents with medium reasoning for read-only context gathering before Sol makes the final judgment. Use for requests such as "ask Sol", "have Sol review this", "get Sol's opinion", "use Sol with Terra context gatherers", or "let Sol implement this".
---

# Delegate to Sol

Delegate through Herdr with one explicit mode:

- `review`: Keep Sol and all Terra gatherers read-only. Require Sol to launch two or three distinct
  `gpt-5.6-terra` subagents at `medium` reasoning, collect their evidence, and own the final review.
- `implement`: Make Sol the sole writer. Stop editing until Sol finishes, then inspect and verify its work.

Default to `review` when authorization is ambiguous. Never infer permission to edit from phrases
such as "ask Sol", "take a look", "analyze", or "check this". Start Sol with `gpt-5.6-sol` and
`xhigh` reasoning unless the user explicitly requests another Sol reasoning level.

## Prepare the handoff

Create a self-contained task containing:

- the objective and relevant project context;
- the exact scope and files when known;
- current evidence, errors, or competing hypotheses;
- constraints and explicit non-goals;
- required verification and return format.

Do not forward the entire conversation. Preserve only information needed for the delegated task.

Before `implement`, inspect the workspace state and preserve unrelated or pre-existing changes.
Tell Sol not to commit, check in, shelve, push, switch branches, or alter workspace configuration
unless the user explicitly requested it.

## Run the delegation

Resolve this skill's directory and invoke its script. Pass the task with `--task`, `--task-file`,
or stdin.

```bash
bash <skill-dir>/scripts/delegate-sol.sh review \
  --target-title "Sol Reviewer" \
  --task "Review the current change for correctness, regressions, and missing tests."
```

```bash
bash <skill-dir>/scripts/delegate-sol.sh implement \
  --task "Implement the agreed fix within the stated scope and run the relevant verification."
```

The script must:

1. Honor `--target` first, then `--target-title`. If a requested target is missing, is the current
   caller pane, or is busy, stop instead of falling back.
2. Without an explicit target, always create a fresh Sol pane. Reuse only a user-designated
   `--target` or the single exact, settled `--target-title` match when that pane was created by this
   skill. Never reuse the calling Codex pane or an arbitrary Codex pane.
3. Start new panes with `gpt-5.6-sol` and `xhigh` reasoning, submit the task, wait for settlement,
   and return visible output.
   For a fresh pane, place the full task in a mode-`600` temporary packet outside the project and
   pass only a short packet-reading instruction as Codex's initial CLI prompt. Keep the packet until
   Sol settles, then delete it through an exit trap.
4. In `review`, require Sol to spawn two or three parallel, read-only context gatherers with
   `model: "gpt-5.6-terra"`, `reasoning_effort: "medium"`, and `fork_turns: "none"`. Give each a
   distinct evidence-gathering scope, wait for all of them, and synthesize their results. Terra
   gatherers must not decide approval or edit files.
5. Correlate the captured terminal tail to Sol's final response with a unique per-invocation handoff
   ID. Verify that it reports two or three distinct structured Terra records, each with the required
   model, effort, fork setting, distinct scope, and evidence disposition.
6. Leave the Sol pane open for follow-up work.

Do not manually duplicate these steps unless the script reports a concrete failure.

Default to one complete Sol turn per hypothesis. If the response lacks the required handoff
sections, report an incomplete handoff; do not automatically send an open-ended continuation. On
timeout in a fresh pane owned by this invocation, send Escape, collect its last output, and stop.
For an explicitly reused pane, leave it untouched on timeout to avoid cancelling unrelated work.

## Handle the result

For `review`, report Sol's findings and Terra-gathered context alongside your own assessment. Do not
implement findings unless the user separately authorizes changes.

For `implement`:

1. Resume ownership only after Sol settles.
2. Inspect the actual changed files and version-control state.
3. Run proportionate verification independently.
4. Report what Sol changed, what you verified, and any remaining risk.

If Sol is `blocked`, show the blocking output. Never auto-approve permissions, destructive actions,
commits, check-ins, shelvesets, pushes, or branch changes.

If no Herdr environment is available, stop and explain that the skill must run from an agent pane
inside Herdr.
