## 1. Analysis
- [ ] 1.1 Build a Session 3 topic checklist from `materials/buoi 3 - tien nghiem, hau nghiem.pptx`, including image-based content cues where text extraction is limited.
- [ ] 1.2 Map Session 3 topics to `contents/vi/chapter02/_posts/2025-01-02-02_02_likelihood.md`, `contents/vi/chapter02/_posts/2025-01-02-02_03_prior.md`, and `contents/vi/chapter02/_posts/2025-01-02-02_04_posterior.md`.
- [ ] 1.3 Document concrete missing or weakly covered topics before editing lessons.

## 2. Content Updates
- [ ] 2.1 Update Chapter 2 lessons to add any missing Session 3 concepts with motivation-first explanations and `$$...$$` math formatting.
- [ ] 2.2 Ensure at least one complete prior-likelihood-posterior worked example is explicitly connected across the chapter flow.
- [ ] 2.3 Update chapter-level orientation/cross-links so learners can find Session 3 additions in sequence.

## 3. Validation
- [ ] 3.1 Run `bundle exec jekyll build --verbose` and fix rendering issues.
- [ ] 3.2 Manually verify touched pages render formulas, links, and image paths correctly with `{{ site.baseurl }}` compatibility.
- [ ] 3.3 Run `openspec validate update-prior-posterior-session3-coverage --strict`.
