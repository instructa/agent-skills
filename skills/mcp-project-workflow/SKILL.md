---
name: mcp-project-workflow
description: Plan, implement, review, and verify MCP servers, tools, resources, prompts, transports, and agent integrations.
---

# MCP Project Workflow

## Purpose

Ship MCP server and agent integration work with explicit tool contracts, safe permissions, durable planning, current protocol evidence, inspector proof, and secret review.

## Use when

- the project is an MCP server, agent tool integration, resource provider, prompt provider, or transport adapter
- the work changes tool descriptors, schemas, resources, prompts, auth, permissions, transports, server startup, or client integration
- the slice needs MCP Inspector proof, protocol docs, secret scanning, or remote repo context

## Do not use when

- the work is an ordinary HTTP API, backend worker, browser UI, desktop app, or content site
- the task is only to consume an MCP tool from another provider rather than build or verify an MCP integration
- the requested behavior would give model-controlled tools broad filesystem, network, credential, or destructive powers without a clear safety boundary

## Inputs needed

- accepted spec, PlanDB task or fallback ledger context, and proof oracle
- MCP server files, tool/resource/prompt descriptors, schemas, transport config, startup command, auth/env vars, tests, and client config
- expected inspector scenario: tool list, sample invocation, safe inputs, expected outputs, and denied/unsafe path
- secret-bearing config, logs, fixtures, generated descriptors, and package manifests

## Output contract

This skill must produce:

```txt
mcp scope decision
tool/resource contract map
permission and safety map
implementation or review plan
ledger receipt
mcp verification proof
secrets proof
handoff
```

## Workflow

### Phase 0 - Triage

- Confirm the work is MCP scope and not general API or desktop scope.
- Read the current PlanDB task or fallback ledger before changing code.
- Identify every tool, resource, prompt, transport, environment variable, and external system touched by the change.
- Name which operations are read-only, mutating, destructive, credential-touching, or externally visible.

### Phase 1 - Context gathering

- Read the server startup path, descriptor generation, schema validation, handlers, client config, auth, tests, and docs needed for the change.
- Use `docs.latest` for current MCP protocol, SDK, transport, client, or inspector behavior only when needed.
- Prepare safe inspector inputs and expected outputs before invoking tools.
- Identify files and logs that may contain secrets or credentials before verification.

### Phase 2 - MCP analysis

- Treat tool descriptors and schemas as the public contract for model-controlled calls.
- Validate all external inputs at the tool boundary and use typed internal data afterward.
- Check capability and permission phrasing: tools should describe exact effects, scopes, required confirmation, and failure modes.
- Check transport and startup safety: command, cwd, env vars, network exposure, local filesystem scope, and uninstall or cleanup notes.
- Check output safety: no secrets, private file contents, excessive logs, or unstable machine-local paths unless explicitly intended.
- Check denied paths for destructive or broad operations.

### Phase 3 - Action / artifact

- Implement or review the smallest server, descriptor, schema, handler, or config change that satisfies the proof oracle.
- Keep MCP protocol contracts in the MCP project owner and provider/install policy in provider manifests.
- Do not encode provider-specific install assumptions into the project plugin skill.
- Record ledger events when tool contracts, permissions, or verification receipts change durable project state.

### Phase 4 - Verification

- Run focused unit, schema, contract, or smoke tests for changed handlers and descriptors.
- Use `mcp.verify` to inspect the server, list tools/resources/prompts, and run safe sample invocations.
- Run `secrets.scan` proof for descriptors, config, env examples, logs, fixtures, and generated files.
- Verify unsafe or denied operations fail safely when touched.
- Record startup command, transport, inspected surface, sample calls, expected results, and actual results.

### Phase 5 - Final report

- Report the MCP contract owner, changed tools/resources/prompts, permission map, ledger receipt, inspector proof, and secret-scan proof.
- State any manual client integration proof that remains.
- Name human decisions needed for permissions, destructive operations, auth scopes, distribution, or public tool naming.

## Gates / stop conditions

- Stop if PlanDB or fallback ledger context is unavailable for a tool contract or permission change.
- Stop before invoking MCP tools that mutate files, external systems, credentials, billing, or production data without approval.
- Stop if the server requires secrets or credentials the user has not provided safely.
- Stop if descriptor or schema ownership is duplicated between generated and hand-written sources.

## Verification requirements

- Files inspected and changed.
- PlanDB or fallback ledger event/receipt.
- Commands run and exact result.
- MCP Inspector or manual verification path with startup command, transport, tools/resources/prompts inspected, sample inputs, and observed outputs.
- Secrets scan result or documented manual substitute.
- Permission and safety risks.

## Capability use

Required by the plugin:

```txt
plan.ledger
docs.latest
mcp.verify
secrets.scan
```

Optional when installed and relevant:

```txt
repo.remote
```

MCP tools, prompts, resources, transports, SDKs, and clients are workflow context. The capability model stays limited to final capability IDs such as `mcp.verify`.

## Anti-patterns

- Do not expose broad filesystem or network tools without narrow scope and explicit permission language.
- Do not let generated descriptors and hand-written schemas drift.
- Do not call a tool safe because it is local; local MCP tools run with user privileges.
- Do not hide mutations behind read-sounding tool names.
- Do not treat successful startup as proof without listing and invoking the changed tool or resource safely.

## Final report

```txt
Skill: mcp-project-workflow
Decision:
Changed:
Ledger:
Proof:
Inspector:
Security:
Risks:
Next:
```
