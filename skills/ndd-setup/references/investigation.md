# Investigation and evidence

Use this procedure when an unresolved question could materially change the
requirements or implementation. Task size alone is not a reason to investigate.
Reuse reliable findings while their relevant inputs and environment are unchanged.

## Choose the stage

- Spec: establish current behaviour relevant to requirements; leave implementation
  exploration to planning. Mark unresolved material questions as clarifications.
- Plan: resolve uncertainty that prevents a credible implementation plan with a
  bounded experiment. If it needs substantial work, propose an investigation-only
  plan for approval, identifying delivery criteria not yet planned or satisfied.
- When the approach is credible but needs confirmation, put investigation first
  and identify which later tasks depend on its findings. Do not repeat completed
  analysis or add a generic "analyze the codebase" task.

Each investigation needs a specific question, identified inputs, a check and an
expected observation that would answer it. Keep hypotheses separate from findings.

## Obtain evidence

Verify testable claims using existing tests, commands or focused scripts. Static
claims can use source inspection with file references; behavioural claims need
executed checks or an actual, recorded manual observation. LLM explanations,
another model's agreement, an unexecuted script or exit code zero alone are not
completion evidence. Check that assertions address the question; a sample result
does not establish an entire population's state.

Record the reproducible command/procedure, input fixture or revision, relevant
environment, expected versus observed outcome, supported finding and limitations
in the existing spec/plan. Use a short evidence note, not a new analysis document
or full logs. Do not put secrets or unsanitized captured data in shared documents.

Inspect commands and imported entry points for external effects before running.
Stay within existing authorization; scratch files do not authorize production
writes, notifications, uploads or dependency installation.

## Optional scratch scripts

Prefer existing checks. When a new probe is needed, spec and plan may create/run
isolated scripts and sanitized inputs in `.ndd-sandbox/` or a host temporary
directory. This narrow exception does not permit application, permanent test,
dependency or configuration changes during those phases. Do may add lasting
regression tests/fixtures to the project's normal test directories within scope.

Create scratch space only when needed, with task-specific names. Keep paths within
the permitted workspace; do not follow redirected paths. Preserve existing files
and never automatically clear the directory. Use an ignored location; a newly
created `.ndd-sandbox/` may contain a local `.gitignore` with `*`. Do not overwrite
existing ignore rules or edit tracked configuration for this. If exclusion cannot
be established, use a permitted temporary directory. Keep enough sanitized inputs
and instructions to reproduce useful findings; do not rely solely on a temporary
path that another session cannot access.

## Completion and continuation

Executing an approved investigation-only plan through `ndd-do` includes recording
evidence and task progress in the existing plan under the usual NDD write scope.
"Investigation-only" limits implementation, not those records. Honor an explicit
read-only request; in that case report findings and any unrecorded progress.

An expected defect reproduction can complete its investigation task when the
specific expected failure is observed and explained. An unrelated exception,
missing tool, unavailable input or inconclusive result cannot: leave it unchecked
and block dependent work. Do not weaken the check to obtain completion.

If findings support the approved approach, continue its dependent tasks without
another approval. Material changes to scope or approach require review and renewed
approval of the affected spec/plan. An investigation-only plan ends with findings
and a proposed next planning step, not unplanned implementation. Completing its
tasks does not satisfy delivery ACs or mark the feature done; those still require
implementation and final acceptance evidence.
