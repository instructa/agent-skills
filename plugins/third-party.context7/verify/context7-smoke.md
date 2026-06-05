# Context7 Smoke Test

1. Confirm the plugin manifest validates against `plugin.v1.json`.
2. Run `agentrig doctor --capability docs.latest`.
3. Confirm doctor reports `third-party.context7` as the provider for `docs.latest`.
4. Query a known public library with an explicit version or library ID.
5. Confirm the result is treated as documentation evidence and not as an automatic code-change authority.
