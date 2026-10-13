---
name: sitrep
description: Status report for a user running several coding agents. Shows product map, active work, blockers and the user's open decisions, each with reviewer positions and a recommendation. Use when the user asks for the current situation, status, or where they are needed.
disable-model-invocation: true
---

# Sitrep

Goal: user sees at a glance what is happening and where they are needed. Collect state fresh; never report from memory. Mark anything you cannot verify with `?`.

## Collect
Use sources that exist; skip missing ones silently. Check project `AGENTS.md`, `CLAUDE.md` or `README.md` for where plans, tasks and run logs live.

- **Agents:** sub-agents, threads, background tasks and worktrees you started or can list with available tools. Active ones: read last message or output.
- **Run logs:** latest entries in project run, coordinator or progress logs.
- **Planning:** open tasks with status in progress, review, blocked or waiting on decision, from the project task tracker (task files, issue tracker, e.g. `gh issue list`, `gh pr list`). Product map: release or roadmap plan, if any.
- **Decision drafts:** pending proposals, review reports and second opinions from other agents or models.
- **Unprocessed results:** result or review file without later log entry waits on coordinator. Real blocker: list it, dispatch it as soon as possible.

## Output
User's language, addressing user as "you". Plain words, no shorthand; IDs only in parentheses. Effort in agent time. Sections in this order; omit empty ones:

**Summary:** two sentences: overall state, most important thing user can do now.

**Product map**
| Area | Status | Next step |

**In progress**
| Who | What | Phase | Remaining |

**Blocked**
| # | What | Blocked by (user, coordinator, environment, provider) | What unblocks it | Answer |

**You decide**
| # | Question | Reviewers | Recommendation | Effort | Answer |

Reviewers cell, per reviewer agent or model: "recommends …", "running", "not asked" or "not needed" (purely operational). Nobody asked although money, legal, security or data affected: say so, offer to ask for a review.

**You deliver:** approvals, logins, sending, real-data acceptance; one numbered line each, ending with expected answer.

### Numbering
- Number every item needing user's answer: one continuous sequence across Blocked, You decide, You deliver (1, 2, 3 …; never restart per section).
- Items not needing user (blocked by coordinator, environment, provider): `#` cell `–`, no number.
- Answer cell: short expected reply, e.g. `yes/no`, `A or B`, `done`, `login done`. Options: label `A`, `B`, …; mark recommended one.
- One question per number. Split compound questions.
- Close with one line: `Reply per number, e.g. "1 yes, 2 B, 3 done".`
- User replies by number: map each answer to its item, act on it, report any number left unanswered or unclear.

End with `Leftovers:` temporary resources still running or left behind (processes, worktrees, containers, temp dirs) with path and reason, or `none`.
