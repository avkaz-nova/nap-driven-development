# NDD — Nap-Driven Development

![Nap-Driven Development — a developer and cat nap while two robot assistants plan and code](docs/assets/nap-driven-development.png)

[![CI](https://github.com/avkaz/nap-driven-development/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/avkaz/nap-driven-development/actions/workflows/ci.yml)

NDD is a lightweight spec-driven workflow for **Claude Code and Codex**, on **Mac
and Windows**. Describe a change, approve a spec and plan, then let the agent
implement and verify it. Specs, tasks and results stay in your project, so you can
resume in another session or switch agents.

```text
╭──────────╮   ╭──────────────╮   ╭──────────────╮   ╭───────────╮   ╭────────╮
│ Describe │ → │ Approve spec │ → │ Approve plan │ → │ Implement │ → │ Verify │
╰──────────╯   ╰──────────────╯   ╰──────────────╯   ╰───────────╯   ╰────────╯
```

[Example spec](examples/002-csv-export/spec.md) ·
[Example plan](examples/002-csv-export/plan.md) ·
[Download v0.5.0 (public preview)](https://github.com/avkaz/nap-driven-development/releases/tag/v0.5.0)

## Install

Requires **Git** and **Claude Code or Codex**.

<details>
<summary><strong>Mac</strong></summary>

```bash
git clone https://github.com/avkaz/nap-driven-development.git
cd nap-driven-development
bash ./install.sh --all
```

Use `--codex` or `--claude` instead of `--all` to install for one agent.
Add `--dry-run` to preview.

</details>

<details>
<summary><strong>Windows</strong></summary>

```powershell
git clone https://github.com/avkaz/nap-driven-development.git
cd nap-driven-development
powershell -NoProfile -File .\install.ps1 -All
```

Use `-Codex` or `-Claude` instead of `-All` to install for one agent.
Add `-DryRun` to preview.

</details>

Restart your agent after installation. Alternatively, extract the
[release ZIP](https://github.com/avkaz/nap-driven-development/releases/tag/v0.5.0)
and run the installer from that folder.
[Custom paths and troubleshooting →](docs/installation.md)

## Use

Run these commands in your agent's chat. Codex uses `$`; Claude Code uses `/`.

| Action | Codex | Claude Code |
|---|---|---|
| Check project and choose prefix | `$ndd-setup` | `/ndd-setup` |
| Describe a change | `$ndd-spec Fix CSV export` | `/ndd-spec Fix CSV export` |
| Plan an approved spec | `$ndd-plan 001` | `/ndd-plan 001` |
| Complete an approved plan | `$ndd-do 001` | `/ndd-do 001` |
| Execute only task T2 | `$ndd-do 001 T2` | `/ndd-do 001 T2` |
| Review the latest stage | `$ndd-review 001` | `/ndd-review 001` |
| Review a specific stage | `$ndd-review 001 plan` | `/ndd-review 001 plan` |
| Show command reference | `$ndd-help` | `/ndd-help` |

Approve the spec and plan in chat before proceeding. After showing a spec, the
agent offers **Approve spec and continue with Plan** for that feature. Selecting
it approves the spec and starts planning; the plan still needs its own approval.
Interactive choices depend on the host; a short chat reply also works.

`ndd-do 001` completes all remaining tasks and final verification.
`ndd-do 001 T2` runs only T2 and its checks, then stops. Unfinished prerequisites
are reported; a later `ndd-do 001` resumes the remaining work.

Review is optional. Use `spec`, `plan` or `code` to select a stage, for example
`ndd-review 001 spec` or `ndd-review 001 code`. Findings appear in chat, with an
option to save `review.md`. Review does not run tests or replace approval and
verification. `ndd-help` includes more examples and works before setup.

## Feature IDs and files

Setup confirms a personal prefix such as `ak` and saves it as local Git config
`ndd.prefix`. Then `001` means `ak-001`; use `iv-001` to select another prefix.
Numbers advance separately per prefix. Each clone needs its own setup.

```text
specs/
└── ak-001-fix-csv-export/
    ├── spec.md
    ├── plan.md
    └── review.md  (optional)
```

Specs contain a goal and acceptance criteria; plans contain tasks and checks.
Create them only for changes you choose. These are ordinary files you can commit
with your code. NDD preserves existing `AGENTS.md` / `CLAUDE.md` instructions and
does not commit, push or deploy automatically.

## Update

Run `git pull --ff-only` in the NDD checkout, then repeat your installation
command and restart the agent. For ZIP installations, use a fresh release ZIP.
Use the same custom destination options if applicable.

Updates replace installed NDD skills, including local edits, and remove old
installation backups. Project files and unrelated skills are preserved.

## Uninstall

Run from the NDD folder:

```bash
bash ./install.sh --all --uninstall
```

```powershell
powershell -NoProfile -File .\install.ps1 -All -Uninstall
```

Use `--codex` / `--claude` or `-Codex` / `-Claude` for one agent; add
`--dry-run` / `-DryRun` to preview. Use the original custom destinations and
`NDD_STATE_DIR` if configured.

Removal deletes NDD skills, local skill edits and installation metadata/backups.
Full removal also clears registered, unchanged project prefixes and can delete
the clean official source clone running the installer. Add `--keep-source` /
`-KeepSource` to retain it. Single-agent removal keeps project prefixes and the
source clone. Project code, specs, plans and unrelated skills are preserved.
[Removal details and recovery →](docs/installation.md#uninstall)

## Learn more

- [Project setup](docs/setup.md)
- [Workflow and approvals](docs/workflow.md)
- [Installation options and troubleshooting](docs/installation.md)
- [Development checks](docs/testing.md)

Inspired by [GitHub Spec Kit](https://github.com/github/spec-kit). [MIT license](LICENSE).
