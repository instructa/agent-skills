---
name: consolidate-test-suites
description: Decide where durable test coverage belongs and clean up temporary test probes. Use while testing a bug fix or architectural change, or before finishing work that added tests, fixtures, snapshots, diagnostics, or temporary assertions. Select one owning layer, reuse canonical suites, merge unique signal, and remove task-created probe residue without disturbing pre-existing work.
---

# Consolidate Test Suites

Purpose: place each invariant in one owning test layer only.

This skill owns test placement and probe cleanup. It does not require new coverage: reusing an
existing check without editing tests is a valid outcome. Reuse any test-admission decision already
made in the task; do not add another admission review or repeat completed verification.

Definitions:
- Invariant: the rule that must stay true.
- Owning layer: the lowest layer that truly owns and can prove that rule.
- Canonical suite: the normal existing suite for that owning layer.
- Probe: temporary test code, fixture, script, snapshot, diagnostic, assertion,
  instrumentation, or helper created to investigate or reproduce one task.

Default: reuse an existing canonical suite. Do not create a new standalone regression test unless the exception rule below allows it.

Probes are useful working material, not permanent coverage by default. Before
finishing, classify every probe created for the current task as `PROMOTE`,
`MERGE`, or `DROP`.

## Hard Rules

- You MUST identify the invariant before adding or moving any test.
- You MUST identify one primary owning layer: unit, integration, or end-to-end.
- You MUST first try to place coverage in an existing canonical suite for that layer.
- You MUST prefer editing an existing test file over creating a new test file.
- You MUST NOT add the same invariant in multiple layers unless each layer covers a different failure mode. If you keep more than one layer, name the distinct failure mode for each.
- You MUST NOT add tests that lock in implementation details unless that implementation unit itself owns the invariant.
- You MUST NOT create a standalone regression test because it is faster or easier.
- If you cannot name the invariant and the owning layer, STOP. Report that placement is not justified.
- You MUST remove current-task probes that are not promoted or merged, including
  temporary code inserted into a permanent test or production file.
- You MUST preserve tests and dirty changes that predate the current task. Never
  delete or rewrite them merely to reduce test count.
- If the request is review-only, report probe dispositions and cleanup
  recommendations without modifying files.

## Required Decision Order

Choose the first option that fits:

1. Reuse existing coverage with no test-code change when it already protects the behavior.
2. Add to an existing test in an existing file in the owning layer.
3. Add a new test to an existing canonical file in the owning layer.
4. Create a new file inside the existing canonical suite in the owning layer.
5. Create a standalone regression-style test only if the Exception Rule passes.

## Owning Layer Rules

These rules select the home of durable automated coverage. They do not delay an early live check
or require converting a live observation into a permanent end-to-end test.

Choose unit when:
- one module owns the rule, and
- the bug reproduces without I/O, transport, persistence, retries, IPC, orchestration, or lifecycle coupling.

Choose integration when:
- the rule lives at a boundary between components, or
- the bug depends on serialization, persistence, ordering, replay, retries, IPC, process lifecycle, or multi-component coordination.

Choose end-to-end only when:
- the user-visible contract cannot be trusted from lower-layer tests alone.

Tie-breakers:
- If torn between unit and integration, choose integration.
- Never choose end-to-end to compensate for uncertainty.
- Never choose a higher layer just because it is easier to reproduce there.

## Exception Rule for Standalone Regression Tests

A standalone regression-style test is allowed only if ALL are true:

- no existing canonical suite can express the case cleanly
- the reproduction is deterministic
- the case has durable incident or contract value
- adding it to the canonical suite would make that suite less clear

If any condition is false, fold the coverage into the canonical suite.

## Probe Lifecycle

Use temporary probes when they materially help reproduce, diagnose, or falsify
a suspected bug. Keep their lifecycle lightweight:

1. Before editing tests, inspect the existing test-related status and diff so
   pre-existing work is distinguishable from task-created probes. Keep this
   baseline in the working context; do not create tracking files for it.
2. Once the behavior is accepted, compare each task-created probe with the
   nearest canonical suite and choose exactly one disposition:
   - `PROMOTE`: keep the smallest version because it protects a unique durable
     invariant at the stable owning boundary.
   - `MERGE`: move only its unique signal into an existing canonical test, then
     remove the redundant probe.
   - `DROP`: remove it because it is diagnostic-only, redundant, speculative,
     implementation-coupled, flaky, slow, or low-value.
3. Parameterize or extend an existing behavior test when several examples prove
   the same invariant. Test count and coverage percentage are not reasons to
   keep another test.
4. Remove every unpromoted task-created probe before final verification. If its
   ownership is uncertain, preserve it and report the uncertainty instead of
   guessing that it is safe to delete.

Promote a probe only when it is deterministic, protects an accepted observable
contract, would catch a meaningful regression, adds signal not already owned
elsewhere, and has maintenance cost proportional to its risk. When cheap and
safe, confirm that the proposed test fails against the faulty behavior and
passes against the fix; do not build extra infrastructure merely to produce
that proof.

## Duplicate Cleanup

After placing coverage:

1. Search for tests that assert the same invariant.
2. Keep the strongest owned location.
3. Merge any unique assertions into that location.
4. Delete or simplify weaker duplicates.
5. Rename tests by behavior and owner, not by ticket number or bug history.

Delete pre-existing tests only when the task includes suite consolidation or explicit requirement
retirement. Demonstrate redundancy or the retired requirement before removing them. Routine bug-fix
cleanup is limited to current-task probes.

Name the surviving check for each deletion, or the requirement explicitly retired by the task.
Assess the entire deletion group: two removed tests cannot serve as each other's protection.
Unknown coverage and similar filenames do not establish redundancy. Check history before claiming
a test repeatedly broke refactors; use the existing reviewer rather than adding a retirement review.

## Verification

Before finishing:

1. Run the narrowest relevant test target first.
2. Run required typecheck, build, or lint steps for touched code.
3. Report exactly what was run and whether it passed.

## Default Output Format

Use this format for a standalone consolidation task. During implementation, include only the
relevant decisions in the existing task record rather than creating a second report:

Invariant: <rule that failed>

Owning layer: <unit | integration | end-to-end>

Target suite/file: <path or suite name>

Action: <reuse without changes | extend existing test | add to existing suite | create file in canonical suite | keep standalone regression>

Why this layer owns it: <one short paragraph>

Duplicates to merge/delete: <list or "none">

Current-task probes: <PROMOTE / MERGE / DROP for each, or "none">

Probe cleanup completed: <removed paths or inline code, or "none">

Verification run: <commands and result>

Residual risk: <what is still not covered, if anything>
