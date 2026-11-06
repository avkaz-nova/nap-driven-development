# NDD — Nap-Driven Development

A small spec-driven workflow for **Claude Code and Codex**, on **macOS and Windows**.
Describe the behaviour, approve a plan, and let the agent implement a verifiable task.

NDD is four Agent Skills and two templates. It needs no Python, Node.js, package
manager or background service to use. Installation uses Bash or PowerShell.
Use it for features that need shared context or several sessions; small fixes can
use your usual workflow.

```text
╭────────────╮     ╭─────────────╮     ╭────────────╮
│ ndd-spec   │ ──→ │ Review spec │ ──→ │ ndd-plan   │
╰────────────╯     ╰─────────────╯     ╰──────┬─────╯
                                           ▼
╭────────────╮     ╭─────────────╮     ╭────────────╮
│ Acceptance │ ◀── │ ndd-do      │ ◀── │ Review plan│
╰──────┬─────╯     ╰──────┬──────╯     ╰────────────╯
       │                  │   ▲
       ▼                  ╰───╯ next task
╭────────────╮
│ Done       │
╰────────────╯
```

## Install once per computer

Download a versioned ZIP from [GitHub Releases](https://github.com/avkaz/nap-driven-development/releases)
and extract it. Before the first release, use **Code → Download ZIP** on the
[repository](https://github.com/avkaz/nap-driven-development); that downloads the current branch,
so use the same archive on both computers. Open a terminal in the extracted folder.

**macOS** (uses the built-in Bash):

```bash
bash ./install.sh --all
```

**Windows** (Windows PowerShell 5.1 or PowerShell 7):

```powershell
powershell -NoProfile -File .\install.ps1 -All
```

With PowerShell 7 use `pwsh` instead of `powershell`. If your own machine blocks
this unsigned script, inspect it first and use a process-only execution-policy
option as described in [installation and recovery](docs/installation.md).
Managed work-computer policies may require your administrator's supported process.

The installer prints its destinations: Claude skills normally go to
`~/.claude/skills`, Codex skills to `~/.agents/skills`. Use `--claude` / `-Claude`
or `--codex` / `-Codex` for only one agent. Without flags, existing agent
configuration directories are used as a detection hint. No detection means an
explicit target is required. The agents themselves must already be available to use NDD.

For a Git checkout instead of a ZIP:

```bash
git clone https://github.com/avkaz/nap-driven-development.git
cd nap-driven-development
```

Choose a published release tag before installing when you need repeatable versions.
The normal copy installation is independent of the downloaded folder afterwards.
Restart the agent if the skills don't appear.

## Connect each project

Open your project in an agent and invoke:

| Action | Claude Code | Codex CLI/IDE |
|---|---|---|
| Setup or update | `/ndd-setup` | `$ndd-setup` |
| Preview only | `/ndd-setup --dry-run` | `$ndd-setup --dry-run` |

These are agent skills entered in chat, not terminal commands. In a graphical
client, use its skill selector if it doesn't expose the same typed syntax.

Setup inventories existing instructions, relevant settings, skills and templates.
It shows concrete changes before asking for approval. It preserves existing
project rules and file layout, and never edits global settings or agent permissions.
It does not automatically migrate instructions or remove another workflow.

A typical preview looks like this; the real preview also includes the exact diff:

| Found | Proposed action |
|---|---|
| Existing `AGENTS.md` | Append a short marked NDD block; preserve current rules |
| Existing `CLAUDE.md` | Preserve it; reuse an import or propose a short NDD block |
| Another spec workflow | Report overlap; leave it installed |
| No NDD templates | Create `specs/_templates/spec.md` and `plan.md` |

Approve the displayed changes or request adjustments. A repeat setup with
unchanged inputs should leave no diff. See [setup and update contract](docs/setup.md).

A typical project gains `.ndd-kit.json`, two templates under `specs/_templates`,
and a small block in its instruction files. A new project can share `AGENTS.md`
through a `CLAUDE.md` import. Existing instruction layouts are preserved.

## Use the workflow

| Step | Claude Code | Codex CLI/IDE | Result |
|---|---|---|---|
| Describe | `/ndd-spec <idea>` | `$ndd-spec <idea>` | Questions, then `spec.md`; no implementation |
| Review spec | Say “I approve this spec” | Same | Agent records approval |
| Plan | `/ndd-plan 001` | `$ndd-plan 001` | Approach, tasks, AC coverage and checks |
| Review plan | Say “I approve this plan” | Same | Agent records approval |
| Implement | `/ndd-do 001` | `$ndd-do 001` | Next task, verification and progress |
| Continue | Invoke again | Invoke again | Final acceptance before `done` |

You can specify a task, e.g. `ndd-do 001 T2`, if its prerequisites are complete.
One task per invocation is the default; explicitly request several to continue
through them. New sessions are optional. No commits, pushes or deployments are
implied by an NDD command.

The spec describes agreed behaviour; the plan describes implementation and
records evidence. Every acceptance criterion maps to tasks and a final check.
Testing fits the work: regression tests for bugs, suitable checks for docs/config,
and the project's required checks before completion.

Plans store a SHA-256 digest of the spec body. Changing requirements invalidates
the plan; return to spec approval and plan review. Metadata-only status changes
and Windows/macOS line endings don't invalidate it. A direct `ndd-do` call cannot
approve an old or draft plan. See the [workflow contract](docs/workflow.md).

Start with the [CSV export example](examples/002-csv-export/spec.md) and its
[plan](examples/002-csv-export/plan.md). The [recommendations example](examples/001-cold-start-fallback/spec.md)
shows a larger data feature. Examples are illustrative approved documents, not
claims of implemented code or passing tests.

## Update and uninstall

Download the desired release and rerun its installer, then run `ndd-setup` in each
project to review template/instruction updates. Updating machine skills never
rewrites projects automatically. Keep the same release on both computers.

```bash
bash ./install.sh --all --dry-run
bash ./install.sh --all --uninstall
```

```powershell
powershell -NoProfile -File .\install.ps1 -All -DryRun
powershell -NoProfile -File .\install.ps1 -All -Uninstall
```

Local changes and unowned same-name skills block replacement/removal. The explicit
`--replace` / `-Replace` install option backs them up before replacing them;
preview that decision first. Uninstall never removes arbitrary `ndd-*` skills.
Receipts/backups live beside the skills folder in `skills.ndd-kit`, outside skill
discovery. Project specs, plans and instructions remain after uninstall.

NDD 0.1 installations have no ownership receipts. Treat them as unverified:
review a replacement preview or move those four directories aside manually.
Old plans need review before adding approval/digest metadata. No progress is
silently discarded. [Recovery and all installer options](docs/installation.md).

## Compatibility and verification

Targets: macOS with Bash 3.2+, Windows with PowerShell 5.1/7, Claude Code and Codex
with Agent Skills support. Linux is also covered by the CI matrix; WSL/Git Bash
are not separate verified targets. Symlinks/junctions are an optional development
installation, not required for normal use.

The automated suite checks filesystem behaviour and spec fingerprints. Agent
behaviour requires separate scenario testing: these are instructions, not a
sandbox or a guaranteed enforcement engine. See [verification status and release
gates](docs/testing.md) before treating a new release as validated on every platform.

## Development

Python 3.10+ is needed only for maintainers' tests and release packaging:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py
```

On Windows use `python`. No third-party test dependencies are required.
Release packaging creates a reproducible ZIP and checksum locally; it does not
publish, commit or push. See [release procedure](docs/releasing.md).

Inspired by [GitHub Spec Kit](https://github.com/github/spec-kit) and the
[Agent Skills standard](https://agentskills.io). MIT licensed.
