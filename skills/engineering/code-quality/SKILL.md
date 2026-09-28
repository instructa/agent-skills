---
name: code-quality
description: Apply focused code-quality checks when implementing or reviewing behavioral changes. Use for maintainability, framework fit, data safety and meaningful verification; not visual design or a full security audit.
---

# Code quality

Apply only the checks relevant to the change. Stay within the requested scope. A review does not authorize fixes. Do not start extra agents, install tooling or run a full audit merely because this skill is loaded.

- **Read before inventing.** Find the existing owner, contract and a comparable implementation. Reuse host guards, SDK ports, components and framework mechanisms. Do not copy host internals, bypass types or add parallel state/version machinery to avoid learning the existing path. Extend the canonical contract only when a real capability is missing.
- **Keep complexity earned.** Prefer explicit types, names and control flow. Separate provider details from shared policy. Add an abstraction when it removes demonstrated duplication or isolates a real boundary, not to anticipate hypothetical reuse. Inspect unexpected core changes, dependencies and build fixes separately from the feature.
- **Protect the lifecycle.** For persistent writes, check relevant sequences, not just endpoints: lost response → same retry; changed payload → same identity; create → delete → old retry; concurrent edits. Assert resulting values, not just success or row counts. A clean conflict is valid; false success, duplicates and silent loss are not. Preserve durable deletion/replay semantics where the contract requires them.
- **Respect async ownership.** A late response must not erase newer input or update the wrong screen/session. Cancellation, navigation, disconnect and timeout must leave a defined state. Resource cleanup must not depend on the event that a leaked resource itself prevents.
- **Keep failure visible.** Follow the framework's error contract. Typed failure results are valid when every consumer handles them; exceptions are not automatically better. Do not silently report rejected work as saved/completed or hide permission denials, fallback behavior or truncated results.
- **Verify the actual boundary.** Use the repo's configured lint, typecheck, build and targeted behavioral checks. For a real defect, add a regression at its owning layer. Mocks must match the host contract; they do not prove host integration. UI lifetime bugs need interaction checks, packaging claims need the installed artifact. Do not add tests that merely mirror implementation or exhaustive suites for trivial edits.

Report actionable findings with file/line, trigger, consequence and evidence. Separate reproduced defects, source-level risks and untested cases. State checks actually run and remaining blockers. Lint scores, component counts, lines and passing-test totals are diagnostics, not quality grades or release approval. Keep the report short; omit unaffected checklist items.
