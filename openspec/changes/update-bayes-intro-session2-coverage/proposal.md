## Why
The source slide deck for Session 2 (`materials/buoi 2 - gioi thieu ve Bayesian.pptx`) and the published course pages are not fully aligned. Core introductory elements from the session (especially explicit confusion-matrix framing for diagnostic Bayes reasoning and a compact prerequisite formula recap) are either missing or not clearly surfaced in the current lesson flow.

## What Changes
- Add a Session 2 coverage audit step that maps slide topics to existing Vietnamese course lessons before editing content.
- Update Chapter 1 introduction content to close identified gaps from Session 2, with motivation-first explanations and worked examples.
- Add missing instructional coverage for:
  - conditional probability and total-probability recap used by Bayes theorem,
  - confusion matrix interpretation (sensitivity, specificity, false positive context) tied to Bayes diagnostic reasoning,
  - explicit Session 2 course logistics details (core references and grading split) on the course introduction page.
- Keep links and assets `{{ site.baseurl }}` compatible and preserve existing front matter conventions.

## Impact
- Affected specs: `publish-course-content`
- Affected content:
  - `contents/vi/chapter01/_posts/2025-01-05-01_00_course_introduction.md`
  - `contents/vi/chapter01/_posts/2025-01-02-01_03_bayes_theorem_posterior.md`
  - `contents/vi/chapter01/_posts/2025-01-02-01_04_bayesian_vs_frequentist.md` (if cross-links/order cues are needed)
- Potential affected assets: `img/chapter_img/chapter01/` (only if new figures are required)
