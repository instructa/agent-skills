# Clarify

Sometimes an agent gives me a long and technically correct answer, but after reading it I
still do not know what I should do. The recommendation is buried in background, every
option sounds equally reasonable, and the important caveat appears near the end.

That is why I made `clarify`. I use it on an existing answer when I want the actual point
without losing the details that could change the decision. It should remove jargon and
repetition, say which option it recommends, and make the main risk visible. It is not
supposed to turn everything into five cheerful bullet points or hide uncertainty just to
sound decisive.

I often use it after architecture discussions, debugging sessions, or research where the
agent has gathered enough information but has not turned it into something I can approve
or act on.

```text
$clarify Turn the previous answer into something I can approve or reject.

$clarify Explain what this error means, whether it blocks the release, and what I should
do next.
```

## Install

```bash
npx skills add instructa/agent-skills --skill clarify -g
```

Remove `-g` for a project-only installation.
