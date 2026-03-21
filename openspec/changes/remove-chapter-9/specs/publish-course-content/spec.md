## MODIFIED Requirements
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
