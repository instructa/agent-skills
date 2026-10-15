# Choosing sufficient evidence

Assess protected behavior, not extensions. `node:test` driving real CLI processes can be a
system check; browser tests mocking meaningful boundaries may offer little integration
evidence. Minimize cost of exposing the named risk, including execution, diagnosis and future
maintenance, not generation alone.

| Situation | Decision |
| --- | --- |
| Existing check catches relevant failure | Run or reuse unchanged; zero new tests |
| One-time save/reload uncertainty | Exercise real save/reload; inspect stored outcomes; retain observation, not automatically probe |
| Journey misses recurring rounding or authorization regression | Add smallest focused case to existing suite |
| Rare race, retry or partial-write fault impractical live | Controlled focused invariant test |
| Product contract intentionally changed | Update affected expectation from contract; preserve unrelated assertions |
| Minor change needs many mocks/helper tests | Reconsider test boundary; reuse tooling before expanding infrastructure |

Reproduced bugs justify regression tests through useful future detection, not automatic files
per bug. Critical faults need not have occurred to warrant protection. Promote temporary
probes only for clear unique recurring value.

Copied lookup tables, private call order, incidental wording, broad snapshots and fixed catalog
counts can reject legitimate changes while missing defects. Assert externally required
properties. Preserve exact values required by contracts, including serialization, security
allowlists and financial outputs; never weaken them merely to pass.

For failed checks, establish whether expectations match the agreed contract and whether the
fault belongs to product, test or environment. Unexplained reds remain unresolved. Never alter
correct product behavior for invented expectations or relax safeguards for green results.
Leave correction rounds to the existing workflow.

Small changes may need only existing checks and a temporary live probe; small high-risk changes
may need several focused cases. Size alone decides neither. No fixed test quota, mandatory
mutation campaign or extra reviewer.
