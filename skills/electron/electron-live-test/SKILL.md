---
name: electron-live-test
description: Live-test any Electron desktop app with native-devtools-mcp, Chrome DevTools Protocol, screenshots, OCR, and accessibility tools. Use when the user asks for Electron UI verification, MCP-driven app control, renderer CDP interaction, native desktop automation, screenshots, or OCR-driven checks.
---

# Electron Live Test

## When To Use

Use this skill for live, headed testing of a running Electron desktop app. It is for interactive verification while developing, not for replacing automated smoke tests.

Use Playwright, WebDriver, Spectron replacements, or app-specific smoke tests for deterministic CI coverage. Use native-devtools-mcp when the user wants the agent to inspect or drive the currently running desktop app.

## Requirements

- `native-devtools-mcp` available to the agent host.
- macOS: Accessibility and Screen Recording permissions for the controlling app.
- Electron renderer debugging enabled through a Chrome DevTools Protocol endpoint.
- The target app running in headed mode.

## MCP Setup

Prefer launching native-devtools-mcp from a neutral directory so project-local package-manager policies do not break `npx`:

```bash
sh -c "cd /tmp && exec npx -y native-devtools-mcp"
```

If native permissions or helpers need setup, run one of:

```bash
pnpm dlx native-devtools-mcp setup
cd /tmp && npx native-devtools-mcp setup
```

Do not run setup from a target repo root when that repo has strict `devEngines`, package-manager, or lifecycle policies that could block `npx`.

Quick check:

```bash
cd /tmp && npx -y native-devtools-mcp --help
```

## Starting The App

Do not start, stop, or restart the user's app unless they explicitly ask.

For CDP control, the Electron app must expose a remote debugging port. Common launch patterns:

```bash
electron . --remote-debugging-port=9222
ELECTRON_ENABLE_LOGGING=1 npm run dev -- --remote-debugging-port=9222
```

Many apps wrap Electron startup in npm, pnpm, yarn, turbo, forge, vite, or custom scripts. Prefer the repo's documented dev command if it already supports CDP. If not, inspect the app's main-process startup path and add/pass Electron's `--remote-debugging-port=<port>` only with user approval.

Verify the endpoint before attaching:

```bash
curl --fail --silent http://127.0.0.1:9222/json/version
curl --fail --silent http://127.0.0.1:9222/json/list
```

If the current app was started without CDP, ask the user to restart it with the app-specific CDP-enabled command.

## Target Selection

Attach to the existing Electron renderer target, not a new blank page.

Use `/json/list` to identify the target by title, URL, or app route. If multiple targets exist, choose the one matching the visible app window and report the selected title/URL. For ambiguous or multi-target apps, read `references/cdp-targeting.md`.

## Tool Choice

- Use CDP for renderer DOM, React/Vue/Svelte shells, routes, sidebars, dialogs, forms, keyboard input, console logs, and network-visible renderer behavior.
- Use screenshots, OCR, or template matching for canvas, WebGL, Pixi, Three.js, game, map, or custom-rendered surfaces.
- Use macOS accessibility/AX tools for native window chrome, menus, file pickers, permission dialogs, and OS dialogs.
- Use process logs or app-specific logs for main-process behavior; CDP only proves renderer state unless the app exposes main-process diagnostics.
- Prefer element references from fresh snapshots over coordinates. Use coordinates only after a fresh screenshot.

## Live Testing Flow

1. Confirm native-devtools-mcp is connected.
2. Confirm the Electron app is running and headed.
3. Confirm the app exposes CDP on the expected `127.0.0.1:<port>` endpoint.
4. Inspect `/json/list` and select the existing renderer target.
5. Take a fresh DOM snapshot before interacting.
6. Perform one deliberate action at a time.
7. After clicks, typing, navigation, waits, or anything that can change the page, take a fresh snapshot before the next structural action.
8. For canvas or native-window interactions, take a screenshot first and explain any coordinate-based action.
9. Stop and report blockers such as login, missing app window, missing CDP port, missing permissions, unexpected dialogs, wrong target, or repeated failed interactions.

## Safety

- Do not expose CDP in packaged or production builds unless the user explicitly accepts that risk.
- Bind CDP to loopback only. Treat externally reachable remote debugging as a security issue.
- Do not enter secrets, payment data, production credentials, or private user data into a live app unless the user explicitly provides safe test values.
- Avoid destructive UI actions unless they are the requested test path and the user has approved the target data.

## Verification Report

After live testing, summarize:

- What was tested.
- Which interaction path was used: CDP, screenshot/OCR, AX, logs, or mixed.
- The CDP endpoint and selected renderer target title/URL, if used.
- What passed or failed.
- Any automated checks run separately, such as unit tests, typecheck, or smoke tests.
