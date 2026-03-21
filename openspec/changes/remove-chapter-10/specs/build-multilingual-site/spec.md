## MODIFIED Requirements
### Requirement: Active Curriculum Navigation
The site SHALL expose only active curriculum chapters in global navigation and chapter-to-chapter calls to action, and active pages SHALL not surface links into retired chapter URLs.

#### Scenario: Render sidebar navigation after a chapter retirement
- **WHEN** the site builds navigation after Chapter 10 has been retired
- **THEN** the sidebar chapter list excludes Chapter 10
- **AND** the remaining active chapters continue to render in order

#### Scenario: Render chapter-level next-step cues after a chapter retirement
- **WHEN** a learner finishes the final active lecture chapter after Chapter 10 retirement
- **THEN** the page does not point to a retired Chapter 10 URL
- **AND** any next-step cue points to the remaining active learning path or ends the lecture sequence cleanly
