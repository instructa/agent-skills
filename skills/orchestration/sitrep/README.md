# Sitrep

When several agents work on the same project, I lose track quickly. One is still running,
one finished an hour ago and its result sits in a file nobody has read, and one is waiting
for a login only I can provide. Asking the coordinating agent "what's the status?" usually
gets me a long summary from memory, and the thing that actually needs me is somewhere in
the middle.

`sitrep` (short for situation report) makes the agent collect the state fresh from threads,
run logs, task trackers and review files, and report it in a fixed order. A short summary
first, then what is in progress, what is blocked and by whom, which decisions are waiting
on me with what the reviewers recommend, and what only I can deliver. Anything it cannot
verify gets a `?`.

Everything that needs my answer gets one running number with the expected reply next to
it, so I can answer in one line like `1 yes, 2 B, 3 done` and the agent knows which answer
belongs to which item.

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
