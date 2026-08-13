# Root Cause Finder

When an API rejects a null field, the obvious fix is to make the parser accept null. But
sometimes that request should never have been sent. A startup hook wrote stale state, a
restore callback ran twice, or a retry continued after the operation had already ended.
Relaxing the parser makes the error disappear while the actual bug stays alive.

I use `root-cause-finder` whenever the proposed fix changes a schema, type, or contract to
accept something unexpected. It makes the agent trace the path from the intended user
action to the failing request and find the first thing that should not have happened.

This has been especially useful for hydration problems, background writes, mirrored
stores, retries, and lifecycle code. Those paths produce failures several layers away
from their origin, which makes the last error in the log look more important than it is.
A good result shows the causal chain, identifies the first wrong side effect, and says
which layer should be fixed before touching the downstream contract.

```text
$root-cause-finder The API rejects a null project ID during restore. Prove why that
request is sent before changing the API schema.
```

## Install

```bash
npx skills add instructa/agent-skills --skill root-cause-finder -g
```

Remove `-g` for a project-only installation.
