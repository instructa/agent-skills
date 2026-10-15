# Lean CI

I asked an agent to cut CI cost on a private solo repo and got seven suggestions. Add a
pre-push hook, path filters, concurrency cancellation, docs exclusions, Docker layer
caching, nightly runs, and investigate a supposedly flaky test. Each sounded reasonable,
but I would have ended up maintaining most of that machinery without knowing what it saved.

I use `lean-ci` to make the agent read step timings, run history, and failure causes before
proposing changes. In this case, the Docker/x64 proof job took about 19 of the pipeline's
21 minutes. After measuring, only two changes survived. Run that job on `main` or manually
instead of on every `develop` push, and add a tiny pre-push hook with typecheck and the
boundary check that had escaped to CI twice.

I still needed the expensive job. Release evidence cited its runs for exact commits, and
local checks could not replace its x64 proof. The job had to move, not disappear. Keeping
the same checks meant accepting that failures on `develop` would surface on the next manual
run or merge to `main`.

I reach for this skill when an agent starts making a pipeline more elaborate to make it
cheaper. A useful result shows where the minutes go, which proof must stay, and which one
or two changes are worth maintaining. The remaining suggestions can go.

```text
$lean-ci Cut CI cost in this repo. Measure recent runs, preserve release evidence, and
recommend only the changes that justify their maintenance cost.
```

## Install

```bash
npx skills add instructa/agent-skills --skill lean-ci -g
```

Remove `-g` for a project-only installation.
