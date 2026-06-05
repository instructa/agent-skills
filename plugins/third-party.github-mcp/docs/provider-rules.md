# Provider Rules

## Ownership

`third-party.github-mcp` is a curated wrapper manifest. GitHub owns the MCP server and GitHub API behavior. AgentRig owns only the capability mapping and safety rules.

## Usage Rules

- Use only for the canonical `repo.remote` capability.
- Default to read-only repository, issue and pull request context.
- Use `actions`, `code_security`, `dependabot`, `secret_protection` and `security_advisories` only on explicit need.
- Never default to the `all` toolset.
- Prefer local git for repository state that is already available in the checkout.

## Security Rules

- Show the exact MCP install/configuration command.
- Use the smallest GitHub token scope that satisfies the task.
- Require human approval before writes, workflow dispatch/cancel/rerun, branch protection changes, security alert changes or secret-protection changes.
- Revoke unused tokens during uninstall or provider replacement.
