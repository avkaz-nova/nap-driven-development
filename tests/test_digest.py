"""Cross-platform body-hash contract used to invalidate stale feature plans."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from process_environment import child_environment

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/ndd-plan/scripts'


class DigestTests(unittest.TestCase):
    def digest(self, data: bytes, *, success: bool = True) -> str:
        with tempfile.TemporaryDirectory(prefix='ndd-digest-') as directory:
            path = Path(directory) / 'спецификация space.md'
            path.write_bytes(data)
            if os.name == 'nt' or os.environ.get('NDD_TEST_POWERSHELL'):
                command = [os.environ.get('NDD_TEST_POWERSHELL', 'powershell'), '-NoProfile',
                           '-ExecutionPolicy', 'Bypass', '-File', str(SCRIPTS / 'spec-digest.ps1'), '-Path', str(path)]
            else:
                command = ['/bin/bash', str(SCRIPTS / 'spec-digest.sh'), str(path)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=15,
                                    env=child_environment(command[0]))
            if success:
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout.strip()
            self.assertNotEqual(result.returncode, 0)
            return ''

    def test_lifecycle_metadata_does_not_invalidate_plan(self) -> None:
        body = '# Feature\n\n- R1: Текст.\n'.encode()
        expected = hashlib.sha256(body).hexdigest()
        for status in ('draft', 'approved', 'in-progress', 'done'):
            data = f'---\nstatus: {status}\n---\n'.encode() + body
            self.assertEqual(self.digest(data), expected)

    def test_line_endings_bom_and_final_blank_lines(self) -> None:
        base = b'---\nstatus: approved\n---\n# Feature\n\nR1: behaviour\n'
        expected = self.digest(base)
        for data in (base.replace(b'\n', b'\r\n'), b'\xef\xbb\xbf' + base,
                     base.rstrip(b'\n'), base + b'\n\n'):
            self.assertEqual(self.digest(data), expected)

    def test_changed_requirement_invalidates_plan(self) -> None:
        base = b'---\nstatus: approved\n---\n# Feature\nR1: original\n'
        self.assertNotEqual(self.digest(base), self.digest(base.replace(b'original', b'changed')))

    def test_malformed_or_empty_spec_fails(self) -> None:
        for data in (b'', b'# no metadata\n', b'---\nstatus: approved\n', b'---\n---\n\n'):
            self.digest(data, success=False)


if __name__ == '__main__':
    unittest.main()
