# Electron Live Test

Live-test running Electron desktop apps with native-devtools-mcp, Chrome DevTools Protocol, screenshots, OCR, and accessibility tools.

## Install

```bash
# Codex
npx skills add instructa/agent-skills --skill electron-live-test --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill electron-live-test --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill electron-live-test --agent cursor
```

## Use When

- You need an agent to inspect or drive a headed Electron app that is already running.
- Renderer DOM, routes, forms, dialogs, console logs, or network-visible behavior need live verification through CDP.
- Canvas, WebGL, game, map, or custom-rendered UI needs screenshot/OCR-based verification.
- Native window chrome, menus, file pickers, or OS permission dialogs need accessibility tooling.

## Requirements

- `native-devtools-mcp` for native desktop control, screenshots, OCR, and accessibility.
- A loopback CDP endpoint exposed by the Electron app, for example `--remote-debugging-port=9222`. CDP comes from Electron; this skill does not provide it.
- macOS permissions when needed: Accessibility and Screen Recording

## CDP Setup

Start native-devtools-mcp from a neutral directory:

```bash
sh -c "cd /tmp && exec npx -y native-devtools-mcp"
```

Quick check:

```bash
cd /tmp && npx -y native-devtools-mcp --help
```

Launch the Electron app with remote debugging enabled through its app-specific dev command. Then verify:

```bash
curl --fail --silent http://127.0.0.1:9222/json/version
curl --fail --silent http://127.0.0.1:9222/json/list
```

Attach to the existing Electron renderer target from `/json/list`. Do not create a new blank page for renderer verification.

See `SKILL.md` for the full agent workflow.
