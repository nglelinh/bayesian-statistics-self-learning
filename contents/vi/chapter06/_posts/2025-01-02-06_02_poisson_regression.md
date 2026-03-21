---
layout: post
title: "Bài 6.2: Poisson Regression - Count Data"
chapter: '06'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter06
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu về **Poisson Regression** - model cho **count data** (số lần xảy ra events). Bạn sẽ học tại sao linear regression không phù hợp cho counts, cách sử dụng **log link function**, và cách interpret coefficients theo **rate ratios**. Đây là GLM thứ hai quan trọng sau logistic regression.

## Giới thiệu: Count Data Everywhere

**Count data** (dữ liệu đếm) xuất hiện khắp nơi:
- Số lượng khách hàng đến cửa hàng mỗi giờ
- Số lượng emails nhận được mỗi ngày
- Số lượng accidents trên đường cao tốc mỗi tháng
- Số lượng goals trong một trận bóng đá
- Số lượng mutations trong DNA sequence

**Đặc điểm**:
- $$y \in \{0, 1, 2, 3, ...\}$$ (non-negative integers)
- Không có upper bound
- Variance thường tăng với mean

**Câu hỏi**: Có thể dùng linear regression không?

## 1. Vấn đề của Linear Regression cho Count Data

![Poisson Regression Basics]({{ site.baseurl }}/img/chapter_img/chapter06/poisson_regression_basics.png)

**Vấn đề của linear regression cho count data:**
- **Linear regression** có thể dự đoán giá trị âm (invalid cho counts!)
- **Count data** yêu cầu predictions ≥ 0
- Hình minh họa:
  - Panel trái: Linear regression cho negative predictions (sai!)
  - Panel phải: Poisson regression với log link đảm bảo λ > 0 (đúng!)
- **Giải pháp**: Sử dụng **log link function**: $$\log(\lambda) = \alpha + \beta x$$

## 2. Poisson Regression: Generative Model

### 2.1. Log Link Function

**Idea**: Transform linear predictor để đảm bảo output > 0.

**Log link**:
$$
\log(\lambda) = \alpha + \beta x
$$

**Inverse** (exponential):
$$
\lambda = e^{\alpha + \beta x}
$$

### 2.2. Generative Story

1. **Linear predictor**: $$\eta = \alpha + \beta x$$
2. **Transform to rate**: $$\lambda = \exp(\eta)$$
3. **Generate counts**: $$y \sim \text{Poisson}(\lambda)$$

**Poisson distribution**:
$$
P(y = k \mid \lambda) = \frac{\lambda^k e^{-\lambda}}{k!}
$$

- Mean = $$\lambda$$
- Variance = $$\lambda$$ (equidispersion)

![Exponential Function Parameters](../../../img/chapter_img/chapter06/exponential_function_parameters.png)

**Exponential function và parameter effects:**
- **Panel trái**: Hàm exponential cơ bản $$\lambda = e^{\eta}$$
  - Khi $$\eta = 0$$ → $$\lambda = 1$$ (baseline rate)
  - Hàm luôn dương, tăng exponentially
- **Panel giữa**: Effect của $$\alpha$$ (intercept)
  - $$\alpha < 0$$: Baseline rate thấp ($$e^{-1} \approx 0.37$$)
  - $$\alpha = 0$$: Baseline rate = 1
  - $$\alpha > 0$$: Baseline rate cao ($$e^{1} \approx 2.72$$)
  - $$\alpha$$ controls độ cao của baseline
- **Panel phải**: Effect của $$\beta$$ (slope)
  - $$\beta$$ nhỏ → tăng chậm (weak effect)
  - $$\beta$$ lớn → tăng nhanh (strong effect)
  - $$\beta$$ controls tốc độ tăng trưởng exponential

## 3. Bayesian Poisson Regression trong PyMC

```python
import pymc as pm
import arviz as az

# Generate data
np.random.seed(42)
n = 150
x = np.random.uniform(0, 5, n)
lambda_true = np.exp(0.5 + 0.4*x)
y = np.random.poisson(lambda_true)

# Standardize predictor
x_z = (x - x.mean()) / x.std()

# Bayesian Poisson regression
with pm.Model() as poisson_model:
    # Priors
    alpha = pm.Normal('alpha', 2, 1)  # log(λ) ~ 2 → λ ~ 7
    beta = pm.Normal('beta', 0, 1)
    
    # Linear predictor
    eta = alpha + beta * x_z
    
    # Exponential transformation
    lambda_ = pm.Deterministic('lambda', pm.math.exp(eta))
    
    # Likelihood
    y_obs = pm.Poisson('y_obs', mu=lambda_, observed=y)
    
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
                 figsize=(14, 5))
plt.suptitle('Posterior Distributions',
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

## 4. Interpretation: Rate Ratios

### 4.1. Rate Ratio

**On log scale**:
$$
\log(\lambda) = \alpha + \beta x
$$

**Interpretation**: 1 unit increase in $$x$$ → $$\beta$$ increase in log(rate).

**On rate scale**:
$$
\lambda = e^{\alpha + \beta x}
$$

**Rate ratio**: 1 unit increase in $$x$$ → rate multiply by $$e^\beta$$.

```python
# Compute rate ratios
beta_samples = trace.posterior['beta'].values.flatten()
rate_ratio = np.exp(beta_samples)

print("\n" + "=" * 70)
print("RATE RATIO INTERPRETATION")
print("=" * 70)
print(f"\nβ (log scale): {beta_samples.mean():.3f}")
print(f"Rate Ratio (e^β): {rate_ratio.mean():.3f}")
print(f"95% CI: [{np.percentile(rate_ratio, 2.5):.3f}, " +
      f"{np.percentile(rate_ratio, 97.5):.3f}]")

print("\nInterpretation:")
print(f"  1 SD increase in x → rate multiply by {rate_ratio.mean():.2f}")
if rate_ratio.mean() > 1:
    print(f"  → {(rate_ratio.mean()-1)*100:.1f}% increase in rate")
else:
    print(f"  → {(1-rate_ratio.mean())*100:.1f}% decrease in rate")
print("=" * 70)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Beta (log scale)
axes[0].hist(beta_samples, bins=50, density=True, alpha=0.7,
            color='skyblue', edgecolor='black')
axes[0].axvline(beta_samples.mean(), color='red', linewidth=3,
               label=f'Mean = {beta_samples.mean():.3f}')
axes[0].axvline(0, color='black', linestyle='--', linewidth=2)
axes[0].set_xlabel('β (log scale)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('COEFFICIENT β\n(Log Scale)',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')

# Rate ratio
axes[1].hist(rate_ratio, bins=50, density=True, alpha=0.7,
            color='lightgreen', edgecolor='black')
axes[1].axvline(rate_ratio.mean(), color='red', linewidth=3,
               label=f'Mean = {rate_ratio.mean():.3f}')
axes[1].axvline(1, color='black', linestyle='--', linewidth=2)
axes[1].set_xlabel('Rate Ratio (e^β)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('RATE RATIO\n(Multiplicative Effect)',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

## 5. Posterior Predictive Checks

```python
# Posterior predictive
with poisson_model:
    ppc = pm.sample_posterior_predictive(trace, random_seed=42)

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Predicted rates
lambda_samples = trace.posterior['lambda'].values.reshape(-1, n)
lambda_mean = lambda_samples.mean(axis=0)
lambda_lower = np.percentile(lambda_samples, 2.5, axis=0)
lambda_upper = np.percentile(lambda_samples, 97.5, axis=0)

sort_idx = np.argsort(x)
axes[0, 0].scatter(x, y, alpha=0.4, s=40, label='Observed', edgecolors='black')
axes[0, 0].plot(x[sort_idx], lambda_mean[sort_idx], 'r-', linewidth=3,
               label='Posterior mean λ')
axes[0, 0].fill_between(x[sort_idx], lambda_lower[sort_idx], lambda_upper[sort_idx],
                        alpha=0.3, color='red', label='95% CI')
axes[0, 0].set_xlabel('x', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('y (counts)', fontsize=12, fontweight='bold')
axes[0, 0].set_title('PREDICTED RATES\nwith Uncertainty',
                    fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=11)
axes[0, 0].grid(alpha=0.3)

# Observed vs Predicted
y_pred = ppc.posterior_predictive['y_obs'].values.reshape(-1, n)
y_pred_mean = y_pred.mean(axis=0)

axes[0, 1].scatter(y, y_pred_mean, alpha=0.5, s=50, edgecolors='black')
axes[0, 1].plot([0, max(y)], [0, max(y)], 'r--', linewidth=2,
               label='Perfect prediction')
axes[0, 1].set_xlabel('Observed y', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Predicted E[y]', fontsize=12, fontweight='bold')
axes[0, 1].set_title('POSTERIOR PREDICTIVE CHECK\nObserved vs Predicted',
                    fontsize=14, fontweight='bold')
axes[0, 1].legend(fontsize=11)
axes[0, 1].grid(alpha=0.3)

# Distribution comparison
axes[1, 0].hist(y, bins=range(0, max(y)+2), alpha=0.6, density=True,
               label='Observed', edgecolor='black')
for i in range(min(100, y_pred.shape[0])):
    axes[1, 0].hist(y_pred[i], bins=range(0, max(y)+2), alpha=0.01,
                   density=True, color='red')
axes[1, 0].set_xlabel('y (counts)', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1, 0].set_title('DISTRIBUTION CHECK\nObserved vs PPC samples',
                    fontsize=14, fontweight='bold')
axes[1, 0].legend(fontsize=11)
axes[1, 0].grid(alpha=0.3, axis='y')

# Residuals
residuals = y - lambda_mean
axes[1, 1].scatter(lambda_mean, residuals, alpha=0.5, s=50, edgecolors='black')
axes[1, 1].axhline(0, color='red', linestyle='--', linewidth=2)
axes[1, 1].set_xlabel('Predicted λ', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Residuals (y - λ)', fontsize=12, fontweight='bold')
axes[1, 1].set_title('RESIDUAL PLOT\nCheck for patterns',
                    fontsize=14, fontweight='bold')
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## 6. Overdispersion: Khi Variance > Mean

**Poisson assumption**: Variance = Mean

**Reality**: Thường Variance > Mean (**overdispersion**)

**Solutions**:
1. **Negative Binomial** regression (allows overdispersion)
2. **Zero-Inflated Poisson** (nếu có nhiều zeros)

```python
# Check overdispersion
print("\n" + "=" * 70)
print("OVERDISPERSION CHECK")
print("=" * 70)
print(f"\nObserved data:")
print(f"  Mean: {y.mean():.2f}")
print(f"  Variance: {y.var():.2f}")
print(f"  Variance/Mean ratio: {y.var()/y.mean():.2f}")

if y.var() / y.mean() > 1.5:
    print("\n→ Overdispersion detected!")
    print("  Consider Negative Binomial or Zero-Inflated models")
else:
    print("\n→ Poisson assumption reasonable")
print("=" * 70)
```

## Tóm tắt

Poisson regression cho count data:

- **Problem**: Linear regression can predict negative counts
- **Solution**: Log link function
- **Model**: $$\log(\lambda) = \alpha + \beta x$$
- **Interpretation**: Rate ratios ($$e^\beta$$)
- **Assumption**: Variance = Mean (check for overdispersion!)

**Key insight**: Log link ensures predictions always positive, suitable for counts and rates.

Bài tiếp theo: **Model Evaluation for GLMs**.

## Bài tập

**Bài tập 1**: Generate count data. Fit Poisson regression. Interpret rate ratio.

**Bài tập 2**: Compare linear vs Poisson predictions. Visualize differences.

**Bài tập 3**: Multiple predictors Poisson regression. Interpret each coefficient.

**Bài tập 4**: Real data - predict number of customer visits từ time/weather features.

**Bài tập 5**: Check for overdispersion. If present, try Negative Binomial model.

## Tài liệu Tham khảo

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.
- Chapter 6: Generalized linear models

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 11: God Spiked the Integers

---

*Bài học tiếp theo: [6.3 Model Evaluation for GLMs](/vi/chapter06/model-evaluation-glm/)*
