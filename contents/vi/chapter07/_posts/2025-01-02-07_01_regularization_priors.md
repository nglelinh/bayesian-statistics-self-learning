---
layout: post
title: "Bài 7.1: Regularization với Priors - Ngăn Overfitting"
chapter: '07'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter07
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu về **regularization** - kỹ thuật quan trọng để ngăn **overfitting**. Bạn sẽ học cách priors trong Bayesian statistics tự nhiên thực hiện regularization, so sánh với Ridge (L2) và Lasso (L1) regression, và biết khi nào cần regularization. Đây là kỹ năng thiết yếu cho modeling với nhiều predictors.

## Giới thiệu: Vấn đề Overfitting

**Scenario**: Bạn có 20 data points và muốn fit polynomial regression.

**Câu hỏi**: Degree bao nhiêu là đủ?
- Degree 1: Simple linear (có thể underfit)
- Degree 10: Perfect fit training data (nhưng overfit!)
- Degree 15: Crazy wiggles!

**Overfitting**: Model học **noise** thay vì **signal** → poor generalization.

## 1. Demonstrating Overfitting

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split

# Generate data
np.random.seed(42)
n = 25
x = np.random.uniform(0, 10, n)
y_true = 2 + 0.5*x + np.random.normal(0, 2, n)

# Split train/test
x_train, x_test, y_train, y_test = train_test_split(
    x, y_true, test_size=0.3, random_state=42
)

# Fit models with different polynomial degrees
degrees = [1, 3, 10, 15]
x_plot = np.linspace(0, 10, 200)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.ravel()

for idx, degree in enumerate(degrees):
    # Transform
    poly = PolynomialFeatures(degree=degree)
    X_train_poly = poly.fit_transform(x_train.reshape(-1, 1))
    X_test_poly = poly.transform(x_test.reshape(-1, 1))
    X_plot_poly = poly.transform(x_plot.reshape(-1, 1))
    
    # Fit
    lr = LinearRegression().fit(X_train_poly, y_train)
    
    # Predict
    y_pred_train = lr.predict(X_train_poly)
    y_pred_test = lr.predict(X_test_poly)
    y_plot = lr.predict(X_plot_poly)
    
    # Compute errors
    train_rmse = np.sqrt(np.mean((y_train - y_pred_train)**2))
    test_rmse = np.sqrt(np.mean((y_test - y_pred_test)**2))
    
    # Plot
    axes[idx].scatter(x_train, y_train, s=80, alpha=0.7, label='Train',
                     edgecolors='black', zorder=3)
    axes[idx].scatter(x_test, y_test, s=80, alpha=0.7, label='Test',
                     edgecolors='black', zorder=3)
    axes[idx].plot(x_plot, y_plot, 'r-', linewidth=3, label='Fit', zorder=2)
    
    # Title with error
    color = 'green' if degree <= 3 else 'red'
    axes[idx].set_title(f'Degree = {degree}\n' +
                       f'Train RMSE = {train_rmse:.2f}, Test RMSE = {test_rmse:.2f}',
                       fontsize=13, fontweight='bold', color=color)
    axes[idx].set_xlabel('x', fontsize=11, fontweight='bold')
    axes[idx].set_ylabel('y', fontsize=11, fontweight='bold')
    axes[idx].legend(fontsize=10)
    axes[idx].grid(alpha=0.3)
    axes[idx].set_ylim(-5, 15)

plt.tight_layout()
plt.show()

print("=" * 70)
print("OVERFITTING DEMONSTRATION")
print("=" * 70)
print("\nObservations:")
print("  • Low degree: High train & test error (UNDERFIT)")
print("  • Medium degree: Low train & test error (GOOD FIT)")
print("  • High degree: Low train, HIGH test error (OVERFIT)")
print("\n→ Overfitting = model memorizes training data!")
print("=" * 70)
```

## 2. Regularization: The Solution

**Idea**: **Penalize large coefficients** → prefer simpler models.

### 2.1. Ridge Regression (L2 Regularization)

**Objective**:
$$
\min_{\beta} \sum_{i=1}^n (y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^p \beta_j^2
$$

- First term: Fit data well
- Second term: Keep coefficients small
- $$\lambda$$: Regularization strength (higher = more penalty)

**Bayesian interpretation**: Ridge = **Normal prior** on coefficients!

$$
\beta_j \sim \text{Normal}(0, \sigma^2)
$$

### 2.2. Lasso Regression (L1 Regularization)

**Objective**:
$$
\min_{\beta} \sum_{i=1}^n (y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^p |\beta_j|
$$

**Bayesian interpretation**: Lasso = **Laplace prior** on coefficients!

$$
\beta_j \sim \text{Laplace}(0, b)
$$

```python
# Visualize priors
from scipy import stats

beta_vals = np.linspace(-3, 3, 200)

# Normal (Ridge)
normal_prior = stats.norm.pdf(beta_vals, 0, 1)

# Laplace (Lasso)
laplace_prior = stats.laplace.pdf(beta_vals, 0, 0.7)

# Uniform (no regularization)
uniform_prior = np.ones_like(beta_vals) * 0.3

# Visualize
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Normal prior (Ridge)
axes[0].plot(beta_vals, normal_prior, 'b-', linewidth=3)
axes[0].fill_between(beta_vals, normal_prior, alpha=0.3)
axes[0].set_xlabel('β', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('NORMAL PRIOR\n(Ridge / L2 Regularization)\n' +
                 'β ~ Normal(0, σ²)',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)
axes[0].text(0, max(normal_prior)*0.5, 'Prefers small β\nGaussian tails',
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Laplace prior (Lasso)
axes[1].plot(beta_vals, laplace_prior, 'g-', linewidth=3)
axes[1].fill_between(beta_vals, laplace_prior, alpha=0.3, color='green')
axes[1].set_xlabel('β', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('LAPLACE PRIOR\n(Lasso / L1 Regularization)\n' +
                 'β ~ Laplace(0, b)',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)
axes[1].text(0, max(laplace_prior)*0.5, 'Prefers β = 0\nSparse solutions',
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# Comparison
axes[2].plot(beta_vals, normal_prior, 'b-', linewidth=3, label='Normal (Ridge)')
axes[2].plot(beta_vals, laplace_prior, 'g-', linewidth=3, label='Laplace (Lasso)')
axes[2].plot(beta_vals, uniform_prior, 'r--', linewidth=2, label='Uniform (No reg.)')
axes[2].set_xlabel('β', fontsize=12, fontweight='bold')
axes[2].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[2].set_title('COMPARISON\nDifferent Regularization Priors',
                 fontsize=14, fontweight='bold')
axes[2].legend(fontsize=11)
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("REGULARIZATION PRIORS")
print("=" * 70)
print("\nRidge (L2) = Normal prior:")
print("  • Shrinks all coefficients toward 0")
print("  • Keeps all predictors")
print("  • Good for correlated predictors")

print("\nLasso (L1) = Laplace prior:")
print("  • Sets some coefficients EXACTLY to 0")
print("  • Automatic feature selection")
print("  • Sparse solutions")
print("=" * 70)
```

## 3. Bayesian Regularization trong PyMC

```python
import pymc as pm
import arviz as az

# Generate data with many predictors
np.random.seed(42)
n = 100
p = 20  # 20 predictors

X = np.random.randn(n, p)
# Only first 3 predictors matter
beta_true = np.zeros(p)
beta_true[:3] = [2, -1.5, 1]
y = X @ beta_true + np.random.normal(0, 1, n)

# Standardize
X_z = (X - X.mean(axis=0)) / X.std(axis=0)
y_z = (y - y.mean()) / y.std()

# Model 1: Weak priors (no regularization)
with pm.Model() as model_weak:
    alpha = pm.Normal('alpha', 0, 10)  # Weak!
    beta = pm.Normal('beta', 0, 10, shape=p)  # Weak!
    sigma = pm.HalfNormal('sigma', 2)
    
    mu = alpha + pm.math.dot(X_z, beta)
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    trace_weak = pm.sample(1000, tune=500, chains=2, random_seed=42,
                          return_inferencedata=True, progressbar=False)

# Model 2: Strong priors (regularization)
with pm.Model() as model_reg:
    alpha = pm.Normal('alpha', 0, 1)
    beta = pm.Normal('beta', 0, 0.5, shape=p)  # Strong regularization!
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + pm.math.dot(X_z, beta)
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    trace_reg = pm.sample(1000, tune=500, chains=2, random_seed=42,
                         return_inferencedata=True, progressbar=False)

# Compare coefficients
beta_weak = trace_weak.posterior['beta'].values.reshape(-1, p).mean(axis=0)
beta_reg = trace_reg.posterior['beta'].values.reshape(-1, p).mean(axis=0)

# Visualize
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# True coefficients
axes[0].bar(range(p), beta_true, alpha=0.7, edgecolor='black')
axes[0].axhline(0, color='red', linestyle='--', linewidth=2)
axes[0].set_xlabel('Predictor Index', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
axes[0].set_title('TRUE COEFFICIENTS\nOnly first 3 non-zero',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3, axis='y')

# Weak priors
axes[1].bar(range(p), beta_weak, alpha=0.7, edgecolor='black', color='orange')
axes[1].axhline(0, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Predictor Index', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
axes[1].set_title('WEAK PRIORS (No Regularization)\n' +
                 'Many non-zero coefficients',
                 fontsize=14, fontweight='bold', color='red')
axes[1].grid(alpha=0.3, axis='y')

# Strong priors (regularization)
axes[2].bar(range(p), beta_reg, alpha=0.7, edgecolor='black', color='green')
axes[2].axhline(0, color='red', linestyle='--', linewidth=2)
axes[2].set_xlabel('Predictor Index', fontsize=12, fontweight='bold')
axes[2].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
axes[2].set_title('STRONG PRIORS (Regularization)\n' +
                 'Shrinkage toward 0',
                 fontsize=14, fontweight='bold', color='green')
axes[2].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("REGULARIZATION EFFECT")
print("=" * 70)
print(f"\nWeak priors:")
print(f"  Non-zero coefficients: {np.sum(np.abs(beta_weak) > 0.1)}/{p}")
print(f"  Max |β|: {np.abs(beta_weak).max():.3f}")

print(f"\nStrong priors (regularization):")
print(f"  Non-zero coefficients: {np.sum(np.abs(beta_reg) > 0.1)}/{p}")
print(f"  Max |β|: {np.abs(beta_reg).max():.3f}")

print(f"\n→ Regularization shrinks coefficients toward 0!")
print("=" * 70)
```

## 4. Choosing Regularization Strength

**How strong should priors be?**

### 4.1. Cross-Validation

Use cross-validation to choose prior scale.

### 4.2. Prior Predictive Checks

Check if priors generate reasonable predictions.

```python
# Prior predictive check
with pm.Model() as model_check:
    alpha = pm.Normal('alpha', 0, 1)
    beta = pm.Normal('beta', 0, 0.5, shape=p)
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + pm.math.dot(X_z, beta)
    y_prior = pm.Normal('y_prior', mu=mu, sigma=sigma, shape=n)
    
    # Sample from prior
    prior_samples = pm.sample_prior_predictive(samples=500, random_seed=42)

# Visualize
y_prior_samples = prior_samples.prior['y_prior'].values.reshape(-1, n)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Prior predictions
for i in range(min(100, y_prior_samples.shape[0])):
    axes[0].hist(y_prior_samples[i], bins=30, alpha=0.02, color='blue', density=True)
axes[0].hist(y_z, bins=30, alpha=0.7, color='red', edgecolor='black',
            density=True, label='Observed data')
axes[0].set_xlabel('y (standardized)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('PRIOR PREDICTIVE CHECK\n' +
                 'Do priors generate reasonable data?',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')

# Prior means and SDs
prior_means = y_prior_samples.mean(axis=1)
prior_sds = y_prior_samples.std(axis=1)

axes[1].scatter(prior_means, prior_sds, alpha=0.5, s=30, edgecolors='black')
axes[1].axvline(y_z.mean(), color='red', linewidth=2, label='Observed mean')
axes[1].axhline(y_z.std(), color='red', linewidth=2, linestyle='--',
               label='Observed SD')
axes[1].set_xlabel('Prior Predicted Mean', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Prior Predicted SD', fontsize=12, fontweight='bold')
axes[1].set_title('PRIOR PREDICTIONS\nMean vs SD',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## 5. Khi nào Cần Regularization?

**Regularization cần thiết khi**:
1. **Many predictors** (p large relative to n)
2. **Correlated predictors** (multicollinearity)
3. **Small sample size** (n small)
4. **Want sparse solutions** (feature selection)

**Regularization KHÔNG cần khi**:
- Few predictors (p << n)
- Large sample size
- Predictors uncorrelated
- Strong theory about all predictors

## Tóm tắt

Regularization ngăn overfitting bằng cách penalize large coefficients:

- **Ridge (L2)**: Normal prior → shrinks all coefficients
- **Lasso (L1)**: Laplace prior → sparse solutions
- **Bayesian**: Priors = natural regularization
- **Strength**: Choose via cross-validation or prior predictive checks

**Key insight**: In Bayesian statistics, regularization is just **choosing appropriate priors**!

Bài tiếp theo: **Bias-Variance Tradeoff**.

## Bài tập

**Bài tập 1**: Generate high-dimensional data (p > n). Fit với weak và strong priors. Compare.

**Bài tập 2**: Implement Lasso prior (Laplace) trong PyMC. Compare với Ridge.

**Bài tập 3**: Use cross-validation to choose optimal prior scale.

**Bài tập 4**: Prior predictive checks với different prior scales. Which is reasonable?

**Bài tập 5**: Real data với many predictors. Apply regularization và interpret results.

## Tài liệu Tham khảo

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 12: Transformations and regression

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 4: Geocentric Models (Priors as regularization)

---

*Bài học tiếp theo: [7.2 Bias-Variance Tradeoff](/vi/chapter07/bias-variance-tradeoff/)*
