"""Behaviour tests in disposable directories; never redirect HOME or real agent state.

Uses only Python's standard library. On Windows runs install.ps1; on POSIX runs
install.sh. NDD_TEST_POWERSHELL selects powershell/pwsh for the Windows CI matrix.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
NAMES = ('ndd-setup', 'ndd-spec', 'ndd-plan', 'ndd-do')
WINDOWS = os.name == 'nt'
POWERSHELL = WINDOWS or bool(os.environ.get('NDD_TEST_POWERSHELL'))


def snapshot(root: Path) -> dict[str, tuple[str, bytes | str]]:
    result = {}
    if not root.exists():
        return result
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()):
                result[relative] = ('link', str(path.resolve()))
                if name in dirs:
                    dirs.remove(name)
            elif path.is_dir():
                result[relative] = ('directory', '')
            else:
                result[relative] = ('file', path.read_bytes())
    return result


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix='ndd-test-')
        self.root = Path(self.temporary.name).resolve()
        self.addCleanup(self.temporary.cleanup)
        self.distribution = self.root / 'kit space Кириллица'
        self.distribution.mkdir()
        shutil.copytree(REPO / 'skills', self.distribution / 'skills')
        for name in ('install.sh', 'install.ps1'):
            shutil.copy2(REPO / name, self.distribution / name)
        self.target = self.root / 'user space Кириллица' / 'skills'
        self.other = self.root / 'other-agent' / 'skills'
        self.state = Path(str(self.target) + '.ndd-kit')

    def run_installer(self, *options: str, success: bool = True,
                      environment: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        if POWERSHELL:
            mapping = {'--dry-run': '-DryRun', '--replace': '-Replace', '--link': '-Link',
                       '--uninstall': '-Uninstall', '--codex-dir': '-CodexDir'}
            command = [os.environ.get('NDD_TEST_POWERSHELL', 'powershell'), '-NoProfile',
                       '-ExecutionPolicy', 'Bypass', '-File', str(self.distribution / 'install.ps1'),
                       '-ClaudeDir', str(self.target), *[mapping.get(x, x) for x in options]]
        else:
            command = ['/bin/bash', str(self.distribution / 'install.sh'),
                       '--claude-dir', str(self.target), *options]
        result = subprocess.run(command, text=True, errors='replace', stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                env=environment, timeout=60)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def test_copy_install_and_reinstall(self) -> None:
        source_before = snapshot(self.distribution)
        self.run_installer()
        for name in NAMES:
            self.assertEqual(snapshot(self.target / name), snapshot(self.distribution / 'skills' / name))
            self.assertTrue((self.state / f'{name}.receipt').is_file())
        installed = snapshot(self.target)
        self.run_installer()
        self.assertEqual(snapshot(self.target), installed)
        self.assertEqual(snapshot(self.distribution), source_before)

    def test_both_targets(self) -> None:
        self.run_installer('--codex-dir', str(self.other))
        self.assertEqual(snapshot(self.target), snapshot(self.other))

    def test_dry_run_has_no_writes(self) -> None:
        before = snapshot(self.root)
        self.run_installer('--dry-run')
        self.assertEqual(snapshot(self.root), before)

    def test_uninstall_absent_kit_has_no_writes(self) -> None:
        before = snapshot(self.root)
        self.run_installer('--uninstall')
        self.assertEqual(snapshot(self.root), before)

    def test_partial_distribution_changes_nothing(self) -> None:
        (self.distribution / 'skills/ndd-do/agents/openai.yaml').unlink()
        before = snapshot(self.root)
        self.run_installer(success=False)
        self.assertEqual(snapshot(self.root), before)

    def test_foreign_name_refused_before_any_target_changes(self) -> None:
        foreign = self.other / 'ndd-do'
        foreign.mkdir(parents=True)
        (foreign / 'user.txt').write_text('user work', encoding='utf-8')
        before = snapshot(self.root)
        self.run_installer('--codex-dir', str(self.other), success=False)
        self.assertEqual(snapshot(self.root), before)

    def test_explicit_replace_backs_up_foreign_directory(self) -> None:
        foreign = self.target / 'ndd-spec'
        foreign.mkdir(parents=True)
        (foreign / 'user.txt').write_text('user work', encoding='utf-8')
        self.run_installer('--replace', '--dry-run')
        self.assertTrue((foreign / 'user.txt').exists())
        self.run_installer('--replace')
        backups = list((self.state / 'backups').glob('ndd-spec.*/skill/user.txt'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding='utf-8'), 'user work')

    def test_local_edits_block_update(self) -> None:
        self.run_installer()
        file = self.target / 'ndd-spec/SKILL.md'
        file.write_bytes(file.read_bytes() + b'\nLocal instructions.\n')
        before = snapshot(self.root)
        self.run_installer(success=False)
        self.assertEqual(snapshot(self.root), before)
        self.run_installer('--replace')
        self.assertTrue(any(b'Local instructions.' in p.read_bytes()
                            for p in (self.state / 'backups').glob('ndd-spec.*/skill/SKILL.md')))

    def test_uninstall_preserves_other_skills_and_source(self) -> None:
        self.run_installer()
        custom = self.target / 'ndd-custom'
        custom.mkdir()
        (custom / 'keep.md').write_text('keep')
        source_before = snapshot(self.distribution)
        self.run_installer('--uninstall')
        self.assertEqual([p.name for p in self.target.iterdir()], ['ndd-custom'])
        self.assertEqual(snapshot(self.distribution), source_before)
        self.assertFalse(self.state.exists())
        self.run_installer('--uninstall')
        self.assertEqual((custom / 'keep.md').read_text(), 'keep')

    @unittest.skipIf(POWERSHELL and not WINDOWS, 'Directory junctions require Windows')
    def test_link_uninstall_never_deletes_source(self) -> None:
        source_before = snapshot(self.distribution)
        self.run_installer('--link')
        self.run_installer('--link')  # Old backups now contain links/junctions too.
        for name in NAMES:
            self.assertEqual((self.target / name).resolve(), (self.distribution / 'skills' / name).resolve())
        self.run_installer('--uninstall')
        self.assertEqual(snapshot(self.distribution), source_before)
        self.assertFalse(self.state.exists())

    @unittest.skipIf(POWERSHELL and not WINDOWS, 'Directory junctions require Windows')
    def test_broken_links_can_be_uninstalled(self) -> None:
        self.run_installer('--link')
        source = self.distribution / 'skills/ndd-spec'
        saved = self.distribution / 'saved-source'
        source.rename(saved)
        self.run_installer('--uninstall')
        self.assertTrue((saved / 'SKILL.md').exists())
        self.assertFalse((self.target / 'ndd-spec').exists())
        self.assertFalse((self.target / 'ndd-spec').is_symlink())

    def test_active_lock_blocks_without_removing_existing_lock(self) -> None:
        self.run_installer()
        lock = self.state / 'lock'
        if POWERSHELL:
            lock.write_text('active')
        else:
            lock.mkdir()
        before = snapshot(self.root)
        self.run_installer(success=False)
        self.assertEqual(snapshot(self.root), before)

    def test_modified_receipt_does_not_authorize_deletion(self) -> None:
        self.run_installer()
        (self.state / 'ndd-spec.receipt').write_text('not an NDD receipt')
        before = snapshot(self.root)
        self.run_installer('--uninstall', success=False)
        self.assertEqual(snapshot(self.root), before)

    @unittest.skipIf(WINDOWS, 'POSIX permission/symlink checks; junction coverage is in link tests')
    def test_redirected_target_parent_refused(self) -> None:
        real = self.root / 'real'
        real.mkdir()
        self.target.parent.symlink_to(real, target_is_directory=True)
        self.run_installer(success=False)
        self.assertEqual(list(real.iterdir()), [])

    @unittest.skipIf(POWERSHELL, 'POSIX cp injection; PowerShell has a separate rollback test')
    def test_failure_rolls_back_completed_replacements(self) -> None:
        self.run_installer()
        before_skills = snapshot(self.target)
        before_receipts = {p.name: p.read_bytes() for p in self.state.glob('*.receipt')}
        (self.distribution / 'skills/ndd-setup/VERSION').write_text('0.3.1\n')
        bin_dir = self.root / 'fake-bin'
        bin_dir.mkdir()
        wrapper = bin_dir / 'cp'
        wrapper.write_text('#!/bin/bash\ncase "$2" in */ndd-spec) echo "injected copy failure" >&2; exit 9;; esac\nexec /bin/cp "$@"\n')
        wrapper.chmod(0o755)
        environment = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ['PATH'])
        result = self.run_installer(success=False, environment=environment)
        self.assertIn('injected copy failure', result.stdout)
        self.assertEqual(snapshot(self.target), before_skills)
        self.assertEqual({p.name: p.read_bytes() for p in self.state.glob('*.receipt')}, before_receipts)
        self.assertFalse((self.state / 'lock').exists())
        self.assertEqual(list(self.state.glob('stage.*')), [])

    @unittest.skipUnless(POWERSHELL, 'PowerShell Copy-Item failure injection')
    def test_powershell_failure_rolls_back_completed_replacements(self) -> None:
        self.run_installer()
        before = snapshot(self.target)
        before_receipts = {p.name: p.read_bytes() for p in self.state.glob('*.receipt')}
        (self.distribution / 'skills/ndd-setup/VERSION').write_text('0.3.1\n')
        driver = self.root / 'fail-copy.ps1'
        driver.write_text('''param([string]$Installer, [string]$Target)
function Copy-Item {
    param([string]$LiteralPath, [string]$Destination, [switch]$Recurse, [switch]$Force)
    if ((Split-Path $LiteralPath -Leaf) -eq 'ndd-spec') { throw 'injected copy failure' }
    Microsoft.PowerShell.Management\\Copy-Item @PSBoundParameters
}
& $Installer -ClaudeDir $Target
''')
        result = subprocess.run([os.environ.get('NDD_TEST_POWERSHELL', 'powershell'),
                                 '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(driver),
                                 '-Installer', str(self.distribution / 'install.ps1'), '-Target', str(self.target)],
                                capture_output=True, text=True, errors='replace', timeout=60)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('injected copy failure', result.stderr)
        self.assertEqual(snapshot(self.target), before)
        self.assertEqual({p.name: p.read_bytes() for p in self.state.glob('*.receipt')}, before_receipts)
        self.assertFalse((self.state / 'lock').exists())

    def test_install_inside_distribution_is_rejected(self) -> None:
        self.target = self.distribution / 'nested-skills'
        before = snapshot(self.root)
        self.run_installer(success=False)
        self.assertEqual(snapshot(self.root), before)

    def test_overlapping_targets_are_rejected(self) -> None:
        before = snapshot(self.root)
        self.run_installer('--codex-dir', str(self.target / 'ndd-setup/nested'), success=False)
        self.assertEqual(snapshot(self.root), before)

    @unittest.skipIf(WINDOWS, 'POSIX symlink check')
    def test_redirected_backup_directory_is_rejected(self) -> None:
        self.run_installer()
        backup = self.state / 'backups'
        saved = self.root / 'saved-backups'
        backup.rename(saved)
        backup.symlink_to(saved, target_is_directory=True)
        before = snapshot(self.root)
        self.run_installer(success=False)
        self.assertEqual(snapshot(self.root), before)

    @unittest.skipIf(WINDOWS, 'POSIX mode bits; native Windows ACL test is a manual gate')
    def test_unwritable_destination_changes_nothing(self) -> None:
        self.target.parent.mkdir(parents=True)
        self.target.parent.chmod(0o500)
        try:
            if os.access(self.target.parent, os.W_OK):
                self.skipTest('Runner bypasses directory permission bits')
            before = snapshot(self.root)
            self.run_installer(success=False)
            self.assertEqual(snapshot(self.root), before)
        finally:
            self.target.parent.chmod(0o700)

    def test_uninstall_purges_modified_skills_and_all_state(self) -> None:
        self.run_installer('--codex-dir', str(self.other))
        self.run_installer('--codex-dir', str(self.other))  # Accumulate update backups.
        (self.target / 'ndd-spec/SKILL.md').write_text('local NDD edits', encoding='utf-8')
        project = self.root / 'work-project'
        project.mkdir()
        (project / 'AGENTS.md').write_text('team rules')
        (project / 'spec.md').write_text('project specification')
        project_before = snapshot(project)
        self.run_installer('--uninstall', '--codex-dir', str(self.other))
        for target in (self.target, self.other):
            self.assertEqual(list(target.iterdir()), [])
            self.assertFalse(Path(str(target) + '.ndd-kit').exists())
        self.assertEqual(snapshot(project), project_before)

    def test_uninstall_purges_leftover_state_without_installed_skills(self) -> None:
        self.run_installer()
        self.run_installer()  # State like an old 0.2 uninstall that retained backups.
        for name in NAMES:
            shutil.rmtree(self.target / name)
            (self.state / f'{name}.receipt').unlink()
        stage = self.state / 'stage.interrupted'
        stage.mkdir()
        (stage / 'leftover.txt').write_text('temporary installer data')
        self.run_installer('--uninstall')
        self.assertFalse(self.state.exists())
        self.run_installer('--uninstall')
        self.assertFalse(self.state.exists())

    def test_uninstall_dry_run_preserves_edits_and_backups(self) -> None:
        self.run_installer()
        self.run_installer()
        (self.target / 'ndd-spec/user-note.txt').write_text('local edits')
        before = snapshot(self.root)
        self.run_installer('--uninstall', '--dry-run')
        self.assertEqual(snapshot(self.root), before)

    def test_uninstall_foreign_name_blocks_all_targets(self) -> None:
        self.run_installer()
        foreign = self.other / 'ndd-spec'
        foreign.mkdir(parents=True)
        (foreign / 'user.txt').write_text('not NDD')
        before = snapshot(self.root)
        self.run_installer('--uninstall', '--codex-dir', str(self.other), success=False)
        self.assertEqual(snapshot(self.root), before)

    def test_uninstall_respects_active_lock(self) -> None:
        self.run_installer()
        lock = self.state / 'lock'
        if POWERSHELL:
            lock.write_text('active')
        else:
            lock.mkdir()
        before = snapshot(self.root)
        self.run_installer('--uninstall', success=False)
        self.assertEqual(snapshot(self.root), before)

    @unittest.skipIf(WINDOWS, 'POSIX nested link test; Windows junction backups covered separately')
    def test_uninstall_does_not_follow_nested_or_broken_links(self) -> None:
        self.run_installer()
        external = self.root / 'external-project'
        external.mkdir()
        (external / 'keep.txt').write_text('preserve')
        (self.state / 'backups' / 'external-link').symlink_to(external, target_is_directory=True)
        (self.state / 'backups' / 'broken-link').symlink_to(self.root / 'missing')
        (self.target / 'ndd-do' / 'external-link').symlink_to(external, target_is_directory=True)
        before = snapshot(external)
        self.run_installer('--uninstall')
        self.assertEqual(snapshot(external), before)
        self.assertFalse(self.state.exists())

    @unittest.skipIf(POWERSHELL, 'POSIX delete failure injection')
    def test_uninstall_failure_is_reported_and_retry_finishes_cleanup(self) -> None:
        self.run_installer()
        backups = snapshot(self.state / 'backups')
        bin_dir = self.root / 'fake-bin'
        bin_dir.mkdir()
        wrapper = bin_dir / 'rm'
        wrapper.write_text('#!/bin/bash\ncase "${@: -1}" in */ndd-spec) echo "injected delete failure" >&2; exit 9;; esac\nexec /bin/rm "$@"\n')
        wrapper.chmod(0o755)
        environment = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ['PATH'])
        result = self.run_installer('--uninstall', success=False, environment=environment)
        self.assertIn('Uninstall incomplete', result.stdout)
        self.assertFalse((self.target / 'ndd-setup').exists())
        self.assertTrue((self.target / 'ndd-spec').exists())
        self.assertFalse((self.state / 'lock').exists())
        self.assertEqual(snapshot(self.state / 'backups'), backups)
        self.run_installer('--uninstall')
        self.assertFalse(self.state.exists())

    def test_bundled_templates_work_without_source_or_project_setup(self) -> None:
        self.run_installer()
        shutil.rmtree(self.distribution / 'skills')
        project = self.root / 'work-project'
        project.mkdir()
        (project / 'AGENTS.md').write_text('existing team rules')
        before = snapshot(project)
        for skill, template in (('ndd-spec', 'spec.md'), ('ndd-plan', 'plan.md')):
            asset = self.target / skill / '../ndd-setup/assets' / template
            self.assertTrue(asset.is_file())
            self.assertIn('Acceptance', asset.read_text(encoding='utf-8'))
        self.assertEqual(snapshot(project), before)
        self.run_installer('--uninstall')
        self.assertFalse(self.state.exists())

    @unittest.skipUnless(POWERSHELL, 'PowerShell delete failure injection')
    def test_powershell_uninstall_failure_and_retry(self) -> None:
        self.run_installer()
        before_backups = snapshot(self.state / 'backups')
        driver = self.root / 'fail-delete.ps1'
        driver.write_text('''param([string]$Installer, [string]$Target)
function Remove-Item {
    param([string]$LiteralPath, [switch]$Force, [switch]$Recurse)
    if ((Split-Path $LiteralPath -Leaf) -eq 'SKILL.md' -and
        (Split-Path (Split-Path $LiteralPath -Parent) -Leaf) -eq 'ndd-spec') {
        throw 'injected delete failure'
    }
    Microsoft.PowerShell.Management\\Remove-Item @PSBoundParameters
}
& $Installer -ClaudeDir $Target -Uninstall
''')
        result = subprocess.run([os.environ.get('NDD_TEST_POWERSHELL', 'powershell'),
                                 '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(driver),
                                 '-Installer', str(self.distribution / 'install.ps1'), '-Target', str(self.target)],
                                capture_output=True, text=True, errors='replace', timeout=60)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Uninstall incomplete', result.stdout)
        self.assertIn('injected delete failure', result.stderr)
        self.assertFalse((self.target / 'ndd-setup').exists())
        self.assertFalse((self.state / 'lock').exists())
        self.assertEqual(snapshot(self.state / 'backups'), before_backups)
        self.run_installer('--uninstall')
        self.assertFalse(self.state.exists())


if __name__ == '__main__':
    unittest.main()
