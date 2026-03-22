# Capability: Protect Site Access

## ADDED Requirements
### Requirement: Configurable Static Access Gate
The site SHALL support an optional static access gate controlled from `_config.yml`, and when the gate is enabled the rendered site SHALL require configured credentials before the main UI is usable.

#### Scenario: Gate enabled for the site
- **WHEN** the site build reads an enabled access-gate configuration
- **THEN** the shared page layout renders the access-gate bootstrap data and login UI
- **AND** the page content remains visually blocked until the visitor is authenticated

#### Scenario: Gate disabled for the site
- **WHEN** the site build reads a disabled or missing access-gate configuration
- **THEN** the shared page layout does not block page usage with an access gate

### Requirement: Build-Time Credential Sanitization
The site SHALL derive a sanitized access-gate payload during the Jekyll build so that rendered pages do not expose the configured plaintext password.

#### Scenario: Build pages with configured credentials
- **WHEN** `_config.yml` contains a fixed password for the access gate
- **THEN** the build derives a non-plaintext credential payload for the browser
- **AND** the generated pages do not embed the plaintext password value

### Requirement: Session-Scoped Browser Unlock
The access gate SHALL remember successful authentication for the current browser session so learners do not have to log in again on every page navigation within the same session.

#### Scenario: Open another page after authenticating
- **WHEN** a learner authenticates successfully and then navigates to another course page in the same browser session
- **THEN** the site recognizes the existing authenticated state
- **AND** the learner is not prompted again until the session is cleared or expires
