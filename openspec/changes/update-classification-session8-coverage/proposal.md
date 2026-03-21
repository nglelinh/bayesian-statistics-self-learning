## Why
Session 8 material (`materials/buoi 8 - phan lop.pptx`) presents Bayesian pattern classification with explicit prior-likelihood-posterior classification rules, risk-minimizing decision rules, discriminant-function formulations, rejection action, and Gaussian-case decision boundaries. Current course coverage in Chapter 6 focuses on logistic/Poisson GLMs and evaluation metrics, but does not explicitly provide a full Session 8-style Bayesian classifier decision-theory pathway.

## What Changes
- Add a Session 8 topic-coverage audit that maps slide-level classification topics to existing Chapter 6 lessons.
- Fill missing Session 8 content in the course with a coherent Bayesian classification narrative from posterior class probabilities to decision actions.
- Ensure explicit instructional coverage for:
  - posterior-based class assignment from `P(c_i|x) \propto P(x|c_i)P(c_i)`,
  - minimum-risk decision rule with configurable loss matrix (including reject/defer action),
  - discriminant-function view and equivalent monotone transforms (e.g., log discriminants),
  - Gaussian class-conditional cases and implications for linear vs quadratic decision boundaries.
- Preserve Session 8 worked-example fidelity, including: prior-shift fruit classification intuition, the two-class/three-action risk example (with reject option), and discriminant/log-discriminant computation examples.
- Keep edits tightly scoped to classification-related lessons and existing teaching style conventions.

## Impact
- Affected specs: `publish-course-content`
- Affected content (expected):
  - `contents/vi/chapter06/_posts/2025-01-02-06_01_logistic_regression.md`
  - `contents/vi/chapter06/_posts/2025-01-02-06_03_model_evaluation_glm.md`
  - `contents/vi/chapter06/index.html` (if chapter-level navigation cues are needed)
- Potential new/updated lesson file (if scope requires a dedicated theory lesson):
  - `contents/vi/chapter06/_posts/` (classification decision-theory topic)
- Potential EN parity updates (if paired pages are edited):
  - `contents/en/chapter06/_posts/`
