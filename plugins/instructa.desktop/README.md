# Instructa Desktop Project

Project workflow layer for installable, local-first and native desktop applications.

`instructa.desktop` depends on `instructa.base`; it coordinates desktop workflow concerns and requires a desktop runtime provider without choosing a framework in the public plugin contract.

## Included Skills

- `desktop-project-workflow`

## Required Capabilities

- `plan.ledger` from `third-party.plandb`
- `docs.latest` from `third-party.context7`
- `desktop.runtime` from `third-party.desktop-runtime`

## Optional Capabilities

- `native.debug`
- `secrets.scan`
- `repo.remote`

## Workflow Boundary

Use this plugin for apps that install locally, bridge OS resources, persist local state or require desktop runtime proof. Native debugging remains an optional provider capability, not a desktop project capability definition.
