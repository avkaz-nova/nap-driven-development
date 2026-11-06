"""Check release contents, reproducibility and example plan/spec consistency."""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import re
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MODULE_SPEC = importlib.util.spec_from_file_location('build_release', ROOT / 'scripts/build_release.py')
assert MODULE_SPEC and MODULE_SPEC.loader
BUILDER = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(BUILDER)


class DistributionTests(unittest.TestCase):
    def test_release_reproducibility_and_contents(self) -> None:
        with tempfile.TemporaryDirectory(prefix='ndd-release-') as directory:
            output = Path(directory)
            archive = BUILDER.build_release(output)
            original = archive.read_bytes()
            BUILDER.build_release(output)
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
                self.assertFalse(any('/.git/' in p or '__pycache__' in p or '/dist/' in p for p in bundle.namelist()))
                self.assertTrue(bundle.getinfo(prefix + 'install.sh').external_attr >> 16 & 0o100)

    def test_example_plans_match_spec_bodies(self) -> None:
        for folder in (ROOT / 'examples').iterdir():
            spec = (folder / 'spec.md').read_text(encoding='utf-8')
            body = spec.split('---\n', 2)[2].rstrip('\n') + '\n'
            expected = hashlib.sha256(body.encode('utf-8')).hexdigest()
            plan = (folder / 'plan.md').read_text(encoding='utf-8')
            self.assertIn(f'spec_digest: {expected}', plan, folder.name)
            acs = set(re.findall(r'^- (AC\d+) ', spec, re.MULTILINE))
            coverage = set(re.findall(r'^\| (AC\d+) \|', plan, re.MULTILINE))
            self.assertEqual(acs, coverage, folder.name)

    def test_skill_metadata_and_bundled_resources(self) -> None:
        names = ('ndd-setup', 'ndd-spec', 'ndd-plan', 'ndd-do')
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
