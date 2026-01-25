---
layout: post
title: "Bài 3.6: PyMC - Bayesian Modeling trong Thực tế"
chapter: '03'
order: 6
owner: Nguyen Le Linh
lang: vi
categories:
- chapter03
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ biết cách sử dụng **PyMC** - một trong những thư viện Bayesian modeling mạnh mẽ nhất cho Python. Bạn sẽ học cách xây dựng models một cách declarative, chạy MCMC với NUTS sampler, và thực hiện diagnostics với ArviZ. Quan trọng hơn, bạn sẽ hiểu rằng PyMC không phải là "black box" - mọi thứ bạn đã học từ các bài trước (Prior, Likelihood, Posterior, MCMC, Diagnostics) đều được PyMC thực hiện một cách tự động và hiệu quả.

## Giới thiệu: Từ "Làm Tay" đến Công cụ Chuyên nghiệp

Trong các bài trước, chúng ta đã học cách implement MCMC từ đầu. Điều này cực kỳ quan trọng để hiểu sâu về cách thuật toán hoạt động. Nhưng trong thực tế, khi làm việc với các mô hình phức tạp, việc implement từ đầu sẽ:

- Tốn thời gian và dễ mắc lỗi
- Khó optimize performance
- Khó mở rộng cho nhiều tham số
- Cần implement lại diagnostics

**PyMC** giải quyết tất cả các vấn đề này. Nó cung cấp:

✅ **Declarative syntax**: Mô tả model bằng ngôn ngữ gần với toán học  
✅ **Automatic differentiation**: Tự động tính gradient cho HMC  
✅ **NUTS sampler**: Thuật toán MCMC hiện đại nhất, tự động tuning  
✅ **Diagnostics**: Tích hợp với ArviZ cho visualization và diagnostics  
✅ **Performance**: Optimized code, có thể chạy trên GPU  

Hãy xem PyMC như một "compiler" cho Bayesian models - bạn mô tả model, PyMC lo phần còn lại.

## 1. PyMC Basics: Model Đầu tiên

![MCMC Workflow]({{ site.baseurl }}/img/chapter_img/chapter03/mcmc_workflow.png)

### 1.1. Installation và Setup

```python
# Installation (chạy trong terminal hoặc notebook)
# pip install pymc arviz

import pymc as pm
import arviz as az
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print(f"PyMC version: {pm.__version__}")
print(f"ArviZ version: {az.__version__}")

# Thiết lập style
az.style.use("arviz-darkgrid")
```

### 1.2. Ví dụ Đơn giản: Beta-Binomial

Hãy bắt đầu với một ví dụ quen thuộc: Beta-Binomial (coin flipping).

**Bài toán**: 10 lần toss, 7 lần heads. Ước lượng xác suất heads.

**Model**:
- Prior: $$\theta \sim \text{Beta}(2, 2)$$
- Likelihood: $$y \sim \text{Binomial}(n=10, p=\theta)$$
- Posterior: $$P(\theta \mid y=7)$$ = ?

```python
# Data
n_trials = 10
n_success = 7

# Định nghĩa model trong PyMC
with pm.Model() as beta_binomial_model:
    # Prior: Beta(2, 2) - slightly informative
    theta = pm.Beta('theta', alpha=2, beta=2)
    
    # Likelihood: Binomial
    y_obs = pm.Binomial('y_obs', n=n_trials, p=theta, observed=n_success)
    
    # Sampling với NUTS
    trace = pm.sample(
        draws=2000,        # Số mẫu sau burn-in
        tune=1000,         # Burn-in period
        chains=4,          # Số chains
        random_seed=42,
        return_inferencedata=True
    )

# In summary
print("=" * 70)
print("POSTERIOR SUMMARY")
print("=" * 70)
print(az.summary(trace, var_names=['theta']))
print("=" * 70)
```

**Giải thích code**:

1. **`with pm.Model() as ...`**: Context manager để định nghĩa model
2. **`pm.Beta('theta', ...)`**: Định nghĩa prior cho tham số `theta`
3. **`pm.Binomial('y_obs', ..., observed=...)`**: Định nghĩa likelihood với data quan sát
4. **`pm.sample(...)`**: Chạy MCMC (mặc định dùng NUTS)
5. **`az.summary(...)`**: Tóm tắt posterior với diagnostics

### 1.3. Visualization với ArviZ

```python
# Comprehensive visualization
fig = plt.figure(figsize=(16, 10))

# 1. Trace plot (convergence check)
ax1 = plt.subplot(2, 3, 1)
az.plot_trace(trace, var_names=['theta'], axes=[[ax1, plt.subplot(2, 3, 2)]])
plt.suptitle('', fontsize=1)  # Remove default title

# 2. Posterior distribution
ax3 = plt.subplot(2, 3, 3)
az.plot_posterior(trace, var_names=['theta'], ax=ax3, 
                  hdi_prob=0.95, point_estimate='mean')
ax3.set_title('Posterior Distribution\n95% HDI', fontsize=12, fontweight='bold')

# 3. Autocorrelation
ax4 = plt.subplot(2, 3, 4)
az.plot_autocorr(trace, var_names=['theta'], ax=ax4, max_lag=50)
ax4.set_title('Autocorrelation', fontsize=12, fontweight='bold')

# 4. Rank plot (convergence diagnostic)
ax5 = plt.subplot(2, 3, 5)
az.plot_rank(trace, var_names=['theta'], ax=ax5)
ax5.set_title('Rank Plot\n(Should be uniform)', fontsize=12, fontweight='bold')

# 5. Forest plot (summary)
ax6 = plt.subplot(2, 3, 6)
az.plot_forest(trace, var_names=['theta'], ax=ax6, hdi_prob=0.95)
ax6.set_title('Forest Plot\n95% HDI', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()

print("\n✓ Tất cả diagnostics đều tốt!")
print("  - Trace plot: Fuzzy caterpillar")
print("  - R-hat ≈ 1.0")
print("  - ESS cao")
print("  - Autocorrelation thấp")
```

### 1.4. So sánh với True Posterior

Vì đây là Beta-Binomial conjugate, chúng ta biết true posterior: Beta(9, 5).

```python
from scipy import stats

# True posterior
true_posterior = stats.beta(9, 5)

# Extract PyMC samples
theta_samples = trace.posterior['theta'].values.flatten()

# Plot comparison
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# Histogram vs True
axes[0].hist(theta_samples, bins=50, density=True, alpha=0.7,
            color='skyblue', edgecolor='black', label='PyMC Samples')
theta_grid = np.linspace(0, 1, 1000)
axes[0].plot(theta_grid, true_posterior.pdf(theta_grid), 
            'r-', linewidth=3, label='True Posterior: Beta(9,5)')
axes[0].set_xlabel('θ', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('PyMC Posterior vs True Posterior\n' +
                 'PyMC samples ≈ True posterior!',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')

# Statistics comparison
stats_comparison = {
    'Mean': [np.mean(theta_samples), true_posterior.mean()],
    'SD': [np.std(theta_samples), true_posterior.std()],
    '95% CI Lower': [np.percentile(theta_samples, 2.5), true_posterior.ppf(0.025)],
    '95% CI Upper': [np.percentile(theta_samples, 97.5), true_posterior.ppf(0.975)]
}

axes[1].axis('off')
table_text = "STATISTICS COMPARISON\n" + "=" * 50 + "\n\n"
table_text += f"{'Statistic':<20} {'PyMC':<12} {'True':<12} {'Error'}\n"
table_text += "-" * 50 + "\n"

for stat, (pymc_val, true_val) in stats_comparison.items():
    error = abs(pymc_val - true_val)
    table_text += f"{stat:<20} {pymc_val:>11.4f} {true_val:>11.4f} {error:>11.4f}\n"

table_text += "\n→ PyMC estimates rất chính xác!"

axes[1].text(0.5, 0.5, table_text, ha='center', va='center',
            fontsize=11, family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.show()
```

## 2. Ví dụ Thực tế: Linear Regression

Bây giờ hãy thử một ví dụ phức tạp hơn - Bayesian Linear Regression.

### 2.1. Bài toán

Giả sử chúng ta có dữ liệu về chiều cao và cân nặng của 50 người. Chúng ta muốn mô hình hóa mối quan hệ:

$$\text{Weight} = \alpha + \beta \times \text{Height} + \epsilon$$

Trong đó $$\epsilon \sim \mathcal{N}(0, \sigma^2)$$.

### 2.2. Generate Data

```python
# Generate synthetic data
np.random.seed(42)
n = 50

true_alpha = 50  # Intercept
true_beta = 0.7  # Slope
true_sigma = 5   # Noise

height = np.random.uniform(150, 190, n)
weight = true_alpha + true_beta * height + np.random.normal(0, true_sigma, n)

# Standardize for better sampling
height_std = (height - height.mean()) / height.std()
weight_std = (weight - weight.mean()) / weight.std()

# Visualize
plt.figure(figsize=(10, 6))
plt.scatter(height, weight, s=50, alpha=0.6, edgecolors='black')
plt.plot(height, true_alpha + true_beta * height, 'r-', linewidth=2,
        label=f'True: y = {true_alpha:.1f} + {true_beta:.2f}x')
plt.xlabel('Height (cm)', fontsize=12, fontweight='bold')
plt.ylabel('Weight (kg)', fontsize=12, fontweight='bold')
plt.title('Height vs Weight\n(Synthetic Data)', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.show()
```

### 2.3. Bayesian Linear Regression với PyMC

```python
with pm.Model() as linear_regression:
    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=10)
    beta = pm.Normal('beta', mu=0, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=1)
    
    # Linear model
    mu = alpha + beta * height_std
    
    # Likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=weight_std)
    
    # Sampling
    trace_lr = pm.sample(
        draws=2000,
        tune=1000,
        chains=4,
        random_seed=42,
        return_inferencedata=True
    )

# Summary
print("=" * 70)
print("LINEAR REGRESSION POSTERIOR SUMMARY")
print("=" * 70)
print(az.summary(trace_lr, var_names=['alpha', 'beta', 'sigma']))
print("=" * 70)

# Visualization
az.plot_trace(trace_lr, var_names=['alpha', 'beta', 'sigma'])
plt.tight_layout()
plt.show()
```

### 2.4. Posterior Predictive Distribution

Một trong những tính năng mạnh mẽ của Bayesian là **posterior predictive distribution** - phân phối dự đoán cho dữ liệu mới.

```python
# Posterior predictive samples
with linear_regression:
    ppc = pm.sample_posterior_predictive(trace_lr, random_seed=42)

# Visualize posterior predictive
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 1. Posterior predictive check
az.plot_ppc(ppc, ax=axes[0], num_pp_samples=100)
axes[0].set_title('Posterior Predictive Check\n' +
                 'Simulated data vs Observed data',
                 fontsize=14, fontweight='bold')

# 2. Regression lines with uncertainty
axes[1].scatter(height, weight, s=50, alpha=0.6, edgecolors='black',
               label='Observed Data')

# Draw posterior samples of regression lines
alpha_samples = trace_lr.posterior['alpha'].values.flatten()
beta_samples = trace_lr.posterior['beta'].values.flatten()

# Convert back to original scale
height_range = np.linspace(height.min(), height.max(), 100)
height_range_std = (height_range - height.mean()) / height.std()

for i in np.random.choice(len(alpha_samples), 100, replace=False):
    weight_pred_std = alpha_samples[i] + beta_samples[i] * height_range_std
    weight_pred = weight_pred_std * weight.std() + weight.mean()
    axes[1].plot(height_range, weight_pred, 'b-', alpha=0.02)

# True line
axes[1].plot(height_range, true_alpha + true_beta * height_range,
            'r-', linewidth=3, label='True Regression Line')

axes[1].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[1].set_title('Posterior Regression Lines\n' +
                 'Uncertainty quantification',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\n✓ Posterior predictive check tốt!")
print("  → Simulated data giống observed data")
print("  → Model fit hợp lý")
```

## 3. PyMC Workflow: Best Practices

### 3.1. Workflow Chuẩn

Khi làm việc với PyMC, hãy tuân theo workflow này:

```
1. Định nghĩa Model
   ↓
2. Prior Predictive Check (optional nhưng nên làm)
   ↓
3. Sample từ Posterior
   ↓
4. Convergence Diagnostics
   ↓
5. Posterior Predictive Check
   ↓
6. Inference và Interpretation
```

### 3.2. Prior Predictive Check

Trước khi fit model, hãy kiểm tra prior có hợp lý không bằng cách sample từ prior predictive distribution.

```python
# Prior predictive check
with linear_regression:
    prior_pred = pm.sample_prior_predictive(samples=1000, random_seed=42)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Prior distributions
az.plot_dist(prior_pred.prior['alpha'].values.flatten(), ax=axes[0],
            label='alpha', color='blue')
az.plot_dist(prior_pred.prior['beta'].values.flatten(), ax=axes[0],
            label='beta', color='red')
axes[0].set_title('Prior Distributions\nAlpha và Beta', 
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)

# Prior predictive
prior_pred_samples = prior_pred.prior_predictive['y_obs'].values
axes[1].hist(prior_pred_samples.flatten(), bins=50, density=True, alpha=0.7,
            color='skyblue', edgecolor='black')
axes[1].axvline(weight_std.mean(), color='red', linestyle='--', linewidth=2,
               label='Observed Mean')
axes[1].set_xlabel('Weight (standardized)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('Prior Predictive Distribution\n' +
                 'Dữ liệu mô phỏng từ prior',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\nPRIOR PREDICTIVE CHECK:")
print("-" * 70)
print("Kiểm tra xem prior có cho phép dữ liệu hợp lý không")
print("Nếu prior quá restrictive hoặc quá vague, cần điều chỉnh")
```

## 4. Khi nào Dùng PyMC?

### 4.1. Ưu điểm

✅ **Production-ready**: Stable, well-tested, widely used  
✅ **Modern algorithms**: NUTS, automatic tuning  
✅ **Rich ecosystem**: ArviZ, Bambi, PyMC-Marketing  
✅ **Flexible**: Có thể xây dựng mô hình phức tạp  
✅ **Community**: Active community, good documentation  

### 4.2. Nhược điểm

❌ **Learning curve**: Cần thời gian làm quen  
❌ **Performance**: Chậm hơn Stan trong một số trường hợp  
❌ **Debugging**: Khó debug khi model phức tạp  

### 4.3. Alternatives

- **Stan**: Faster, nhưng cần học Stan language
- **NumPyro**: JAX-based, rất nhanh, nhưng ít tài liệu hơn
- **TensorFlow Probability**: Tích hợp với TensorFlow ecosystem

## Tóm tắt và Kết nối

PyMC là công cụ mạnh mẽ để thực hành Bayesian modeling:

- **Declarative syntax**: Mô tả model gần với toán học
- **NUTS sampler**: Tự động, hiệu quả
- **ArviZ integration**: Diagnostics và visualization
- **Workflow**: Prior predictive → Sampling → Diagnostics → Posterior predictive

Với PyMC, bạn có thể tập trung vào **modeling** thay vì lo lắng về implementation details. Nhưng nhớ rằng: hiểu rõ MCMC từ các bài trước là thiết yếu để sử dụng PyMC hiệu quả!

## Bài tập

**Bài tập 1: Beta-Binomial**
(a) Implement Beta-Binomial với PyMC
(b) Thử các prior khác nhau: Beta(1,1), Beta(5,5), Beta(10,2)
(c) So sánh posteriors. Prior nào ảnh hưởng nhiều nhất?

**Bài tập 2: Linear Regression**
(a) Generate data với true_alpha=20, true_beta=1.5, true_sigma=3
(b) Fit Bayesian linear regression với PyMC
(c) Vẽ posterior regression lines với uncertainty
(d) Compute 95% credible interval cho beta

**Bài tập 3: Prior Predictive Check**
(a) Thử prior quá vague: Normal(0, 100) cho alpha và beta
(b) Thử prior quá restrictive: Normal(0, 0.1)
(c) Vẽ prior predictive distributions
(d) Prior nào hợp lý nhất? Tại sao?

**Bài tập 4: Diagnostics**
(a) Chạy model với chỉ 100 samples
(b) Kiểm tra R-hat, ESS, trace plots
(c) Có vấn đề gì không?
(d) Chạy lại với 2000 samples và so sánh

**Bài tập 5: Posterior Predictive Check**
(a) Fit linear regression model
(b) Generate posterior predictive samples
(c) So sánh với observed data
(d) Model có fit tốt không? Làm sao bạn biết?

## Tài liệu Tham khảo

### Primary References:

**PyMC Documentation**: https://www.pymc.io/
- Comprehensive tutorials và examples

**ArviZ Documentation**: https://python.arviz.org/
- Visualization và diagnostics

### Books:

**Martin, O. A., Kumar, R., & Lao, J. (2021).** *Bayesian Modeling and Computation in Python*. CRC Press.
- Sách chính thức về PyMC

**Gelman, A., et al. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Nền tảng lý thuyết

### Supplementary:

**PyMC Examples**: https://www.pymc.io/projects/examples/
- Nhiều ví dụ thực tế

**PyMC Discourse**: https://discourse.pymc.io/
- Community support

---

**🎉 CHÚC MỪNG! BẠN ĐÃ HOÀN THÀNH CHAPTER 03! 🎉**

Bạn đã học được:
- Sampling và Monte Carlo
- Markov Chains
- Metropolis-Hastings
- Hamiltonian Monte Carlo
- MCMC Diagnostics
- PyMC Implementation

Bạn giờ đã sẵn sàng để áp dụng Bayesian statistics vào các vấn đề thực tế! 🚀
