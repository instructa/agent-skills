---
name: desktop-project-workflow
description: Plan, implement, review, and verify installable, local-first, native, or desktop-shell applications.
---

# Desktop Project Workflow

## Purpose

Ship desktop application work with clear platform ownership, local runtime proof, safe OS boundaries, durable planning, and targeted debugging when needed.

## Use when

- the project is an installable, local-first, native, hybrid, or desktop-shell application
- the work touches app launch, windows, menus, tray, permissions, filesystem, local data, packaging, auto-update, IPC, native bridges, or desktop UI behavior
- the slice needs desktop runtime verification or optional native debugging

## Do not use when

- the project is only a browser webapp, website, SaaS backend, API, or MCP server
- the desktop app is only a wrapper for a webapp and the change is entirely browser-route logic
- the task is a low-level native crash investigation better owned by a dedicated native-debug provider workflow

## Inputs needed

- accepted spec, PlanDB task or fallback ledger context, and proof oracle
- app framework/runtime, launch commands, package scripts, OS targets, permissions, local data paths, IPC/native bridge files, and tests
- reproduction path, screenshots, logs, crash reports, stack traces, or profiler output when debugging
- safe local test data and confirmation before launching production-connected apps

## Output contract

This skill must produce:

```txt
desktop scope decision
runtime/platform ownership map
implementation or review plan
ledger receipt
desktop runtime proof
debug proof when used
handoff
```

## Workflow

### Phase 0 - Triage

- Confirm the work is desktop scope and name the platform concern.
- Read the current PlanDB task or fallback ledger before changing code.
- Separate runtime owner, first fix owner, canonical long-term owner, and wrong competing owners.
- Decide whether the change belongs to platform shell, domain/application logic, shared core, renderer/UI, or adapter integration.

### Phase 1 - Context gathering

- Read the launch path, desktop shell, IPC/native bridge, local persistence, renderer route, packaging, and test files that own the behavior.
- Use `docs.latest` for current runtime, OS, packaging, native bridge, signing, update, or permission docs only when needed.
- Identify the safest runtime command; do not start, stop, or restart the user's app unless the user requested it.
- Gather logs, screenshots, local data paths, and reproduction steps before changing code.

### Phase 2 - Desktop analysis

- Map OS boundary behavior: filesystem, dialogs, permissions, keychain, notifications, clipboard, shell open, deep links, and network.
- Map local state ownership: project data, user preferences, caches, migrations, backup/restore, and destructive operations.
- Map process and IPC behavior: main/native process, renderer/UI, preload/bridge, workers, child processes, and message contracts.
- Check security posture: least-privilege bridges, no remote code execution, no broad filesystem access, no secret exposure in logs.
- Decide whether native debugging is necessary or whether runtime logs and UI proof are sufficient.

### Phase 3 - Action / artifact

- Implement or review the smallest platform or app change that satisfies the proof oracle.
- Keep OS and shell concerns in the platform layer and reusable product policy in the domain/application owner.
- Avoid framework-specific public assumptions; the plugin workflow supports any desktop runtime with a provider-backed runtime proof.
- Record ledger events when architecture decisions, runtime proof, or risk state changes.

### Phase 4 - Verification

- Run focused tests for changed domain, renderer, bridge, or platform code.
- Use `desktop.runtime` proof for launch, relevant window state, logs, and the target user path.
- Use optional `native.debug` only when a hang, deadlock, crash, high CPU loop, or native stack question requires it.
- Use optional `secrets.scan` when packaging, config, logs, credentials, env, or local data handling changed.
- Record OS, runtime command, app version/build mode, and proof artifacts.

### Phase 5 - Final report

- Report platform owner, changed surface, runtime proof, debug proof if used, ledger receipt, and residual risks.
- State any manual verification that remains for signing, notarization, auto-update, installer behavior, or OS-specific permissions.
- Name human decisions needed for destructive local data behavior, telemetry, update channels, or permission prompts.

## Gates / stop conditions

- Stop if PlanDB or fallback ledger context is unavailable for a desktop architecture or release-risk change.
- Stop before launching production-connected desktop apps or commands that can alter local user data without approval.
- Stop if OS permissions, signing credentials, or private local data are required and unavailable.
- Stop if the first fix would put platform shell behavior in shared domain code.

## Verification requirements

- Files inspected and changed.
- PlanDB or fallback ledger event/receipt.
- Commands run and exact result.
- Desktop runtime proof with launch path, OS, target window/flow, and logs/screenshots as available.
- Native debug proof when used.
- Security and local data risks.

## Capability use

Required by the plugin:

```txt
plan.ledger
docs.latest
desktop.runtime
```

Optional when installed and relevant:

```txt
native.debug
secrets.scan
repo.remote
```

Desktop framework names, IPC libraries, packaging systems, and OS features are workflow context, not capability IDs.

## Anti-patterns

- Do not start or restart the user's running app unless they explicitly asked.
- Do not put OS-specific bridge behavior in generic domain modules.
- Do not debug by repeatedly clicking a frozen app without collecting logs or stack evidence.
- Do not expose remote debugging, broad filesystem access, or production credentials as convenience.
- Do not treat a desktop runtime proof as browser-only proof when native shell behavior changed.

## Final report

```txt
Skill: desktop-project-workflow
Decision:
Changed:
Ledger:
Proof:
Runtime:
Debug:
Risks:
Next:
```
