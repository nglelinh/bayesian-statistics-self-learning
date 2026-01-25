---
layout: post
title: "Bài 4.2: Priors for Regression - Chọn Prior có Nguyên tắc"
chapter: '04'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ biết cách chọn **priors hợp lý** cho regression models - một trong những kỹ năng quan trọng nhất trong Bayesian modeling. Bạn sẽ học về weakly informative priors, prior predictive checks, và tầm quan trọng của standardization. Quan trọng hơn, bạn sẽ hiểu rằng chọn prior không phải là "arbitrary" hay "subjective", mà là một quy trình có nguyên tắc dựa trên domain knowledge và regularization.

## Giới thiệu: Prior Selection - Nghệ thuật và Khoa học

Một trong những câu hỏi phổ biến nhất về Bayesian statistics là: **"Làm sao tôi biết prior nào là 'đúng'?"**

Câu trả lời ngắn gọn: **Không có prior "đúng" duy nhất**. Nhưng có priors **hợp lý** và priors **không hợp lý**.

Prior selection là sự kết hợp giữa:
- **Domain knowledge**: Hiểu biết về vấn đề
- **Regularization**: Tránh overfitting
- **Computational stability**: Giúp MCMC hội tụ
- **Prior predictive checks**: Kiểm tra prior có hợp lý không

Trong bài này, chúng ta sẽ học cách chọn priors cho 3 parameters trong linear regression: intercept ($$\alpha$$), slope ($$\beta$$), và noise ($$\sigma$$).

## 1. Standardization: Bước Đầu Quan trọng

![Standardization Comparison]({{ site.baseurl }}/img/chapter_img/chapter04/standardization_comparison.png)

Trước khi chọn priors, **standardize data** là cực kỳ quan trọng.

### 1.1. Tại sao Standardize?

**Vấn đề với raw data**:
- Scales khác nhau (ví dụ: chiều cao 150-190 cm, cân nặng 50-90 kg)
- Prior phụ thuộc vào units (cm vs m, kg vs pounds)
- Khó chọn prior "reasonable"

**Giải pháp: Standardization (Z-score)**:

$$x_{\text{std}} = \frac{x - \bar{x}}{\text{SD}(x)}$$

$$y_{\text{std}} = \frac{y - \bar{y}}{\text{SD}(y)}$$

**Lợi ích**:
- Mean = 0, SD = 1 cho cả $$x$$ và $$y$$
- Priors không phụ thuộc units
- Intercept có ý nghĩa rõ ràng ($$y$$ tại $$x$$ trung bình)
- MCMC hội tụ nhanh hơn

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Generate example data
np.random.seed(42)
n = 50
height = np.random.uniform(150, 190, n)  # cm
weight = 50 + 0.7 * height + np.random.normal(0, 5, n)  # kg

# Standardize
height_std = (height - height.mean()) / height.std()
weight_std = (weight - weight.mean()) / weight.std()

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Raw data
axes[0].scatter(height, weight, s=80, alpha=0.6, edgecolors='black')
axes[0].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0].set_title('Raw Data\n' +
                 f'Height: [{height.min():.0f}, {height.max():.0f}] cm\n' +
                 f'Weight: [{weight.min():.0f}, {weight.max():.0f}] kg',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)

# Standardized data
axes[1].scatter(height_std, weight_std, s=80, alpha=0.6, edgecolors='black')
axes[1].axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
axes[1].axvline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
axes[1].set_xlabel('Height (standardized)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Weight (standardized)', fontsize=12, fontweight='bold')
axes[1].set_title('Standardized Data\n' +
                 f'Both: mean=0, SD=1',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("=" * 70)
print("STANDARDIZATION")
print("=" * 70)
print(f"\nRaw Data:")
print(f"  Height: mean={height.mean():.1f}, SD={height.std():.1f}")
print(f"  Weight: mean={weight.mean():.1f}, SD={weight.std():.1f}")
print(f"\nStandardized Data:")
print(f"  Height: mean={height_std.mean():.2f}, SD={height_std.std():.2f}")
print(f"  Weight: mean={weight_std.mean():.2f}, SD={weight_std.std():.2f}")
print("\n→ Bây giờ có thể dùng priors 'standard' cho cả hai!")
print("=" * 70)
```

## 2. Priors cho Intercept ($$\alpha$$)

Sau khi standardize, intercept ($$\alpha$$) là **giá trị trung bình của $$y$$ tại $$x$$ trung bình**.

### 2.1. Weakly Informative Prior

**Khuyến nghị**: $$\alpha \sim \mathcal{N}(0, 1)$$ hoặc $$\mathcal{N}(0, 2)$$

**Lý do**:
- Data đã standardized → $$\alpha$$ nên gần 0
- SD = 1 hoặc 2 cho phép flexibility hợp lý
- Không quá restrictive, không quá vague

```python
# Visualize priors for intercept
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

theta_range = np.linspace(-6, 6, 1000)

priors = [
    (stats.norm(0, 5), 'N(0, 5)', 'Too wide', 'red'),
    (stats.norm(0, 1), 'N(0, 1)', 'Weakly informative ✓', 'green'),
    (stats.norm(0, 0.1), 'N(0, 0.1)', 'Too narrow', 'orange')
]

for ax, (prior, label, title, color) in zip(axes, priors):
    pdf = prior.pdf(theta_range)
    ax.plot(theta_range, pdf, linewidth=3, color=color)
    ax.fill_between(theta_range, pdf, alpha=0.3, color=color)
    ax.set_xlabel('α', fontsize=12, fontweight='bold')
    ax.set_ylabel('Density', fontsize=12, fontweight='bold')
    ax.set_title(f'{title}\nα ~ {label}', fontsize=13, fontweight='bold')
    ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\nPRIOR FOR INTERCEPT (α):")
print("-" * 70)
print("✗ N(0, 5):   Too wide - cho phép α = ±10 (vô lý với standardized data)")
print("✓ N(0, 1):   Weakly informative - hợp lý, flexible")
print("✗ N(0, 0.1): Too narrow - quá restrictive, ảnh hưởng nhiều đến posterior")
print("-" * 70)
```

![Prior Selection for Regression]({{ site.baseurl }}/img/chapter_img/chapter04/prior_selection.png)

## 3. Priors cho Slope ($$\beta$$)

Slope ($$\beta$$) đo lường **mức độ thay đổi của $$y$$ khi $$x$$ thay đổi 1 SD**.

### 3.1. Weakly Informative Prior

**Khuyến nghị**: $$\beta \sim \mathcal{N}(0, 1)$$

**Lý do**:
- Với standardized data, $$\beta$$ thường trong khoảng [-2, 2]
- $$\mathcal{N}(0, 1)$$ cho 95% mass trong [-2, 2]
- Regularization: Tránh slopes quá extreme

### 3.2. Prior Predictive Check

![Prior Predictive Check]({{ site.baseurl }}/img/chapter_img/chapter04/prior_predictive_check.png)

Hãy kiểm tra prior có hợp lý không bằng cách sample từ prior predictive distribution.

```python
# Prior predictive check
n_samples = 100
x_range = np.linspace(-3, 3, 100)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Prior 1: N(0, 1) - Weakly informative
alpha_samples = np.random.normal(0, 1, n_samples)
beta_samples = np.random.normal(0, 1, n_samples)

for i in range(n_samples):
    y_pred = alpha_samples[i] + beta_samples[i] * x_range
    axes[0].plot(x_range, y_pred, 'b-', alpha=0.1, linewidth=1)

axes[0].set_xlabel('x (standardized)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('y (standardized)', fontsize=12, fontweight='bold')
axes[0].set_title('Prior Predictive: β ~ N(0, 1)\n' +
                 'Weakly informative ✓',
                 fontsize=14, fontweight='bold', color='green')
axes[0].set_ylim(-6, 6)
axes[0].grid(alpha=0.3)

# Prior 2: N(0, 5) - Too wide
beta_samples_wide = np.random.normal(0, 5, n_samples)

for i in range(n_samples):
    y_pred = alpha_samples[i] + beta_samples_wide[i] * x_range
    axes[1].plot(x_range, y_pred, 'r-', alpha=0.1, linewidth=1)

axes[1].set_xlabel('x (standardized)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('y (standardized)', fontsize=12, fontweight='bold')
axes[1].set_title('Prior Predictive: β ~ N(0, 5)\n' +
                 'Too wide - cho phép slopes vô lý ✗',
                 fontsize=14, fontweight='bold', color='red')
axes[1].set_ylim(-6, 6)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\nPRIOR PREDICTIVE CHECK:")
print("-" * 70)
print("β ~ N(0, 1): Slopes hợp lý, không quá extreme")
print("β ~ N(0, 5): Slopes quá wild, cho phép relationships vô lý")
print("\n→ Prior predictive check giúp phát hiện priors không hợp lý!")
print("-" * 70)
```

## 4. Priors cho Noise ($$\sigma$$)

Noise ($$\sigma$$) đo lường **độ biến động** xung quanh regression line.

### 4.1. HalfNormal Prior

**Khuyến nghị**: $$\sigma \sim \text{HalfNormal}(1)$$

**Lý do**:
- $$\sigma > 0$$ (must be positive)
- HalfNormal(1) cho phép $$\sigma$$ từ 0 đến ~3
- Với standardized data, $$\sigma$$ thường < 1 (nếu model fit tốt)

```python
# Visualize prior for sigma
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sigma_range = np.linspace(0, 5, 1000)

# HalfNormal(1)
prior_sigma = stats.halfnorm(0, 1).pdf(sigma_range)
axes[0].plot(sigma_range, prior_sigma, linewidth=3, color='blue')
axes[0].fill_between(sigma_range, prior_sigma, alpha=0.3, color='blue')
axes[0].set_xlabel('σ', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('Prior for σ\nσ ~ HalfNormal(1)',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)

# Interpretation
axes[1].axis('off')
interpretation = """
╔═══════════════════════════════════════════════════════════╗
║              PRIOR FOR NOISE (σ)                          ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  σ ~ HalfNormal(1)                                        ║
║                                                           ║
║  Ý nghĩa:                                                 ║
║    • σ > 0 (must be positive)                             ║
║    • 95% mass trong [0, 2]                                ║
║    • Cho phép flexibility hợp lý                          ║
║                                                           ║
║  Với standardized data:                                   ║
║    • σ < 0.5: Model fit rất tốt                           ║
║    • σ ≈ 1:   Model fit trung bình                        ║
║    • σ > 2:   Model fit kém                               ║
║                                                           ║
║  Alternatives:                                            ║
║    • Exponential(1)                                       ║
║    • HalfCauchy(1) (heavier tails)                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[1].text(0.5, 0.5, interpretation, fontsize=10, family='monospace',
               ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9))

plt.tight_layout()
plt.show()
```

## 5. Summary: Recommended Priors

Với **standardized data** (mean=0, SD=1):

```python
# RECOMMENDED PRIORS FOR STANDARDIZED LINEAR REGRESSION

α ~ Normal(0, 1)           # Intercept
β ~ Normal(0, 1)           # Slope
σ ~ HalfNormal(1)          # Noise
```

**Lý do**:
- **Weakly informative**: Không quá restrictive, không quá vague
- **Regularization**: Tránh overfitting
- **Computational stability**: MCMC hội tụ tốt
- **Domain-agnostic**: Hoạt động tốt cho nhiều problems

## 6. Prior Sensitivity Analysis

Luôn luôn kiểm tra **prior sensitivity** - posterior có thay đổi nhiều khi prior thay đổi không?

```python
# Simulate posterior with different priors (simplified illustration)
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# True posterior (giả định)
beta_true = 0.7
beta_range = np.linspace(-1, 2, 1000)

# Different priors
priors_to_test = [
    (stats.norm(0, 0.5), 'N(0, 0.5)', 'narrow'),
    (stats.norm(0, 1), 'N(0, 1)', 'weakly informative'),
    (stats.norm(0, 2), 'N(0, 2)', 'wide')
]

# Simulate posteriors (simplified: prior + likelihood)
for prior, label, desc in priors_to_test:
    # Simplified posterior (not exact)
    posterior = stats.norm(beta_true, 0.1).pdf(beta_range) * prior.pdf(beta_range)
    posterior = posterior / np.trapz(posterior, beta_range)
    
    axes[0].plot(beta_range, posterior, linewidth=2, label=f'Prior: {label}')

axes[0].axvline(beta_true, color='red', linestyle='--', linewidth=2,
               label=f'True β = {beta_true}')
axes[0].set_xlabel('β', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Posterior Density', fontsize=12, fontweight='bold')
axes[0].set_title('Prior Sensitivity Analysis\n' +
                 'Posterior với priors khác nhau',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Summary
axes[1].axis('off')
summary = """
╔═══════════════════════════════════════════════════════════╗
║           PRIOR SENSITIVITY ANALYSIS                      ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Câu hỏi:                                                 ║
║    Posterior có thay đổi nhiều khi prior thay đổi?       ║
║                                                           ║
║  Nếu YES (sensitive):                                     ║
║    • Data ít hoặc weak                                    ║
║    • Prior có ảnh hưởng lớn                               ║
║    • Cần cẩn thận chọn prior                              ║
║    • Report sensitivity analysis                          ║
║                                                           ║
║  Nếu NO (robust):                                         ║
║    • Data nhiều và strong                                 ║
║    • Prior ít ảnh hưởng                                   ║
║    • Posterior chủ yếu từ likelihood                      ║
║    • Prior choice ít quan trọng                           ║
║                                                           ║
║  Best practice:                                           ║
║    → LUÔN kiểm tra prior sensitivity                      ║
║    → Report kết quả với multiple priors                   ║
║    → Nếu sensitive, justify prior choice                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[1].text(0.5, 0.5, summary, fontsize=10, family='monospace',
               ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.show()
```

## Tóm tắt và Kết nối

Chọn priors cho regression là có nguyên tắc:

1. **Standardize data** trước tiên
2. **Weakly informative priors**:
   - $$\alpha \sim \mathcal{N}(0, 1)$$
   - $$\beta \sim \mathcal{N}(0, 1)$$
   - $$\sigma \sim \text{HalfNormal}(1)$$
3. **Prior predictive check**: Kiểm tra priors có hợp lý
4. **Sensitivity analysis**: Kiểm tra robustness

Trong bài tiếp theo, chúng ta sẽ implement Bayesian regression với PyMC và những priors này.

## Bài tập

**Bài tập 1: Standardization**
(a) Tại sao standardization quan trọng cho prior selection?
(b) Implement standardization trong Python
(c) Intercept có ý nghĩa gì sau standardization?

**Bài tập 2: Prior Predictive Check**
(a) Generate 100 regression lines từ priors: α~N(0,1), β~N(0,1)
(b) Vẽ prior predictive distribution
(c) Có hợp lý không? Tại sao?

**Bài tập 3: Prior Sensitivity**
(a) Chạy regression với β ~ N(0, 0.5), N(0, 1), N(0, 2)
(b) So sánh posteriors
(c) Prior nào ảnh hưởng nhiều nhất?

**Bài tập 4: Sigma Prior**
(a) Tại sao dùng HalfNormal thay vì Normal cho σ?
(b) So sánh HalfNormal(1) vs Exponential(1)
(c) Prior nào flexible hơn?

**Bài tập 5: Domain Knowledge**
Cho scenario: Dự đoán điểm thi (0-100) từ số giờ học (0-50).
(a) Bạn sẽ standardize như thế nào?
(b) Priors nào hợp lý cho α, β, σ?
(c) Prior predictive check sẽ như thế nào?

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Simpson, D., & Betancourt, M. (2017).** *The prior can often only be understood in the context of the likelihood*. Entropy, 19(10), 555.

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 4.4: Linear models

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 9: Prediction and Bayesian inference

---

*Bài học tiếp theo: [4.3 Posterior Inference với PyMC](/vi/chapter04/posterior-inference-pymc/)*
