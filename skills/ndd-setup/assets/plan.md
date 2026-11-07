---
status: draft
spec_digest: <SHA-256 from the ndd-plan spec-digest helper>
---

# Plan: <Feature name>

Spec: ./spec.md

<Short approach and key implementation choice.>

## Tasks
<!-- Each AC needs task coverage and a concrete check. Include files where useful.
     Add a final integration check only when task checks are insufficient.
     Keep required project checks; no duplicate coverage table. -->
<!-- Add investigation first only for a material unresolved question. Name the
     question, inputs, check/expected observation and dependent tasks. For an
     investigation-only plan, state its limited scope and delivery ACs still unmet;
     implementation needs a subsequent approved plan. No mandatory analysis step. -->
- [ ] T1 (AC1): <Change and related tests.> — verify: `<command or observation>`

<!-- Keep simple tasks on one line. For a longer task, use this alternative:
- [ ] T1 (AC1): **<Short outcome>**
  - <Concrete action or constraint.>
  - Tools/method: <Only consequential tools, execution methods or limits.>
  - Verify: <Command or observable completion check.>
     Use one checkbox per task; ordinary bullets for details, numbered substeps
     only when their order matters. Tools/method is optional: omit it if the
     action or verification already says enough. No empty fields or routine
     file-reading/editing inventory. -->

## Results
<!-- After implementation, record concise task/AC, check, result and limitations,
     including relevant tool/method deviations rather than a tool inventory.
     Investigation evidence: reproducible command/procedure, inputs, relevant
     environment, expected/observed outcome, finding and limitations. An expected
     reproduction failure is not successful implementation; missing tools or
     inconclusive checks leave investigation and dependent work incomplete.
     Do not claim unperformed checks passed. -->

<!-- Aim for 100–250 words or fewer for ordinary tasks. Add risks, rollback,
     dependencies or decisions only when material. Preserve useful existing
     progress/evidence; changes of approach or scope need renewed approval. -->
