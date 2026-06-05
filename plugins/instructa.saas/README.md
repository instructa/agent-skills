# Instructa SaaS Project

Project workflow layer for SaaS products with users, data, billing, teams, jobs, webhooks and production operations.

`instructa.saas` depends on `instructa.base`; it coordinates the domain workflow and declares provider-backed requirements for planning, docs, browser proof and security checks.

## Included Skills

- `saas-project-workflow`

## Required Capabilities

- `plan.ledger` from `third-party.plandb`
- `docs.latest` from `third-party.context7`
- `browser.verify` from `third-party.playwright-mcp`
- `secrets.scan` from `third-party.local-scanners`
- `supplychain.scan` from `third-party.local-scanners`

## Optional Capabilities

- `repo.remote`
- `deploy.preview`
- `observability.logs`

## Workflow Boundary

Use this plugin when product lifecycle, account data, security, billing, background work or operational proof are part of the implementation. Do not model auth, billing or database concerns as capabilities; they are SaaS workflow contexts that may use `docs.latest` and security capabilities when needed.
