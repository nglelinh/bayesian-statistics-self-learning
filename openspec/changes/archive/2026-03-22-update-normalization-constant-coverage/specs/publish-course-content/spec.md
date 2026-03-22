## ADDED Requirements
### Requirement: Normalization-Constant Learning Path for Common Distributions
The course content workflow SHALL place normalization-constant knowledge in a staged learning path: conceptual/derivation grounding in foundational math lessons and practical distribution-level reference in introductory distribution lessons, so learners can connect unnormalized expressions to valid probability models.

#### Scenario: Learner studies foundational derivation context
- **WHEN** a learner reads the foundational Gamma/Beta lesson in `contents/vi/chapter00/_posts/2025-01-02-00_10_gamma_function_intro.md`
- **THEN** the lesson explains why normalization constants are required for densities/posteriors
- **AND** the learner can find at least one explicit walkthrough from an unnormalized expression to a normalized distribution form

#### Scenario: Learner reviews common distribution constants
- **WHEN** a learner reads the probability-distributions overview lesson in `contents/vi/chapter02/_posts/2025-01-02-02_01_probability_distributions.md`
- **THEN** the learner can find a compact reference covering normalization constants for Bernoulli/Binomial, Poisson, Normal, Exponential, Gamma, and Beta
- **AND** each listed family includes domain and parameterization cues needed to avoid common misuse

#### Scenario: Maintainer applies this update in Vietnamese scope
- **WHEN** maintainers implement this normalization-constant coverage change
- **THEN** the required additions are applied to the Vietnamese target lessons under `contents/vi/`
- **AND** no cross-language parity requirement is introduced by this specific change
