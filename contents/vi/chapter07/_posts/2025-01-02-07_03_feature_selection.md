---
layout: post
title: "Bài 7.3: Feature Selection - Chọn Predictors Quan trọng"
chapter: '07'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter07
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **feature selection** (chọn biến) như bài toán xác định predictor nào thật sự quan trọng khi ta có rất nhiều ứng viên. Bài học sẽ đi qua các Bayesian approaches như Laplace priors, spike-and-slab, và horseshoe priors, đồng thời so sánh chúng với những frequentist methods quen thuộc như Lasso hay stepwise procedures. Mục tiêu không chỉ là biết công cụ nào tồn tại, mà là hiểu mỗi công cụ đang mã hóa giả định gì về độ thưa của mô hình, và khi nào mỗi cách tiếp cận là hợp lý hơn trong bối cảnh dữ liệu có số chiều cao.

## Giới thiệu: Vấn đề của Many Predictors

Hãy xét tình huống bạn có 100 **potential predictors** nhưng chỉ khoảng 5 biến trong số đó thật sự có tín hiệu. Nếu giữ tất cả các biến, mô hình dễ overfit; nếu thử mọi tổ hợp có thể, chi phí tính toán sẽ bùng nổ vì số mô hình cần xét lên đến $$2^{100}$$; còn nếu kiểm định từng biến riêng lẻ, ta lại đối mặt với nguy cơ **false discoveries** do multiple testing. Vì vậy, mục tiêu của feature selection không đơn thuần là “làm mô hình gọn hơn”, mà là nhận diện một cách có nguyên tắc những biến thật sự liên quan trong khi vẫn kiểm soát được độ bất định và chi phí mô hình hóa.

## 1. Frequentist Approaches

### 1.1. Lasso (L1 Regularization)

**Lasso** sets some coefficients **exactly to 0** → automatic feature selection.

![Lasso Feature Selection]({{ site.baseurl }}/img/chapter_img/chapter07/lasso_feature_selection.png)

Ví dụ trong hình dùng một dataset có 20 features nhưng chỉ 5 feature đầu có hệ số thật sự khác 0. Khi $$\alpha$$ còn rất nhỏ như 0.001 hoặc 0.01, regularization quá yếu nên mô hình vẫn giữ lại khoảng 13 feature, nghĩa là còn nhiều biến nhiễu lọt vào mô hình. Khi tăng lên mức trung bình như 0.1, các hệ số bắt đầu co mạnh hơn về 0 nhưng số biến được giữ lại vẫn còn khá lớn. Chỉ khi $$\alpha$$ đủ mạnh, chẳng hạn 0.5, ta mới thấy rõ hiệu ứng thưa hơn: nhiều hệ số bị đẩy về 0 và số feature được chọn giảm xuống. Bài học trực tiếp từ ví dụ này là Lasso thực hiện feature selection bằng cách ép một số hệ số về đúng 0, và mức độ **sparsity** tăng lên khi regularization mạnh hơn.

### 1.2. Cross-Validation để Chọn α

![Lasso CV and Regularization Path]({{ site.baseurl }}/img/chapter_img/chapter07/lasso_cv_regularization_path.png)

Kết quả cross-validation trong ví dụ này chọn $$\alpha=1.0$$ như mức regularization tốt nhất theo năng lực dự báo ngoài mẫu. Ở mức đó, mô hình giữ lại 7 feature, nhiều hơn một chút so với 5 feature thật sự liên quan, nhưng vẫn khá gần với cấu trúc thưa thật của dữ liệu. Regularization path ở panel bên phải bổ sung một trực giác rất quan trọng: khi $$\alpha$$ còn nhỏ, hầu hết hệ số đều khác 0 và có độ lớn đáng kể; khi $$\alpha$$ tăng dần, các hệ số co lại về 0 theo những tốc độ khác nhau; và những feature mang tín hiệu thật thường “trụ” lâu hơn các biến nhiễu. Vì vậy, cross-validation không chỉ giúp chọn mức regularization tối ưu mà còn cho ta một cách nhìn động về việc từng biến rời khỏi mô hình như thế nào.

## 2. Bayesian Approaches

### 2.1. Laplace Prior (Bayesian Lasso)

**Laplace prior** = Bayesian equivalent of Lasso.

$$
\beta_j \sim \text{Laplace}(0, b)
$$

```python
import pymc as pm
import arviz as az

# Bayesian Lasso
with pm.Model() as bayesian_lasso:
    # Laplace priors
    alpha = pm.Normal('alpha', 0, 1)
    beta = pm.Laplace('beta', 0, 0.3, shape=p)  # Laplace!
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + pm.math.dot(X_z, beta)
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    trace_lasso = pm.sample(1000, tune=500, chains=2, random_seed=42,
                           return_inferencedata=True, progressbar=False)

# Extract coefficients
beta_lasso = trace_lasso.posterior['beta'].values.reshape(-1, p).mean(axis=0)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Coefficients
axes[0].bar(range(p), true_coef, alpha=0.5, label='True', edgecolor='black')
axes[0].bar(range(p), beta_lasso, alpha=0.7, label='Bayesian Lasso',
           edgecolor='black')
axes[0].axhline(0, color='red', linestyle='--', linewidth=2)
axes[0].set_xlabel('Feature Index', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
axes[0].set_title('BAYESIAN LASSO\n(Laplace Prior)',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')

# Posterior distributions (first 6 features)
beta_samples = trace_lasso.posterior['beta'].values.reshape(-1, p)
for i in range(6):
    axes[1].hist(beta_samples[:, i], bins=30, alpha=0.5, density=True,
                label=f'β{i}', edgecolor='black')
axes[1].axvline(0, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Coefficient Value', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('POSTERIOR DISTRIBUTIONS\nFirst 6 features',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=10)
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

### 2.2. Horseshoe Prior

**Horseshoe prior** linh hoạt hơn Laplace prior vì nó vừa cho phép một số hệ số thật sự lớn tồn tại nhờ phần đuôi dày, vừa co rất mạnh những hệ số nhỏ về gần 0. Chính khả năng vừa “tha” cho tín hiệu mạnh vừa “phạt” mạnh nhiễu yếu khiến horseshoe trở thành một prior đặc biệt hấp dẫn trong các bài toán sparse signals.

```python
# Horseshoe prior
with pm.Model() as horseshoe_model:
    alpha = pm.Normal('alpha', 0, 1)
    
    # Horseshoe prior
    tau = pm.HalfCauchy('tau', 1)  # Global shrinkage
    lambda_j = pm.HalfCauchy('lambda', 1, shape=p)  # Local shrinkage
    beta = pm.Normal('beta', 0, tau * lambda_j, shape=p)
    
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + pm.math.dot(X_z, beta)
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    trace_horseshoe = pm.sample(1000, tune=500, chains=2, random_state=42,
                               return_inferencedata=True, progressbar=False)

# Extract
beta_horseshoe = trace_horseshoe.posterior['beta'].values.reshape(-1, p).mean(axis=0)

# Compare all methods
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

methods = [
    ('True', true_coef, 'blue'),
    ('Lasso (Freq.)', lasso_cv.coef_, 'green'),
    ('Bayesian Lasso', beta_lasso, 'orange'),
    ('Horseshoe', beta_horseshoe, 'red')
]

for idx, (name, coef, color) in enumerate(methods):
    axes[idx//2, idx%2].bar(range(p), coef, alpha=0.7, color=color,
              edgecolor='black')
    axes[idx//2, idx%2].axhline(0, color='black', linestyle='--', linewidth=2)
    axes[idx//2, idx%2].set_xlabel('Feature Index', fontsize=12, fontweight='bold')
    axes[idx//2, idx%2].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
    axes[idx//2, idx%2].set_title(f'{name}\n' +
                                 f'Non-zero: {np.sum(np.abs(coef) > 0.1)}/{p}',
                                 fontsize=14, fontweight='bold')
    axes[idx//2, idx%2].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("FEATURE SELECTION COMPARISON")
print("=" * 70)
print(f"\nTrue non-zero: 5")
print(f"Lasso: {np.sum(np.abs(lasso_cv.coef_) > 0.1)} selected")
print(f"Bayesian Lasso: {np.sum(np.abs(beta_lasso) > 0.1)} selected")
print(f"Horseshoe: {np.sum(np.abs(beta_horseshoe) > 0.1)} selected")
print("=" * 70)
```

## 3. Posterior Inclusion Probabilities

Ưu điểm quan trọng của cách tiếp cận Bayesian là nó không chỉ đưa ra một danh sách biến được chọn, mà còn định lượng được độ bất định của chính quá trình lựa chọn đó. **Posterior Inclusion Probability (PIP)** được hiểu như xác suất hậu nghiệm để một hệ số đủ khác 0 theo một tiêu chuẩn thực dụng, và nhờ vậy nó cho phép ta nói về mức độ chắc chắn của tầm quan trọng biến, thay vì chỉ nói “được chọn” hay “không được chọn”.

```python
# Compute PIPs
beta_samples_horseshoe = trace_horseshoe.posterior['beta'].values.reshape(-1, p)

# PIP = proportion of posterior samples where |β| > threshold
threshold = 0.1
pips = np.mean(np.abs(beta_samples_horseshoe) > threshold, axis=0)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# PIPs
axes[0].bar(range(p), pips, alpha=0.7, edgecolor='black')
axes[0].axhline(0.5, color='red', linestyle='--', linewidth=2,
               label='Threshold = 0.5')
axes[0].set_xlabel('Feature Index', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Posterior Inclusion Probability', fontsize=12, fontweight='bold')
axes[0].set_title('POSTERIOR INCLUSION PROBABILITIES\n' +
                 'P(|β| > 0.1 \\mid data)',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')
axes[0].set_ylim(0, 1)

# Coefficient vs PIP
beta_mean = beta_samples_horseshoe.mean(axis=0)
axes[1].scatter(beta_mean, pips, s=100, alpha=0.7, edgecolors='black')
for i in range(p):
    axes[1].text(beta_mean[i], pips[i], str(i), fontsize=9, ha='center', va='center')
axes[1].axhline(0.5, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[1].axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.7)
axes[1].set_xlabel('Mean Coefficient', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Posterior Inclusion Probability', fontsize=12, fontweight='bold')
axes[1].set_title('COEFFICIENT vs PIP\nLarge |β| → High PIP',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("FEATURES WITH HIGH PIP (> 0.5)")
print("=" * 70)
selected = np.where(pips > 0.5)[0]
print(f"\nSelected features: {selected}")
print(f"True relevant: [0, 1, 2, 3, 4]")
print("\n→ Bayesian approach quantifies uncertainty!")
print("=" * 70)
```

## 4. Applied Case Study (Phan 3): Stability selection + interpretation risk

Trong bai toan thuc te, mot feature duoc chon 1 lan chua du de ket luan no quan trong. Ta can kiem tra **do on dinh cua feature selection** qua nhieu lan resampling.

```python
import numpy as np

def ridge_fit(X, y, lam):
    p = X.shape[1]
    eye = np.eye(p)
    return np.linalg.solve(X.T @ X + lam * eye, X.T @ y)

def bootstrap_stability(X, y, lam, n_boot=200, threshold=0.15, seed=42):
    rng = np.random.default_rng(seed)
    n, p = X.shape
    picks = np.zeros((n_boot, p), dtype=int)

    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        Xb, yb = X[idx], y[idx]
        beta_b = ridge_fit(Xb, yb, lam)
        picks[b] = (np.abs(beta_b) > threshold).astype(int)

    return picks.mean(axis=0)  # selection frequency

stability = bootstrap_stability(X_train_z, y_train_z, best_lambda)

# Quy tac don gian: chon bien co tan suat xuat hien >= 0.7
stable_features = np.where(stability >= 0.7)[0]
print("Stable features (freq >= 0.7):", stable_features)
```

### 4.1. Uncertainty-aware thresholds

Thay vi mot nguong co dinh duy nhat, hay bao cao ket qua theo nhieu muc:

- **Nong (>= 0.9)**: bang chung rat manh, de dua vao mo hinh dien giai chinh.
- **Am (0.7 - 0.9)**: kha on dinh, can doi chieu domain knowledge.
- **Yeu (< 0.7)**: chua on dinh, uu tien xem nhu feature du phong.

Voi Bayesian models, ban co the ghep them nguong PIP (vi du PIP >= 0.8) de bao cao selection uncertainty mot cach minh bach.

### 4.2. Interpretation risks trong machine learning

Ngay ca khi feature duoc chon on dinh, dien giai van co rui ro:

1. **Collinearity**: feature duoc chon co the la dai dien cho mot cum bien tuong quan, khong nhat thiet la nguyen nhan truc tiep.
2. **Proxy bias**: feature co the dong vai tro bien thay the cho dac trung nhay cam.
3. **Data drift**: tan suat duoc chon co the thay doi theo thoi gian khi phan phoi du lieu doi.
4. **Actionability gap**: feature quan trong ve mat du bao chua chac da huu ich cho quyet dinh van hanh.

**Decision checkpoint 3 (ket thuc case study)**:
- Bao cao dong thoi: performance ngoai mau + uncertainty (PIP/stability) + canh bao dien giai.
- Chi chot danh sach feature "hanh dong" sau khi da qua 3 lop kiem tra tren.

Neu ban muon tai lap toan bo case study da trinh bay xuyen suot 7.1 -> 7.3, co the chay script:

`python img/chapter_img/chapter07/generate_applied_ml_workflow_tradeoffs.py`

## 5. Khi nào Dùng Method Nào?

| Method | Pros | Cons | When to Use |
|--------|------|------|-------------|
| **Lasso** | Fast, sparse | No uncertainty | Large n, quick results |
| **Bayesian Lasso** | Uncertainty, flexible | Slower | Need uncertainty quantification |
| **Horseshoe** | Heavy tails, flexible | Complex | Strong sparsity assumption |
| **Spike-and-Slab** | Explicit selection | Very slow | Small p, explicit probabilities |

## Tóm tắt

Feature selection là bài toán chọn ra những predictor thật sự liên quan khi số biến ứng viên lớn và nguy cơ overfitting hiện hữu. Lasso giải bài toán này bằng cách dùng L1 penalty để tạo lời giải thưa, Bayesian Lasso diễn giải cùng ý tưởng ấy qua Laplace prior, còn horseshoe prior mang lại một cơ chế co rút tinh tế hơn, đặc biệt hữu ích khi ta tin rằng chỉ có một số ít tín hiệu mạnh nổi bật giữa rất nhiều biến yếu. Quan trọng hơn, cách tiếp cận Bayesian còn cung cấp **uncertainty quantification** cho chính việc chọn biến, chẳng hạn qua Posterior Inclusion Probabilities, thay vì chỉ trả về một danh sách biến có vẻ tối ưu.

Điểm quan trọng nhất của bài là chọn biến không nên được hiểu như một thao tác lọc cơ học, mà là một phần của quá trình suy luận về cấu trúc tín hiệu trong dữ liệu.

**Chapter 07 Complete!** Regularization, Bias-Variance, Feature Selection.

## Bài tập

**Bài tập 1**: Generate sparse data. Compare Lasso, Bayesian Lasso, Horseshoe. Which recovers true features best?

**Bài tập 2**: Compute PIPs. Threshold at 0.5, 0.7, 0.9. How does selection change?

**Bài tập 3**: Regularization path: Plot coefficients vs λ. Observe when features enter/exit.

**Bài tập 4**: Real high-dimensional data. Perform feature selection. Interpret selected features.

**Bài tập 5**: Compare computational time: Lasso vs Bayesian approaches. Trade-offs?

## Tài liệu Tham khảo

**Carvalho, C. M., et al. (2010).** "The horseshoe estimator for sparse signals." *Biometrika*, 97(2), 465-480.

**Piironen, J., & Vehtari, A. (2017).** "Sparsity information and regularization in the horseshoe and other shrinkage priors." *Electronic Journal of Statistics*, 11(2), 5018-5051.

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 11: Assumptions, diagnostics, and model evaluation

---

*Chương tiếp theo: [Chapter 08: Model Comparison](/vi/chapter08/)*
