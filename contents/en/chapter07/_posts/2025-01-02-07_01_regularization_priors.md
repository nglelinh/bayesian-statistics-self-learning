---
layout: post
title: "Lesson 7.1: Regularization with Priors - Preventing Overfitting"
chapter: '07'
order: 1
owner: Nguyen Le Linh
lang: en
categories:
- chapter07
lesson_type: required
---

## Learning objectives

After completing this lesson, you will understand **regularization** as a core mechanism for preventing **overfitting**. The lesson clarifies why priors in Bayesian statistics perform regularization naturally, how they relate to Ridge regression and Lasso regression in frequentist language, and in which situations we truly need regularization rather than simply adding complexity to the model. This is an essential skill when modeling with many **predictors**, especially in problems where the number of variables exceeds what our intuition can control by eye.

## Introduction: The overfitting problem

Imagine you have only 20 data points but want to fit a polynomial regression. A question that seems technical, such as whether to choose degree 1, degree 10, or degree 15, actually leads straight to a very fundamental problem of modern statistics. If the model is too simple, it will **underfit** and miss important structure; but if the model is too flexible, it can cling tightly even to the random fluctuations of the training data. The model then learns **noise** instead of **signal**, and although it seems very good on the training data, it predicts poorly on new data. That is exactly the phenomenon of overfitting.

## 1. Demonstrating Overfitting

![Overfitting Demonstration]({{ site.baseurl }}/img/chapter_img/chapter07/overfitting_demonstration.png)

The figure shows the logic of the problem very clearly. With a degree-1 polynomial, the model is too simple, so both the training error and the test error are high; this is the classic underfit state. With degree 3, the model is flexible enough to capture the main trend of the data without starting to memorize noise, so both the training error and the test error are lower. When we increase to degree 10, we begin to see a model that looks very good on the training data but has a high test error, because it has “memorized” random fluctuations that do not repeat in new data. By degree 15, the phenomenon becomes more extreme: the model almost completely loses its ability to **generalize**. The important point to keep is that the test error usually rises again when the model is too complex, and that is exactly when regularization becomes necessary.

## 2. Regularization: The Solution

The core idea of regularization is not to let the model freely use coefficients that are too large just to follow the training data closely. In other words, we add a mechanism that prefers simpler models by penalizing overly extreme coefficient configurations.

### 2.1. Ridge Regression (L2 Regularization)

**Objective**:
$$
\min_{\beta} \sum_{i=1}^n (y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^p \beta_j^2
$$

In this expression, the first term forces the model to fit the data, while the second term penalizes the sum of squares of the coefficients to keep them at a moderate scale. The parameter $$\lambda$$ controls the strength of the penalty; the larger $$\lambda$$ is, the stronger the regularization and the more the model is pushed toward “gentler” solutions.

From a Bayesian viewpoint, Ridge regression can be understood as placing a **Normal prior** on the coefficients.

$$
\beta_j \sim \text{Normal}(0, \sigma^2)
$$

### 2.2. Lasso Regression (L1 Regularization)

**Objective**:
$$
\min_{\beta} \sum_{i=1}^n (y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^p |\beta_j|
$$

In Bayesian language, Lasso corresponds to placing a **Laplace prior** on the coefficients.

$$
\beta_j \sim \text{Laplace}(0, b)
$$

![Regularization Priors]({{ site.baseurl }}/img/chapter_img/chapter07/regularization_priors.png)

The comparison figure of priors shows that regularization in Bayesian statistics is actually a very concrete modeling choice, not a trick added afterwards. The **Normal prior** in the left panel is centered at 0 and has smooth tails, so it tends to pull coefficients toward 0 but rarely forces them to be exactly 0; this kind of prior is appropriate when we believe that many predictors each have a small effect. The **Laplace prior** in the middle panel is sharper at 0 and has heavier tails, so it encourages **sparsity**, meaning many coefficients are pushed more strongly to 0; it is therefore especially useful for **feature selection**. The comparison panel on the right emphasizes that choosing a prior is really choosing a “regularization philosophy”: a flat prior barely regularizes, while Normal and Laplace encode different degrees and kinds of shrinkage.

### Experiment: a normal prior shrinks the coefficients (ridge)

Decrease τ step by step: the curve gradually smooths, and the test error falls and then rises.

<div class="interactive-demo" markdown="1">
<div data-demo="shrink-explainer" data-lang="en"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 3. Bayesian Regularization in PyMC

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

One of the most practical questions is how strongly to regularize, or in Bayesian language, how narrow the prior should be so as to control overfitting without suffocating the real signal.

### 4.1. Cross-Validation

A pragmatic approach is to use cross-validation to choose the prior scale so that the out-of-sample predictive ability is best.

### 4.2. Prior Predictive Checks

An approach with a more Bayesian spirit is to use **prior predictive checks** to see whether the current prior generates reasonable predictions, even before looking at the data.

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

### 4.3. Checklist for choosing prior strength in an ML workflow

In real machine learning practice, prior strength (or regularization strength) should be chosen following a clear procedure rather than random experimentation:

1. **Define prediction target + metric**: determine the metric appropriate to the problem (RMSE, MAE, log-loss, calibration...).
2. **Split data from the start**: separate train/validation/test before tuning any parameter.
3. **Fit preprocessing on train only**: standardization, imputation, and encoding must be learned on train and applied to validation/test to avoid leakage.
4. **Tune prior scale on validation**: sweep a grid of reasonable prior scales and compare out-of-sample performance.
5. **Check the prior predictive**: eliminate priors that generate absurd predictions before looking at detailed fit results.
6. **Lock the model on test once**: evaluate on test only at the final step to preserve objectivity.

The checklist above connects Bayes directly to the ML training workflow: the prior is not just a "theory" part, but a hyperparameter with modeling meaning.

## 5. Applied Case Study (Part 1): Setup, split, and leakage control

We use a simulated high-dimensional regression problem: predicting a continuous value from 25 predictors, of which only a few truly carry signal. The goal of Part 1 is to build the data pipeline correctly.

```python
import numpy as np

rng = np.random.default_rng(42)
n, p = 180, 25

# Sparse ground truth: only 6 variables have signal
beta_true = np.zeros(p)
beta_true[:6] = np.array([2.4, -1.8, 1.2, 0.9, -0.7, 0.5])

X = rng.normal(0, 1, size=(n, p))
y = 1.5 + X @ beta_true + rng.normal(0, 1.2, size=n)

# 60/20/20 split
idx = rng.permutation(n)
train_idx = idx[: int(0.6 * n)]
val_idx = idx[int(0.6 * n): int(0.8 * n)]
test_idx = idx[int(0.8 * n):]

X_train, y_train = X[train_idx], y[train_idx]
X_val, y_val = X[val_idx], y[val_idx]
X_test, y_test = X[test_idx], y[test_idx]

# Preprocessing fit on train only (anti-leakage)
mu_x = X_train.mean(axis=0)
sd_x = X_train.std(axis=0)
sd_x[sd_x == 0] = 1.0

X_train_z = (X_train - mu_x) / sd_x
X_val_z = (X_val - mu_x) / sd_x
X_test_z = (X_test - mu_x) / sd_x

mu_y = y_train.mean()
sd_y = y_train.std() if y_train.std() > 0 else 1.0

y_train_z = (y_train - mu_y) / sd_y
y_val_z = (y_val - mu_y) / sd_y
y_test_z = (y_test - mu_y) / sd_y
```

**Decision checkpoint 1**:
- If the data has been split and scaled with a train-only procedure, you can start tuning the prior/regularization.
- If preprocessing was fit on the full data before the split, the validation results will be falsely optimistic because of leakage.

## 6. When is Regularization Needed?

Regularization is especially necessary when the number of predictors is large relative to the sample size, when predictors are strongly correlated with each other causing **multicollinearity**, when data is scarce so the model easily swings strongly from sample to sample, or when our goal is to find a sparse solution that keeps only a few important variables. Conversely, if the number of predictors is small, the sample is large, the variables are nearly independent of each other, and we have strong theoretical grounds to keep all variables in the model, regularization can play a more secondary role. The key point is that regularization is not always a “tonic”; it is a deliberate response to the risk that the model is too flexible relative to the amount of information the data actually provides.

## Summary

Regularization prevents overfitting by controlling the scale of the coefficients instead of letting the model freely chase every fluctuation of the training data. Ridge regression can be understood as placing a Normal prior to shrink all coefficients toward 0, while Lasso corresponds to a Laplace prior and encourages a sparser solution. From the Bayesian viewpoint, regularization is not an auxiliary part outside the model, but precisely the consequence of choosing priors that match our degree of belief about the size and structure of the coefficients. The strength of regularization can be tuned by cross-validation or by prior predictive checks, depending on the analysis goal.

The most important point of the lesson is to recognize that in Bayesian statistics, saying “regularize” is essentially saying “choose the prior responsibly”.

Next lesson: **Bias-Variance Tradeoff** (going deeper into validation strategy and model-complexity tuning within the same case study).

## Reference videos

- [Regularization Part 1: Ridge (L2) Regression](https://www.youtube.com/watch?v=Q81RR3yKn30) — StatQuest with Josh Starmer, English. **watch first**. Watch the L2 penalty pull coefficients toward zero to reduce variance, exactly the overfitting phenomenon the lesson opens with using a high-degree polynomial.
- [Ridge Regression is a Gaussian Prior](https://www.youtube.com/watch?v=W_SjooqeOqM) — DataMListic, English. Watch ridge as a normal prior on the coefficients, supporting the claim that a Bayesian prior is regularization.
- [Lasso Regression is a Laplace Prior](https://www.youtube.com/watch?v=8-_hZD0BRK8) — DataMListic, English. Watch lasso correspond to a Laplace prior, used for the part of the lesson comparing ways of shrinking coefficients.

## Exercises

**Exercise 1**: Generate high-dimensional data (p > n). Fit with weak and strong priors. Compare.

**Exercise 2**: Implement Lasso prior (Laplace) in PyMC. Compare with Ridge.

**Exercise 3**: Use cross-validation to choose optimal prior scale.

**Exercise 4**: Prior predictive checks with different prior scales. Which is reasonable?

**Exercise 5**: Real data with many predictors. Apply regularization and interpret results.

## References

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 12: Transformations and regression

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 4: Geocentric Models (Priors as regularization)

---

*Next lesson: [7.2 Bias-Variance Tradeoff]({{ site.baseurl }}/contents/en/chapter07/07_02_bias_variance_tradeoff/)*
