## Why
Chapter 00 currently mixes writing tones and depth across lessons, which makes the learning experience less coherent than the opening lesson `00_01_probability_basics`. A chapter-wide writing upgrade is needed so learners encounter a consistent scientific style, stronger conceptual motivation, and clearer mathematical exposition from prerequisite topics through modeling foundations.

## What Changes
- Improve all Vietnamese Chapter 00 lessons under `contents/vi/chapter00/_posts/` using `00_01_probability_basics` as the writing-quality reference.
- Standardize chapter prose to a scientific, motivation-first lecture style aligned with rules in `.cursor/rules` (especially narrative continuity, generative-story framing, interpretation-first explanations, and careful term annotation).
- Strengthen mathematical exposition where needed by adding or refining formal statements and derivation flow while preserving the existing curriculum sequence and links.
- Keep edits scoped to style, clarity, and pedagogical rigor (no curriculum reordering, no new tooling, no structural site changes).

## Impact
- Affected specs: `publish-course-content`
- Affected content scope:
  - `contents/vi/chapter00/_posts/*.md`
  - style references from `.cursor/rules/lecture-notes-rule.mdc`, `.cursor/rules/math-formula-rule.mdc`, `.cursor/rules/illustration-rule.mdc`
- User-visible outcome: Chapter 00 reads as a coherent scientific chapter with consistent lecture voice, clearer explanations, and mathematically explicit transitions.
