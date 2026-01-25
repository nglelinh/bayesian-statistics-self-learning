---
layout: post
title: "Bài 4.3: Posterior Inference với PyMC - Từ Theory đến Practice"
chapter: '04'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ biết cách **implement Bayesian linear regression** với PyMC và diễn giải posterior distributions. Bạn sẽ học cách kết nối theory (từ Bài 4.1 và 4.2) với practice: fit model, check diagnostics, interpret results, và make predictions. Đây là bài "hands-on" quan trọng nhất trong Chapter 04.

## Giới thiệu: Từ Math đến Code

Trong hai bài trước, chúng ta đã học:
- **Bài 4.1**: Model là gì (generative story)
- **Bài 4.2**: Priors nào hợp lý

Bây giờ đến lúc **implement**! Chúng ta sẽ:
1. Generate synthetic data (để biết "truth")
2. Standardize data
3. Specify model trong PyMC với priors đã chọn
4. Run MCMC (NUTS sampler)
5. Check diagnostics
6. Interpret posterior
7. Make predictions

Let's go! 🚀

## 1. Generate và Prepare Data

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
import seaborn as sns
from scipy import stats

# Set style
az.style.use("arviz-darkgrid")
sns.set_palette("husl")

# Generate synthetic data
np.random.seed(42)
n = 100

# True parameters (we know these, but pretend we don't)
true_alpha = 50  # kg (intercept)
true_beta = 0.7  # kg/cm (slope)
true_sigma = 5   # kg (noise)

# Generate data: Height → Weight
height = np.random.uniform(150, 190, n)  # cm
weight = true_alpha + true_beta * height + np.random.normal(0, true_sigma, n)  # kg

# Visualize raw data
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].scatter(height, weight, s=80, alpha=0.6, edgecolors='black')
axes[0].plot(height, true_alpha + true_beta * height, 'r-', linewidth=3,
            label=f'True: y = {true_alpha:.1f} + {true_beta:.2f}x')
axes[0].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0].set_title('Raw Data\nHeight → Weight', fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Standardize (remember Bài 4.2!)
height_mean, height_std = height.mean(), height.std()
weight_mean, weight_std = weight.mean(), weight.std()

height_z = (height - height_mean) / height_std
weight_z = (weight - weight_mean) / weight_std

axes[1].scatter(height_z, weight_z, s=80, alpha=0.6, edgecolors='black')
axes[1].axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
axes[1].axvline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
axes[1].set_xlabel('Height (standardized)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Weight (standardized)', fontsize=12, fontweight='bold')
axes[1].set_title('Standardized Data\nmean=0, SD=1', fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("=" * 70)
print("DATA PREPARATION")
print("=" * 70)
print(f"\nRaw Data:")
print(f"  Height: mean={height_mean:.1f} cm, SD={height_std:.1f} cm")
print(f"  Weight: mean={weight_mean:.1f} kg, SD={weight_std:.1f} kg")
print(f"\nStandardized Data:")
print(f"  Height: mean={height_z.mean():.2f}, SD={height_z.std():.2f}")
print(f"  Weight: mean={weight_z.mean():.2f}, SD={weight_z.std():.2f}")
print(f"\n→ Ready for Bayesian regression với weakly informative priors!")
print("=" * 70)
```

## 2. Specify Model trong PyMC

Bây giờ implement model với priors từ Bài 4.2:

```python
# Bayesian Linear Regression với PyMC
with pm.Model() as regression_model:
    # Priors (weakly informative, từ Bài 4.2)
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1)
    sigma = pm.HalfNormal('sigma', sigma=1)
    
    # Linear model
    mu = alpha + beta * height_z
    
    # Likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=weight_z)
    
    # Sample from posterior
    trace = pm.sample(
        draws=2000,        # Số mẫu sau tune
        tune=1000,         # Burn-in
        chains=4,          # Số chains
        random_seed=42,
        return_inferencedata=True
    )

print("\n" + "=" * 70)
print("SAMPLING COMPLETE!")
print("=" * 70)
```

## 3. Diagnostics: Kiểm tra Chất lượng

Trước khi tin tưởng posterior, phải check diagnostics (nhớ Bài 3.5!):

```python
# Summary với diagnostics
print("\n" + "=" * 70)
print("POSTERIOR SUMMARY")
print("=" * 70)
summary = az.summary(trace, var_names=['alpha', 'beta', 'sigma'])
print(summary)
print("=" * 70)

# Comprehensive diagnostics visualization
fig, axes = plt.subplots(3, 3, figsize=(18, 15))

# Row 1: Trace plots
for idx, var in enumerate(['alpha', 'beta', 'sigma']):
    az.plot_trace(trace, var_names=[var], axes=axes[idx, :2])
    axes[idx, 0].set_title(f'Trace Plot: {var}', fontsize=12, fontweight='bold')
    axes[idx, 1].set_title(f'Posterior: {var}', fontsize=12, fontweight='bold')

# Column 3: Autocorrelation
for idx, var in enumerate(['alpha', 'beta', 'sigma']):
    az.plot_autocorr(trace, var_names=[var], ax=axes[idx, 2], max_lag=50)
    axes[idx, 2].set_title(f'Autocorrelation: {var}', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()

# Check diagnostics
print("\nDIAGNOSTICS CHECK:")
print("-" * 70)
for var in ['alpha', 'beta', 'sigma']:
    rhat = summary.loc[var, 'r_hat']
    ess_bulk = summary.loc[var, 'ess_bulk']
    ess_tail = summary.loc[var, 'ess_tail']
    
    print(f"\n{var}:")
    print(f"  R-hat = {rhat:.4f} {'✓' if rhat < 1.01 else '✗ WARNING'}")
    print(f"  ESS (bulk) = {ess_bulk:.0f} {'✓' if ess_bulk > 400 else '✗ LOW'}")
    print(f"  ESS (tail) = {ess_tail:.0f} {'✓' if ess_tail > 400 else '✗ LOW'}")

print("\n→ Tất cả diagnostics tốt! Có thể tin tưởng posterior.")
print("-" * 70)
```

## 4. Interpret Posterior: Ý nghĩa là gì?

Bây giờ interpret posterior distributions:

```python
# Extract posterior samples
alpha_samples = trace.posterior['alpha'].values.flatten()
beta_samples = trace.posterior['beta'].values.flatten()
sigma_samples = trace.posterior['sigma'].values.flatten()

# Posterior statistics
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# Alpha
axes[0, 0].hist(alpha_samples, bins=50, density=True, alpha=0.7,
               color='skyblue', edgecolor='black')
axes[0, 0].axvline(alpha_samples.mean(), color='red', linewidth=2,
                  label=f'Mean = {alpha_samples.mean():.3f}')
axes[0, 0].axvline(np.percentile(alpha_samples, 2.5), color='orange',
                  linestyle='--', linewidth=2)
axes[0, 0].axvline(np.percentile(alpha_samples, 97.5), color='orange',
                  linestyle='--', linewidth=2, label='95% CI')
axes[0, 0].set_xlabel('α (standardized)', fontsize=11, fontweight='bold')
axes[0, 0].set_ylabel('Density', fontsize=11, fontweight='bold')
axes[0, 0].set_title('Posterior: Intercept (α)', fontsize=13, fontweight='bold')
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(alpha=0.3, axis='y')

# Beta
axes[0, 1].hist(beta_samples, bins=50, density=True, alpha=0.7,
               color='lightgreen', edgecolor='black')
axes[0, 1].axvline(beta_samples.mean(), color='red', linewidth=2,
                  label=f'Mean = {beta_samples.mean():.3f}')
axes[0, 1].axvline(np.percentile(beta_samples, 2.5), color='orange',
                  linestyle='--', linewidth=2)
axes[0, 1].axvline(np.percentile(beta_samples, 97.5), color='orange',
                  linestyle='--', linewidth=2, label='95% CI')
axes[0, 1].set_xlabel('β (standardized)', fontsize=11, fontweight='bold')
axes[0, 1].set_ylabel('Density', fontsize=11, fontweight='bold')
axes[0, 1].set_title('Posterior: Slope (β)', fontsize=13, fontweight='bold')
axes[0, 1].legend(fontsize=10)
axes[0, 1].grid(alpha=0.3, axis='y')

# Sigma
axes[0, 2].hist(sigma_samples, bins=50, density=True, alpha=0.7,
               color='lightyellow', edgecolor='black')
axes[0, 2].axvline(sigma_samples.mean(), color='red', linewidth=2,
                  label=f'Mean = {sigma_samples.mean():.3f}')
axes[0, 2].axvline(np.percentile(sigma_samples, 2.5), color='orange',
                  linestyle='--', linewidth=2)
axes[0, 2].axvline(np.percentile(sigma_samples, 97.5), color='orange',
                  linestyle='--', linewidth=2, label='95% CI')
axes[0, 2].set_xlabel('σ (standardized)', fontsize=11, fontweight='bold')
axes[0, 2].set_ylabel('Density', fontsize=11, fontweight='bold')
axes[0, 2].set_title('Posterior: Noise (σ)', fontsize=13, fontweight='bold')
axes[0, 2].legend(fontsize=10)
axes[0, 2].grid(alpha=0.3, axis='y')

# Interpretation text
axes[1, 0].axis('off')
interp_alpha = f"""
INTERCEPT (α)

Standardized scale:
  Mean: {alpha_samples.mean():.3f}
  95% CI: [{np.percentile(alpha_samples, 2.5):.3f}, 
           {np.percentile(alpha_samples, 97.5):.3f}]

Ý nghĩa:
  Weight (standardized) khi
  Height = mean height

→ Gần 0 là hợp lý!
"""
axes[1, 0].text(0.5, 0.5, interp_alpha, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

axes[1, 1].axis('off')
interp_beta = f"""
SLOPE (β)

Standardized scale:
  Mean: {beta_samples.mean():.3f}
  95% CI: [{np.percentile(beta_samples, 2.5):.3f}, 
           {np.percentile(beta_samples, 97.5):.3f}]

Ý nghĩa:
  Weight tăng {beta_samples.mean():.3f} SD
  khi Height tăng 1 SD

95% tin rằng β trong CI!
"""
axes[1, 1].text(0.5, 0.5, interp_beta, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

axes[1, 2].axis('off')
interp_sigma = f"""
NOISE (σ)

Standardized scale:
  Mean: {sigma_samples.mean():.3f}
  95% CI: [{np.percentile(sigma_samples, 2.5):.3f}, 
           {np.percentile(sigma_samples, 97.5):.3f}]

Ý nghĩa:
  Độ biến động cá nhân
  xung quanh regression line

σ < 1: Model fit tốt!
"""
axes[1, 2].text(0.5, 0.5, interp_sigma, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.show()
```

## 5. Transform Back: Diễn giải trong Original Scale

Standardized parameters khó diễn giải. Hãy transform về original scale:

```python
# Transform parameters back to original scale
# y_original = y_mean + y_std * (alpha + beta * x_standardized)
# y_original = y_mean + y_std * (alpha + beta * (x - x_mean) / x_std)
# y_original = (y_mean + y_std * alpha - y_std * beta * x_mean / x_std) + 
#              (y_std * beta / x_std) * x
# y_original = alpha_original + beta_original * x

beta_original = beta_samples * (weight_std / height_std)
alpha_original = weight_mean + weight_std * alpha_samples - beta_original * height_mean

print("\n" + "=" * 70)
print("PARAMETERS IN ORIGINAL SCALE")
print("=" * 70)
print(f"\nIntercept (α):")
print(f"  Mean: {alpha_original.mean():.2f} kg")
print(f"  95% CI: [{np.percentile(alpha_original, 2.5):.2f}, " +
      f"{np.percentile(alpha_original, 97.5):.2f}] kg")
print(f"  True value: {true_alpha:.2f} kg")

print(f"\nSlope (β):")
print(f"  Mean: {beta_original.mean():.3f} kg/cm")
print(f"  95% CI: [{np.percentile(beta_original, 2.5):.3f}, " +
      f"{np.percentile(beta_original, 97.5):.3f}] kg/cm")
print(f"  True value: {true_beta:.3f} kg/cm")
print(f"\n  Interpretation: Mỗi cm chiều cao tăng →")
print(f"                  cân nặng tăng {beta_original.mean():.3f} kg (trung bình)")

sigma_original = sigma_samples * weight_std
print(f"\nNoise (σ):")
print(f"  Mean: {sigma_original.mean():.2f} kg")
print(f"  95% CI: [{np.percentile(sigma_original, 2.5):.2f}, " +
      f"{np.percentile(sigma_original, 97.5):.2f}] kg")
print(f"  True value: {true_sigma:.2f} kg")
print("=" * 70)
```

## 6. Visualize Posterior Regression Lines

```python
# Visualize uncertainty in regression line
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Standardized scale
height_range_z = np.linspace(height_z.min(), height_z.max(), 100)

# Draw posterior samples of regression lines
n_lines = 100
for i in np.random.choice(len(alpha_samples), n_lines, replace=False):
    weight_pred_z = alpha_samples[i] + beta_samples[i] * height_range_z
    axes[0].plot(height_range_z, weight_pred_z, 'b-', alpha=0.02, linewidth=1)

axes[0].scatter(height_z, weight_z, s=50, alpha=0.6, edgecolors='black',
               label='Observed Data')
axes[0].plot(height_range_z, alpha_samples.mean() + beta_samples.mean() * height_range_z,
            'r-', linewidth=3, label='Posterior Mean')
axes[0].set_xlabel('Height (standardized)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Weight (standardized)', fontsize=12, fontweight='bold')
axes[0].set_title('Posterior Regression Lines\n(Standardized Scale)',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Original scale
height_range = np.linspace(height.min(), height.max(), 100)

for i in np.random.choice(len(alpha_original), n_lines, replace=False):
    weight_pred = alpha_original[i] + beta_original[i] * height_range
    axes[1].plot(height_range, weight_pred, 'b-', alpha=0.02, linewidth=1)

axes[1].scatter(height, weight, s=50, alpha=0.6, edgecolors='black',
               label='Observed Data')
axes[1].plot(height_range, alpha_original.mean() + beta_original.mean() * height_range,
            'r-', linewidth=3, label='Posterior Mean')
axes[1].plot(height_range, true_alpha + true_beta * height_range,
            'g--', linewidth=3, label='True Line', alpha=0.7)
axes[1].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[1].set_title('Posterior Regression Lines\n(Original Scale)',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\n→ Posterior uncertainty được quantified đầy đủ!")
print("  Blue lines: Posterior samples")
print("  Red line: Posterior mean")
print("  Green line: True (chỉ biết vì synthetic data)")
```

## Tóm tắt và Kết nối

Chúng ta đã hoàn thành full workflow của Bayesian regression:

1. **Data preparation**: Generate và standardize
2. **Model specification**: PyMC với weakly informative priors
3. **Sampling**: NUTS với 4 chains
4. **Diagnostics**: R-hat, ESS, trace plots, autocorrelation
5. **Interpretation**: Posterior distributions và credible intervals
6. **Transform back**: Original scale cho diễn giải
7. **Visualization**: Posterior regression lines với uncertainty

**Key insights**:
- Posterior là **distributions**, không phải point estimates
- Credible intervals có diễn giải trực tiếp: "95% tin rằng..."
- Uncertainty được quantified đầy đủ
- Diagnostics đảm bảo kết quả đáng tin cậy

Trong bài tiếp theo, chúng ta sẽ học **model checking** và **prediction** - cách đảm bảo model fit tốt và make predictions cho data mới.

## Bài tập

**Bài tập 1: Full Workflow**
Generate data với α=10, β=2, σ=3, n=50.
(a) Standardize data
(b) Fit Bayesian regression với PyMC
(c) Check diagnostics
(d) Interpret posterior trong original scale

**Bài tập 2: Credible Intervals**
(a) Compute 95% credible interval cho β
(b) Diễn giải: "95% tin rằng..."
(c) So sánh với frequentist confidence interval
(d) Interpretation khác nhau như thế nào?

**Bài tập 3: Uncertainty Visualization**
(a) Vẽ 200 posterior regression lines
(b) Compute 95% prediction band
(c) Có bao nhiêu observed points nằm trong band?
(d) Nên là ~95%, đúng không?

**Bài tập 4: Prior Sensitivity**
Fit model với 3 priors khác nhau cho β:
(a) N(0, 0.5) - narrow
(b) N(0, 1) - weakly informative
(c) N(0, 2) - wide
So sánh posteriors. Prior nào ảnh hưởng nhiều nhất?

**Bài tập 5: Transform Back**
(a) Tại sao cần transform về original scale?
(b) Công thức transform cho α và β là gì?
(c) Implement transformation trong Python
(d) Verify bằng cách so sánh predictions

## Tài liệu Tham khảo

### Primary References:

**PyMC Documentation**: https://www.pymc.io/
- Examples: Linear Regression

**Martin, O. A., Kumar, R., & Lao, J. (2021).** *Bayesian Modeling and Computation in Python*. CRC Press.
- Chapter 3: Linear Models

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 4: Geocentric Models

---

*Bài học tiếp theo: [4.4 Model Checking và Prediction](/vi/chapter04/model-checking-prediction/)*
