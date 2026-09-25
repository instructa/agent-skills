---
name: claude-designer
description: "Delegate UI/UX design or frontend implementation to Claude Code through a separate GPT-6 Luna max task, with Astra owning sequencing and integration. Use when the user invokes $claude-designer or requests this delegated design workflow."
---

# Claude Designer

Keep expensive architectural work in the parent task. Use a separate, user-visible Luna task to supervise Claude's design implementation and verification. This skill supports existing interfaces and new interfaces requested by the user; it does not prescribe a framework.

## Parent: choose the sequence

The intended parent is Astra. Do not change the current task's model automatically. Inspect enough of the user journey, existing UI, repository instructions, and data contracts to decide:

- **Design first:** the interaction, information hierarchy, or product direction is uncertain. Delegate a prototype or design implementation with explicitly isolated fixtures, then use its requirements to guide backend work.
- **Contracts first:** calculations, permissions, persistence, or API semantics determine the interface. Establish the necessary contracts before asking Claude to integrate them. Do not build speculative APIs merely to unblock cosmetic work.
- **Parallel:** the UI can use an agreed contract while Astra implements the backend in separate files/checkouts. Identify who owns each shared file and integration step.

State the chosen sequence and its reason briefly. Give Luna a concrete outcome, not a request to rediscover the whole project. Astra retains architectural decisions, backend/domain ownership, and final integration unless the user explicitly assigns them otherwise.

## Dispatch a separate Luna task

An explicit invocation of this skill requests a new task. Automatic skill discovery alone is not permission to create one: if the user has not requested a new task or this workflow, propose using the skill rather than silently creating a task.

Use the Codex app's `list_projects`, then `create_thread` with:

- `model: "gpt-6-luna"`
- `thinking: "max"`
- `title: "<Area> · <Design scope> · Luna→Claude"`, following the naming rules below.
- The matching project ID. Default to `environment: {type: "worktree"}` for Git projects and `local` otherwise. Use the existing checkout directly only when the user explicitly requests that arrangement. Use `projectless` for a requested standalone artifact without a project.

Use concise English titles. Reuse the parent's product area and name the concrete design scope, such as `Invoices · Editor Design · Luna→Claude` for a parent named `Invoices · Editor & API`, or `Settings · Navigation · Luna→Claude`. Keep model versions, effort levels, and status out of titles. Preserve the existing parent title unless the user requests renaming it. Continue corrections in the same child task rather than creating titles such as “Design v2” or “Final fix”.

Follow the actual tool schema. A worktree starts at the project's default branch unless the user explicitly requests a particular starting state. Do not assume it contains the parent's branch or uncommitted changes. Before implementation, Luna must verify the required files and contracts exist in its checkout. Include missing contracts as explicit design inputs or defer integration until dependencies are available; report an incompatible baseline to Astra before editing. Never silently copy the parent's entire dirty tree.

The dispatch prompt must contain:

- User request, intended audience, primary workflow, relevant references/screenshots, scope, and acceptance criteria.
- Sequencing decision, implementation versus prototype mode, authoritative data/API contracts, and any unresolved dependencies.
- Relevant paths, repository instructions, file ownership, and existing preview location if usable from the worker's checkout.
- Parent task ID and host when available from actual task context; never invent IDs. Resolve the parent via task tools if needed.
- Budget or time limits only if provided by the user.
- Instruction to read this skill's [Luna worker guide](references/luna-worker.md), supervise Claude, and return a compact result to the parent. **Luna must not dispatch another Luna task or re-enter the parent dispatch procedure.**

Pass the worker guide's absolute path, or its contents when the child runs on another host where that path is unavailable. Include concrete instructions in the child prompt; do not assume the child can discover a newly created skill by name.

Creation is asynchronous. If it returns only `clientThreadId`, use app task discovery to resolve the real `threadId`; do not pass the provisional ID to tools requiring a real task ID. Once ready, take one `wait_threads` snapshot with `timeoutMs: 0` to confirm progress. Emit the required `::created-thread{threadId="..."}` or provisional `clientThreadId` directive in the parent response.

Continue useful independent coding in the parent. Avoid repeated polling, blocking waits, or duplicating Luna's supervision. Inspect compact progress when a dependency matters. Do not claim background monitoring unless a real mechanism has been established. Luna's authorized completion message to the parent provides the handoff; no recurring automation is required.

## Integrate the result

Luna returns its actual checkout, changed paths, preview/screenshots, verification evidence, unresolved issues, and Claude session ID. Worktree changes are not automatically present in the parent. Inspect and integrate the scoped diff while preserving other work, then verify affected contracts and flows. A finished design task is not proof of successful integration or user acceptance.

Keep the parent response short: task link, sequencing, work Astra can continue, and later the integrated outcome. Never substitute a native Codex design implementation for the requested Claude implementation without explaining the unavailable dependency.
