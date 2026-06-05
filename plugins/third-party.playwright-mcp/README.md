# third-party.playwright-mcp

Curated AgentRig wrapper for the `browser.verify` capability.

This plugin describes Microsoft Playwright MCP as the default browser verification provider for website, webapp and SaaS project plugins. It does not own Playwright, browser automation policy for all providers or product testing strategy.

## Capability

- `browser.verify` -> Playwright MCP browser automation

## Upstream

- Owner/source: Microsoft, `https://github.com/microsoft/playwright-mcp`
- Install method: configure the upstream Playwright MCP server for the target agent, then run `agentrig doctor --capability browser.verify`
- Provider targets: `codex`, `claude-code`, `cursor`
- Required env: none
- Optional env: `PLAYWRIGHT_BROWSERS_PATH`

## Permissions

- Filesystem: browser profile/cache paths selected by the upstream server
- Network: web pages opened for verification
- Local code: yes, local MCP server
- Approval: mutating UI flows require explicit user confirmation when they touch real accounts, data or payments

## Fallback

Use manual browser verification with screenshots, accessibility notes and reproduction steps.

## Verification

Smoke test: `verify/playwright-mcp-smoke.md`
