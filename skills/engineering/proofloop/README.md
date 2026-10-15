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

## Apply across projects

Install it where the agent executes, then add the short
[activation template](assets/AGENTS.md.template.md) to the global instruction source the host actually
loads. Project templates can carry the same activation when global instructions are unavailable.
The template activates the skill; the rules stay in `SKILL.md`.

Verify loading once through the start paths you use, including delegated workers and an existing
and a new project. Installing the skill alone does not require agents to use it. Resolve conflicting
project rules explicitly, and use a supported reload or context update for running sessions.

## Related skills

Proofloop owns test selection and the decision to add lasting tests. Split Orchestrator or the
existing workflow owns roles, review timing, reruns and acceptance. Farcall owns worker transport.
[Consolidate Test Suites](https://github.com/instructa/agent-skills/tree/main/skills/engineering/consolidate-test-suites) owns placement, deduplication and
probe cleanup when that work is needed. They are independently installable. If both apply, reuse
the same test decision and task record; do not create another review or report.

The former bundled command runner remains in
[codex-proofloop](https://github.com/regenrek/codex-proofloop). The skill does not depend on it.
Structural validation does not establish a delivery-speed improvement or unchanged defect detection;
evaluate those through actual tasks and their existing records.

## Research basis

The approach reflects research reviewed on **15 October 2026**, not a claim that current models
make unit tests obsolete or achieve a universal correctness rate.

- [Anthropic, March 2026](https://www.anthropic.com/engineering/harness-design-long-running-apps): stronger models made some evaluator scaffolding unnecessary within their reliable capabilities; actual application use still exposed defects.
- [Testing with AI Agents, March 2026](https://arxiv.org/abs/2603.13724): generated tests contributed coverage comparable to human tests; coverage alone does not establish maintenance value.
- [Beyond Test Presence, July 2026](https://arxiv.org/abs/2607.12068): static analysis found broader boundary checks alongside more potential flakiness in agent tests, not measured runtime flake rates.
- [OpenAI, February 2026](https://openai.com/index/harness-engineering/): an agent-built product used fewer blocking gates and follow-up treatment of some flakes; this is context-specific experience, not permission to ignore failures.

Our policy inference is to require meaningful additional protection before retaining more test
code. These sources do not establish a universal optimal test count or validate this skill's
impact on delivery speed. Assess that impact through real tasks and their existing evidence.
