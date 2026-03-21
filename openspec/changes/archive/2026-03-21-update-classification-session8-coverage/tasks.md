## 1. Analysis
- [x] 1.1 Build a Session 8 topic checklist from `materials/buoi 8 - phan lop.pptx` (posterior classification, risk rules, discriminant functions, Gaussian cases, reject option).
- [x] 1.2 Map Session 8 topics to Chapter 6 lessons and mark each item as covered, partial, or missing.
- [x] 1.3 Document concrete content gaps and decide whether updates fit existing lessons or need one dedicated classification-theory lesson.
- [x] 1.4 Extract and verify Session 8 worked examples (fruit-prior shift, risk-with-reject action, discriminant transforms) from slide text/image content.

## 2. Content Updates
- [x] 2.1 Add or refine posterior-based Bayesian classification rule coverage (`P(c_i|x) \propto P(x|c_i)P(c_i)`) with clear interpretation.
- [x] 2.2 Add minimum-risk decision-rule coverage with loss matrix, including defer/reject action and expected risk interpretation.
- [x] 2.3 Add discriminant-function formulation and equivalent monotone-transform forms used for practical computation.
- [x] 2.4 Add Gaussian class-conditional boundary cases (shared covariance vs class-specific covariance) and explain resulting decision boundaries.
- [x] 2.5 Add at least one worked example linking priors, class-conditional likelihoods, posterior class probabilities, and action choice under loss.
- [x] 2.6 Add Session 8 example set fidelity: include the two-class/three-action reject-option example and at least one discriminant/log-discriminant computation path.
- [x] 2.7 Update chapter navigation/cross-links so Session 8 additions are discoverable in learning order.
- [x] 2.8 Keep EN/VI parity for corresponding lesson updates when paired English pages exist.

## 3. Validation
- [x] 3.1 Run `bundle exec jekyll build --verbose` and resolve rendering issues.
- [x] 3.2 Verify touched pages render formulas, links, and image paths correctly with `{{ site.baseurl }}` compatibility.
- [x] 3.3 Run `openspec validate update-classification-session8-coverage --strict`.
