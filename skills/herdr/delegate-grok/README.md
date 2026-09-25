# Delegate Grok

I use this skill when I want a second opinion from Grok without copying context into a
separate terminal and managing another agent by hand. It opens or reuses a Grok pane in
the same Herdr workspace, sends a bounded task, waits for the response, and brings the
result back to the original Codex session.

The skill has two modes because asking for a review and handing over implementation are
not the same permission.

## Review

Review mode tells Grok to stay read-only. I use it for architecture decisions, debugging
hypotheses, plans, diffs, and adversarial checks when I want an independent answer before
changing anything.

```text
$delegate-grok review the current diff for correctness, regressions, and missing tests.
Give me findings with file references and recommend the smallest safe next step.
```

The returned handoff contains a status, findings, evidence, and a recommendation. Review
mode is enforced by the prompt, not by a separate filesystem sandbox, so Grok still runs
inside the same workspace.

## Implementation

Implementation mode makes Grok the sole writer for the delegated task. Codex should stop
editing until Grok finishes, then inspect the actual diff and run its own verification.

```text
$delegate-grok implement the agreed parser fix in packages/core. Stay inside that scope,
preserve unrelated changes, and run the relevant tests. Do not commit or push.
```

The handoff reports changed files, verification, blockers, and the next suggested action.
The implementation prompt tells Grok not to commit, push, switch branches, or change
workspace configuration.

Clients that invoke skills with slash commands can use `/delegate-grok` instead of
`$delegate-grok`.

## Requirements

This is deliberately a Herdr skill. It must run from an agent pane inside Herdr and
requires `herdr`, `jq`, and the `grok` CLI on `PATH`. New panes use Grok 4.6 with `xhigh`
reasoning by default. The model and effort can be changed with script flags or the
`DELEGATE_GROK_MODEL` and `DELEGATE_GROK_EFFORT` environment variables.

Installing the skill does not install Herdr or Grok.

## Install

```bash
npx skills add instructa/agent-skills --skill delegate-grok -g
```

Remove `-g` for a project-only installation.
