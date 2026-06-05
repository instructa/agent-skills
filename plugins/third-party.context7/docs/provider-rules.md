# Provider Rules

## Ownership

`third-party.context7` is a curated wrapper manifest. Context7 owns its tools and documentation index. AgentRig owns only the capability mapping and safety rules.

## Usage Rules

- Use only for the canonical `docs.latest` capability.
- Prefer explicit library IDs and versions.
- Treat Context7 results as evidence, not final truth.
- Cross-check security-sensitive guidance against official docs or source code.
- Core workflows must remain useful when this provider is absent.

## Security Rules

- Show the exact install/configuration command for the selected target agent.
- Do not send secrets, private code snippets or proprietary data to documentation lookup tools unless the user explicitly approves.
- Warn when results come from community-contributed documentation.
