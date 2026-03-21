## Why
Chapter 10 is currently published in the active Vietnamese curriculum (`contents/vi/chapter10/`), but the requested scope is to remove Chapter 10 from the course. Retiring it cleanly requires more than deleting one folder because chapter navigation, chapter-to-chapter next links, and tracked generated lab exports may still point learners into `/vi/chapter10/` URLs.

## What Changes
- **BREAKING** Retire `contents/vi/chapter10/` from the active published curriculum.
- Remove or update active navigation and chapter-level next-step cues so learners are not sent to Chapter 10 URLs.
- Update practice-material references (including tracked generated lab HTML) that still link to Chapter 10 lessons.
- Keep the removal tightly scoped to active-course visibility and references; no dedicated redirect pages for retired Chapter 10 URLs are added by default.

## Impact
- Affected specs:
  - `publish-course-content`
  - `build-multilingual-site`
  - `deliver-practice-materials`
- Affected content/code (expected):
  - `contents/vi/chapter10/index.html`
  - `contents/vi/chapter10/_posts/*`
  - `contents/vi/chapter10/practice_10.ipynb`
  - `_includes/sidebar.html` (if Chapter 10 appears in global navigation)
  - `contents/vi/chapter09/_posts/2025-01-04-09_03_multilevel_regression.md`
  - `public/generated/labs/*.html` entries that link to Chapter 10
- Assumption:
  - Chapter 10 retirement removes it from active course flow without adding compatibility redirects unless requested later.
