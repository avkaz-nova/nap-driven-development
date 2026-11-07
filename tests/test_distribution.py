"""Check distribution contents, reproducibility and example plan/spec consistency."""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import re
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MODULE_SPEC = importlib.util.spec_from_file_location('build_distribution', ROOT / 'scripts/build_distribution.py')
assert MODULE_SPEC and MODULE_SPEC.loader
BUILDER = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(BUILDER)


class DistributionTests(unittest.TestCase):
    def test_help_command_table_matches_available_skills(self) -> None:
        skill_names = {path.parent.name for path in (ROOT / 'skills').glob('*/SKILL.md')}
        self.assertTrue(skill_names, 'No skills found to compare with help')
        help_text = (ROOT / 'skills/ndd-help/assets/help.md').read_text(encoding='utf-8')
        # Require a command-table row with both agent examples and a description;
        # mentioning a command elsewhere in the help is not enough.
        rows = re.findall(
            r'^\| *`\$([a-z0-9-]+)(?: [^`]*)?` *\| *`/([a-z0-9-]+)(?: [^`]*)?` *\| *\S[^\n]*\| *$',
            help_text, re.MULTILINE,
        )
        for column, agent in enumerate(('Codex', 'Claude Code')):
            with self.subTest(agent=agent):
                self.assertCountEqual(
                    [row[column] for row in rows], skill_names,
                    f'{agent} help must list every current skill exactly once, with no obsolete commands',
                )
        for codex, claude in rows:
            self.assertEqual(codex, claude, 'Both examples in a help row must describe the same skill')

    def test_distribution_reproducibility_and_contents(self) -> None:
        with tempfile.TemporaryDirectory(prefix='ndd-distribution-') as directory:
            output = Path(directory)
            archive = BUILDER.build_distribution(output)
            self.assertEqual(archive.name, 'ndd-kit.zip')
            original = archive.read_bytes()
            BUILDER.build_distribution(output)
            self.assertEqual(original, archive.read_bytes())
            self.assertTrue((output / f'{archive.name}.sha256').read_text().startswith(hashlib.sha256(original).hexdigest()))
            with zipfile.ZipFile(archive) as bundle:
                prefix = archive.stem + '/'
                self.assertIn(prefix + 'install.sh', bundle.namelist())
                self.assertIn(prefix + 'install.ps1', bundle.namelist())
                self.assertIn(prefix + 'skills/ndd-plan/scripts/spec-digest.ps1', bundle.namelist())
                for name in ('spec.md', 'plan.md'):
                    self.assertIn(prefix + 'skills/ndd-setup/assets/' + name, bundle.namelist())
                self.assertIn(prefix + 'skills/ndd-setup/references/diagrams.md', bundle.namelist())
                for name in ('SKILL.md', 'agents/openai.yaml', 'assets/help.md'):
                    self.assertIn(prefix + 'skills/ndd-help/' + name, bundle.namelist())
                for name in ('SKILL.md', 'agents/openai.yaml', 'assets/review.md',
                             'references/report-updates.md'):
                    self.assertIn(prefix + 'skills/ndd-review/' + name, bundle.namelist())
                for name in ('SKILL.md', 'agents/openai.yaml'):
                    self.assertIn(prefix + 'skills/ndd-init/' + name, bundle.namelist())
                self.assertIn(prefix + 'skills/ndd-setup/references/project-context.md', bundle.namelist())
                self.assertIn(prefix + 'docs/init.md', bundle.namelist())
                self.assertNotIn(prefix + 'skills/ndd-setup/VERSION', bundle.namelist())
                self.assertNotIn(prefix + 'CHANGELOG.md', bundle.namelist())
                banner = 'docs/assets/nap-driven-development.png'
                self.assertEqual(bundle.read(prefix + banner), (ROOT / banner).read_bytes())
                self.assertFalse(any('/.git/' in p or '__pycache__' in p or '/dist/' in p for p in bundle.namelist()))
                self.assertTrue(bundle.getinfo(prefix + 'install.sh').external_attr >> 16 & 0o100)
                self.assertFalse(any(p.startswith(prefix + 'skills/ndd-help/scripts/')
                                     for p in bundle.namelist()))

    def test_distribution_normalizes_text_and_preserves_other_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix='ndd-distribution-') as directory:
            root = Path(directory) / 'source'
            root.mkdir()
            for name in BUILDER.FILES:
                (root / name).write_bytes(b'')
            for name in BUILDER.DIRECTORIES:
                (root / name).mkdir()
            text_files = ('README.md', 'LICENSE', '.gitattributes', 'install.sh',
                          'install.ps1', 'scripts/example.py', 'scripts/example.ps1', 'docs/example.txt',
                          'skills/example.yaml', 'skills/example.yml')
            for name in text_files:
                (root / name).write_bytes(b'first\r\nsecond\r\n')
            binary = b'\x00\xff\r\n\x89PNG\r\n\x1a\n'
            for name in ('docs/image.png', 'docs/unknown.asset'):
                (root / name).write_bytes(binary)

            archive = BUILDER.build_distribution(Path(directory) / 'output', root=root)
            with zipfile.ZipFile(archive) as bundle:
                prefix = archive.stem + '/'
                for name in text_files:
                    self.assertEqual(bundle.read(prefix + name), b'first\nsecond\n', name)
                for name in ('docs/image.png', 'docs/unknown.asset'):
                    self.assertEqual(bundle.read(prefix + name), binary, name)

    def test_example_plans_match_spec_bodies(self) -> None:
        for folder in (ROOT / 'examples').iterdir():
            spec = (folder / 'spec.md').read_text(encoding='utf-8')
            body = spec.split('---\n', 2)[2].rstrip('\n') + '\n'
            expected = hashlib.sha256(body.encode('utf-8')).hexdigest()
            plan = (folder / 'plan.md').read_text(encoding='utf-8')
            self.assertIn(f'spec_digest: {expected}', plan, folder.name)
            acs = set(re.findall(r'^- (AC\d+)(?=[: ])', spec, re.MULTILINE))
            tasks = re.findall(r'^- \[[ x]\] T\d+ \(([^)]+)\):.*$', plan, re.MULTILINE)
            task_coverage = set(re.findall(r'\bAC\d+\b', ' '.join(tasks)))
            self.assertEqual(acs, task_coverage, folder.name)
            # Legacy plans may also have a table; compact plans need only tasks.
            coverage = set(re.findall(r'^\| (AC\d+) \|', plan, re.MULTILINE))
            if coverage:
                self.assertEqual(acs, coverage, folder.name)

    def test_skill_metadata_and_bundled_resources(self) -> None:
        names = ('ndd-setup', 'ndd-spec', 'ndd-plan', 'ndd-do', 'ndd-help', 'ndd-review', 'ndd-init')
        for name in names:
            folder = ROOT / 'skills' / name
            text = (folder / 'SKILL.md').read_text(encoding='utf-8')
            self.assertTrue(text.startswith('---\n'))
            frontmatter = text.split('---\n', 2)[1]
            fields = dict(line.split(': ', 1) for line in frontmatter.splitlines() if ': ' in line)
            self.assertEqual(fields['name'], name)
            self.assertTrue(0 < len(fields['description']) <= 1024)
            self.assertEqual(fields['disable-model-invocation'], 'true')
            policy = (folder / 'agents/openai.yaml').read_text()
            self.assertIn('allow_implicit_invocation: false', policy)
            for reference in re.findall(r'\]\(([^)]+)\)', text):
                self.assertTrue((folder / reference).is_file(), reference)
        for name in ('spec.md', 'plan.md'):
            self.assertTrue((ROOT / 'skills/ndd-setup/assets' / name).is_file())


if __name__ == '__main__':
    unittest.main()
