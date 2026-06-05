# MCP Inspector Smoke Test

1. Confirm the plugin manifest validates against `plugin.v1.json`.
2. Run `agentrig doctor --capability mcp.verify`.
3. Confirm doctor reports `third-party.mcp-inspector` as the provider for `mcp.verify`.
4. Launch MCP Inspector against a harmless local test MCP server.
5. Inspect tool descriptors before invoking any tool.
6. Invoke only a read-only test tool.
7. Confirm write or credential-touching tools require explicit human approval.
