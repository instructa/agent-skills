---
name: clarify
description: Turn complex, technical, ambiguous, or verbose material into clear language without losing important detail. Use when the user asks to simplify an answer, identify what matters, compare options, recommend an action, or make the next step explicit.
---

# Clarify

Make difficult material easy for a capable human to understand and use. Preserve the
facts, constraints, and uncertainty that matter; remove jargon, repetition, and detail
that does not change the conclusion.

## Method

1. Identify whether the user needs to understand, decide, or act.
2. Lead with the answer or practical meaning.
3. Explain unavoidable technical terms the first time they appear.
4. Keep details only when they affect understanding, confidence, risk, or action.
5. If there is a decision, recommend one default and name the main tradeoff.
6. End with a concrete next step when the user needs to act.

## Writing rules

- Match the user's language and level of technical detail.
- Prefer concrete words, active voice, short paragraphs, and one idea per sentence.
- Preserve important numbers, citations, constraints, and caveats.
- Separate verified facts from assumptions and unknowns when the distinction matters.
- State what would change the recommendation when useful.
- Use headings or a small table only when they make the answer faster to understand.
- Do not bury the answer in background or present weak alternatives as equal choices.

## When rewriting existing material

- Preserve supported facts and meaningful uncertainty.
- Combine repeated or scattered points.
- Flag contradictions instead of silently resolving them.
- Translate system or agent terminology into consequences for the user.
- Return the improved answer, not a critique of the original writing.

## Suggested shape

Use only the parts the task needs:

```markdown
**Bottom line:** [Direct answer or recommendation.]

**Why:** [The few reasons that change the conclusion.]

**Risk or unknown:** [Only if material.]

**Next step:** [One concrete action, if needed.]
```

Do not force this template when a short paragraph is clearer.
