---
name: ship-gate
description: Make the final ship/no-ship decision using spec, ledger, review receipts, test proof, security proof, docs state, and release risks.
---

# Ship Gate

## Purpose

Prevent unfinished or unproven work from being called done when review, tests, security, docs, or ownership state is missing.

## Use when

- the user says work is done or ready to ship
- preparing a PR, release, merge, or handoff
- checking whether review findings and proof receipts are complete

## Do not use when

- the project has not reached reviewable implementation
- the user only wants a local code edit
- no proof commands or manual verification can be produced

## Inputs needed

- repo state and active branch
- user request and acceptance criteria
- relevant files, diffs, docs, ADRs, or manifests
- known constraints, non-goals, and risk boundaries
- optional capability context when justified

## Output contract

This skill must produce:

```txt
ship decision
required proof checklist
blocking risks
accepted residual risks
release or handoff note
ship receipt
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

- Analyze spec alignment.
- Analyze ledger state.
- Analyze review state.
- Analyze test state.
- Analyze security state.
- Analyze docs state.
- Analyze rollback or handoff.
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

Primary event emitted when the ship gate completes:

```txt
ship_gate.completed
```

Possible event types:

```txt
ship_gate.completed
review.completed
proof.receipt.added
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
repo.remote
secrets.scan
supplychain.scan
shell.lint
```

Only use capabilities that are available, relevant, and justified by the current task.

## Anti-patterns

- Do not hide uncertainty behind confident prose.
- Do not add compatibility layers for internal draft shapes.
- Do not create duplicate owners for the same rule.
- Do not treat chat memory as durable project state.
- Do not use optional capabilities just because they exist.
- Do not mark work done with unresolved blocking review findings.
- Do not treat absence of CI as proof.

## Final report

```txt
Skill: ship-gate
Decision:
Changed:
Proof:
Ledger:
Risks:
Next:
```
