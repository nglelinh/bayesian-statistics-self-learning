# Chapter 04 - New Visualizations (March 2026)

## Bayesian Regression Diagnostics

This directory contains 3 new visualizations for regression analysis and model validation.

### New Images Added (March 9, 2026)

**Script**: `generate_regression_diagnostics.py`

1. **regression_assumptions_diagnostic.png**
   - 6-panel comprehensive regression diagnostics
   - Checks: Linearity, homoscedasticity, normality, independence
   - Use: Teaching regression assumptions workflow

2. **posterior_predictive_checks.png**
   - Full posterior predictive checking workflow
   - 4-panel: Data, replications, test statistics, p-values
   - Use: Bayesian model validation

3. **model_comparison_loo_waic.png**
   - LOO-CV and WAIC visual explanation
   - 4-panel: LOO process, WAIC, comparison, decision
   - Use: Model selection methods

### Regenerate Images

```bash
python3 generate_regression_diagnostics.py
```

### Integration Example

```markdown
![Regression Diagnostics]({{ site.baseurl }}/img/chapter_img/chapter04/regression_assumptions_diagnostic.png)

![Posterior Predictive Checks]({{ site.baseurl }}/img/chapter_img/chapter04/posterior_predictive_checks.png)

![Model Comparison]({{ site.baseurl }}/img/chapter_img/chapter04/model_comparison_loo_waic.png)
```

**Total images in chapter**: 22 (3 new + 19 existing)
