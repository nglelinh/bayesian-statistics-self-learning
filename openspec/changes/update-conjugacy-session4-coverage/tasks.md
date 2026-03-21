## 1. Analysis
- [ ] 1.1 Build a Session 4 topic checklist from `materials/buoi 4 - lien hop.pptx`, including image/diagram-based topics where text extraction is incomplete.
- [ ] 1.2 Map Session 4 topics to Chapter 2 lessons, especially `2025-01-02-02_01_probability_distributions.md` and `2025-01-02-02_05_conjugate_priors.md`.
- [ ] 1.3 Document which Session 4 topics are fully covered, partially covered, or missing before edits.

## 2. Content Updates
- [ ] 2.1 Add any missing Session 4 prerequisite recap (Gamma function and distribution-parameterization context) to the most appropriate Chapter 2 lesson sections.
- [ ] 2.2 Strengthen conjugacy lesson coverage for Session 4 essentials: formal conjugacy definition, core conjugate families, and Bayesian-estimation interpretation where needed.
- [ ] 2.3 Add concise approximation-caveat guidance from Session 4 where currently missing (Normal approximation conditions and limitations).
- [ ] 2.4 Update chapter-level cross-links/orientation if needed so additions are easy to discover in sequence.

## 3. Validation
- [ ] 3.1 Run `bundle exec jekyll build --verbose` and resolve any rendering issues.
- [ ] 3.2 Verify touched pages render formulas, internal links, and image paths correctly with `{{ site.baseurl }}` compatibility.
- [ ] 3.3 Run `openspec validate update-conjugacy-session4-coverage --strict`.
