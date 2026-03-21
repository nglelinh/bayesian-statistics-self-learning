# Capability: Deliver Practice Materials

## Purpose
Describe how the repository provides exercises, labs, and generated lab lesson pages that support hands-on Bayesian practice.
## Requirements
### Requirement: Chapter Exercise Notebooks
The repository SHALL provide chapter-aligned exercise notebooks in `exercises/`, and each exercise notebook SHALL follow the `ChapterXX_<Topic>_Exercises.ipynb` naming convention.

#### Scenario: Access chapter exercises
- **WHEN** a learner opens the `exercises/` directory
- **THEN** the available notebooks are organized as chapter-specific Jupyter notebooks
- **AND** each notebook filename identifies its chapter number and topic

### Requirement: Paired Lab Prompts And Solutions
The repository SHALL provide numbered lab prompt notebooks in `labs/` and corresponding solution notebooks in `labs/solutions/`, matched by lab number.

#### Scenario: Review a lab and its solution
- **WHEN** a numbered lab is published
- **THEN** the prompt notebook exists in `labs/`
- **AND** the matching solution notebook exists in `labs/solutions/`
- **AND** both files use the same lab number

### Requirement: Generate Chapter 12 Lab Pages
Running `python scripts/generate_lab_chapter.py` SHALL match numbered lab prompts with numbered solutions, clear stale generated outputs, export standalone HTML notebook renders to `public/generated/labs/`, and regenerate Vietnamese Chapter 12 lesson pages that embed both the prompt and solution notebooks.

#### Scenario: Generate lab-backed lesson pages
- **WHEN** every discovered lab number has both a prompt notebook and a solution notebook
- **THEN** the script writes `lab-XX.html` and `lab-XX-solution.html` files under `public/generated/labs/`
- **AND** it regenerates `contents/vi/chapter12/_posts/` markdown pages for each lab number
- **AND** each generated lesson page links to and embeds both the prompt and solution notebook exports

#### Scenario: Detect incomplete lab pairs
- **WHEN** a prompt notebook or solution notebook is missing for a discovered lab number
- **THEN** the script exits with a mismatch error
- **AND** it does not silently generate a partial Chapter 12 set

### Requirement: Practice References Align With Active Curriculum
Practice notebooks and tracked exported lab HTML SHALL not reference retired chapter URLs from the active course.

#### Scenario: Update practice references after a chapter retirement
- **WHEN** a chapter such as Chapter 11 is retired
- **THEN** lab notebooks and tracked generated exports no longer link learners to that retired chapter
- **AND** any replacement references point to active lessons or use neutral wording without a retired URL

