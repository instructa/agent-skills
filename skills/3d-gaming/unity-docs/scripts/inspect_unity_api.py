#!/usr/bin/env python3
"""Inspect the exact installed Unity editor's public API without network access."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from doc_cache import editor_cache, xml_lookup, metadata_lookup
from editor_platform import find_editor, editor_identity, layout, toolchain


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect exact Unity DLL metadata and matching XML documentation.")
    parser.add_argument("query", help="Type or member name, simple or fully qualified.")
    parser.add_argument(
        "--assembly",
        action="append",
        default=[],
        help="Assembly name or DLL path to inspect; repeat as needed.")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON.")
    parser.add_argument("--max-results", type=int, default=40)
    parser.add_argument("--refresh", action="store_true", help="Rebuild selected cached evidence.")
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Unity project root; otherwise discover it from the current directory.")
    return parser.parse_args()


def find_project_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (
            (candidate / "ProjectSettings" / "ProjectVersion.txt").is_file()
            and (candidate / "Packages" / "manifest.json").is_file()
        ):
            return candidate
    raise RuntimeError(f"No Unity project root was found from {start}")


def project_version(project_root: Path) -> tuple[str, str]:
    version_file = project_root / "ProjectSettings" / "ProjectVersion.txt"
    text = version_file.read_text(encoding="utf-8")
    version_match = re.search(r"^m_EditorVersion:\s*(\S+)", text, re.MULTILINE)
    revision_match = re.search(
        r"^m_EditorVersionWithRevision:\s*\S+\s*\(([^)]+)\)", text, re.MULTILINE)
    if version_match is None:
        raise RuntimeError(f"Missing m_EditorVersion in {version_file}")
    return version_match.group(1), revision_match.group(1) if revision_match else "unknown"


def resolve_assemblies(
    project_root: Path,
    managed: Path,
    requested: list[str],
    inferred: list[Path],
) -> list[Path]:
    resolved: list[Path] = []
    search_roots = [managed, project_root / "Library" / "ScriptAssemblies"]
    for value in requested:
        candidate = Path(value)
        if candidate.is_file():
            resolved.append(candidate.resolve())
            continue
        name = value if value.endswith(".dll") else value + ".dll"
        hits = [path for root in search_roots if root.exists() for path in root.rglob(name)]
        if not hits:
            raise RuntimeError(f"Assembly '{value}' was not found under: {search_roots}")
        resolved.extend(hits)
    if not requested:
        resolved.extend(inferred)
    if not resolved:
        fallback = managed / "UnityEngine" / "UnityEngine.CoreModule.dll"
        if fallback.exists():
            resolved.append(fallback)
    unique: list[Path] = []
    for path in resolved:
        if path not in unique:
            unique.append(path)
    return unique


def helper_paths(
    editor: Path,
    version: str,
    script_dir: Path,
) -> tuple[Path, Path, Path, Path]:
    mono, compiler, cecil, netstandard = toolchain(editor)
    helper_source = script_dir / "UnityApiMetadata.cs"
    digest = hashlib.sha256(
        helper_source.read_bytes()
        + cecil.read_bytes()
        + netstandard.read_bytes()
        + compiler.read_bytes()
        + str(mono).encode("utf-8")
        + version.encode("utf-8")
    ).hexdigest()[:16]
    cache_dir = Path(tempfile.gettempdir()) / "unity-api-inspector" / digest
    cache_dir.mkdir(parents=True, exist_ok=True)
    helper_exe = cache_dir / "UnityApiMetadata.exe"
    if not helper_exe.exists() or helper_exe.stat().st_mtime < helper_source.stat().st_mtime:
        subprocess.run([
            str(mono),
            str(compiler),
            "-nologo",
            "-optimize+",
            "-r:" + str(netstandard),
            "-r:" + str(cecil),
            "-out:" + str(helper_exe),
            str(helper_source),
        ], check=True)
    return mono, cecil, netstandard, helper_exe


def decode(value: str) -> str:
    return base64.b64decode(value).decode("utf-8")


def metadata_matches(
    editor: Path,
    version: str,
    assemblies: list[Path],
    query: str,
    limit: int,
    script_dir: Path,
) -> list[dict]:
    mono, cecil, netstandard, helper_exe = helper_paths(editor, version, script_dir)
    environment = os.environ.copy()
    environment["MONO_PATH"] = os.pathsep.join([str(cecil.parent), str(netstandard.parent)])
    matches: list[dict] = []
    seen: set[tuple[str, str, bool, bool, str]] = set()
    for assembly in assemblies:
        completed = subprocess.run(
            [
                str(mono),
                str(helper_exe),
                str(assembly),
                query,
                str(layout(editor).managed),
                str(netstandard.parent),
            ],
            text=True,
            capture_output=True,
            env=environment,
            check=False,
        )
        if completed.returncode not in (0, 3):
            raise RuntimeError(
                f"Metadata inspection failed for {assembly}:\n{completed.stderr.strip()}")
        for line in completed.stdout.splitlines():
            fields = line.split("\t")
            if len(fields) != 8:
                continue
            kind, assembly_name, fqn, signature, namespace_name, obsolete, obsolete_error, message = (
                decode(field) for field in fields)
            key = (
                kind,
                signature,
                obsolete == "true",
                obsolete_error == "true",
                message,
            )
            if key in seen:
                continue
            seen.add(key)
            matches.append({
                "kind": kind,
                "assembly": assembly_name,
                "fqn": fqn,
                "signature": signature,
                "namespace": namespace_name,
                "obsolete": obsolete == "true",
                "obsoleteIsError": obsolete_error == "true",
                "obsoleteMessage": message,
                "source": str(assembly),
            })
            if len(matches) >= limit:
                return matches
    return matches


def print_text(result: dict) -> None:
    print(f"Unity: {result['unityVersion']} ({result['unityRevision']})")
    print(f"Editor: {result['editor']}")
    print(f"Cache: {result['cache']}")
    if not result["revisionVerified"]:
        print("Revision: unverified (not exposed by the project or installation)")
    for item in result["metadata"]:
        print(f"\n[{item['kind'].upper()}] {item['signature']}")
        print(f"  Assembly: {item['assembly']}")
        print(f"  Namespace: {item['namespace'] or '(global)'}")
        if item["obsolete"]:
            severity = "error" if item["obsoleteIsError"] else "warning"
            print(f"  Obsolete ({severity}): {item['obsoleteMessage'] or '(no message)'}")
        else:
            print("  Obsolete: no")
        print(f"  Source: {item['source']}")
    for item in result["documentation"]:
        print(f"\n[XML] {item['id']}")
        if item["summary"]:
            print(f"  {item['summary']}")
        print(f"  Source: {item['source']}")
    if not result["metadata"] and not result["documentation"]:
        print("\nNo matching API was found in the selected exact-editor sources.")


def main() -> int:
    args = parse_args()
    project_root = (
        args.project_root.resolve()
        if args.project_root is not None
        else find_project_root(Path.cwd().resolve())
    )
    version, revision = project_version(project_root)
    editor = find_editor(project_root, version, revision)
    target = layout(editor)
    managed = target.managed
    _, installed_revision = editor_identity(editor)
    if args.max_results < 1:
        raise RuntimeError("--max-results must be positive")
    cache = editor_cache(editor, version, installed_revision)
    requested_stems = {Path(value).stem for value in args.assembly} if args.assembly else None
    documentation, inferred = xml_lookup(
        cache,
        managed,
        args.query,
        args.max_results,
        requested_stems,
        args.refresh,
    )
    assemblies = resolve_assemblies(project_root, managed, args.assembly, inferred)
    script_dir = Path(__file__).resolve().parent
    # Include dependency assemblies, not just the queried DLL: inherited signatures
    # can change when a referenced assembly is rebuilt.
    dependencies = sorted(set(managed.rglob("*.dll")) |
        set((project_root / "Library" / "ScriptAssemblies").glob("*.dll")) |
        set(assemblies) | {Path(__file__), script_dir / "UnityApiMetadata.cs",
                           script_dir / "doc_cache.py", script_dir / "editor_platform.py"})
    metadata, cache_status = metadata_lookup(
        cache, [args.query, args.max_results, [str(p) for p in assemblies]],
        dependencies,
        lambda: metadata_matches(editor, version, assemblies, args.query,
                                 args.max_results, script_dir),
        args.refresh,
    )
    result = {
        "cache": cache_status,
        "unityVersion": version,
        "unityRevision": installed_revision,
        "projectRevision": revision,
        "revisionVerified": revision != "unknown" and installed_revision != "unknown",
        "platform": target.platform,
        "versionSource": "editor-resources" if target.platform == "linux" else "editor-metadata",
        "editor": str(editor),
        "assembliesInspected": [str(path) for path in assemblies],
        "metadata": metadata,
        "documentation": documentation,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text(result)
    return 0 if metadata or documentation else 3


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exception:
        print(f"unity-api-inspector: {exception}", file=sys.stderr)
        sys.exit(2)
