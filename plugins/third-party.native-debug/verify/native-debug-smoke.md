# Native Debug Smoke Test

1. Confirm the plugin manifest validates against `plugin.v1.json`.
2. Run `agentrig doctor --capability native.debug`.
3. Confirm doctor reports `third-party.native-debug` as the provider for `native.debug`.
4. Show the exact debugger command and target before running it.
5. Collect a harmless backtrace or crash-report sample from a safe local target.
6. Confirm process attach, privilege escalation and memory inspection require explicit human approval.
