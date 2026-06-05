# Local Scanners Smoke Test

1. Confirm the plugin manifest validates against `plugin.v1.json`.
2. Run `agentrig doctor --capability secrets.scan`.
3. Run `agentrig doctor --capability supplychain.scan`.
4. Run `agentrig doctor --capability shell.lint`.
5. Confirm doctor reports `third-party.local-scanners` for all three capabilities.
6. Run one harmless project-scoped scanner command for each installed scanner family.
7. Confirm no scan uploads data or expands outside the project without explicit human approval.
