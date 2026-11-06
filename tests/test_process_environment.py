import os
import unittest
from unittest.mock import patch

from process_environment import child_environment


class ProcessEnvironmentTests(unittest.TestCase):
    def test_windows_powershell_drops_module_paths_and_preserves_other_values(self) -> None:
        for executable in ('powershell', 'PowerShell.EXE',
                           r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'):
            for key in ('PSModulePath', 'PSMODULEPATH', 'psmodulepath'):
                with self.subTest(executable=executable, key=key):
                    environment = {key: 'PowerShell 7 modules', 'PATH': 'test-bin', 'CUSTOM': 'keep'}
                    original = environment.copy()
                    self.assertEqual(child_environment(executable, environment),
                                     {'PATH': 'test-bin', 'CUSTOM': 'keep'})
                    self.assertEqual(environment, original)

    def test_other_shells_keep_module_paths(self) -> None:
        environment = {'PSModulePath': 'custom modules', 'PATH': 'test-bin'}
        for executable in ('pwsh', 'pwsh.exe', '/opt/bin/pwsh', '/bin/bash'):
            with self.subTest(executable=executable):
                self.assertEqual(child_environment(executable, environment), environment)

    def test_inherited_environment_is_not_modified(self) -> None:
        environment = {'PSModulePath': 'PowerShell 7 modules', 'CUSTOM': 'keep'}
        with patch.dict(os.environ, environment, clear=True):
            # Windows normalizes os.environ keys to uppercase when setting them.
            before = dict(os.environ)
            self.assertEqual(child_environment('powershell'), {'CUSTOM': 'keep'})
            self.assertEqual(dict(os.environ), before)

    def test_explicit_empty_environment_does_not_inherit_parent_values(self) -> None:
        with patch.dict(os.environ, {'CUSTOM': 'parent'}):
            self.assertEqual(child_environment('powershell', {}), {})


if __name__ == '__main__':
    unittest.main()
