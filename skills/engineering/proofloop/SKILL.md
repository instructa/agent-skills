---
name: proofloop
description: Verify coding changes with early live checks, justified permanent tests and bounded reruns. Use when implementing features, fixing bugs, changing tests, or reducing testing and review overhead.
---

# Proofloop

Reach a working product path early. Use the chosen agent, tools and review owner; add no model,
reviewer or approval stage. Preserve explicit user requirements and required project checks.
Use existing project tools and task records; this skill needs no runner, policy file or service.

## Exercise real behavior early

- Identify the expected behavior, concrete risks and smallest existing check in the task's brief.
  No separate policy file or report is needed.
- As soon as a runnable slice exists, exercise its real entry point and relevant backend, including
  stored outcomes. Do this before expanding test scaffolding or repeating reviews. Retain required
  security/design review and use authorized environments and data.
- Reuse commands and fixtures. Try a new or changed probe on the smallest available target before
  a long matrix or remote run. New test frameworks are separate work. Disposable prototypes and
  test assets get criteria for their experiment, not the final product.
- Record revision/build, target, expected and observed outcome, reproduction steps and relevant
  evidence in the existing task record. Screenshots or green exits alone do not prove behavior.
  If live access is unavailable, leave that verification open and use relevant existing checks;
  do not build a large mock suite to replace access.

## Justify permanent tests

New permanent tests are not a default deliverable. Before adding one, name a concrete meaningful
failure and the gap in existing checks or the selected real journey. One sentence in the existing
brief or diff is enough; no separate admission review.

Keep exploratory probes temporary by default. Preserve focused tests for money, authorization,
concurrency, protocols and controlled faults that live journeys do not adequately expose. Do not
mirror newly written code or expand one bugfix into a speculative test family.

When deciding whether to add or change tests, read [testing.md](references/testing.md). Judge
protected behavior, not filenames, coverage targets, test counts or test-to-product line ratios.
Suite consolidation is separate work; ordinary implementation does not authorize broad test deletion.

## Bound corrections

Classify failures from evidence: product defect, wrong test expectation, harness fault or environment
limitation. Unexplained failures stay unresolved. Fix the owning layer; never weaken a product
safeguard to obtain green results.

Rerun affected checks or user paths. Broaden for shared changes, new evidence or required project
checks. Use the existing reviewer when required; nonblocking follow-ups do not start another round.
After two unsuccessful attempts on the same path, stop repeating it and narrow or change the
approach. Respect stricter task limits and report unresolved criteria; spending limits never imply
acceptance.

Finish when required behavior, checks and assigned review are satisfied. Briefly report the outcome,
material gaps and existing evidence location. No extra success report or audit pass. Keep live
evidence in that record; do not wrap it in artificial tests to fit a reporter.
