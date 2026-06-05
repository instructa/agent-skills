# Instructa Webapp Project

Project workflow layer for interactive web applications, dashboards and internal tools.

`instructa.webapp` depends on `instructa.base`; it composes project workflows and declares capability needs without owning the capability model.

## Included Skills

- `webapp-project-workflow`

## Required Capabilities

- `docs.latest` from `third-party.context7`
- `browser.verify` from `third-party.playwright-mcp`

## Optional Capabilities

- `plan.ledger`
- `repo.remote`

## Workflow Boundary

Use this plugin for interactive UI work where application state, route flows, accessibility and browser proof are central. Use `instructa.saas` when users, billing, teams, jobs, webhooks or production operations become part of the project scope.
