## ADDED Requirements
### Requirement: Path-Scoped Access Gate Configuration
The site SHALL support configuring the access gate for a scoped set of page paths, so maintainers can require password authentication for selected course sections without forcing a site-wide lock.

#### Scenario: Configure gate for Chapter 12 paths
- **WHEN** maintainers configure the gate scope to `contents/vi/chapter12/` routes
- **THEN** only Chapter 12 pages are marked as protected during build output
- **AND** pages outside that scope remain unprotected

### Requirement: Chapter 12 Password Prompt Enforcement
When Chapter 12 path scope is protected, the rendered site SHALL block Chapter 12 page content behind the password gate until valid credentials are entered in the current browser session.

#### Scenario: Open Chapter 12 page directly
- **WHEN** a learner opens `contents/vi/chapter12/index.html` or a Chapter 12 lesson URL directly
- **THEN** the password gate appears before usable chapter content is accessible
- **AND** content is unlocked only after the submitted password matches the configured Chapter 12 credential hash

### Requirement: Scoped Session Unlock Behavior
Successful unlock for Chapter 12 SHALL persist for that browser session and SHALL apply to other Chapter 12 pages in the same session without introducing password prompts for unprotected chapters.

#### Scenario: Navigate across protected and unprotected pages
- **WHEN** a learner unlocks one Chapter 12 page and then navigates to another Chapter 12 lesson in the same session
- **THEN** the learner is not prompted again on Chapter 12 pages during that session
- **AND** navigation to non-Chapter-12 pages does not trigger scoped Chapter 12 gate prompts
