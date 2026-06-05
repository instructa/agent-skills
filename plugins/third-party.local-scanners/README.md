# third-party.local-scanners

Curated AgentRig wrapper for local scanner capabilities.

This plugin groups the ADR-0005 local scanner provider mappings. It does not own the scanner CLIs, hosted security products or cross-provider security policy.

## Capabilities

- `secrets.scan` -> `secleak-check` / Gitleaks / Trivy / GitHub secret protection
- `supplychain.scan` -> `package-security-check` / npm audit / pnpm audit / OSV / Trivy / GitHub Dependabot
- `shell.lint` -> `shellck` / ShellCheck

## Upstream

- Owner/source: Gitleaks, Trivy, ShellCheck, OSV, package-manager audit tooling and GitHub security product maintainers
- Install method: install selected local scanner CLIs through the project package manager or system package manager, then run `agentrig doctor --capability <capability>`
- Provider targets: `codex`, `claude-code`, `cursor`
- Required env: none
- Optional env: `GITHUB_TOKEN`, `OSV_API_KEY`

## Permissions

- Filesystem: project source tree, package manifests, lockfiles, shell scripts and temporary scanner reports
- Network: optional vulnerability databases and GitHub security APIs when explicitly enabled
- Local code: yes
- Approval: broad filesystem scans, hosted security changes and scan-result uploads require human approval

## Fallback

Run reviewed local scanner commands manually, use hosted provider security checks when available, or perform manual shell/security review for small changes.

## Verification

Smoke test: `verify/local-scanners-smoke.md`
