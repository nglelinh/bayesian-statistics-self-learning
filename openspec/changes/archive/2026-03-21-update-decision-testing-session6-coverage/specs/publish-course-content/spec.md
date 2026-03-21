## ADDED Requirements

### Requirement: Session 6 Decision-Testing Coverage Audit
Before revising content from Session 6 material, the course workflow SHALL produce a traceable mapping from `materials/buoi 6 - phoi hop.pptx` topics to published lessons, marking each topic as covered, partial, or missing.

#### Scenario: Audit Session 6 teaching topics
- **WHEN** an editor updates course content based on Session 6 slides
- **THEN** the editor creates a checklist for loss-based decision, posterior-risk evaluation, Bayes testing, Bayes factor, and mixture prior/posterior topics
- **AND** each checklist item is mapped to an existing lesson section or flagged as missing

### Requirement: Session 6 Bayesian Testing Completeness
The Vietnamese Bayesian lesson flow SHALL explicitly cover Bayesian hypothesis-testing interpretation for one-sided and two-sided decision contexts, and SHALL explain Bayes factor as an evidence ratio between competing hypotheses/models.

#### Scenario: Learner studies Bayesian testing from Session 6 content
- **WHEN** a learner reads the testing-related lesson sections
- **THEN** the learner can distinguish one-sided and two-sided Bayesian decision contexts
- **AND** the learner can interpret a Bayes factor as relative evidence for competing hypotheses/models

### Requirement: Session 6 Decision and Mixture Continuity
The Vietnamese course flow SHALL connect posterior inference to decision rules through loss/posterior-risk reasoning and SHALL include mixture-prior to mixture-posterior weight-updating intuition in at least one worked example.

#### Scenario: Learner moves from posterior to decision
- **WHEN** a learner follows Session 6-aligned lessons from posterior summaries to action choice
- **THEN** the learner can compute or interpret decision preference via expected posterior loss
- **AND** the learner can explain how data updates mixture weights from prior to posterior in a practical example

### Requirement: Session 6 Worked Example Fidelity
The Vietnamese Session 6-aligned update SHALL include representative worked examples traceable to Session 6 slides, including a binary MAP detection decision, an asymmetric-cost alarm/action decision, and at least one mixture-prior posterior-weight update example.

#### Scenario: Learner validates decision/testing examples in revised content
- **WHEN** a learner reviews worked examples in Session 6-aligned lessons
- **THEN** the learner can find one example where MAP selects between two hypotheses under noisy observations
- **AND** the learner can find one example where expected-loss asymmetry changes the preferred action
- **AND** the learner can find one example where mixture-prior weights are updated after data
