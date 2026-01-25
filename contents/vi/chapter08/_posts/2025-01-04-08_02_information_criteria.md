---
layout: post
title: "Bài 8.2: Information Criteria - WAIC và LOO"
chapter: '08'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter08
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu về **information criteria** - metrics để compare models dựa trên predictive accuracy. Bạn sẽ học WAIC (Watanabe-Akaike IC) và LOO-CV (Leave-One-Out Cross-Validation), cách compute chúng với ArviZ, và interpret results. Đây là công cụ quan trọng cho model selection.

## Giới thiệu: The Problem of Model Selection

**Scenario**: Bạn có 3 models:
- Model 1: Simple (y ~ x)
- Model 2: Polynomial (y ~ x + x²)
- Model 3: Complex (y ~ x + x² + x³ + ...)

**Question**: Which is best?

**Wrong answer**: Model with lowest training error (→ overfitting!)

**Right answer**: Model with best **out-of-sample predictive accuracy**.

## 1. Predictive Accuracy: The Gold Standard

**Goal**: Estimate how well model predicts **new data**.

**Log Pointwise Predictive Density (lppd)**:
$$
\text{lppd} = \sum_{i=1}^n \log p(y_i | y_{-i})
$$

where $$y_{-i}$$ = all data except $$i$$.

**Problem**: Need to refit model $$n$$ times (expensive!).

**Solution**: Approximate with **information criteria**.

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az

# Generate data
np.random.seed(42)
n = 50
x = np.random.uniform(0, 10, n)
y_true = 2 + 0.5*x + 0.1*x**2 + np.random.normal(0, 1, n)

# Standardize
x_z = (x - x.mean()) / x.std()
y_z = (y_true - y_true.mean()) / y_true.std()

print("=" * 70)
print("MODEL SELECTION PROBLEM")
print("=" * 70)
print("\nWe have data generated from: y = 2 + 0.5x + 0.1x²")
print("\nWhich model fits best?")
print("  Model 1: Linear (y ~ x)")
print("  Model 2: Quadratic (y ~ x + x²)")
print("  Model 3: Cubic (y ~ x + x² + x³)")
print("=" * 70)
```

## 2. WAIC: Watanabe-Akaike Information Criterion

**WAIC** = Bayesian generalization of AIC.

$$
\text{WAIC} = -2(\text{lppd} - p_{\text{WAIC}})
$$

where $$p_{\text{WAIC}}$$ = effective number of parameters (penalty).

**Lower WAIC = Better predictive accuracy**

```python
# Fit 3 models
models = {}
traces = {}

# Model 1: Linear
with pm.Model() as model_linear:
    alpha = pm.Normal('alpha', 0, 1)
    beta1 = pm.Normal('beta1', 0, 1)
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + beta1 * x_z
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    traces['Linear'] = pm.sample(1000, tune=500, chains=2, random_seed=42,
                                 return_inferencedata=True, progressbar=False)

# Model 2: Quadratic
with pm.Model() as model_quad:
    alpha = pm.Normal('alpha', 0, 1)
    beta1 = pm.Normal('beta1', 0, 1)
    beta2 = pm.Normal('beta2', 0, 1)
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + beta1 * x_z + beta2 * x_z**2
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    traces['Quadratic'] = pm.sample(1000, tune=500, chains=2, random_seed=42,
                                    return_inferencedata=True, progressbar=False)

# Model 3: Cubic
with pm.Model() as model_cubic:
    alpha = pm.Normal('alpha', 0, 1)
    beta1 = pm.Normal('beta1', 0, 1)
    beta2 = pm.Normal('beta2', 0, 1)
    beta3 = pm.Normal('beta3', 0, 1)
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + beta1 * x_z + beta2 * x_z**2 + beta3 * x_z**3
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    traces['Cubic'] = pm.sample(1000, tune=500, chains=2, random_seed=42,
                                return_inferencedata=True, progressbar=False)

# Compute WAIC
print("\n" + "=" * 70)
print("WAIC COMPARISON")
print("=" * 70)

for name, trace in traces.items():
    waic = az.waic(trace)
    print(f"\n{name}:")
    print(f"  WAIC: {waic.waic:.2f}")
    print(f"  pWAIC: {waic.p_waic:.2f} (effective parameters)")
    print(f"  SE: {waic.waic_se:.2f}")

print("\n→ Lower WAIC = Better!")
print("=" * 70)
```

## 3. LOO-CV: Leave-One-Out Cross-Validation

**LOO-CV**: Gold standard for predictive accuracy.

**Idea**: For each data point $$i$$:
1. Remove $$y_i$$
2. Fit model on remaining $$n-1$$ points
3. Predict $$y_i$$
4. Compute log probability

**Problem**: Need $$n$$ model fits!

**Solution**: **PSIS-LOO** (Pareto Smoothed Importance Sampling) approximates LOO without refitting.

```python
# Compute LOO
print("\n" + "=" * 70)
print("LOO-CV COMPARISON")
print("=" * 70)

for name, trace in traces.items():
    loo = az.loo(trace)
    print(f"\n{name}:")
    print(f"  LOO: {loo.loo:.2f}")
    print(f"  pLOO: {loo.p_loo:.2f} (effective parameters)")
    print(f"  SE: {loo.loo_se:.2f}")
    
    # Check Pareto k diagnostic
    if hasattr(loo, 'pareto_k'):
        bad_k = np.sum(loo.pareto_k > 0.7)
        if bad_k > 0:
            print(f"  ⚠️  Warning: {bad_k} observations with high Pareto k")

print("\n→ Lower LOO = Better!")
print("=" * 70)
```

## 4. Model Comparison with az.compare

**Best practice**: Use `az.compare` to compare all models at once.

```python
# Compare all models
comp = az.compare(traces, ic='loo')

print("\n" + "=" * 70)
print("MODEL COMPARISON TABLE")
print("=" * 70)
print(comp)
print("=" * 70)

# Visualize
az.plot_compare(comp, figsize=(10, 4))
plt.title('Model Comparison (LOO)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("INTERPRETING RESULTS")
print("=" * 70)
print("\nColumns:")
print("  rank: 0 = best model")
print("  loo: LOO score (higher = better)")
print("  p_loo: Effective number of parameters")
print("  d_loo: Difference from best model")
print("  weight: Stacking weights for model averaging")
print("  se: Standard error")
print("  dse: SE of difference")

best_model = comp.index[0]
print(f"\n→ Best model: {best_model}")
print("=" * 70)
```

## 5. Pareto k Diagnostic

**Pareto k**: Diagnostic for LOO reliability.

- k < 0.5: Good
- 0.5 < k < 0.7: OK
- k > 0.7: Bad (LOO unreliable)

```python
# Plot Pareto k
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, (name, trace) in enumerate(traces.items()):
    loo = az.loo(trace, pointwise=True)
    k_values = loo.pareto_k.values
    
    axes[idx].scatter(range(len(k_values)), k_values, s=50, alpha=0.6,
                     edgecolors='black')
    axes[idx].axhline(0.5, color='orange', linestyle='--', linewidth=2,
                     label='Threshold 0.5')
    axes[idx].axhline(0.7, color='red', linestyle='--', linewidth=2,
                     label='Threshold 0.7')
    axes[idx].set_xlabel('Data Point', fontsize=12, fontweight='bold')
    axes[idx].set_ylabel('Pareto k', fontsize=12, fontweight='bold')
    axes[idx].set_title(f'{name}\nMax k = {k_values.max():.3f}',
                       fontsize=13, fontweight='bold')
    axes[idx].legend(fontsize=10)
    axes[idx].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## Tóm tắt

Information Criteria cho model selection:

- **WAIC**: Bayesian AIC, fast computation
- **LOO-CV**: Gold standard, uses PSIS approximation
- **Lower = Better** predictive accuracy
- **Pareto k**: Check LOO reliability
- **az.compare**: Compare multiple models

**Key insight**: Choose model based on **predictive accuracy**, not training fit!

Bài tiếp theo: **Model Comparison** strategies.

## Bài tập

**Bài tập 1**: Fit 4 polynomial models (degree 1-4). Compute WAIC and LOO. Which is best?

**Bài tập 2**: Check Pareto k. If k > 0.7, what does it mean? How to fix?

**Bài tập 3**: Use `az.compare`. Interpret all columns. What is "weight"?

**Bài tập 4**: Compare GLMs (Logistic, Poisson) using LOO. Which fits better?

**Bài tập 5**: Real data. Fit multiple models. Use information criteria to select best.

## Tài liệu Tham khảo

**Vehtari, A., Gelman, A., & Gabry, J. (2017).** "Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC." *Statistics and Computing*, 27(5), 1413-1432.

**Gelman, A., et al. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 7: Evaluating, comparing, and expanding models

---

*Bài học tiếp theo: [8.3 Model Comparison Strategies](/vi/chapter08/model-comparison/)*
