## ADDED Requirements

### Requirement: Session 7 Regression Coverage Audit
Before revising regression lessons from Session 7 material, the course workflow SHALL produce a traceable mapping from `materials/buoi 7 - hoi quy.pptx` topics to published Chapter 4 lessons, marking each topic as covered, partial, or missing.

#### Scenario: Audit Session 7 regression topics
- **WHEN** an editor updates the course using Session 7 slides
- **THEN** the editor creates a checklist covering assumptions, joint distributions, interval estimation, and multivariate extension topics
- **AND** each topic is mapped to an existing Chapter 4 section or flagged for new coverage

### Requirement: Session 7 Regression Foundations Completeness
The Vietnamese Chapter 4 regression flow SHALL explicitly include Session 7 foundations: model assumptions for linear regression errors, joint likelihood/prior/posterior framing for regression parameters, and Bayesian slope-interval interpretation in both known-variance and unknown-variance contexts.

#### Scenario: Learner studies regression foundations
- **WHEN** a learner reads the Chapter 4 regression foundation lessons
- **THEN** the learner can explain the role of core linear-regression assumptions before posterior interpretation
- **AND** the learner can identify how joint likelihood with priors yields posterior inference for regression parameters
- **AND** the learner can interpret slope intervals with clear known-vs-unknown variance context

### Requirement: Session 7 Multivariate Transition
The Vietnamese Chapter 4 flow SHALL provide a concise transition from single-predictor linear regression to multivariate regression using matrix notation and interpretation of parameter vectors.

#### Scenario: Learner moves from simple to multivariate regression
- **WHEN** a learner completes single-predictor regression lessons
- **THEN** the learner can recognize the matrix-form model structure for multivariate regression
- **AND** the learner can relate scalar intercept/slope notation to vector-matrix parameterization
