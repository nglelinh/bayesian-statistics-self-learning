---
layout: post
title: "Bài 10.2: Model Diagnostics & Reporting Best Practices"
chapter: '10'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter10
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu comprehensive diagnostics cho Bayesian models và best practices cho reporting results. Bạn sẽ biết check convergence (R-hat, ESS), identify problems (divergences, low ESS), và communicate findings effectively.

## Giới thiệu: Why Diagnostics Matter

**MCMC is not magic**: Sampling can fail! Diagnostics help detect:
- **Non-convergence**: Chains haven't reached stationary distribution
- **Poor mixing**: Chains explore posterior slowly
- **Numerical issues**: Divergences, max treedepth warnings

**Best practice**: ALWAYS check diagnostics before trusting results!

## 1. Essential MCMC Diagnostics

### 1.1. Trace Plots - Visual Convergence Check

**Trace plot**: Parameter value vs iteration.

**Good trace**: "Hairy caterpillar" - random fluctuations around stable mean.
**Bad trace**: Trends, stuck values, different chains in different regions.

```python
import pymc as pm
import arviz as az
import numpy as np
import matplotlib.pyplot as plt

# Example: Fit model
np.random.seed(42)
x = np.random.uniform(0, 10, 50)
y = 2 + 0.5*x + np.random.normal(0, 2, 50)

with pm.Model() as model:
    alpha = pm.Normal('alpha', 0, 10)
    beta = pm.Normal('beta', 0, 10)
    sigma = pm.HalfNormal('sigma', 5)
    mu = alpha + beta * x
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
    trace = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                     return_inferencedata=True)

# Trace plots
az.plot_trace(trace, var_names=['alpha', 'beta', 'sigma'])
plt.tight_layout()
plt.show()

print("✅ GOOD TRACE: Chains overlap, no trends, stable")
```

### 1.2. R-hat (Gelman-Rubin Statistic)

**R-hat**: Measures convergence by comparing within-chain vs between-chain variance.

**Interpretation**:
- R-hat ≈ 1.00: Converged ✅
- R-hat > 1.01: Potential convergence issues ⚠️
- R-hat > 1.05: Serious problems ❌

**Rule**: R-hat < 1.01 for all parameters.

```python
print("\n" + "=" * 70)
print("R-HAT DIAGNOSTICS")
print("=" * 70)
summary = az.summary(trace, var_names=['alpha', 'beta', 'sigma'])
print(summary[['mean', 'sd', 'r_hat']])
print("\n✅ All R-hat < 1.01 → Converged!")
print("=" * 70)
```

### 1.3. Effective Sample Size (ESS)

**ESS**: Number of "independent" samples (accounting for autocorrelation).

**Two types**:
- **ESS bulk**: For mean/median
- **ESS tail**: For quantiles (e.g., 95% CI)

**Rule**: ESS > 400 for reliable inference (per chain: > 100).

```python
print("\n" + "=" * 70)
print("EFFECTIVE SAMPLE SIZE")
print("=" * 70)
print(summary[['ess_bulk', 'ess_tail']])
print("\n✅ All ESS > 400 → Sufficient samples!")
print("=" * 70)
```

### 1.4. Divergences

**Divergence**: MCMC step rejected due to numerical instability.

**Causes**: Difficult posterior geometry (e.g., funnel, multimodality).

**Solutions**:
- Increase `target_accept` (default 0.8 → 0.95)
- Reparameterize model
- Use non-centered parameterization

```python
# Check divergences
n_divergences = trace.sample_stats['diverging'].sum().item()
print(f"\n Divergences: {n_divergences}")
if n_divergences > 0:
    print("⚠️ WARNING: Increase target_accept or reparameterize")
else:
    print("✅ No divergences!")
```

## 2. Reporting Best Practices

### 2.1. What to Report

**Essential**:
1. **Model specification**: Priors, likelihood, structure
2. **Posterior estimates**: Mean, SD, credible intervals
3. **Diagnostics**: R-hat, ESS, divergences
4. **Uncertainty**: Always report intervals, not just point estimates
5. **Visualizations**: Posterior distributions, predictions

**Example report**:
```python
print("\n" + "=" * 70)
print("BAYESIAN REGRESSION REPORT")
print("=" * 70)
print("\n1. MODEL:")
print("   y ~ Normal(α + βx, σ)")
print("   Priors: α ~ Normal(0, 10), β ~ Normal(0, 10), σ ~ HalfNormal(5)")

print("\n2. DATA:")
print(f"   n = {len(y)} observations")

print("\n3. POSTERIOR ESTIMATES (mean ± SD, 94% HDI):")
for var in ['alpha', 'beta', 'sigma']:
    samples = trace.posterior[var].values.flatten()
    hdi = az.hdi(samples, hdi_prob=0.94)
    print(f"   {var}: {samples.mean():.3f} ± {samples.std():.3f}, " +
          f"HDI = [{hdi[0]:.3f}, {hdi[1]:.3f}]")

print("\n4. DIAGNOSTICS:")
print(f"   All R-hat < 1.01: ✅")
print(f"   All ESS > 400: ✅")
print(f"   Divergences: {n_divergences} ✅")

print("\n5. INTERPRETATION:")
print(f"   • Slope (β): {trace.posterior['beta'].values.mean():.3f}")
print(f"     → 1 unit increase in x → {trace.posterior['beta'].values.mean():.3f} increase in y")
print("=" * 70)
```

## Tóm tắt

**Diagnostics**:
- **Trace plots**: Visual check
- **R-hat < 1.01**: Convergence
- **ESS > 400**: Sufficient samples
- **Divergences = 0**: No numerical issues

**Reporting**:
- Model specification
- Posterior + uncertainty
- Diagnostics
- Interpretation

**Key**: Always check diagnostics before trusting results!

## Bài tập

**Bài tập 1**: Fit model. Check all diagnostics. Report results.

**Bài tập 2**: Intentionally create bad model (e.g., very wide priors). Observe poor diagnostics.

**Bài tập 3**: Real data. Write comprehensive report following best practices.

## Tài liệu Tham khảo

**Gelman, A., et al. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.

**Vehtari, A., et al. (2021).** "Rank-Normalization, Folding, and Localization: An Improved R-hat for Assessing Convergence of MCMC." *Bayesian Analysis*.

---

*Bài học tiếp theo: [10.3 Prior Sensitivity Analysis](/vi/chapter10/prior-sensitivity/)*
