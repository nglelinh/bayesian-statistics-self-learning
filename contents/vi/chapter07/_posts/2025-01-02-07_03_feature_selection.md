---
layout: post
title: "Bài 7.3: Feature Selection - Chọn Predictors Quan trọng"
chapter: '07'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter07
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu về **feature selection** - kỹ thuật identify predictors quan trọng khi có nhiều candidates. Bạn sẽ học Bayesian approaches (Laplace priors, spike-and-slab, horseshoe), so sánh với frequentist methods (Lasso, stepwise), và biết khi nào nên dùng approach nào. Đây là kỹ năng quan trọng cho high-dimensional data.

## Giới thiệu: Vấn đề của Many Predictors

**Scenario**: Bạn có 100 potential predictors, nhưng chỉ 5 thực sự quan trọng.

**Challenges**:
1. Fitting all 100 → overfitting
2. Testing all combinations → computationally expensive (2^100 models!)
3. Multiple testing → false discoveries

**Goal**: Automatically identify relevant predictors.

## 1. Frequentist Approaches

### 1.1. Lasso (L1 Regularization)

**Lasso** sets some coefficients **exactly to 0** → automatic feature selection.

![Lasso Feature Selection](../../../img/chapter_img/chapter07/lasso_feature_selection.png)

**Kết quả quan sát:**

**Dataset**: 20 features, chỉ 5 features đầu có true coefficients khác 0.

- **α = 0.001** (Weak regularization):
  - 13 features selected
  - Model giữ nhiều features, including noise
  
- **α = 0.01** (Still weak):
  - 13 features selected
  - Vẫn chưa đủ mạnh để loại bỏ noise

- **α = 0.1** (Moderate):
  - 13 features selected
  - Coefficients bắt đầu shrink về 0
  
- **α = 0.5** (Strong):
  - 9 features selected
  - Nhiều coefficients bị set về 0
  - Sparsity tăng

**Key observation**: Higher α → more sparsity. Lasso automatically performs feature selection bằng cách set coefficients = 0 exactly.

### 1.2. Cross-Validation để Chọn α

![Lasso CV and Regularization Path](../../../img/chapter_img/chapter07/lasso_cv_regularization_path.png)

**Kết quả Cross-Validation:**

- **Optimal α**: 1.0000 (from 5-fold CV)
- **Selected features**: 7 features
- **True relevant**: 5 features
- CV slightly overselects but close to true sparsity

**Regularization Path (Right plot):**

- **Low α** (left side): All coefficients non-zero, large magnitudes
- **Increasing α**: Coefficients shrink gradually toward 0
- **Optimal α** (red line): Balance between fit and sparsity
- **High α** (right side): Most coefficients reach 0, only strongest signals survive

**Key insight**: Cross-validation finds optimal λ that balances bias-variance. Regularization path shows how each feature "drops out" as regularization increases. The first 5 features (colored lines) are the true non-zero coefficients and persist longer than noise features (gray lines).

## 2. Bayesian Approaches

### 2.1. Laplace Prior (Bayesian Lasso)

**Laplace prior** = Bayesian equivalent of Lasso.

$$
\beta_j \sim \text{Laplace}(0, b)
$$

```python
import pymc as pm
import arviz as az

# Bayesian Lasso
with pm.Model() as bayesian_lasso:
    # Laplace priors
    alpha = pm.Normal('alpha', 0, 1)
    beta = pm.Laplace('beta', 0, 0.3, shape=p)  # Laplace!
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + pm.math.dot(X_z, beta)
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    trace_lasso = pm.sample(1000, tune=500, chains=2, random_seed=42,
                           return_inferencedata=True, progressbar=False)

# Extract coefficients
beta_lasso = trace_lasso.posterior['beta'].values.reshape(-1, p).mean(axis=0)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Coefficients
axes[0].bar(range(p), true_coef, alpha=0.5, label='True', edgecolor='black')
axes[0].bar(range(p), beta_lasso, alpha=0.7, label='Bayesian Lasso',
           edgecolor='black')
axes[0].axhline(0, color='red', linestyle='--', linewidth=2)
axes[0].set_xlabel('Feature Index', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
axes[0].set_title('BAYESIAN LASSO\n(Laplace Prior)',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')

# Posterior distributions (first 6 features)
beta_samples = trace_lasso.posterior['beta'].values.reshape(-1, p)
for i in range(6):
    axes[1].hist(beta_samples[:, i], bins=30, alpha=0.5, density=True,
                label=f'β{i}', edgecolor='black')
axes[1].axvline(0, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Coefficient Value', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('POSTERIOR DISTRIBUTIONS\nFirst 6 features',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=10)
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

### 2.2. Horseshoe Prior

**Horseshoe prior**: More flexible than Laplace.
- Allows large coefficients (heavy tails)
- Strong shrinkage for small coefficients

```python
# Horseshoe prior
with pm.Model() as horseshoe_model:
    alpha = pm.Normal('alpha', 0, 1)
    
    # Horseshoe prior
    tau = pm.HalfCauchy('tau', 1)  # Global shrinkage
    lambda_j = pm.HalfCauchy('lambda', 1, shape=p)  # Local shrinkage
    beta = pm.Normal('beta', 0, tau * lambda_j, shape=p)
    
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + pm.math.dot(X_z, beta)
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    trace_horseshoe = pm.sample(1000, tune=500, chains=2, random_state=42,
                               return_inferencedata=True, progressbar=False)

# Extract
beta_horseshoe = trace_horseshoe.posterior['beta'].values.reshape(-1, p).mean(axis=0)

# Compare all methods
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

methods = [
    ('True', true_coef, 'blue'),
    ('Lasso (Freq.)', lasso_cv.coef_, 'green'),
    ('Bayesian Lasso', beta_lasso, 'orange'),
    ('Horseshoe', beta_horseshoe, 'red')
]

for idx, (name, coef, color) in enumerate(methods):
    axes[idx//2, idx%2].bar(range(p), coef, alpha=0.7, color=color,
              edgecolor='black')
    axes[idx//2, idx%2].axhline(0, color='black', linestyle='--', linewidth=2)
    axes[idx//2, idx%2].set_xlabel('Feature Index', fontsize=12, fontweight='bold')
    axes[idx//2, idx%2].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
    axes[idx//2, idx%2].set_title(f'{name}\n' +
                                 f'Non-zero: {np.sum(np.abs(coef) > 0.1)}/{p}',
                                 fontsize=14, fontweight='bold')
    axes[idx//2, idx%2].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("FEATURE SELECTION COMPARISON")
print("=" * 70)
print(f"\nTrue non-zero: 5")
print(f"Lasso: {np.sum(np.abs(lasso_cv.coef_) > 0.1)} selected")
print(f"Bayesian Lasso: {np.sum(np.abs(beta_lasso) > 0.1)} selected")
print(f"Horseshoe: {np.sum(np.abs(beta_horseshoe) > 0.1)} selected")
print("=" * 70)
```

## 3. Posterior Inclusion Probabilities

**Bayesian advantage**: Quantify uncertainty about feature importance.

**Posterior Inclusion Probability (PIP)**: P(β_j ≠ 0 \mid data)

```python
# Compute PIPs
beta_samples_horseshoe = trace_horseshoe.posterior['beta'].values.reshape(-1, p)

# PIP = proportion of posterior samples where |β| > threshold
threshold = 0.1
pips = np.mean(np.abs(beta_samples_horseshoe) > threshold, axis=0)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# PIPs
axes[0].bar(range(p), pips, alpha=0.7, edgecolor='black')
axes[0].axhline(0.5, color='red', linestyle='--', linewidth=2,
               label='Threshold = 0.5')
axes[0].set_xlabel('Feature Index', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Posterior Inclusion Probability', fontsize=12, fontweight='bold')
axes[0].set_title('POSTERIOR INCLUSION PROBABILITIES\n' +
                 'P(|β| > 0.1 \\mid data)',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')
axes[0].set_ylim(0, 1)

# Coefficient vs PIP
beta_mean = beta_samples_horseshoe.mean(axis=0)
axes[1].scatter(beta_mean, pips, s=100, alpha=0.7, edgecolors='black')
for i in range(p):
    axes[1].text(beta_mean[i], pips[i], str(i), fontsize=9, ha='center', va='center')
axes[1].axhline(0.5, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[1].axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.7)
axes[1].set_xlabel('Mean Coefficient', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Posterior Inclusion Probability', fontsize=12, fontweight='bold')
axes[1].set_title('COEFFICIENT vs PIP\nLarge |β| → High PIP',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("FEATURES WITH HIGH PIP (> 0.5)")
print("=" * 70)
selected = np.where(pips > 0.5)[0]
print(f"\nSelected features: {selected}")
print(f"True relevant: [0, 1, 2, 3, 4]")
print("\n→ Bayesian approach quantifies uncertainty!")
print("=" * 70)
```

## 4. Khi nào Dùng Method Nào?

| Method | Pros | Cons | When to Use |
|--------|------|------|-------------|
| **Lasso** | Fast, sparse | No uncertainty | Large n, quick results |
| **Bayesian Lasso** | Uncertainty, flexible | Slower | Need uncertainty quantification |
| **Horseshoe** | Heavy tails, flexible | Complex | Strong sparsity assumption |
| **Spike-and-Slab** | Explicit selection | Very slow | Small p, explicit probabilities |

## Tóm tắt

Feature selection identifies relevant predictors:

- **Lasso**: L1 penalty → sparse solutions
- **Bayesian Lasso**: Laplace prior
- **Horseshoe**: Heavy-tailed prior → better for strong signals
- **PIPs**: Quantify uncertainty about feature importance

**Key insight**: Bayesian approaches provide **uncertainty quantification** about which features matter!

**Chapter 07 Complete!** Regularization, Bias-Variance, Feature Selection.

## Bài tập

**Bài tập 1**: Generate sparse data. Compare Lasso, Bayesian Lasso, Horseshoe. Which recovers true features best?

**Bài tập 2**: Compute PIPs. Threshold at 0.5, 0.7, 0.9. How does selection change?

**Bài tập 3**: Regularization path: Plot coefficients vs λ. Observe when features enter/exit.

**Bài tập 4**: Real high-dimensional data. Perform feature selection. Interpret selected features.

**Bài tập 5**: Compare computational time: Lasso vs Bayesian approaches. Trade-offs?

## Tài liệu Tham khảo

**Carvalho, C. M., et al. (2010).** "The horseshoe estimator for sparse signals." *Biometrika*, 97(2), 465-480.

**Piironen, J., & Vehtari, A. (2017).** "Sparsity information and regularization in the horseshoe and other shrinkage priors." *Electronic Journal of Statistics*, 11(2), 5018-5051.

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 11: Assumptions, diagnostics, and model evaluation

---

*Chương tiếp theo: [Chapter 08: Model Comparison](/vi/chapter08/)*
