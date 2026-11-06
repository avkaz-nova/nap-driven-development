# Testing NDD

## Automated checks

From the repository root, use Python 3.13 (the version configured in CI):

```bash
python3 -m unittest discover -s tests -v
```

On Windows:

```powershell
python -m unittest discover -s tests -v
```

Python is needed for development checks, not for using the installed skills.
Tests use temporary projects and installation paths. They cover installation,
updates, rollback, removal, project registration, spec checksums and ZIP contents.
They do not install into your real agent folders or clean your real project registry.

The CI workflow (`.github/workflows/ci.yml`) configures macOS, Ubuntu and
Windows runs, including Windows PowerShell and PowerShell 7. Some checks are
platform-specific and may be skipped. To select another PowerShell executable:

```bash
NDD_TEST_POWERSHELL=/absolute/path/to/pwsh python3 -m unittest discover -s tests -v
```

Check the actual test output and CI run for results; this page does not maintain
a separate count of passing tests or claim end-to-end agent compatibility.

## Checking the agent workflow

Unit tests cannot verify how an agent follows skill instructions. For a manual
check, use a disposable project and record the agent version, OS and actual result:

1. Run setup, confirm a prefix, then repeat setup. Check that it preserves project
   instructions and reuses the saved value without rewriting it. Outside Git,
   check that the prefix remains session-only.
2. Create a small spec, approve it, create a plan and approve it. Confirm that an
   unapproved draft does not allow implementation.
3. Implement a task. Change the spec body and confirm that the stale plan stops
   implementation until reviewed. Check that a failed verification leaves work incomplete.
4. Resume in a new session or the other agent. Confirm that progress is preserved
   and completion requires the final acceptance checks.

Use disposable installation paths for manual uninstall checks too. Preview first;
verify that single-agent removal keeps shared settings and full removal cleans
registered prefixes while skipping failed entries. Check source-clone removal
on the target OS, including open-file failures on Windows.
