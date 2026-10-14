![Proofloop banner](assets/proofloop-banner.png)

# Proofloop

Agents can spend longer building tests and repairing verification machinery than exercising the
feature. Proofloop brings the first real user path forward and makes new permanent tests a deliberate
choice: name the meaningful failure and the gap in existing checks before adding coverage.

Use it while implementing features, fixing bugs or changing tests. It keeps exploratory checks
temporary, distinguishes product failures from test or environment faults, and bounds repeated
attempts. Tests for money, authorization, concurrency and hard-to-reach faults still matter when
the live path does not adequately expose them. Required project checks remain required.

```text
$proofloop Fix this save bug. Exercise save and reload early, reuse the existing checks,
and add a permanent test only for a concrete failure they miss.
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

## Apply across projects

Install it where the agent executes, then add the short
[activation template](assets/AGENTS.md.template.md) to the global instruction source the host actually
loads. Project templates can carry the same activation when global instructions are unavailable.
The template activates the skill; the rules stay in `SKILL.md`.

Verify loading once through the start paths you use, including delegated workers and an existing
and a new project. Installing the skill alone does not require agents to use it. Resolve conflicting
project rules explicitly, and use a supported reload or context update for running sessions.

## Related skills

Proofloop owns early live verification, the decision to add lasting tests and bounded reruns.
[Consolidate Test Suites](https://github.com/instructa/agent-skills/tree/main/skills/engineering/consolidate-test-suites) owns placement, deduplication and
probe cleanup when that work is needed. They are independently installable. If both apply, reuse
the same test decision and task record; do not create another review or report.

The former bundled command runner remains in
[codex-proofloop](https://github.com/regenrek/codex-proofloop). The skill does not depend on it.
Structural validation does not establish a delivery-speed improvement or unchanged defect detection;
evaluate those through actual tasks and their existing records.
