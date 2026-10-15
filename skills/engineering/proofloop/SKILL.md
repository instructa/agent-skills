---
name: proofloop
description: Prevent unnecessary test generation in agentic coding. Use when implementing features, fixing bugs or deciding whether to add tests; select the smallest sufficient check and justify lasting test code.
---

# Proofloop

Choose the smallest sufficient check for the concrete risk. **Zero new tests is a valid,
often preferable outcome.** Agents can generate tests cheaply; execution, diagnosis, review
and maintenance still cost time. Do not treat test production as proof of progress.

This skill owns test selection and permanent-test admission. The existing workflow owns
roles, delegation, review timing, reruns and acceptance.
Use this skill with a single agent or an orchestrator. Preserve explicit user requirements
and required project checks; add no reviewer, approval stage or runner.

## Choose the evidence before generating tests

Identify the changed behavior and a meaningful failure. Check whether existing coverage
already detects it. Reuse that coverage unchanged when sufficient; adding an assertion or
file is not a mandatory deliverable.

For uncertainty about actual behavior, prefer a direct check through the runnable product's
real entry point and relevant backend. Inspect the outcome, including persistence when
relevant. Use authorized environments and data; live means a running system, not necessarily
production. A temporary command, browser interaction or diagnostic probe need not become
permanent test code. Keep useful observations in the existing task record.

Choose tests by the risk they expose, not by a fixed unit/integration/E2E pyramid. A focused
unit test may be the cheapest reliable way to check rounding or controlled faults; a real
journey may expose a wiring failure that many mocks cannot. Neither live success nor a
stronger model guarantees untested behavior. Missing live access stays an evidence gap,
not a reason to manufacture a large replacement mock suite.

## Admit lasting tests deliberately

Before adding a permanent test, identify:

- A concrete meaningful failure that existing checks do not adequately expose.
- Why repeated automated detection is worth the execution and maintenance cost.

One sentence in the existing task brief or change description is enough. No admission form,
score or extra review. A recurring regression, important invariant or hard-to-reach fault
can justify a small durable test. Preserve targeted protection for money, authorization,
concurrency and protocol boundaries. One successful live run does not replace that protection.

Do not mirror the implementation, copy its expected-value tables or expand a small fix into
a speculative family of tests. Derive expectations from the requirement or contract. Prefer
existing cases and fixtures. If mocks, helpers and tests of helpers grow around a small change,
first reconsider whether an existing command or direct check answers the question.

Read [testing.md](references/testing.md) for ambiguous admission decisions and examples.
Coverage, test counts and test-to-product line ratios are signals, never generation targets
or deletion quotas. Reassess added machinery when tools and model capabilities change, using
observed task results rather than assumed model accuracy. Useful existing tests need no
ceremonial re-proving; broad suite deletion or consolidation is separate authorized work.
