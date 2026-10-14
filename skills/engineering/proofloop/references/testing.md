# Decide whether a permanent test is needed

Assess assertions, not file extensions. A `node:test` file driving real CLI processes or restarting
a Worker is a system check. A browser test mocking every meaningful boundary may add little
confidence. Prefer the least expensive check that exposes the actual risk.

## Admission

Before a permanent addition, explain the failure it catches and the gap in existing checks. Reuse
or extend an existing case before building another fixture or suite. A reproduced bug or a concrete
high-risk case can justify a focused regression test; no mutation campaign or new reviewer is needed.

| Situation | Action |
| --- | --- |
| Temporary probe used to diagnose a failure | Keep the relevant observation in the task record; do not promote the probe automatically |
| Existing check already catches the same failure | Extend or reuse it; avoid a second assertion of the same outcome |
| Real journey misses a relevant state combination or controlled fault | Keep the smallest focused test that exercises that gap |
| Product behavior intentionally changed | Update the affected expectation to the agreed contract and run that check |

Look for copied lookup tables, incidental text, private call ordering, broad snapshots and fixed
catalog counts that fail on legitimate additions before reaching their useful assertions. Prefer
the required observable property. Exact values remain appropriate when they are the product
contract, such as a protocol representation or security allowlist; do not relax them by category.

Tests of a newly invented test helper can create more maintenance than the feature. First ask
whether an existing command or direct observation removes the need for the helper. If a verifier
protects a real boundary, test it locally before an expensive run; do not grow a framework around it.

## Scope

This decision adds no separate test-placement or cleanup review. Reuse the project's normal suite
and cleanup workflow when test changes are justified. Existing useful tests need no ceremonial
re-proving merely to stay. Test counts, coverage percentages and line ratios are diagnostic
signals, never admission or deletion quotas. A successful live check alone does not justify deleting
existing tests; update expectations only for the agreed behavior change and preserve unrelated work.
