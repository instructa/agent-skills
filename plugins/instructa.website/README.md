# Instructa Website Project

Project workflow layer for marketing, content, documentation, landing and blog sites.

`instructa.website` depends on `instructa.base`; it does not redefine capability IDs or provider behavior. It uses current-doc and browser-verification capabilities supplied by third-party provider plugins.

## Included Skills

- `website-project-workflow`
- `redesign-my-landingpage` (support skill for landing-page and conversion work)

## Required Capabilities

- `docs.latest` from `third-party.context7`
- `browser.verify` from `third-party.playwright-mcp`

## Optional Capabilities

- `deploy.preview`
- `repo.remote`

## Workflow Boundary

Use this plugin for public-facing sites where content structure, conversion clarity, accessibility, performance and browser proof are the main risks. `redesign-my-landingpage` lives here because landing-page conversion work is website-specific, not reusable core. Use `instructa.webapp` or `instructa.saas` when the work becomes an interactive application or product lifecycle.
