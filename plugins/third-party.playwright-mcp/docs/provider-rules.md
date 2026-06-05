# Provider Rules

## Ownership

`third-party.playwright-mcp` is a curated wrapper manifest. Microsoft owns Playwright MCP. AgentRig owns only the capability mapping and wrapper safety policy.

## Usage Rules

- Use only for the canonical `browser.verify` capability.
- Default to read-only verification flows.
- Prefer accessibility snapshots for action grounding.
- Capture evidence in the project workflow rather than relying on unrecorded browser state.
- Do not use this provider as a substitute for owned application tests.

## Security Rules

- Show the exact MCP install/configuration command.
- Require explicit human approval before mutating real accounts, production data, paid resources or payment flows.
- Use minimal browser/profile scope.
- Warn when the target page is authenticated, production, destructive or payment-related.
