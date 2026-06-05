---
name: webapp-project-workflow
description: Plan, implement, review, and verify interactive web apps, dashboards, and internal tools that are not full SaaS products.
---

# Webapp Project Workflow

## Purpose

Ship an interactive web application slice with clear route ownership, state boundaries, accessible UI behavior, focused tests, and browser proof.

## Use when

- the project is an interactive UI, dashboard, admin tool, editor, calculator, workflow tool, or internal app
- the main risk is user flow, state, data loading, forms, component behavior, or browser-visible correctness
- the app does not yet require SaaS lifecycle concerns such as billing, teams, background jobs, account operations, or production operations

## Do not use when

- the work is only a static marketing or content site
- the product scope includes billing, teams, account lifecycle, jobs, webhooks, or production operations
- the primary deliverable is a headless API, desktop app, or MCP server

## Inputs needed

- user goal, target role, primary task, data source, and acceptance criteria
- repo routing model, component model, state management, data loading, validation, tests, and styling conventions
- current failing behavior, screenshots, logs, or reproduction path when debugging
- target browser path and expected UI state for verification

## Output contract

This skill must produce:

```txt
webapp scope decision
route/state ownership map
implementation or review plan
test and browser proof
residual risks
handoff
```

## Workflow

### Phase 0 - Triage

- Confirm the project is a webapp rather than website, SaaS, API, desktop, or MCP.
- Identify the user-visible workflow and the smallest route or component owner.
- Name the data and state boundaries: URL state, server state, local form state, derived UI state, and persisted state.
- Decide whether PlanDB context is needed; it is optional for webapps and should be used only when the slice needs durable task state.

### Phase 1 - Context gathering

- Read the route, component, data loader, mutation, validation, and test files that own the behavior.
- Follow existing repo conventions for routing, data fetching, styling, accessibility, and tests.
- Use `docs.latest` only when external framework, library, browser API, or platform behavior needs current evidence.
- Prepare a browser verification path with initial state, actions, expected state, and cleanup needs.

### Phase 2 - Webapp analysis

- Separate domain state from presentation state and avoid duplicate sources of truth.
- Identify loading, empty, error, permission, optimistic, and stale-data states affected by the work.
- Check form validation, disabled states, keyboard path, focus restoration, aria names, and destructive-action confirmation.
- Check component boundaries: avoid broad shared abstractions unless repeated behavior already exists.
- Check route-level behavior before optimizing isolated components.

### Phase 3 - Action / artifact

- Make the smallest implementation, review, or plan artifact that satisfies the acceptance criteria.
- Keep state ownership explicit and local to the route or domain owner that already controls the behavior.
- Add focused tests around state transitions, validation, and regressions.
- Use remote repo context only when branch, PR, issue, or CI state affects the decision.

### Phase 4 - Verification

- Run the narrowest relevant unit, component, integration, or type checks.
- Use `browser.verify` for the route and user action path when UI behavior changed.
- Verify keyboard and pointer paths for interactive controls.
- Verify loading, empty, error, and success states when touched.
- Record any untested external states as residual risk rather than implying proof.

### Phase 5 - Final report

- Report the workflow, state owner, files changed, checks run, browser proof, and remaining risks.
- Mention whether PlanDB or remote repo context was used.
- Name any user decisions still needed, such as product copy, permissions, data retention, or production rollout.

## Gates / stop conditions

- Stop if the work becomes SaaS lifecycle scope and switch to `saas-project-workflow`.
- Stop before mutating real user data, production accounts, or payment-like flows without explicit approval.
- Stop if browser verification requires credentials or test data the user has not provided.
- Stop if the route owner is unclear and multiple modules could become competing sources of truth.

## Verification requirements

- Files inspected and changed.
- Commands run and exact result.
- Browser path, actions, expected result, and actual result.
- State ownership decision and remaining unverified states.

## Capability use

Required by the plugin:

```txt
docs.latest
browser.verify
```

Optional when installed and relevant:

```txt
plan.ledger
repo.remote
```

Do not create local capability IDs for frontend docs, state management, forms, or accessibility. Those are webapp workflow concerns.

## Anti-patterns

- Do not keep two stores for the same UI or domain state.
- Do not add generic component frameworks for one route-level behavior.
- Do not skip browser verification after changing visible interactions.
- Do not promote a simple app to SaaS scope unless lifecycle concerns are present.
- Do not use optional capabilities without a concrete decision they support.

## Final report

```txt
Skill: webapp-project-workflow
Decision:
Changed:
Proof:
Browser:
Risks:
Next:
```
