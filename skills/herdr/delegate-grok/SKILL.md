---
name: delegate-grok
description: Delegate a bounded task from a Codex session to Grok 4.6 with xhigh reasoning in the same Herdr workspace, then wait for and collect the result. Use when Codex should ask Grok for a strong independent opinion, read-only review, architecture or debugging analysis, second opinion, or explicitly authorized implementation. Trigger for requests such as "ask Grok", "have Grok review this", "get Grok 4.6 xhigh's opinion", or "let Grok implement this".
---

# Delegate to Grok

Delegate through Herdr with one explicit mode:

- `review`: Keep Grok read-only. Use for plans, diffs, bugs, research, architecture, tests, adversarial analysis, or a second opinion.
- `implement`: Make Grok the sole writer. Stop editing until Grok finishes, then inspect and verify its work.

Default to `review` when authorization is ambiguous. Never infer permission to edit from phrases such as "ask Grok", "take a look", "analyze", or "check this". Use Grok 4.6 with `xhigh` reasoning by default.

## Prepare the handoff

Create a self-contained task containing:

- the objective and relevant project context;
- the exact scope and files when known;
- current evidence, errors, or competing hypotheses;
- constraints and explicit non-goals;
- required verification and return format.

Do not forward the entire conversation. Preserve only information needed for the delegated task. For opinion or research requests, distinguish sourced facts from inference and ask Grok to identify uncertainty.

Before `implement`, inspect the current workspace state and preserve unrelated or pre-existing changes. Tell Grok not to commit, check in, shelve, push, switch branches, or alter workspace configuration unless explicitly requested.

## Run the delegation

Resolve this skill's directory and invoke its script. Pass the task with `--task`, `--task-file`, or stdin.

```bash
bash <skill-dir>/scripts/delegate-grok.sh review \
  --target-title "Grok 4.6 xhigh Reviewer" \
  --task "Review the current change for correctness, regressions, and missing tests."
```

```bash
bash <skill-dir>/scripts/delegate-grok.sh implement \
  --task "Implement the agreed fix within the stated scope and run the relevant verification."
```

The script must:

1. Honor `--target` first, then `--target-title`. If a requested target is missing or busy, stop instead of falling back.
2. Without an explicit target, prefer a settled pane titled `Grok 4.6 xhigh Reviewer`, then reuse another idle Grok agent in the current Herdr workspace. Split only when no suitable Grok pane exists.
3. Start new panes with model `grok-4.6` and reasoning effort `xhigh`, submit the task, wait for settlement, and return visible output.
4. Leave the Grok pane open for follow-up work.

Do not manually duplicate these steps unless the script reports a concrete failure.

Default to one complete Grok turn per hypothesis. If the response lacks the required handoff sections, report an incomplete handoff; do not automatically send an open-ended continuation. On timeout, send Escape to cancel the active turn, collect its last output, and stop.

## Handle the result

For `review`, report Grok's findings alongside your own assessment. Do not implement findings unless the user separately authorizes changes.

For `implement`:

1. Resume ownership only after Grok settles.
2. Inspect the actual changed files and version-control state.
3. Run proportionate verification independently.
4. Report what Grok changed, what you verified, and any remaining risk.

If Grok is `blocked`, show the blocking output. Never auto-approve permissions, destructive actions, commits, check-ins, shelvesets, pushes, or branch changes.

If no Herdr environment is available, stop and explain that the skill must run from an agent pane inside Herdr.
