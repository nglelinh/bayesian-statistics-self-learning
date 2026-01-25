---
layout: post
title: "Bài 4.1: Bayesian Linear Regression - Mô hình Sinh dữ liệu"
chapter: '04'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **hồi quy tuyến tính Bayesian** không chỉ là công cụ tìm "đường thẳng phù hợp nhất", mà là một **generative model** - một câu chuyện về cách dữ liệu được sinh ra. Bạn sẽ học cách suy nghĩ về regression như một data-generating process, với uncertainty ở mọi nơi: trong parameters, trong predictions, và trong model itself. Đây là bước chuyển quan trọng từ "fitting a line" sang "modeling a process".

## Giới thiệu: Regression - Hai Cách Nhìn

![Frequentist vs Bayesian Regression]({{ site.baseurl }}/img/chapter_img/chapter04/frequentist_vs_bayesian_regression.png)

Hầu hết chúng ta đã học linear regression theo cách frequentist:

**Frequentist view**: Tìm đường thẳng $$y = \beta_0 + \beta_1 x$$ sao cho tổng bình phương sai số (sum of squared errors) nhỏ nhất. Kết quả là một ước lượng điểm cho $$\beta_0$$ và $$\beta_1$$, kèm theo standard errors và p-values.

Cách tiếp cận này hoạt động tốt trong nhiều trường hợp, nhưng nó có những hạn chế:
- Chỉ cho ta **point estimates**, không phải distributions
- P-values khó diễn giải (nhớ lại Chapter 01!)
- Không tự nhiên cho phép incorporate prior knowledge
- Khó mở rộng cho models phức tạp

**Bayesian view**: Regression là một **generative model** - một câu chuyện về cách dữ liệu được sinh ra:

1. Có một mối quan hệ tuyến tính giữa $$x$$ và $$y$$
2. Mỗi quan sát dao động xung quanh đường thẳng này
3. Chúng ta không chắc chắn về parameters (slope, intercept, noise)
4. Posterior distribution cho ta **full uncertainty** về parameters và predictions

Trong bài này, chúng ta sẽ học cách xây dựng và hiểu Bayesian linear regression như một generative model.

## 1. Generative Story: Dữ liệu Được Sinh Ra Như Thế Nào?

![Linear Regression: Generative Model]({{ site.baseurl }}/img/chapter_img/chapter04/linear_regression_generative.png)

### 1.1. Câu chuyện Sinh dữ liệu

Hãy tưởng tượng chúng ta muốn mô hình hóa mối quan hệ giữa **chiều cao** ($$x$$) và **cân nặng** ($$y$$) của người trưởng thành.

**Câu chuyện generative**:

1. **Có một mối quan hệ tuyến tính**: Trung bình, người cao hơn nặng hơn
   $$\mu_i = \alpha + \beta \cdot x_i$$
   
   Trong đó:
   - $$\alpha$$: Intercept - cân nặng khi chiều cao = 0 (không thực tế, nhưng là tham số toán học)
   - $$\beta$$: Slope - cân nặng tăng bao nhiêu khi chiều cao tăng 1 cm

2. **Mỗi người dao động xung quanh giá trị trung bình**: Không phải ai cũng nặng đúng bằng $$\mu_i$$
   $$y_i \sim \mathcal{N}(\mu_i, \sigma)$$
   
   Trong đó:
   - $$\sigma$$: Standard deviation - độ biến động xung quanh đường thẳng

3. **Chúng ta không chắc chắn về parameters**: $$\alpha$$, $$\beta$$, $$\sigma$$ là unknown
   - Prior: $$\alpha \sim \mathcal{N}(\mu_\alpha, \sigma_\alpha)$$
   - Prior: $$\beta \sim \mathcal{N}(\mu_\beta, \sigma_\beta)$$
   - Prior: $$\sigma \sim \text{HalfNormal}(\sigma_\sigma)$$

**Đây là một câu chuyện hoàn chỉnh về data-generating process!**

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Minh họa: Generative Story
np.random.seed(42)

# True parameters (trong thực tế không biết)
true_alpha = 50  # kg (intercept)
true_beta = 0.7  # kg/cm (slope)
true_sigma = 5   # kg (noise)

# Generate data
n = 50
height = np.random.uniform(150, 190, n)  # cm
weight = true_alpha + true_beta * height + np.random.normal(0, true_sigma, n)  # kg

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Data-generating process
axes[0, 0].scatter(height, weight, s=80, alpha=0.6, edgecolors='black')
height_line = np.linspace(height.min(), height.max(), 100)
weight_line = true_alpha + true_beta * height_line
axes[0, 0].plot(height_line, weight_line, 'r-', linewidth=3, 
               label=f'True: y = {true_alpha:.1f} + {true_beta:.2f}x')

# Show uncertainty bands
for i in [1, 2]:
    axes[0, 0].fill_between(height_line, 
                            weight_line - i*true_sigma,
                            weight_line + i*true_sigma,
                            alpha=0.15, color='red')

axes[0, 0].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0, 0].set_title('Data-Generating Process\n' +
                     f'μ = {true_alpha} + {true_beta}·x, σ = {true_sigma}',
                     fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=11)
axes[0, 0].grid(alpha=0.3)

# 2. Generative story
axes[0, 1].axis('off')
story = f"""
╔═══════════════════════════════════════════════════════════╗
║           GENERATIVE STORY: HEIGHT → WEIGHT              ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Bước 1: Mối quan hệ tuyến tính                           ║
║    μᵢ = α + β·xᵢ                                          ║
║    α = {true_alpha:.1f} kg (intercept)                             ║
║    β = {true_beta:.2f} kg/cm (slope)                              ║
║                                                           ║
║  Bước 2: Mỗi người dao động xung quanh μᵢ                 ║
║    yᵢ ~ Normal(μᵢ, σ)                                     ║
║    σ = {true_sigma:.1f} kg (noise)                                ║
║                                                           ║
║  Ý nghĩa:                                                 ║
║    • Người cao 170cm: μ = {true_alpha + true_beta*170:.1f} kg                  ║
║    • Nhưng cân nặng thực tế dao động ±{true_sigma}kg              ║
║    • 68% trong [{true_alpha + true_beta*170 - true_sigma:.1f}, {true_alpha + true_beta*170 + true_sigma:.1f}]                    ║
║    • 95% trong [{true_alpha + true_beta*170 - 2*true_sigma:.1f}, {true_alpha + true_beta*170 + 2*true_sigma:.1f}]                    ║
║                                                           ║
║  Điều chúng ta KHÔNG biết:                                ║
║    → α, β, σ là UNKNOWN                                   ║
║    → Cần estimate từ data                                 ║
║    → Bayesian: Posterior distribution!                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[0, 1].text(0.5, 0.5, story, fontsize=9.5, family='monospace',
               ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9))

# 3. Distribution of y for specific x
x_example = 170
mu_example = true_alpha + true_beta * x_example
y_range = np.linspace(mu_example - 4*true_sigma, mu_example + 4*true_sigma, 1000)
y_pdf = stats.norm(mu_example, true_sigma).pdf(y_range)

axes[1, 0].plot(y_pdf, y_range, linewidth=3, color='blue')
axes[1, 0].fill_betweenx(y_range, 0, y_pdf, alpha=0.3, color='blue')
axes[1, 0].axhline(mu_example, color='red', linestyle='--', linewidth=2,
                   label=f'μ = {mu_example:.1f} kg')
axes[1, 0].axhline(mu_example - true_sigma, color='orange', linestyle=':', linewidth=2)
axes[1, 0].axhline(mu_example + true_sigma, color='orange', linestyle=':', linewidth=2,
                   label=f'μ ± σ')
axes[1, 0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Probability Density', fontsize=12, fontweight='bold')
axes[1, 0].set_title(f'Distribution of Weight\nfor Height = {x_example} cm',
                     fontsize=14, fontweight='bold')
axes[1, 0].legend(fontsize=11)
axes[1, 0].grid(alpha=0.3)

# 4. Residuals
residuals = weight - (true_alpha + true_beta * height)
axes[1, 1].hist(residuals, bins=15, density=True, alpha=0.7,
               color='skyblue', edgecolor='black', label='Observed Residuals')
x_resid = np.linspace(residuals.min(), residuals.max(), 1000)
axes[1, 1].plot(x_resid, stats.norm(0, true_sigma).pdf(x_resid),
               'r-', linewidth=3, label=f'Theoretical: N(0, {true_sigma})')
axes[1, 1].set_xlabel('Residual (kg)', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1, 1].set_title('Residuals Distribution\n' +
                     'Should be ~ Normal(0, σ)',
                     fontsize=14, fontweight='bold')
axes[1, 1].legend(fontsize=11)
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("=" * 70)
print("GENERATIVE MODEL: HEIGHT → WEIGHT")
print("=" * 70)
print(f"\nTrue Parameters:")
print(f"  α (intercept) = {true_alpha:.2f} kg")
print(f"  β (slope)     = {true_beta:.2f} kg/cm")
print(f"  σ (noise)     = {true_sigma:.2f} kg")
print(f"\nInterpretation:")
print(f"  - Mỗi cm chiều cao tăng → cân nặng tăng {true_beta:.2f} kg (trung bình)")
print(f"  - Độ biến động cá nhân: ±{true_sigma:.2f} kg")
print(f"\nExample:")
print(f"  Height = 170 cm → Weight ~ N({mu_example:.1f}, {true_sigma:.1f})")
print(f"  → 95% probability: [{mu_example - 2*true_sigma:.1f}, {mu_example + 2*true_sigma:.1f}] kg")
print("=" * 70)
```

### 1.2. So sánh: Frequentist vs Bayesian

```python
# So sánh hai cách tiếp cận
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Frequentist: Point estimate
from scipy.stats import linregress
slope_freq, intercept_freq, r_value, p_value, std_err = linregress(height, weight)

axes[0].scatter(height, weight, s=80, alpha=0.6, edgecolors='black')
axes[0].plot(height_line, intercept_freq + slope_freq * height_line,
            'r-', linewidth=3, label=f'OLS: y = {intercept_freq:.1f} + {slope_freq:.2f}x')
axes[0].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0].set_title('Frequentist: Point Estimate\n' +
                 f'R² = {r_value**2:.3f}, p < 0.001',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Bayesian: Uncertainty
axes[1].scatter(height, weight, s=80, alpha=0.6, edgecolors='black',
               label='Observed Data')
# Simulate posterior samples (giả định)
n_samples = 100
alpha_samples = np.random.normal(intercept_freq, 5, n_samples)
beta_samples = np.random.normal(slope_freq, 0.05, n_samples)

for i in range(n_samples):
    axes[1].plot(height_line, alpha_samples[i] + beta_samples[i] * height_line,
                'b-', alpha=0.05, linewidth=1)

axes[1].plot(height_line, intercept_freq + slope_freq * height_line,
            'r-', linewidth=3, label='Posterior Mean')
axes[1].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[1].set_title('Bayesian: Uncertainty Quantification\n' +
                 'Posterior distribution of regression lines',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\nSO SÁNH:")
print("-" * 70)
print("Frequentist:")
print(f"  - Point estimate: β = {slope_freq:.3f} ± {std_err:.3f}")
print(f"  - P-value: {p_value:.2e}")
print(f"  - Diễn giải: 'Nếu β=0, xác suất thấy data này là...'")
print("\nBayesian:")
print(f"  - Posterior distribution: β ~ N({slope_freq:.3f}, {std_err:.3f})")
print(f"  - Credible interval: [β_lower, β_upper]")
print(f"  - Diễn giải: 'Xác suất β trong [a,b] là...'")
print("-" * 70)
```

## 2. Mathematical Formulation: Model Hoàn chỉnh

Bây giờ hãy viết model một cách formal.

### 2.1. Likelihood

Với mỗi quan sát $$i$$:

$$y_i \sim \mathcal{N}(\mu_i, \sigma)$$

Trong đó:

$$\mu_i = \alpha + \beta \cdot x_i$$

**Diễn giải**: Cân nặng của người $$i$$ được sinh từ phân phối Normal với mean phụ thuộc vào chiều cao của họ.

### 2.2. Priors

Chúng ta cần priors cho 3 parameters: $$\alpha$$, $$\beta$$, $$\sigma$$.

**Prior cho $$\alpha$$ (intercept)**:
$$\alpha \sim \mathcal{N}(\mu_\alpha, \sigma_\alpha)$$

**Prior cho $$\beta$$ (slope)**:
$$\beta \sim \mathcal{N}(\mu_\beta, \sigma_\beta)$$

**Prior cho $$\sigma$$ (noise)**:
$$\sigma \sim \text{HalfNormal}(\sigma_\sigma)$$

(Chúng ta sẽ học cách chọn priors cụ thể trong Bài 4.2)

### 2.3. Posterior

Theo Bayes' theorem:

$$P(\alpha, \beta, \sigma \mid \mathbf{y}, \mathbf{x}) \propto P(\mathbf{y} \mid \mathbf{x}, \alpha, \beta, \sigma) \cdot P(\alpha) \cdot P(\beta) \cdot P(\sigma)$$

**Điều quan trọng**: Posterior là **joint distribution** của cả 3 parameters. Chúng ta không chỉ có $$P(\beta \mid \text{data})$$, mà có $$P(\alpha, \beta, \sigma \mid \text{data})$$.

## 3. Interpretation: Ý nghĩa của Parameters

![Parameter Interpretation]({{ site.baseurl }}/img/chapter_img/chapter04/parameter_interpretation.png)

### 3.1. Intercept ($$\alpha$$)

**Định nghĩa**: Giá trị trung bình của $$y$$ khi $$x = 0$$.

**Trong ví dụ**: Cân nặng khi chiều cao = 0 cm.

**Vấn đề**: Thường không có ý nghĩa thực tế (ai có chiều cao 0 cm?).

**Giải pháp**: **Centering** - trừ mean của $$x$$:
$$\mu_i = \alpha + \beta \cdot (x_i - \bar{x})$$

Bây giờ $$\alpha$$ là cân nặng trung bình tại chiều cao trung bình - có ý nghĩa hơn!

### 3.2. Slope ($$\beta$$)

**Định nghĩa**: Thay đổi trung bình của $$y$$ khi $$x$$ tăng 1 đơn vị.

**Trong ví dụ**: Cân nặng tăng bao nhiêu kg khi chiều cao tăng 1 cm.

**Diễn giải Bayesian**: 
- Frequentist: "$$\beta = 0.7$$"
- Bayesian: "95% tin rằng $$\beta \in [0.6, 0.8]$$"

### 3.3. Noise ($$\sigma$$)

**Định nghĩa**: Standard deviation của residuals.

**Trong ví dụ**: Độ biến động cá nhân xung quanh đường hồi quy.

**Ý nghĩa**: 
- $$\sigma$$ nhỏ: Dữ liệu gần đường thẳng, model fit tốt
- $$\sigma$$ lớn: Dữ liệu phân tán, nhiều variability không giải thích được

```python
# Minh họa: Ý nghĩa của parameters
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. Intercept (α)
x_centered = height - height.mean()
axes[0].scatter(x_centered, weight, s=80, alpha=0.6, edgecolors='black')
axes[0].axvline(0, color='red', linestyle='--', linewidth=2, alpha=0.5)
axes[0].axhline(weight.mean(), color='red', linestyle='--', linewidth=2, alpha=0.5,
               label=f'α ≈ {weight.mean():.1f} kg (mean weight)')
axes[0].set_xlabel('Height - Mean Height (cm)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0].set_title('Intercept (α) after Centering\n' +
                 'α = mean weight at mean height',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# 2. Slope (β)
axes[1].scatter(height, weight, s=80, alpha=0.6, edgecolors='black')
# Draw slope interpretation
x1, x2 = 170, 171
y1 = true_alpha + true_beta * x1
y2 = true_alpha + true_beta * x2
axes[1].plot([x1, x2], [y1, y1], 'r-', linewidth=2)
axes[1].plot([x2, x2], [y1, y2], 'r-', linewidth=2)
axes[1].annotate('', xy=(x2, y1), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
axes[1].annotate('', xy=(x2, y2), xytext=(x2, y1),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
axes[1].text(x1 + 0.5, y1 - 2, '+1 cm', fontsize=11, color='red', fontweight='bold')
axes[1].text(x2 + 0.5, (y1 + y2)/2, f'+{true_beta:.2f} kg', fontsize=11, 
            color='red', fontweight='bold')
axes[1].plot(height_line, true_alpha + true_beta * height_line, 'b-', linewidth=2)
axes[1].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[1].set_title(f'Slope (β) = {true_beta:.2f} kg/cm\n' +
                 'Weight increase per 1 cm height',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)

# 3. Noise (σ)
axes[2].scatter(height, weight, s=80, alpha=0.6, edgecolors='black')
axes[2].plot(height_line, true_alpha + true_beta * height_line, 'r-', linewidth=3)
axes[2].fill_between(height_line,
                     true_alpha + true_beta * height_line - true_sigma,
                     true_alpha + true_beta * height_line + true_sigma,
                     alpha=0.3, color='red', label=f'μ ± σ ({true_sigma} kg)')
axes[2].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[2].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[2].set_title(f'Noise (σ) = {true_sigma:.1f} kg\n' +
                 'Individual variability',
                 fontsize=14, fontweight='bold')
axes[2].legend(fontsize=11)
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## Tóm tắt và Kết nối

Bayesian linear regression là một **generative model**:

- **Generative story**: Mô tả cách dữ liệu được sinh ra
- **Parameters**: $$\alpha$$ (intercept), $$\beta$$ (slope), $$\sigma$$ (noise)
- **Priors**: Encode uncertainty về parameters
- **Likelihood**: $$y_i \sim \mathcal{N}(\alpha + \beta x_i, \sigma)$$
- **Posterior**: Full uncertainty về parameters

**Khác với frequentist**:
- Không chỉ point estimates, mà **distributions**
- Không p-values, mà **credible intervals**
- Không "reject H0", mà **quantify uncertainty**

Trong bài tiếp theo, chúng ta sẽ học cách chọn priors cho regression models một cách có nguyên tắc.

## Bài tập

**Bài tập 1: Generative Story**
Viết generative story cho các mối quan hệ sau:
(a) Điểm thi phụ thuộc vào số giờ học
(b) Giá nhà phụ thuộc vào diện tích
(c) Doanh thu phụ thuộc vào chi phí quảng cáo

**Bài tập 2: Parameters Interpretation**
Cho model: Weight = 50 + 0.7·Height, σ = 5
(a) Diễn giải ý nghĩa của 50, 0.7, và 5
(b) Dự đoán cân nặng cho người cao 175cm
(c) 95% prediction interval là gì?

**Bài tập 3: Centering**
(a) Tại sao centering giúp intercept có ý nghĩa hơn?
(b) Centering có thay đổi slope không? Tại sao?
(c) Implement centering trong Python

**Bài tập 4: Frequentist vs Bayesian**
(a) Frequentist: "β = 0.7, p < 0.05"
(b) Bayesian: "95% credible interval: [0.6, 0.8]"
(c) Diễn giải khác nhau như thế nào?

**Bài tập 5: Simulation**
(a) Generate data với α=10, β=2, σ=3
(b) Fit frequentist regression (scipy.stats.linregress)
(c) So sánh estimates với true values
(d) Tăng σ lên 10 và quan sát thay đổi

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Hill, J., & Vehtari, A. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 7: Linear regression with a single predictor

**McElreath, R. (2020).** *Statistical Rethinking: A Bayesian Course with Examples in R and Stan* (2nd Edition). CRC Press.
- Chapter 4: Geocentric Models (Linear Regression)

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis* (2nd Edition). Academic Press.
- Chapter 17: Metric Predicted Variable on One Metric Predictor

---

*Bài học tiếp theo: [4.2 Priors for Regression - Chọn Prior có Nguyên tắc](/vi/chapter04/priors-for-regression/)*
