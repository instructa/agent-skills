---
name: hol-guard
description: Protect local coding-agent harnesses with the HOL Guard runtime before state-changing commands and tool calls. Use when a supported agent may edit files, execute commands, call external tools or MCP servers, or perform destructive work that must fail closed when protection is unavailable.
---

# HOL Guard

Use HOL Guard as a local runtime boundary around a supported coding-agent harness. It complements repository permissions, human review, tests, and service-side controls; it does not replace them.

## Workflow

1. Preserve the current workspace and native approval gates. Never read `.env` files to set this up.
2. Probe the real CLI:

```bash
hol-guard --version
```

If it is missing and the user asked for runtime setup, prefer an isolated install:

```bash
pipx install hol-guard
```

If `pipx` is unavailable, stop instead of silently changing the user's Python environment.

3. Discover the supported harness and use only the exact identifier returned by HOL Guard:

```bash
hol-guard status
hol-guard detect --json
```

Do not maintain a hard-coded harness list. If no supported harness is detected, stop before mutation-bearing work.

4. Let Guard own setup and prove the protected launch path:

```bash
hol-guard bootstrap
hol-guard install <harness>
hol-guard run <harness> --dry-run
```

If setup or dry-run fails, reports an unexpected mutation, or cannot prove protection, stop. Never fall back to launching the agent unprotected.

5. Launch through Guard, then verify current protection:

```bash
hol-guard run <harness>
hol-guard doctor <harness> --json
hol-guard status
```

Only claim protection when current command output proves it.

6. Continue the original task with the project's own approvals, tests, and deployment controls still enabled. If Guard queues work, inspect it rather than bypassing it:

```bash
hol-guard approvals
hol-guard approvals open
```

Approve or deny only after understanding the requested scope and risk.

## Stop Conditions

Stop before side-effecting work when:
- `hol-guard --version` is unavailable and installation is not authorized.
- `hol-guard detect --json` finds no supported harness.
- bootstrap, install, dry-run, doctor, or status cannot prove the protected path.
- the proposed workaround is a direct unprotected harness launch.

## Verification

Before reporting success, show evidence that the CLI is available, the harness came from runtime detection, dry-run succeeded, the real launch used `hol-guard run`, and doctor/status prove current protection. Keep native project and provider controls in force.
