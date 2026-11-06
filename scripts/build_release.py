#!/usr/bin/env python3
"""Build a deterministic local release ZIP. Never publishes or invokes Git."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = ('README.md', 'LICENSE', 'CHANGELOG.md', 'install.sh', 'install.ps1', '.gitattributes')
DIRECTORIES = ('skills', 'docs', 'examples', 'tests', 'scripts')
TEXT_SUFFIXES = {'.md', '.sh', '.ps1', '.py', '.yaml', '.yml', '.txt'}
TEXT_NAMES = {'LICENSE', 'VERSION', '.gitattributes'}


def build_release(output: Path, *, root: Path = ROOT) -> Path:
    version = (root / 'skills/ndd-setup/VERSION').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('VERSION must contain a numeric major.minor.patch version')
    paths = [root / name for name in FILES]
    for directory in DIRECTORIES:
        for path in (root / directory).rglob('*'):
            if '__pycache__' in path.parts or path.suffix == '.pyc':
                continue
            if path.is_symlink():
                raise ValueError(f'Release sources may not contain symlinks: {path}')
            if path.is_file():
                paths.append(path)
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f'ndd-kit-{version}.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(paths):
            if path.is_symlink() or not path.is_file():
                raise ValueError(f'Expected a regular release file: {path}')
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f'ndd-kit-{version}/{relative}', date_time=(2020, 1, 1, 0, 0, 0))
            info.create_system = 3
            mode = 0o755 if path.suffix == '.sh' else 0o644
            info.external_attr = (0o100000 | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            content = path.read_bytes()
            # Normalize known text assets; preserve binary and unknown formats exactly.
            if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES:
                content = content.replace(b'\r\n', b'\n')
            bundle.writestr(info, content)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / f'{archive.name}.sha256').write_text(f'{digest}  {archive.name}\n', encoding='utf-8')
    return archive


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    print(build_release(args.output))


if __name__ == '__main__':
    main()
