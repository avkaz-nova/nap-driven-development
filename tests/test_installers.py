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
from unittest.mock import patch

from process_environment import child_environment

REPO = Path(__file__).resolve().parents[1]
NAMES = ('ndd-setup', 'ndd-spec', 'ndd-plan', 'ndd-do', 'ndd-help', 'ndd-review')
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
        self.registry_state = self.root / 'ndd-state'
        self.enterContext(patch.dict(os.environ, NDD_STATE_DIR=str(self.registry_state)))
        self.distribution = self.root / 'kit space Кириллица'
        self.distribution.mkdir()
        shutil.copytree(REPO / 'skills', self.distribution / 'skills')
        for name in ('install.sh', 'install.ps1'):
            shutil.copy2(REPO / name, self.distribution / name)
        self.target = self.root / 'user space Кириллица' / 'skills'
        self.other = self.root / 'other-agent' / 'skills'
        self.state = Path(str(self.target) + '.ndd-kit')

    def run_installer(self, *options: str, success: bool = True,
                      environment: dict[str, str] | None = None,
                      working_directory: Path | None = None) -> subprocess.CompletedProcess[str]:
        if POWERSHELL:
            mapping = {'--dry-run': '-DryRun', '--replace': '-Replace', '--link': '-Link',
                       '--uninstall': '-Uninstall', '--codex-dir': '-CodexDir',
                       '--keep-source': '-KeepSource'}
            command = [os.environ.get('NDD_TEST_POWERSHELL', 'powershell'), '-NoProfile',
                       '-ExecutionPolicy', 'Bypass', '-File', str(self.distribution / 'install.ps1'),
                       '-ClaudeDir', str(self.target), *[mapping.get(x, x) for x in options]]
        else:
            command = ['/bin/bash', str(self.distribution / 'install.sh'),
                       '--claude-dir', str(self.target), *options]
        result = subprocess.run(command, text=True, errors='replace', stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                env=child_environment(command[0], environment),
                                cwd=working_directory, timeout=60)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def source_git(self, *args: str) -> str:
        # Synthetic history only, with no real user identity/config/hooks or network.
        environment = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
        environment.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1',
                           GIT_AUTHOR_NAME='NDD Test', GIT_AUTHOR_EMAIL='ndd@example.invalid',
                           GIT_COMMITTER_NAME='NDD Test', GIT_COMMITTER_EMAIL='ndd@example.invalid')
        result = subprocess.run(['git', '-C', str(self.distribution), *args], env=environment,
                                capture_output=True, text=True, errors='replace', timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def prepare_source_clone(self) -> None:
        self.source_git('init', '--quiet', '--template=')
        self.source_git('config', '--local', 'core.autocrlf', 'false')
        self.source_git('add', '.')
        self.source_git('commit', '--quiet', '-m', 'Synthetic NDD distribution')
        self.source_git('remote', 'add', 'origin', 'https://github.com/avkaz/nap-driven-development.git')
        self.source_git('update-ref', 'refs/remotes/origin/main', 'HEAD')

    def test_all_uninstall_removes_clean_source_clone(self) -> None:
        self.prepare_source_clone()
        self.run_installer('--codex-dir', str(self.other))
        project = self.root / 'work-project'
        project.mkdir()
        (project / 'spec.md').write_text('keep project documents')
        result = self.run_installer('--uninstall', '--codex-dir', str(self.other),
                                    working_directory=self.distribution)
        self.assertIn('Removed source clone:', result.stdout)
        self.assertFalse(self.distribution.exists())
        for target in (self.target, self.other):
            self.assertFalse(Path(str(target) + '.ndd-kit').exists())
            self.assertEqual(list(target.iterdir()), [])
        self.assertEqual((project / 'spec.md').read_text(), 'keep project documents')

    def test_clean_clone_without_remaining_install_state_is_removed(self) -> None:
        self.prepare_source_clone()
        self.run_installer('--uninstall', '--codex-dir', str(self.other))
        self.assertFalse(self.distribution.exists())

    @unittest.skipIf(POWERSHELL and not WINDOWS, 'Directory junctions require Windows')
    def test_all_link_uninstall_also_removes_clean_source(self) -> None:
        self.prepare_source_clone()
        self.run_installer('--link', '--codex-dir', str(self.other))
        self.run_installer('--uninstall', '--codex-dir', str(self.other))
        self.assertFalse(self.distribution.exists())
        for target in (self.target, self.other):
            self.assertEqual(list(target.iterdir()), [])
            self.assertFalse(Path(str(target) + '.ndd-kit').exists())

    def test_source_cleanup_dry_run_is_read_only(self) -> None:
        self.prepare_source_clone()
        self.run_installer('--codex-dir', str(self.other))
        before = snapshot(self.root)
        result = self.run_installer('--uninstall', '--codex-dir', str(self.other), '--dry-run')
        self.assertIn('Permanently remove source clone after uninstall:', result.stdout)
        self.assertEqual(snapshot(self.root), before)

    def test_keep_source_preserves_clean_clone(self) -> None:
        self.prepare_source_clone()
        self.run_installer('--codex-dir', str(self.other))
        before = snapshot(self.distribution)
        self.run_installer('--uninstall', '--codex-dir', str(self.other), '--keep-source')
        self.assertEqual(snapshot(self.distribution), before)
        self.assertFalse(self.state.exists())

    def test_keep_source_requires_uninstall(self) -> None:
        before = snapshot(self.root)
        self.run_installer('--keep-source', success=False)
        self.assertEqual(snapshot(self.root), before)

    def test_one_agent_uninstall_keeps_clone(self) -> None:
        self.prepare_source_clone()
        self.run_installer('--codex-dir', str(self.other))
        before = snapshot(self.distribution)
        self.run_installer('--uninstall')
        self.assertEqual(snapshot(self.distribution), before)
        self.assertTrue((self.other / 'ndd-setup/SKILL.md').is_file())

    def test_uninstall_keeps_local_source_changes(self) -> None:
        self.prepare_source_clone()
        self.run_installer('--codex-dir', str(self.other))
        file = self.distribution / 'skills/ndd-spec/SKILL.md'
        file.write_bytes(file.read_bytes() + b'\nLocal source work.\n')
        before = snapshot(self.distribution)
        result = self.run_installer('--uninstall', '--codex-dir', str(self.other))
        self.assertIn('clone contains local changes', result.stdout)
        self.assertEqual(snapshot(self.distribution), before)
        self.assertFalse(self.state.exists())

    def test_uninstall_keeps_untracked_and_ignored_source_files(self) -> None:
        self.prepare_source_clone()
        for ignored in (False, True):
            with self.subTest(ignored=ignored):
                note = self.distribution / 'personal-note.txt'
                note.write_text('keep even when ignored')
                if ignored:
                    exclude = self.distribution / '.git/info/exclude'
                    exclude.parent.mkdir(exist_ok=True)
                    exclude.write_text('personal-note.txt\n')
                self.run_installer('--codex-dir', str(self.other))
                before = snapshot(self.distribution)
                self.run_installer('--uninstall', '--codex-dir', str(self.other))
                self.assertEqual(snapshot(self.distribution), before)
                note.unlink()

    def test_uninstall_keeps_unpublished_source_history(self) -> None:
        self.prepare_source_clone()
        note = self.distribution / 'committed-work.txt'
        note.write_text('unpublished work')
        self.source_git('add', '.')
        self.source_git('commit', '--quiet', '-m', 'Local work')
        self.run_installer('--codex-dir', str(self.other))
        before = snapshot(self.distribution)
        result = self.run_installer('--uninstall', '--codex-dir', str(self.other))
        self.assertIn('history not present', result.stdout)
        self.assertEqual(snapshot(self.distribution), before)

    def test_uninstall_keeps_source_with_hidden_index_changes(self) -> None:
        self.prepare_source_clone()
        file = self.distribution / 'install.sh'
        original = file.read_bytes()
        for flag in ('assume-unchanged', 'skip-worktree'):
            with self.subTest(flag=flag):
                self.source_git('update-index', '--' + flag, 'install.sh')
                file.write_bytes(original + b'\n# Hidden local work\n')
                self.run_installer('--codex-dir', str(self.other))
                before = snapshot(self.distribution)
                result = self.run_installer('--uninstall', '--codex-dir', str(self.other))
                self.assertIn('source index can hide changes', result.stdout)
                self.assertEqual(snapshot(self.distribution), before)
                self.source_git('update-index', '--no-' + flag, 'install.sh')
                file.write_bytes(original)

    def test_uninstall_keeps_stashed_source_work(self) -> None:
        self.prepare_source_clone()
        file = self.distribution / 'install.sh'
        file.write_bytes(file.read_bytes() + b'\n# Stashed source work\n')
        self.source_git('stash', 'push', '--quiet')
        self.run_installer('--codex-dir', str(self.other))
        before = snapshot(self.distribution)
        self.run_installer('--uninstall', '--codex-dir', str(self.other))
        self.assertEqual(snapshot(self.distribution), before)

    def test_uninstall_keeps_unrelated_repository(self) -> None:
        self.prepare_source_clone()
        self.source_git('remote', 'set-url', 'origin', 'https://example.invalid/team/project.git')
        self.run_installer('--codex-dir', str(self.other))
        before = snapshot(self.distribution)
        result = self.run_installer('--uninstall', '--codex-dir', str(self.other))
        self.assertIn('origin is not the NDD repository', result.stdout)
        self.assertEqual(snapshot(self.distribution), before)

    def test_uninstall_keeps_clone_with_linked_worktree(self) -> None:
        self.prepare_source_clone()
        worktree = self.root / 'linked-worktree'
        self.source_git('worktree', 'add', '--quiet', '--detach', str(worktree), 'HEAD')
        self.run_installer('--codex-dir', str(self.other))
        before_source = snapshot(self.distribution)
        before_worktree = snapshot(worktree)
        self.run_installer('--uninstall', '--codex-dir', str(self.other))
        self.assertEqual(snapshot(self.distribution), before_source)
        self.assertEqual(snapshot(worktree), before_worktree)

    def test_uninstall_from_linked_worktree_keeps_source(self) -> None:
        self.prepare_source_clone()
        original = self.distribution
        worktree = self.root / 'linked-worktree'
        self.source_git('worktree', 'add', '--quiet', '--detach', str(worktree), 'HEAD')
        self.distribution = worktree
        self.run_installer('--codex-dir', str(self.other))
        before_source = snapshot(original)
        before_worktree = snapshot(worktree)
        self.run_installer('--uninstall', '--codex-dir', str(self.other))
        self.assertEqual(snapshot(original), before_source)
        self.assertEqual(snapshot(worktree), before_worktree)

    def test_blocked_uninstall_never_removes_source_clone(self) -> None:
        self.prepare_source_clone()
        self.run_installer('--codex-dir', str(self.other))
        lock = self.state / 'lock'
        if POWERSHELL:
            lock.write_text('active')
        else:
            lock.mkdir()
        before = snapshot(self.root)
        self.run_installer('--uninstall', '--codex-dir', str(self.other), success=False)
        self.assertEqual(snapshot(self.root), before)

    @unittest.skipIf(POWERSHELL, 'POSIX rm injection')
    def test_source_changed_during_uninstall_is_retained(self) -> None:
        self.prepare_source_clone()
        self.run_installer('--codex-dir', str(self.other))
        bin_dir = self.root / 'fake-bin'
        bin_dir.mkdir()
        wrapper = bin_dir / 'rm'
        wrapper.write_text('''#!/bin/bash
case "${@: -1}" in */skills/ndd-setup) printf 'concurrent work' > "$NDD_TEST_SOURCE/concurrent.txt";; esac
exec /bin/rm "$@"
''')
        wrapper.chmod(0o755)
        environment = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ['PATH'],
                           NDD_TEST_SOURCE=str(self.distribution))
        result = self.run_installer('--uninstall', '--codex-dir', str(self.other), environment=environment)
        self.assertIn('Source retained:', result.stdout)
        self.assertEqual((self.distribution / 'concurrent.txt').read_text(), 'concurrent work')
        self.assertFalse(self.state.exists())

    @unittest.skipIf(POWERSHELL, 'POSIX source deletion failure injection')
    def test_source_removal_failure_is_reported_and_can_be_retried(self) -> None:
        self.prepare_source_clone()
        self.run_installer('--codex-dir', str(self.other))
        bin_dir = self.root / 'fake-bin'
        bin_dir.mkdir()
        wrapper = bin_dir / 'rm'
        wrapper.write_text('''#!/bin/bash
if [[ "${@: -1}" == "$NDD_TEST_SOURCE" ]]; then echo 'injected source deletion failure' >&2; exit 9; fi
exec /bin/rm "$@"
''')
        wrapper.chmod(0o755)
        environment = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ['PATH'],
                           NDD_TEST_SOURCE=str(self.distribution))
        result = self.run_installer('--uninstall', '--codex-dir', str(self.other), success=False,
                                    environment=environment)
        self.assertIn('Uninstall incomplete', result.stdout)
        self.assertIn('injected source deletion failure', result.stdout)
        self.assertTrue(self.distribution.is_dir())
        self.assertFalse(self.state.exists())
        self.run_installer('--uninstall', '--codex-dir', str(self.other))
        self.assertFalse(self.distribution.exists())

    @unittest.skipUnless(POWERSHELL, 'PowerShell source deletion failure injection')
    def test_powershell_source_removal_failure_is_reported_and_retried(self) -> None:
        self.prepare_source_clone()
        self.run_installer('--codex-dir', str(self.other))
        driver = self.root / 'fail-source-delete.ps1'
        driver.write_text('''param([string]$Installer, [string]$Target, [string]$Other)
function Remove-Item {
    param([string]$LiteralPath, [switch]$Force, [switch]$Recurse)
    if ($LiteralPath -like '*kit space*') { throw 'injected source deletion failure' }
    Microsoft.PowerShell.Management\\Remove-Item @PSBoundParameters
}
& $Installer -ClaudeDir $Target -CodexDir $Other -Uninstall
''')
        result = subprocess.run([os.environ.get('NDD_TEST_POWERSHELL', 'powershell'),
                                 '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(driver),
                                 '-Installer', str(self.distribution / 'install.ps1'),
                                 '-Target', str(self.target), '-Other', str(self.other)],
                                capture_output=True, text=True, errors='replace', timeout=60,
                                env=child_environment(os.environ.get('NDD_TEST_POWERSHELL', 'powershell')))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Uninstall incomplete', result.stdout)
        self.assertIn('injected source deletion failure', result.stderr)
        self.assertTrue(self.distribution.is_dir())
        self.assertFalse(self.state.exists())
        self.run_installer('--uninstall', '--codex-dir', str(self.other))
        self.assertFalse(self.distribution.exists())

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

    def test_upgrade_four_skill_030_installation(self) -> None:
        # Reproduce the previous four-skill layout using the unchanged receipt
        # protocol. No network/history dependency and no hand-forged receipts.
        originals = {name: (self.distribution / name).read_bytes()
                     for name in ('install.sh', 'install.ps1', 'skills/ndd-setup/VERSION')}
        for name in ('install.sh', 'install.ps1'):
            path = self.distribution / name
            content = originals[name].replace(b' ndd-help ndd-review)', b')')
            content = content.replace(b", 'ndd-help', 'ndd-review')", b")")
            path.write_bytes(content)
        (self.distribution / 'skills/ndd-setup/VERSION').write_text('0.3.0\n')
        self.run_installer('--codex-dir', str(self.other))
        for target in (self.target, self.other):
            self.assertEqual({p.name for p in target.iterdir()}, set(NAMES[:4]))
            state = Path(str(target) + '.ndd-kit')
            self.assertEqual({p.stem for p in state.glob('*.receipt')}, set(NAMES[:4]))
        for name, content in originals.items():
            (self.distribution / name).write_bytes(content)
        self.run_installer('--codex-dir', str(self.other))
        self.run_installer('--codex-dir', str(self.other))
        for target in (self.target, self.other):
            for name in NAMES:
                self.assertEqual(snapshot(target / name), snapshot(self.distribution / 'skills' / name))
                self.assertTrue((Path(str(target) + '.ndd-kit') / f'{name}.receipt').is_file())
        other_before = snapshot(self.other)
        self.run_installer('--uninstall', '--keep-source')
        self.assertEqual(snapshot(self.other), other_before)
        self.assertEqual(list(self.target.iterdir()), [])
        self.run_installer('--uninstall', '--codex-dir', str(self.other), '--keep-source')
        self.assertEqual(list(self.other.iterdir()), [])

    def test_new_skill_conflicts_and_resources_fail_before_writes(self) -> None:
        for name in ('ndd-help', 'ndd-review'):
            with self.subTest(conflict=name):
                foreign = self.other / name
                foreign.mkdir(parents=True)
                (foreign / 'user.txt').write_text('keep me')
                before = snapshot(self.root)
                self.run_installer('--codex-dir', str(self.other), success=False)
                self.assertEqual(snapshot(self.root), before)
                shutil.rmtree(foreign)
        for resource in ('ndd-help/SKILL.md', 'ndd-review/agents/openai.yaml',
                         'ndd-review/assets/review.md', 'ndd-review/references/report-updates.md'):
            with self.subTest(missing=resource):
                path = self.distribution / 'skills' / resource
                original = path.read_bytes()
                path.unlink()
                before = snapshot(self.root)
                self.run_installer('--codex-dir', str(self.other), success=False)
                self.assertEqual(snapshot(self.root), before)
                path.write_bytes(original)

    def test_both_targets(self) -> None:
        self.run_installer('--codex-dir', str(self.other))
        self.assertEqual(snapshot(self.target), snapshot(self.other))

    def test_dry_run_has_no_writes(self) -> None:
        before = snapshot(self.root)
        result = self.run_installer('--dry-run')
        for name in ('ndd-help', 'ndd-review'):
            self.assertIn(name, result.stdout)
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
                                capture_output=True, text=True, errors='replace', timeout=60,
                                env=child_environment(os.environ.get('NDD_TEST_POWERSHELL', 'powershell')))
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
        expected = {name: (self.distribution / 'skills/ndd-setup/assets' / name).read_bytes()
                    for name in ('spec.md', 'plan.md')}
        self.run_installer()
        shutil.rmtree(self.distribution / 'skills')
        project = self.root / 'work-project'
        project.mkdir()
        (project / 'AGENTS.md').write_text('existing team rules')
        before = snapshot(project)
        for skill, template in (('ndd-spec', 'spec.md'), ('ndd-plan', 'plan.md')):
            asset = self.target / skill / '../ndd-setup/assets' / template
            self.assertTrue(asset.is_file())
            self.assertEqual(asset.read_bytes(), expected[template])
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
                                capture_output=True, text=True, errors='replace', timeout=60,
                                env=child_environment(os.environ.get('NDD_TEST_POWERSHELL', 'powershell')))
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
