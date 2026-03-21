# Capability: Build Multilingual Site

## Purpose
Describe how the Jekyll site renders bilingual content, preserves older links, and deploys the course to GitHub Pages.

## Requirements

### Requirement: Multilingual Jekyll Configuration
The site SHALL build as a Jekyll project configured for `en` and `vi`, SHALL use `en` as the default language, and SHALL keep site URLs compatible with the configured `baseurl`.

#### Scenario: Build the localized site
- **WHEN** Jekyll reads `_config.yml` during a build
- **THEN** English and Vietnamese are both configured as supported languages
- **AND** English is used as the default language
- **AND** generated links can be prefixed by the configured `baseurl`

### Requirement: Language-Aware Liquid Tags
Custom Liquid tags SHALL provide translated UI labels, active-language CSS state, and a language switch link that targets the equivalent page or post when one exists.

#### Scenario: Render translated navigation
- **WHEN** a localized page uses the custom language tags
- **THEN** the `t` tag returns the label for the current page language when a translation key exists
- **AND** the `lang` tag marks the active language selection
- **AND** the language switch link points to the matching page or post in the other language when one can be resolved

#### Scenario: Fall back when no exact counterpart exists
- **WHEN** the current page has no matching post in the other language
- **THEN** the language switch falls back to the corresponding chapter landing page when possible
- **AND** otherwise it falls back to the other language's chapter 00 landing page

### Requirement: Legacy URL Compatibility
The site SHALL preserve compatibility with legacy content URLs by generating redirect pages from old `/contents/chapterXX/...` paths to localized English destinations, and the custom multilingual post URL tag SHALL resolve old-style post references to matching localized posts when possible.

#### Scenario: Visit a legacy chapter or post URL
- **WHEN** a learner requests an old chapter or post URL without a language segment
- **THEN** the generated redirect page sends the learner to the corresponding English localized URL

#### Scenario: Resolve an old-style post reference
- **WHEN** content uses the `multilang_post_url` tag with an old `contents/chapterXX/...` reference
- **THEN** the tag resolves the matching post in the current language when available
- **AND** otherwise it falls back to another matching post before returning `#post-not-found`

### Requirement: GitHub Pages Deployment
The repository SHALL build and deploy the Jekyll site through `.github/workflows/jekyll.yml` on pushes to `main` and on manual workflow dispatch, using the GitHub Pages base path during the build job.

#### Scenario: Deploy from the default branch
- **WHEN** changes are pushed to `main` or the workflow is run manually
- **THEN** GitHub Actions builds the site with `bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"`
- **AND** the workflow uploads the built Pages artifact
- **AND** the deploy job publishes that artifact to GitHub Pages
