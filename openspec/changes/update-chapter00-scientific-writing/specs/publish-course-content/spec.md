## ADDED Requirements
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
