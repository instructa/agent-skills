# Provider Rules

## Ownership

`third-party.native-debug` is a curated wrapper manifest. Debugger maintainers and the target project own debugger behavior. AgentRig owns only the `native.debug` capability mapping and wrapper safety policy.

## Usage Rules

- Use only for the canonical `native.debug` capability.
- Prefer logs, crash reports and thread dumps before attaching a debugger.
- Show the exact debugger command, target process and expected output before running.
- Keep debugger output scoped to the investigation.

## Security Rules

- Require human approval before attaching to a process.
- Require human approval before using `sudo`, developer-mode escalation or platform-specific attach permissions.
- Do not inspect process memory that may contain credentials unless the user explicitly approves the risk.
- Treat backtraces, dumps and debugger logs as sensitive project artifacts.
