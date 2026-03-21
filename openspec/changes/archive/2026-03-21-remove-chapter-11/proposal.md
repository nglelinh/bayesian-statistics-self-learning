## Why
Chapter 11 is currently published as part of the active Vietnamese course path, but the curriculum direction has changed and this chapter should be retired. Removing it cleanly requires more than deleting three files because navigation, chapter-to-chapter cues, and at least one lab reference still point learners into Chapter 11.

## What Changes
- **BREAKING** Retire `contents/vi/chapter11/` from the active course and remove its lesson pages from the published curriculum.
- Update global navigation and chapter-level next-step cues so the active course path no longer exposes Chapter 11.
- Update practice-material references that still point to Chapter 11 content and regenerate any tracked exported artifacts that embed those links.
- Treat Chapter 10 as the end of the lecture sequence and keep Chapter 12 available as the lab track that follows the core lessons.

## Impact
- Affected specs:
  - `publish-course-content`
  - `build-multilingual-site`
  - `deliver-practice-materials`
- Affected content/code (expected):
  - `contents/vi/chapter11/index.html`
  - `contents/vi/chapter11/_posts/*`
  - `_includes/sidebar.html`
  - `contents/vi/chapter10/_posts/2025-01-04-10_04_bayesian_workflow_synthesis.md`
  - `labs/solutions/Lab_06_Solutions.ipynb`
  - `public/generated/labs/lab-06-solution.html`
- Assumption:
  - Retiring Chapter 11 removes it from the active site without preserving dedicated redirects for old Chapter 11 URLs unless explicitly requested later.
