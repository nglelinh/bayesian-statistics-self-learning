## Why
Learners currently encounter normalization constants in scattered places, but the course does not yet provide a clearly staged path for *where* to learn the concept first and *where* to revisit it across common distributions. This creates confusion about why constants such as \(B(a,b)\), \(\Gamma(\alpha)\), \(\sqrt{2\pi\sigma^2}\), or \(y!\) appear and when they matter in Bayesian workflows.

## What Changes
- Add a dedicated content requirement that places normalization-constant knowledge in the right lessons by learning depth:
  - foundation/derivation in `contents/vi/chapter00/_posts/2025-01-02-00_10_gamma_function_intro.md`
  - common-distribution survey and quick-usage framing in `contents/vi/chapter02/_posts/2025-01-02-02_01_probability_distributions.md`
- Require at least one explicit “unnormalized form -> normalized density” walkthrough tied to Bayesian interpretation.
- Require a compact reference of normalization constants for common families (Bernoulli/Binomial, Poisson, Normal, Exponential, Gamma, Beta) with domain/parameterization reminders to reduce misuse.
- Scope this change to Vietnamese lessons only.

## Impact
- Affected specs: `publish-course-content`
- Affected content files (planned):
  - `contents/vi/chapter00/_posts/2025-01-02-00_10_gamma_function_intro.md`
  - `contents/vi/chapter02/_posts/2025-01-02-02_01_probability_distributions.md`
- User-visible outcome: learners can identify where normalization constants come from, where they are used, and why they are required for valid probability models.
