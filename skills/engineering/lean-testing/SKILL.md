---
name: lean-testing
description: Prevent unnecessary test generation in agentic coding. Use when implementing features, fixing bugs or deciding whether to add tests; select the smallest sufficient check and justify lasting test code.
---

# Lean Testing

Choose the smallest sufficient check for the concrete risk. **Zero new tests is valid, often
preferable.** Cheap generation does not remove execution, diagnosis, review or maintenance
costs. Test production is not proof of progress.

Own test selection and permanent-test admission; leave roles, delegation, review timing,
reruns and acceptance to the existing workflow. Works with single agents or orchestrators.
Preserve explicit user requirements and required project checks. Add no reviewer, approval
stage or runner.

## Select evidence before generating tests

Identify changed behavior and a meaningful failure. Reuse existing coverage unchanged when
sufficient; new assertions or files are not mandatory deliverables.

For behavioral uncertainty, prefer checking the runnable product's real entry point and
relevant backend. Inspect outcomes, including relevant persistence. Use authorized environments
and data; live means running, not necessarily production. Commands, browser interactions and
diagnostic probes may remain temporary. Keep useful observations in the existing task record.

Assess protected behavior, not filenames or a fixed unit/integration/E2E pyramid.
`node:test` driving real CLI processes can be a system check; browser tests mocking meaningful
boundaries may offer little integration evidence. Focused unit tests may check
rounding or controlled faults most cheaply; real journeys may expose wiring failures mocks
miss. Neither live success nor stronger models guarantee untested behavior. Missing live access
remains an evidence gap; do not manufacture a large replacement mock suite.

## Justify permanent tests

Before adding one, identify a meaningful failure existing checks inadequately expose and why
repeated automated detection warrants execution and maintenance costs. One sentence in the
existing brief or change description suffices. No admission form, score or extra review.

Recurring regressions, important invariants and hard-to-reach faults can justify small durable
tests. Preserve targeted money, authorization, concurrency and protocol protection; one live
pass does not replace it. Critical faults need not have occurred to warrant protection.
Reproduced bugs warrant useful future detection, not automatic files per bug. Promote temporary
probes only for clear unique recurring value.

Derive expectations from requirements or contracts. Do not mirror implementation, copy its
expected-value tables or expand small fixes into speculative test families. Prefer existing
cases and fixtures. When mocks, helpers and helper tests grow around a small change, first
reconsider whether an existing command or direct check answers the question.

Assert externally required properties. Private call order, incidental wording, broad snapshots
and fixed catalog counts can reject legitimate changes while missing defects. Preserve exact
contract values, including serialization, security allowlists and financial outputs.

| Situation | Decision |
| --- | --- |
| One-time save/reload uncertainty | Exercise real save/reload; inspect stored outcomes; retain observation, not automatically probe |
| Rare race, retry or partial-write fault impractical live | Controlled focused invariant test |
| Product contract intentionally changed | Update affected expectation from contract; preserve unrelated assertions |

For failed checks, establish whether expectations match the agreed contract and whether the
fault belongs to product, test or environment. Unexplained reds remain unresolved. Never alter
correct product behavior for invented expectations or weaken safeguards or contract values
merely to pass.

Small changes may need only existing checks and a temporary live probe; small high-risk changes
may need several focused cases. Size alone decides neither. No mandatory mutation campaign.
Coverage, test counts and test-to-product line ratios are signals, never generation targets
or deletion quotas. Reassess machinery as tools and models change using observed task results,
not assumed model accuracy. Useful existing tests need no ceremonial re-proving. Broad suite
deletion or consolidation requires separate authorization.
