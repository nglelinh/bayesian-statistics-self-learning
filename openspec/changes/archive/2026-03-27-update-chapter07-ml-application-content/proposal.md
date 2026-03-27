## Why
Chapter 07 currently introduces regularization, bias-variance tradeoff, and feature selection well at concept level, but it does not yet provide a strong end-to-end application flow for real machine learning work. A targeted update is needed so learners can translate Bayesian ideas into practical modeling decisions (data split strategy, metric choice, tuning, and robust model interpretation).

## What Changes
- Update Vietnamese Chapter 07 content under `contents/vi/chapter07/` to emphasize application-oriented ML workflows while preserving current chapter structure (7.1, 7.2, 7.3).
- Add practical sections that connect Bayesian regularization to common ML pipeline decisions: preprocessing and leakage control, train/validation/test strategy, and hyperparameter/prior-scale tuning.
- Expand worked examples to include at least one end-to-end applied case (problem framing -> modeling choices -> evaluation -> interpretation) using reproducible Python code.
- Strengthen model-selection guidance with uncertainty-aware criteria (posterior predictive checks, out-of-sample performance, and feature-selection stability) instead of single-metric optimization.
- Keep scope Vietnamese-only for this change; no English parity requirement is introduced.

## Impact
- Affected specs: `publish-course-content`
- Affected content scope:
  - `contents/vi/chapter07/index.html`
  - `contents/vi/chapter07/_posts/*.md`
  - optional supporting visuals/scripts in `img/chapter_img/chapter07/` when needed for new applied examples
- User-visible outcome: Chapter 07 becomes directly usable as an applied ML guide for Bayesian regularization and feature-selection decisions on real datasets.
