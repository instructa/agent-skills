# GitHub MCP Smoke Test

1. Confirm the plugin manifest validates against `plugin.v1.json`.
2. Confirm `GITHUB_PERSONAL_ACCESS_TOKEN` is present with minimal scopes for the intended repository.
3. Run `agentrig doctor --capability repo.remote`.
4. Confirm doctor reports `third-party.github-mcp` as the provider for `repo.remote`.
5. List repository metadata or pull request context in read-only mode.
6. Confirm the `all` toolset is not configured by default.
7. Confirm write/security/action toolsets require explicit human approval.
