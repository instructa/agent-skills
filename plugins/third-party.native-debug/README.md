# third-party.native-debug

Curated AgentRig wrapper for the `native.debug` capability.

This plugin describes native debugging support for desktop/native workflows. It owns the `debug-lldb` support workflow and does not own LLDB, GDB, platform debugger behavior or the desktop product's debugging policy.

## Capability

- `native.debug` -> platform-native debugger tooling

## Included Skills

- `debug-lldb`

## Upstream

- Owner/source: LLDB, GDB and platform debugger maintainers; `debug-lldb`, LLDB, GDB and platform-native debugger tooling
- Install method: use platform debugger tooling already available for the project or install through trusted system channels, then run `agentrig doctor --capability native.debug`
- Provider targets: `codex`, `claude-code`, `cursor`
- Required env: none
- Optional env: `LLDB_DEBUGSERVER_PATH`, `DEBUG_SYMBOLS_PATH`

## Permissions

- Filesystem: debug symbols, crash reports, process logs and temporary backtrace files
- Network: none required by this wrapper
- Local code: yes
- Approval: attaching to a process, escalating privileges or reading sensitive process memory requires human approval

## Fallback

Collect logs, crash reports, thread dumps and platform debugger steps manually.

## Verification

Smoke test: `verify/native-debug-smoke.md`
