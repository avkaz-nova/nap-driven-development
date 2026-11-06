<!-- ndd-kit:start v{{VERSION}} -->
## NDD workflow

Use NDD when explicitly requested: `ndd-spec` → review → `ndd-plan` → review → `ndd-do`.
Invoke skills with `/ndd-*` in Claude Code or `$ndd-*` in Codex CLI/IDE.
Specs: `{{SPECS_DIR}}/NNN-feature-slug/spec.md`; plans: the adjacent `plan.md`.
Templates: `{{SPECS_DIR}}/_templates/`. Preserve existing project rules and tooling.

- Spec = agreed behaviour; plan = approach, tasks and verification evidence.
- Require an approved spec and current approved plan before implementation.
- If implementation disagrees with the spec, investigate. Fix an implementation
  bug against the agreed spec; changing intended behaviour requires spec review.
- One task per invocation by default; fresh sessions are optional.
- Record verification before marking work complete. Keep specs/plans with code.
- NDD does not authorize commits, pushes, deployments or production operations.
- Small fixes can skip this workflow unless the user or project requires it.
<!-- ndd-kit:end -->
