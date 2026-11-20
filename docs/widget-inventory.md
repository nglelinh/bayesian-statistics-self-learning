# Danh mục widget (widget inventory)

## Explainer Svelte (bundle `public/js/explainers/bayes-explainer.js`, 261 kB)
Có 22 loại explainer, 56 instance trên 32 trang. Tab/biến thể trong ngoặc. Mọi URL có dạng `/bayesian-statistics-self-learning/contents/<lang>/<chapter>/<slug>/` (slug = tên file bỏ ngày).

| `data-demo` | Trang |
|---|---|
| `bayesrule-explainer` | vi/chapter01/01_03_bayes_theorem_posterior (tree); vi/chapter01/01_03_bayes_theorem_posterior (sequential) |
| `bf-explainer` | vi/chapter08/08_03_model_comparison (seq); vi/chapter08/08_03_model_comparison (prior) |
| `biasvar-explainer` | vi/chapter07/07_02_bias_variance_tradeoff |
| `clt-explainer` | vi/chapter00/00_14_law_large_numbers_clt (lln); vi/chapter00/00_14_law_large_numbers_clt (clt); vi/chapter00/00_15_sampling_distribution_standard_error (clt) |
| `collinear-explainer` | vi/chapter05/05_03_multicollinearity |
| `confound-explainer` | vi/chapter05/05_02_confounding_dags (fork); vi/chapter05/05_02_confounding_dags (collider); vi/chapter05/05_04_interaction_effects (interaction) |
| `conjugate-explainer` | en/chapter02/02_03_prior (betabinom); en/chapter02/02_04_posterior (betabinom); en/chapter02/02_05_conjugate_priors (betabinom); en/chapter02/02_05_conjugate_priors (gammapoisson); en/chapter02/02_05_conjugate_priors (normalnormal); vi/chapter02/02_03_prior (betabinom); vi/chapter02/02_04_posterior (betabinom); vi/chapter02/02_05_conjugate_priors (betabinom); vi/chapter02/02_05_conjugate_priors (gammapoisson); vi/chapter02/02_05_conjugate_priors (normalnormal) |
| `decision-explainer` | vi/chapter08/08_04_decision_analysis (threshold); vi/chapter08/08_04_decision_analysis (loss); vi/chapter08/08_04_decision_analysis (voi) |
| `glm-explainer` | vi/chapter06/06_01_logistic_regression (logistic); vi/chapter06/06_02_poisson_regression (poisson) |
| `glmppc-explainer` | vi/chapter06/06_03_model_evaluation_glm (logistic) |
| `grid-explainer` | en/chapter02/02_06_grid_approximation; en/chapter02/02_06_grid_approximation; vi/chapter02/02_06_grid_approximation; vi/chapter02/02_06_grid_approximation |
| `horseshoe-explainer` | vi/chapter07/07_03_feature_selection |
| `ic-explainer` | vi/chapter08/08_02_information_criteria (waic); vi/chapter08/08_03_model_comparison (avg) |
| `interval-explainer` | en/chapter02/02_04_posterior; vi/chapter00/00_08_pvalues_and_hypothesis_testing; vi/chapter01/01_04_bayesian_vs_frequentist; vi/chapter02/02_04_posterior |
| `likelihood-explainer` | en/chapter02/02_02_likelihood (poisson); en/chapter02/02_02_likelihood (binom); en/chapter02/02_03_prior (predictive); vi/chapter02/02_02_likelihood (poisson); vi/chapter02/02_02_likelihood (binom); vi/chapter02/02_03_prior (predictive) |
| `mcmc-explainer` | vi/chapter04/04_02b_mcmc_theory (metropolis); vi/chapter04/04_02b_mcmc_theory (gibbs); vi/chapter04/04_02b_mcmc_theory (hmc) |
| `overdisp-explainer` | vi/chapter06/06_02_poisson_regression (nb) |
| `pooling-explainer` | vi/chapter04/04_06_case_study_complex_dataset |
| `ppc-explainer` | vi/chapter08/08_01_ppc |
| `pvalue-explainer` | vi/chapter00/00_08_pvalues_and_hypothesis_testing (pnull); vi/chapter00/00_08_pvalues_and_hypothesis_testing (power); vi/chapter00/00_09_t_test_and_t_distribution (tdist) |
| `regression-explainer` | vi/chapter04/04_01_linear_regression_generative |
| `shrink-explainer` | vi/chapter07/07_01_regularization_priors |

## Widget có sẵn từ trước
| Widget | Vị trí | Ghi chú |
|---|---|---|
| DAG explorer | `tools/dag-explorer/` (liên kết từ 05_02 §11) | JS thuần, không đụng tới; `confound-explainer` bổ sung bằng mô phỏng số (Simpson, collider, interaction) |

## Thư viện/JS chung
MathJax (CDN, `_includes/head.html`), `public/js/*` (điều hướng, ngôn ngữ, access gate). Chưa có hub công cụ (trang `tools`), nên chưa cập nhật hub nào.

## Ứng viên còn lại
Các mục 1–16 trong `docs/plan-interactive-explainer.md` và 6 ý tưởng đợt 3 (17–22) đã hoàn thành. Còn lại: bản tiếng Anh cho chương 00–08 khi có bài; bổ sung nhỏ như biến thể PPC cho 04_03/04_04, GLM phân cấp, thêm prior co rút cho 07_01.
