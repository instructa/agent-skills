# Sitrep

When several agents work on the same project, I lose track quickly. One is still running,
one finished an hour ago and its result sits in a file nobody has read, and one is waiting
for a login only I can provide. Asking the coordinating agent "what's the status?" usually
gets me a long summary from memory, and the thing that actually needs me is somewhere in
the middle.

`sitrep` (short for situation report) makes the agent collect the state fresh from threads,
run logs, task trackers and review files, and report it in a fixed template. A two-sentence
summary, then everything that needs me, then short tables for the product map, the work in
progress and blockers I can't solve myself. Anything it cannot verify gets a `?`.

Each thing that needs me gets its own number and has to make sense without opening a file.
Decisions spell out the options with their consequences, and the recommended one always
comes first as A. Below it is a short reason and who backs it, for example a second model I
asked for a review, and what happens if I don't answer. So I can reply in one line
like `1 A, 2 done` and the agent knows which answer belongs to which item.

It also flags results nobody has picked up yet. Those are easy to miss and often the
real reason work has stalled.

```text
$sitrep

$sitrep What's blocked right now, and what do you need from me?
```

## Install

```bash
npx skills add instructa/agent-skills --skill sitrep -g
```

Remove `-g` for a project-only installation.
