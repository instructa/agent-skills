---
name: instructa-init
description: Start the Agentic Engineer Kit flow: verify base/core install, choose a project plugin, run project-spec-packager, then seed plan-ledger.
---

# Instructa Init

## Purpose

Start the Agentic Engineer Kit flow: verify base/core install, choose a project plugin, run project-spec-packager, then seed plan-ledger.

## Use when

- A user is entering the Agentic Engineer Kit workflow.
- A course page or setup flow needs routing rather than domain implementation.
- The next step must be connected to core anti-drift skills without duplicating them.

## Do not use when

- The task is generic architecture, review, root-cause, or ship gating; use an instructa.core skill.
- The task belongs to a project plugin such as website, webapp, saas, api, desktop, or mcp.
- The user only wants third-party provider installation details.

## Workflow

1. Confirm `instructa.core` is installed or listed as a dependency.
2. Verify `instructa.base` is the current kit-entry layer.
3. Check whether `plan.ledger` is available through the required provider.
4. If unavailable, use `docs/plan-ledger/events.jsonl` as fallback and report the provider gap.
5. Route the user through `project-spec-packager` before implementation.
6. Route the generated seed into `plan-ledger` before project plugin work.
7. Select or confirm the project plugin only after project type is clear.
8. Report the course or learning-path checkpoint with exact next action.

## Project Type Decision Tree

- Marketing, content, docs, landing, or blog site -> `instructa.website`.
- Interactive UI, dashboard, or tool without product lifecycle complexity -> `instructa.webapp`.
- Product with users, auth, database, billing, teams, jobs, webhooks, or operations -> `instructa.saas`.
- Headless backend, API, worker, or integration service -> `instructa.api`.
- Installable, local-first, or native desktop app -> `instructa.desktop`.
- MCP server or agent tool integration -> `instructa.mcp`.
- Unsure -> `instructa.webapp` until requirements prove otherwise.

## First Kit Flow

```txt
project-spec-packager
-> docs/specs/project-spec.md
-> docs/specs/proof-oracle.md
-> docs/adrs/ADR-candidates.md
-> docs/plan-ledger/seed.json
-> docs/handoffs/agent-handoff.md
-> plan-ledger
-> PlanDB provider or docs/plan-ledger/events.jsonl fallback
-> selected project plugin workflow
```

## Gates / stop conditions

- Stop if the user has not chosen enough project intent to select a plugin.
- Stop if a required `plan.ledger` provider failure blocks the course flow and fallback is not acceptable.
- Stop if a domain plugin would own the next step.
- Stop before changing provider configuration without explicit user consent.

## Verification requirements

- Confirm dependency direction: base depends on core.
- Confirm `plan.ledger` required capability is declared by base.
- Confirm project-spec artifacts exist or are the next commanded step.
- Confirm selected project plugin depends on base when project plugins are present.

## Final report

```txt
Skill: instructa-init
Kit layer:
Project plugin:
Spec package:
Ledger:
Course checkpoint:
Next:
```
