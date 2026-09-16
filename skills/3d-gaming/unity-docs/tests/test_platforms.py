"""Portable fixtures test discovery/tool selection; no Unity install or network."""
import ctypes
import json
import os
from pathlib import Path
import plistlib
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import editor_platform as platform
import inspect_unity_api as inspector
import doc_cache


class PlatformTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "Project & Spaces"
        self.project.mkdir()
        self.version = "6000.0.1f1"
        self.revision = "abcdef123456"
        self.environment = patch.dict(os.environ, {}, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def file(self, path, data=b""):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def editor(self, host):
        version_root = self.root / host / "Hub with spaces" / self.version
        if host == "darwin":
            root = version_root / "Unity.app"
            data = root / "Contents"
            executable = self.file(data / "MacOS/Unity")
            managed = data / "Resources/Scripting/Managed"
            mono = data / "Resources/Scripting/MonoBleedingEdge"
            self.file(data / "Info.plist", plistlib.dumps({
                "CFBundleVersion": self.version, "UnityBuildNumber": self.revision}))
        else:
            root = version_root / "Editor"
            data = root / "Data"
            executable = self.file(root / ("Unity.exe" if host == "win32" else "Unity"))
            managed = data / "Managed"
            mono = data / "MonoBleedingEdge"
            header = bytearray(48)
            struct.pack_into(">I", header, 8, 22)
            self.file(data / "Resources/unity editor resources", bytes(header) + self.version.encode() + b"\0")
        self.file(managed / "UnityEngine/UnityEngine.CoreModule.dll")
        self.file(mono / "bin" / ("mono.exe" if host == "win32" else "mono"))
        self.file(mono / "lib/mono/4.5/mcs.exe")
        self.file(mono / "lib/mono/4.7.1-api/Facades/netstandard.dll")
        self.file(data / "Resources/BuildPipeline/Compilation/ApiUpdater/Mono.Cecil.dll")
        return root, executable, managed

    def test_layouts_executables_and_version_roots(self):
        for host in ("darwin", "win32", "linux"):
            root, executable, managed = self.editor(host)
            for entry in (root, executable, root.parent, managed):
                with self.subTest(host=host, entry=entry):
                    result = platform.layout(entry)
                    self.assertEqual(result.root, root)
                    self.assertEqual(result.platform, host)
                    self.assertEqual(result.managed, managed)
                    self.assertEqual(result.packages, result.data / "Resources/PackageManager/BuiltInPackages")

    def test_toolchain_uses_managed_compiler_on_all_platforms(self):
        for host in ("darwin", "win32", "linux"):
            root, _, _ = self.editor(host)
            mono, compiler, cecil, netstandard = platform.toolchain(root)
            self.assertEqual(mono.name, "mono.exe" if host == "win32" else "mono")
            self.assertEqual(compiler.name, "mcs.exe")
            self.assertTrue(all(p.is_file() for p in (mono, compiler, cecil, netstandard)))
            with patch.object(inspector.subprocess, "run") as run, patch.object(inspector.tempfile, "gettempdir", return_value=str(self.root)):
                inspector.helper_paths(root, self.version, Path(inspector.__file__).parent)
                command = run.call_args.args[0]
                self.assertEqual(command[:2], [str(mono), str(compiler)])
                self.assertFalse(run.call_args.kwargs.get("shell", False))
                self.assertNotIn(str(platform.layout(root).executable), command)

    def test_explicit_mismatch_never_falls_back(self):
        root, executable, _ = self.editor("darwin")
        with patch.dict(os.environ, {"UNITY_EDITOR_PATH": str(executable)}):
            self.assertEqual(platform.find_editor(self.project, self.version, self.revision), root)
            with self.assertRaisesRegex(RuntimeError, "found"):
                platform.find_editor(self.project, "6000.0.2f1", self.revision)
            with self.assertRaisesRegex(RuntimeError, "found"):
                platform.find_editor(self.project, self.version, "111111111111")

    def test_namespaced_hintpaths_and_windows_separators(self):
        root, _, managed = self.editor("win32")
        hint = str(managed / "UnityEngine/UnityEngine.CoreModule.dll").replace("/", "\\")
        (self.project / "Assembly-CSharp.csproj").write_text(
            '<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003"><ItemGroup>'
            '<Reference><HintPath>' + hint + '</HintPath></Reference></ItemGroup></Project>', encoding="utf-8")
        self.assertIn(root, platform.editor_candidates(self.project, self.version))

    def test_default_hub_roots_and_custom_root(self):
        custom = self.root / "custom"
        with patch.dict(os.environ, {"UNITY_EDITOR_ROOT": str(custom), "ProgramFiles": str(self.root / "Program Files")}):
            for host in ("win32", "darwin", "linux"):
                self.assertEqual(platform.hub_roots(host)[0], custom)
            self.assertIn(self.root / "Program Files/Unity/Hub/Editor", platform.hub_roots("win32"))
            self.assertIn(Path.home() / "Unity/Hub/Editor", platform.hub_roots("linux"))

    def test_linux_version_and_unknown_revision(self):
        root, _, _ = self.editor("linux")
        self.assertEqual(platform.editor_identity(root), (self.version, "unknown"))
        with patch.dict(os.environ, {"UNITY_EDITOR_PATH": str(root)}):
            self.assertEqual(platform.find_editor(self.project, self.version, self.revision), root)
        self.file(root.parent / "metadata.hub.json", json.dumps({"revisionHash": self.revision}).encode())
        self.assertEqual(platform.editor_identity(root), (self.version, self.revision))
        self.file(platform.layout(root).data / "Resources/unity editor resources", b"invalid")
        with self.assertRaisesRegex(RuntimeError, "Truncated"):
            platform.editor_identity(root)

    def test_windows_uses_pe_metadata_not_directory_name(self):
        root, exe, _ = self.editor("win32")
        with patch.object(platform, "windows_product_version", return_value=self.version) as read:
            self.assertEqual(platform.editor_identity(root), (self.version, "unknown"))
            read.assert_called_once_with(exe)

    @unittest.skipUnless(sys.platform == "win32", "native Windows version API")
    def test_native_windows_version_resource(self):
        # Python is a real PE file with version info, but not a Unity installation.
        with self.assertRaisesRegex(RuntimeError, "No full Unity ProductVersion"):
            platform.windows_product_version(Path(sys.executable))

    def test_cache_unicode_paths_and_reuse(self):
        root = self.root / "Dokumente ü"
        managed = root / "Managed"
        cache = root / "cache"
        cache.mkdir(parents=True)
        xml = self.file(managed / "Example.xml", b'<doc><members><member name="M:Example.Method"><summary>first</summary></member></members></doc>')
        dll = self.file(managed / "Example.dll", b"dll")
        self.assertEqual(doc_cache.xml_lookup(cache, managed, "Example.Method", 10)[0][0]["summary"], "first")
        with patch.object(doc_cache.ET, "parse", side_effect=AssertionError("XML reparsed")):
            self.assertTrue(doc_cache.xml_lookup(cache, managed, "Example.Method", 10)[0])
        xml.write_bytes(xml.read_bytes().replace(b"first", b"changed"))
        self.assertEqual(doc_cache.xml_lookup(cache, managed, "Example.Method", 10)[0][0]["summary"], "changed")
        self.assertEqual(doc_cache.metadata_lookup(cache, "query", [dll], lambda: ["result"])[1], "miss")
        self.assertEqual(doc_cache.metadata_lookup(cache, "query", [dll], lambda: self.fail("recomputed"))[1], "hit")
        dll.write_bytes(b"different")
        self.assertEqual(doc_cache.metadata_lookup(cache, "query", [dll], lambda: ["new"])[0], ["new"])


if __name__ == "__main__":
    unittest.main()
