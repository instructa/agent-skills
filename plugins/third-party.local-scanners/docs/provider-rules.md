# Provider Rules

## Ownership

`third-party.local-scanners` is a curated wrapper manifest. Scanner maintainers own scanner behavior and vulnerability data. AgentRig owns only the capability mapping and wrapper safety policy.

## Usage Rules

- Use `secrets.scan` for secret leak checks.
- Use `supplychain.scan` when package, dependency, install or lockfile surfaces change.
- Use `shell.lint` when shell scripts change.
- Keep scans scoped to the project unless the user explicitly approves broader paths.
- Prefer once-and-exit scanner commands in automation.

## Security Rules

- Show exact scanner commands before running.
- Do not upload source, lockfiles, secrets or scan results to hosted services without explicit approval.
- Warn before scanning home directories, SSH keys, credentials, browser profiles or broad filesystem roots.
- Treat scanner output as sensitive when it contains secret values, dependency names or internal paths.
