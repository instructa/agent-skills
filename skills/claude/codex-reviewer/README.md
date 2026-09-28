# Codex Reviewer for Claude Code

Claude implements a change, asks Codex for an independent review, applies justified
corrections and requests verification. Use it in any project, including monorepos,
changes spanning several repositories, and non-Git directories.

The default pairing is **Claude Opus 5.5 high → GPT-6 Astra high review**. The skill
does not switch your active Claude model. It discovers project rules and verification
commands instead of assuming a framework, package manager or application domain.

## Install

Once this skill is published in the repository:

```bash
npx skills add instructa/agent-skills --skill codex-reviewer -g -a claude-code
```

For a local checkout, copy or symlink this folder to
`~/.claude/skills/codex-reviewer`. Personal skills are available across projects.
Requires Python 3.9+, Codex CLI on PATH and a Codex login. No Codex plugin for
Claude Code is required, and no global Codex model configuration is changed.

## Use in Claude Code

```text
/codex-reviewer Implement the requested feature, then have Astra review it.
```

Or review existing work:

```text
/codex-reviewer Review this branch against develop, including the uncommitted changes.
```

Claude supplies the actual assignment, acceptance criteria, code scope and check
results. For UI work, Claude owns browser verification and shares evidence. Astra
reviews read-only and reports findings; Claude makes the fixes. Two correction
rounds are followed by a final verification if needed. Reviews can run through
Claude's background tasks without a model-driven polling loop.

Each invocation preserves the prompt, final report, native JSONL/session/usage
events, stderr, CLI version and exit status in a fresh local output directory.
No review silently commits, pushes, merges or deploys the project.

See [SKILL.md](SKILL.md) and [the review template](references/review-brief.md).

## Relationship to the benchmark

This generalizes the custom `codex exec` workflow from the Marlies workflow
benchmark. It does **not** use Codex's built-in `/review` or its `review_model`
setting. The template adds targeted failure-mode questions learned from the later
readiness recheck; those additions have not been benchmarked as a new workflow.
A clean review is not a release guarantee.

References: [Claude Code skills](https://code.claude.com/docs/en/skills),
[Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode).
