# instructa-doctor-routing

Purpose: route the user through the kit-entry workflow without duplicating core skill logic.

Run order:

1. Verify `instructa.core` and `instructa.base` are installed.
2. Check the required `plan.ledger` provider or fallback path.
3. Run `project-spec-packager` when the spec package is missing.
4. Run `plan-ledger` to seed durable state.
5. Continue with `instructa-doctor-routing` for the next kit step.

Fallback ledger: `docs/plan-ledger/events.jsonl`.
