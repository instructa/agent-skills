# Choosing sufficient evidence

Assess protected behavior, not file extensions. A `node:test` case driving real CLI processes
can be a system check; a browser test mocking every meaningful boundary may offer little
integration evidence. Choose the least costly method that exposes the named risk, including
execution, diagnosis and future maintenance rather than generation cost alone.

| Situation | Decision |
| --- | --- |
| Existing check catches the relevant failure | Run or reuse it unchanged; zero new tests |
| One-time uncertainty about save/reload behavior | Exercise the real save and reload path and inspect stored outcomes; keep the observation, not automatically the probe |
| Existing journey misses a recurring rounding or authorization regression | Add the smallest focused case to an existing suite |
| Rare race, retry or partial-write fault is impractical to reproduce live | Use a controlled focused test for the invariant |
| Product contract intentionally changed | Update the affected expectation from that contract; preserve unrelated assertions |
| Many mocks and helper tests are needed for a minor change | Reconsider the test boundary and reuse existing tooling before expanding infrastructure |

A reproduced bug supports a regression test when it supplies useful future detection, not
an automatic new file per bug. A critical fault need not have occurred already to justify
protection. Temporary probes become permanent only when their unique recurring value is clear.

Copied lookup tables, private call order, incidental wording, broad snapshots and fixed catalog
counts can fail on legitimate changes while missing the real defect. Assert the externally
required property. Exact values remain appropriate for actual contracts such as serialization,
security allowlists or financial outputs; do not weaken them merely to make a test pass.

When a check fails, establish whether the expectation comes from the agreed contract and
whether the failure belongs to the product, test or environment. An unexplained red result
is unresolved. Do not repair correct product behavior to satisfy an invented expectation,
or relax a safeguard to obtain green. Correction rounds remain the existing workflow's job.

A small change may legitimately finish with existing checks and one temporary live probe.
A small high-risk change may need several focused cases. Size alone decides neither outcome.
No fixed test quota, mandatory mutation campaign or extra reviewer is implied.
