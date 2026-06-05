# Instructa API Project

Project workflow layer for APIs, backend services, workers and integration services.

`instructa.api` depends on `instructa.base`; it keeps API contracts, data boundaries and verification in the project domain layer while security and docs capabilities resolve through provider plugins.

## Included Skills

- `api-project-workflow`
- `go-local-health` (support skill for Go API/runtime health checks)

## Required Capabilities

- `plan.ledger` from `third-party.plandb`
- `docs.latest` from `third-party.context7`
- `secrets.scan` from `third-party.local-scanners`
- `supplychain.scan` from `third-party.local-scanners`

## Optional Capabilities

- `repo.remote`
- `observability.logs`
- `deploy.preview`

## Workflow Boundary

Use this plugin for headless APIs, backend workers, webhook handlers and integration services. `go-local-health` lives here as API/runtime-context support for Go services, not as a core workflow surface. Use `instructa.mcp` for MCP protocol/tool-server work and `instructa.saas` when the API is only one slice of a user-facing product lifecycle.
