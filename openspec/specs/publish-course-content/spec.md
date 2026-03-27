# Capability: Publish Course Content

## Purpose
Describe how the course stores, structures, and writes lesson content for the bilingual Bayesian statistics learning experience.
## Requirements
### Requirement: Language-Scoped Chapter Content
The repository SHALL organize active lesson content by language under `contents/en/` and `contents/vi/`, and each active chapter directory SHALL provide a chapter landing page plus a `_posts/` collection for lesson pages. Retired chapters SHALL be removed from the active course tree and SHALL not remain linked from active lesson pages.

#### Scenario: Render a chapter collection
- **WHEN** Jekyll reads an active chapter directory such as `contents/vi/chapter04/`
- **THEN** the directory includes an `index.html` landing page
- **AND** lesson pages for that chapter live under the same directory's `_posts/` folder

#### Scenario: Retire a chapter from the active curriculum
- **WHEN** a chapter such as Chapter 9 is retired
- **THEN** its chapter directory and lesson posts are removed from the active published course tree
- **AND** active lesson pages do not continue linking learners into that retired chapter

### Requirement: Lesson Metadata Contract
Each lesson post SHALL declare Jekyll front matter for `layout`, `title`, `chapter`, `order`, `owner`, `lang`, `categories`, and `lesson_type`.

#### Scenario: Render a lesson post
- **WHEN** a lesson post is added or updated under `contents/<lang>/chapterXX/_posts/`
- **THEN** the post declares all required metadata fields before the lesson body
- **AND** `layout` is set to `post`
- **AND** `lang` and `chapter` identify the lesson's language and chapter

### Requirement: Bayesian Teaching Style
Lesson bodies SHALL teach Bayesian statistics in a motivation-first style that frames models as data-generating stories, emphasizes uncertainty and interpretation, uses `$$...$$` delimiters for math, and keeps embedded asset links compatible with `{{ site.baseurl }}`.

#### Scenario: Author a lesson page
- **WHEN** an author writes or revises a lesson
- **THEN** the lesson explains the concept and its interpretation before implementation-heavy detail
- **AND** mathematical expressions use `$$...$$`
- **AND** embedded image or asset links remain compatible with `{{ site.baseurl }}`

### Requirement: Chapter Visual Asset Organization
Chapter-specific illustrations SHALL live under `img/chapter_img/<chapter>/`, and reproducible figure generators SHALL be stored alongside those assets using `generate_<topic>.py` naming.

#### Scenario: Regenerate a chapter figure
- **WHEN** a chapter includes reproducible visualization scripts
- **THEN** the generated images and their generator scripts are colocated under the matching `img/chapter_img/<chapter>/` directory
- **AND** each generator script follows the `generate_<topic>.py` naming convention

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

### Requirement: Session 3 Prior-Posterior Coverage Audit
Before revising lessons from Session 3 material, the content workflow SHALL produce a traceable mapping between `materials/buoi 3 - tien nghiem, hau nghiem.pptx` topics and current Chapter 2 lesson pages, marking each topic as covered, partial, or missing.

#### Scenario: Audit Session 3 image-heavy source slides
- **WHEN** an editor reviews Session 3 source slides with limited extractable text
- **THEN** the editor creates a topic checklist from slide titles, visible formulas/diagrams, and lesson context
- **AND** each checklist item is mapped to an existing Chapter 2 lesson or flagged as missing

### Requirement: Session 3 Prior-Likelihood-Posterior Continuity
The Vietnamese Chapter 2 course flow SHALL explicitly present prior, likelihood, and posterior as a connected Bayesian update pipeline and SHALL include at least one end-to-end worked example that demonstrates the full update from prior assumptions to posterior interpretation.

#### Scenario: Learner follows Chapter 2 core Bayes update lessons
- **WHEN** a learner studies the Chapter 2 sequence for likelihood, prior, and posterior
- **THEN** the learner can follow one continuous update narrative across the three concepts
- **AND** the learner can locate at least one complete worked example that starts with a prior, incorporates observed data through likelihood, and ends with posterior interpretation

### Requirement: Session 3 Example Fidelity From Image Slides
When Session 3 examples are embedded in image-heavy slides, the Vietnamese Chapter 2 update SHALL preserve at least one recovered worked example (OCR-assisted or manually reconstructed) with explicit equations and interpretation.

#### Scenario: Learner checks worked examples from Session 3-aligned content
- **WHEN** a learner opens the revised Chapter 2 lessons
- **THEN** the learner can find at least one worked example traceable to Session 3 slide material
- **AND** the example includes enough numeric/algebraic detail to reproduce the update result

### Requirement: Session 4 Conjugacy Coverage Audit
Before revising conjugacy content from Session 4 material, the course workflow SHALL produce a traceable mapping from `materials/buoi 4 - lien hop.pptx` topics to published Chapter 2 lessons, with each topic marked as covered, partial, or missing.

#### Scenario: Audit Session 4 source topics
- **WHEN** an editor updates the course from Session 4 slides
- **THEN** the editor creates a topic checklist from slide text and visual cues
- **AND** each topic is mapped to existing Chapter 2 content or flagged as missing

### Requirement: Session 4 Conjugacy Prerequisite Completeness
The Vietnamese Chapter 2 lesson flow SHALL include Session 4 prerequisite context needed to understand conjugacy, including the Gamma-function role in Beta/Gamma distributions, recap of Beta/Gamma/Normal parameterization domains, and concise approximation caveats used in Session 4 teaching.

#### Scenario: Learner studies conjugacy prerequisites
- **WHEN** a learner reads Chapter 2 lessons leading into conjugate priors
- **THEN** the learner can find prerequisite context for Gamma/Beta/Normal families and parameter domains
- **AND** the learner can find concise guidance on when Normal approximation statements are appropriate or limited

### Requirement: Session 4 Conjugate Family Continuity
The Vietnamese Chapter 2 conjugacy lesson SHALL explicitly connect Session 4 core families (Beta-Binomial, Gamma-Poisson, Normal-Normal) with Bayesian estimation interpretation so learners can move from conjugate formulas to practical posterior summaries.

#### Scenario: Learner transitions from conjugate formulas to estimation
- **WHEN** a learner finishes the conjugacy lesson
- **THEN** the learner can identify the three core Session 4 conjugate families and their data stories
- **AND** the learner can connect posterior updates to Bayesian estimation interpretation in at least one worked example

### Requirement: Session 4 Worked Example Fidelity
The Vietnamese Chapter 2 conjugacy update SHALL preserve Session 4 worked-example intent from image-heavy slides by including at least one Gamma-Poisson update example and one Normal-Normal Bayes-estimation example with explicit posterior-summary computation.

#### Scenario: Learner validates conjugacy examples against Session 4 content
- **WHEN** a learner reviews worked examples in the revised conjugacy lessons
- **THEN** the learner can find a Gamma-Poisson example with prior-to-posterior parameter update
- **AND** the learner can find a Normal-Normal example that reports Bayes estimate and posterior uncertainty/risk summary

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

### Requirement: Session 5 Worked Example Fidelity
The Vietnamese Chapter 2 estimation update SHALL include representative Session 5 worked examples (OCR-recovered when image-based), covering MAP derivation, ML-vs-MAP comparison, MMSE/posterior-mean derivation, and one Bayesian interval computation.

#### Scenario: Learner reviews Session 5 example set in revised lessons
- **WHEN** a learner studies estimation examples in the Chapter 2 flow
- **THEN** the learner can find at least one explicit MAP derivation and one MMSE/posterior-mean derivation
- **AND** the learner can find at least one explicit ML-vs-MAP comparison
- **AND** the learner can find at least one worked Bayesian interval computation

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

### Requirement: Session 7 Worked Example Fidelity
The Vietnamese Chapter 4 update SHALL include at least one Session 7-traceable worked example (OCR-recovered when image-based) that shows prior-to-posterior updating for regression parameters with explicit posterior-summary values.

#### Scenario: Learner checks regression update example in revised Chapter 4
- **WHEN** a learner reviews worked examples in Session 7-aligned lessons
- **THEN** the learner can find one derivation-oriented example with concrete prior assumptions and resulting posterior summaries for regression parameters
- **AND** the learner can relate the computed posterior summaries to slope/intercept interpretation

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

### Requirement: Session 8 Worked Example Fidelity
The Vietnamese Session 8 classification update SHALL include worked examples traceable to Session 8 slides, including a prior-shift classification intuition example and a two-class/three-action decision example with reject/defer option and explicit risk comparison.

#### Scenario: Learner reproduces Session 8 decision examples
- **WHEN** a learner reads the revised Session 8-aligned classification lessons
- **THEN** the learner can find an example showing how class priors change posterior classification preference
- **AND** the learner can find an example where action choice is based on comparing expected risks across at least three actions (including reject/defer)

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

### Requirement: Chapter 00 Scientific Writing Consistency (Vietnamese)
The Vietnamese Chapter 00 lessons SHALL be edited to maintain a consistent scientific lecture style anchored to `contents/vi/chapter00/_posts/2025-01-02-00_01_probability_basics.md`, with motivation-first narrative flow, interpretation-focused explanations, and mathematically explicit transitions aligned with `.cursor/rules` guidance.

#### Scenario: Learner reads two different Chapter 00 lessons
- **WHEN** a learner studies any two revised lessons in `contents/vi/chapter00/_posts/`
- **THEN** both lessons present concepts using coherent academic prose rather than disconnected bullet-style fragments
- **AND** each lesson motivates why a concept is needed before introducing formalism

#### Scenario: Learner checks mathematical exposition in revised Chapter 00 lessons
- **WHEN** a learner encounters formulas in a revised Chapter 00 lesson
- **THEN** mathematical expressions use `$$...$$` delimiters and are accompanied by interpretation in context
- **AND** lessons include at least one explicit transition from concept intuition to formal statement or derivation where relevant

#### Scenario: Editor applies Chapter 00 writing improvements
- **WHEN** an editor updates Chapter 00 lesson prose for this change
- **THEN** updates stay within `contents/vi/chapter00/_posts/` and preserve existing chapter sequence and lesson linkage
- **AND** front matter and `{{ site.baseurl }}`-compatible links remain valid

