# Playwright MCP Smoke Test

1. Confirm the plugin manifest validates against `plugin.v1.json`.
2. Run `agentrig doctor --capability browser.verify`.
3. Confirm doctor reports `third-party.playwright-mcp` as the provider for `browser.verify`.
4. Open a harmless local or public test page.
5. Capture an accessibility snapshot and screenshot.
6. Confirm no mutating action is attempted without explicit user approval.
