---
name: plan-ledger
description: Persist specs, ADRs, tasks, ownership changes, proof receipts, review receipts, and ship receipts in a provider-backed ledger or local fallback ledger.
---

# Plan Ledger

## Purpose

Keep durable project decisions and proof out of transient chat so later agents can resume from evidence instead of memory.

## Use when

- creating or importing project spec seed data
- recording ADR or task state that must survive chat context
- adding proof, review, or ship receipts
- falling back to local ledger files when no provider is installed

## Do not use when

- the information is temporary conversation scratchpad
- the event has no evidence and no explicit human decision
- the user needs a full project-management board rather than durable state receipts

## Inputs needed

- repo state and active branch
- user request and acceptance criteria
- relevant files, diffs, docs, ADRs, or manifests
- known constraints, non-goals, and risk boundaries
- optional capability context when justified

## Output contract

This skill must produce:

```txt
accepted ledger event JSON
provider import/write when plan.ledger is available
fallback docs/plan-ledger/events.jsonl entry
linked ADR/spec/proof artifact
proof/receipt
ledger event when durable state changes
```

## Workflow

### Phase 0 - Triage

- Restate the task in one sentence.
- Decide whether this skill is the right owner or whether another gate should run first.
- Identify the current artifact, behavior, or decision that can drift.
- Name the expected durable output before touching files.

### Phase 1 - Context gathering

- Read only the files, docs, manifests, tests, or diffs needed for this decision.
- Prefer repo-local architecture and test conventions over generic advice.
- Use optional capabilities only when the request depends on current external facts, ledger state, remote state, scanning, or shell linting.
- Capture missing context as an explicit assumption rather than filling gaps with guesses.

### Phase 2 - Analysis

- Analyze event type.
- Analyze source skill.
- Analyze status.
- Analyze linked files.
- Analyze evidence commands.
- Analyze human decisions.
- Analyze superseded events.
- Analyze fallback path.
- Separate facts found in files from judgments or recommendations.
- Choose one canonical owner or one canonical artifact whenever the decision concerns ownership.

### Phase 3 - Action / artifact

- Produce the smallest durable artifact that satisfies the output contract.
- Keep edits or recommendations scoped to the stated owner and acceptance criteria.
- If writing files, avoid broad rewrites that are not required by the proof target.
- If recording state, prefer provider-backed ledger events and use the fallback ledger when no provider is installed.

### Phase 4 - Verification

- Run the narrowest relevant verification first.
- Add broader checks only when the touched surface or risk requires them.
- Verify generated artifacts are linked from the final report.
- If verification is impossible, state why and what would prove the result.

### Phase 5 - Final report

- Report the decision, changed artifacts, proof, ledger event, risks, and next step.
- Include enough evidence for a later agent to resume without re-reading the whole chat.

## Gates / stop conditions

- Stop if required files or user intent are unavailable.
- Stop if the output would invent authority the repo does not have.
- Stop if a human product/security/architecture decision is required.
- Stop if proof cannot be produced or explicitly marked as missing.
- Stop before remote, destructive, or credential-touching actions without consent.

## Verification requirements

- List files inspected.
- List commands run and exact result.
- List generated or changed artifacts.
- Record manual verification when automation is not available.
- Record unresolved risks instead of implying certainty.

## PlanDB / ledger events

Event shape, matching `agentrig-web/public/schema/plan-ledger-event.schema.json`:

```txt
id
type
sourceSkill
title
summary
status
links
evidence
createdAt
supersedes
```

Required by the schema:

```txt
type
sourceSkill
title
summary
status
createdAt
```

Allowed statuses:

```txt
proposed
accepted
rejected
superseded
completed
blocked
```

Use `links` for related owners, files, ADRs, tasks, PRs or receipts. Use `evidence.commands`, `evidence.files` and `evidence.urls` when available; keep any additional evidence fields durable and reviewable. Use `supersedes` as an array of event ids when replacing an earlier durable decision.

Possible event types:

```txt
project.spec.created
adr.proposed
adr.accepted
adr.superseded
task.created
task.updated
task.blocked
proof.oracle.created
proof.receipt.added
ownership.changed
duplicate.detected
hard_cut.executed
root_cause.verified
review.completed
ship_gate.completed
```

Fallback path if `plan.ledger` is unavailable:

```txt
docs/plan-ledger/events.jsonl
docs/adrs/*.md
docs/specs/*.md
```

When the `plan.ledger` provider is installed, write or import the same event payload into PlanDB. When it is unavailable, append JSON Lines to `docs/plan-ledger/events.jsonl` and keep linked ADR/spec artifacts in the fallback docs paths above.

## Optional capabilities

```txt
plan.ledger
```

Only use capabilities that are available, relevant, and justified by the current task.

## Anti-patterns

- Do not hide uncertainty behind confident prose.
- Do not add compatibility layers for internal draft shapes.
- Do not create duplicate owners for the same rule.
- Do not treat chat memory as durable project state.
- Do not use optional capabilities just because they exist.
- Do not log every chat turn.
- Do not overwrite superseded decisions; append a superseding event.

## Final report

```txt
Skill: plan-ledger
Decision:
Changed:
Proof:
Ledger:
Risks:
Next:
```
