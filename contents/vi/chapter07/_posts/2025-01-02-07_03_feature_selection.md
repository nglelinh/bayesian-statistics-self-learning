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

Trong các bộ dữ liệu sinh học, tài chính hay hành vi người dùng hiện đại, ta thường có hàng chục đến hàng nghìn biến dự báo nhưng chỉ một nhóm nhỏ trong đó thực sự mang tín hiệu. Chọn lọc từng biến bằng phương pháp truyền thống kiểu *stepwise regression* (thêm/bớt theo $$p$$-value) nổi tiếng là mong manh: chỉ cần bỏ đi vài dòng dữ liệu, danh sách biến "có ý nghĩa" đã đổi khác hoàn toàn, nhất là khi các biến có đa cộng tuyến.

Thống kê Bayes tiếp cận chọn lọc đặc trưng theo hướng nhân văn và trung thực hơn nhiều: thay vì ép buộc câu trả lời cứng "chọn hay bỏ", ta tính **xác suất hậu nghiệm chọn biến (Posterior Inclusion Probability — PIP)** hoặc dùng **prior co cụm liên tục (Horseshoe)** để giữ trọn vẹn bất định chọn mô hình.

---

## Mục tiêu học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **chọn biến (feature selection)** như bài toán xác định những biến dự báo thực sự quan trọng trong số rất nhiều biến ứng viên. Bài học trình bày các hướng tiếp cận Bayes như tiên nghiệm Laplace, spike-and-slab và horseshoe, đồng thời so sánh với các phương pháp tần suất quen thuộc như Lasso hay chọn biến từng bước (stepwise). Mục tiêu không chỉ là biết các công cụ hiện có, mà là hiểu mỗi công cụ mã hóa giả định gì về độ thưa của mô hình và khi nào nên áp dụng từng cách tiếp cận trong dữ liệu nhiều chiều.


## Bản đồ kiến thức nền: Không gian $$2^p$$ mô hình, PIP và Prior Co cụm Thưa

Để nắm chắc chiến lược chọn lọc biến Bayes, hãy kết nối ba trụ cột:

- **Vấn đề tổ hợp $$2^p$$ mô hình & Bất ổn của Stepwise:** Với $$p$$ biến dự báo, có tới $$2^p$$ tập con mô hình khả dĩ. Các thuật toán tham lam chọn ra đúng một tập con duy nhất thường đánh giá quá cao độ chắc chắn của các hệ số còn lại (*post-selection inference bias*).
- **Spike-and-Slab & Xác suất chọn biến (PIP):** Mô hình hóa mỗi hệ số qua biến chỉ thị $$\gamma_j \in \{0, 1\}$$: nếu $$\gamma_j = 0$$ hệ số nằm ở đỉnh nhọn tại 0 (*spike*); nếu $$\gamma_j = 1$$ hệ số lấy từ phân phối rộng (*slab*). Trung bình hậu nghiệm $$\mathrm{PIP}_j = P(\gamma_j = 1 \mid y)$$ cho biết xác suất biến $$j$$ thuộc mô hình.
- **Co cụm liên tục (Horseshoe) & Lựa chọn theo Dự báo (Projection Predictive):** Trong thực hành với PyMC/Stan, lấy mẫu biến rời rạc $$\gamma_j$$ có thể khó hội tụ; prior Horseshoe (liên tục, thân thiện với HMC/NUTS) và phương pháp *projection predictive* (Piironen & Vehtari) là lựa chọn hiện đại vừa ổn định vừa đạt độ chính xác dự báo cao.

---

## Giới thiệu: Bài toán khi có quá nhiều biến dự báo

Giả sử bạn có 100 biến dự báo tiềm năng nhưng chỉ khoảng 5 biến trong số đó thực sự mang tín hiệu. Nếu giữ toàn bộ biến, mô hình dễ bị quá khớp; nếu thử mọi tổ hợp có thể, chi phí tính toán sẽ bùng nổ vì số mô hình lên tới $$2^{100}$$; còn nếu kiểm định từng biến riêng lẻ, ta lại đối mặt với nguy cơ **phát hiện sai (false discoveries)** do kiểm định lặp nhiều lần (multiple testing). Vì vậy, mục tiêu của chọn biến không chỉ là làm mô hình gọn hơn, mà là nhận diện một cách có nguyên tắc các biến thực sự liên quan trong khi vẫn kiểm soát được độ bất định và chi phí tính toán.

## 1. Các phương pháp tần suất (Frequentist Approaches)

### 1.1. Lasso (Điều chuẩn L1)

**Lasso** có khả năng đưa một số hệ số về **đúng bằng 0**, nhờ đó thực hiện chọn biến tự động.

![Lasso Feature Selection]({{ site.baseurl }}/img/chapter_img/chapter07/lasso_feature_selection.png)

Ví dụ trong hình sử dụng một tập dữ liệu gồm 20 đặc trưng, trong đó chỉ 5 đặc trưng đầu có hệ số thật khác 0. Khi $$\alpha$$ còn rất nhỏ như 0.001 hoặc 0.01, điều chuẩn quá yếu nên mô hình vẫn giữ khoảng 13 đặc trưng, tức còn nhiều biến nhiễu lọt vào. Khi tăng lên mức trung bình như 0.1, các hệ số bắt đầu co mạnh hơn về 0 nhưng số biến được giữ lại vẫn còn lớn. Chỉ khi $$\alpha$$ đủ mạnh (chẳng hạn 0.5), hiệu ứng thưa mới thể hiện rõ: nhiều hệ số bị ép về đúng 0 và số đặc trưng được chọn giảm xuống. Như vậy, Lasso chọn biến bằng cách triệt tiêu trực tiếp một số hệ số, và mức độ **thưa (sparsity)** tăng lên khi cường độ điều chuẩn mạnh hơn.

### 1.2. Chọn $$\alpha$$ bằng kiểm định chéo (Cross-Validation)

![Lasso CV and Regularization Path]({{ site.baseurl }}/img/chapter_img/chapter07/lasso_cv_regularization_path.png)

Kết quả kiểm định chéo trong ví dụ này chọn $$\alpha=1.0$$ làm mức điều chuẩn tối ưu theo năng lực dự báo ngoài mẫu. Ở mức này, mô hình giữ lại 7 đặc trưng — nhiều hơn một chút so với 5 đặc trưng thật sự liên quan nhưng đã khá sát với cấu trúc thưa của dữ liệu. Đường điều chuẩn (regularization path) ở hình bên phải bổ sung một trực giác quan trọng: khi $$\alpha$$ nhỏ, phần lớn hệ số khác 0 và có độ lớn đáng kể; khi $$\alpha$$ tăng dần, các hệ số co về 0 với tốc độ khác nhau, và những đặc trưng mang tín hiệu thật thường tồn tại lâu hơn các biến nhiễu. Nhờ vậy, kiểm định chéo không chỉ chọn mức điều chuẩn tối ưu mà còn cho thấy trình tự từng biến rời khỏi mô hình.

## 2. Các phương pháp Bayes (Bayesian Approaches)

### 2.1. Tiên nghiệm Laplace (Bayesian Lasso)

**Tiên nghiệm Laplace** là phiên bản tương ứng trong thống kê Bayes của hồi quy Lasso:

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

### 2.2. Tiên nghiệm Horseshoe (Horseshoe Prior)

**Tiên nghiệm Horseshoe** linh hoạt hơn tiên nghiệm Laplace vì nó vừa cho phép một số hệ số thực sự lớn tồn tại nhờ phần đuôi dày, vừa co rất mạnh các hệ số nhỏ về gần 0. Nhờ cơ chế đồng thời giữ lại tín hiệu mạnh và nén chặt nhiễu yếu, horseshoe trở thành lựa chọn rất hiệu quả trong các bài toán có tín hiệu thưa.

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
    
    trace_horseshoe = pm.sample(1000, tune=500, chains=2, random_seed=42,
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

### Thử nghiệm: So sánh cơ chế co rút của Gaussian, Laplace và Horseshoe

Với 50 hệ số nhưng chỉ 5 hệ số thật sự lớn, hãy so sánh trung bình hậu nghiệm và đường cong co rút của từng loại tiên nghiệm.

<div class="interactive-demo" markdown="1">
<div data-demo="horseshoe-explainer" data-lang="vi"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 3. Xác suất hậu nghiệm chọn biến (Posterior Inclusion Probabilities)

Ưu điểm quan trọng của cách tiếp cận Bayes là không chỉ trả về một danh sách biến được chọn, mà còn định lượng được độ bất định của chính việc lựa chọn đó. **Xác suất hậu nghiệm chọn biến (Posterior Inclusion Probability — PIP)** đo xác suất hậu nghiệm để độ lớn của một hệ số vượt qua một ngưỡng thực dụng khác 0, cho phép ta đánh giá mức độ chắc chắn về tầm quan trọng của từng biến thay vì chỉ đưa ra quyết định nhị phân chọn hoặc bỏ.

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

## 4. Nghiên cứu tình huống ứng dụng (Phần 3): Độ ổn định chọn biến và rủi ro diễn giải

Trong bài toán thực tế, một đặc trưng được chọn trong một lần chạy đơn lẻ chưa đủ để khẳng định nó thực sự quan trọng. Ta cần kiểm tra **độ ổn định của việc chọn biến (stability selection)** qua nhiều lần lấy mẫu lại (resampling).

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

### 4.1. Phân tầng ngưỡng theo độ bất định

Thay vì dùng một ngưỡng cắt cứng duy nhất, nên báo cáo kết quả theo nhiều mức độ tin cậy:

- **Mức cao ($$\ge 0.9$$)**: bằng chứng rất mạnh, phù hợp để đưa vào mô hình diễn giải chính.
- **Mức trung bình ($$0.7 - 0.9$$)**: khá ổn định, cần đối chiếu thêm với kiến thức chuyên môn.
- **Mức thấp ($$< 0.7$$)**: chưa ổn định, chỉ nên xem là đặc trưng dự phòng.

Với mô hình Bayes, ta có thể kết hợp thêm ngưỡng PIP (ví dụ $$\text{PIP} \ge 0.8$$) để trình bày minh bạch độ bất định của việc chọn biến.

### 4.2. Rủi ro diễn giải trong học máy

Ngay cả khi một đặc trưng được chọn ổn định, việc diễn giải vẫn tiềm ẩn nhiều rủi ro:

1. **Đa cộng tuyến (Collinearity)**: đặc trưng được chọn có thể chỉ đại diện cho một cụm biến tương quan với nhau, không nhất thiết là nguyên nhân trực tiếp.
2. **Thiên lệch biến đại diện (Proxy bias)**: đặc trưng có thể vô tình đóng vai trò biến thay thế cho các thuộc tính nhạy cảm.
3. **Trôi dữ liệu (Data drift)**: tần suất được chọn có thể thay đổi theo thời gian khi phân phối dữ liệu biến động.
4. **Khoảng cách với khả năng hành động (Actionability gap)**: một đặc trưng quan trọng về mặt dự báo chưa chắc đã can thiệp được trong vận hành thực tế.

**Điểm kiểm tra quyết định 3 (kết thúc nghiên cứu tình huống)**:
- Báo cáo đồng thời hiệu năng ngoài mẫu, độ bất định chọn biến (PIP/stability) và các cảnh báo diễn giải.
- Chỉ chốt danh sách đặc trưng phục vụ hành động sau khi đã kiểm tra đầy đủ cả ba lớp trên.

Nếu muốn tái lập toàn bộ nghiên cứu tình huống xuyên suốt các bài 7.1 đến 7.3, bạn có thể chạy script:

`python img/chapter_img/chapter07/generate_applied_ml_workflow_tradeoffs.py`

## 5. Khi nào nên dùng phương pháp nào?

| Phương pháp | Ưu điểm | Hạn chế | Khi nào nên dùng |
|--------|------|------|-------------|
| **Lasso** | Nhanh, tạo lời giải thưa | Không định lượng độ bất định | Cỡ mẫu lớn, cần kết quả nhanh |
| **Bayesian Lasso** | Có độ bất định, linh hoạt | Chậm hơn | Cần định lượng độ bất định của hệ số |
| **Horseshoe** | Đuôi dày, co rút thích nghi linh hoạt | Phức tạp hơn | Giả định tín hiệu có độ thưa mạnh |
| **Spike-and-Slab** | Chọn biến tường minh | Rất chậm | Số biến $$p$$ nhỏ, cần xác suất chọn biến trực tiếp |

## Tóm tắt

Chọn biến (feature selection) nhằm nhận diện các biến dự báo thực sự liên quan khi số biến ứng viên lớn và nguy cơ quá khớp cao. Lasso sử dụng phạt L1 để tạo lời giải thưa, Bayesian Lasso biểu diễn cùng ý tưởng qua tiên nghiệm Laplace, còn tiên nghiệm horseshoe mang lại cơ chế co rút chọn lọc hơn khi chỉ có một số ít tín hiệu mạnh nằm lẫn giữa nhiều biến nhiễu. Quan trọng hơn, hướng tiếp cận Bayes cung cấp khả năng **định lượng độ bất định** cho quá trình chọn biến (chẳng hạn qua Posterior Inclusion Probabilities), thay vì chỉ trả về một danh sách cố định.

Chọn biến không nên bị xem như thao tác lọc cơ học, mà là một phần của quá trình suy luận về cấu trúc tín hiệu trong dữ liệu.

Kết thúc Chương 07 về điều chuẩn (Regularization), đánh đổi độ lệch – phương sai (Bias-Variance) và chọn biến (Feature Selection).


## Khung giải thích (nên đọc chậm): Tính Xác suất chọn biến (PIP) từ trọng số hậu nghiệm của không gian mô hình

Khi nhiều mô hình con cùng giải thích dữ liệu gần tương đương nhau (đặc biệt khi hai biến dự báo tương quan mạnh), PIP giúp ta không đưa ra kết luận cực đoan. Hãy đi qua 3 bước:

1. **Tính xác suất hậu nghiệm $$P(M_k \mid y)$$ cho từng mô hình con $$M_k$$** (tổng các xác suất mô hình bằng 1).
2. **Với mỗi biến $$X_j$$, cộng xác suất hậu nghiệm của tất cả các mô hình có chứa $$X_j$$:**
   $$\mathrm{PIP}_j = \sum_{k:\; X_j \in M_k} P(M_k \mid y).$$
3. **Diễn giải theo ngưỡng hành động:** $$\mathrm{PIP}_j > 0.5$$ tương ứng mô hình xác suất trung vị (*median probability model*); nếu hai biến tương quan cao cùng chia nhau $$\mathrm{PIP} \approx 0.45$$ mỗi biến, tổng xác suất có ít nhất một trong hai biến lại rất cao ($$\approx 0.90$$).

### Ví dụ tính toán cầm tay chỉ việc: Tính PIP khi $$X_2$$ và $$X_3$$ đa cộng tuyến

Giả sử có 3 biến dự báo $$X_1, X_2, X_3$$ (trong đó $$X_2$$ và $$X_3$$ tương quan mạnh với nhau). Ta xét 4 mô hình có xác suất hậu nghiệm đáng kể:

| Mô hình $$M_k$$ | Các biến có mặt | Xác suất hậu nghiệm $$P(M_k \vert y)$$ |
| --- | --- | --- |
| $$M_1$$ | $$\{X_1, X_2\}$$ | $$0.45$$ |
| $$M_2$$ | $$\{X_1, X_3\}$$ | $$0.40$$ |
| $$M_3$$ | $$\{X_1, X_2, X_3\}$$ | $$0.10$$ |
| $$M_4$$ | $$\{X_1\}$$ | $$0.05$$ |
| **Tổng** | — | **$$1.00$$** |

Tính tay PIP cho từng biến:
- $$\mathrm{PIP}(X_1) = 0.45 + 0.40 + 0.10 + 0.05 = 1.00$$ (chắc chắn quan trọng).
- $$\mathrm{PIP}(X_2) = 0.45 + 0.10 = 0.55$$.
- $$\mathrm{PIP}(X_3) = 0.40 + 0.10 = 0.50$$.

Nếu chỉ chọn mô hình đỉnh $$M_1$$, ta sẽ vứt bỏ $$X_3$$ và tuyên bố nhầm rằng $$X_3$$ "không liên quan". Bảng PIP cho thấy đúng sự thật: dữ liệu cần $$X_1$$ cùng với *ít nhất một trong hai* biến $$X_2$$ hoặc $$X_3$$ (xác suất $$0.45 + 0.40 + 0.10 = 0.95$$), nhưng không đủ để phân định rạch ròi giữa hai biến tương quan này.

**Hiểu lầm cần tránh:** Nhầm rằng $$\mathrm{PIP}_j = 0.50$$ nghĩa là biến $$X_j$$ vô dụng. Khi có đa cộng tuyến, xác suất bị chia đôi giữa các biến thay thế nhau — cần kiểm tra cả xác suất hậu nghiệm đồng thời của cụm biến.

**Kiểm tra nhanh:** Trong ví dụ trên, xác suất mô hình chứa đồng thời cả hai biến tương quan $$X_2$$ và $$X_3$$ chỉ là $$P(M_3 \mid y) = 0.10$$ — phản ánh cơ chế "dao cạo Occam" tự động phạt độ phức tạp thừa của suy diễn Bayes.

---

## Video tham khảo

- [Regularization Part 2: Lasso (L1) Regression](https://www.youtube.com/watch?v=NGf0voTMlcs) — StatQuest with Josh Starmer, English. **Xem trước**. Giải thích vì sao phạt L1 có thể đưa một số hệ số về đúng 0 để chọn biến.
- [Lecture 31 Bayesian Regression and Variable Selection (Part A)](https://www.youtube.com/watch?v=Mv6MSIVKEIc) — Nicholas Zabaras, English. Trình bày hồi quy Bayes và bài toán chọn biến bằng các phân phối tiên nghiệm co rút khi có nhiều biến dự báo.
- [Regularized Horseshoe - Aki Vehtari](https://www.youtube.com/watch?v=EuhvfvY8ISc) — Stan, English. Giới thiệu tiên nghiệm regularized horseshoe cho bài toán tín hiệu thưa trong thống kê Bayes.

## Bài tập

**Bài tập 1**: Sinh dữ liệu có cấu trúc thưa, so sánh Lasso, Bayesian Lasso và Horseshoe để xem phương pháp nào khôi phục các đặc trưng thật tốt nhất.

**Bài tập 2**: Tính xác suất hậu nghiệm chọn biến (PIP) và kiểm tra tập biến được chọn thay đổi ra sao ở các ngưỡng 0.5, 0.7 và 0.9.

**Bài tập 3**: Vẽ đường điều chuẩn (regularization path) của các hệ số theo $$\lambda$$ và quan sát thời điểm từng đặc trưng đi vào hoặc rời khỏi mô hình.

**Bài tập 4**: Thực hiện chọn biến trên một tập dữ liệu thực nhiều chiều và diễn giải các đặc trưng được chọn.

**Bài tập 5**: So sánh thời gian tính toán giữa Lasso và các phương pháp Bayes, đồng thời phân tích những đánh đổi đi kèm.

## Tài liệu tham khảo

**Carvalho, C. M., et al. (2010).** "The horseshoe estimator for sparse signals." *Biometrika*, 97(2), 465-480.

**Piironen, J., & Vehtari, A. (2017).** "Sparsity information and regularization in the horseshoe and other shrinkage priors." *Electronic Journal of Statistics*, 11(2), 5018-5051.

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 11: Assumptions, diagnostics, and model evaluation

---

*Chương tiếp theo: [Chapter 08: Model Comparison]({{ site.baseurl }}/contents/vi/chapter08/)*
