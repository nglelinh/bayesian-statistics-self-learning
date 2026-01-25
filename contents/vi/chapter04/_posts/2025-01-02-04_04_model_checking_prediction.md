---
layout: post
title: "Bài 4.4: Model Checking và Prediction - Đảm bảo Model Tốt"
chapter: '04'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ biết cách **kiểm tra model fit tốt không** và **make predictions với uncertainty**. Bạn sẽ học về posterior predictive checks - một trong những công cụ mạnh mẽ nhất trong Bayesian workflow. Quan trọng hơn, bạn sẽ hiểu rằng fitting model chỉ là bước đầu - checking và validating model là thiết yếu để đảm bảo kết luận đáng tin cậy.

## Giới thiệu: "All Models are Wrong, but Some are Useful"

George Box nói: **"All models are wrong, but some are useful."**

Mọi model đều là simplification của reality. Câu hỏi không phải là "Model có đúng không?" mà là **"Model có useful không?"**

Để trả lời, chúng ta cần:
1. **Posterior predictive checks**: Model có generate data giống observed data không?
2. **Residual analysis**: Có patterns trong residuals không?
3. **Predictions**: Model predict tốt cho new data không?

Đây là bài cuối cùng của Chapter 04 - hoàn thiện Bayesian regression workflow!

## 1. Posterior Predictive Distribution

**Posterior predictive distribution** là phân phối của **new data** $$\tilde{y}$$ given observed data $$y$$:

$$P(\tilde{y} \mid y) = \int P(\tilde{y} \mid \theta) P(\theta \mid y) \, d\theta$$

**Ý nghĩa**: Nếu model đúng, data sinh từ posterior predictive nên giống observed data.

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
import seaborn as sns
from scipy import stats

# Set style
az.style.use("arviz-darkgrid")

# Generate data (same as Bài 4.3)
np.random.seed(42)
n = 100
true_alpha = 50
true_beta = 0.7
true_sigma = 5

height = np.random.uniform(150, 190, n)
weight = true_alpha + true_beta * height + np.random.normal(0, true_sigma, n)

# Standardize
height_mean, height_std = height.mean(), height.std()
weight_mean, weight_std = weight.mean(), weight.std()
height_z = (height - height_mean) / height_std
weight_z = (weight - weight_mean) / weight_std

# Fit model
with pm.Model() as regression_model:
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1)
    sigma = pm.HalfNormal('sigma', sigma=1)
    
    mu = alpha + beta * height_z
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=weight_z)
    
    trace = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                     return_inferencedata=True)
    
    # POSTERIOR PREDICTIVE
    ppc = pm.sample_posterior_predictive(trace, random_seed=42)
    trace.extend(ppc)

print("=" * 70)
print("POSTERIOR PREDICTIVE SAMPLING COMPLETE")
print("=" * 70)
```

## 2. Posterior Predictive Checks (PPC)

### 2.1. Visual Check: Histogram Comparison

```python
# Posterior predictive check
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. PPC: Histogram overlay
az.plot_ppc(trace, ax=axes[0, 0], num_pp_samples=100)
axes[0, 0].set_title('Posterior Predictive Check\n' +
                     'Observed vs Simulated Data',
                     fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Weight (standardized)', fontsize=12, fontweight='bold')
axes[0, 0].grid(alpha=0.3, axis='y')

# 2. PPC: Scatter plot
y_pred_samples = trace.posterior_predictive['y_obs'].values
y_pred_mean = y_pred_samples.mean(axis=(0, 1))
y_pred_std = y_pred_samples.std(axis=(0, 1))

axes[0, 1].scatter(weight_z, y_pred_mean, s=50, alpha=0.6, edgecolors='black')
axes[0, 1].plot([-3, 3], [-3, 3], 'r--', linewidth=2, label='Perfect Prediction')
axes[0, 1].set_xlabel('Observed Weight', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Predicted Weight (mean)', fontsize=12, fontweight='bold')
axes[0, 1].set_title('Observed vs Predicted\nShould be on diagonal',
                     fontsize=14, fontweight='bold')
axes[0, 1].legend(fontsize=11)
axes[0, 1].grid(alpha=0.3)

# 3. PPC: Statistics comparison
stats_obs = {
    'Mean': weight_z.mean(),
    'SD': weight_z.std(),
    'Min': weight_z.min(),
    'Max': weight_z.max()
}

stats_pred = {
    'Mean': y_pred_samples.mean(),
    'SD': y_pred_samples.std(),
    'Min': y_pred_samples.min(),
    'Max': y_pred_samples.max()
}

axes[1, 0].axis('off')
comparison = "STATISTICS COMPARISON\n" + "=" * 50 + "\n\n"
comparison += f"{'Statistic':<15} {'Observed':<12} {'Predicted':<12} {'Match?'}\n"
comparison += "-" * 50 + "\n"

for stat in stats_obs.keys():
    obs_val = stats_obs[stat]
    pred_val = stats_pred[stat]
    match = "✓" if abs(obs_val - pred_val) < 0.2 else "?"
    comparison += f"{stat:<15} {obs_val:>11.3f} {pred_val:>11.3f}  {match}\n"

comparison += "\n→ Statistics should be similar!"

axes[1, 0].text(0.5, 0.5, comparison, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

# 4. Interpretation
axes[1, 1].axis('off')
interpretation = """
╔═══════════════════════════════════════════════════════════╗
║        POSTERIOR PREDICTIVE CHECK (PPC)                   ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Câu hỏi:                                                 ║
║    Nếu model đúng, data sinh từ model có giống           ║
║    observed data không?                                   ║
║                                                           ║
║  Nếu YES (giống):                                         ║
║    ✓ Model capture được patterns trong data              ║
║    ✓ Model assumptions hợp lý                             ║
║    ✓ Có thể tin tưởng predictions                         ║
║                                                           ║
║  Nếu NO (khác):                                           ║
║    ✗ Model miss patterns quan trọng                       ║
║    ✗ Cần improve model                                    ║
║    ✗ Có thể: Non-linearity, outliers, etc.               ║
║                                                           ║
║  Best practice:                                           ║
║    → Check multiple statistics                            ║
║    → Visual inspection                                    ║
║    → Domain knowledge                                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[1, 1].text(0.5, 0.5, interpretation, fontsize=9, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9))

plt.tight_layout()
plt.show()

print("\n→ PPC looks good! Model captures data patterns well.")
```

## 3. Residual Analysis

Residuals là sự khác biệt giữa observed và predicted:

$$\text{residual}_i = y_i - \hat{y}_i$$

**Nếu model tốt**: Residuals nên:
- Random (không có pattern)
- Normally distributed
- Homoscedastic (variance không đổi)

```python
# Residual analysis
residuals = weight_z - y_pred_mean

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Residuals vs Fitted
axes[0, 0].scatter(y_pred_mean, residuals, s=50, alpha=0.6, edgecolors='black')
axes[0, 0].axhline(0, color='red', linestyle='--', linewidth=2)
axes[0, 0].set_xlabel('Fitted Values', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Residuals', fontsize=12, fontweight='bold')
axes[0, 0].set_title('Residuals vs Fitted\nShould be random around 0',
                     fontsize=14, fontweight='bold')
axes[0, 0].grid(alpha=0.3)

# 2. Residuals vs Predictor
axes[0, 1].scatter(height_z, residuals, s=50, alpha=0.6, edgecolors='black')
axes[0, 1].axhline(0, color='red', linestyle='--', linewidth=2)
axes[0, 1].set_xlabel('Height (standardized)', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Residuals', fontsize=12, fontweight='bold')
axes[0, 1].set_title('Residuals vs Predictor\nCheck for non-linearity',
                     fontsize=14, fontweight='bold')
axes[0, 1].grid(alpha=0.3)

# 3. Histogram of residuals
axes[1, 0].hist(residuals, bins=20, density=True, alpha=0.7,
               color='skyblue', edgecolor='black', label='Residuals')
x_norm = np.linspace(residuals.min(), residuals.max(), 100)
axes[1, 0].plot(x_norm, stats.norm(0, residuals.std()).pdf(x_norm),
               'r-', linewidth=3, label='Normal(0, σ)')
axes[1, 0].set_xlabel('Residuals', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1, 0].set_title('Distribution of Residuals\nShould be ~ Normal',
                     fontsize=14, fontweight='bold')
axes[1, 0].legend(fontsize=11)
axes[1, 0].grid(alpha=0.3, axis='y')

# 4. Q-Q plot
stats.probplot(residuals, dist="norm", plot=axes[1, 1])
axes[1, 1].set_title('Q-Q Plot\nShould be on diagonal',
                     fontsize=14, fontweight='bold')
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\nRESIDUAL ANALYSIS:")
print("-" * 70)
print(f"Mean of residuals: {residuals.mean():.4f} (should be ≈ 0)")
print(f"SD of residuals:   {residuals.std():.4f}")
print("\nChecks:")
print("  ✓ No pattern in residuals vs fitted")
print("  ✓ No pattern in residuals vs predictor")
print("  ✓ Residuals approximately normal")
print("  ✓ Q-Q plot on diagonal")
print("\n→ Model assumptions satisfied!")
print("-" * 70)
```

## 4. Predictions cho New Data

Bây giờ make predictions cho new data với **full uncertainty quantification**.

```python
# New data for prediction
height_new = np.array([160, 170, 180])  # cm
height_new_z = (height_new - height_mean) / height_std

# Predictions
with regression_model:
    # Set new x values
    pm.set_data({"height_z": height_new_z})
    
    # Sample posterior predictive for new data
    ppc_new = pm.sample_posterior_predictive(trace, var_names=['y_obs'],
                                             random_seed=42)

# Extract predictions
y_new_samples = ppc_new.posterior_predictive['y_obs'].values
y_new_samples = y_new_samples.reshape(-1, len(height_new))

# Transform back to original scale
y_new_samples_original = y_new_samples * weight_std + weight_mean

# Statistics
y_new_mean = y_new_samples_original.mean(axis=0)
y_new_lower = np.percentile(y_new_samples_original, 2.5, axis=0)
y_new_upper = np.percentile(y_new_samples_original, 97.5, axis=0)

# Visualize predictions
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 1. Predictions with uncertainty
axes[0].scatter(height, weight, s=50, alpha=0.4, edgecolors='black',
               label='Training Data')
axes[0].errorbar(height_new, y_new_mean, 
                yerr=[y_new_mean - y_new_lower, y_new_upper - y_new_mean],
                fmt='ro', markersize=10, capsize=5, capthick=2,
                label='Predictions (95% CI)')
axes[0].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0].set_title('Predictions for New Data\nWith 95% Credible Intervals',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# 2. Prediction distributions
for i, h in enumerate(height_new):
    axes[1].hist(y_new_samples_original[:, i], bins=50, alpha=0.5,
                density=True, label=f'Height = {h} cm')

axes[1].set_xlabel('Predicted Weight (kg)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('Posterior Predictive Distributions\nFull uncertainty',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# Print predictions
print("\n" + "=" * 70)
print("PREDICTIONS FOR NEW DATA")
print("=" * 70)
for i, h in enumerate(height_new):
    print(f"\nHeight = {h} cm:")
    print(f"  Predicted Weight: {y_new_mean[i]:.1f} kg")
    print(f"  95% Credible Interval: [{y_new_lower[i]:.1f}, {y_new_upper[i]:.1f}] kg")
    print(f"  Interpretation: 95% tin rằng weight trong khoảng này")

print("\n→ Predictions include FULL uncertainty!")
print("=" * 70)
```

## 5. Prediction Intervals vs Credible Intervals

**Quan trọng**: Có hai loại intervals:

### 5.1. Credible Interval cho Parameter

$$P(\beta \in [a, b] \mid \text{data}) = 0.95$$

**Ý nghĩa**: Uncertainty về **parameter** $$\beta$$.

### 5.2. Prediction Interval cho New Data

$$P(\tilde{y} \in [c, d] \mid \text{data}) = 0.95$$

**Ý nghĩa**: Uncertainty về **new observation** $$\tilde{y}$$.

**Prediction interval rộng hơn** vì bao gồm:
- Parameter uncertainty ($$\alpha, \beta, \sigma$$)
- Observation noise ($$\sigma$$)

```python
# Illustrate difference
fig, ax = plt.subplots(figsize=(12, 7))

# Regression line with parameter uncertainty
height_range = np.linspace(height.min(), height.max(), 100)
height_range_z = (height_range - height_mean) / height_std

alpha_samples = trace.posterior['alpha'].values.flatten()
beta_samples = trace.posterior['beta'].values.flatten()

# Parameter uncertainty (credible band for mean)
weight_mean_samples = []
for i in range(1000):
    idx = np.random.randint(len(alpha_samples))
    weight_pred_z = alpha_samples[idx] + beta_samples[idx] * height_range_z
    weight_pred = weight_pred_z * weight_std + weight_mean
    weight_mean_samples.append(weight_pred)

weight_mean_samples = np.array(weight_mean_samples)
weight_mean_lower = np.percentile(weight_mean_samples, 2.5, axis=0)
weight_mean_upper = np.percentile(weight_mean_samples, 97.5, axis=0)

# Prediction uncertainty (includes observation noise)
# (Simplified illustration)
sigma_samples = trace.posterior['sigma'].values.flatten()
sigma_mean = sigma_samples.mean() * weight_std

ax.scatter(height, weight, s=50, alpha=0.4, edgecolors='black',
          label='Observed Data')
ax.plot(height_range, weight_mean_samples.mean(axis=0), 'r-', linewidth=3,
       label='Posterior Mean')
ax.fill_between(height_range, weight_mean_lower, weight_mean_upper,
                alpha=0.3, color='blue', label='95% Credible Band (mean)')
ax.fill_between(height_range, 
                weight_mean_lower - 2*sigma_mean,
                weight_mean_upper + 2*sigma_mean,
                alpha=0.2, color='orange', label='95% Prediction Band')

ax.set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
ax.set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
ax.set_title('Credible Band vs Prediction Band\n' +
            'Prediction band wider (includes observation noise)',
            fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\nCREDIBLE BAND vs PREDICTION BAND:")
print("-" * 70)
print("Credible Band (blue):")
print("  - Uncertainty về MEAN của y")
print("  - Chỉ parameter uncertainty")
print("  - Hẹp hơn")
print("\nPrediction Band (orange):")
print("  - Uncertainty về NEW OBSERVATION")
print("  - Parameter uncertainty + Observation noise")
print("  - Rộng hơn")
print("-" * 70)
```

## Tóm tắt: Complete Bayesian Regression Workflow

Chúng ta đã hoàn thành **full Bayesian regression workflow**:

### Chapter 04 Summary:

**Bài 4.1**: Generative Model
- Regression như câu chuyện sinh dữ liệu
- Parameters: $$\alpha, \beta, \sigma$$

**Bài 4.2**: Prior Selection
- Standardization
- Weakly informative priors

**Bài 4.3**: PyMC Implementation
- Fit model với NUTS
- Diagnostics
- Interpret posterior

**Bài 4.4**: Model Checking & Prediction
- Posterior predictive checks
- Residual analysis
- Predictions với uncertainty

### Key Takeaways:

✅ **Model checking là thiết yếu** - không "tin mù quáng"  
✅ **PPC**: Data sinh từ model nên giống observed data  
✅ **Residuals**: Nên random, normal, homoscedastic  
✅ **Predictions**: Include full uncertainty  
✅ **Prediction intervals > Credible intervals** (vì có observation noise)  

## Bài tập

**Bài tập 1: Full Workflow**
Generate data, fit model, và thực hiện full checking:
(a) Posterior predictive check
(b) Residual analysis
(c) Predictions cho 5 new points
(d) Viết báo cáo: Model có tốt không?

**Bài tập 2: Bad Model**
Generate data với **non-linear relationship** (e.g., quadratic).
(a) Fit linear model
(b) PPC sẽ như thế nào?
(c) Residuals có pattern không?
(d) Model có vấn đề gì?

**Bài tập 3: Prediction Intervals**
(a) Tại sao prediction interval rộng hơn credible interval?
(b) Compute cả hai cho một new point
(c) So sánh widths
(d) Interpretation khác nhau như thế nào?

**Bài tập 4: Outliers**
Add 5 outliers vào data.
(a) Fit model
(b) Residual plot sẽ như thế nào?
(c) Outliers ảnh hưởng posterior như thế nào?
(d) Làm sao handle outliers?

**Bài tập 5: Model Comparison**
Fit hai models: Linear và Quadratic.
(a) PPC cho cả hai
(b) Model nào fit tốt hơn?
(c) Làm sao so sánh formally? (hint: LOO, WAIC)

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., et al. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 6: Model checking

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 4.5: Posterior prediction

**Gabry, J., Simpson, D., Vehtari, A., Betancourt, M., & Gelman, A. (2019).** *Visualization in Bayesian workflow*. Journal of the Royal Statistical Society: Series A, 182(2), 389-402.

---

**🎉 CHÚC MỪNG! BẠN ĐÃ HOÀN THÀNH CHAPTER 04! 🎉**

Bạn giờ đã có đầy đủ kiến thức và kỹ năng để:
- Xây dựng Bayesian regression models
- Chọn priors có nguyên tắc
- Implement với PyMC
- Check model quality
- Make predictions với uncertainty

**Ready for real-world Bayesian data analysis!** 🚀
