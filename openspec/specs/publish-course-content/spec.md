# Capability: Publish Course Content

## Purpose
Describe how the course stores, structures, and writes lesson content for the bilingual Bayesian statistics learning experience.

## Requirements

### Requirement: Language-Scoped Chapter Content
The repository SHALL organize lesson content by language under `contents/en/` and `contents/vi/`, and each chapter directory SHALL provide a chapter landing page plus a `_posts/` collection for lesson pages.

#### Scenario: Render a chapter collection
- **WHEN** Jekyll reads a chapter directory such as `contents/vi/chapter04/`
- **THEN** the directory includes an `index.html` landing page
- **AND** lesson pages for that chapter live under the same directory's `_posts/` folder

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
