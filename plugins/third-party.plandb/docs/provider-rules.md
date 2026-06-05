# Provider Rules

## Ownership

`third-party.plandb` is a curated wrapper manifest. It does not own PlanDB behavior, task semantics or cross-provider product policy.

## Usage Rules

- Use only for the canonical `plan.ledger` capability.
- Persist durable ledger events only when the user or project workflow has made the planning intent clear.
- Keep PlanDB events project-scoped; do not write global planning state from this provider.
- If the provider is unavailable, write the canonical fallback files instead of inventing a second ledger format.

## Security Rules

- Show the exact command before running PlanDB tooling.
- Require explicit consent before any operation that creates, mutates or deletes durable planning records.
- Do not request network access for this wrapper unless the upstream PlanDB installation explicitly requires it and the user approves.
- Treat local database paths as project data.
