---
name: sitrep
description: Status report for a user running several coding agents. MUST read this file before answering whenever a message is or contains "/sitrep", "$sitrep" or "sitrep", also mid-turn. Shows what needs the user's answer first (numbered, self-contained options, recommendation), then product map, active work and blockers.
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
MUST follow template below exactly: these sections, this order, these headings, verbatim (`Needs you`, never `Needs <name>`). Earlier sitreps or status messages in this conversation are NOT a template; NEVER copy their format. Re-read this file each time. NEVER add other sections (no "Done", "Notes", "Open items", "Next", environment stats). Omit empty sections. Detail that matters goes into a table cell or a Needs-you item; everything else is dropped.

User's language, addressing user as "you". Plain words, no shorthand. Task, commit and thread IDs only in parentheses after the plain name, never as the name. Effort in agent time.

```markdown
**Sitrep** · <date time>

**Summary:** <sentence: overall state>. <sentence: most important thing you can do now>.

**Needs you**

1. **<Question in plain words, answerable alone?>**
   <One sentence of context: what this is about and why it is needed now.>
   - **A (recommended)** <option>: <consequence, cost or risk>
   - **B** <option>: <consequence, cost or risk>
   - Why A: <reason in one sentence>. Basis: <who backs it and why, e.g. "review model recommends A because …" or "my assessment, no review">.
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
- Decisions: 2–4 options, each with consequence. Recommended option MUST be **A**, listed first, marked `(recommended)`; others follow as B, C … Relabel options from decision drafts accordingly; draft used other label: add it in parentheses, e.g. `(draft: C)`.
- Why line: one-sentence reason, then Basis: who backs the recommendation and their short reason. Per reviewer agent or model, if any: "recommends A because …", "prefers B because …", "running" or "not asked". Reviewers disagree: say so with both reasons. No reviewer: write "my assessment". Nobody asked although money, legal, security or data affected: say so, offer a review.
- Optional or not-yet-due asks: include only if answer is useful now; mark `(optional)` in the question.
- Reply line gives exact accepted answers.
- User replies by number: map each answer to its item, act on it, report any number left unanswered or unclear.
- Before sending, check every item: could the user answer it without opening a file or asking back? If not, rewrite it. Options unknown because the decision draft is unread: read it first; still unknown: say so and ask the owner agent instead of listing the item.

Wrong:
```markdown
**Needs Alex**
1. ADR 006 A/B/C. I recommend C.
   - Recommendation: **C**. Reviewer: recommends C.
4. Later: reboot window, mail provider, deploy OK.
```

Right:
```markdown
**Needs you**

1. **Which transport should the game server use?** (ADR 006)
   Gameplay phase 4 needs the network layer; this choice fixes it.
   - **A (recommended)** WebSocket now, WebRTC later behind the same interface: ships fast, one migration later. (draft: C)
   - **B** WebSocket over TLS only: simplest, but higher latency for fast duels. (draft: A)
   - **C** WebRTC data channels only: lowest latency, needs a TURN server (cost, setup). (draft: B)
   - Why A: unblocks phase 4 today and keeps WebRTC open. Basis: review model recommends A because latency targets need a WebRTC path later.
   - No answer: phase 4 waits; other work continues.
   - Reply: `1 A`, `1 B` or `1 C`
2. **Which subdomain should the server's TLS certificate use?**
   Needed for the secure WebSocket demo on the server host.
   - Reply: `2 <subdomain>`, e.g. `2 duel.example.com`
```
(Options above illustrate the shape only; always take real options from the decision draft.)

### Tables
- One row per stream, task or area. Cells short: max ~12 words; no sentences chained with commas.
- Who: agent or role, model in parentheses if useful.
- Blocked by: coordinator, environment or provider. Blockers needing user belong in Needs you, not here.
