# third-party.plandb

Curated AgentRig wrapper for the `plan.ledger` capability.

This plugin describes PlanDB as the default provider for durable project planning and receipt state. It does not fork, vendor or own PlanDB. AgentRig owns only the wrapper manifest, provider rules and verification checklist.

## Capability

- `plan.ledger` -> local PlanDB task graph/ledger tooling

## Upstream

- Owner/source: PlanDB project and repository-local PlanDB tooling
- Install method: use the project's existing PlanDB setup, then run `agentrig doctor --capability plan.ledger`
- Provider targets: `codex`, `claude-code`, `cursor`
- Required env: none
- Optional env: `PLANDB_DB_PATH`

## Permissions

- Filesystem: project-local PlanDB database and fallback files under `docs/plan-ledger`, `docs/adrs` and `docs/specs`
- Network: none required by this wrapper
- Local code: yes, through the installed PlanDB tooling
- Approval: durable planning writes require human-visible intent

## Fallback

If PlanDB is unavailable, use:

- `docs/plan-ledger/events.jsonl`
- `docs/adrs/*.md`
- `docs/specs/*.md`

## Verification

Smoke test: `verify/plandb-smoke.md`
