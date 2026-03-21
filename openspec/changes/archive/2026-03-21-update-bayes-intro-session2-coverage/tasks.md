## 1. Analysis
- [x] 1.1 Build a topic coverage matrix between `materials/buoi 2 - gioi thieu ve Bayesian.pptx` and current `contents/vi/chapter01/_posts/*.md` lessons.
- [x] 1.2 Confirm and document the concrete missing topics to add (formula recap, confusion matrix framing, and session logistics metadata).
- [x] 1.3 Extract and verify Session 2 example content (including image-based slides) for VD1/VD2/VD3 before drafting edits.

## 2. Content Updates
- [x] 2.1 Update `contents/vi/chapter01/_posts/2025-01-05-01_00_course_introduction.md` to include Session 2 logistics details (reference list and grading split) in course style.
- [x] 2.2 Update `contents/vi/chapter01/_posts/2025-01-02-01_03_bayes_theorem_posterior.md` with a concise prerequisite block for conditional probability and total probability used in Bayes theorem.
- [x] 2.3 Add confusion-matrix-based diagnostic interpretation to the Bayes theorem lesson, including sensitivity/specificity and base-rate-aware reading.
- [x] 2.4 Add Session 2 worked examples into Chapter 1 lesson flow: VD1 (rare-disease test), VD2 (Holmes/Watson icy-road), and VD3 (two-test sequential update), with explicit equations and interpretations.
- [x] 2.5 Adjust Chapter 1 cross-links/order cues if needed so new additions are discoverable in the lesson flow.

## 3. Validation
- [x] 3.1 Run `bundle exec jekyll build --verbose` and resolve rendering issues.
- [x] 3.2 Manually verify touched pages render math and image links correctly with `{{ site.baseurl }}` compatibility.
- [x] 3.3 Run `openspec validate update-bayes-intro-session2-coverage --strict`.
