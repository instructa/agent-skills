# Instructa Base

Kit-entry layer for the Agentic Engineer Kit.

`instructa.base` depends on `instructa.core`, requires the `plan.ledger` capability for the kit flow, and routes users into the right project plugin. It may mention Instructa, the course, and kit onboarding. Core skills stay vendor-neutral and generic.

## What Is Included

Skills:

- `instructa-init`
- `instructa-status`
- `instructa-doctor-routing`
- `kit-decision-tree`
- `project-plugin-selector`
- `install-verification`
- `course-checkpoint`
- `learning-path-handoff`
- `plandb-setup`

Public commands:

- `instructa-init`
- `instructa-status`
- `instructa-doctor-routing`
- `project-plugin-selector`
- `course-checkpoint`

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
-> project-plugin-selector
-> selected project plugin workflow
```

## Capability

Requires `plan.ledger` through `third-party.plandb`, with `docs/plan-ledger/events.jsonl` as the documented fallback path.
