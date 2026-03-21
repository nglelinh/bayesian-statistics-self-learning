<!-- OPENSPEC:START -->
# OpenSpec Instructions
These instructions are for AI assistants working in this project.
Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding
Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines
Keep this managed block so 'openspec update' can refresh the instructions.
<!-- OPENSPEC:END -->

# AGENTS.md
Practical guide for coding agents in this repository.

## Project Snapshot
- Stack: Jekyll (Ruby), Markdown, JavaScript, Python notebooks/scripts.
- Main content: `contents/vi/` and `contents/en/` (bilingual lessons).
- Practice assets: `exercises/` and `labs/` notebooks.
- Figures: `img/chapter_img/**/generate_*.py`.
- Plugins: `_plugins/*.rb`.
- Deployment: `.github/workflows/jekyll.yml` (GitHub Pages).

## Build, Lint, and Test Commands

### Setup
```bash
bundle install
pip install numpy matplotlib scipy seaborn pymc arviz pandas jupyter
pip install -r src/requirements.txt
```

### Build and run
```bash
# Local server
bundle exec jekyll serve

# Build checks
bundle exec jekyll build --verbose
bundle exec jekyll doctor

# Docker option
docker-compose up
```

### Lint/format status
- No dedicated lint configs found (`ruff`, `pytest`, `eslint`, `rubocop`, `make`).
- Quality gate is convention-based: clean diffs + successful build + targeted execution checks.

### Test status
- No centralized unit/integration test suite exists.
- Use single-file/single-task execution as test equivalents.

### Single-test equivalents (important)
```bash
# Site regression check
bundle exec jekyll build --verbose

# Run one exercise notebook
jupyter nbconvert --to notebook --execute \
  exercises/Chapter01_Bayesian_Inference_Exercises.ipynb \
  --output /tmp/chapter01-executed.ipynb

# Run one lab notebook (path has spaces)
jupyter nbconvert --to notebook --execute \
  "labs/Bayesian Inference - Lab 1.ipynb" \
  --output /tmp/lab1-executed.ipynb

# Run one figure script
python img/chapter_img/chapter04/generate_regression_generative_images.py
```

### CI-like local check
```bash
bundle exec jekyll build --baseurl "/bayesian-statistics-self-learning"
```

## Code Style Guidelines

### Cross-cutting
- Keep changes minimal and task-focused.
- Do not refactor unrelated files.
- Preserve backward compatibility unless explicitly requested.
- Keep EN/VI content in sync when editing lesson material.
- Avoid adding new frameworks/tools unless requested.

### Imports, formatting, and types
- Python imports: standard library -> third-party -> local.
- Follow file-local style; no global formatter is enforced.
- Python: manual PEP 8 style.
- Ruby: follow style in `_plugins/*.rb`.
- JavaScript: repo mixes ES5/ES6; stay consistent with the touched file.
- Python type hints are optional, but recommended for new reusable functions.
- Do not introduce heavy type-system migrations unless explicitly requested.

### Naming conventions
- Python: `snake_case` for variables/functions, `UPPER_CASE` for constants.
- JavaScript: `camelCase` for variables/functions.
- Lesson posts: `YYYY-MM-DD-topic.md`.
- Figure scripts: `generate_<topic>.py`.
- Exercise notebooks: `ChapterXX_<Topic>_Exercises.ipynb`.

### Error handling
- Handle expected user/data errors with clear messages.
- Keep unexpected exceptions visible (avoid broad silent catches).
- JS DOM logic should guard null selectors before access.
- Ruby plugin code should handle missing keys/`nil` defensively.

### Reproducibility
- Set fixed random seeds in simulation/visualization scripts.
- Avoid hidden global state in notebooks/scripts when practical.

### Markdown/content rules
- Preserve front matter keys used by nearby posts.
- Keep lesson writing narrative and motivation-first.
- Use `$$...$$` for formulas in this repository.
- Keep links/asset paths compatible with existing `{{ site.baseurl }}` patterns.

## Cursor/Copilot Rules

### Detected rule files
- `.cursor/rules/lecture-notes-rule.mdc`
- `.cursor/rules/practice-rule.mdc`
- `.cursor/rules/lab-rule.mdc`
- `.cursor/rules/math-formula-rule.mdc`
- `.cursorrules`: not found
- `.github/copilot-instructions.md`: not found

### Required behavior distilled from Cursor rules
- Teach Bayesian statistics as reasoning about data-generating processes.
- Present models as generative stories before heavy formalism/code.
- Prioritize interpretation, uncertainty, and model criticism.
- For practical/lab tasks, prefer Python + PyMC + ArviZ.
- For formula explainers: statement, explanation, derivation, example.
- Use `$$` delimiters consistently for math expressions.

## Validation Checklist
- Run `bundle exec jekyll build --verbose`.
- Verify touched pages render (math, image paths, internal links).
- Execute changed notebook/script at least once when applicable.
- Confirm EN/VI parity for bilingual content updates.

## Git Hygiene
- Do not push unless explicitly requested.
- Do not rewrite history unless explicitly requested.
- Avoid unrelated formatting churn.
- Report commands run and files changed in handoff.

Last updated: 2026-03-21
