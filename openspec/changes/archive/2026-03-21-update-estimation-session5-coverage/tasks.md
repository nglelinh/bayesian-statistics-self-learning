## 1. Analysis
- [x] 1.1 Build a Session 5 topic checklist from `materials/buoi 5 - uoc luong.pptx`, including key estimation concepts and exercise patterns.
- [x] 1.2 Map Session 5 topics to Chapter 2 lessons, especially `2025-01-02-02_02_likelihood.md` and `2025-01-02-02_04_posterior.md`.
- [x] 1.3 Document which Session 5 topics are fully covered, partially covered, or missing before edits.
- [x] 1.4 Extract and verify Session 5 image-based examples via OCR/manual review (MAP, ML vs MAP, MMSE, credible interval).

## 2. Content Updates
- [x] 2.1 Strengthen point-estimation coverage in Chapter 2 for MAP and posterior mean (MMSE framing) with clear interpretation and notation.
- [x] 2.2 Add/clarify MAP-vs-MLE comparison and prior-dependence conditions in the likelihood/posterior lesson flow.
- [x] 2.3 Strengthen Bayesian interval-estimation coverage with explicit probability statement and practical interpretation.
- [x] 2.4 Add Session 5 worked examples: one MAP derivation, one ML-vs-MAP comparison, one MMSE posterior-mean derivation, and one credible-interval computation.
- [x] 2.5 Add at least one coherent integrated example that presents point estimators and interval estimation from the same posterior.
- [x] 2.6 Update chapter-level orientation/cross-links if needed so Session 5 additions are easy to find in sequence.

## 3. Validation
- [x] 3.1 Run `bundle exec jekyll build --verbose` and fix any rendering issues.
- [x] 3.2 Verify touched pages render formulas, internal links, and image paths correctly with `{{ site.baseurl }}` compatibility.
- [x] 3.3 Run `openspec validate update-estimation-session5-coverage --strict`.
