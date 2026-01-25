---
layout: post
title: "Bài 11.1: Gaussian Processes - Distributions over Functions"
chapter: '11'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter11
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **Gaussian Processes (GP)** - một trong những nonparametric methods mạnh nhất trong machine learning. Bạn sẽ hiểu GP as distributions over functions, kernels (covariance functions), và cách fit GP models. Đây là advanced topic cho flexible function learning without specifying functional form.

## Giới thiệu: Beyond Parametric Models

**Parametric models** (linear, polynomial): Must specify functional form.
- Problem: What if form is wrong?

**Gaussian Process**: Let data determine function shape!
- No need to specify form (e.g., linear, quadratic)
- Flexible, smooth interpolation
- Full uncertainty quantification

**Key idea**: Instead of parameters, we have **distribution over functions**.

## 1. GP Intuition

**Gaussian Process**: Collection of random variables, any finite subset is jointly Gaussian.

**Formal definition**:
$$
f(x) \sim \mathcal{GP}(m(x), k(x, x'))
$$

where:
- $$m(x)$$: Mean function (usually 0)
- $$k(x, x')$$: Covariance function (kernel) - defines similarity

**Kernel**: Determines how function values at different x are correlated.

## 2. Common Kernels

**Squared Exponential (RBF)**:
$$
k(x, x') = \eta^2 \exp\left(-\frac{(x - x')^2}{2\ell^2}\right)
$$

- $$\eta^2$$: Variance (amplitude)
- $$\ell$$: Length scale (smoothness)

**Properties**: Smooth, infinitely differentiable.

## 3. GP Regression Example

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az

# Generate data
np.random.seed(42)
X_train = np.array([1, 3, 5, 6, 8])[:, None]
y_train = np.sin(X_train).flatten() + np.random.normal(0, 0.1, 5)

# GP model
with pm.Model() as gp_model:
    # Kernel parameters
    ℓ = pm.Gamma('ℓ', alpha=2, beta=1)  # Length scale
    η = pm.HalfNormal('η', sigma=5)     # Amplitude
    
    # Covariance function
    cov_func = η**2 * pm.gp.cov.ExpQuad(1, ℓ)
    
    # GP
    gp = pm.gp.Marginal(cov_func=cov_func)
    
    # Noise
    σ = pm.HalfNormal('σ', sigma=0.5)
    
    # Likelihood
    y_obs = gp.marginal_likelihood('y_obs', X=X_train, y=y_train, noise=σ)
    
    # Sample
    trace = pm.sample(1000, tune=500, chains=2, random_seed=42,
                     return_inferencedata=True, progressbar=False)
    
    # Predict
    X_test = np.linspace(0, 10, 100)[:, None]
    f_pred = gp.conditional('f_pred', X_test)
    pred_samples = pm.sample_posterior_predictive(
        trace, var_names=['f_pred'], random_seed=42
    )

print("=" * 70)
print("GAUSSIAN PROCESS REGRESSION")
print("=" * 70)
print("\nGP learns smooth function from data")
print("No need to specify polynomial degree!")
print("Uncertainty increases away from data")
print("=" * 70)

# Visualize
f_pred_samples = pred_samples.posterior_predictive['f_pred'].values.reshape(-1, 100)
f_mean = f_pred_samples.mean(axis=0)
f_std = f_pred_samples.std(axis=0)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(X_test, f_mean, 'b-', linewidth=2, label='GP mean')
ax.fill_between(X_test.flatten(), f_mean - 2*f_std, f_mean + 2*f_std,
               alpha=0.3, label='±2 SD')
ax.scatter(X_train, y_train, s=100, color='red', zorder=5,
          edgecolors='black', linewidths=2, label='Training data')
ax.set_xlabel('x', fontsize=13, fontweight='bold')
ax.set_ylabel('f(x)', fontsize=13, fontweight='bold')
ax.set_title('GAUSSIAN PROCESS: Flexible Function Learning',
            fontsize=15, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

## Tóm tắt

**Gaussian Processes**:
- **Nonparametric**: No fixed functional form
- **Flexible**: Adapts to data
- **Kernel**: Defines similarity/smoothness
- **Uncertainty**: Full posterior over functions
- **Cost**: Computationally expensive (O(n³))

**Applications**: Time series, spatial data, Bayesian optimization.

**Key insight**: GP automatically balances smoothness and fit to data!

## Bài tập

**Bài tập 1**: Vary length scale ℓ. How does smoothness change?

**Bài tập 2**: Real data. Fit GP. Compare with polynomial regression.

**Bài tập 3**: Predict at new x. Visualize uncertainty.

## Tài liệu Tham khảo

**Rasmussen, C. E., & Williams, C. K. I. (2006).** *Gaussian Processes for Machine Learning*. MIT Press.

---

*Bài học tiếp theo: [11.2 Mixture Models](/vi/chapter11/mixture-models/)*
