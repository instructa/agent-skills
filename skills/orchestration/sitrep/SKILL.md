---
name: sitrep
description: Status report for a user running several coding agents. Shows what needs the user's answer first, then product map, active work and blockers. Use when the user asks for the current situation, status, or where they are needed.
disable-model-invocation: true
---

# Sitrep

Goal: user sees at a glance where they are needed and can answer everything in one line. Collect state fresh; never report from memory. Mark anything you cannot verify with `?`.

## Collect
Use sources that exist; skip missing ones silently. Read project `AGENTS.md`, `CLAUDE.md` or `README.md` first for where plans, tasks and run logs live.

- **Agents:** sub-agents, threads, background tasks and worktrees you started or can list with available tools. Active ones: read last message or output.
- **Run logs:** latest entries in project run, coordinator or progress logs.
- **Planning:** open tasks with status in progress, review, blocked or waiting on decision, from project task tracker (task files, issue tracker, e.g. `gh issue list`, `gh pr list`). Product map: release or roadmap plan, if any.
- **Decision drafts:** pending proposals, review reports, second opinions from other agents or models. Read them; extract options and consequences.
- **Unprocessed results:** result or review file without later log entry waits on coordinator. Real blocker: list it, dispatch it as soon as possible.

## Output
MUST follow template below exactly: these sections, this order, these headings. NEVER add other sections (no "Done", "Notes", "Open items", "Next", environment stats). Omit empty sections. Detail that matters goes into a table cell or a Needs-you item; everything else is dropped.

User's language, addressing user as "you". Plain words, no shorthand. Task, commit and thread IDs only in parentheses after the plain name, never as the name. Effort in agent time.

```markdown
**Sitrep** · <date time>

**Summary:** <sentence: overall state>. <sentence: most important thing you can do now>.

**Needs you**

1. **<Question in plain words, answerable alone?>**
   <One sentence of context: what this is about and why it is needed now.>
   - **A** <option>: <consequence, cost or risk>
   - **B** <option>: <consequence, cost or risk>
   - Recommendation: **<A|B>**, because <reason>. Reviewers: <reviewer> <position>.
   - No answer: <what happens or stays blocked>.
   - Reply: `1 A` or `1 B`

2. **<Request: login, approval, value, sending, real-data check>**
   <What exactly to do, where, and what it unblocks.>
   - Reply: `2 done` or `2 <value>`

**Product map**

| Area | Status | Next step |
|---|---|---|

**In progress**

| Who | What | Phase | Remaining |
|---|---|---|---|

**Blocked (not by you)**

| What | Blocked by | What unblocks it |
|---|---|---|

Reply per number, e.g. `1 A, 2 done`.

Leftovers: <temporary resources still running or left behind, with path and reason, or none>
```

### Needs-you rules
- One continuous number sequence. One question or request per number; split compound items. NEVER group several asks under one number or a "later" list.
- Each item MUST be understandable without opening any file: name options in full words, never only `A/B/C` or a document ID.
- Decisions: 2–4 options, each with consequence. Always one recommendation with reason.
- Reviewers line, per reviewer agent or model: "recommends …", "running", "not asked". Nobody asked although money, legal, security or data affected: say so in the item, offer review as an option.
- Optional or not-yet-due asks: include only if answer is useful now; mark `(optional)` in the question.
- Reply line gives exact accepted answers.
- User replies by number: map each answer to its item, act on it, report any number left unanswered or unclear.

### Tables
- One row per stream, task or area. Cells short: max ~12 words; no sentences chained with commas.
- Who: agent or role, model in parentheses if useful.
- Blocked by: coordinator, environment or provider. Blockers needing user belong in Needs you, not here.
