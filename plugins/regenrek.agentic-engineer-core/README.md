# Agentic Engineer Core

Core skills for agentic software engineering work.

Architecture / Ownership:

- `architecture-ownership`: decide the runtime, first-fix, and canonical long-term owner for behavior in layered codebases.
- `duplicate-ownership-audit`: audit codebases for hidden second sources of truth and contract drift.
- `hard-cut`: enforce one canonical implementation during pre-release or internal-draft refactors.

Debugging / Investigation:

- `root-cause-finder`: trace downstream failures back to the first unintended side effect before changing contracts.
- `search-context`: search external repositories and reference code before guessing.

Testing:

- `test-ownership`: place test coverage in one owning layer and remove weaker duplicate tests.

## Bundle Contents

This directory is the complete portable package root. `plugin.json` contains Agent Plugins v1 metadata, while each declared skill is present under `skills/<name>/SKILL.md`. Registry category, review, provenance, risk, approval, ownership, support, and advisory state remain outside the package.

## Install

Install the complete package through AgentRig for Codex, Claude Code, or Cursor:

```bash
npx agentrig plugin install cursor agentrig/regenrek.agentic-engineer-core
```

AgentRig validates the package before publication and compiles it into provider-native layouts for Codex, Claude Code, and Cursor.
