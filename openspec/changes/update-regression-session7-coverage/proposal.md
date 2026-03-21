## Why
Session 7 material (`materials/buoi 7 - hoi quy.pptx`) covers Bayesian linear regression foundations including OLS assumptions, joint likelihood/prior/posterior framing, slope interval estimation under known vs unknown variance, and multivariate matrix form. Current Chapter 4 lessons already teach generative regression and PyMC workflow, but they do not explicitly trace all Session 7 elements (especially joint-distribution derivation cues and matrix-form extension).

## What Changes
- Add a Session 7 coverage-audit step that maps slide topics to Chapter 4 lessons.
- Fill identified content gaps from Session 7 in the regression lesson flow, with motivation-first explanations.
- Ensure explicit coverage for:
  - classical regression assumptions and their role before Bayesian inference,
  - joint likelihood/prior/posterior view for regression parameters,
  - slope interval interpretation with known-variance vs unknown-variance context,
  - transition from univariate to multivariate linear regression in matrix notation.
- Keep updates scoped to existing Chapter 4 regression content and avoid unrelated refactors.

## Impact
- Affected specs: `publish-course-content`
- Affected content (expected):
  - `contents/vi/chapter04/_posts/2025-01-02-04_01_linear_regression_generative.md`
  - `contents/vi/chapter04/_posts/2025-01-02-04_03_posterior_inference_pymc.md`
  - `contents/vi/chapter04/_posts/2025-01-02-04_04_model_checking_prediction.md` (if assumptions diagnostics are linked)
  - `contents/vi/chapter04/index.html` (if navigation cues are required)
- Potential EN parity updates (if corresponding VI lessons are edited):
  - `contents/en/chapter04/_posts/`
