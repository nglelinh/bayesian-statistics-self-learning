## Why
Session 6 material (`materials/buoi 6 - phoi hop.pptx`) introduces Bayesian decision and testing concepts (loss, posterior risk, Bayes hypothesis testing, Bayes factor, one-sided/two-sided testing, and mixture priors/posteriors). Current course coverage is fragmented: decision-loss framing appears in later Chapter 8, mixture prior ideas appear in Chapter 2, and Bayes-factor-based testing is not clearly covered in the main Bayesian lesson flow.

## What Changes
- Add a Session 6 topic-coverage audit that maps slide topics to existing course lessons.
- Fill missing Session 6 coverage in the published course with a coherent bridge from posterior inference to decision/testing.
- Ensure explicit instructional coverage for:
  - posterior risk and loss-based decision rules,
  - Bayesian hypothesis testing framing (one-sided vs two-sided decisions),
  - Bayes factor interpretation as evidence ratio,
  - mixture prior and mixture posterior weight-updating intuition.
- Preserve Session 6 worked-example fidelity (OCR-backed for image slides), including a binary MAP detection example, an asymmetric-cost alarm decision example, and at least one mixture-prior posterior-weight update example.
- Keep updates scoped to existing Bayesian course chapters and avoid unrelated refactors.

## Impact
- Affected specs: `publish-course-content`
- Affected content (expected):
  - `contents/vi/chapter08/_posts/2025-01-05-08_04_decision_analysis.md`
  - `contents/vi/chapter02/_posts/2025-01-02-02_03_prior.md`
  - `contents/vi/chapter02/_posts/2025-01-02-02_04_posterior.md`
  - `contents/vi/chapter08/index.html` (if lesson ordering or links need updates)
- Potential EN parity updates (if corresponding lessons are touched):
  - `contents/en/chapter08/_posts/`
  - `contents/en/chapter02/_posts/`
