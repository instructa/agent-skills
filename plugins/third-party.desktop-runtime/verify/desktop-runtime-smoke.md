# Desktop Runtime Smoke Test

1. Confirm the plugin manifest validates against `plugin.v1.json`.
2. Run `agentrig doctor --capability desktop.runtime`.
3. Confirm doctor reports `third-party.desktop-runtime` as the provider for `desktop.runtime`.
4. Show the exact project desktop run command and working directory.
5. Launch only a safe local/dev runtime target.
6. Confirm logs or screenshots can be collected.
7. Confirm production-connected or data-mutating launches require explicit human approval.
