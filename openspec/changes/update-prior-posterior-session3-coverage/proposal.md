## Why
Session 3 source material (`materials/buoi 3 - tien nghiem, hau nghiem.pptx`) covers the prior-likelihood-posterior core update story, but this deck is image-heavy and not directly traceable to a clear topic checklist in the published course pages. A focused coverage audit is needed to confirm whether any Session 3 teaching points are missing and to add them explicitly to the course flow.

## What Changes
- Add a Session 3 coverage-audit workflow that maps slide-level prior/posterior content to current Vietnamese Chapter 2 lessons.
- Add missing Session 3 concepts (if any) into Chapter 2 with motivation-first explanations and consistent Bayes notation.
- Ensure the Chapter 2 flow clearly connects `likelihood -> prior -> posterior` as a single update narrative, not only separate lesson fragments.
- Add or refine worked examples (especially one end-to-end update example) when the audit finds missing continuity from Session 3.
- Add OCR-backed example fidelity checks for image-heavy Session 3 slides, and preserve at least one recovered worked example in course content when relevant to Bayes prerequisites and update flow.

## Impact
- Affected specs: `publish-course-content`
- Affected content (expected):
  - `contents/vi/chapter02/_posts/2025-01-02-02_02_likelihood.md`
  - `contents/vi/chapter02/_posts/2025-01-02-02_03_prior.md`
  - `contents/vi/chapter02/_posts/2025-01-02-02_04_posterior.md`
  - `contents/vi/chapter02/index.html` (if chapter-level orientation cues are needed)
- Potential affected assets: `img/chapter_img/chapter02/` (only if new figures are needed)
