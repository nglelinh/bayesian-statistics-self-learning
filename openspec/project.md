# Project Context

## Purpose
This repository powers a bilingual (Vietnamese/English) Bayesian Statistics self-learning course and website. It combines lecture notes, hands-on exercises, labs, and generated visualizations to teach Bayesian reasoning, probabilistic modeling, and model criticism with an emphasis on practical implementation.

Primary goals:
- Deliver a complete Bayesian learning path from prerequisites to advanced workflows.
- Keep lessons motivation-first and interpretation-focused, not formula-only.
- Provide reproducible examples using modern Python Bayesian tooling.
- Publish the course as a Jekyll site via GitHub Pages.

## Tech Stack
- Jekyll (Ruby) for static site generation and publishing
- Markdown for lesson content and documentation
- JavaScript for frontend behavior (search, multilingual UX, interactions)
- Python + Jupyter notebooks for exercises, labs, and figure generation
- PyMC + ArviZ + NumPy/SciPy/Matplotlib/Seaborn/Pandas for Bayesian workflows
- GitHub Actions for CI build/deploy to GitHub Pages

## Project Conventions

### Code Style
- Keep changes minimal, scoped to the task, and avoid unrelated refactors.
- Match existing local style in touched files (no enforced global formatter).
- Python imports: standard library -> third-party -> local.
- Python naming: `snake_case` for functions/variables, `UPPER_CASE` for constants.
- JavaScript naming: `camelCase` for variables/functions; preserve existing ES5/ES6 style per file.
- Lesson file naming: `YYYY-MM-DD-topic.md`.
- Figure script naming: `generate_<topic>.py`.
- Exercise notebooks: `ChapterXX_<Topic>_Exercises.ipynb`.
- Use `$$...$$` for math formulas in markdown.

### Architecture Patterns
- Content-first architecture:
  - Lessons live under `contents/vi/` and `contents/en/`.
  - Practice assets live in `exercises/` and `labs/`.
  - Generated figures live under `img/chapter_img/<chapter>/` with generator scripts.
- Presentation layer:
  - Jekyll layouts/includes in `_layouts/` and `_includes/`.
  - Custom Ruby plugins in `_plugins/`.
  - Static assets in `public/`.
- Teaching pattern:
  - Introduce Bayesian models as generative stories first.
  - Emphasize uncertainty, interpretation, and model checking.
  - For practical modeling work, default to Python + PyMC + ArviZ.

### Testing Strategy
- No centralized unit/integration test suite; validation is task-targeted.
- Required baseline check for most changes: `bundle exec jekyll build --verbose`.
- For content/rendering changes, verify pages render correctly (math, image paths, internal links).
- For notebook/script changes, run the changed notebook/script at least once (e.g., via `jupyter nbconvert --execute` or direct Python script execution).
- CI-like local verification when needed: `bundle exec jekyll build --baseurl "/bayesian-statistics-self-learning"`.

### Git Workflow
- Use feature branches and open pull requests; avoid direct pushes to protected/default branch.
- Keep commits focused and avoid formatting churn unrelated to the task.
- Do not rewrite history or force push unless explicitly required.
- Do not push from automation/agents unless explicitly requested by the user/maintainer.
- Preserve existing unrelated work in a dirty worktree.

## Domain Context
- Domain: Bayesian statistics education.
- Core pedagogical stance:
  - Teach Bayesian reasoning as reasoning about data-generating processes.
  - Contrast Bayesian methods with NHST/p-value workflows where relevant.
  - Prioritize posterior interpretation, uncertainty quantification, diagnostics, and model criticism.
- Typical topics include priors/posteriors, conjugacy, grid approximation, MCMC (MH/HMC/NUTS), regression/GLMs, confounding/DAGs, and posterior predictive checks.
- Repository is bilingual; when editing lesson content, keep EN/VI parity where applicable.

## Important Constraints
- Preserve backward compatibility in site structure and links unless change is explicitly requested.
- Keep `{{ site.baseurl }}`-compatible paths for assets/links.
- Maintain front matter keys expected by Jekyll pages/posts.
- Avoid introducing new frameworks/tooling unless clearly needed and requested.
- Ensure reproducibility in simulations/visualizations (fixed random seeds where appropriate).
- Large generated artifacts (images/notebooks) should be updated only when intentionally regenerated.

## External Dependencies
- Ruby/Bundler + Jekyll for static site build.
- Python scientific stack: `numpy`, `scipy`, `matplotlib`, `seaborn`, `pandas`, `jupyter`.
- Bayesian stack: `pymc`, `arviz`.
- GitHub Pages + GitHub Actions workflow (`.github/workflows/jekyll.yml`) for deployment.
