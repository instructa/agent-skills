![Agent Skills banner](publics/agent-skills-banner.webp)

# Agent Skills

A curated collection of independent, reusable skills for coding agents.

The public skills follow the open Agent Skills layout and are installed with the
open `skills` CLI. Categories organize the repository without changing skill names
or installation commands.

## Install

List all available skills:

```bash
npx skills add instructa/agent-skills --list
```

Install one skill for a specific agent:

```bash
npx skills add instructa/agent-skills --skill architecture-ownership --agent codex
npx skills add instructa/agent-skills --skill architecture-ownership --agent claude-code
npx skills add instructa/agent-skills --skill architecture-ownership --agent cursor
```

Use `-g` for a global installation. Omit it for a project-local installation.
Add `--copy` when copied files are preferable to symlinks.

## Skills

### Engineering

- `architecture-ownership`: determine the runtime, first-fix, and canonical long-term owner.
- `find-duplicate-ownership`: find hidden second sources of truth and contract drift.
- `hard-cut`: replace draft compatibility paths with one canonical implementation.
- `root-cause-finder`: trace downstream failures to the first unintended side effect.
- `consolidate-test-suites`: place regression coverage in one owning test layer.
- `search-context`: find and evaluate high-quality reference repositories before implementing.

### Go

- `go-local-health`: run local Go tests, coverage, and lint health checks.

### Electron

- `electron-live-test`: live-test Electron apps with native-devtools-mcp and CDP.

### Security

- `secleak-check`: scan for secrets, vulnerabilities, and risky repository paths.
- `package-security-check`: audit JavaScript dependency and supply-chain risks.

### Shell

- `shellck`: run ShellCheck over repository shell scripts.

### Git

- `gitwhat`: print a concise branch, status, repository, and worktree snapshot.

### Release

- `homebrew-publish`: prepare and validate Homebrew releases for CLI and TUI projects.

### Specifications

- `app-spec-packager`: create production-ready specification packages for coding agents.

### Design

- `redesign-my-landingpage`: build and critique React, Vite, Tailwind, and shadcn/ui landing pages.

## Repository Layout

Each category is one level below `skills/`, which keeps every skill discoverable by
the open CLI:

```text
skills/
  engineering/
    architecture-ownership/
    find-duplicate-ownership/
    hard-cut/
    root-cause-finder/
    consolidate-test-suites/
    search-context/
  go/
    go-local-health/
  electron/
    electron-live-test/
  security/
    secleak-check/
    package-security-check/
  shell/
    shellck/
  git/
    gitwhat/
  release/
    homebrew-publish/
  specs/
    app-spec-packager/
  design/
    redesign-my-landingpage/
```

## Design Principles

- Canonical engineering skills are product-neutral and have no workflow-platform dependency.
- Tool-specific skills may depend only on tools required for their stated purpose.
- Skills do not require project ledgers, provider capabilities, or proprietary installation flows.
- Public skill names remain stable even when repository categories change.

## Links

- X/Twitter: [@kregenrek](https://x.com/kregenrek)
- Bluesky: [@kevinkern.dev](https://bsky.app/profile/kevinkern.dev)
- Learn Cursor AI: [Ultimate Cursor Course](https://www.instructa.ai/en/cursor-ai)
- Learn to build software with AI: [AI Builder Hub](https://www.instructa.ai)
