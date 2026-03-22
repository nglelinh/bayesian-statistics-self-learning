## 1. Scope and placement
- [x] 1.1 Confirm target lesson placement and narrative split: derivation-heavy content in Chapter 00 lesson `00_10`, distribution-level quick reference in Chapter 02 lesson `02_01`.
- [x] 1.2 Draft a minimal outline for each lesson section so coverage is additive and avoids duplicating the same explanation verbatim.

## 2. Vietnamese lesson updates
- [x] 2.1 Update `contents/vi/chapter00/_posts/2025-01-02-00_10_gamma_function_intro.md` with a concise explanation of why normalization constants are needed, anchored by at least one unnormalized-to-normalized derivation.
- [x] 2.2 Update `contents/vi/chapter02/_posts/2025-01-02-02_01_probability_distributions.md` with a compact normalization-constant reference for common distributions (Bernoulli/Binomial, Poisson, Normal, Exponential, Gamma, Beta) plus domain/parameterization cues.

## 3. Validation
- [x] 3.1 Verify math formatting, section flow, and `{{ site.baseurl }}` asset/link compatibility on all touched pages.
- [x] 3.2 Run `bundle exec jekyll build --verbose` and resolve any rendering/link issues.
