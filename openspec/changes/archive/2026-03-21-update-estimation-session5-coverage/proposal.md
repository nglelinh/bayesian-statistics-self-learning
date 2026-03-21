## Why
Session 5 material (`materials/buoi 5 - uoc luong.pptx`) focuses on Bayesian point and interval estimation (MAP, MMSE/posterior mean, and interval estimation), but these topics are currently distributed across lessons without an explicit Session 5 coverage trace. A targeted audit is needed to identify missing or weak coverage and add it clearly to the course flow.

## What Changes
- Add a Session 5 topic-coverage audit that maps slide topics to current Chapter 2 Bayesian inference lessons.
- Update lessons to close any Session 5 gaps in estimation-focused teaching, especially:
  - MAP as posterior mode and its optimization form,
  - relationship between MAP and maximum likelihood under different priors,
  - posterior mean as Bayes estimator under squared-error loss (MMSE framing),
  - Bayesian interval estimation interpretation and construction.
- Preserve Session 5 example fidelity (OCR-backed where needed) by covering representative worked problems: MAP with continuous prior + geometric likelihood, ML vs MAP in Gaussian channel model, MMSE posterior-mean derivation, and a credible-interval computation from conditional normal posterior.
- Ensure at least one end-to-end worked example compares two point estimators (e.g., MAP vs posterior mean, or MAP vs MLE) and links to interval interpretation for the same posterior.
- Keep edits scoped to existing Chapter 2 content and current teaching conventions.

## Impact
- Affected specs: `publish-course-content`
- Affected content (expected):
  - `contents/vi/chapter02/_posts/2025-01-02-02_02_likelihood.md`
  - `contents/vi/chapter02/_posts/2025-01-02-02_04_posterior.md`
  - `contents/vi/chapter02/index.html` (only if navigation cues are needed)
- Potential affected assets: `img/chapter_img/chapter02/` (only if new figures/examples are required)
