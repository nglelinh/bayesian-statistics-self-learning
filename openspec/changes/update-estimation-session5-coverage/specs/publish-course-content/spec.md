## ADDED Requirements

### Requirement: Session 5 Estimation Coverage Audit
Before revising Bayesian estimation content from Session 5 material, the course workflow SHALL produce a traceable mapping from `materials/buoi 5 - uoc luong.pptx` topics to Chapter 2 lessons, marking each topic as covered, partial, or missing.

#### Scenario: Audit Session 5 estimation topics
- **WHEN** an editor updates the course using Session 5 slides
- **THEN** the editor creates a checklist for MAP, MLE comparison, posterior-mean/MMSE framing, and interval estimation topics
- **AND** each checklist item is mapped to existing lesson sections or flagged for new coverage

### Requirement: Session 5 Point Estimation Completeness
The Vietnamese Chapter 2 Bayesian inference flow SHALL explicitly teach Session 5 point-estimation components: MAP as posterior mode, posterior mean as Bayes estimator under squared-error loss (MMSE framing), and conditions relating MAP to MLE under weak/uniform priors.

#### Scenario: Learner studies Bayesian point estimation in Chapter 2
- **WHEN** a learner reads the Chapter 2 likelihood and posterior lessons
- **THEN** the learner can distinguish MAP, posterior mean (MMSE), and MLE by objective and interpretation
- **AND** the learner can explain how prior choice changes MAP relative to MLE

### Requirement: Session 5 Interval Estimation Continuity
The Vietnamese Chapter 2 flow SHALL include Bayesian interval estimation as a continuation of posterior analysis, with an explicit probability statement for interval interpretation and at least one worked example that links point estimates and interval estimates from the same posterior.

#### Scenario: Learner moves from point to interval estimation
- **WHEN** a learner completes the posterior-estimation section
- **THEN** the learner can read and interpret a Bayesian interval statement as posterior probability over parameter values
- **AND** the learner can compare interval interpretation with point-estimate summaries in one coherent example
