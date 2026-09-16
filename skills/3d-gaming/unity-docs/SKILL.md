---
name: unity-docs
description: Resolve Unity signatures, deprecations, package APIs and behavior using local evidence and official docs.
---

# Unity Docs

Resolve the uncertainty, then stop. Reuse project/version evidence unless the
target changes or sources conflict. Choose one sufficient source: metadata/source
for signatures, docs for behavior. Existing compiler diagnostics and matching
metadata/source outrank prose. Never compile or launch Unity just for docs.

Paths below are relative to this skill's installation. Use Python 3.10+
(`python3`, typically `python` or `py -3` on Windows); quote paths for the shell.
Windows/macOS/Linux detection is automatic.

- Engine: run `scripts/inspect_unity_api.py QUERY` directly; don't reread its code.
  Use a fully qualified type/member, e.g. `UnityEngine.GameObject.SetActive` or
  `UnityEngine.GameObject.activeSelf`; add `--assembly NAME` when known.
  Inspect overloads only as needed. Type queries don't enumerate members;
  no `--members` exists. See `--help` for options.
  Project/editor detection is automatic; outside projects add `--project-root PATH`.
  If discovery fails, set `UNITY_EDITOR_PATH` to the local editor executable or
  installation directory, or `UNITY_EDITOR_ROOT` to its versioned installations'
  parent. `revisionVerified: false` forbids claiming an exact revision match.
  Exit 3 means unresolved, not absent: check spelling, declaring type and assembly,
  then relevant package source/versioned docs. Report remaining uncertainty.
- Packages: `scripts/doc_cache.py package NAME --project-root PATH` resolves local
  sources against the lockfile; search with available tools (`rg` if installed).
  Missing/ambiguous sources aren't verified. Use vendor sources for vendor APIs.
- Explanation: `scripts/doc_cache.py web URL --find TERM`; omit `--find` for full
  text. Use explicitly versioned `docs.unity3d.com` URLs derived from the project
  or resolved package; confirm the page version. Pages retain URL/fetch date and
  are reused until `--refresh`. Browse current release notes/Issue Tracker live.

Persistent XML/metadata cache: `.cache/unity-docs` under the user's home directory;
override with `UNITY_DOCS_CACHE`. Changed sources invalidate evidence;
`--refresh` rebuilds it. Refresh web pages only when freshness matters.

Broaden only for an unresolved gap; don't repeat equivalent searches.
Answer with result and relevant signature/source; version details only when
material. Omit the lookup diary.
