# Find Duplicate Ownership

Duplicate code is usually easy to find. Duplicate ownership is not. The frontend clamps
a value, the API applies a default, and restore code normalizes it again. Each piece looks
reasonable on its own, but together they mean that three places decide what the value is
allowed to be.

I use this skill when a feature survives through glue code: repeated validation, mappings
between persisted and runtime state, helpers with different names but the same job, or
business rules hiding in a cache or query layer. I also run it occasionally across a
larger domain with read-only subagents, because these second owners are easy to miss when
you only inspect the file involved in the current bug.

The point is not to report every repeated transformation. A protocol adapter may need to
translate wire data, and UI formatting belongs near the UI. I want the skill to separate
those real boundaries from rules that can drift. For each real problem it should name the
competing owners, choose one winner, and say what can be deleted.

```text
$find-duplicate-ownership Audit session restore and persistence. Find every place that
owns defaults or repairs the stored shape, then name the canonical owner.
```

The skill also includes [prompts for broader audits](references/audit-prompts.md).

## Install

```bash
npx skills add instructa/agent-skills --skill find-duplicate-ownership -g
```

Remove `-g` for a project-only installation.
