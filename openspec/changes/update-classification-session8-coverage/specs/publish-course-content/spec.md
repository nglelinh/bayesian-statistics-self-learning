## ADDED Requirements

### Requirement: Session 8 Classification Coverage Audit
Before revising classification content from Session 8 material, the course workflow SHALL produce a traceable mapping from `materials/buoi 8 - phan lop.pptx` topics to published lessons, marking each topic as covered, partial, or missing.

#### Scenario: Audit Session 8 classification topics
- **WHEN** an editor updates the course using Session 8 slides
- **THEN** the editor creates a checklist covering posterior class probabilities, risk-based decisions, discriminant functions, and Gaussian boundary cases
- **AND** each checklist item is mapped to an existing lesson section or flagged as missing

### Requirement: Session 8 Bayesian Classification Decision Completeness
The Vietnamese classification lesson flow SHALL explicitly teach Bayesian pattern-classification decisions using posterior class probabilities and minimum-expected-risk actions under a loss matrix, including support for a defer/reject action when applicable.

#### Scenario: Learner performs Bayesian class assignment
- **WHEN** a learner studies classification decision rules in the course
- **THEN** the learner can compute or interpret class posteriors from priors and class-conditional likelihoods
- **AND** the learner can choose an action by minimizing expected posterior risk, including a reject option when its loss is lower

### Requirement: Session 8 Discriminant and Gaussian Boundary Continuity
The Vietnamese classification flow SHALL connect posterior decision rules to discriminant-function formulations (including monotone-transform equivalents) and SHALL explain Gaussian class-conditional boundary simplifications in at least one worked example.

#### Scenario: Learner transitions from posterior formulas to decision boundaries
- **WHEN** a learner follows the Session 8-aligned classification section
- **THEN** the learner can relate posterior-based rules to discriminant comparisons such as log-discriminants
- **AND** the learner can distinguish linear-boundary and quadratic-boundary cases under Gaussian class-conditional assumptions
