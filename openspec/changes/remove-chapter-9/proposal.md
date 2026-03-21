## Why
Chapter 9 is currently active in the Vietnamese curriculum (`contents/vi/chapter09/`), but the requested change is to remove this chapter from the published course. Retiring it cleanly requires removing chapter files and also updating navigation and next-step links so learners are not routed into `/vi/chapter09/`.

## What Changes
- **BREAKING** Retire `contents/vi/chapter09/` from the active published curriculum.
- Update global navigation and chapter-level next-step cues so Chapter 9 no longer appears as an active destination.
- Update any tracked practice-material references that point to Chapter 9 URLs.
- Keep scope focused to active-course visibility and links; no legacy redirect layer is introduced by default.

## Impact
- Affected specs:
  - `publish-course-content`
  - `build-multilingual-site`
  - `deliver-practice-materials`
- Affected content/code (expected):
  - `contents/vi/chapter09/index.html`
  - `contents/vi/chapter09/_posts/*`
  - `contents/vi/chapter09/practice_09.ipynb`
  - `_includes/sidebar.html`
  - `contents/vi/chapter08/_posts/2025-01-05-08_04_decision_analysis.md`
  - tracked files under `public/generated/labs/` only if Chapter 9 links are present
- Assumption:
  - Chapter 9 is removed from the active learning path without adding compatibility redirects unless explicitly requested later.
