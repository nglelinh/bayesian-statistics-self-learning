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

![Overfitting Demonstration](../../../img/chapter_img/chapter07/overfitting_demonstration.png)

**Overfitting demonstration với polynomial regression:**
- **Degree 1** (top-left): UNDERFIT - Too simple
  - High training error, high test error
  - Model quá đơn giản, không capture được pattern
- **Degree 3** (top-right): GOOD FIT - Just right
  - Low training error, low test error
  - Balance giữa bias và variance
- **Degree 10** (bottom-left): OVERFIT - Too complex
  - Very low training error, HIGH test error
  - Bắt đầu memorize noise trong training data
- **Degree 15** (bottom-right): SEVERE OVERFIT
  - Perfect training fit, terrible test performance
  - Model hoàn toàn mất khả năng generalize

**Key insight**: Test error tăng cao khi model quá phức tạp → cần regularization!

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

![Regularization Priors](../../../img/chapter_img/chapter07/regularization_priors.png)

**Regularization priors comparison:**
- **Normal prior (Ridge/L2)** - Panel trái:
  - Gaussian distribution centered at 0
  - Smooth tails → coefficients shrink towards 0 but rarely exactly 0
  - Good for when many predictors có small effects
- **Laplace prior (Lasso/L1)** - Panel giữa:
  - Sharp peak at 0, heavier tails
  - Promotes **sparsity**: nhiều coefficients = exactly 0
  - Good for **feature selection** (automatic variable selection)
- **Comparison** - Panel phải:
  - Laplace có sharper peak → stronger sparsity
  - Normal smoother → shrinkage without exact zeros
  - Uniform (flat) = no regularization → overfitting risk
  
**Key insight**: Priors encode regularization preferences!

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
