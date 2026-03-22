---
layout: post
title: "Bài 7.1: Regularization với Priors - Ngăn Overfitting"
chapter: '07'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter07
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **regularization** (điều chuẩn) như một cơ chế cốt lõi để ngăn **overfitting** (quá khớp). Bài học sẽ làm rõ vì sao priors trong Bayesian statistics thực hiện regularization một cách tự nhiên, chúng liên hệ thế nào với Ridge regression và Lasso regression trong ngôn ngữ frequentist, và trong những tình huống nào ta thật sự cần dùng regularization thay vì chỉ thêm độ phức tạp cho mô hình. Đây là kỹ năng thiết yếu khi làm modeling với nhiều **predictors** (biến dự báo), đặc biệt trong các bài toán mà số biến nhiều hơn trực giác của ta có thể kiểm soát bằng mắt.

## Giới thiệu: Vấn đề Overfitting

Hãy tưởng tượng bạn chỉ có 20 điểm dữ liệu nhưng lại muốn fit một polynomial regression. Câu hỏi tưởng như kỹ thuật, chẳng hạn nên chọn bậc 1, bậc 10, hay bậc 15, thực ra dẫn thẳng tới một vấn đề rất nền tảng của thống kê hiện đại. Nếu mô hình quá đơn giản, nó sẽ **underfit** và bỏ sót cấu trúc quan trọng; nhưng nếu mô hình quá linh hoạt, nó có thể bám chặt cả những dao động ngẫu nhiên của dữ liệu huấn luyện. Khi đó, mô hình học **noise** thay vì **signal**, và dù có vẻ rất giỏi trên training data, nó lại dự đoán kém trên dữ liệu mới. Đó chính là hiện tượng overfitting.

## 1. Demonstrating Overfitting

![Overfitting Demonstration](../../../img/chapter_img/chapter07/overfitting_demonstration.png)

Hình minh họa cho thấy rất rõ logic của vấn đề. Với polynomial bậc 1, mô hình quá đơn giản nên cả training error lẫn test error đều cao; đây là trạng thái underfit cổ điển. Với bậc 3, mô hình đủ linh hoạt để nắm bắt xu hướng chính của dữ liệu mà chưa bắt đầu học thuộc nhiễu, nên sai số huấn luyện và sai số kiểm tra đều thấp hơn. Khi tăng lên bậc 10, ta bắt đầu thấy một mô hình có vẻ rất đẹp trên training data nhưng lại có test error cao, bởi nó đã “ghi nhớ” những dao động ngẫu nhiên vốn không lặp lại ở dữ liệu mới. Đến bậc 15, hiện tượng này trở nên cực đoan hơn: mô hình gần như mất hẳn khả năng **generalize** (khái quát hóa). Điểm quan trọng cần giữ lại là test error thường tăng trở lại khi mô hình quá phức tạp, và đó chính là lúc regularization trở nên cần thiết.

## 2. Regularization: The Solution

Ý tưởng cốt lõi của regularization là không để mô hình tự do sử dụng những hệ số quá lớn chỉ để bám sát training data. Nói cách khác, ta thêm một cơ chế ưu tiên các mô hình đơn giản hơn bằng cách phạt những cấu hình hệ số quá cực đoan.

### 2.1. Ridge Regression (L2 Regularization)

**Objective**:
$$
\min_{\beta} \sum_{i=1}^n (y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^p \beta_j^2
$$

Trong biểu thức này, hạng đầu tiên buộc mô hình phải khớp dữ liệu, còn hạng thứ hai phạt tổng bình phương của các hệ số để giữ chúng ở quy mô vừa phải. Tham số $$\lambda$$ đóng vai trò điều khiển mức độ phạt; khi $$\lambda$$ càng lớn thì regularization càng mạnh và mô hình càng bị ép về phía những lời giải “hiền” hơn.

Từ góc nhìn Bayesian, Ridge regression có thể được hiểu như việc đặt **Normal prior** (tiên nghiệm chuẩn) lên các hệ số.

$$
\beta_j \sim \text{Normal}(0, \sigma^2)
$$

### 2.2. Lasso Regression (L1 Regularization)

**Objective**:
$$
\min_{\beta} \sum_{i=1}^n (y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^p |\beta_j|
$$

Trong ngôn ngữ Bayesian, Lasso tương ứng với việc đặt **Laplace prior** (tiên nghiệm Laplace) lên các hệ số.

$$
\beta_j \sim \text{Laplace}(0, b)
$$

![Regularization Priors](../../../img/chapter_img/chapter07/regularization_priors.png)

Hình so sánh các priors cho thấy regularization trong Bayes thực chất là một lựa chọn mô hình hóa rất cụ thể chứ không phải một thủ thuật thêm vào sau. **Normal prior** ở panel bên trái có tâm tại 0 và phần đuôi trơn, nên nó có xu hướng kéo các hệ số về gần 0 nhưng hiếm khi ép chúng bằng đúng 0; kiểu prior này phù hợp khi ta tin rằng nhiều predictor đều có ảnh hưởng nhỏ. **Laplace prior** ở panel giữa nhọn hơn tại 0 và có đuôi dày hơn, nên nó khuyến khích **sparsity** (tính thưa), tức nhiều hệ số sẽ bị đẩy mạnh về 0 hơn; vì vậy nó đặc biệt hữu ích cho **feature selection** (chọn biến). Panel so sánh ở bên phải nhấn mạnh rằng lựa chọn prior thực chất là lựa chọn một “triết lý điều chuẩn”: prior phẳng gần như không regularize, trong khi Normal và Laplace mã hóa những mức độ và kiểu co rút khác nhau.

## 3. Bayesian Regularization trong PyMC

```python
import pymc as pm
import arviz as az

# Generate data with many predictors
np.random.seed(42)
n = 100
p = 20  # 20 predictors

X = np.random.randn(n, p)
# Only first 3 predictors matter
beta_true = np.zeros(p)
beta_true[:3] = [2, -1.5, 1]
y = X @ beta_true + np.random.normal(0, 1, n)

# Standardize
X_z = (X - X.mean(axis=0)) / X.std(axis=0)
y_z = (y - y.mean()) / y.std()

# Model 1: Weak priors (no regularization)
with pm.Model() as model_weak:
    alpha = pm.Normal('alpha', 0, 10)  # Weak!
    beta = pm.Normal('beta', 0, 10, shape=p)  # Weak!
    sigma = pm.HalfNormal('sigma', 2)
    
    mu = alpha + pm.math.dot(X_z, beta)
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    trace_weak = pm.sample(1000, tune=500, chains=2, random_seed=42,
                          return_inferencedata=True, progressbar=False)

# Model 2: Strong priors (regularization)
with pm.Model() as model_reg:
    alpha = pm.Normal('alpha', 0, 1)
    beta = pm.Normal('beta', 0, 0.5, shape=p)  # Strong regularization!
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + pm.math.dot(X_z, beta)
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    trace_reg = pm.sample(1000, tune=500, chains=2, random_seed=42,
                         return_inferencedata=True, progressbar=False)

# Compare coefficients
beta_weak = trace_weak.posterior['beta'].values.reshape(-1, p).mean(axis=0)
beta_reg = trace_reg.posterior['beta'].values.reshape(-1, p).mean(axis=0)

# Visualize
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# True coefficients
axes[0].bar(range(p), beta_true, alpha=0.7, edgecolor='black')
axes[0].axhline(0, color='red', linestyle='--', linewidth=2)
axes[0].set_xlabel('Predictor Index', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
axes[0].set_title('TRUE COEFFICIENTS\nOnly first 3 non-zero',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3, axis='y')

# Weak priors
axes[1].bar(range(p), beta_weak, alpha=0.7, edgecolor='black', color='orange')
axes[1].axhline(0, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Predictor Index', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
axes[1].set_title('WEAK PRIORS (No Regularization)\n' +
                 'Many non-zero coefficients',
                 fontsize=14, fontweight='bold', color='red')
axes[1].grid(alpha=0.3, axis='y')

# Strong priors (regularization)
axes[2].bar(range(p), beta_reg, alpha=0.7, edgecolor='black', color='green')
axes[2].axhline(0, color='red', linestyle='--', linewidth=2)
axes[2].set_xlabel('Predictor Index', fontsize=12, fontweight='bold')
axes[2].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
axes[2].set_title('STRONG PRIORS (Regularization)\n' +
                 'Shrinkage toward 0',
                 fontsize=14, fontweight='bold', color='green')
axes[2].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("REGULARIZATION EFFECT")
print("=" * 70)
print(f"\nWeak priors:")
print(f"  Non-zero coefficients: {np.sum(np.abs(beta_weak) > 0.1)}/{p}")
print(f"  Max |β|: {np.abs(beta_weak).max():.3f}")

print(f"\nStrong priors (regularization):")
print(f"  Non-zero coefficients: {np.sum(np.abs(beta_reg) > 0.1)}/{p}")
print(f"  Max |β|: {np.abs(beta_reg).max():.3f}")

print(f"\n→ Regularization shrinks coefficients toward 0!")
print("=" * 70)
```

## 4. Choosing Regularization Strength

Một trong những câu hỏi thực tế nhất là nên regularize mạnh đến mức nào, hay trong ngôn ngữ Bayesian, prior nên hẹp đến đâu để vừa kiểm soát overfitting vừa không bóp nghẹt tín hiệu thật.

### 4.1. Cross-Validation

Một cách làm thực dụng là dùng cross-validation để chọn prior scale sao cho năng lực dự báo ngoài mẫu là tốt nhất.

### 4.2. Prior Predictive Checks

Một cách làm mang tinh thần Bayesian hơn là dùng **prior predictive checks** để xem liệu prior hiện tại có sinh ra những dự đoán hợp lý hay không, trước cả khi nhìn dữ liệu.

```python
# Prior predictive check
with pm.Model() as model_check:
    alpha = pm.Normal('alpha', 0, 1)
    beta = pm.Normal('beta', 0, 0.5, shape=p)
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + pm.math.dot(X_z, beta)
    y_prior = pm.Normal('y_prior', mu=mu, sigma=sigma, shape=n)
    
    # Sample from prior
    prior_samples = pm.sample_prior_predictive(samples=500, random_seed=42)

# Visualize
y_prior_samples = prior_samples.prior['y_prior'].values.reshape(-1, n)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Prior predictions
for i in range(min(100, y_prior_samples.shape[0])):
    axes[0].hist(y_prior_samples[i], bins=30, alpha=0.02, color='blue', density=True)
axes[0].hist(y_z, bins=30, alpha=0.7, color='red', edgecolor='black',
            density=True, label='Observed data')
axes[0].set_xlabel('y (standardized)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('PRIOR PREDICTIVE CHECK\n' +
                 'Do priors generate reasonable data?',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')

# Prior means and SDs
prior_means = y_prior_samples.mean(axis=1)
prior_sds = y_prior_samples.std(axis=1)

axes[1].scatter(prior_means, prior_sds, alpha=0.5, s=30, edgecolors='black')
axes[1].axvline(y_z.mean(), color='red', linewidth=2, label='Observed mean')
axes[1].axhline(y_z.std(), color='red', linewidth=2, linestyle='--',
               label='Observed SD')
axes[1].set_xlabel('Prior Predicted Mean', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Prior Predicted SD', fontsize=12, fontweight='bold')
axes[1].set_title('PRIOR PREDICTIONS\nMean vs SD',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## 5. Khi nào Cần Regularization?

Regularization đặc biệt cần thiết khi số lượng predictor lớn so với cỡ mẫu, khi các predictor tương quan mạnh với nhau gây ra **multicollinearity** (đa cộng tuyến), khi dữ liệu ít nên mô hình dễ dao động mạnh theo từng mẫu, hoặc khi mục tiêu của ta là tìm một lời giải thưa với chỉ một số ít biến quan trọng được giữ lại. Ngược lại, nếu số predictor ít, cỡ mẫu lớn, các biến gần như độc lập với nhau, và ta có cơ sở lý thuyết mạnh để giữ toàn bộ biến trong mô hình, thì regularization có thể đóng vai trò thứ yếu hơn. Điểm mấu chốt là regularization không phải lúc nào cũng là “thuốc bổ”; nó là phản ứng có chủ đích trước nguy cơ mô hình quá linh hoạt so với lượng thông tin mà dữ liệu thực sự cung cấp.

## Tóm tắt

Regularization ngăn overfitting bằng cách kiểm soát quy mô của các hệ số thay vì để mô hình tự do đuổi theo mọi dao động của dữ liệu huấn luyện. Ridge regression có thể được hiểu như việc đặt Normal prior để co tất cả hệ số về gần 0, còn Lasso tương ứng với Laplace prior và khuyến khích lời giải thưa hơn. Từ góc nhìn Bayesian, regularization không phải một phần phụ trợ nằm ngoài mô hình, mà chính là hệ quả của việc chọn priors phù hợp với mức độ tin tưởng của ta về độ lớn và cấu trúc của các hệ số. Cường độ regularization có thể được điều chỉnh bằng cross-validation hoặc bằng prior predictive checks, tùy mục tiêu của phân tích.

Điểm quan trọng nhất của bài là nhận ra rằng trong Bayesian statistics, nói “regularize” về bản chất chính là nói “chọn prior một cách có trách nhiệm”.

Bài tiếp theo: **Bias-Variance Tradeoff**.

## Bài tập

**Bài tập 1**: Generate high-dimensional data (p > n). Fit với weak và strong priors. Compare.

**Bài tập 2**: Implement Lasso prior (Laplace) trong PyMC. Compare với Ridge.

**Bài tập 3**: Use cross-validation to choose optimal prior scale.

**Bài tập 4**: Prior predictive checks với different prior scales. Which is reasonable?

**Bài tập 5**: Real data với many predictors. Apply regularization và interpret results.

## Tài liệu Tham khảo

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 12: Transformations and regression

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 4: Geocentric Models (Priors as regularization)

---

*Bài học tiếp theo: [7.2 Bias-Variance Tradeoff](/vi/chapter07/bias-variance-tradeoff/)*
