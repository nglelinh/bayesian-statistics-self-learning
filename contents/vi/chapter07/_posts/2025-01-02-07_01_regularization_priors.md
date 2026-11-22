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

## Mục tiêu học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **điều chuẩn (regularization)** như một cơ chế cốt lõi để ngăn **quá khớp (overfitting)**. Bài học làm rõ vì sao phân phối tiên nghiệm (prior) trong thống kê Bayes tự nhiên thực hiện điều chuẩn, mối liên hệ giữa tiên nghiệm với hồi quy Ridge và Lasso trong thống kê tần suất (frequentist), và khi nào ta thực sự cần điều chuẩn thay vì tiếp tục tăng độ phức tạp của mô hình. Đây là kỹ năng thiết yếu khi xây dựng mô hình có nhiều **biến dự báo (predictors)**, đặc biệt khi số lượng biến vượt quá khả năng kiểm soát bằng trực giác.

## Giới thiệu: Vấn đề quá khớp (Overfitting)

Giả sử bạn chỉ có 20 điểm dữ liệu nhưng muốn khớp một mô hình hồi quy đa thức (polynomial regression). Câu hỏi tưởng như mang tính kỹ thuật — nên chọn bậc 1, bậc 10 hay bậc 15 — thực chất dẫn thẳng tới một vấn đề nền tảng của thống kê hiện đại. Nếu mô hình quá đơn giản, nó sẽ bị **thiếu khớp (underfit)** và bỏ sót cấu trúc quan trọng; ngược lại, nếu mô hình quá linh hoạt, nó sẽ bám chặt cả những dao động ngẫu nhiên của dữ liệu huấn luyện. Khi đó, mô hình học **nhiễu (noise)** thay vì **tín hiệu (signal)**: kết quả có vẻ rất tốt trên tập huấn luyện nhưng lại dự đoán kém trên dữ liệu mới. Đó là hiện tượng quá khớp (overfitting).

## 1. Minh họa hiện tượng quá khớp

![Overfitting Demonstration]({{ site.baseurl }}/img/chapter_img/chapter07/overfitting_demonstration.png)

Hình minh họa cho thấy rõ cơ chế của vấn đề. Với đa thức bậc 1, mô hình quá đơn giản nên cả sai số huấn luyện lẫn sai số kiểm tra đều cao — đây là trạng thái thiếu khớp điển hình. Với bậc 3, mô hình đủ linh hoạt để nắm bắt xu hướng chính mà chưa học thuộc nhiễu, nhờ đó cả hai loại sai số đều giảm. Khi tăng lên bậc 10, mô hình khớp rất sát dữ liệu huấn luyện nhưng sai số kiểm tra lại tăng, vì nó đã ghi nhớ các dao động ngẫu nhiên không lặp lại ở dữ liệu mới. Đến bậc 15, hiện tượng này trở nên cực đoan hơn khi mô hình gần như mất khả năng **khái quát hóa (generalize)**. Điểm cần ghi nhớ là sai số kiểm tra thường tăng trở lại khi mô hình quá phức tạp, và đó là lúc điều chuẩn trở nên cần thiết.

## 2. Điều chuẩn (Regularization): Hướng giải quyết

Ý tưởng cốt lõi của điều chuẩn là không để mô hình tự do sử dụng các hệ số quá lớn chỉ nhằm bám sát dữ liệu huấn luyện. Ta bổ sung một cơ chế ưu tiên các mô hình đơn giản hơn bằng cách phạt những cấu hình hệ số quá cực đoan.

### 2.1. Hồi quy Ridge (Điều chuẩn L2)

**Hàm mục tiêu**:
$$
\min_{\beta} \sum_{i=1}^n (y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^p \beta_j^2
$$

Trong biểu thức này, hạng tử đầu tiên yêu cầu mô hình khớp dữ liệu, còn hạng tử thứ hai phạt tổng bình phương các hệ số để giữ chúng ở quy mô vừa phải. Tham số $$\lambda$$ điều khiển mức độ phạt: $$\lambda$$ càng lớn thì điều chuẩn càng mạnh và các hệ số càng bị kéo gần về 0.

Từ góc nhìn Bayes, hồi quy Ridge tương ứng với việc đặt **tiên nghiệm chuẩn (Normal prior)** lên các hệ số:

$$
\beta_j \sim \text{Normal}(0, \sigma^2)
$$

### 2.2. Hồi quy Lasso (Điều chuẩn L1)

**Hàm mục tiêu**:
$$
\min_{\beta} \sum_{i=1}^n (y_i - \hat{y}_i)^2 + \lambda \sum_{j=1}^p |\beta_j|
$$

Trong ngôn ngữ Bayes, Lasso tương ứng với việc đặt **tiên nghiệm Laplace (Laplace prior)** lên các hệ số:

$$
\beta_j \sim \text{Laplace}(0, b)
$$

![Regularization Priors]({{ site.baseurl }}/img/chapter_img/chapter07/regularization_priors.png)

Hình so sánh các phân phối tiên nghiệm cho thấy điều chuẩn trong thống kê Bayes là một lựa chọn mô hình hóa trực tiếp chứ không phải thủ thuật bổ sung từ bên ngoài. **Tiên nghiệm chuẩn** ở hình bên trái có tâm tại 0 và đỉnh trơn, nên có xu hướng co các hệ số về gần 0 nhưng hiếm khi ép chúng bằng đúng 0; cách này phù hợp khi ta tin rằng nhiều biến dự báo đều có đóng góp nhỏ. **Tiên nghiệm Laplace** ở hình giữa nhọn hơn tại 0 và có đuôi dày hơn, nên khuyến khích **tính thưa (sparsity)** — nhiều hệ số bị đẩy mạnh về gần 0 hơn — do đó đặc biệt hữu ích cho bài toán **chọn biến (feature selection)**. Hình so sánh bên phải nhấn mạnh rằng chọn tiên nghiệm thực chất là chọn một cơ chế điều chuẩn: tiên nghiệm phẳng gần như không điều chuẩn, trong khi tiên nghiệm chuẩn và Laplace mã hóa những mức độ và kiểu co rút khác nhau.

### Thử nghiệm: Tiên nghiệm chuẩn co rút hệ số (Ridge)

Giảm $$\tau$$ từng bước để quan sát đường cong mượt dần, trong khi sai số kiểm tra giảm xuống rồi tăng trở lại.

<div class="interactive-demo" markdown="1">
<div data-demo="shrink-explainer" data-lang="vi"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 3. Điều chuẩn Bayes trong PyMC

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

## 4. Lựa chọn cường độ điều chuẩn

Một trong những câu hỏi thực tế nhất là nên điều chuẩn mạnh đến mức nào — hay theo ngôn ngữ Bayes, phân phối tiên nghiệm nên hẹp đến đâu để vừa kiểm soát quá khớp vừa không làm mất tín hiệu thật.

### 4.1. Kiểm định chéo (Cross-Validation)

Một cách tiếp cận thực dụng là dùng kiểm định chéo (cross-validation) để chọn độ rộng tiên nghiệm sao cho năng lực dự báo ngoài mẫu đạt tốt nhất.

### 4.2. Kiểm tra dự báo tiên nghiệm (Prior Predictive Checks)

Một cách tiếp cận mang tính Bayes hơn là dùng **kiểm tra dự báo tiên nghiệm (prior predictive checks)** để xem tiên nghiệm hiện tại có sinh ra những dự đoán hợp lý hay không, trước cả khi đưa dữ liệu vào khớp mô hình.

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

### 4.3. Danh sách kiểm tra chọn độ mạnh tiên nghiệm trong quy trình học máy

Trong thực tế học máy, độ mạnh của tiên nghiệm (hay cường độ điều chuẩn) nên được chọn theo một quy trình rõ ràng thay vì thử nghiệm ngẫu nhiên:

1. **Xác định mục tiêu dự báo và thước đo**: chọn metric phù hợp với bài toán (RMSE, MAE, log-loss, calibration...).
2. **Chia tập dữ liệu ngay từ đầu**: tách train/validation/test trước khi tinh chỉnh bất kỳ tham số nào.
3. **Chỉ khớp bước tiền xử lý trên tập huấn luyện**: chuẩn hóa, điền khuyết và mã hóa phải học từ tập train rồi mới áp dụng sang validation và test để tránh rò rỉ dữ liệu (data leakage).
4. **Tinh chỉnh độ rộng tiên nghiệm trên tập validation**: quét qua một lưới giá trị độ rộng tiên nghiệm hợp lý và so sánh hiệu năng ngoài mẫu.
5. **Thực hiện kiểm tra dự báo tiên nghiệm**: loại bỏ những tiên nghiệm sinh ra dự đoán phi lý trước khi đánh giá chi tiết kết quả khớp mô hình.
6. **Đánh giá trên tập test đúng một lần cuối**: chỉ dùng tập test ở bước cuối cùng để bảo toàn tính khách quan.

Quy trình trên kết nối trực tiếp tư duy Bayes với quy trình huấn luyện học máy: tiên nghiệm không chỉ là yếu tố lý thuyết, mà là một siêu tham số mang ý nghĩa mô hình hóa rõ ràng.

## 5. Nghiên cứu tình huống ứng dụng (Phần 1): Thiết lập, chia tập và kiểm soát rò rỉ dữ liệu

Ta xây dựng một bài toán hồi quy nhiều chiều giả lập: dự đoán giá trị liên tục từ 25 biến dự báo, trong đó chỉ một số ít biến thực sự mang tín hiệu. Mục tiêu của Phần 1 là thiết lập pipeline xử lý dữ liệu đúng cách.

```python
import numpy as np

rng = np.random.default_rng(42)
n, p = 180, 25

# Sparse ground truth: chi 6 bien co signal
beta_true = np.zeros(p)
beta_true[:6] = np.array([2.4, -1.8, 1.2, 0.9, -0.7, 0.5])

X = rng.normal(0, 1, size=(n, p))
y = 1.5 + X @ beta_true + rng.normal(0, 1.2, size=n)

# 60/20/20 split
idx = rng.permutation(n)
train_idx = idx[: int(0.6 * n)]
val_idx = idx[int(0.6 * n): int(0.8 * n)]
test_idx = idx[int(0.8 * n):]

X_train, y_train = X[train_idx], y[train_idx]
X_val, y_val = X[val_idx], y[val_idx]
X_test, y_test = X[test_idx], y[test_idx]

# Preprocessing fit tren train only (anti-leakage)
mu_x = X_train.mean(axis=0)
sd_x = X_train.std(axis=0)
sd_x[sd_x == 0] = 1.0

X_train_z = (X_train - mu_x) / sd_x
X_val_z = (X_val - mu_x) / sd_x
X_test_z = (X_test - mu_x) / sd_x

mu_y = y_train.mean()
sd_y = y_train.std() if y_train.std() > 0 else 1.0

y_train_z = (y_train - mu_y) / sd_y
y_val_z = (y_val - mu_y) / sd_y
y_test_z = (y_test - mu_y) / sd_y
```

**Điểm kiểm tra quyết định 1**:
- Chỉ bắt đầu tinh chỉnh tiên nghiệm hoặc cường độ điều chuẩn sau khi dữ liệu đã được chia tập và chuẩn hóa đúng theo quy trình chỉ dùng tập huấn luyện.
- Nếu tiền xử lý được khớp trên toàn bộ dữ liệu trước khi chia tập, kết quả trên tập validation sẽ lạc quan giả tạo do rò rỉ dữ liệu.

## 6. Khi nào cần điều chuẩn?

Điều chuẩn đặc biệt cần thiết khi số lượng biến dự báo lớn so với cỡ mẫu, khi các biến dự báo tương quan mạnh gây ra **đa cộng tuyến (multicollinearity)**, khi dữ liệu ít khiến mô hình dễ dao động mạnh theo từng mẫu, hoặc khi mục tiêu là tìm lời giải thưa chỉ giữ lại một số ít biến quan trọng. Ngược lại, nếu số biến dự báo ít, cỡ mẫu lớn, các biến gần như độc lập và có cơ sở lý thuyết vững để giữ toàn bộ biến trong mô hình, vai trò của điều chuẩn sẽ thứ yếu hơn. Điều chuẩn không phải lúc nào cũng cần thiết một cách máy móc; nó là biện pháp có chủ đích khi mô hình quá linh hoạt so với lượng thông tin mà dữ liệu cung cấp.

## Tóm tắt

Điều chuẩn giúp ngăn quá khớp bằng cách kiểm soát độ lớn của các hệ số thay vì để mô hình tự do bám theo mọi dao động của dữ liệu huấn luyện. Hồi quy Ridge tương ứng với việc đặt tiên nghiệm chuẩn để co các hệ số về gần 0, còn Lasso tương ứng với tiên nghiệm Laplace và khuyến khích lời giải thưa hơn. Từ góc nhìn Bayes, điều chuẩn không phải một thành phần gắn thêm bên ngoài, mà là hệ quả tự nhiên của việc chọn tiên nghiệm phù hợp với hiểu biết về quy mô và cấu trúc của các hệ số. Cường độ điều chuẩn có thể được điều chỉnh bằng kiểm định chéo hoặc kiểm tra dự báo tiên nghiệm tùy mục tiêu phân tích.

Điểm cốt lõi của bài là trong thống kê Bayes, thực hiện điều chuẩn về bản chất chính là lựa chọn phân phối tiên nghiệm một cách có cơ sở.

Bài tiếp theo: **Đánh đổi giữa độ lệch và phương sai (Bias-Variance Tradeoff)** — đi sâu vào chiến lược kiểm định và tinh chỉnh độ phức tạp mô hình trên cùng nghiên cứu tình huống.

## Video tham khảo

- [Regularization Part 1: Ridge (L2) Regression](https://www.youtube.com/watch?v=Q81RR3yKn30) — StatQuest with Josh Starmer, English. **Xem trước**. Giải thích cơ chế phạt L2 kéo hệ số về gần 0 để giảm phương sai, liên hệ trực tiếp với hiện tượng quá khớp ở đa thức bậc cao.
- [Ridge Regression is a Gaussian Prior](https://www.youtube.com/watch?v=W_SjooqeOqM) — DataMListic, English. Trình bày mối liên hệ giữa Ridge và tiên nghiệm chuẩn trên hệ số, củng cố góc nhìn tiên nghiệm Bayes chính là điều chuẩn.
- [Lasso Regression is a Laplace Prior](https://www.youtube.com/watch?v=8-_hZD0BRK8) — DataMListic, English. Giải thích sự tương ứng giữa Lasso và tiên nghiệm Laplace, bổ sung cho phần so sánh các cơ chế co rút hệ số.

## Bài tập

**Bài tập 1**: Sinh dữ liệu nhiều chiều ($$p > n$$), khớp mô hình với tiên nghiệm yếu và tiên nghiệm mạnh, sau đó so sánh kết quả.

**Bài tập 2**: Triển khai tiên nghiệm Lasso (Laplace) trong PyMC và so sánh với Ridge.

**Bài tập 3**: Sử dụng kiểm định chéo (cross-validation) để chọn độ rộng tiên nghiệm tối ưu.

**Bài tập 4**: Thực hiện kiểm tra dự báo tiên nghiệm với nhiều độ rộng tiên nghiệm khác nhau và xác định mức nào là hợp lý.

**Bài tập 5**: Áp dụng điều chuẩn trên một tập dữ liệu thực có nhiều biến dự báo và diễn giải kết quả thu được.

## Tài liệu tham khảo

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 12: Transformations and regression

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 4: Geocentric Models (Priors as regularization)

---

*Bài học tiếp theo: [7.2 Bias-Variance Tradeoff]({{ site.baseurl }}/contents/vi/chapter07/07_02_bias_variance_tradeoff/)*
