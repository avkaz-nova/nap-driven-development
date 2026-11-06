# Help and review acceptance scenarios

These are manual acceptance checks, not claims of completed verification. Run
in a disposable project with a disposable NDD installation. Never point cleanup
at personal agent folders. Test all four combinations: macOS/Codex,
macOS/Claude Code, Windows/Codex and Windows/Claude Code. Use `$` in Codex and `/`
in Claude Code. Record kit version, agent version, OS, input, actual response,
files read/commands run, before/after file contents and pass/fail/blocked per case.
Git diff alone misses newly created reports; compare all files including untracked
ones and local Git configuration. Do not execute the sample code during review.

## Fixture

Prepare these files yourself in an isolated project. Setup can confirm `ak` for
this project. Make separate copies for destructive/error scenarios.

- `specs/ak-009-old/spec.md`, `specs/ak-010-csv/spec.md`,
  `specs/iv-100-other/spec.md`: use the installed spec template with matching IDs.
- In ak-010 use: R1 exports every row as CSV; R2 doubles embedded quotes and quotes
  fields containing commas or quotes; R3 empty input produces `name,note` header.
  AC1 checks `Ada / plain`; AC2 checks `Ada / hello, "world"`; AC3 checks no rows.
- Add a deliberate contradiction for spec review: R4 says empty input returns an
  empty string. Also add an untestable AC4: "Export feels fast and friendly."
  Expected findings are R3 vs R4 and missing measurable AC4 conditions. Remove
  AC4 before the plan/code cases.
- For plan review remove R4, explicitly approve the spec, create a plan via
  `ndd-plan`, then in the disposable fixture omit AC2 coverage and make T1 depend
  on T2 while T2 depends on T1. Record these deliberate edits as test inputs.
- For code review use a plan covering all three ACs with a current helper-computed
  digest. Select the following implementation and test explicitly:

```python
# export.py — deliberately faulty fixture

def export_csv(rows):
    return "name,note\n" + "\n".join(
        ",".join((row["name"], row["note"])) for row in rows
    )

# test_export.py — insufficient fixture coverage
from export import export_csv

def test_creates_file(tmp_path):
    output = tmp_path / "export.csv"
    output.write_text(export_csv([{"name": "Ada", "note": "plain"}]))
    assert output.is_file()
```

Expected code finding: comma/quote input does not satisfy R2/AC2; file-existence-only test
coverage misses it. Finding must include the trigger, consequence and location.
The agent must not run the test, fix code or change completion/approval markers.
For a no-defect case explicitly select a tiny spec whose requirements and ACs are
consistent; expect a scoped conclusion, not a correctness guarantee.

## Cases and expected observations

| Case / AC | Inputs | Expected observation |
|---|---|---|
| H1 / AC1–AC3 | In empty non-Git folder, call help; repeat after setup in project; call help with `code 001` extra text; ask in Russian and English | Verbatim English `assets/help.md` with only `{{VERSION}}` substituted: six commands, installed version, workflow/approvals, optional review, illustrative IDs and specs location; no translation or added commentary. No project scan, menu, command execution or writes. |
| H2 / AC3 | Hide VERSION in the disposable loaded installation; keep another version in a source clone | Incomplete-installation/version-unavailable notice; no invented version or fallback to clone/other installation/network. Restore fixture afterward. |
| H3 | Remove `assets/help.md` in the disposable installation | Report the missing resource; do not reconstruct help or search another installation. |
| S1 / AC4 | Explicit `010`, `ak-010`, full folder name and path to its spec; then missing ID, path outside project and link escaping project | Same feature for valid inputs; report missing/unsafe selections without creating anything or selecting a replacement. |
| S2 / AC4 | Create duplicate `ak-010-duplicate`; try qualified and short ID | Ask for full name/path, no arbitrary match. Remove duplicate for later cases. |
| S3 / AC13 | With ak prefix, review without arguments; answer no, then retry and give no answer, then confirm | Propose ak-010 with title/path, ignoring iv-100 and timestamps; analyze only after confirmation. |
| S4 / AC13 | No prefix, prefix with no tasks, duplicate maximum number; review with mode only; explicit ak-009 | Ask for qualified ID/setup, report no candidates, or list duplicates respectively. Mode-only retains confirmation; explicit ID avoids the extra confirmation. |
| M1 / AC5, AC7 | Spec only; then add plan; then related partial code; try `010 spec` and `spec 010` | Automatic spec/plan/code selection follows actual artifacts; explicit spec wins in both orders. Plan review finds missing AC2 and cyclic dependencies. |
| M2 / AC7–AC8 | Existing unrelated code plus checked tasks or done status; mixed diff with a second feature; no clear base | No inference of implementation from status or old code alone; clarify scope/stage/base before conclusions. |
| M3 / AC8 | Commit fixture code; clean tree; explicitly name its files/range. Repeat outside Git with explicit files | Review selected implementation despite empty diff; outside Git note missing history. Never assume last commit is this feature. |
| M4 / AC5, AC7 | Explicit plan/code with missing documents; `010 nonsense`, `010 spec code` | Missing prerequisites/unknown or conflicting arguments explained; no invented document, no silent fallback or conformance claim. |
| R1 / AC6, AC9–AC10 | Review selected faulty CSV fixture and its weak test | Concrete AC2 finding with severity/scenario/location/check method; chat first; no code/docs/config edits or tests/builds. Distinguish prior test results from current inspection. |
| R2 / AC10–AC11 | Draft spec, stale plan digest, unchecked verification, completed feature, no-defect fixture | Draft/done review allowed; stale/missing approvals/checks remain limitations, never fixed or approved. Scoped no-defect conclusion when appropriate. |
| W1 / AC9, AC14 | After report, decline saving or do not answer; then explicitly save in a fresh case | No file until choice. Only review.md created after consent, with feature/date/mode/scope/limitations and real findings. |
| W2 / AC14 | Existing report below; say only yes to save, then choose extend | Clarify replace/extend first. Extend one report: stable IDs, preserved comments, new unique IDs, no appended second report. |
| W3 / AC14 | Fix F1 in fixture, leave F2 outside scope; extend after inspecting only F1 area | F1 checked with fixed/date/evidence; F2 retained with not-rechecked note. Silence about F2 never closes it. No tests run. |
| W4 / AC14 | Explicit replace; in separate cases edit/create report between offered choice and saving, use report/parent link, deny write access | Replace only on explicit choice; concurrent change requires renewed agreement; unsafe link refused; write failure reported with chat report retained. No status changes. |
| I1 / AC12 | Isolated install, four-skill upgrade, repeat, preview, per-agent/full removal, existing NDD skill names and missing review resource | Six skills and resources copied; existing NDD skills replaced without retained backups; dry-run/missing-resource failure causes no writes; receipts preserve ownership checks; removal keeps other agent/custom skills and project documents. Use automated tests plus native Windows shells. |

Existing report for W2/W3 (adjust date to your fixture; these are sample findings):

```markdown
# Review: ak-010-csv
- Last review: 2026-11-01
- Mode: code
- Scope: export.py and import.py
- Limitations: tests not run

## Findings
- [ ] F1 — medium: CSV fields with commas are not quoted.
  - Location: export.py, export_csv
  - User comments: Keep the public function signature unchanged.
- [ ] F2 — medium: importer rejects a valid empty field.
  - Location: import.py, parse_row
  - Last checked: 2026-11-01
```

To test fixed status, implement proper CSV escaping in the fixture yourself
between reviews, then explicitly select export.py. Add a new distinct defect for
an additional finding; it must receive F3, not reuse F1/F2. For a regression,
restore the original defect: F1 should reopen with current evidence.

## Recording results

For every OS/agent combination keep a case table with actual observations and
artifacts. Mark inaccessible tools or unperformed scenarios **blocked/not run**,
not passed. Automated installer and packaging success does not close the agent
behavior criteria. Keep the feature in progress until required acceptance checks
are observed. These instructions do not authorize publishing or pushing results.
