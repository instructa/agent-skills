# third-party.github-mcp

Curated AgentRig wrapper for the `repo.remote` capability.

This plugin describes GitHub MCP as the default remote repository context provider. It does not own GitHub workflows, CI policy, repository security policy or cross-provider product behavior.

## Capability

- `repo.remote` -> GitHub MCP remote repository context

ADR-0005 also calls out GitHub MCP functions for CI status and repository security. The AgentRig 1.0 manifest schema exposes only the canonical capability ID `repo.remote`; optional CI/security toolsets stay explicitly gated.

## Upstream

- Owner/source: GitHub, `https://github.com/github/github-mcp-server`
- Install method: configure the upstream GitHub MCP server with minimal toolsets, then run `agentrig doctor --capability repo.remote`
- Provider targets: `codex`, `claude-code`, `cursor`
- Required env: `GITHUB_PERSONAL_ACCESS_TOKEN`

## Permissions

- Filesystem: none required by this wrapper
- Network: `api.github.com` and repositories allowed by the configured token
- Local code: yes, local MCP server
- Default toolsets: `context`, `repos`, `issues`, `pull_requests`
- Optional toolsets on explicit need: `actions`, `code_security`, `dependabot`, `secret_protection`, `security_advisories`
- Never default: `all`
- Approval: writes, workflow actions, security changes and token-scope changes require human approval

## Fallback

Use local `git`, `gh` CLI with explicit commands, or the GitHub web UI manually.

## Verification

Smoke test: `verify/github-mcp-smoke.md`
