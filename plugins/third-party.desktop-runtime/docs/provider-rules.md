# Provider Rules

## Ownership

`third-party.desktop-runtime` is a curated wrapper manifest. The project and its runtime framework own app behavior. AgentRig owns only the `desktop.runtime` capability mapping and wrapper safety policy.

## Usage Rules

- Use only for the canonical `desktop.runtime` capability.
- Defer framework-specific behavior to the desktop project plugin or the project under test.
- Show the exact run command and working directory before launching.
- Capture logs and evidence without changing the runtime contract.

## Security Rules

- Require human approval before launching apps connected to production services, user accounts, payment flows or real local user data.
- Do not broaden filesystem access beyond the project and runtime artifacts without explicit approval.
- Warn when runtime commands use `sudo`, destructive flags, shell pipelines from the network or broad home-directory access.
