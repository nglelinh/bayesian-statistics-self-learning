## ADDED Requirements

### Requirement: Session Material Coverage Audit
Before revising lesson content from instructor slide materials, the course content workflow SHALL create a session-to-lesson coverage map that marks each source topic as covered, partially covered, or missing in published lessons.

#### Scenario: Audit Session 2 Bayesian introduction material
- **WHEN** an editor updates the course based on `materials/buoi 2 - gioi thieu ve Bayesian.pptx`
- **THEN** the editor produces a topic mapping against existing Chapter 1/2 lesson pages
- **AND** any missing or partial topics are explicitly listed before drafting lesson edits

### Requirement: Session 2 Bayesian Introduction Completeness
The Vietnamese introductory Bayesian lesson flow SHALL include Session 2 core concepts: (1) a concise conditional-probability and total-probability refresher for Bayes theorem, (2) diagnostic-test interpretation using confusion-matrix terms (including sensitivity, specificity, and false positives), and (3) course logistics context on references and grading split in the course introduction page.

#### Scenario: Learner studies Chapter 1 introduction sequence
- **WHEN** a learner reads the Chapter 1 introduction lessons in `contents/vi/chapter01/_posts/`
- **THEN** the learner can find Bayes-theorem prerequisites and diagnostic confusion-matrix interpretation without leaving the chapter
- **AND** the course introduction page states the main Session 2 references and grading composition

### Requirement: Session 2 Worked Example Fidelity
The Vietnamese Chapter 1 Bayes-theorem lesson SHALL include Session 2 worked examples with explicit numeric updates: VD1 rare-disease test posterior calculation, VD2 Holmes/Watson icy-road conditional update, and VD3 two-test sequential posterior update.

#### Scenario: Learner follows Session 2 examples in Chapter 1
- **WHEN** a learner studies worked examples in the Bayes-theorem lesson
- **THEN** the learner can see at least one full rare-disease posterior computation using total probability in the denominator
- **AND** the learner can see one conditional-update example equivalent to the Holmes/Watson case
- **AND** the learner can see one sequential two-test example where posterior is updated more than once
