# Delegate Sol

I use this skill when I want another Sol instance to take a difficult review without
leaving my current Codex session. The delegated Sol runs in a separate Herdr pane, gets
one bounded task, and returns its result to the original session.

The skill can review or implement. Those are different permissions, so the mode must be
clear.

## Review

For a review, Sol first sends two or three Terra agents to inspect different parts of the
problem in parallel. They stay read-only and gather evidence. Sol checks their work,
resolves disagreements, and makes the final call.

```text
$delegate-sol review the proposed UI architecture. Have Terra inspect ownership, runtime
call paths, and test coverage, then tell me what should change before implementation.
```

The result includes Sol's status, findings, evidence, recommendation, and the Terra work
it used. The read-only boundary comes from the delegated prompts rather than a separate
filesystem sandbox.

## Implementation

Implementation mode makes the delegated Sol the only writer. The original Codex session
waits, then inspects the changed files and verifies the result itself.

```text
$delegate-sol implement the agreed UI ownership fix. Preserve unrelated changes, run the
focused tests, and do not commit or push.
```

Sol reports what changed, what it verified, any blockers, and the next suggested action.

Clients that invoke skills with slash commands can use `/delegate-sol` instead of
`$delegate-sol`.

## Requirements

The skill must run inside Herdr and requires `herdr`, `jq`, and `codex` on `PATH`. New
panes use `gpt-5.6-sol` with `xhigh` reasoning. Review mode also requires Codex subagent
support and access to `gpt-5.6-terra`; it launches two or three Terra agents with medium
reasoning.

New Sol panes run with full filesystem access and without approval prompts. Use this
skill only in a workspace you trust. Installing it does not install Herdr or Codex.

## Install

```bash
npx skills add instructa/agent-skills --skill delegate-sol -g
```

Remove `-g` for a project-only installation.
