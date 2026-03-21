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

**Vấn đề của linear regression cho binary data:**
- **Linear regression** dự đoán giá trị bất kỳ (-∞ đến +∞)
- **Binary outcomes** yêu cầu probability trong [0, 1]
- Hình minh họa:
  - Panel trái: Linear regression cho predictions ngoài [0,1] (invalid!)
  - Panel phải: Logistic regression đảm bảo predictions luôn trong [0,1]
- **Giải pháp**: Sử dụng **logistic function** để transform linear predictor thành probability

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

### 2.3. Quy tắc phân lớp Bayes từ prior-likelihood-posterior

Cho lớp $$c_i$$ và đặc trưng $$x$$, xác suất hậu nghiệm lớp có dạng:

$$
P(c_i\mid x)=\frac{P(x\mid c_i)P(c_i)}{\sum_j P(x\mid c_j)P(c_j)}
\propto P(x\mid c_i)P(c_i).
$$

Với mất mát 0-1, quy tắc phân lớp tối ưu là chọn lớp có posterior lớn nhất:

$$
\hat c(x)=\arg\max_i\;P(c_i\mid x).
$$

Điểm này là cầu nối trực tiếp từ Bayes theorem (Chapter 1-2) sang bài toán phân lớp ở Buổi 8.

### 2.4. Ví dụ Session 8: prior-shift trong phân lớp trái cây

Giả sử có 2 lớp: Táo ($$c_1$$) và Cam ($$c_2$$). Cùng một đặc trưng $$x$$ cho likelihood ratio:

$$
\frac{P(x\mid c_1)}{P(x\mid c_2)}=2.
$$

**Bối cảnh A** (siêu thị miền ôn đới): $$P(c_1)=0.8,\;P(c_2)=0.2$$.

Khi đó posterior odds:

$$
\frac{P(c_1\mid x)}{P(c_2\mid x)}=2\times\frac{0.8}{0.2}=8.
$$

**Bối cảnh B** (chợ miền nhiệt đới): $$P(c_1)=0.2,\;P(c_2)=0.8$$.

Khi đó:

$$
\frac{P(c_1\mid x)}{P(c_2\mid x)}=2\times\frac{0.2}{0.8}=0.5.
$$

Kết luận: cùng một bằng chứng cảm biến $$x$$ nhưng thay prior lớp có thể đảo quyết định phân lớp.

### 2.5. Từ posterior sang decision rule tối thiểu rủi ro

Khi chi phí sai khác nhau, không nên dùng ngưỡng 0.5 cố định. Với tập hành động $$a$$, chọn:

$$
a^*(x)=\arg\min_a\sum_i L(a,c_i)P(c_i\mid x).
$$

#### Ví dụ hai lớp, ba hành động (có reject)

Hai trạng thái thật: $$c_1, c_2$$. Ba hành động: chọn $$c_1$$, chọn $$c_2$$, hoặc **reject** (trì hoãn để đo thêm).

Loss matrix minh họa:

- đúng lớp: 0,
- nhầm lớp: 10,
- reject: 3 (chi phí đo thêm/đợi).

Giả sử posterior tại một điểm $$x$$ là $$P(c_1\mid x)=0.55,\;P(c_2\mid x)=0.45$$.

Khi đó:

$$
R(a=c_1\mid x)=10\cdot 0.45=4.5,
$$

$$
R(a=c_2\mid x)=10\cdot 0.55=5.5,
$$

$$
R(a=\text{reject}\mid x)=3.
$$

Nên hành động tối ưu là reject vì rủi ro kỳ vọng thấp nhất. Đây là ví dụ chuẩn "two-class/three-action" của Buổi 8.

### 2.6. Dạng discriminant và log-discriminant

Trong thực hành, ta thường so sánh trực tiếp discriminant:

$$
g_i(x)=\log P(x\mid c_i)+\log P(c_i),
$$

và chọn lớp có $$g_i(x)$$ lớn nhất.

Vì log là phép biến đổi đơn điệu, việc tối đa hóa posterior tương đương tối đa hóa log-discriminant, đồng thời ổn định số học tốt hơn khi xác suất rất nhỏ.

### 2.7. Trường hợp Gaussian: biên tuyến tính hay bậc hai

Nếu $$P(x\mid c_i)$$ là Gaussian đa biến:

- **Covariance chung** giữa các lớp ($$\Sigma_i=\Sigma$$): biên quyết định là tuyến tính (LDA-like).
- **Covariance khác nhau** theo lớp ($$\Sigma_i$$ khác nhau): biên quyết định là bậc hai (QDA-like).

Đây là cách đọc trực quan giúp nối posterior rule với hình học biên phân lớp.

![Logistic Function Parameters](../../../img/chapter_img/chapter06/logistic_function_parameters.png)

**Logistic function và parameter effects:**
- **Panel trái**: Hàm logistic cơ bản $$p = \frac{1}{1 + e^{-\eta}}$$
  - Khi $$\eta = 0$$ → $$p = 0.5$$ (điểm uốn)
  - Hàm có dạng chữ S, tiệm cận đến 0 và 1
- **Panel giữa**: Effect của $$\alpha$$ (intercept)
  - $$\alpha < 0$$: Curve dịch sang phải (baseline probability thấp)
  - $$\alpha > 0$$: Curve dịch sang trái (baseline probability cao)
  - $$\alpha$$ controls vị trí của điểm uốn
- **Panel phải**: Effect của $$\beta$$ (slope)
  - $$\beta$$ nhỏ → curve thoải (weak effect)
  - $$\beta$$ lớn → curve dốc (strong effect)
  - $$\beta$$ controls độ mạnh của relationship

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

![Odds vs Probability](../../../img/chapter_img/chapter06/odds_probability_relationship.png)

**Relationship giữa probability, odds, và log-odds:**
- **Panel trái**: Probability → Odds transformation
  - p = 0.2 → odds = 0.25 (4:1 against)
  - p = 0.5 → odds = 1.0 (even odds, breakpoint)
  - p = 0.8 → odds = 4.0 (4:1 favor)
  - Odds nhỏ hơn 1 = less likely, lớn hơn 1 = more likely
- **Panel phải**: Probability → Log-Odds (logit)
  - p = 0.5 → log-odds = 0 (symmetric point)
  - p < 0.5 → log-odds < 0 (negative)
  - p > 0.5 → log-odds > 0 (positive)
  - Log-odds scale là linear trong logistic regression: $$\text{logit}(p) = \alpha + \beta x$$

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
