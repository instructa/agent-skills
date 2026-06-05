---
name: saas-project-workflow
description: Plan, implement, review, and verify SaaS product slices involving users, data, auth, billing, teams, jobs, webhooks, or operations.
---

# SaaS Project Workflow

## Purpose

Ship SaaS product work with durable planning, explicit domain ownership, secure data handling, browser proof, and release-quality security checks.

## Use when

- the project has users, accounts, auth, permissions, billing, teams, subscriptions, webhooks, background jobs, data retention, or production operations
- the work affects product lifecycle, customer data, tenant boundaries, secrets, dependencies, or browser-visible product flows
- the slice needs durable planning and proof before implementation proceeds

## Do not use when

- the project is only a marketing site, simple interactive webapp, headless API, desktop app, or MCP server
- auth, payments, or database work is only documentation research outside a product implementation
- the user asks for a narrow local edit that does not touch product lifecycle, data, security, or release risk

## Inputs needed

- accepted spec, proof oracle, PlanDB task or fallback ledger context
- user roles, tenant/account model, data ownership, permissions, billing or job/webhook requirements
- repo architecture, routes, API boundaries, schema/migration model, background workers, config, tests, and deployment notes
- security-sensitive files, env var names, package manifests, lockfiles, and external service docs when relevant
- browser verification path and safe test data

## Output contract

This skill must produce:

```txt
saas scope decision
ownership and data-boundary map
implementation or review plan
ledger receipt
browser proof when UI changed
secrets and supply-chain proof
release risks and handoff
```

## Workflow

### Phase 0 - Triage

- Confirm the task is SaaS scope and name the lifecycle concern it touches.
- Read the current PlanDB task or fallback ledger before changing code.
- Identify runtime owner, first fix owner, canonical long-term owner, and wrong competing owners.
- Name the customer data, tenant boundary, secret, package, or operational surface affected by the work.

### Phase 1 - Context gathering

- Read the narrow set of route, service, schema, job, webhook, auth, billing, config, and test files that own the behavior.
- Use `docs.latest` for current external docs only when integration behavior, SDKs, billing APIs, auth libraries, or platform limits matter.
- Confirm safe test accounts or fixtures before browser verification.
- Capture dependency and secret-scan scope before running security proof.

### Phase 2 - SaaS analysis

- Separate product policy from adapter behavior; third-party services do not own product rules.
- Map data ownership: tenant/account/user/entity, source of truth, migration, validation, retention, and deletion behavior.
- Map permissions: who can read, write, administer, invite, bill, cancel, retry, or export.
- Map billing, jobs, and webhooks as state machines with idempotency, retries, observability, and failure recovery.
- Check secrets handling, env var boundaries, package risk, and accidental exposure in logs, client bundles, fixtures, and docs.
- Decide which tests prove the invariant closest to its owner.

### Phase 3 - Action / artifact

- Implement or review the smallest product slice that satisfies the accepted proof oracle.
- Keep domain rules in the product/application owner and vendor-specific behavior in adapters.
- Update ledger state when durable product decisions or proof receipts change.
- Add or adjust tests at the owning layer; avoid duplicate weaker tests in unrelated layers.

### Phase 4 - Verification

- Run focused tests for the changed route, service, schema, job, webhook, or billing flow.
- Use `browser.verify` for changed user-facing flows with safe test data.
- Run `secrets.scan` proof for changed config, env, docs, logs, fixtures, and generated files.
- Run `supplychain.scan` proof when package manifests, lockfiles, install scripts, or dependency surfaces changed.
- Record observability or deploy preview proof only when those optional capabilities are available and relevant.

### Phase 5 - Final report

- Report the product scope, ownership decision, ledger receipt, tests, browser proof, security proof, and residual release risks.
- State clearly when external docs were used and which behavior they informed.
- Name any human decisions needed for pricing, legal, privacy, retention, customer communication, or rollout.

## Gates / stop conditions

- Stop if PlanDB or fallback ledger context is unavailable for a product lifecycle change.
- Stop before touching production accounts, real customer data, payment systems, or secrets without explicit approval.
- Stop if tenant/account ownership is ambiguous and a code change would encode the wrong policy.
- Stop if required security proof cannot be run or manually substituted.

## Verification requirements

- Files inspected and changed.
- PlanDB or fallback ledger event/receipt.
- Commands run and exact result.
- Browser path and safe test data when UI changed.
- Secrets scan and supply-chain scan result or documented manual substitute.
- Release risks and unresolved human decisions.

## Capability use

Required by the plugin:

```txt
plan.ledger
docs.latest
browser.verify
secrets.scan
supplychain.scan
```

Optional when installed and relevant:

```txt
repo.remote
deploy.preview
observability.logs
```

Auth, payments, database, jobs, teams, webhooks, and tenancy are SaaS workflow contexts. Do not define them as capability IDs.

## Anti-patterns

- Do not put cross-provider product policy inside SDK adapters.
- Do not change auth, billing, tenancy, or retention without naming the canonical owner.
- Do not skip security scans after changing config, env, dependencies, logs, or generated files.
- Do not use browser automation against production data unless the user explicitly approved the target and data.
- Do not treat optional observability or preview data as required when the task can be proven locally.

## Final report

```txt
Skill: saas-project-workflow
Decision:
Changed:
Ledger:
Proof:
Security:
Browser:
Risks:
Next:
```
