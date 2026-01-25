---
layout: post
title: "Bài 5.3: Multicollinearity - Khi Predictors Tương quan"
chapter: '05'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter05
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu về **multicollinearity** - vấn đề khi predictors correlate cao với nhau. Bạn sẽ học cách nhận biết multicollinearity, hiểu tại sao nó là vấn đề, và biết cách xử lý. Quan trọng hơn, bạn sẽ hiểu rằng multicollinearity không phải lúc nào cũng là "bad" - nó phụ thuộc vào mục tiêu phân tích.

## Giới thiệu: Vấn đề của Predictors Tương quan

Trong multiple regression, chúng ta giả định mỗi predictor đóng góp **độc lập** vào outcome. Nhưng điều gì xảy ra khi hai predictors **correlate cao** với nhau?

**Ví dụ**: Dự đoán cân nặng từ:
- Chiều cao (cm)
- Chiều cao (inches)

Rõ ràng hai predictors này **hoàn toàn tương quan** (r ≈ 1). Làm sao model có thể tách biệt effect của mỗi cái?

**Câu trả lời**: Không thể! Đây là **multicollinearity**.

## 1. Multicollinearity là gì?

![Multicollinearity Effects]({{ site.baseurl }}/img/chapter_img/chapter05/multicollinearity_effects.png)

### 1.1. Định nghĩa

**Multicollinearity** xảy ra khi:
- Hai hoặc nhiều predictors **correlate cao** với nhau
- Một predictor có thể được dự đoán tốt từ các predictors khác

**Hậu quả**:
- Coefficients có **high uncertainty** (wide credible intervals)
- Coefficients có thể có **unexpected signs**
- Model predictions vẫn tốt, nhưng interpretation khó

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
from scipy import stats

# Demonstrate multicollinearity
np.random.seed(42)
n = 100

# Generate correlated predictors
x1 = np.random.normal(0, 1, n)
x2 = 0.95 * x1 + np.random.normal(0, 0.1, n)  # High correlation with x1

# Outcome depends on both
y = 2 + 3*x1 + 2*x2 + np.random.normal(0, 1, n)

# Visualize correlation
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. x1 vs x2 (high correlation)
axes[0].scatter(x1, x2, s=50, alpha=0.6, edgecolors='black')
corr = np.corrcoef(x1, x2)[0, 1]
axes[0].set_xlabel('x₁', fontsize=12, fontweight='bold')
axes[0].set_ylabel('x₂', fontsize=12, fontweight='bold')
axes[0].set_title(f'Predictors Correlation\nr = {corr:.3f} (HIGH!)',
                 fontsize=14, fontweight='bold', color='red')
axes[0].grid(alpha=0.3)

# 2. Both predict y well individually
axes[1].scatter(x1, y, s=50, alpha=0.6, label='x₁ vs y', edgecolors='black')
axes[1].scatter(x2, y, s=50, alpha=0.6, label='x₂ vs y', edgecolors='black')
axes[1].set_xlabel('Predictor', fontsize=12, fontweight='bold')
axes[1].set_ylabel('y', fontsize=12, fontweight='bold')
axes[1].set_title('Both Predictors Correlate with y\n' +
                 'Hard to separate their effects!',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

# 3. Problem illustration
axes[2].axis('off')
problem = """
╔═══════════════════════════════════════════════╗
║        MULTICOLLINEARITY PROBLEM              ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  Khi x₁ và x₂ correlate cao:                  ║
║                                               ║
║  Vấn đề:                                      ║
║    • Không thể tách biệt effects              ║
║    • Coefficients có high uncertainty         ║
║    • Interpretation khó khăn                  ║
║                                               ║
║  Tại sao?                                     ║
║    Khi x₁ tăng, x₂ cũng tăng                  ║
║    → Effect của x₁ hay x₂?                    ║
║    → Model không biết!                        ║
║                                               ║
║  Lưu ý:                                       ║
║    • Predictions vẫn tốt                      ║
║    • Chỉ interpretation bị ảnh hưởng          ║
║                                               ║
╚═══════════════════════════════════════════════╝
"""
axes[2].text(0.5, 0.5, problem, fontsize=10, family='monospace',
            ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.show()

print("=" * 70)
print("MULTICOLLINEARITY EXAMPLE")
print("=" * 70)
print(f"\nCorrelation between x₁ and x₂: r = {corr:.3f}")
print(f"True coefficients: β₁ = 3, β₂ = 2")
print("\n→ Let's see what happens when we fit the model...")
print("=" * 70)
```

### 1.2. Fit Model với Multicollinearity

```python
# Fit Bayesian regression
with pm.Model() as model_collinear:
    # Priors
    alpha = pm.Normal('alpha', 0, 5)
    beta1 = pm.Normal('beta1', 0, 5)
    beta2 = pm.Normal('beta2', 0, 5)
    sigma = pm.HalfNormal('sigma', 2)
    
    # Linear model
    mu = alpha + beta1*x1 + beta2*x2
    
    # Likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
    
    # Sample
    trace = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                     return_inferencedata=True)

# Summary
print("\n" + "=" * 70)
print("POSTERIOR WITH MULTICOLLINEARITY")
print("=" * 70)
summary = az.summary(trace, var_names=['beta1', 'beta2'])
print(summary)
print("=" * 70)

# Extract posteriors
beta1_samples = trace.posterior['beta1'].values.flatten()
beta2_samples = trace.posterior['beta2'].values.flatten()

# Visualize
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Beta1 posterior
axes[0].hist(beta1_samples, bins=50, density=True, alpha=0.7,
            color='skyblue', edgecolor='black')
axes[0].axvline(beta1_samples.mean(), color='red', linewidth=2,
               label=f'Mean = {beta1_samples.mean():.2f}')
axes[0].axvline(3, color='green', linestyle='--', linewidth=2,
               label='True = 3')
axes[0].set_xlabel('β₁', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title(f'Posterior: β₁\nSD = {beta1_samples.std():.2f} (HIGH!)',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')

# Beta2 posterior
axes[1].hist(beta2_samples, bins=50, density=True, alpha=0.7,
            color='lightgreen', edgecolor='black')
axes[1].axvline(beta2_samples.mean(), color='red', linewidth=2,
               label=f'Mean = {beta2_samples.mean():.2f}')
axes[1].axvline(2, color='green', linestyle='--', linewidth=2,
               label='True = 2')
axes[1].set_xlabel('β₂', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title(f'Posterior: β₂\nSD = {beta2_samples.std():.2f} (HIGH!)',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3, axis='y')

# Joint posterior (negative correlation!)
axes[2].scatter(beta1_samples, beta2_samples, s=1, alpha=0.3)
axes[2].axvline(3, color='green', linestyle='--', linewidth=2)
axes[2].axhline(2, color='green', linestyle='--', linewidth=2)
axes[2].set_xlabel('β₁', fontsize=12, fontweight='bold')
axes[2].set_ylabel('β₂', fontsize=12, fontweight='bold')
axes[2].set_title('Joint Posterior\nNegative correlation!',
                 fontsize=14, fontweight='bold')
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\nOBSERVATIONS:")
print("-" * 70)
print("1. Wide posteriors (high uncertainty)")
print("2. Means may not match true values")
print("3. β₁ and β₂ negatively correlated in posterior")
print("   → When β₁ high, β₂ low (and vice versa)")
print("   → Many combinations give same predictions!")
print("-" * 70)
```

## 2. Tại sao Multicollinearity là Vấn đề?

### 2.1. High Uncertainty

Khi predictors correlate cao, model không thể tách biệt effects → **wide credible intervals**.

### 2.2. Unstable Estimates

Coefficients có thể thay đổi nhiều với small changes in data.

### 2.3. Interpretation Khó

"Effect của x₁ holding x₂ constant" không có ý nghĩa khi x₁ và x₂ luôn thay đổi cùng nhau.

## 3. Giải pháp

### 3.1. Option 1: Remove One Predictor

Nếu hai predictors measure cùng một concept → giữ một, bỏ một.

### 3.2. Option 2: Combine Predictors

Tạo composite variable (e.g., average, PCA).

### 3.3. Option 3: Regularization Priors

Sử dụng priors mạnh hơn để "shrink" coefficients (Chapter 07).

### 3.4. Option 4: Accept It!

Nếu mục tiêu là **prediction**, multicollinearity không phải vấn đề lớn.

```python
# Compare: With vs Without one predictor
# Model without x2
with pm.Model() as model_no_collinear:
    alpha = pm.Normal('alpha', 0, 5)
    beta1 = pm.Normal('beta1', 0, 5)
    sigma = pm.HalfNormal('sigma', 2)
    
    mu = alpha + beta1*x1
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
    
    trace_no = pm.sample(1000, tune=500, chains=2, random_seed=42,
                        return_inferencedata=True, progressbar=False)

beta1_no = trace_no.posterior['beta1'].values.flatten()

print("\n" + "=" * 70)
print("COMPARISON")
print("=" * 70)
print(f"\nWith both x₁ and x₂ (multicollinearity):")
print(f"  β₁: {beta1_samples.mean():.2f} ± {beta1_samples.std():.2f}")
print(f"  (Wide uncertainty)")

print(f"\nWith only x₁ (no multicollinearity):")
print(f"  β₁: {beta1_no.mean():.2f} ± {beta1_no.std():.2f}")
print(f"  (Narrow uncertainty)")

print(f"\n→ Removing correlated predictor reduces uncertainty!")
print("=" * 70)
```

## Tóm tắt

Multicollinearity xảy ra khi predictors correlate cao:

- **Vấn đề**: Wide credible intervals, interpretation khó
- **Không phải vấn đề**: Predictions vẫn tốt
- **Giải pháp**: Remove predictor, combine, regularization, hoặc accept it

**Key insight**: Multicollinearity chỉ là vấn đề nếu mục tiêu là **interpretation**. Nếu chỉ cần **prediction**, không sao!

Bài tiếp theo: **Interaction Effects** - khi effects phụ thuộc nhau.

## Bài tập

**Bài tập 1**: Generate data với perfect multicollinearity (r=1). Fit model và observe posteriors.

**Bài tập 2**: So sánh uncertainty với r = 0.3, 0.6, 0.9. Khi nào multicollinearity trở thành vấn đề?

**Bài tập 3**: Prediction accuracy với và không có multicollinearity. Có khác biệt không?

## Tài liệu Tham khảo

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 11: Assumptions, diagnostics, and model evaluation

---

*Bài học tiếp theo: [5.4 Interaction Effects](/vi/chapter05/interaction-effects/)*
