# Provider Rules

## Ownership

`third-party.mcp-inspector` is a curated wrapper manifest. The MCP project owns MCP Inspector. AgentRig owns only the `mcp.verify` capability mapping and wrapper safety policy.

## Usage Rules

- Use only for the canonical `mcp.verify` capability.
- Use this provider for `instructa.mcp` verification, not as a generic browser or API test runner.
- Inspect descriptors and scopes before invoking any MCP tool.
- Keep generated verification evidence with the project workflow.

## Security Rules

- Show the exact inspector command and MCP server command before running.
- Require explicit consent for local executable MCP servers.
- Require human approval before invoking tools that write files, call external systems, access credentials or perform account mutations.
- Warn on broad filesystem, home-directory, SSH key or network scopes.
