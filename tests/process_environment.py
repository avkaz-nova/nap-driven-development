"""Keep Windows PowerShell from inheriting incompatible PowerShell 7 modules."""
from __future__ import annotations

import ntpath
import os


def child_environment(executable: str, environment: dict[str, str] | None = None) -> dict[str, str]:
    result = dict(os.environ if environment is None else environment)
    if ntpath.basename(executable).lower() in ('powershell', 'powershell.exe'):
        # Python bypasses pwsh's direct-child PSModulePath compatibility handling.
        result = {key: value for key, value in result.items() if key.upper() != 'PSMODULEPATH'}
    return result
