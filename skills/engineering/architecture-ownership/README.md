# Architecture Ownership

I built this skill because bugs rarely show up where the underlying rule should live. A
wrong value appears in the UI, so the agent fixes it in a component. The same value is
also used by the API and a worker, so both get their own version of the fix. A small bug
has now created three owners for one decision.

I reach for `architecture-ownership` when a change crosses several layers or when a patch
starts putting product rules into a controller, hook, runtime runner, or provider adapter.
The skill makes the agent look past the nearest editable file and answer a harder
question: which package should make this decision for every caller?

That does not mean the immediate fix and the long-term home must be the same place. The
runtime may need a patch now, while the actual rule belongs in a domain package or shared
core. I want that distinction made explicitly, using the real modules in the repository.
I also want to know which competing implementations can be removed afterwards.

```text
$architecture-ownership This retry policy currently lives in the API handler, but it
also affects the worker and CLI. Where should it live?
```

The [ownership matrix](references/ownership-matrix.md) contains the layer definitions
used by the skill.

## Install

```bash
npx skills add instructa/agent-skills --skill architecture-ownership -g
```

Remove `-g` for a project-only installation.
