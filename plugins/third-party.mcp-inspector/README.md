# third-party.mcp-inspector

Curated AgentRig wrapper for the `mcp.verify` capability.

This plugin describes MCP Inspector as the default verification provider for MCP project plugins. It does not own MCP server implementation, MCP security policy across all providers or the upstream inspector.

## Capability

- `mcp.verify` -> MCP Inspector verification

## Upstream

- Owner/source: Model Context Protocol, `https://github.com/modelcontextprotocol/inspector`
- Install method: install and run the upstream MCP Inspector for local MCP server verification, then run `agentrig doctor --capability mcp.verify`
- Provider targets: `codex`, `claude-code`, `cursor`
- Required env: none

## Permissions

- Filesystem: MCP server files selected for inspection and temporary inspector logs
- Network: localhost inspector UI and endpoints exposed by the MCP server under test
- Local code: yes
- Approval: invoking tools that mutate files, external systems or credentials requires human approval

## Fallback

Use manual MCP server smoke tests with client logs, tool descriptors and explicit test prompts.

## Verification

Smoke test: `verify/mcp-inspector-smoke.md`
