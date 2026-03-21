## Why
Session 4 material (`materials/buoi 4 - lien hop.pptx`) includes conjugate-prior content plus prerequisite refreshers (Gamma function, Beta/Gamma/Normal recap, and approximation notes) that are not explicitly tracked against current published lessons. A focused audit is needed to confirm what is already covered and add any missing Session 4 concepts to the course.

## What Changes
- Add a Session 4 topic-coverage audit step that maps slide topics to existing Chapter 2 lessons.
- Update conjugacy-related lessons where the audit finds missing or weak coverage from Session 4.
- Ensure the course explicitly includes:
  - the definition of conjugacy in Bayesian inference and core pairs (Beta-Binomial, Gamma-Poisson, Normal-Normal),
  - prerequisite recap needed by Session 4 (Gamma function role and Beta/Gamma/Normal parameterization context),
  - approximation caveats noted in Session 4 (e.g., when Normal approximation is reasonable for Beta/CLT-style sums).
- Keep edits tightly scoped to Chapter 2 content and existing style conventions.

## Impact
- Affected specs: `publish-course-content`
- Affected content (expected):
  - `contents/vi/chapter02/_posts/2025-01-02-02_01_probability_distributions.md`
  - `contents/vi/chapter02/_posts/2025-01-02-02_05_conjugate_priors.md`
  - `contents/vi/chapter02/index.html` (only if chapter navigation cues are needed)
- Potential affected assets: `img/chapter_img/chapter02/` (only if new figures are required)
