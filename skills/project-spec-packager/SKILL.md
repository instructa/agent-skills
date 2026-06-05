---
name: project-spec-packager
description: Package a project idea or messy implementation request into a durable spec, proof oracle, ADR candidates, task seed, and agent handoff before coding starts.
aliases:
  - app-spec-packager
---

# Project Spec Packager

## Purpose

Turn product intent into a small, durable project package that prevents implementation drift before agents start editing code.

## Use when

- starting a new project or major slice
- turning ambiguous product intent into agent-ready artifacts
- capturing proof criteria before implementation
- seeding a planning ledger from a spec package

## Do not use when

- the user only wants a small code edit
- the project already has a current accepted spec and proof oracle for this slice
- the request is only to run tests or review an existing diff

## Inputs needed

- repo state and active branch
- user request and acceptance criteria
- relevant files, diffs, docs, ADRs, or manifests
- known constraints, non-goals, and risk boundaries
- optional capability context when justified

## Output contract

This skill must produce:

```txt
docs/specs/project-spec.md
docs/specs/proof-oracle.md
docs/adrs/ADR-candidates.md
docs/plan-ledger/seed.json
docs/handoffs/agent-handoff.md
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

- Analyze product or app intent.
- Analyze target user or operator.
- Analyze primary workflows.
- Analyze non-goals.
- Analyze project type.
- Analyze ownership map.
- Analyze data and state assumptions.
- Analyze external dependencies.
- Analyze agent constraints.
- Analyze proof oracle.
- Analyze initial ADR candidates.
- Analyze initial ledger units.
- Analyze review and ship gates.
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

Possible event types:

```txt
project.spec.created
proof.oracle.created
adr.proposed
task.created
```

Fallback path if `plan.ledger` is unavailable:

```txt
docs/plan-ledger/events.jsonl
docs/adrs/*.md
docs/specs/*.md
```

## Optional capabilities

```txt
plan.ledger
docs.latest
```

Only use capabilities that are available, relevant, and justified by the current task.

## Anti-patterns

- Do not hide uncertainty behind confident prose.
- Do not add compatibility layers for internal draft shapes.
- Do not create duplicate owners for the same rule.
- Do not treat chat memory as durable project state.
- Do not use optional capabilities just because they exist.
- Do not produce timelines, staffing plans, or story points unless explicitly requested.
- Do not start implementation before the proof oracle exists.

## Final report

```txt
Skill: project-spec-packager
Decision:
Changed:
Proof:
Ledger:
Risks:
Next:
```
