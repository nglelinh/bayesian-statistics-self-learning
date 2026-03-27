## Chapter 07 Applied-ML Gap Checklist

| Applied topic | Current status in Chapter 07 | Gap summary |
|---|---|---|
| ML pipeline framing (problem -> data -> model -> evaluation -> interpretation) | Partial | Existing lessons are concept-strong but not organized as one applied workflow. |
| Data splitting (train/validation/test) | Partial | Mentioned indirectly via overfitting but not formalized as a decision protocol. |
| Data leakage prevention | Missing | No explicit guardrails for scaling/feature engineering inside folds only. |
| Metric-based model selection | Partial | General mention of test error and CV, but little guidance on task-specific metric choice. |
| Prior-scale / regularization tuning | Partial | Prior strength is discussed; operational tuning process is not explicit. |
| Uncertainty-aware evaluation | Partial | Posterior predictive checks and uncertainty exist separately, but not integrated into model selection checklist. |
| Feature-selection stability | Missing | Selection uncertainty is introduced, but resampling stability and threshold calibration are not operationalized. |
| End-to-end reproducible applied case | Missing | No single Chapter 07 case that connects all three lessons in one flow. |

## Integration Map Across Lessons

- **Lesson 7.1 (Regularization with priors)**
  - Add pipeline guardrails for preprocessing and leakage control.
  - Add practical prior-scale tuning workflow (validation + prior predictive checks).
  - Introduce the applied case context and dataset setup used across Chapter 07.

- **Lesson 7.2 (Bias-variance tradeoff)**
  - Add explicit train/validation/test strategy and learning-curve reading.
  - Add model-complexity tuning playbook linked to bias-variance diagnostics.
  - Continue the same applied case with model comparison checkpoints.

- **Lesson 7.3 (Feature selection)**
  - Add uncertainty-aware thresholding and resampling stability guidance.
  - Add interpretation-risk notes (correlation, proxy features, domain plausibility).
  - Complete applied case with final feature interpretation and reporting template.

## Scope Note

All changes are limited to Vietnamese Chapter 07 (`contents/vi/chapter07/`) and optional supporting visual scripts under `img/chapter_img/chapter07/`.
