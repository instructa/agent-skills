---
name: lean-ci
description: "Right-size CI from measured run data instead of stacking pipeline mechanics. Use when CI is slow, expensive, flaky, or runs too often; when the user asks to clean up, speed up, split, or reduce GitHub Actions, GitLab CI, or other pipelines; when reviewing a CI proposal for over-engineering; and before you yourself add jobs, caches, matrices, path filters, concurrency rules, nightly runs, pre-push hooks, or test selection to a workflow."
---

# Lean CI

Most CI advice is generic: cache everything, add path filters, cancel stale runs, split into
matrices, run nightly, select tests smartly. Each item sounds cheap, but each one is another
thing to maintain and another way to silently skip a check. Right-sizing CI means finding the
one or two changes that remove most of the measured cost and dropping the rest.

The question that drives everything: **what must CI prove that a developer or agent cannot
prove locally?** That part stays. Everything else should be as fast and as few as possible,
and most of it belongs before the push.

## 1. Measure before proposing

Do not suggest a single change before you have looked at the real data. Collect:

- **Workflows and triggers:** which files run on which events (`push`, `pull_request`,
  `schedule`, `workflow_dispatch`), with or without filters and concurrency.
- **Run history:** e.g. `gh run list --limit 100 --json event,headBranch,status,conclusion,createdAt,updatedAt,headSha`.
  Count runs per day, per event and per branch. Does the team actually use PRs, or does
  everything go straight to one branch?
- **Where the time goes:** step durations from a recent green run (`gh run view <id> --json jobs`).
  Usually two or three steps account for most of the minutes.
- **Why runs fail:** read the failing step of each red run. Group failures by cause, and note
  timing. Failures clustered on one day that then stop point to a real, fixed break, not flakiness.
- **What reaches CI that should have been caught locally:** fast checks (typecheck, boundary or
  lint scripts) that failed in CI are the strongest argument for a local gate.
- **Cost context:** private repos burn paid minutes; public repos mostly cost wait time.
- **What CI already covers:** compare the tested files against the full suite. Often CI already
  runs a subset and the "stop running everything" advice is already satisfied.
- **What depends on CI output:** docs, release notes or plans that cite a run for an exact
  commit, image digests, architecture-specific proof (x64 vs. local ARM), hermetic or
  network-less runs. These are evidence and must keep producing the same proof.

Also read `AGENTS.md`, `CLAUDE.md`, contributing docs and existing hooks, so you know what the
project promises and what it already enforces.

## 2. Separate "what it proves" from "when it runs"

Classify every expensive step:

- **Only CI can prove it** (clean environment, target architecture, release artifact, image
  hardening): keep it unchanged. Move *when* it runs, never *what* it checks.
- **A developer can prove it locally in seconds or minutes:** move it into a local gate and
  keep at most a thin copy in the fast CI job.
- **Nobody relies on it:** diagnostic wrappers from an old investigation, duplicated builds,
  checks whose results are never read. Remove it.

The biggest lever is almost always the same: stop running the expensive proof on every push,
and run it where it is actually needed, such as on the release branch, on PRs into it, or
manually for a release candidate.

## 3. Challenge every proposal, including your own

List each candidate change and give it a verdict tied to the numbers from step 1. A change
survives only if it removes a measured cost that is larger than the maintenance and risk it adds.
Keep the list honest: it is normal for most ideas to be dropped.

Common over-engineering and when it does not pay off:

| Proposal | Usually unnecessary when |
|---|---|
| Path filters on the expensive job | The job already runs only on the release branch or manually. Filter lists rot, and a missing path silently skips a real check. |
| `paths-ignore` for docs | The fast job takes a few minutes and docs-only pushes are a minority. |
| Docker or build layer cache | The expensive job runs rarely, or exact image IDs are part of the evidence. |
| `concurrency: cancel-in-progress` | Per-commit runs serve as proof, or pushes are frequent and cancelling would discard exactly the runs someone needs. |
| Nightly or scheduled runs | A manual `workflow_dispatch` for a release candidate already covers the need. |
| Extra triggers or branch rules | The event never happens (e.g. no PRs in a solo repo). |
| Matrices across versions or OSes | Only one runtime is shipped or supported. |
| AI-driven or heuristic test selection | The domain is high-stakes (finance, security, compliance). Prefer dependency- or path-based selection that is explainable. |
| `--changed` or affected-only test runs in hooks | Tests are integration-heavy (databases, PDFs, containers) and change detection misses the real dependencies. |
| Lint in the hook | CI does not lint either, or the codebase is not lint-clean today. |
| Self-hosted runners, Dagger, remote build farms | A solo or small team has not yet taken the cheap steps; the upkeep outweighs the minutes saved. |
| Investigating or quarantining a "flaky" test | Failures clustered and then stopped, which indicates a real bug that was fixed. |
| Splitting into many small jobs | Setup and install would be repeated for little parallel gain. |

This table is a starting point, not a verdict. If the data shows a case where the mechanism does
pay off, keep it and say why.

## 4. Keep the local gate minimal and enforced

Written instructions do not enforce anything; a hook does. When fast checks escaped to CI:

- Add one script (e.g. `verify`) with only the checks that are fast (roughly under a minute) and
  have actually failed in CI or protect a core promise of the project.
- Call it from a `pre-push` hook, committed in the repo (e.g. `.githooks/`), and activate it
  automatically through the package manager's install/prepare step or equivalent.
- Make sure the script produces any generated files it needs, so it does not fail on stale local
  state.
- Do not add slow suites to the hook. People and agents bypass slow hooks.

## 5. Recommend, then implement only what survived

Present the result before editing anything:

1. The three or four facts that shaped the decision (time split, run counts, failure causes,
   evidence dependencies).
2. A verdict table: each proposal with **keep** or **drop** and a one-line reason from the data.
3. The remaining changes, usually one or two.
4. The explicit trade-off, e.g. "PDF or packaging failures on `develop` now surface on the next
   manual run or on merge, not right after each push."

When implementing:

- Move expensive steps without changing them, so the evidence stays identical.
- Keep the fast job fast; state its expected duration.
- Document the new rules where agents and people read them (`AGENTS.md`, `CLAUDE.md` or the
  contributing guide): which checks run locally, that hooks are not skipped with `--no-verify`,
  how to trigger the expensive proof manually (e.g. `gh workflow run <file> --ref <branch>`), and
  to confirm the run tested the intended commit.
- Validate what you can locally: run the verify script, run the hook, parse the workflow YAML.
  Say clearly that the new workflow has not run on the CI provider until it is pushed.
- Do not commit, push or trigger workflows without the user's go-ahead.
