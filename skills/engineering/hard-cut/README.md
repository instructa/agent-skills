# Hard Cut

Coding agents are very good at preserving old behavior. Rename a field and they add an
alias. Replace a schema and they keep both parsers. Remove an enum value and they add a
fallback plus tests for the value you wanted gone. This is sensible for a public API, but
inside a pre-release codebase it keeps every draft decision alive forever.

I use `hard-cut` when I have decided that an old internal shape should disappear. The
agent should update producers, consumers, fixtures, tests, and documentation to one final
shape, then delete the compatibility code. I do not want another adapter between two
versions that only ever existed on my branch.

The important boundary is real data. If users already have the old shape on disk, rows in
a database depend on it, or another service consumes the wire format, then this is no
longer a casual cleanup. That boundary needs an explicit migration. The mere existence of
old code is not proof that compatibility is required.

```text
$hard-cut Replace `legacyMode` with the capability enum. Update every live caller and
delete support for the draft boolean shape.
```

## Install

```bash
npx skills add instructa/agent-skills --skill hard-cut -g
```

Remove `-g` for a project-only installation.
