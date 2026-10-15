![Proofloop banner](assets/proofloop-banner.png)

# Proofloop

Proofloop prevents unnecessary test generation in agentic coding. It chooses the smallest
sufficient check for a concrete risk and treats **zero new tests as a valid outcome**.
Generating tests is cheap; running, diagnosing, reviewing and maintaining them still costs time.

Reuse existing coverage unchanged when it is sufficient. Use a direct runtime check or temporary
probe for one-time uncertainty. Add permanent tests when they close a meaningful gap and provide
lasting regression protection. Money, authorization, concurrency and controlled faults still
warrant focused tests where needed. Required project checks remain required.

```text
$proofloop Fix this save bug. Reuse existing coverage, check save and reload in the running
application, and add lasting tests only if they protect an otherwise uncovered recurring risk.
```

## Install

```bash
npx skills add instructa/agent-skills --skill proofloop -g
```

Remove `-g` for a project-only installation. For local development, run
`npx skills add . --skill proofloop -g` from this repository's checkout.

The skill is self-contained; it uses the host's existing
tools. It includes no CLI, Node dependency, policy schema or prescribed reviewer. Hosts such as
Codex, Claude Code and Muse need a supported way to load these instructions; each host's automatic
discovery must be verified separately.
