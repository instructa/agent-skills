# Consolidate Test Suites

Every fixed bug seems to invite one more regression file. It feels safe in the moment,
but after a while the same rule is tested in a unit test, an integration test, and an
end-to-end test. Nobody knows which one really protects the behavior, and simple changes
require updating all three.

I use `consolidate-test-suites` after fixing a bug, before asking the agent to add tests.
The first question should be which rule failed, not which test file is easiest to create.
Once that rule is clear, the skill finds the lowest test layer that can prove it and tries
to place the case in an existing suite.

Temporary tests and diagnostics are often useful while investigating a failure, but they
should not become permanent by accident. The skill treats each task-created probe as
something to `PROMOTE`, `MERGE`, or `DROP`: keep only unique durable coverage, merge useful
signal into the canonical suite, and remove the remaining diagnostic residue. Existing
tests and unrelated work are preserved unless duplicate coverage has actually been shown.

This is especially useful when a repository has accumulated ticket-shaped files such as
`issue-423-regression.test.ts`. A useful result tells me which existing test should own
the case and which weaker duplicates can go. Sometimes more than one layer is justified,
but then each test needs to protect a genuinely different failure mode.

```text
$consolidate-test-suites This restore bug is fixed. Where should its regression coverage
live, which temporary probes should survive, and which existing tests can it replace?
```

## Install

```bash
npx skills add instructa/agent-skills --skill consolidate-test-suites -g
```

Remove `-g` for a project-only installation.
