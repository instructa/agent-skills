# third-party.desktop-runtime

Curated AgentRig wrapper for the `desktop.runtime` capability.

This plugin describes the runtime contract used by desktop project plugins. It wraps a project's existing desktop runtime command; it does not choose Electron vs Tauri vs native frameworks or own desktop product policy.

## Capability

- `desktop.runtime` -> project-provided desktop runtime command

## Upstream

- Owner/source: desktop runtime maintainers and the project under test, such as Electron, Tauri, native app commands or project-provided run scripts
- Install method: use the desktop project's existing runtime command and dependencies, then run `agentrig doctor --capability desktop.runtime`
- Provider targets: `codex`, `claude-code`, `cursor`
- Required env: none
- Optional env: `AGENTRIG_DESKTOP_COMMAND`, `DISPLAY`, `WAYLAND_DISPLAY`

## Permissions

- Filesystem: project source tree, build artifacts, app logs and temporary runtime data
- Network: local development servers or app endpoints declared by the project
- Local code: yes
- Approval: launching production-connected apps or commands that alter local user data requires human approval

## Fallback

Launch the desktop app manually and capture logs, screenshots and project-specific reproduction notes.

## Verification

Smoke test: `verify/desktop-runtime-smoke.md`
