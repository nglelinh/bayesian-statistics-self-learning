---
layout: post
title: "Bài 7.2: Bias-Variance Tradeoff - Cốt lõi của Model Selection"
chapter: '07'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter07
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu sâu về **bias-variance tradeoff** - một trong những concepts quan trọng nhất trong machine learning và statistics. Bạn sẽ học tại sao simple models có high bias, complex models có high variance, và làm sao tìm sweet spot ở giữa. Đây là foundation để hiểu regularization và model selection.

## Giới thiệu: Hai Loại Error

Khi model dự đoán sai, có hai nguyên nhân:

1. **Bias**: Model quá simple → không capture được pattern
2. **Variance**: Model quá complex → học noise thay vì signal

**Tradeoff**: Giảm bias → tăng variance (và ngược lại).

## 1. Bias và Variance: Định nghĩa

### 1.1. Mathematical Definitions

Giả sử chúng ta train model nhiều lần trên different datasets từ cùng một distribution.

**Bias**: Sai lệch giữa **average prediction** và **true value**
$$
\text{Bias}[\hat{f}(x)] = \mathbb{E}[\hat{f}(x)] - f(x)
$$

**Variance**: Variability của predictions across datasets
$$
\text{Variance}[\hat{f}(x)] = \mathbb{E}[(\hat{f}(x) - \mathbb{E}[\hat{f}(x)])^2]
$$

**Total Error**:
$$
\mathbb{E}[(y - \hat{f}(x))^2] = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}
$$

### 1.2. Intuitive Understanding

![Bias-Variance Demonstration](../../../img/chapter_img/chapter07/bias_variance_demonstration.png)

**Kết quả quan sát:**

- **HIGH BIAS (Underfitting)** - Degree 1:
  - Model đơn giản (đường thẳng)
  - Predictions sát nhau (low variance)
  - Nhưng xa sự thật (high bias)
  - Avg |Bias| ≈ 1.5-2.0, Avg Variance ≈ 0.2-0.3

- **BALANCED** - Degree 3:
  - Độ phức tạp vừa phải
  - Variance hợp lý
  - Bias thấp
  - Avg |Bias| ≈ 0.3-0.5, Avg Variance ≈ 0.5-0.7
  - **Sweet spot** cho trade-off

- **HIGH VARIANCE (Overfitting)** - Degree 10:
  - Model phức tạp (polynomial bậc cao)
  - Predictions spread out (high variance)
  - Mean prediction gần sự thật (low bias)
  - Nhưng individual predictions không đáng tin cậy!
  - Avg |Bias| ≈ 0.2-0.4, Avg Variance ≈ 2.0-3.0

**Key insight**: 50 training sets khác nhau → 50 models khác nhau. Variance đo độ "dao động" của predictions giữa các models.

## 2. Decomposition: MSE = Bias² + Variance + Noise

![MSE Decomposition](../../../img/chapter_img/chapter07/mse_decomposition.png)

**Kết quả phân tích:**

**Optimal Complexity:**
- **Optimal degree**: 2
- **Bias²**: 0.046
- **Variance**: 0.227
- **MSE**: 0.274

**Quan sát từ đường cong:**

- **Low complexity (degree 1-2)**:
  - Bias² cao (đường đỏ)
  - Variance thấp (đường xanh)
  - Model quá đơn giản → underfitting

- **Optimal complexity (degree 2-3)**:
  - Bias² và Variance cân bằng
  - MSE thấp nhất (đường xanh lá)
  - **Sweet spot** - trade-off tối ưu!

- **High complexity (degree 10+)**:
  - Bias² thấp (model fit data tốt)
  - Variance cao (không ổn định)
  - MSE tăng → overfitting

**Stacked view** (plot bên phải) cho thấy rõ: MSE = Bias² + Variance. Mục tiêu là tìm độ phức tạp minimize tổng error, không phải minimize riêng bias hay variance.

## 3. Regularization và Bias-Variance

**Regularization** controls bias-variance tradeoff:
- **Weak regularization** (λ small): Low bias, high variance
- **Strong regularization** (λ large): High bias, low variance

![Regularization Bias-Variance](../../../img/chapter_img/chapter07/regularization_bias_variance.png)

**Kết quả quan sát với polynomial degree 10:**

- **λ = 0.001** (Very Weak):
  - Bias² ≈ 0.05-0.10, Variance ≈ 8-12
  - HIGH variance → Overfitting
  - Predictions spread out wildly
  
- **λ = 0.1** (Weak):
  - Bias² ≈ 0.10-0.15, Variance ≈ 2-4
  - Still high variance but better
  
- **λ = 1** (Balanced):
  - Bias² ≈ 0.20-0.30, Variance ≈ 0.8-1.5
  - Good balance
  
- **λ = 10** (Strong):
  - Bias² ≈ 0.40-0.60, Variance ≈ 0.3-0.5
  - Higher bias, lower variance
  
- **λ = 100** (Very Strong):
  - Bias² ≈ 1.5-2.5, Variance ≈ 0.1-0.2
  - HIGH bias → Underfitting
  - Model too constrained, predictions almost flat

**Key insight**: Regularization parameter λ controls the trade-off. Optimal λ balances bias and variance for minimum MSE.

## 4. Bayesian Perspective

Trong Bayesian statistics:
- **Prior strength** controls bias-variance
- **Weak priors**: High variance (flexible, data-driven)
- **Strong priors**: High bias (rigid, prior-driven)

```python
import pymc as pm
import arviz as az

# Generate data
np.random.seed(42)
n = 30
x_data = np.random.uniform(0, 10, n)
y_data = true_function(x_data) + np.random.normal(0, 1, n)

x_data_z = (x_data - x_data.mean()) / x_data.std()
y_data_z = (y_data - y_data.mean()) / y_data.std()

# Different prior strengths
prior_sds = [0.1, 0.5, 2, 10]

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.ravel()

for idx, prior_sd in enumerate(prior_sds):
    with pm.Model() as model:
        alpha = pm.Normal('alpha', 0, 1)
        beta = pm.Normal('beta', 0, prior_sd)  # Varying prior strength
        sigma = pm.HalfNormal('sigma', 1)
        
        mu = alpha + beta * x_data_z
        y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_data_z)
        
        trace = pm.sample(500, tune=200, chains=2, random_seed=42,
                         return_inferencedata=True, progressbar=False)
    
    # Posterior predictions
    alpha_samples = trace.posterior['alpha'].values.flatten()
    beta_samples = trace.posterior['beta'].values.flatten()
    
    # Plot
    x_plot_z = (x_test - x_data.mean()) / x_data.std()
    for i in range(min(100, len(alpha_samples))):
        y_plot_z = alpha_samples[i] + beta_samples[i] * x_plot_z
        y_plot = y_plot_z * y_data.std() + y_data.mean()
        axes[idx].plot(x_test, y_plot, '-', alpha=0.05, color='orange')
    
    axes[idx].scatter(x_data, y_data, s=60, alpha=0.7, edgecolors='black',
                     label='Data', zorder=5)
    axes[idx].plot(x_test, y_true, 'b-', linewidth=3, label='True', zorder=4)
    axes[idx].set_xlabel('x', fontsize=11, fontweight='bold')
    axes[idx].set_ylabel('y', fontsize=11, fontweight='bold')
    
    if prior_sd < 1:
        title_color = 'red'
        subtitle = '(High Bias)'
    elif prior_sd > 5:
        title_color = 'orange'
        subtitle = '(High Variance)'
    else:
        title_color = 'green'
        subtitle = '(Balanced)'
    
    axes[idx].set_title(f'Prior SD = {prior_sd} {subtitle}',
                       fontsize=13, fontweight='bold', color=title_color)
    axes[idx].legend(fontsize=10)
    axes[idx].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## Tóm tắt

Bias-Variance Tradeoff:

- **Bias**: Error from overly simple model
- **Variance**: Error from sensitivity to training data
- **MSE = Bias² + Variance + Irreducible Error**
- **Regularization**: Controls tradeoff
- **Goal**: Find sweet spot that minimizes total error

**Key insight**: Perfect fit on training data ≠ good model. Balance is key!

Bài tiếp theo: **Feature Selection**.

## Bài tập

**Bài tập 1**: Implement bias-variance decomposition from scratch. Verify MSE = Bias² + Variance.

**Bài tập 2**: Generate data. Compute bias-variance for models with different complexities. Find optimal.

**Bài tập 3**: Use Ridge với different λ. Plot bias-variance curve. Find optimal λ.

**Bài tập 4**: Bayesian models với different prior SDs. Compute posterior variance. Relate to bias-variance.

**Bài tập 5**: Real data. Split train/test. Show overfitting với high-degree polynomial. Fix với regularization.

## Tài liệu Tham khảo

**Hastie, T., Tibshirani, R., & Friedman, J. (2009).** *The Elements of Statistical Learning* (2nd Edition). Springer.
- Chapter 7: Model Assessment and Selection

**James, G., et al. (2013).** *An Introduction to Statistical Learning*. Springer.
- Chapter 2: Statistical Learning

---

*Bài học tiếp theo: [7.3 Feature Selection](/vi/chapter07/feature-selection/)*
