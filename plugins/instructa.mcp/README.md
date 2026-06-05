# Instructa MCP Project

Project workflow layer for MCP servers and agent tool integrations.

`instructa.mcp` depends on `instructa.base`; it owns MCP project workflow quality while the `mcp.verify` capability resolves through the MCP Inspector provider.

## Included Skills

- `mcp-project-workflow`

## Required Capabilities

- `plan.ledger` from `third-party.plandb`
- `docs.latest` from `third-party.context7`
- `mcp.verify` from `third-party.mcp-inspector`
- `secrets.scan` from `third-party.local-scanners`

## Optional Capabilities

- `repo.remote`

## Workflow Boundary

Use this plugin for MCP servers, tool descriptors, resources, prompts and agent integration surfaces. Use `instructa.api` for ordinary HTTP or worker services that are not MCP protocol integrations.
