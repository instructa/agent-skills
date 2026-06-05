---
name: website-project-workflow
description: Plan, build, review, and verify marketing, content, documentation, landing, and blog sites without turning them into app or SaaS workflows.
---

# Website Project Workflow

## Purpose

Ship a public-facing website slice with clear information architecture, strong copy, accessible implementation, performance awareness, and browser proof.

## Use when

- the project is a marketing, content, documentation, landing, blog, portfolio, or campaign site
- the main user action is reading, navigating, signing up, contacting, or following a call to action
- the work needs browser verification, accessibility checks, responsive layout proof, or current library docs

## Do not use when

- the project is an authenticated product, dashboard, SaaS, API, desktop app, or MCP server
- account data, billing, teams, jobs, webhooks, or durable user records are part of the core scope
- the user only asks for a small copy edit that does not need project workflow analysis

## Inputs needed

- user goal, audience, offer, content source, brand constraints, and primary call to action
- current repo structure, routes, page files, design system, and build/test commands
- existing analytics, SEO metadata, screenshots, accessibility reports, or performance notes when available
- target pages and proof criteria for browser verification

## Output contract

This skill must produce:

```txt
website scope decision
page/content map
implementation or review plan
browser verification receipt
accessibility/performance notes
final handoff
```

## Workflow

### Phase 0 - Triage

- Confirm the project is a website, not a webapp or SaaS product.
- Name the primary audience and one primary action.
- Identify the current page, route, or content surface that owns the requested outcome.
- Decide whether the task is creation, redesign, migration, audit, or verification.

### Phase 1 - Context gathering

- Read the existing routes, components, content sources, metadata, layout primitives, and styles needed for the page.
- Inspect local conventions for routing, styling, image handling, forms, SEO, and tests before proposing changes.
- Use `docs.latest` only for current external library, framework, analytics, SEO, CMS, or deployment docs.
- Gather browser proof targets: viewport sizes, navigation path, form state, interactive components, and expected visible result.

### Phase 2 - Website analysis

- Define the page promise, audience, objection, proof, and next action.
- Map information architecture: navigation, page sections, links, metadata, footer, and empty/error states if relevant.
- Check accessibility basics: semantic landmarks, heading order, labels, focus states, contrast, keyboard path, reduced motion.
- Check performance basics: image sizes, above-the-fold weight, font loading, script usage, caching, and unnecessary client JavaScript.
- Check content durability: avoid hard-coded claims that should come from data, docs, or a CMS.

### Phase 3 - Action / artifact

- Make the smallest page, component, content, or review artifact that satisfies the stated outcome.
- Keep copy, design, and code aligned to one primary conversion or comprehension goal.
- Preserve repo-local design primitives and routing patterns unless they are the source of the problem.
- Record preview or remote-repo evidence only when those optional capabilities are available and relevant.

### Phase 4 - Verification

- Run the narrowest relevant local checks for the edited surface.
- Use `browser.verify` for the actual page path, not only component assumptions.
- Verify responsive behavior for at least mobile and desktop when layout changed.
- Verify keyboard navigation and visible focus for interactive elements.
- Capture failures as specific page, viewport, action, expected result, and actual result.

### Phase 5 - Final report

- Report what page or flow changed, what proof was collected, and any content/design risks.
- Separate automated proof from manual browser observations.
- Name any remaining decisions the user must make, such as final copy, brand assets, legal text, or analytics configuration.

## Gates / stop conditions

- Stop if the requested outcome actually belongs to `instructa.webapp` or `instructa.saas`.
- Stop before adding analytics, forms, tracking pixels, or production-connected integrations without user approval.
- Stop if required content, brand assets, or legal copy are missing and the work would invent facts.
- Stop if browser verification cannot reach the target page; report the blocker and the manual proof needed.

## Verification requirements

- Files inspected and changed.
- Commands run and exact result.
- Browser path, viewport, and pass/fail observations.
- Accessibility and performance notes proportional to the change.

## Capability use

Required by the plugin:

```txt
docs.latest
browser.verify
```

Optional when installed and relevant:

```txt
deploy.preview
repo.remote
```

Do not introduce domain-specific capability IDs for SEO, copywriting, landing pages, CMS, analytics, or forms. Those are website workflow concerns.

## Anti-patterns

- Do not optimize for visual novelty while the primary action is unclear.
- Do not add framework-specific scaffolding unless the repo already uses it or the user chose it.
- Do not make browser verification a screenshot-only check when interactive behavior changed.
- Do not turn a content site into an app architecture just because a component is interactive.
- Do not use optional capabilities just because they exist.

## Final report

```txt
Skill: website-project-workflow
Decision:
Changed:
Proof:
Browser:
Risks:
Next:
```
