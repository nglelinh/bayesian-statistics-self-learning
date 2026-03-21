## 1. Analysis
- [ ] 1.1 Build a topic coverage matrix between `materials/buoi 2 - gioi thieu ve Bayesian.pptx` and current `contents/vi/chapter01/_posts/*.md` lessons.
- [ ] 1.2 Confirm and document the concrete missing topics to add (formula recap, confusion matrix framing, and session logistics metadata).

## 2. Content Updates
- [ ] 2.1 Update `contents/vi/chapter01/_posts/2025-01-05-01_00_course_introduction.md` to include Session 2 logistics details (reference list and grading split) in course style.
- [ ] 2.2 Update `contents/vi/chapter01/_posts/2025-01-02-01_03_bayes_theorem_posterior.md` with a concise prerequisite block for conditional probability and total probability used in Bayes theorem.
- [ ] 2.3 Add confusion-matrix-based diagnostic interpretation to the Bayes theorem lesson, including sensitivity/specificity and base-rate-aware reading.
- [ ] 2.4 Adjust Chapter 1 cross-links/order cues if needed so new additions are discoverable in the lesson flow.

## 3. Validation
- [ ] 3.1 Run `bundle exec jekyll build --verbose` and resolve rendering issues.
- [ ] 3.2 Manually verify touched pages render math and image links correctly with `{{ site.baseurl }}` compatibility.
- [ ] 3.3 Run `openspec validate update-bayes-intro-session2-coverage --strict`.
