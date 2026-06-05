---
name: root-cause-finder
description: Trace expected behavior to the first unintended side effect before changing contracts, parsing, types, schemas, null handling, or downstream guards.
---

# Root Cause Finder

## Purpose

Stop symptom fixes by proving whether the payload, request, mutation, or side effect should have existed at all.

## Use when

- debugging protocol errors, null payloads, missing fields, hydration bugs, state ownership bugs, background writes, or restore issues
- reviewing a patch that changes a contract to accept surprising data
- finding the first unintended write in a causal chain

## Do not use when

- the failure is already proven to be an isolated local typo
- the user asks only for a broad code review
- the correct fix is purely test placement

## Inputs needed

- repo state and active branch
- user request and acceptance criteria
- relevant files, diffs, docs, ADRs, or manifests
- known constraints, non-goals, and risk boundaries
- optional capability context when justified

## Output contract

This skill must produce:

```txt
expected behavior
invariant
causal chain
first unintended side effect
root cause
minimal fix
architectural follow-up
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

- Analyze trigger event.
- Analyze call path.
- Analyze should-have-happened decision.
- Analyze state owners.
- Analyze hidden writes.
- Analyze symptom versus cause.
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

Primary event emitted when the finding is durable:

```txt
root_cause.verified
```

Possible event types:

```txt
root_cause.verified
proof.receipt.added
task.updated
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
- Do not make a contract more permissive until the observed payload is proven intended.
- Do not stop at the first downstream parser or type error.

## Final report

```txt
Skill: root-cause-finder
Decision:
Changed:
Proof:
Ledger:
Risks:
Next:
```
