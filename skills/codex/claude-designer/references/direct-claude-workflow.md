# Direct Claude workflow for Astra

Astra uses this guide in the current task. Astra owns the brief, Claude process, visual inspection, focused corrections, and integration. Do not create a separate Codex worker task or delegate the work through another model.

## Prepare a bounded brief

Confirm the current checkout and baseline. Read relevant project instructions, installed component and framework versions, existing styles, and data contracts. Preserve unrelated changes. If Astra is changing backend files in parallel, agree on file ownership before Claude edits shared components or translations. Never restart another task's preview server.

Describe the user outcome, journey, design direction, target routes, allowed files, authoritative contracts, and observable acceptance criteria. Ask Claude to implement the requested work, including a new interface when required; do not reduce a build request to an audit or mockup.

Treat “2026 best practices” as current, verified guidance applied to this product, not a visual trend checklist. Consult relevant primary documentation when a decision depends on it. Start with:

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/): aim for AA where applicable; verify concrete keyboard, focus, contrast, reflow, labeling, and target-size behaviors. Do not claim full conformance from a screenshot.
- The installed design system's official documentation; [shadcn/ui](https://ui.shadcn.com/docs) only when used or requested. Prefer the project's existing primitives and tokens.
- The installed framework's official documentation for routing, data loading, and accessibility-sensitive components. Check version compatibility before adopting examples.

Focus on the actual experience: readable hierarchy and typography, coherent spacing, discoverable actions, responsive navigation, useful density, and clear feedback. Account for applicable loading, empty, error, success, validation, disabled, long-content, and unsaved-change states. Keep labels and translations consistent. Use motion purposefully and respect reduced-motion preferences. For charts, use truthful units and accessible alternatives; evaluate loading cost before adding libraries.

Preserve established behavior and domain rules unless the task explicitly changes them. Missing APIs are dependencies to resolve or report. Synthetic data belongs in clearly identified previews/fixtures, never in production metrics. Existing backend logic, entitlements, licensing, and extension boundaries remain authoritative.

## Invoke and supervise Claude Code

Check `claude --version`, `claude --help`, and `claude auth status` without printing credentials. Do not install, update, log in, or switch models silently. If a prerequisite is unavailable, report the exact blocker.

Use the configured Claude Code model unless the user requests a specific model. Check the installed CLI help for supported flags. Write the exact brief to a task-specific file outside versioned source. From the assigned checkout, launch Claude with stdin and separate stdout/stderr files. Adapt this shell template to the installed CLI and the task's authorized scope:

When a verified direct Claude worker MCP tool is available, use it instead of the shell launch below. Pass the same brief, working directory, model/permission choices and exact session ID for resumes. The tool must await worker completion, not merely return a job ID for repeated status queries. Invoke it directly outside Code Mode.

```sh
claude -p \
  --permission-mode acceptEdits \
  --permission-prompts none \
  --output-format json \
  < /absolute/task-artifacts/brief.txt \
  > /absolute/task-artifacts/result.json \
  2> /absolute/task-artifacts/claude.stderr.log
```

The selected permission mode accepts edits; other tools may be denied. Use already authorized, narrowly scoped tool permissions where needed, or perform authorized checks yourself. Do not repeatedly retry a denied operation or add `--dangerously-skip-permissions` unless permission bypass was explicitly authorized for this run.

### Completion waiting

Keep the process handle and Claude session ID. Prefer a host-side wait that returns on completion, failure or a required decision without intermediate parent-model status turns. Do not use repeated sleeps, clock checks, log tails or status requests as the normal supervision workflow. Independent useful work is allowed within the agreed ownership boundaries.

For Codex hosts supporting it, `[features.code_mode].direct_only_tool_namespaces` keeps an exact MCP namespace top-level and out of nested Code Mode. The local reserved name is `mcp__claude_worker`; verify the actual exposed namespace before relying on it. The MCP server must be installed separately and its tool timeout must cover the run. Increasing an MCP timeout alone does not remove an outer Code Mode yield.

If no verified completion mechanism is available, state that before dispatch. Do not silently replace it with a polling loop or claim zero polling overhead. The shell example remains a launch fallback for an explicitly accepted polling-based workflow; obey the current host's waiting limits and preserve the resulting usage. A prompt cannot change tool transport behavior.

Before labeling a setup polling-free, test a slow deterministic worker across the normal yield interval and inspect actual parent response IDs. Test timeout/cancellation recovery without launching duplicate workers. Configuration persistence is not runtime proof. On this machine, the benchmark protocol and research are at `/Users/devbook/projects/marlies-workflow-benchmark-kit/protocols/event-driven-v1/`.

When Claude completes, inspect the exit status, result subtype, errors/permission denials, actual filesystem changes, and any session ID or usage metadata the runtime provides. Report only measured usage fields. For focused corrections, resume the same Claude session with its returned session ID and a new brief/result file; do not start duplicate work while the original process is alive. Stop after one focused correction fails with the same issue and explain the blocker.

Stable instructions and tool configuration can improve cache reuse. Session continuation alone does not guarantee cache hits; models/providers do not share their KV caches. Avoid resending full transcripts, repeated repository analysis, or large logs. Never claim API list-price savings as measured subscription savings.

## Review and integrate

Inspect the actual diff independently of Claude's summary. Verify the requested user journey in a browser when available, including narrow and wide viewports, relevant breakpoints, keyboard operation, and applicable populated/error/empty states. Use an isolated preview and synthetic data when needed. Save useful screenshots and the preview URL with checkout/port information. If browser tooling, dependencies, or data are unavailable, report what remains unverified; do not equate a successful build with verified design quality.

Send concrete visual or behavioral defects to Claude in its existing session. Avoid unlimited aesthetic iteration. Integrate the scoped changes into the current task while preserving unrelated work. Do not commit, push, or deploy unless explicitly authorized.

Report the result, acceptance status, changed paths, preview/screenshots, checks actually executed, remaining gaps, API dependencies or architectural decisions, and Claude session ID. Keep the report concise and state which evidence is local versus externally accepted.
