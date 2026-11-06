---
status: approved
spec_digest: 31e11a9a0167ae332f3cb148d8df2563ad84e8a8c9b2a13f1f065a72ca5ec6bc
---

# Plan: Cold-start fallback

Spec: ./spec.md

Illustrative approved plan. Commands name tests that would be added to a host
project; they are not runnable tests supplied by this kit. No task is complete.

## Approach
Classify source titles at the daily snapshot. Preserve the warm route. For cold
titles use content candidates (embedding similarity with genre/tag metadata,
or genre/tag-only retrieval when embeddings are absent). Filter and deduplicate
before filling from same-genre popularity, or overall popularity without a genre.
Attach a strategy to each row at its generator, not to the entire list.

## Affected components and contracts
- Daily candidate generation, routing and validation.
- Recommendation rows add `strategy` (`collaborative|content|popular_fill`).
- Candidate retrieval and filling operate within one catalogue at a time.

## Risks and rollback
- Poor content neighbours: inspect a fixed sample alongside automated validation.
- Feature flag disables the cold route; retain the column as `collaborative`
  when serving the original route. Test both flag states.

## Tasks
- [ ] T1 (R1, R5, AC1, AC7): snapshot routing and warm-route regression fixtures — verify: `python -m pytest tests/test_routing.py`
- [ ] T2 (R1, R5, AC1, AC6): content retrieval and missing-metadata cases — verify: `python -m pytest tests/test_content_candidates.py`
- [ ] T3 (R2, R3, AC2, AC3, AC4, AC6): exclusions, deduplication and eligible popular fill — verify: `python -m pytest tests/test_popular_fill.py`
- [ ] T4 (R4, AC2, AC5): attach and validate per-row provenance — verify: `python -m pytest tests/test_strategy.py`
- [ ] T5 (R1–R5, AC1–AC7): integrate behind flag; validate complete fixture output and rollback — verify: `python -m pytest tests/test_daily_recommendations.py`

## Acceptance coverage
| AC | Tasks | Final verification |
|---|---|---|
| AC1 | T1, T2, T5 | Boundary/window fixtures and generator-specific candidates |
| AC2 | T3, T4, T5 | Full list has the specified 3/7 composition |
| AC3 | T3, T5 | Insufficient/empty fixture pools produce exact eligible sets |
| AC4 | T3, T5 | Complete fixture output passes exclusion and uniqueness checks |
| AC5 | T4, T5 | Each row's provenance matches its generator |
| AC6 | T2, T3, T5 | All three missing-metadata paths run end-to-end |
| AC7 | T1, T5 | Daily transition and warm-route regression comparison |

## Verification results
None yet. The host project's required checks and sample review remain outstanding.

## Decisions
None yet.
