# PlanDB Smoke Test

1. Confirm the plugin manifest validates against `plugin.v1.json`.
2. Run `agentrig doctor --capability plan.ledger` from a project with PlanDB configured.
3. Confirm doctor reports `third-party.plandb` as the provider for `plan.ledger`.
4. Create or read a non-destructive test ledger event in the project-local PlanDB store.
5. Confirm fallback paths are documented: `docs/plan-ledger/events.jsonl`, `docs/adrs/*.md`, `docs/specs/*.md`.
