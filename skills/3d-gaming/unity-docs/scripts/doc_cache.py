"""Version-scoped local Unity documentation cache (standard library only)."""
import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sqlite3
import tempfile
from urllib.parse import urlsplit
from urllib.request import urlopen
import xml.etree.ElementTree as ET


ROOT = Path(os.environ.get("UNITY_DOCS_CACHE", "~/.cache/unity-docs")).expanduser()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def stamp(path):
    info = Path(path).stat()
    return [str(Path(path).resolve()), info.st_size, info.st_mtime_ns, info.st_ctime_ns]


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as stream:
        json.dump(value, stream)
        temporary = stream.name
    os.replace(temporary, path)


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def editor_cache(editor, version, revision):
    path = ROOT / "editors" / f"{version}-{revision}" / digest(str(editor))[:12]
    path.mkdir(parents=True, exist_ok=True)
    return path


def xml_lookup(cache, managed, query, limit, allowed=None, refresh=False):
    """Index each XML once; stat checks invalidate only changed/deleted files."""
    db = sqlite3.connect(cache / "xml.sqlite", timeout=30)
    try:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS files(path TEXT PRIMARY KEY, stamp TEXT);
            CREATE TABLE IF NOT EXISTS members(path TEXT, alias TEXT, body TEXT);
            CREATE INDEX IF NOT EXISTS lookup ON members(alias);
            CREATE INDEX IF NOT EXISTS by_path ON members(path);
        ''')
        files = sorted(managed.rglob("*.xml"))
        known = dict(db.execute("SELECT path, stamp FROM files"))
        present = {str(p) for p in files}
        with db:
            for missing in known.keys() - present:
                db.execute("DELETE FROM members WHERE path=?", (missing,))
                db.execute("DELETE FROM files WHERE path=?", (missing,))
            for path in files:
                if allowed is not None and path.stem not in allowed:
                    continue
                signature = json.dumps(stamp(path))
                if not refresh and known.get(str(path)) == signature:
                    continue
                db.execute("DELETE FROM members WHERE path=?", (str(path),))
                try:
                    root = ET.parse(path).getroot()
                except ET.ParseError:
                    continue
                for member in root.findall("./members/member"):
                    name = member.get("name", "")
                    def content(node):
                        return " ".join("".join(node.itertext()).split()) if node is not None else ""
                    body = json.dumps({"id": name, "summary": content(member.find("summary")),
                        "parameters": {p.get("name", ""): content(p) for p in member.findall("param")},
                        "returns": content(member.find("returns")), "source": str(path)})
                    normalized = name[2:].split("(")[0].split("<")[0].lower()
                    parts = normalized.split(".")
                    db.executemany("INSERT INTO members VALUES (?, ?, ?)",
                        [(str(path), ".".join(parts[i:]), body) for i in range(len(parts))])
                db.execute("INSERT OR REPLACE INTO files VALUES (?, ?)", (str(path), signature))
        needle = query.strip().split("(")[0].split("<")[0].lower()
        results, assemblies, seen = [], [], set()
        for path, body in db.execute("SELECT path, body FROM members WHERE alias=? ORDER BY path, rowid", (needle,)):
            if allowed is not None and Path(path).stem not in allowed:
                continue
            item = json.loads(body)
            key = (item["id"], item["summary"])
            dll = Path(path).with_suffix(".dll")
            if dll.exists() and dll not in assemblies:
                assemblies.append(dll)
            if key not in seen:
                seen.add(key)
                results.append(item)
            if len(results) >= limit:
                break
        return results, assemblies
    finally:
        db.close()


def metadata_lookup(cache, key, dependencies, compute, refresh=False):
    path = cache / "metadata" / (digest(key) + ".json")
    stamps = [stamp(p) for p in dependencies]
    record = read_json(path)
    if not refresh and record and record["dependencies"] == stamps:
        return record["result"], "hit"
    result = compute()
    atomic_json(path, {"dependencies": stamps, "result": result})
    return result, "miss"


class PageText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.hidden += 1
        if tag in ("p", "div", "br", "li", "pre", "h1", "h2", "h3", "tr"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def validate_url(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "docs.unity3d.com":
        raise ValueError("Use an HTTPS docs.unity3d.com URL.")
    if not re.match(r"/(?:\d+\.\d+/|Packages/[^/]+@\d+\.\d+[^/]*/)", parsed.path):
        raise ValueError("Use an explicit editor/package version URL; current/latest are not cache targets.")


def web_page(url, refresh=False):
    validate_url(url)
    path = ROOT / "web" / (digest(url) + ".json")
    record = read_json(path)
    if record and not refresh:
        return dict(record, cache="hit")
    with urlopen(url, timeout=30) as response:
        validate_url(response.url)
        if urlsplit(response.url).path != urlsplit(url).path:
            raise ValueError("Documentation redirected to another path; verify its version before caching.")
        page = response.read(8 * 1024 * 1024 + 1)
        if len(page) > 8 * 1024 * 1024:
            raise ValueError("Page exceeds 8 MiB.")
        parser = PageText()
        parser.feed(page.decode(response.headers.get_content_charset() or "utf-8", errors="replace"))
        text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines() if line.strip())
        record = {"url": url, "resolvedUrl": response.url,
            "fetchedAt": datetime.now(timezone.utc).isoformat(), "text": text}
    atomic_json(path, record)
    return dict(record, cache="miss")


def package_sources(project, name):
    """Resolve one package; retain provenance separately for each resolved version."""
    lock = json.loads((project / "Packages/packages-lock.json").read_text(encoding="utf-8"))
    entry = lock["dependencies"][name]
    candidates = [project / "Packages" / name]
    if entry.get("source") == "local" and entry["version"].startswith("file:"):
        candidates.insert(0, (project / "Packages" / entry["version"][5:]).resolve())
    candidates.extend(sorted((project / "Library/PackageCache").glob(name + "@*")))
    if entry.get("source") == "builtin":
        from inspect_unity_api import project_version
        from editor_platform import find_editor, layout
        version, revision = project_version(project)
        editor = find_editor(project, version, revision)
        candidates.append(layout(editor).packages / name)
    matches = []
    for candidate in candidates:
        manifest = read_json(candidate / "package.json")
        if not manifest or manifest.get("name") != name:
            continue
        if entry.get("source") in ("registry", "builtin") and manifest.get("version") != entry["version"]:
            continue
        if entry.get("source") == "git":
            revision = entry.get("hash", "")
            if not revision or not candidate.name.split("@")[-1].startswith(revision[:7]):
                continue
        matches.append({"path": str(candidate.resolve()), "version": manifest.get("version"),
            "documentation": str(candidate / "Documentation~") if (candidate / "Documentation~").is_dir() else None})
        if candidate == project / "Packages" / name or entry.get("source") in ("local", "builtin"):
            break
    record = {"package": name, "resolved": entry, "sources": matches,
        "status": "found" if len(matches) == 1 else "missing" if not matches else "ambiguous"}
    path = ROOT / "packages" / name / digest(entry) / (digest(str(project))[:12] + ".json")
    if read_json(path) != record:
        atomic_json(path, record)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    web = sub.add_parser("web")
    web.add_argument("url")
    web.add_argument("--refresh", action="store_true")
    web.add_argument("--find", help="Print matching paragraphs only.")
    package = sub.add_parser("package")
    package.add_argument("name")
    package.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "package":
        result = package_sources(args.project_root.resolve(), args.name)
    else:
        result = web_page(args.url, args.refresh)
        if args.find:
            result["text"] = "\n".join(line for line in result["text"].splitlines() if args.find.lower() in line.lower())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
