---
layout: post
title: "Bài 6.1: Logistic Regression - Binary Outcomes"
chapter: '06'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter06
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu về **Logistic Regression** - một trong những models quan trọng nhất cho **binary outcomes** (yes/no, success/failure, 0/1). Bạn sẽ học tại sao linear regression không phù hợp cho binary data, cách sử dụng **link functions**, và cách interpret coefficients theo **odds ratios**. Đây là bước đầu vào **Generalized Linear Models (GLMs)**.

## Giới thiệu: Vấn đề của Linear Regression cho Binary Data

Giả sử chúng ta muốn predict:
- Có mua sản phẩm không? (yes/no)
- Có vượt qua kỳ thi không? (pass/fail)
- Có mắc bệnh không? (disease/healthy)

**Outcome**: $$y \in \{0, 1\}$$

**Câu hỏi**: Có thể dùng linear regression không?

$$
y = \alpha + \beta x + \epsilon
$$

**Vấn đề**: Linear regression có thể predict **bất kỳ giá trị nào** (-∞ đến +∞), nhưng probability phải trong **[0, 1]**!

## 1. Tại sao Linear Regression Không Hoạt động

![Logistic Regression Basics]({{ site.baseurl }}/img/chapter_img/chapter06/logistic_regression_basics.png)

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Generate binary data
np.random.seed(42)
n = 200
x = np.random.uniform(-3, 3, n)

# True probability (logistic function)
p_true = 1 / (1 + np.exp(-(1 + 0.8*x)))
y = np.random.binomial(1, p_true)

# Try linear regression
lr = LinearRegression().fit(x.reshape(-1, 1), y)
x_line = np.linspace(-4, 4, 100)
y_pred_linear = lr.predict(x_line.reshape(-1, 1))

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Linear regression (WRONG!)
axes[0].scatter(x, y, alpha=0.4, s=50, edgecolors='black', label='Data')
axes[0].plot(x_line, y_pred_linear, 'r-', linewidth=3, label='Linear Regression')
axes[0].axhline(0, color='green', linestyle='--', linewidth=2, alpha=0.7)
axes[0].axhline(1, color='green', linestyle='--', linewidth=2, alpha=0.7)
axes[0].fill_between(x_line, -0.5, 0, alpha=0.2, color='red', label='Invalid (<0)')
axes[0].fill_between(x_line, 1, 1.5, alpha=0.2, color='red', label='Invalid (>1)')
axes[0].set_xlabel('x', fontsize=12, fontweight='bold')
axes[0].set_ylabel('y', fontsize=12, fontweight='bold')
axes[0].set_title('LINEAR REGRESSION (WRONG!)\n' +
                 'Predictions outside [0,1]!',
                 fontsize=14, fontweight='bold', color='red')
axes[0].set_ylim(-0.5, 1.5)
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Logistic regression (CORRECT!)
p_logistic = 1 / (1 + np.exp(-(lr.intercept_ + lr.coef_[0]*x_line)))
axes[1].scatter(x, y, alpha=0.4, s=50, edgecolors='black', label='Data')
axes[1].plot(x_line, p_logistic, 'b-', linewidth=3, label='Logistic Regression')
axes[1].axhline(0, color='green', linestyle='--', linewidth=2, alpha=0.7)
axes[1].axhline(1, color='green', linestyle='--', linewidth=2, alpha=0.7)
axes[1].set_xlabel('x', fontsize=12, fontweight='bold')
axes[1].set_ylabel('P(y=1)', fontsize=12, fontweight='bold')
axes[1].set_title('LOGISTIC REGRESSION (CORRECT!)\n' +
                 'Predictions always in [0,1]',
                 fontsize=14, fontweight='bold', color='green')
axes[1].set_ylim(-0.1, 1.1)
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("=" * 70)
print("LINEAR vs LOGISTIC REGRESSION")
print("=" * 70)
print("\nLinear Regression:")
print(f"  Min prediction: {y_pred_linear.min():.2f} (< 0!)")
print(f"  Max prediction: {y_pred_linear.max():.2f} (> 1!)")
print("  → Invalid probabilities!")

print("\nLogistic Regression:")
print(f"  Min prediction: {p_logistic.min():.3f}")
print(f"  Max prediction: {p_logistic.max():.3f}")
print("  → Always in [0, 1] ✓")
print("=" * 70)
```

## 2. Logistic Regression: Generative Model

![Link Functions Comparison]({{ site.baseurl }}/img/chapter_img/chapter06/link_functions_comparison.png)

### 2.1. Link Function

**Idea**: Transform linear predictor để đảm bảo output trong [0, 1].

**Logit link function**:
$$
\text{logit}(p) = \log\left(\frac{p}{1-p}\right) = \alpha + \beta x
$$

**Inverse** (logistic function):
$$
p = \frac{1}{1 + e^{-(\alpha + \beta x)}} = \frac{e^{\alpha + \beta x}}{1 + e^{\alpha + \beta x}}
$$

### 2.2. Generative Story

1. **Linear predictor**: $$\eta = \alpha + \beta x$$
2. **Transform to probability**: $$p = \text{logistic}(\eta)$$
3. **Generate outcome**: $$y \sim \text{Bernoulli}(p)$$

```python
# Visualize logistic function
x_vals = np.linspace(-6, 6, 200)
p_vals = 1 / (1 + np.exp(-x_vals))

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Logistic function
axes[0].plot(x_vals, p_vals, 'b-', linewidth=3)
axes[0].axhline(0.5, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[0].axvline(0, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[0].set_xlabel('η = α + βx', fontsize=12, fontweight='bold')
axes[0].set_ylabel('p = P(y=1)', fontsize=12, fontweight='bold')
axes[0].set_title('LOGISTIC FUNCTION\n' +
                 'p = 1/(1+e⁻ᶯ)',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)
axes[0].text(0, 0.5, '  η=0 → p=0.5', fontsize=11, ha='left', va='bottom')

# Effect of α (intercept)
for alpha in [-2, 0, 2]:
    p = 1 / (1 + np.exp(-(alpha + x_vals)))
    axes[1].plot(x_vals, p, linewidth=2, label=f'α = {alpha}')
axes[1].set_xlabel('x', fontsize=12, fontweight='bold')
axes[1].set_ylabel('P(y=1)', fontsize=12, fontweight='bold')
axes[1].set_title('EFFECT OF α (Intercept)\n' +
                 'Shifts curve left/right',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

# Effect of β (slope)
for beta in [0.5, 1, 2]:
    p = 1 / (1 + np.exp(-(beta * x_vals)))
    axes[2].plot(x_vals, p, linewidth=2, label=f'β = {beta}')
axes[2].set_xlabel('x', fontsize=12, fontweight='bold')
axes[2].set_ylabel('P(y=1)', fontsize=12, fontweight='bold')
axes[2].set_title('EFFECT OF β (Slope)\n' +
                 'Steeper = stronger effect',
                 fontsize=14, fontweight='bold')
axes[2].legend(fontsize=11)
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## 3. Bayesian Logistic Regression trong PyMC

```python
import pymc as pm
import arviz as az

# Generate data
np.random.seed(42)
n = 200
x = np.random.uniform(-3, 3, n)
p_true = 1 / (1 + np.exp(-(1 + 0.8*x)))
y = np.random.binomial(1, p_true)

# Standardize
x_z = (x - x.mean()) / x.std()

# Bayesian logistic regression
with pm.Model() as logistic_model:
    # Priors
    alpha = pm.Normal('alpha', 0, 1.5)  # Weakly informative
    beta = pm.Normal('beta', 0, 1)
    
    # Linear predictor
    eta = alpha + beta * x_z
    
    # Logistic transformation
    p = pm.Deterministic('p', pm.math.invlogit(eta))
    
    # Likelihood
    y_obs = pm.Bernoulli('y_obs', p=p, observed=y)
    
    # Sample
    trace = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                              return_inferencedata=True)

# Summary
print("\n" + "=" * 70)
print("POSTERIOR SUMMARY")
print("=" * 70)
summary = az.summary(trace, var_names=['alpha', 'beta'])
print(summary)
print("=" * 70)

# Visualize posteriors
az.plot_posterior(trace, var_names=['alpha', 'beta'],
                 figsize=(14, 5), ref_val=[1, 0.8])
plt.suptitle('Posterior Distributions\n(True: α=1, β=0.8)',
            fontsize=14, fontweight='bold', y=1.05)
plt.tight_layout()
plt.show()

# Trace plots
az.plot_trace(trace, var_names=['alpha', 'beta'], compact=True,
             figsize=(14, 6))
plt.suptitle('Trace Plots (Check Convergence)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

## 4. Interpretation: Odds Ratios

### 4.1. Odds vs Probability

**Probability**: $$p = P(y=1)$$

**Odds**: $$\text{odds} = \frac{p}{1-p}$$

**Example**:
- p = 0.5 → odds = 1 (50-50 chance)
- p = 0.8 → odds = 4 (4 times more likely to be 1 than 0)
- p = 0.2 → odds = 0.25 (4 times more likely to be 0 than 1)

```python
# Visualize odds vs probability
p_range = np.linspace(0.01, 0.99, 100)
odds_range = p_range / (1 - p_range)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Probability to Odds
axes[0].plot(p_range, odds_range, 'b-', linewidth=3)
axes[0].axhline(1, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[0].axvline(0.5, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[0].set_xlabel('Probability (p)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Odds', fontsize=12, fontweight='bold')
axes[0].set_title('PROBABILITY → ODDS\n' +
                 'odds = p/(1-p)',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)
axes[0].set_ylim(0, 10)

# Key points
key_probs = [0.2, 0.5, 0.8]
for p_val in key_probs:
    odds_val = p_val / (1 - p_val)
    axes[0].scatter([p_val], [odds_val], s=150, zorder=5, edgecolors='black')
    axes[0].text(p_val, odds_val + 0.5, f'p={p_val:.1f}\nodds={odds_val:.2f}',
                ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

# Log-odds
log_odds_range = np.log(odds_range)
axes[1].plot(p_range, log_odds_range, 'g-', linewidth=3)
axes[1].axhline(0, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[1].axvline(0.5, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[1].set_xlabel('Probability (p)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Log-Odds', fontsize=12, fontweight='bold')
axes[1].set_title('PROBABILITY → LOG-ODDS\n' +
                 'log-odds = log(p/(1-p)) = α + βx',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

### 4.2. Interpreting β

**On log-odds scale**:
$$
\log\left(\frac{p}{1-p}\right) = \alpha + \beta x
$$

**Interpretation**: 1 unit increase in $$x$$ → $$\beta$$ increase in log-odds.

**On odds scale**:
$$
\text{odds} = e^{\alpha + \beta x}
$$

**Odds ratio**: 1 unit increase in $$x$$ → odds multiply by $$e^\beta$$.

```python
# Compute odds ratios
beta_samples = trace.posterior['beta'].values.flatten()
odds_ratio = np.exp(beta_samples)

print("\n" + "=" * 70)
print("ODDS RATIO INTERPRETATION")
print("=" * 70)
print(f"\nβ (log-odds scale): {beta_samples.mean():.3f}")
print(f"Odds Ratio (e^β): {odds_ratio.mean():.3f}")
print(f"95% CI: [{np.percentile(odds_ratio, 2.5):.3f}, " +
      f"{np.percentile(odds_ratio, 97.5):.3f}]")

print("\nInterpretation:")
print(f"  1 SD increase in x → odds multiply by {odds_ratio.mean():.2f}")
if odds_ratio.mean() > 1:
    print(f"  → {(odds_ratio.mean()-1)*100:.1f}% increase in odds")
else:
    print(f"  → {(1-odds_ratio.mean())*100:.1f}% decrease in odds")
print("=" * 70)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Beta (log-odds scale)
axes[0].hist(beta_samples, bins=50, density=True, alpha=0.7,
            color='skyblue', edgecolor='black')
axes[0].axvline(beta_samples.mean(), color='red', linewidth=3,
               label=f'Mean = {beta_samples.mean():.3f}')
axes[0].axvline(0, color='black', linestyle='--', linewidth=2)
axes[0].set_xlabel('β (log-odds scale)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('COEFFICIENT β\n(Log-Odds Scale)',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')

# Odds ratio
axes[1].hist(odds_ratio, bins=50, density=True, alpha=0.7,
            color='lightgreen', edgecolor='black')
axes[1].axvline(odds_ratio.mean(), color='red', linewidth=3,
               label=f'Mean = {odds_ratio.mean():.3f}')
axes[1].axvline(1, color='black', linestyle='--', linewidth=2)
axes[1].set_xlabel('Odds Ratio (e^β)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('ODDS RATIO\n(Multiplicative Effect)',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

## 5. Posterior Predictive Checks

```python
# Posterior predictive
with logistic_model:
    ppc = pm.sample_posterior_predictive(trace, random_seed=42)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Predicted probabilities
p_samples = trace.posterior['p'].values.reshape(-1, n)
p_mean = p_samples.mean(axis=0)
p_lower = np.percentile(p_samples, 2.5, axis=0)
p_upper = np.percentile(p_samples, 97.5, axis=0)

# Sort by x for plotting
sort_idx = np.argsort(x)
axes[0].scatter(x, y, alpha=0.3, s=30, label='Observed', edgecolors='black')
axes[0].plot(x[sort_idx], p_mean[sort_idx], 'r-', linewidth=3, label='Posterior mean')
axes[0].fill_between(x[sort_idx], p_lower[sort_idx], p_upper[sort_idx],
                     alpha=0.3, color='red', label='95% CI')
axes[0].set_xlabel('x', fontsize=12, fontweight='bold')
axes[0].set_ylabel('P(y=1)', fontsize=12, fontweight='bold')
axes[0].set_title('PREDICTED PROBABILITIES\nwith Uncertainty',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# PPC: Compare observed vs predicted
y_pred = ppc.posterior_predictive['y_obs'].values.reshape(-1, n)
y_pred_mean = y_pred.mean(axis=0)

axes[1].scatter(y, y_pred_mean, alpha=0.5, s=50, edgecolors='black')
axes[1].plot([0, 1], [0, 1], 'r--', linewidth=2, label='Perfect prediction')
axes[1].set_xlabel('Observed y', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Predicted P(y=1)', fontsize=12, fontweight='bold')
axes[1].set_title('POSTERIOR PREDICTIVE CHECK\nObserved vs Predicted',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## Tóm tắt

Logistic regression cho binary outcomes:

- **Problem**: Linear regression predicts outside [0,1]
- **Solution**: Logit link function
- **Model**: $$\log(p/(1-p)) = \alpha + \beta x$$
- **Interpretation**: Odds ratios ($$e^\beta$$)
- **PyMC**: `pm.Bernoulli` với `pm.math.invlogit`

**Key insight**: GLMs = Linear models + Link functions → handle non-normal outcomes!

Bài tiếp theo: **Poisson Regression** cho count data.

## Bài tập

**Bài tập 1**: Generate binary data. Fit logistic regression. Interpret odds ratio.

**Bài tập 2**: Compare predictions của linear vs logistic regression. Visualize differences.

**Bài tập 3**: Multiple predictors logistic regression. Interpret each coefficient.

**Bài tập 4**: Real data - predict customer churn (0/1) từ usage features.

**Bài tập 5**: Posterior predictive checks. Compute accuracy, sensitivity, specificity.

## Tài liệu Tham khảo

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.
- Chapter 5: Logistic regression

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 10: Big Entropy and the Generalized Linear Model

---

*Bài học tiếp theo: [6.2 Poisson Regression](/vi/chapter06/poisson-regression/)*
