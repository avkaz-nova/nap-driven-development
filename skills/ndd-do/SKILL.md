---
name: ndd-do
description: Implement and verify the next task in an approved, current NDD plan. Invoke explicitly with ndd-do; do not start from an unapproved or stale plan.
argument-hint: "<feature id | path to plan.md> [task id]"
disable-model-invocation: true
---

# ndd-do

Implement one task per invocation by default. If the user explicitly requests
several tasks, perform them in order, checking the same gates before each.
A fresh session is optional; spec, plan and recorded evidence carry the context.

## Before editing

1. Read applicable instructions, the spec, plan, relevant code and tests, and
   Git status if available. Preserve unrelated changes. A manifest or project
   templates are not required. If legacy NDD files exist, follow the
   [existing-project guidance](../ndd-setup/references/project-state.md).
   Resolve the feature with the shared
   [prefix and identifier rules](../ndd-setup/references/feature-ids.md): `001`
   uses the current user's confirmed prefix; a qualified id/full folder name/path
   selects an explicit feature. Report the resolved path and task id; explain
   missing feature files or task ids without creating setup files.
   If the spec is already done, report it without editing unless the user
   requests a new revision through `ndd-spec`.
2. Require spec status `approved` or `in-progress` and no unresolved
   `[NEEDS CLARIFICATION]`. Recompute the spec digest using the
   sibling `ndd-plan/scripts/spec-digest.sh` or `.ps1` as documented in that
   skill. Require equality with the plan's `spec_digest`. Missing metadata,
   a failed helper or a mismatch blocks implementation; return to spec/plan
   review. Do not silently update the digest or grant approval yourself.
3. Require plan status `approved`. A clear approval of the displayed current
   plan in this conversation can be recorded now, after the digest check;
   a bare `ndd-do 001` is not retrospective approval.
   If all tasks are checked, perform any outstanding final acceptance checks
   instead of inventing another task.
4. Select the requested task or first unchecked one. Respect prerequisites;
   don't repeat a checked task without an explicit reason. State its R/AC scope.
   Inspect verification commands for external effects before execution.

## Implement and verify

- Choose the verification method first. For bugs, reproduce the symptom and
  add a meaningful regression test where feasible. For other work, use suitable
  tests, builds, static checks or a documented manual check; do not manufacture
  a failing test for a documentation edit or already-covered behaviour.
- Implement the smallest coherent change. Keep existing architecture and
  dependencies unless an approved requirement justifies a change.
- Run task verification, related tests and required project checks. Do not
  weaken checks, hide unexpected failures or fix unrelated failures to go green.
- On a behavioural contradiction, stop and propose a spec correction. Once
  approved, revise the spec and review the affected plan before continuing.
  Small implementation details within approved scope can go in Decisions.
  Changes to approach, scope, dependencies or external effects require review.
- Check off a task only when its required checks pass. Record a concise result
  in the plan: task/AC, command or observation, outcome and relevant limitation.
  If blocked, leave it unchecked and record what remains. Set the spec to
  `in-progress` when implementation starts.
- When all tasks are complete, verify every AC against the assembled feature,
  run required final project checks, and review the diff for unintended changes.
  Mark the spec `done` only when that evidence is recorded. Missing tools,
  unperformed manual checks or pre-existing failures are not passing results.

Report changes, verification, remaining blockers and a suggested commit message.
Do not commit, push, deploy, change shared data or run production workflows
unless separately authorized. Recommend committing code and its spec/plan
updates together. Stop after the requested task(s).

When a diagram helps explain a change or a blocker, use the
[rounded Unicode diagram style](../ndd-setup/references/diagrams.md).
