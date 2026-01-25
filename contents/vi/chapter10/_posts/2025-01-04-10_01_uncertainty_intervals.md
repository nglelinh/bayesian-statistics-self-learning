---
layout: post
title: "Bài 10.1: Communicating Uncertainty - Credible Intervals & Predictions"
chapter: '10'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter10
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu sâu về **uncertainty quantification** trong Bayesian statistics - một trong những strengths lớn nhất của Bayesian approach. Bạn sẽ phân biệt rõ ràng giữa credible intervals (parameter uncertainty) và prediction intervals (data uncertainty), hiểu sự khác biệt giữa Bayesian credible intervals và frequentist confidence intervals, và biết cách communicate uncertainty một cách chính xác và honest.

## Giới thiệu: Tại sao Uncertainty Matters?

### Câu chuyện Động lực

Bạn là data scientist cho một công ty y tế. Bạn vừa fit một Bayesian regression model để predict **recovery time** (ngày) dựa trên **treatment dose** (mg). Model của bạn cho kết quả:

> "With dose = 100mg, predicted recovery time = 14.2 days"

**CEO hỏi**: "14.2 days chính xác chứ? Tôi có thể hứa với khách hàng không?"

**Câu trả lời sai**: "Vâng, chính xác 14.2 days."

**Câu trả lời đúng**: "Best estimate là 14.2 days, nhưng có uncertainty:
- **Parameter uncertainty**: True effect có thể từ 13.5 đến 14.9 days (95% credible)
- **Prediction uncertainty**: Individual patient có thể recover từ 9 đến 19 days (95% prediction interval)
- Nếu CEO cần guarantee, nên dùng upper bound: 19 days."

**Key lesson**: Reporting point estimates without uncertainty là **misleading và nguy hiểm**. Bayesian statistics excels at quantifying uncertainty!

## 1. Two Fundamental Types of Uncertainty

Trong Bayesian inference, có **hai loại uncertainty** fundamentally different:

### 1.1. Epistemic Uncertainty (Parameter Uncertainty)

**Definition**: Uncertainty về **true value của parameters** do limited data.

**Characteristics**:
- **Reducible**: More data → less uncertainty
- **Captured by posterior**: $$p(\theta \mid y)$$
- **Quantified by credible intervals**

**Example**: "What is the true effect of treatment?"
- With 10 patients: $$\beta \in [0.3, 0.9]$$ (95% CI)
- With 1000 patients: $$\beta \in [0.55, 0.65]$$ (95% CI) → narrower!

### 1.2. Aleatoric Uncertainty (Data Uncertainty)

**Definition**: Inherent **randomness in data** that cannot be reduced.

**Characteristics**:
- **Irreducible**: More data doesn't reduce it
- **Captured by likelihood**: $$p(y \mid \theta)$$
- **Quantified by prediction intervals**

**Example**: "Where will next patient's recovery time be?"
- Even with perfect knowledge of $$\beta$$, individual outcomes vary due to $$\sigma$$
- Prediction interval includes both parameter uncertainty AND data noise

### 1.3. Visualize The Difference

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az

# Generate data: Simple regression
np.random.seed(42)
n = 50
x = np.random.uniform(0, 10, n)
true_alpha = 2.0
true_beta = 0.5
true_sigma = 2.0
y = true_alpha + true_beta * x + np.random.normal(0, true_sigma, n)

# Fit Bayesian regression
with pm.Model() as model:
    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=5)
    
    # Likelihood
    mu = alpha + beta * x
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
    
    # Sample posterior
    trace = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                     return_inferencedata=True, target_accept=0.95)
    
    # Posterior predictive
    trace.extend(pm.sample_posterior_predictive(trace, random_seed=42))

print("=" * 70)
print("BAYESIAN REGRESSION: UNCERTAINTY QUANTIFICATION")
print("=" * 70)
print(f"\nData: n = {n} observations")
print(f"True parameters: α = {true_alpha}, β = {true_beta}, σ = {true_sigma}")
print("\nPosterior estimates:")
print(az.summary(trace, var_names=['alpha', 'beta', 'sigma']))
print("=" * 70)
```

## 2. Credible Intervals - Parameter Uncertainty

### 2.1. Definition và Interpretation

**Credible Interval (CI)**: Range containing parameter with specified probability.

**Mathematical definition**:
$$
P(\theta \in [\theta_L, \theta_U] \mid y) = 1 - \alpha
$$

**95% Credible Interval**: $$P(\theta \in [\theta_L, \theta_U] \mid y) = 0.95$$

**Bayesian interpretation** (CORRECT):
> "Given the observed data, there is a 95% probability that $$\theta$$ lies in this interval."

**Contrast with frequentist confidence interval** (common misinterpretation):
> ❌ "If we repeat experiment many times, 95% of intervals will contain true $$\theta$$"
> ✅ Bayesian CI: Direct probability statement about $$\theta$$

### 2.2. Two Types of Credible Intervals

**Equal-Tailed Interval (ETI)**: Equal probability in both tails.
$$
P(\theta < \theta_L \mid y) = P(\theta > \theta_U \mid y) = \frac{\alpha}{2}
$$

**Highest Density Interval (HDI)**: Shortest interval containing $$(1-\alpha)$$ probability.
- All points inside HDI have higher density than points outside
- Preferred for skewed distributions

```python
# Extract posterior samples
alpha_post = trace.posterior['alpha'].values.flatten()
beta_post = trace.posterior['beta'].values.flatten()
sigma_post = trace.posterior['sigma'].values.flatten()

# Compute credible intervals
print("\n" + "=" * 70)
print("CREDIBLE INTERVALS (Parameter Uncertainty)")
print("=" * 70)

for name, samples in [('α (intercept)', alpha_post), 
                      ('β (slope)', beta_post), 
                      ('σ (noise)', sigma_post)]:
    # ETI (Equal-Tailed Interval)
    eti_94 = np.percentile(samples, [3, 97])  # 94% ETI
    
    # HDI (Highest Density Interval)
    hdi_94 = az.hdi(samples, hdi_prob=0.94)
    
    print(f"\n{name}:")
    print(f"  Posterior mean: {samples.mean():.3f}")
    print(f"  Posterior SD: {samples.std():.3f}")
    print(f"  94% ETI: [{eti_94[0]:.3f}, {eti_94[1]:.3f}]")
    print(f"  94% HDI: [{hdi_94[0]:.3f}, {hdi_94[1]:.3f}]")
    print(f"  → Interpretation: 94% probability that {name} is in this range")

print("\n✅ KEY INSIGHT:")
print("   • Credible intervals quantify PARAMETER uncertainty")
print("   • More data → narrower intervals")
print("   • Direct probability interpretation (Bayesian advantage!)")
print("=" * 70)
```

### 2.3. Visualize Credible Intervals

```python
# Visualize posterior distributions with credible intervals
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

params = [('α', alpha_post, true_alpha), 
          ('β', beta_post, true_beta), 
          ('σ', sigma_post, true_sigma)]

for ax, (name, samples, true_val) in zip(axes, params):
    # Histogram
    ax.hist(samples, bins=50, alpha=0.7, edgecolor='black', 
           density=True, color='steelblue')
    
    # HDI
    hdi = az.hdi(samples, hdi_prob=0.94)
    ax.axvline(hdi[0], color='blue', linestyle='--', linewidth=2.5, alpha=0.7)
    ax.axvline(hdi[1], color='blue', linestyle='--', linewidth=2.5, alpha=0.7,
              label=f'94% HDI: [{hdi[0]:.2f}, {hdi[1]:.2f}]')
    
    # Mean
    ax.axvline(samples.mean(), color='red', linestyle='-', linewidth=2.5,
              label=f'Mean: {samples.mean():.2f}')
    
    # True value
    ax.axvline(true_val, color='green', linestyle=':', linewidth=2.5,
              label=f'True: {true_val:.2f}')
    
    ax.set_xlabel(name, fontsize=14, fontweight='bold')
    ax.set_ylabel('Posterior Density', fontsize=13, fontweight='bold')
    ax.set_title(f'Posterior for {name}', fontsize=15, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('credible_intervals.png', dpi=150, bbox_inches='tight')
plt.show()
```

## 3. Prediction Intervals - Data Uncertainty

### 3.1. Posterior Predictive Distribution

**Question**: Where will **new observation** $$\tilde{y}$$ be?

**Posterior predictive distribution**:
$$
p(\tilde{y} | y) = \int p(\tilde{y} | \theta) p(\theta | y) d\theta
$$

**Interpretation**:
- Average over **all plausible parameter values** (weighted by posterior)
- Includes **both** parameter uncertainty AND data noise

**Prediction interval**: Range containing new observation with specified probability.

### 3.2. Compute Prediction Intervals

```python
# Posterior predictive samples (already computed)
y_pred = trace.posterior_predictive['y_obs'].values.reshape(-1, n)

# For a new x value
x_new = 5.0
alpha_samples = trace.posterior['alpha'].values.flatten()
beta_samples = trace.posterior['beta'].values.flatten()
sigma_samples = trace.posterior['sigma'].values.flatten()

# Generate predictions for x_new
n_samples = len(alpha_samples)
y_new_pred = np.zeros(n_samples)
for i in range(n_samples):
    mu_i = alpha_samples[i] + beta_samples[i] * x_new
    y_new_pred[i] = np.random.normal(mu_i, sigma_samples[i])

# Prediction interval
pred_interval_94 = np.percentile(y_new_pred, [3, 97])

print("\n" + "=" * 70)
print("PREDICTION INTERVAL (Data Uncertainty)")
print("=" * 70)
print(f"\nFor new observation at x = {x_new}:")
print(f"  Predicted mean: {y_new_pred.mean():.2f}")
print(f"  94% Prediction Interval: [{pred_interval_94[0]:.2f}, {pred_interval_94[1]:.2f}]")
print(f"\n→ Interpretation: 94% probability that NEW observation will be in this range")
print(f"→ Much WIDER than credible interval (includes data noise σ)")
print("=" * 70)
```

### 3.3. Visualize: Credible vs Prediction Intervals

```python
# Generate predictions for range of x values
x_range = np.linspace(0, 10, 100)
n_draws = 200

# Storage
mu_draws = np.zeros((n_draws, len(x_range)))
y_draws = np.zeros((n_draws, len(x_range)))

for i in range(n_draws):
    idx = np.random.randint(len(alpha_post))
    alpha_i = alpha_post[idx]
    beta_i = beta_post[idx]
    sigma_i = sigma_post[idx]
    
    # Mean function (credible)
    mu_draws[i, :] = alpha_i + beta_i * x_range
    
    # Predictions (includes noise)
    y_draws[i, :] = mu_draws[i, :] + np.random.normal(0, sigma_i, len(x_range))

# Compute intervals
mu_mean = mu_draws.mean(axis=0)
mu_hdi_low = np.percentile(mu_draws, 3, axis=0)
mu_hdi_high = np.percentile(mu_draws, 97, axis=0)

y_pred_low = np.percentile(y_draws, 3, axis=0)
y_pred_high = np.percentile(y_draws, 97, axis=0)

# Plot
fig, ax = plt.subplots(figsize=(14, 8))

# Data
ax.scatter(x, y, s=80, alpha=0.6, edgecolors='black', linewidths=1,
          label='Observed data', zorder=5, color='black')

# Mean regression line
ax.plot(x_range, mu_mean, 'r-', linewidth=3, label='Posterior mean', zorder=4)

# Credible interval (parameter uncertainty)
ax.fill_between(x_range, mu_hdi_low, mu_hdi_high, alpha=0.4, color='blue',
               label='94% Credible Interval (parameter uncertainty)', zorder=2)

# Prediction interval (data uncertainty)
ax.fill_between(x_range, y_pred_low, y_pred_high, alpha=0.2, color='green',
               label='94% Prediction Interval (data uncertainty)', zorder=1)

ax.set_xlabel('x', fontsize=14, fontweight='bold')
ax.set_ylabel('y', fontsize=14, fontweight='bold')
ax.set_title('CREDIBLE vs PREDICTION INTERVALS\n' +
            'Blue = Where is the mean? | Green = Where will new data be?',
            fontsize=16, fontweight='bold')
ax.legend(fontsize=12, loc='upper left')
ax.grid(alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('credible_vs_prediction.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n" + "=" * 70)
print("KEY DIFFERENCES")
print("=" * 70)
print("\n1. CREDIBLE INTERVAL (Blue):")
print("   • Uncertainty about MEAN function μ(x) = α + βx")
print("   • Answers: 'Where is the true regression line?'")
print("   • Narrower (only parameter uncertainty)")
print("   • Gets narrower with more data")

print("\n2. PREDICTION INTERVAL (Green):")
print("   • Uncertainty about NEW OBSERVATION ỹ")
print("   • Answers: 'Where will next data point be?'")
print("   • Wider (parameter uncertainty + data noise σ)")
print("   • Width limited by irreducible noise σ")
print("=" * 70)
```

## 4. Bayesian vs Frequentist: Philosophical Difference

### 4.1. Interpretation Comparison

**Bayesian Credible Interval** (95%):
> ✅ "Given the data, there is a 95% probability that θ is in [a, b]"
- Direct probability statement
- Conditional on observed data
- Intuitive interpretation

**Frequentist Confidence Interval** (95%):
> ❌ (Common misinterpretation): "95% probability θ is in [a, b]"
> ✅ (Correct): "If we repeat experiment infinitely, 95% of intervals will contain θ"
- Long-run frequency interpretation
- θ is fixed, interval is random
- Counter-intuitive

### 4.2. Example Illustrating The Difference

```python
# Demonstrate frequentist CI behavior
np.random.seed(42)
n_experiments = 100
coverage_count = 0
intervals = []

for exp in range(n_experiments):
    # Generate new data
    x_exp = np.random.uniform(0, 10, 30)
    y_exp = true_alpha + true_beta * x_exp + np.random.normal(0, true_sigma, 30)
    
    # Fit Bayesian model
    with pm.Model():
        alpha = pm.Normal('alpha', 0, 10)
        beta = pm.Normal('beta', 0, 10)
        sigma = pm.HalfNormal('sigma', 5)
        mu = alpha + beta * x_exp
        y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_exp)
        trace_exp = pm.sample(1000, tune=500, chains=2, random_seed=exp,
                             return_inferencedata=True, progressbar=False)
    
    # Extract CI for beta
    beta_exp = trace_exp.posterior['beta'].values.flatten()
    ci = az.hdi(beta_exp, hdi_prob=0.95)
    intervals.append(ci)
    
    # Check coverage
    if ci[0] <= true_beta <= ci[1]:
        coverage_count += 1

coverage_rate = coverage_count / n_experiments

print("\n" + "=" * 70)
print("FREQUENTIST INTERPRETATION OF CREDIBLE INTERVALS")
print("=" * 70)
print(f"\nRepeated {n_experiments} experiments")
print(f"True β = {true_beta}")
print(f"\nCoverage rate: {coverage_rate:.1%}")
print(f"→ {coverage_rate:.1%} of 95% CIs contained true β")
print(f"→ This is the FREQUENTIST property")
print(f"\nBut for ANY SINGLE interval, Bayesian interpretation:")
print(f"→ '95% probability β is in this specific interval'")
print("=" * 70)
```

## Tóm tắt

**Uncertainty quantification** là core strength của Bayesian statistics:

**Two types of uncertainty**:
1. **Epistemic (Parameter)**: Reducible, quantified by credible intervals
2. **Aleatoric (Data)**: Irreducible, quantified by prediction intervals

**Credible Intervals**:
- Range for **parameters**
- Direct probability interpretation
- Narrower (only parameter uncertainty)
- Types: ETI (equal-tailed), HDI (highest density)

**Prediction Intervals**:
- Range for **new observations**
- Includes parameter + data uncertainty
- Wider (irreducible noise)
- Essential for decision-making

**Bayesian advantage**:
- Direct probability statements
- Intuitive interpretation
- Honest uncertainty quantification

**Best practices**:
- Always report uncertainty, not just point estimates
- Choose appropriate interval type (credible vs prediction)
- Use HDI for skewed distributions
- Communicate clearly to stakeholders

## Bài tập

**Bài tập 1**: Fit regression model. Compute 89% credible intervals for all parameters. Interpret.

**Bài tập 2**: Generate posterior predictive samples. Compute 89% prediction interval for new x. Compare width with credible interval.

**Bài tập 3**: Vary sample size (n = 10, 50, 200). How do credible and prediction intervals change?

**Bài tập 4**: Real data. Report both credible and prediction intervals. Explain difference to non-technical audience.

**Bài tập 5**: Compare ETI vs HDI for skewed distribution (e.g., σ posterior). Which is shorter?

## Tài liệu Tham khảo

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis* (2nd Edition). Academic Press.
- Chapter 12: Bayesian Approaches to Testing

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 3: Sampling the Imaginary

**Gelman, A., et al. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 7: Evaluating, comparing, and expanding models

---

*Bài học tiếp theo: [10.2 Model Diagnostics & Reporting](/vi/chapter10/diagnostics-reporting/)*
