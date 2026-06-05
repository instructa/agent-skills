---
name: course-checkpoint
description: Record or report the current Instructa course checkpoint after kit install, project plugin selection, spec packaging, ledger seeding, or handoff.
---

# Course Checkpoint

## Purpose

Keep the course-facing checkpoint aligned with the actual kit setup state, without moving generic engineering decisions out of core skills.

## Use when

- A user needs to know where they are in the Agentic Engineer Kit flow.
- A lesson needs proof that install, routing, spec packaging, or ledger seeding happened.
- A handoff should connect generated artifacts to the next learning step.

## Do not use when

- The task is generic architecture, review, root-cause, test ownership, or ship gating.
- The task belongs to a project plugin workflow.
- The user only wants to edit implementation code.

## Inputs needed

- Installed plugin state for `instructa.core` and `instructa.base`.
- Selected project plugin or current project type.
- Spec package artifact status.
- Ledger provider or fallback ledger status.
- Current course or lesson checkpoint name when available.

## Output contract

This skill must produce:

```txt
checkpoint name
completed kit steps
missing kit steps
linked spec/ledger artifacts
next course action
```

## Workflow

### Phase 0 - Triage

- Identify the course or kit step being checked.
- Confirm the request is about onboarding, routing, or handoff.
- Route generic engineering decisions back to core skills.

### Phase 1 - Context gathering

- Check whether `instructa.base` depends on `instructa.core`.
- Check whether `plan.ledger` is available or the fallback path is in use.
- Check whether `project-spec-packager` has produced its five required artifacts.
- Check whether `plan-ledger` has seeded durable state.
- Check whether a project plugin has been selected.

### Phase 2 - Decision

- Classify the checkpoint as not started, in progress, blocked, or complete.
- Treat missing spec package artifacts as a blocker before implementation.
- Treat missing ledger provider as a kit-flow issue, unless fallback was explicitly accepted.
- Keep project-domain work out of base and route it to the selected plugin.

### Phase 3 - Report

- Name the completed steps.
- Name the missing or blocked steps.
- Link the artifact paths that prove progress.
- Give one next command or skill to run.

## Gates / stop conditions

- Stop if there is no enough context to identify the course or kit step.
- Stop if the next step would require provider configuration without consent.
- Stop if a project plugin decision is needed before continuing.

## Verification requirements

- Confirm dependency direction: base depends on core.
- Confirm `plan.ledger` required capability or fallback ledger.
- Confirm the spec package and ledger seed state.
- Confirm the selected project plugin when known.

## Final report

```txt
Skill: course-checkpoint
Checkpoint:
Completed:
Blocked:
Artifacts:
Ledger:
Next:
```
