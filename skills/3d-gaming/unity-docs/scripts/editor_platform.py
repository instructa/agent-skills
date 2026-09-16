"""Offline Unity installation discovery and platform-specific tool paths."""
from dataclasses import dataclass
import ctypes
from ctypes import wintypes
import json
import os
from pathlib import Path
import plistlib
import re
import struct
import sys
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class EditorLayout:
    root: Path
    data: Path
    executable: Path
    platform: str

    @property
    def managed(self):
        return first_path([self.data / "Resources/Scripting/Managed",
                           self.data / "Managed"], directory=True)

    @property
    def mono_root(self):
        return first_path([self.data / "Resources/Scripting/MonoBleedingEdge",
                           self.data / "MonoBleedingEdge"], directory=True)

    @property
    def packages(self):
        return self.data / "Resources/PackageManager/BuiltInPackages"


def first_path(paths, directory=False):
    for path in paths:
        if path.is_dir() if directory else path.is_file():
            return path
    raise RuntimeError("Missing Unity artifact; checked: " + ", ".join(map(str, paths)))


def layout(path):
    """Accept an executable, bundle, Editor directory, or version directory."""
    path = Path(path).expanduser()
    for root in (path, *path.parents):
        if root.suffix.lower() == ".app" and (root / "Contents").is_dir():
            return EditorLayout(root, root / "Contents", root / "Contents/MacOS/Unity", "darwin")
        if (root / "Data").is_dir():
            for exe, platform in [("Unity.exe", "win32"), ("Unity", "linux")]:
                if (root / exe).is_file():
                    return EditorLayout(root, root / "Data", root / exe, platform)
    for child in (path / "Unity.app", path / "Editor"):
        if child.is_dir():
            return layout(child)
    raise RuntimeError(f"Not a supported Unity editor installation: {path}")


def hub_roots(platform=None):
    platform = platform or sys.platform
    roots = []
    configured = os.environ.get("UNITY_EDITOR_ROOT")
    if configured:
        roots.append(Path(configured).expanduser())
    if platform == "darwin":
        roots.append(Path("/Applications/Unity/Hub/Editor"))
    elif platform == "win32":
        roots.append(Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Unity/Hub/Editor")
    elif platform.startswith("linux"):
        roots.extend([Path.home() / "Unity/Hub/Editor", Path("/opt/unityhub/editor"),
                      Path("/opt/Unity/Hub/Editor")])
    else:
        raise RuntimeError(f"Unsupported platform: {platform}")
    return roots


def editor_candidates(project, version):
    configured = os.environ.get("UNITY_EDITOR_PATH")
    if configured:
        # An explicit installation must not silently fall back to another editor.
        return [Path(configured).expanduser()]
    candidates = []
    files = [project / "Assembly-CSharp.csproj"]
    if not files[0].is_file():
        files = sorted(project.glob("*.csproj"))[:1]
    for csproj in files:
        if not csproj.is_file():
            continue
        try:
            root = ET.parse(csproj).getroot()
        except ET.ParseError:
            continue
        for element in root.iter():
            if element.tag.rsplit("}", 1)[-1] != "HintPath" or not element.text:
                continue
            text = element.text.strip().replace("\\", "/")
            match = re.search(r"^(.*?/Unity\.app)/Contents/|^(.*?/Editor)/Data/", text)
            if match:
                path = Path(match.group(1) or match.group(2))
                candidates.append(path if path.is_absolute() else project / path)
    candidates.extend(root / version for root in hub_roots())
    if sys.platform.startswith("linux"):
        candidates.append(Path("/opt/unity/Editor"))
    return list(dict.fromkeys(candidates))


def windows_product_version(executable):
    """Read the PE version resource without executing Unity or a shell."""
    api = ctypes.WinDLL("version", use_last_error=True)
    api.GetFileVersionInfoSizeW.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.DWORD)]
    api.GetFileVersionInfoSizeW.restype = wintypes.DWORD
    api.GetFileVersionInfoW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p]
    api.GetFileVersionInfoW.restype = wintypes.BOOL
    api.VerQueryValueW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR,
                                 ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.UINT)]
    api.VerQueryValueW.restype = wintypes.BOOL
    ignored = wintypes.DWORD()
    size = api.GetFileVersionInfoSizeW(str(executable), ctypes.byref(ignored))
    if not size:
        raise RuntimeError(f"No Windows version resource: {executable}")
    buffer = ctypes.create_string_buffer(size)
    if not api.GetFileVersionInfoW(str(executable), 0, size, buffer):
        raise RuntimeError(f"Cannot read Windows version resource: {executable}")
    pointer, length = ctypes.c_void_p(), wintypes.UINT()
    if not api.VerQueryValueW(buffer, r"\VarFileInfo\Translation", ctypes.byref(pointer), ctypes.byref(length)):
        raise RuntimeError(f"No version-resource translation: {executable}")
    translations = ctypes.string_at(pointer, length.value)
    for offset in range(0, len(translations) - 3, 4):
        language, codepage = struct.unpack_from("<HH", translations, offset)
        key = f"\\StringFileInfo\\{language:04x}{codepage:04x}\\ProductVersion"
        if api.VerQueryValueW(buffer, key, ctypes.byref(pointer), ctypes.byref(length)):
            value = ctypes.wstring_at(pointer, max(0, length.value - 1))
            match = re.search(r"\d+\.\d+\.\d+[abfp]\d+", value)
            if match:
                return match.group()
    raise RuntimeError(f"No full Unity ProductVersion in {executable}")


def resource_version(data):
    """Read the build version of editor resources; this cannot prove a revision.

    SerializedFile metadata starts after a 20-byte legacy / 48-byte modern header.
    See Unity-Technologies/UnityDataTools, Documentation/command-serialized-file.md.
    Do not use 'unity default resources': it may be reused from an older patch.
    """
    path = data / "Resources/unity editor resources"
    with path.open("rb") as stream:
        header = stream.read(128)
    if len(header) < 20:
        raise RuntimeError(f"Truncated serialized header: {path}")
    format_version = struct.unpack_from(">I", header, 8)[0]
    if format_version < 9 or format_version > 23:
        raise RuntimeError(f"Unsupported SerializedFile format {format_version}: {path}")
    offset = 48 if format_version >= 22 else 20
    value = header[offset:].split(b"\0", 1)[0].decode("ascii")
    if not re.fullmatch(r"\d+\.\d+\.\d+[abfp]\d+", value):
        raise RuntimeError(f"No Unity version in {path}")
    return value


def editor_identity(editor):
    target = layout(editor)
    if target.platform == "darwin":
        with (target.data / "Info.plist").open("rb") as stream:
            info = plistlib.load(stream)
        return str(info.get("CFBundleVersion", "")), str(info.get("UnityBuildNumber") or "unknown")
    version = (windows_product_version(target.executable) if target.platform == "win32"
               else resource_version(target.data))
    revision = "unknown"
    metadata = target.root.parent / "metadata.hub.json"
    if metadata.is_file():
        record = json.loads(metadata.read_text(encoding="utf-8"))
        value = record.get("revisionHash")
        if isinstance(value, str) and re.fullmatch(r"[a-fA-F0-9]{12,40}", value):
            revision = value
    return version, revision


def find_editor(project, version, revision):
    errors = []
    for candidate in editor_candidates(project, version):
        try:
            target = layout(candidate)
            target.managed
            actual_version, actual_revision = editor_identity(target.root)
            known = revision != "unknown" and actual_revision != "unknown"
            if actual_version != version or (known and not (
                    actual_revision.startswith(revision) or revision.startswith(actual_revision))):
                raise RuntimeError(f"found {actual_version} ({actual_revision}), expected {version} ({revision})")
            return target.root
        except (OSError, ValueError, RuntimeError, plistlib.InvalidFileException) as error:
            errors.append(f"{candidate}: {error}")
    raise RuntimeError("Matching Unity installation unavailable. Set UNITY_EDITOR_PATH to its executable or directory.\n"
                       + "\n".join(errors))


def toolchain(editor):
    target = layout(editor)
    mono_root = target.mono_root
    mono = mono_root / "bin" / ("mono.exe" if target.platform == "win32" else "mono")
    # Invoke the managed compiler directly on all platforms; no .bat/shell quoting.
    compiler = mono_root / "lib/mono/4.5/mcs.exe"
    cecil = first_path([target.data / "Resources/BuildPipeline/Compilation/ApiUpdater/Mono.Cecil.dll",
                        target.managed / "Mono.Cecil.dll",
                        target.data / "Tools/ScriptUpdater/Mono.Cecil.dll"])
    netstandard = first_path([mono_root / "lib/mono/4.7.1-api/Facades/netstandard.dll",
                              mono_root / "lib/mono/4.8-api/Facades/netstandard.dll",
                              mono_root / "lib/mono/4.5/Facades/netstandard.dll"])
    for path in (mono, compiler):
        first_path([path])
    return mono, compiler, cecil, netstandard
