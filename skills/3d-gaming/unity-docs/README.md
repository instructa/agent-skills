# Unity Docs

I built this skill to get reliable Unity API answers without sending the agent
through the same documentation searches every time. It checks the editor and
package versions the project actually uses, answers the specific question, and
stops when the evidence is sufficient.

The bundled inspector reads installed DLL metadata and XML documentation. XML
entries are indexed locally, and repeated metadata queries reuse cached results.
The package helper locates sources for the resolved package version. When an
explanation needs a web page, the helper saves that versioned Unity page with its
original URL and fetch date for future local lookups.

```text
$unity-docs Check which overload of this Unity API is available in my project
and whether it is obsolete. Reuse local evidence where available.
```

## Install

```bash
npx skills add instructa/agent-skills --skill unity-docs -g
```

Remove `-g` for a project-only installation. Script paths are resolved from the
installed skill directory, so the skill does not require a particular agent's
global skills folder.

## Requirements

- Python 3.10+; the Python tools use only the standard library.
- A Unity project with `ProjectSettings/ProjectVersion.txt` and package manifests.
- For engine API inspection: the matching Windows, macOS, or Linux Unity Editor,
  including its XML docs, Mono compiler/runtime, Mono.Cecil, and netstandard.
  The inspector builds a small local C# helper; it does not launch Unity.
- Network access for the first web-page fetch or an explicit refresh.

The inspector selects the platform automatically and discovers the editor from
generated project references or the platform's standard Unity Hub directory:

| Platform | Default location | Editor data |
|---|---|---|
| Windows | `%ProgramFiles%/Unity/Hub/Editor/<version>/Editor` | `Data/` |
| macOS | `/Applications/Unity/Hub/Editor/<version>/Unity.app` | `Contents/` |
| Linux | `~/Unity/Hub/Editor/<version>/Editor` | `Data/` |

For custom installations, set `UNITY_EDITOR_PATH` to the editor executable,
`Editor` directory, or `Unity.app`, or set `UNITY_EDITOR_ROOT` to the directory
containing versioned installations. An explicit editor path takes precedence;
a mismatched installation produces an error instead of silently selecting another.

On macOS, identity comes from the app plist; on Windows, from the executable's
ProductVersion resource. Linux uses the version recorded in `unity editor
resources` and reports `versionSource: editor-resources`. Available installation
revision metadata is checked against the project. If either revision is absent,
the result explicitly reports `revisionVerified: false`; directory names alone
are never treated as verified versions.

## Direct use

Set `skill_dir` to the installed skill's directory and run from your Unity project:

```bash
skill_dir="/path/to/installed/unity-docs"
python3 "$skill_dir/scripts/inspect_unity_api.py" \
  UnityEngine.GameObject.SetActive --assembly UnityEngine.CoreModule

python3 "$skill_dir/scripts/doc_cache.py" package com.unity.addressables \
  --project-root "$PWD"
```

For engine lookups outside the project, add `--project-root /path/to/project`.
Use `--json` for structured results and `--max-results` to limit output.
To inspect a property, replace the query with its fully qualified name, such as
`UnityEngine.GameObject.activeSelf`. A type query reports the type itself; it
does not enumerate members, and there is no `--members` option. Run `--help` for
the supported options.

The inspector exits with code `0` when it finds metadata or documentation, `3`
when the selected sources have no match, and `2` for an invalid invocation or
lookup failure. No match does not establish that an API is unavailable: check
the query's spelling, declaring type, and assembly, then use relevant package
sources or versioned documentation if needed.

On Windows, use PowerShell and `python` (or `py -3`):

```powershell
$skill_dir = "C:\path\to\installed\unity-docs"
python "$skill_dir/scripts/inspect_unity_api.py" UnityEngine.GameObject.SetActive --assembly UnityEngine.CoreModule
python "$skill_dir/scripts/doc_cache.py" package com.unity.addressables --project-root "$PWD"
```

To cache a documentation page, supply an explicit editor/package-version URL:

```bash
python3 "$skill_dir/scripts/doc_cache.py" web "$versioned_doc_url" --find SetActive
```

Set `versioned_doc_url` to the matching page on `https://docs.unity3d.com`.
Omit `--find` to read the whole cached text. Unversioned and `@latest` URLs are
rejected; the helper does not download an entire documentation site.

## Cache and freshness

The cache lives under `~/.cache/unity-docs/`; override it with `UNITY_DOCS_CACHE`.
Editor indexes are separated by version, revision, and installation path. XML
changes are detected through file timestamps and size; metadata caches also
check dependency assemblies. Package source records follow the project's lockfile
and available local manifests. Missing or ambiguous sources are reported.

Web pages remain cached until explicitly refreshed. Add `--refresh` to an engine
or web lookup to rebuild its cached evidence. Fresh release status and Issue
Tracker questions still require current sources. A cache entry proves which
sources were available, not that every Unity topic is documented locally.

Only the scripts and instructions are distributed here. Unity documentation and
assemblies are read from the user's installation or fetched on demand.

## Validation

```bash
python3 -B -m unittest discover -s skills/3d-gaming/unity-docs/tests -v
```

Run from the repository root; use `python` on Windows. The tests support
Windows, macOS, and Linux. They cover installation layouts,
version mismatches, compiler command construction, and cache invalidation using
fixtures; they do not install or launch Unity. An actual macOS editor lookup has
also been exercised. Full lookups on real Windows/Linux editors still need native
verification.
