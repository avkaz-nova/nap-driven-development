---
id: 001-cold-start-fallback
status: approved
owner: example
created: 2026-11-06
---

# Cold-start fallback for recommendations

This is an illustrative, reviewed specification; the example has not been implemented.

## Problem and users
New titles have too few interactions for collaborative recommendations. Viewers
need useful neighbours even when a title has just entered their catalogue.

## Requirements
- R1: At the daily run, titles with fewer than 20 interactions in the preceding
  30 days use content metadata for candidates. Titles with 20 or more retain
  existing collaborative candidate generation.
- R2: Fill each cold title's list to at most 10 distinct eligible recommendations.
  Use content candidates first, then popular items of the same primary genre.
  With no primary genre, use popular items across all genres. If fewer than 10
  eligible items exist in these pools, return the available items without duplicates.
- R3: Never recommend the source title or titles unavailable in the selected
  catalogue. Apply exclusions before deciding how many fill candidates are needed.
- R4: Record `strategy` on EACH recommendation row: `collaborative` for warm
  candidate generation, `content` for cold content candidates, `popular_fill`
  for top-up candidates. A list can contain multiple strategies.
- R5: Missing description embeddings must not fail the run: use genre/tag
  metadata. Missing all content metadata produces no content candidates and
  falls through to the applicable popular pool. Routing changes at the next daily run.

## Non-goals
- Personalisation per viewer; changing the collaborative model for warm titles.
- Proving a CTR improvement before shipping this engineering change.

## Edge cases
- Boundaries at 19/20 interactions and interactions outside the 30-day window.
- Missing embedding, missing genre, or no content metadata.
- Duplicate, excluded and insufficient fill candidates; an empty eligible pool.

## Acceptance criteria
- AC1 (R1): Fixtures at 19 and 20 interactions take content and collaborative
  generation respectively; events older than 30 days don't affect classification.
  A candidate that only exists in the content fixture appears for the cold title.
- AC2 (R2, R4): With 3 eligible content candidates and at least 7 distinct
  eligible same-genre popular titles, return 10 rows: 3 `content`, 7 `popular_fill`.
- AC3 (R2, R3): With fewer than 10 eligible distinct titles after exclusions,
  return exactly those titles. With none, return an empty list without error.
- AC4 (R3): Whole-output validation finds zero self-recommendations, unavailable
  recommendations or duplicate (source, catalogue, recommendation) rows.
- AC5 (R4): Every output row has the strategy of the generator that supplied it;
  warm-item fixtures are `collaborative`. A non-null check alone is insufficient.
- AC6 (R2, R5): Without embeddings, candidates use available genre/tags; without
  a genre, top-up uses overall popularity; with no metadata, generation still
  succeeds using eligible overall-popular candidates.
- AC7 (R1, R5): A title crossing the threshold after one daily snapshot changes
  routing at the next snapshot, with no mid-run switch. Warm fixtures retain
  the same recommendation ids and ordering as the current pipeline.

## Later business measurement
Run a separate A/B experiment on cold-title row CTR; a +10% relative lift is a
hypothesis, not an unverified release acceptance criterion.

## Open questions
None.
