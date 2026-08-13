![Agent Skills banner](publics/agent-skills-banner.webp)

# Agent Skills

Independent, reusable skills for coding agents. Install them with the open
`skills` CLI—no custom installer required.

## Install

List all skills:

```bash
npx skills add instructa/agent-skills --list
```

Install one skill (or copy a command from the table below):

```bash
npx skills add instructa/agent-skills --skill architecture-ownership
```

Use `-g` for a global installation. Supported agents include Codex, Claude Code,
Cursor, and other Agent Skills clients.

## Available Skills

| Category | Skill | Purpose | Install |
|---|---|---|---|
| Engineering | [clarify](skills/engineering/clarify/README.md) | Make complex technical material clear and actionable. | `npx skills add instructa/agent-skills --skill clarify` |
| Engineering | [architecture-ownership](skills/engineering/architecture-ownership/README.md) | Find the right owner for code and behavior. | `npx skills add instructa/agent-skills --skill architecture-ownership` |
| Engineering | [find-duplicate-ownership](skills/engineering/find-duplicate-ownership/README.md) | Find competing sources of truth. | `npx skills add instructa/agent-skills --skill find-duplicate-ownership` |
| Engineering | [hard-cut](skills/engineering/hard-cut/README.md) | Replace legacy paths with one canonical implementation. | `npx skills add instructa/agent-skills --skill hard-cut` |
| Engineering | [root-cause-finder](skills/engineering/root-cause-finder/README.md) | Trace failures to their first unintended cause. | `npx skills add instructa/agent-skills --skill root-cause-finder` |
| Engineering | [consolidate-test-suites](skills/engineering/consolidate-test-suites/README.md) | Put regression coverage in the owning test layer. | `npx skills add instructa/agent-skills --skill consolidate-test-suites` |
| Engineering | [search-context](skills/engineering/search-context/README.md) | Find useful reference repositories before implementing. | `npx skills add instructa/agent-skills --skill search-context` |
| Go | [go-local-health](skills/go/go-local-health/README.md) | Run Go tests, coverage, and lint checks. | `npx skills add instructa/agent-skills --skill go-local-health` |
| Electron | [electron-live-test](skills/electron/electron-live-test/README.md) | Test Electron apps with native-devtools-mcp and CDP. | `npx skills add instructa/agent-skills --skill electron-live-test` |
| Security | [secleak-check](skills/security/secleak-check/README.md) | Scan for secrets and repository risks. | `npx skills add instructa/agent-skills --skill secleak-check` |
| Security | [package-security-check](skills/security/package-security-check/README.md) | Audit JavaScript supply-chain risks. | `npx skills add instructa/agent-skills --skill package-security-check` |
| Shell | [shellck](skills/shell/shellck/README.md) | Run ShellCheck on repository scripts. | `npx skills add instructa/agent-skills --skill shellck` |
| Git | [gitwhat](skills/git/gitwhat/README.md) | Show a concise repository and worktree status. | `npx skills add instructa/agent-skills --skill gitwhat` |
| Release | [homebrew-publish](skills/release/homebrew-publish/README.md) | Prepare and validate Homebrew releases. | `npx skills add instructa/agent-skills --skill homebrew-publish` |
| Specs | [app-spec-packager](skills/specs/app-spec-packager/README.md) | Create implementation-ready application specifications. | `npx skills add instructa/agent-skills --skill app-spec-packager` |
| Design | [redesign-my-landingpage](skills/design/redesign-my-landingpage/README.md) | Build and improve React landing pages. | `npx skills add instructa/agent-skills --skill redesign-my-landingpage` |

## Principles

- Public skills are installed with `npx skills`.
- Core engineering skills do not depend on PlanDB, Planr, Instructa, or AgentRig.
- Tool-specific skills only require tools needed for their stated purpose.
- Category folders do not change public skill names.

## Links

- X/Twitter: [@kregenrek](https://x.com/kregenrek)
- Bluesky: [@kevinkern.dev](https://bsky.app/profile/kevinkern.dev)
- [Instructa](https://www.instructa.ai)
