"""The terminal reference is deterministic, read-only, and installation-local."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from process_environment import child_environment
from test_installers import snapshot

ROOT = Path(__file__).resolve().parents[1]
POWERSHELL = os.name == 'nt' or bool(os.environ.get('NDD_TEST_POWERSHELL'))
UNAVAILABLE = 'version unavailable — incomplete installation'


class HelpTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix='ndd-help-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.skills = self.root / 'installation space Кириллица' / 'skills'
        self.help = self.skills / 'ndd-help'
        shutil.copytree(ROOT / 'skills/ndd-help', self.help)
        self.version = self.skills / 'ndd-setup/VERSION'
        self.version.parent.mkdir()
        self.version.write_text('7.8.9\n')
        self.template = (self.help / 'assets/help.md').read_text(encoding='utf-8')
        self.project = self.root / 'unrelated-project'
        self.project.mkdir()
        (self.project / 'VERSION').write_text('99.99.99')
        (self.project / 'AGENTS.md').write_text('unrelated project instructions')

    def run_help(self, *args: str, success: bool = True) -> str:
        if POWERSHELL:
            command = [os.environ.get('NDD_TEST_POWERSHELL', 'powershell'), '-NoProfile',
                       '-ExecutionPolicy', 'Bypass', '-File',
                       str(self.help / 'scripts/print-help.ps1'), *args]
        else:
            command = [str(self.help / 'scripts/ndd-help'), *args]
        before = snapshot(self.project)
        result = subprocess.run(command, cwd=self.project, capture_output=True,
                                text=True, encoding='utf-8', timeout=15,
                                env=child_environment(command[0]))
        self.assertEqual(snapshot(self.project), before)
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, '')
        else:
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('help text missing or unreadable', result.stderr.lower())
            self.assertEqual(result.stdout, '')
        return result.stdout

    def test_exact_reference_and_extra_arguments(self) -> None:
        expected = self.template.replace('{{VERSION}}', '7.8.9')
        self.assertEqual(self.run_help(), expected)
        self.assertEqual(self.run_help('code', '001'), expected)

    def test_version_whitespace_and_incomplete_installations(self) -> None:
        for content in (' 7.8.9 \r\n', '', ' ', 'bad', '7 .8.9', '7.8.9\n1.2.3'):
            with self.subTest(content=content):
                self.version.write_text(content)
                version = '7.8.9' if content.strip() == '7.8.9' else UNAVAILABLE
                self.assertEqual(self.run_help(), self.template.replace('{{VERSION}}', version))
        self.version.unlink()
        self.assertEqual(self.run_help(), self.template.replace('{{VERSION}}', UNAVAILABLE))

    def test_missing_reference_fails_without_reconstructing_help(self) -> None:
        (self.help / 'assets/help.md').unlink()
        self.run_help(success=False)

    @unittest.skipIf(os.name == 'nt', 'POSIX mode bits')
    def test_unreadable_reference_and_version(self) -> None:
        reference = self.help / 'assets/help.md'
        reference.chmod(0)
        try:
            if os.access(reference, os.R_OK):
                self.skipTest('Runner bypasses permission bits')
            self.run_help(success=False)
        finally:
            reference.chmod(0o644)
        self.version.chmod(0)
        try:
            self.assertEqual(self.run_help(), self.template.replace('{{VERSION}}', UNAVAILABLE))
        finally:
            self.version.chmod(0o644)


if __name__ == '__main__':
    unittest.main()
