## Context
Chapter 11 is a small but fully published section of the Vietnamese course, and it is currently wired into the site in three ways: a dedicated chapter tree under `contents/vi/chapter11/`, a hard-coded sidebar chapter list that includes `11`, and downstream references from Chapter 10 plus at least one lab solution/export. A clean retirement needs to remove the content and also prevent learners from encountering stale pointers.

## Goals / Non-Goals
- Goals:
  - Remove Chapter 11 from the active curriculum.
  - Ensure active navigation and cross-links do not point into retired Chapter 11 URLs.
  - Keep the course flow coherent after the removal.
- Non-Goals:
  - Rewriting Chapter 11 material into another chapter.
  - Preserving legacy Chapter 11 URLs with redirects in this change.

## Decisions
- Decision: Treat Chapter 11 as retired content rather than hidden content.
  - Why: The user asked to remove it, and the active curriculum should not carry a dormant published chapter in the main tree.
- Decision: Keep Chapter 12 in the curriculum as the lab track that follows the lecture sequence.
  - Why: Chapter 12 is already framed as a generated practice chapter and is the closest active continuation after Chapter 10.
- Decision: Update practice-material references at the source and regenerate tracked HTML exports.
  - Why: Generated HTML should stay consistent with the notebook sources instead of being hand-edited independently.

## Risks / Trade-offs
- Removing Chapter 11 without redirects means any external bookmarks to its URLs will stop resolving.
- Retiring a chapter can leave subtle orphan references unless both source notebooks and generated outputs are audited.

## Migration Plan
1. Remove the Chapter 11 content tree.
2. Update active navigation and next-step links.
3. Remove or replace remaining Chapter 11 references in lessons and practice materials.
4. Regenerate any tracked generated outputs that embed retired links.
5. Rebuild the site and verify no active Chapter 11 links remain.

## Open Questions
- None for the initial retirement proposal; if redirects are later desired, they can be added in a follow-up change.
