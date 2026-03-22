## MODIFIED Requirements
### Requirement: GitHub Pages Deployment
The repository SHALL build and deploy the Jekyll site through `.github/workflows/jekyll.yml` on pushes to `main` and on manual workflow dispatch, using the GitHub Pages base path during the build job, and any access protection implemented within this repository SHALL remain compatible with static GitHub Pages hosting.

#### Scenario: Deploy from the default branch
- **WHEN** changes are pushed to `main` or the workflow is run manually
- **THEN** GitHub Actions builds the site with `bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"`
- **AND** the workflow uploads the built Pages artifact
- **AND** the deploy job publishes that artifact to GitHub Pages

#### Scenario: Protect the site without changing hosting
- **WHEN** maintainers enable the repository-managed access gate
- **THEN** the protection works entirely from the built static assets
- **AND** the deployment workflow does not require an additional runtime service
