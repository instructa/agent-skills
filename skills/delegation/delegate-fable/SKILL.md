---
name: delegate-fable
description: Delegate a bounded task from a Codex session to a Fable-powered Cursor Agent in the same Herdr workspace, then wait for and collect the result. Use when Codex should bring in Fable for an independent read-only review or make Fable the sole writer for an implementation while Codex pauses and reviews afterward. Trigger for requests such as "ask Fable", "have Fable review this", "let Fable implement this", or recurring Codex-to-Cursor handoffs in Herdr.
---

# Delegate to Fable

Delegate through Herdr with one explicit mode:

- `review`: Keep Fable read-only. Use for plans, diffs, bugs, architecture, tests, or independent verification.
- `implement`: Make Fable the sole writer. Stop editing until Fable finishes, then inspect and verify its work.

Default to `review` when the user's authorization is ambiguous. Never infer permission to edit from phrases such as "take a look" or "check this".

## Prepare the handoff

Create a self-contained task containing:

- the objective and relevant project context;
- the exact scope and files when known;
- current evidence, errors, or competing hypotheses;
- constraints and explicit non-goals;
- required verification and return format.

Do not forward the entire conversation. Preserve only information needed to complete the delegated task.

Before `implement`, inspect the current workspace state and preserve unrelated or pre-existing changes. Tell Fable not to commit, check in, shelve, push, switch branches, or alter workspace configuration unless the user explicitly requested it.

## Run the delegation

Resolve this skill's directory and invoke its script. Pass the task with `--task`, `--task-file`, or stdin.

```bash
bash <skill-dir>/scripts/delegate-fable.sh review \
  --target-title "Fable 5 Reviewer" \
  --task "Review the current change for correctness, regressions, and missing tests."
```

```bash
bash <skill-dir>/scripts/delegate-fable.sh implement \
  --task "Implement the agreed fix within the stated scope and run the relevant verification."
```

The script must:

1. Honor `--target` first, then `--target-title`. A requested target is mandatory: if it is missing
   or busy, stop instead of falling back to another Cursor pane.
2. Without an explicit target, prefer a settled pane titled `Fable 5 Reviewer`, then reuse another
   idle Fable Cursor Agent in the current Herdr workspace. Split only when no Fable pane exists.
3. Submit the task, handle the known Cursor Enter fallback, wait for settlement, and return visible output.
4. Leave the Fable pane open for follow-up work.

Do not manually duplicate these steps unless the script reports a concrete failure.

Default to one complete Fable turn per hypothesis. If the response lacks the required handoff
sections, report an incomplete handoff; do not start a new pane or automatically send an open-ended
continuation. On timeout, send Escape to cancel the active turn, collect its last output, and stop.

## Handle the result

For `review`, report Fable's findings with your own assessment. Do not implement findings unless the user separately authorizes changes.

For `implement`:

1. Resume ownership only after Fable settles.
2. Inspect the actual changed files and version-control state.
3. Run proportionate verification independently.
4. Report what Fable changed, what you verified, and any remaining risk.

If Fable is `blocked`, show the blocking output to the user. Never auto-approve permissions, destructive actions, commits, check-ins, shelvesets, pushes, or branch changes.

If the script reports that no Herdr environment is available, stop and explain that the skill must run from an agent pane inside Herdr.
