---
name: local-health
description: Check local repository health before gates by identifying available package managers, test commands, lint commands, format commands, and risky missing prerequisites.
---

# Local Health

## Purpose

Map the local repository's verification surface before a review or ship gate chooses commands.

## Use when

- A gate needs to know which local checks exist.
- The repo has no obvious test or lint command.
- A feature spans package-manager, shell, or generated-file boundaries.

## Do not use when

- The repo already declares the exact command to run.
- The user only asks for a specific test command.

## Workflow

1. Inspect repo-local command surfaces such as package manifests, task runners, makefiles, cargo, go, or language-specific config.
2. Identify test, lint, typecheck, format, build, and scanner commands.
3. Prefer commands already documented by the repo.
4. Mark unknowns as unknown; do not invent checks.
5. Return the narrowest command set that proves the touched surface.

## Verification

- List files inspected.
- List commands selected.
- State which commands were not run.

## Anti-patterns

- Do not start dev servers.
- Do not run long watchers for one-shot verification.
- Do not install dependencies just to guess commands.

## Final report

```txt
Skill: local-health
Commands found:
Commands missing:
Proof:
Risks:
```
