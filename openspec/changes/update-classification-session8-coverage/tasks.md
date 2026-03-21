## 1. Analysis
- [ ] 1.1 Build a Session 8 topic checklist from `materials/buoi 8 - phan lop.pptx` (posterior classification, risk rules, discriminant functions, Gaussian cases, reject option).
- [ ] 1.2 Map Session 8 topics to Chapter 6 lessons and mark each item as covered, partial, or missing.
- [ ] 1.3 Document concrete content gaps and decide whether updates fit existing lessons or need one dedicated classification-theory lesson.

## 2. Content Updates
- [ ] 2.1 Add or refine posterior-based Bayesian classification rule coverage (`P(c_i|x) \propto P(x|c_i)P(c_i)`) with clear interpretation.
- [ ] 2.2 Add minimum-risk decision-rule coverage with loss matrix, including defer/reject action and expected risk interpretation.
- [ ] 2.3 Add discriminant-function formulation and equivalent monotone-transform forms used for practical computation.
- [ ] 2.4 Add Gaussian class-conditional boundary cases (shared covariance vs class-specific covariance) and explain resulting decision boundaries.
- [ ] 2.5 Add at least one worked example linking priors, class-conditional likelihoods, posterior class probabilities, and action choice under loss.
- [ ] 2.6 Update chapter navigation/cross-links so Session 8 additions are discoverable in learning order.
- [ ] 2.7 Keep EN/VI parity for corresponding lesson updates when paired English pages exist.

## 3. Validation
- [ ] 3.1 Run `bundle exec jekyll build --verbose` and resolve rendering issues.
- [ ] 3.2 Verify touched pages render formulas, links, and image paths correctly with `{{ site.baseurl }}` compatibility.
- [ ] 3.3 Run `openspec validate update-classification-session8-coverage --strict`.
