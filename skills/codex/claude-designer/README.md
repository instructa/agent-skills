# Claude Designer

Use `$claude-designer` in Codex when a UI task should be built or improved by Claude Code. Astra chooses whether design or contracts come first, calls Claude Code directly in the current task, then reviews and integrates the result.

Astra checks the Claude process at five-minute intervals until it finishes. See [SKILL.md](SKILL.md) for the workflow and [the direct Claude guide](references/direct-claude-workflow.md) for invocation and review details.

Requires an authenticated Claude Code CLI.

```bash
npx skills add instructa/agent-skills --skill claude-designer -g
```
