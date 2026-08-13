![Agent Skills banner](publics/agent-skills-banner.webp)

# Agent Skills

Independent, reusable skills for coding agents. Install them with the open
`skills` CLI—no custom installer required.

## Install

List all skills:

```bash
npx skills add instructa/agent-skills --list
```

Install one skill:

```bash
npx skills add instructa/agent-skills --skill architecture-ownership --agent codex
```

Use `-g` for a global installation. Supported agents include Codex, Claude Code,
Cursor, and other Agent Skills clients.

## Available Skills

| Category | Skill | Purpose |
|---|---|---|
| Engineering | `architecture-ownership` | Find the right owner for code and behavior. |
| Engineering | `find-duplicate-ownership` | Find competing sources of truth. |
| Engineering | `hard-cut` | Replace legacy paths with one canonical implementation. |
| Engineering | `root-cause-finder` | Trace failures to their first unintended cause. |
| Engineering | `consolidate-test-suites` | Put regression coverage in the owning test layer. |
| Engineering | `search-context` | Find useful reference repositories before implementing. |
| Go | `go-local-health` | Run Go tests, coverage, and lint checks. |
| Electron | `electron-live-test` | Test Electron apps with native-devtools-mcp and CDP. |
| Security | `secleak-check` | Scan for secrets and repository risks. |
| Security | `package-security-check` | Audit JavaScript supply-chain risks. |
| Shell | `shellck` | Run ShellCheck on repository scripts. |
| Git | `gitwhat` | Show a concise repository and worktree status. |
| Release | `homebrew-publish` | Prepare and validate Homebrew releases. |
| Specs | `app-spec-packager` | Create implementation-ready application specifications. |
| Design | `redesign-my-landingpage` | Build and improve React landing pages. |

## Principles

- Public skills are installed with `npx skills`.
- Core engineering skills do not depend on PlanDB, Planr, Instructa, or AgentRig.
- Tool-specific skills only require tools needed for their stated purpose.
- Category folders do not change public skill names.

## Links

- X/Twitter: [@kregenrek](https://x.com/kregenrek)
- Bluesky: [@kevinkern.dev](https://bsky.app/profile/kevinkern.dev)
- [Instructa](https://www.instructa.ai)
