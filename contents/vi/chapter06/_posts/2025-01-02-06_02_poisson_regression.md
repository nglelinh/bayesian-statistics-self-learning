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

Sau khi hoàn thành bài học này, bạn sẽ hiểu **Poisson Regression** (hồi quy Poisson) như mô hình chuẩn cho **count data** (dữ liệu đếm), tức những dữ liệu ghi nhận số lần một sự kiện xảy ra. Bạn sẽ thấy vì sao linear regression không phù hợp khi biến kết quả chỉ nhận các số nguyên không âm, vì sao **log link function** (hàm liên kết log) giúp mô hình tạo ra dự đoán hợp lệ, và vì sao hệ số của mô hình nên được diễn giải thông qua **rate ratio** (tỷ số tốc độ) thay vì theo hiệu số cộng đơn giản. Đây là GLM quan trọng thứ hai sau logistic regression.

## Giới thiệu: Count Data Everywhere

**Count data** (dữ liệu đếm) xuất hiện ở rất nhiều bối cảnh thực tế, chẳng hạn như số khách đến cửa hàng mỗi giờ, số email nhận được mỗi ngày, số tai nạn trên cao tốc mỗi tháng, số bàn thắng trong một trận bóng đá, hay số đột biến trong một đoạn DNA. Điểm chung của các biến này là $$y \in \{0,1,2,3,\ldots\}$$, tức chúng là các số nguyên không âm, thường không có chặn trên rõ ràng, và phương sai thường tăng lên khi giá trị trung bình tăng lên. Điều đó dẫn đến câu hỏi quen thuộc: liệu ta có thể dùng linear regression cho loại dữ liệu này hay không.

## 1. Vấn đề của Linear Regression cho Count Data

![Poisson Regression Basics]({{ site.baseurl }}/img/chapter_img/chapter06/poisson_regression_basics.png)

Khó khăn cơ bản của linear regression trong bối cảnh này là mô hình tuyến tính có thể cho ra dự đoán âm, trong khi số lần xảy ra của một sự kiện không thể nhỏ hơn 0. Hình minh họa cho thấy ở panel bên trái, đường hồi quy tuyến tính có thể đi vào vùng giá trị âm, còn ở panel bên phải, Poisson regression dùng **log link** để bảo đảm rằng tham số cường độ $$\lambda$$ luôn dương. Nói cách khác, thay vì dự đoán trực tiếp số đếm, ta mô hình hóa log của tốc độ kỳ vọng, nhờ đó đầu ra luôn phù hợp với bản chất của dữ liệu.

## 2. Poisson Regression: Generative Model

### 2.1. Log Link Function

Ý tưởng cốt lõi của Poisson regression là giữ lại phần tuyến tính ở bên trong, nhưng dùng **log link function** để bảo đảm rằng đại lượng cuối cùng, tức tốc độ kỳ vọng $$\lambda$$, luôn lớn hơn 0.

**Log link**:
$$
\log(\lambda) = \alpha + \beta x
$$

**Inverse** (exponential):
$$
\lambda = e^{\alpha + \beta x}
$$

### 2.2. Generative Story

Theo ngôn ngữ **generative story** (câu chuyện sinh dữ liệu), mô hình được đọc như sau. Từ biến dự báo $$x$$, ta tạo ra một đại lượng tuyến tính $$\eta=\alpha+\beta x$$. Đại lượng này sau đó được đưa qua hàm mũ để tạo ra tốc độ kỳ vọng $$\lambda=\exp(\eta)$$. Cuối cùng, số đếm quan sát được sinh ra từ phân phối Poisson, tức $$y\sim\text{Poisson}(\lambda)$$. Việc tách ba bước này ra rõ ràng giúp ta thấy mô hình vừa giữ được phần tuyến tính thuận tiện cho suy luận, vừa tôn trọng cấu trúc xác suất riêng của dữ liệu đếm.

Phân phối Poisson có dạng:
$$
P(y = k \mid \lambda) = \frac{\lambda^k e^{-\lambda}}{k!}
$$

Điểm đặc trưng của phân phối này là giá trị trung bình và phương sai đều bằng $$\lambda$$; tính chất đó thường được gọi là **equidispersion** (đồng phương sai theo nghĩa mean bằng variance).

![Exponential Function Parameters](../../../img/chapter_img/chapter06/exponential_function_parameters.png)

Hình minh họa giúp ta đọc hàm mũ theo cách trực quan hơn. Ở panel bên trái, hàm cơ bản $$\lambda=e^\eta$$ luôn dương và đi qua điểm $$\lambda=1$$ khi $$\eta=0$$, nên có thể xem đó là mức tốc độ nền. Ở panel giữa, thay đổi $$\alpha$$, tức **intercept** (hệ số chặn), chủ yếu làm dịch chuyển toàn bộ đường cong lên hoặc xuống, qua đó thay đổi mức nền của tốc độ. Ở panel bên phải, thay đổi $$\beta$$, tức **slope** (độ dốc), làm tốc độ tăng nhanh hơn hoặc chậm hơn theo $$x$$, vì vậy nó phản ánh sức mạnh của mối quan hệ giữa biến dự báo và cường độ xảy ra sự kiện.

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

Trên thang log, mỗi khi $$x$$ tăng thêm 1 đơn vị thì log của tốc độ kỳ vọng tăng thêm $$\beta$$ đơn vị.

**On rate scale**:
$$
\lambda = e^{\alpha + \beta x}
$$

Khi quay trở về thang gốc, điều đó có nghĩa là tốc độ kỳ vọng được nhân với $$e^\beta$$. Đại lượng $$e^\beta$$ này chính là **rate ratio** (tỷ số tốc độ), và đây là cách diễn giải tự nhiên nhất cho hệ số của Poisson regression.

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

Một giả định trung tâm của Poisson regression là phương sai bằng trung bình. Trong dữ liệu thực, giả định này thường bị phá vỡ vì phương sai lớn hơn trung bình, hiện tượng được gọi là **overdispersion** (quá phân tán). Khi điều đó xảy ra, mô hình Poisson thường tỏ ra quá tự tin và đánh giá thấp độ bất định. Hai hướng xử lý phổ biến là dùng **Negative Binomial regression** khi cần cho phép phương sai lớn hơn mean một cách linh hoạt, hoặc dùng **Zero-Inflated Poisson** nếu dữ liệu có quá nhiều số 0 hơn điều mà Poisson thông thường có thể giải thích.

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

Poisson regression là mô hình tự nhiên cho dữ liệu đếm vì nó giải quyết đúng điểm yếu của linear regression: dự đoán của mô hình tuyến tính có thể âm, còn dữ liệu đếm thì không. Bằng cách dùng **log link**, mô hình hóa $$\log(\lambda)=\alpha+\beta x$$ rồi suy ra $$\lambda$$ trên thang gốc, Poisson regression bảo đảm rằng tốc độ kỳ vọng luôn dương. Hệ số của mô hình được hiểu tốt nhất thông qua **rate ratio** $$e^\beta$$, còn giả định quan trọng nhất luôn cần kiểm tra là phương sai có xấp xỉ trung bình hay không. Nếu dữ liệu quá phân tán, ta phải nghĩ đến những mô hình linh hoạt hơn.

Điểm cốt lõi cần nhớ là hàm liên kết log không chỉ là một thủ thuật toán học, mà là cơ chế giúp phần tuyến tính của mô hình tương thích với bản chất của dữ liệu đếm và dữ liệu tốc độ.

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
