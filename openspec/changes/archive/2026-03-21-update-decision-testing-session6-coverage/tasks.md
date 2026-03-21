## 1. Analysis
- [x] 1.1 Build a Session 6 topic checklist from `materials/buoi 6 - phoi hop.pptx` (loss, posterior risk, testing, Bayes factor, mixture prior/posterior).
- [x] 1.2 Map Session 6 topics to current lessons in Chapter 2 and Chapter 8, marking each item as covered, partial, or missing.
- [x] 1.3 Document concrete content gaps before editing.
- [x] 1.4 Extract and verify Session 6 image-based examples via OCR/manual review (binary MAP test, asymmetric-cost alarm decision, mixture-prior examples).

## 2. Content Updates
- [x] 2.1 Strengthen decision-theory coverage in Chapter 8 with explicit posterior-risk interpretation for point and action decisions.
- [x] 2.2 Add or refine Bayesian hypothesis testing coverage (one-sided/two-sided framing) and Bayes factor interpretation in the appropriate lesson flow.
- [x] 2.3 Ensure mixture-prior to mixture-posterior weight-updating intuition is clearly linked between Chapter 2 prior/posterior lessons and Session 6 decision content.
- [x] 2.4 Add Session 6 worked examples covering: MAP detection rule, asymmetric-loss decision thresholding, and mixture-prior posterior-weight updating.
- [x] 2.5 Add at least one coherent integrated example connecting posterior inference, decision loss, and model/hypothesis comparison.
- [x] 2.6 Update chapter navigation/cross-links so Session 6 additions are discoverable in sequence.
- [x] 2.7 Keep EN/VI parity for any touched lesson pairs where corresponding English pages exist.

## 3. Validation
- [x] 3.1 Run `bundle exec jekyll build --verbose` and resolve rendering issues.
- [x] 3.2 Verify touched pages render formulas, links, and image paths correctly with `{{ site.baseurl }}` compatibility.
- [x] 3.3 Run `openspec validate update-decision-testing-session6-coverage --strict`.
