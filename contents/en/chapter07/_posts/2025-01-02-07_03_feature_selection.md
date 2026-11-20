---
layout: post
title: "Lesson 7.3: Feature Selection - Choosing Important Predictors"
chapter: '07'
order: 3
owner: Nguyen Le Linh
lang: en
categories:
- chapter07
lesson_type: required
---

## Learning objectives

After completing this lesson, you will understand **feature selection** as the problem of determining which predictors truly matter when we have a very large number of candidates. The lesson goes through Bayesian approaches such as Laplace priors, spike-and-slab, and horseshoe priors, while comparing them with familiar frequentist methods such as Lasso or stepwise procedures. The goal is not only to know which tools exist, but to understand what assumption about the sparsity of the model each tool encodes, and when each approach is more reasonable in a high-dimensional data setting.

## Introduction: The Problem of Many Predictors

Consider the situation where you have 100 **potential predictors** but only about 5 of them truly carry signal. If you keep all the variables, the model easily overfits; if you try every possible combination, the computational cost explodes because the number of models to consider reaches $$2^{100}$$; and if you test each variable individually, you face the risk of **false discoveries** due to multiple testing. Therefore, the goal of feature selection is not simply to “make the model more compact”, but to identify in a principled way the variables that are truly relevant while still controlling uncertainty and modeling cost.

## 1. Frequentist Approaches

### 1.1. Lasso (L1 Regularization)

**Lasso** sets some coefficients **exactly to 0** → automatic feature selection.

![Lasso Feature Selection]({{ site.baseurl }}/img/chapter_img/chapter07/lasso_feature_selection.png)

The example in the figure uses a dataset with 20 features, of which only the first 5 have truly nonzero coefficients. When $$\alpha$$ is still very small, such as 0.001 or 0.01, regularization is too weak so the model still keeps about 13 features, meaning many noise variables slip into the model. When it rises to a moderate level such as 0.1, the coefficients begin to shrink more strongly toward 0 but the number of retained variables is still fairly large. Only when $$\alpha$$ is strong enough, for example 0.5, do we clearly see the sparser effect: many coefficients are pushed to 0 and the number of selected features drops. The direct lesson from this example is that Lasso performs feature selection by forcing some coefficients to exactly 0, and the level of **sparsity** increases as regularization gets stronger.

### 1.2. Cross-Validation to Choose α

![Lasso CV and Regularization Path]({{ site.baseurl }}/img/chapter_img/chapter07/lasso_cv_regularization_path.png)

The cross-validation result in this example chooses $$\alpha=1.0$$ as the best regularization level by out-of-sample predictive ability. At that level, the model keeps 7 features, slightly more than the 5 truly relevant features, but still fairly close to the true sparse structure of the data. The regularization path in the right panel adds a very important intuition: when $$\alpha$$ is small, most coefficients are nonzero and have considerable magnitude; as $$\alpha$$ increases, the coefficients shrink to 0 at different rates; and the features carrying real signal usually “hold on” longer than the noise variables. So cross-validation not only helps choose the optimal level of regularization but also gives us a dynamic view of how each variable leaves the model.

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

The **Horseshoe prior** is more flexible than the Laplace prior because it both allows some truly large coefficients to survive thanks to its heavy tails, and shrinks small coefficients very strongly toward 0. This ability to both “spare” strong signals and strongly “penalize” weak noise makes the horseshoe an especially attractive prior in sparse-signal problems.

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

### Experiment: how Gaussian, Laplace and Horseshoe shrink differently

50 coefficients, only 5 large: compare the posterior mean of each prior and the shrinkage curve.

<div class="interactive-demo" markdown="1">
<div data-demo="horseshoe-explainer" data-lang="en"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 3. Posterior Inclusion Probabilities

An important advantage of the Bayesian approach is that it does not only produce a list of selected variables, but also quantifies the uncertainty of the selection process itself. The **Posterior Inclusion Probability (PIP)** is understood as the posterior probability that a coefficient is different enough from 0 under a practical criterion, and thanks to this it lets us talk about the degree of certainty of variable importance, instead of only saying “selected” or “not selected”.

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

## 4. Applied Case Study (Phan 3): Stability selection + interpretation risk

In real problems, a feature being selected once is not enough to conclude that it is important. We need to check the **stability of feature selection** over many resamplings.

```python
import numpy as np

def ridge_fit(X, y, lam):
    p = X.shape[1]
    eye = np.eye(p)
    return np.linalg.solve(X.T @ X + lam * eye, X.T @ y)

def bootstrap_stability(X, y, lam, n_boot=200, threshold=0.15, seed=42):
    rng = np.random.default_rng(seed)
    n, p = X.shape
    picks = np.zeros((n_boot, p), dtype=int)

    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        Xb, yb = X[idx], y[idx]
        beta_b = ridge_fit(Xb, yb, lam)
        picks[b] = (np.abs(beta_b) > threshold).astype(int)

    return picks.mean(axis=0)  # selection frequency

stability = bootstrap_stability(X_train_z, y_train_z, best_lambda)

# Simple rule: choose variables with selection frequency >= 0.7
stable_features = np.where(stability >= 0.7)[0]
print("Stable features (freq >= 0.7):", stable_features)
```

### 4.1. Uncertainty-aware thresholds

Instead of a single fixed threshold, report results at several levels:

- **Hot (>= 0.9)**: very strong evidence, safe to put into the main interpretive model.
- **Warm (0.7 - 0.9)**: fairly stable, needs cross-checking with domain knowledge.
- **Weak (< 0.7)**: not yet stable, treat as a backup feature.

With Bayesian models, you can also add a PIP threshold (for example PIP >= 0.8) to report selection uncertainty transparently.

### 4.2. Interpretation risks in machine learning

Even when a feature is selected stably, interpretation still carries risks:

1. **Collinearity**: a selected feature may be a representative of a cluster of correlated variables, not necessarily a direct cause.
2. **Proxy bias**: a feature may act as a proxy for a sensitive attribute.
3. **Data drift**: the selection frequency may change over time as the data distribution changes.
4. **Actionability gap**: a feature that is important for prediction is not necessarily useful for operational decisions.

**Decision checkpoint 3 (end of the case study)**:
- Report jointly: out-of-sample performance + uncertainty (PIP/stability) + interpretation warnings.
- Only lock the list of "actionable" features after passing the 3 layers of checks above.

If you want to reproduce the whole case study presented throughout 7.1 -> 7.3, you can run the script:

`python img/chapter_img/chapter07/generate_applied_ml_workflow_tradeoffs.py`

## 5. When to Use Which Method?

| Method | Pros | Cons | When to Use |
|--------|------|------|-------------|
| **Lasso** | Fast, sparse | No uncertainty | Large n, quick results |
| **Bayesian Lasso** | Uncertainty, flexible | Slower | Need uncertainty quantification |
| **Horseshoe** | Heavy tails, flexible | Complex | Strong sparsity assumption |
| **Spike-and-Slab** | Explicit selection | Very slow | Small p, explicit probabilities |

## Summary

Feature selection is the problem of choosing the predictors that are truly relevant when the number of candidate variables is large and the risk of overfitting is present. Lasso solves this problem by using an L1 penalty to produce a sparse solution, Bayesian Lasso interprets the same idea through a Laplace prior, and the horseshoe prior brings a more refined shrinkage mechanism, especially useful when we believe that only a few strong signals stand out among a great many weak variables. More importantly, the Bayesian approach also provides **uncertainty quantification** for the variable choice itself, for example through Posterior Inclusion Probabilities, instead of merely returning a list of seemingly optimal variables.

The most important point of the lesson is that variable selection should not be understood as a mechanical filtering operation, but as part of the process of inferring the structure of the signal in the data.

**Chapter 07 Complete!** Regularization, Bias-Variance, Feature Selection.

## Reference videos

- [Regularization Part 2: Lasso (L1) Regression](https://www.youtube.com/watch?v=NGf0voTMlcs) — StatQuest with Josh Starmer, English. **watch first**. Watch L1 be able to set some coefficients exactly to zero, exactly the variable-selection direction the lesson contrasts with searching all combinations.
- [Lecture 31 Bayesian Regression and Variable Selection (Part A)](https://www.youtube.com/watch?v=Mv6MSIVKEIc) — Nicholas Zabaras, English. Watch Bayesian regression and variable selection in one lecture, supporting the shrinkage priors on coefficients when there are too many predictors.
- [Regularized Horseshoe - Aki Vehtari](https://www.youtube.com/watch?v=EuhvfvY8ISc) — Stan, English. Watch the regularized horseshoe, used for the part of the lesson on sparse priors on coefficients rather than just a lasso-style penalty.

## Exercises

**Exercise 1**: Generate sparse data. Compare Lasso, Bayesian Lasso, Horseshoe. Which recovers true features best?

**Exercise 2**: Compute PIPs. Threshold at 0.5, 0.7, 0.9. How does selection change?

**Exercise 3**: Regularization path: Plot coefficients vs λ. Observe when features enter/exit.

**Exercise 4**: Real high-dimensional data. Perform feature selection. Interpret selected features.

**Exercise 5**: Compare computational time: Lasso vs Bayesian approaches. Trade-offs?

## References

**Carvalho, C. M., et al. (2010).** "The horseshoe estimator for sparse signals." *Biometrika*, 97(2), 465-480.

**Piironen, J., & Vehtari, A. (2017).** "Sparsity information and regularization in the horseshoe and other shrinkage priors." *Electronic Journal of Statistics*, 11(2), 5018-5051.

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 11: Assumptions, diagnostics, and model evaluation

---

*Next chapter: [Chapter 08: Model Comparison]({{ site.baseurl }}/contents/en/chapter08/)*
