---
name: api-project-workflow
description: Plan, implement, review, and verify APIs, backend services, workers, webhook handlers, and integration services.
---

# API Project Workflow

## Purpose

Ship backend and integration work with explicit contracts, durable planning, secure configuration, dependency proof, and service-level verification.

## Use when

- the project is a headless API, backend service, worker, webhook handler, queue consumer, scheduled job, or integration service
- the work changes request/response contracts, schemas, auth boundaries, idempotency, retries, external APIs, or background behavior
- the slice needs PlanDB context, current external docs, secret review, or dependency/security proof

## Do not use when

- the primary deliverable is a browser UI, marketing site, desktop app, or MCP server
- the API work is one piece of a broader SaaS lifecycle change with users, billing, teams, or product operations
- the task is only a local script or shell change better handled by a narrower skill

## Inputs needed

- accepted spec, PlanDB task or fallback ledger context, and proof oracle
- API routes, handlers, service modules, schemas, clients, adapters, migrations, jobs, tests, and config
- external API docs, SDK versions, auth scopes, rate limits, idempotency rules, and webhook signatures when relevant
- package manifests, lockfiles, env var names, and secret-bearing config surfaces

## Output contract

This skill must produce:

```txt
api scope decision
contract and ownership map
implementation or review plan
ledger receipt
service verification proof
secrets and supply-chain proof
handoff
```

## Workflow

### Phase 0 - Triage

- Confirm the work is API/backend scope and not SaaS, webapp, desktop, or MCP scope.
- Read the current PlanDB task or fallback ledger before changing code.
- Identify the contract owner: public API, internal service, adapter, job, schema, or generated client.
- Name compatibility expectations for shipped public APIs separately from internal draft contracts.

### Phase 1 - Context gathering

- Read the route/handler, schema, service, adapter, config, and test files that own the contract.
- Inspect existing validation, serialization, error shape, auth, logging, tracing, retry, and idempotency patterns.
- Use `docs.latest` only for current external protocol, provider, SDK, cloud, database, or framework behavior.
- Identify secret and dependency surfaces before verification.

### Phase 2 - API analysis

- Define the canonical request, response, error, event, or job payload shape.
- Check validation at the boundary and typed internal data after validation.
- Check auth and permission boundaries, including machine-to-machine and webhook scenarios.
- Check idempotency, retries, timeouts, cancellation, backpressure, pagination, and rate limiting.
- Check observability: structured logs, correlation IDs, metrics, traces, and safe redaction.
- Decide whether compatibility is a real external contract or only internal draft state.

### Phase 3 - Action / artifact

- Implement or review the smallest contract change that satisfies the proof oracle.
- Keep provider-specific behavior inside adapter boundaries and canonical product/service policy in the API owner.
- Update schemas, generated types, tests, docs, and clients together when they are part of the same contract.
- Record ledger events when contract decisions or proof receipts change durable project state.

### Phase 4 - Verification

- Run focused unit, integration, contract, schema, or smoke tests at the owning layer.
- Exercise success, validation failure, auth failure, external failure, retry, and idempotency paths when touched.
- Run `secrets.scan` proof for config, logs, fixtures, docs, and generated outputs.
- Run `supplychain.scan` proof when package manifests, lockfiles, install scripts, or dependency surfaces changed.
- Use optional observability, preview, or remote repo context only when it proves the API change.

### Phase 5 - Final report

- Report the contract owner, canonical shape, changed files, tests, ledger receipt, security proof, and residual risks.
- State whether any public compatibility boundary remains and why.
- Name any human decision needed for API versioning, auth scopes, retention, rate limits, or rollout.

## Gates / stop conditions

- Stop if PlanDB or fallback ledger context is unavailable for a contract or integration change.
- Stop before changing public API compatibility, auth scopes, secrets, production integrations, or destructive jobs without approval.
- Stop if external provider behavior is unknown and current docs are required but unavailable.
- Stop if required security proof cannot be run or manually substituted.

## Verification requirements

- Files inspected and changed.
- PlanDB or fallback ledger event/receipt.
- Commands run and exact result.
- Contract tests, integration tests, or smoke proof.
- Secrets scan and supply-chain scan result or documented manual substitute.
- Remaining compatibility or rollout risk.

## Capability use

Required by the plugin:

```txt
plan.ledger
docs.latest
secrets.scan
supplychain.scan
```

Optional when installed and relevant:

```txt
repo.remote
observability.logs
deploy.preview
```

Do not create capability IDs for REST, GraphQL, webhooks, databases, queues, or auth. Those are API workflow contexts.

## Anti-patterns

- Do not parse untrusted payloads with ad hoc string logic when structured validation exists.
- Do not hide provider quirks in domain policy or expose domain policy as adapter behavior.
- Do not add compatibility for internal draft shapes unless there is a real external contract.
- Do not log secrets, tokens, full payloads, or personally sensitive data as debugging convenience.
- Do not mark an API change complete without exercising the boundary that changed.

## Final report

```txt
Skill: api-project-workflow
Decision:
Changed:
Ledger:
Proof:
Security:
Risks:
Next:
```
