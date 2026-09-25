# Claude Designer

Use `$claude-designer` in Codex when a UI task should be built or improved by Claude Code. Astra decides whether design or contracts come first, starts a separate GPT-6 Luna max task, and continues independent work. Luna supervises Claude Opus 5.5, checks the result, and reports back for integration.

The created task is titled `<Area> · <Design scope> · Luna→Claude`. See [SKILL.md](SKILL.md) for the workflow and [Luna worker guide](references/luna-worker.md) for the Claude invocation.

Requires Codex desktop task tools and an authenticated Claude Code CLI. Install with:

```bash
npx skills add instructa/agent-skills --skill claude-designer -g
```
