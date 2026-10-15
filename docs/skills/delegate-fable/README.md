# Delegate Fable

I use Fable as a second pair of hands through Cursor Agent. This skill keeps that handoff
inside the current Herdr workspace, so I can ask for an independent review or let Fable
implement one bounded change without manually moving prompts and results between panes.

There are two modes, and the distinction matters because only one of them authorizes
editing.

## Review

Review mode asks Fable to inspect the current project without changing files. It works
well when I want another model to challenge a plan, read a diff, look for missing tests,
or verify whether a proposed fix addresses the actual problem.

```text
$delegate-fable review the current authentication changes. Stay read-only, identify
concrete regressions with file references, and tell me whether the change is ready.
```

Fable returns a status, findings, evidence, and a recommendation. The read-only boundary
comes from the delegated prompt rather than a separate filesystem sandbox.

## Implementation

Implementation mode makes Fable the only writer while the task is running. The original
Codex session should pause, wait for Fable to settle, then review the files and verify the
result independently.

```text
$delegate-fable implement the agreed empty-state fix in the web app. Keep the existing
design, preserve unrelated changes, run the focused tests, and do not commit or push.
```

The final handoff reports what changed, what was verified, any blocker, and the next
action. Fable is told not to commit, push, switch branches, or modify workspace
configuration.

Clients that invoke skills with slash commands can use `/delegate-fable` instead of
`$delegate-fable`.

## Requirements

The skill must run inside Herdr and requires `herdr`, `jq`, and `cursor-agent` on `PATH`.
It starts a Cursor Agent with the Fable model and passes `--trust`, so it should only be
used in a workspace you trust. The default model can be changed with `--model` or
`DELEGATE_FABLE_MODEL`.

Installing the skill does not install Herdr or Cursor Agent.

## Install

```bash
npx skills add instructa/agent-skills --skill delegate-fable -g
```

Remove `-g` for a project-only installation.
