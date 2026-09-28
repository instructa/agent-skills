---
name: claude-designer
description: "Use Claude Code directly from Astra's current task to design or implement UI/UX and frontend work, with Astra owning sequencing, review, and integration. Use when the user invokes $claude-designer or requests this workflow."
---

# Claude Designer

Astra handles the workflow in the current task and calls Claude Code directly. Do not create or route through an intermediary Codex task. This skill supports existing interfaces and new interfaces; it does not prescribe a framework.

## Choose the sequence

Inspect enough of the user journey, repository instructions, UI, and data contracts to choose:

- **Design first:** interaction, information hierarchy, or product direction is uncertain. Ask Claude to implement a bounded prototype using clearly isolated fixtures, then use its findings to guide backend work.
- **Contracts first:** calculations, permissions, persistence, or API semantics determine the interface. Establish those contracts before asking Claude to integrate them. Do not create speculative APIs just to unblock cosmetic work.
- **Parallel:** the UI can use an agreed contract while Astra works on backend or domain files. Define file ownership and integration points before either side edits shared files.

State the sequence and reason briefly. Astra keeps architectural decisions, backend/domain ownership, review, and final integration unless the user explicitly assigns them otherwise.

## Call Claude directly

An explicit `$claude-designer` invocation authorizes this workflow. Use the current checkout by default and keep the Claude run in Astra's current task. Do not create a separate Codex task or worktree just to supervise Claude. Use an isolated checkout only when the requested work needs one and the relevant state can be made available without silently copying the entire dirty tree.

Read [the direct Claude workflow](references/direct-claude-workflow.md). In brief:

- Prepare a bounded brief with the requested outcome, audience, main journey, references, scope, acceptance criteria, agreed contracts, unresolved dependencies, allowed paths, and relevant project instructions.
- Check Claude Code's installed version, supported flags, and authentication status without printing credentials. Do not install, update, log in, or switch models silently.
- Start Claude Code from the relevant checkout using its CLI and the reviewed brief. Keep the process handle and Claude session ID in this task; reuse the same session for focused corrections.
- Prefer a verified, directly exposed Claude worker tool that stays pending until completion. Do not wrap it in Code Mode or replace completion waiting with repeated sleep/status/log-tail responses. If that integration is unavailable, disclose the limitation before starting; the CLI fallback is not verified polling-free. Follow the completion-wait section in the direct workflow reference.
- If a prerequisite or permission blocks the run, report the concrete blocker. Do not retry the same denied operation repeatedly or bypass permissions without explicit authorization.

## Review and integrate

Inspect Claude's actual diff, preserve unrelated changes, and verify the requested user journey against the agreed contracts. Use the project's existing checks when appropriate and inspect the relevant responsive, keyboard, and loading/empty/error/success states. Keep fixtures clearly marked. Save useful screenshots or preview details when available. Report what was verified and what remains unverified; a successful build alone does not establish design acceptance.

Keep the response concise: summarize the sequence, Claude's result, changed paths, evidence, remaining gaps, and integration outcome. Do not substitute a native Codex implementation for the requested Claude work without explaining why Claude Code was unavailable.
