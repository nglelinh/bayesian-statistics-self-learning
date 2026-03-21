## 1. Analysis
- [x] 1.1 Build a Session 3 topic checklist from `materials/buoi 3 - tien nghiem, hau nghiem.pptx`, including image-based content cues where text extraction is limited.
- [x] 1.2 Map Session 3 topics to `contents/vi/chapter02/_posts/2025-01-02-02_02_likelihood.md`, `contents/vi/chapter02/_posts/2025-01-02-02_03_prior.md`, and `contents/vi/chapter02/_posts/2025-01-02-02_04_posterior.md`.
- [x] 1.3 Document concrete missing or weakly covered topics before editing lessons.
- [x] 1.4 Extract and verify image-based Session 3 examples with OCR/manual image review, then map each recovered example to a target lesson section.

## 2. Content Updates
- [x] 2.1 Update Chapter 2 lessons to add any missing Session 3 concepts with motivation-first explanations and `$$...$$` math formatting.
- [x] 2.2 Ensure at least one complete prior-likelihood-posterior worked example is explicitly connected across the chapter flow.
- [x] 2.3 Add at least one OCR-recovered Session 3 worked example (or explicitly equivalent reconstructed example) with full equations and interpretation.
- [x] 2.4 Update chapter-level orientation/cross-links so learners can find Session 3 additions in sequence.

## 3. Validation
- [x] 3.1 Run `bundle exec jekyll build --verbose` and fix rendering issues.
- [x] 3.2 Manually verify touched pages render formulas, links, and image paths correctly with `{{ site.baseurl }}` compatibility.
- [x] 3.3 Run `openspec validate update-prior-posterior-session3-coverage --strict`.
