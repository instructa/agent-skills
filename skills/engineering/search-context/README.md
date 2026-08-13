# Search Context

When I work with a framework or platform I do not know well, I like to see how a few good
projects solved the same problem. A normal GitHub search often gives me abandoned demos,
README-only matches, or huge repositories that mention the right keyword but contain no
useful implementation.

I built `search-context` to make that research useful to a coding agent. It searches for
a small set of maintained repositories, shallow-clones the strongest candidates, and
checks the actual files before recommending them. The result is a short manifest that
says what is worth reading, where the relevant code lives, and which candidates were
rejected.

I use it before building an unfamiliar integration, copying a UI pattern from memory, or
committing to an architecture without seeing prior art. For broad product ideas it splits
the search into smaller questions about the stack, domain, and workflow instead of
looking for one mythical repository that matches everything.

The cloned repositories are treated as untrusted reference material. The tool does not
install their dependencies or run their code.

```text
$search-context Find maintained SwiftUI examples of a circular progress ring with
animation. Show me the files that implement it and reject README-only matches.
```

## Install

```bash
npx skills add instructa/agent-skills --skill search-context -g
```

It requires an authenticated `gh`, plus `git`, `rg`, and Node.js 18 or newer. Remove `-g`
for a project-only installation.

To check the setup or run the helper directly from the installed skill directory:

```bash
node scripts/search-context.mjs check
node scripts/search-context.mjs run "SwiftUI circular progress ring" \
  --preset ios-swift \
  --max-repos 5
```

Use `--dry-run` to inspect the search plan without cloning. Existing local reference
repositories can be registered with `library add` and searched together with fresh GitHub
results through `--sources library,github`.
