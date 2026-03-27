## ADDED Requirements
### Requirement: Chapter 07 Applied ML Workflow Coverage (Vietnamese)
The Vietnamese Chapter 07 lesson flow SHALL teach regularization, bias-variance tradeoff, and feature selection as parts of an applied machine learning workflow, including problem framing, preprocessing constraints, model training choices, and interpretation of out-of-sample behavior.

#### Scenario: Learner studies Chapter 07 as an ML workflow
- **WHEN** a learner reads the revised lessons in `contents/vi/chapter07/_posts/`
- **THEN** each core topic (regularization, bias-variance, feature selection) is connected to concrete modeling decisions in a practical ML pipeline
- **AND** the learner can identify how Bayesian priors influence those decisions under limited or high-dimensional data

### Requirement: Chapter 07 Validation and Tuning Decision Completeness (Vietnamese)
The Vietnamese Chapter 07 update SHALL include practical guidance for selecting model complexity and regularization strength using validation-oriented evidence, including train/validation/test roles, metric interpretation, and at least one uncertainty-aware evaluation method.

#### Scenario: Learner chooses regularization strength in practice
- **WHEN** a learner follows the revised Chapter 07 model-selection guidance
- **THEN** the learner can explain why train-only fit quality is insufficient for model choice
- **AND** the learner can use validation evidence (for example cross-validation or holdout performance) together with Bayesian checks (for example posterior predictive checks) to justify a regularization decision

### Requirement: Chapter 07 End-to-End Applied Example Fidelity (Vietnamese)
The Vietnamese Chapter 07 update SHALL include at least one reproducible end-to-end applied example that goes from data setup to model comparison and final interpretation, with explicit checkpoints for preprocessing assumptions, model fit quality, and feature-importance uncertainty.

#### Scenario: Learner reproduces the applied Chapter 07 example
- **WHEN** a learner follows the Chapter 07 applied example steps
- **THEN** the learner can reproduce the workflow from prepared data to comparative model outputs
- **AND** the learner can report both predictive performance and uncertainty-aware interpretation for selected features or coefficients
