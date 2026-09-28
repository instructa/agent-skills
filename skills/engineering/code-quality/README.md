# Code quality

Short implementation & review guidance from the [Marlies workflow experiment](https://kevinkern.dev/benchmarks/marlies-workflows/). The runs exposed repeated mistakes around existing framework features, retries, deleted records & late save responses. Passing tests often missed those sequences.

The skill turns those findings into focused checks. Read the existing implementation before adding another one, keep complexity justified, protect data across retries & make failures visible. Apply only what matters to the change.

It does not assign quality scores or start extra agents. Reviews stay reviews unless fixes are requested. Findings need a concrete trigger, consequence & evidence.

```text
$code-quality Review this change for framework fit, data safety and unnecessary complexity.
```

```text
$code-quality Apply the relevant checks while implementing this feature.
```

## Install

```bash
npx skills add instructa/agent-skills --skill code-quality -g
```

Remove `-g` for a project-only installation. The [skill instructions](SKILL.md) are self-contained and use the project's existing tooling.
