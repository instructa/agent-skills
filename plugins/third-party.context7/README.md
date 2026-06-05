# third-party.context7

Curated AgentRig wrapper for the `docs.latest` capability.

This plugin points AgentRig at Context7 for current library and API documentation. It does not copy Context7 content or make Context7 output canonical product truth.

## Capability

- `docs.latest` -> Context7 documentation lookup

## Upstream

- Owner/source: Upstash, `https://github.com/upstash/context7`
- Install method: install the upstream Context7 MCP or CLI/skills mode for the target agent, then run `agentrig doctor --capability docs.latest`
- Provider targets: `codex`, `claude-code`, `cursor`
- Required env: none

## Permissions

- Filesystem: none required by this wrapper
- Network: Context7 service and external documentation sources
- Local code: yes when the selected MCP or CLI install mode runs an upstream local command
- Approval: use human review before applying docs to security-sensitive or irreversible decisions

## Fallback

Use official docs, vendored docs, package source code or repository examples. Treat all sources as evidence and verify against the project code before changing behavior.

## Verification

Smoke test: `verify/context7-smoke.md`
