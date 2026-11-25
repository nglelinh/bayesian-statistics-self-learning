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

Một mô hình quá đơn giản bỏ sót quy luật thật (dưới khớp — *underfitting*); một mô hình quá phức tạp học thuộc luôn cả nhiễu ngẫu nhiên của tập huấn luyện (quá khớp — *overfitting*). Giữa hai thái cực ấy là một định luật toán học chi phối mọi bài toán dự báo từ hồi quy tuyến tính đến mạng nơ-ron: **đánh đổi độ chệch – phương sai (bias–variance tradeoff)**.

Bài học này không chỉ chứng minh phép phân rã sai số dự báo thành ba thành phần bất biến, mà còn giải thích cách thống kê Bayes tiếp cận sự đánh đổi này bằng tích phân trên hậu nghiệm (*Bayesian model averaging*) và đường cong học (*learning curves*).

---

## Mục tiêu học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu rõ **sự đánh đổi giữa độ lệch và phương sai (bias-variance tradeoff)** — một trong những khái niệm nền tảng của học máy và thống kê. Bài học giải thích vì sao mô hình quá đơn giản thường có **độ lệch cao (high bias)**, vì sao mô hình quá phức tạp thường có **phương sai cao (high variance)**, và vì sao mục tiêu của chọn mô hình không phải là đẩy một thành phần xuống thấp nhất có thể, mà là tìm điểm cân bằng giúp tổng sai số dự báo nhỏ nhất. Đây là cơ sở trực tiếp để hiểu điều chuẩn, quá khớp và logic của việc lựa chọn mô hình.


## Kiến thức cần nhớ: Phân rã Sai số Dự báo, Đường cong Học và Cách giải của Bayes

Bức tranh tổng thể về độ phức tạp mô hình đứng trên ba trụ cột:

- **Phân rã sai số ngoài mẫu (Expected Prediction Error):** Tại một điểm mới $$x_0$$, sai số bình phương kỳ vọng luôn tách thành: $$\mathbb{E}[(y_0 - \hat f(x_0))^2] = \mathrm{Bias}(\hat f(x_0))^2 + \mathrm{Var}(\hat f(x_0)) + \sigma_\varepsilon^2$$. Thành phần cuối $$\sigma_\varepsilon^2$$ là **nhiễu không thể khử (irreducible noise)** — không mô hình nào vượt qua được trần này.
- **Chẩn đoán bằng Đường cong học (Learning Curves):** Vẽ sai số tập huấn luyện và tập kiểm định theo cỡ mẫu $$n$$ giúp phân biệt tức thì hai bệnh: hai đường hội tụ sát nhau ở mức lỗi cao là **High Bias** (cần mô hình giàu biểu diễn hơn); hai đường cách xa nhau với lỗi huấn luyện rất thấp là **High Variance** (cần thêm dữ liệu hoặc điều chuẩn mạnh hơn).
- **Cách tiếp cận của Bayes:** Thay vì chọn một điểm tham số cố định (dễ có phương sai cao), dự báo hậu nghiệm lấy trung bình có trọng số trên toàn bộ phân phối hậu nghiệm $$\mathbb{E}_{\theta \mid y}[f(x_0; \theta)]$$ — tự động giảm phương sai nhờ hiệu ứng tổ hợp (*ensembling*) kết hợp điều chuẩn từ prior.

---

## Giới thiệu: Hai nguồn sai số

Khi một mô hình dự đoán sai, sai số đó thường không bắt nguồn từ một nguyên nhân duy nhất. Một phần sai số xuất phát từ việc mô hình quá đơn giản nên bỏ sót cấu trúc thật của dữ liệu — đó là **độ lệch (bias)**. Phần khác xuất phát từ việc mô hình quá nhạy với dữ liệu huấn luyện, khiến chỉ cần thay đổi mẫu một chút là dự đoán đã dao động mạnh — đó là **phương sai (variance)**. Hai thành phần này thường biến thiên ngược chiều: giảm độ lệch thường làm phương sai tăng, còn ép phương sai xuống quá mạnh lại làm độ lệch tăng lên.

## 1. Định nghĩa độ lệch và phương sai

### 1.1. Định nghĩa toán học

Giả sử ta huấn luyện mô hình nhiều lần trên các tập dữ liệu khác nhau được lấy từ cùng một phân phối.

**Độ lệch (Bias)**: Sai lệch giữa **dự đoán trung bình** và **giá trị thật**:
$$
\text{Bias}[\hat{f}(x)] = \mathbb{E}[\hat{f}(x)] - f(x)
$$

**Phương sai (Variance)**: Mức độ dao động của các dự đoán giữa các tập dữ liệu khác nhau:
$$
\text{Variance}[\hat{f}(x)] = \mathbb{E}[(\hat{f}(x) - \mathbb{E}[\hat{f}(x)])^2]
$$

**Tổng sai số**:
$$
\mathbb{E}[(y - \hat{f}(x))^2] = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}
$$

### 1.2. Trực giác hình học

![Bias-Variance Demonstration]({{ site.baseurl }}/img/chapter_img/chapter07/bias_variance_demonstration.png)

Hình minh họa làm rõ trực giác này. Với mô hình bậc 1, các đường khớp từ nhiều tập dữ liệu khá gần nhau (phương sai thấp), nhưng hầu hết đều lệch xa quy luật thật (độ lệch cao) — đây là trạng thái thiếu khớp điển hình. Với mô hình bậc 3, độ linh hoạt vừa đủ để bám sát quy luật thật mà chưa dao động mạnh giữa các mẫu, nên độ lệch giảm trong khi phương sai vẫn trong tầm kiểm soát — đây là vùng cân bằng tốt của sự đánh đổi. Với mô hình bậc 10, đường trung bình có thể gần quy luật thật hơn (độ lệch thấp hơn), nhưng từng mô hình riêng lẻ lại dao động mạnh theo mẫu huấn luyện (phương sai tăng vọt). Quan sát 50 tập huấn luyện như 50 lần lặp của cùng một bài toán giúp ta hình dung trực tiếp phương sai là mức độ dao động của dự đoán khi dữ liệu thay đổi.

## 2. Phân rã sai số: MSE = Bias² + Variance + Nhiễu

![MSE Decomposition]({{ site.baseurl }}/img/chapter_img/chapter07/mse_decomposition.png)

Nhìn vào phép phân rã MSE, ta thấy ngay vì sao không thể chọn mô hình dựa trên một thành phần đơn lẻ. Ở vùng độ phức tạp thấp (như bậc 1 hoặc 2), thành phần $$\text{Bias}^2$$ lớn vì mô hình quá đơn giản để mô tả dữ liệu, dù phương sai khá thấp. Khi độ phức tạp tăng lên vùng trung gian, hai thành phần cân bằng hơn và tổng MSE đạt mức nhỏ nhất. Nếu tiếp tục tăng độ phức tạp, độ lệch có thể giảm thêm chút ít nhưng phương sai tăng rất mạnh, kéo MSE tăng trở lại. Biểu đồ xếp chồng ở bên phải cho thấy rõ mục tiêu không phải tối thiểu hóa riêng độ lệch hay riêng phương sai, mà là tối thiểu hóa tổng sai số dự báo.

### Thử nghiệm: Độ lệch, phương sai và tổng sai số theo độ phức tạp

Lặp trên 100 tập dữ liệu cho mỗi bậc đa thức để quan sát $$\text{Bias}^2$$ giảm, phương sai tăng, tổng sai số có dạng chữ U, và cách tiên nghiệm chặt (Ridge) nén phương sai.

<div class="interactive-demo" markdown="1">
<div data-demo="biasvar-explainer" data-lang="vi"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 3. Điều chuẩn và sự đánh đổi độ lệch – phương sai

Điều chuẩn đóng vai trò là nút điều chỉnh sự đánh đổi này. Khi điều chuẩn yếu ($$\lambda$$ nhỏ), mô hình linh hoạt hơn nên độ lệch thường thấp nhưng phương sai cao. Khi điều chuẩn mạnh ($$\lambda$$ lớn), mô hình bị ràng buộc đơn giản hơn nên phương sai giảm, đổi lại độ lệch tăng lên.

![Regularization Bias-Variance]({{ site.baseurl }}/img/chapter_img/chapter07/regularization_bias_variance.png)

Ví dụ với đa thức bậc 10 minh họa rõ điểm này. Khi $$\lambda=0.001$$, điều chuẩn quá yếu nên mô hình dao động mạnh, phương sai rất lớn và quá khớp rõ rệt. Khi tăng dần lên $$0.1$$ rồi $$1$$, phương sai giảm đáng kể và mô hình bước vào vùng cân bằng tốt hơn. Nếu tiếp tục tăng lên $$10$$ hay $$100$$, mô hình bị bó quá chặt, đường dự đoán trở nên gần như phẳng, phương sai thấp nhưng độ lệch tăng cao — tức quay trở lại vùng thiếu khớp. Như vậy, $$\lambda$$ không phải càng lớn càng tốt, mà cần được chọn sao cho độ lệch và phương sai cân bằng tốt nhất cho mục tiêu dự báo.

## 4. Góc nhìn Bayes

Trong thống kê Bayes, vai trò của điều chuẩn chuyển thành vai trò của **độ mạnh tiên nghiệm (prior strength)**. Tiên nghiệm yếu để dữ liệu quyết định nhiều hơn nên mô hình linh hoạt hơn nhưng cũng dễ dao động hơn; tiên nghiệm mạnh ràng buộc mô hình chặt hơn giúp giảm phương sai, nhưng có thể làm tăng độ lệch nếu tiên nghiệm quá cứng.

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

## 5. Chiến lược kiểm định và đường cong học (Learning Curves) trong thực tế

Sự đánh đổi độ lệch – phương sai chỉ thực sự trở thành công cụ ra quyết định khi ta đo lường nó trên dữ liệu ngoài mẫu:

- **Điểm trên tập huấn luyện (Train score)** giúp theo dõi khả năng học trên dữ liệu đã thấy.
- **Điểm trên tập kiểm định (Validation score)** đo mức độ khái quát hóa để tinh chỉnh độ phức tạp hoặc độ rộng tiên nghiệm.
- **Điểm trên tập kiểm tra (Test score)** là kết quả báo cáo cuối cùng, chỉ sử dụng đúng một lần sau khi đã chốt lựa chọn mô hình.

Cách đọc nhanh đường cong học:

1. Tập huấn luyện tốt, tập kiểm định kém và khoảng cách giữa hai tập lớn → **phương sai cao (high variance)**, cần điều chuẩn mạnh hơn hoặc bổ sung dữ liệu.
2. Cả tập huấn luyện lẫn tập kiểm định đều kém → **độ lệch cao (high bias)**, cần mô hình linh hoạt hơn hoặc bổ sung đặc trưng phù hợp.
3. Điểm trên tập kiểm định ổn định quanh mức tối ưu khi điều chỉnh cường độ điều chuẩn → đây là vùng cân bằng phù hợp.

## 6. Nghiên cứu tình huống ứng dụng (Phần 2): Tinh chỉnh độ phức tạp bằng tập kiểm định

Tiếp nối thiết lập dữ liệu từ bài 7.1, ta sử dụng công thức nghiệm đóng của hồi quy Ridge để quét qua các cường độ điều chuẩn và chọn mức cân bằng độ lệch – phương sai dựa trên RMSE trên tập validation.

```python
import numpy as np

def ridge_fit(X, y, lam):
    p = X.shape[1]
    eye = np.eye(p)
    return np.linalg.solve(X.T @ X + lam * eye, X.T @ y)

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

lambdas = np.logspace(-3, 2, 30)
val_scores = []
train_scores = []
coefs = []

for lam in lambdas:
    beta_hat = ridge_fit(X_train_z, y_train_z, lam)
    coefs.append(beta_hat)
    train_scores.append(rmse(y_train_z, X_train_z @ beta_hat))
    val_scores.append(rmse(y_val_z, X_val_z @ beta_hat))

best_idx = int(np.argmin(val_scores))
best_lambda = float(lambdas[best_idx])
best_beta = coefs[best_idx]

test_rmse = rmse(y_test_z, X_test_z @ best_beta)

print(f"Best lambda (validation): {best_lambda:.4f}")
print(f"Train RMSE (z-scale): {train_scores[best_idx]:.3f}")
print(f"Validation RMSE (z-scale): {val_scores[best_idx]:.3f}")
print(f"Test RMSE (z-scale): {test_rmse:.3f}")
```

![Applied ML Workflow Tradeoffs]({{ site.baseurl }}/img/chapter_img/chapter07/applied_ml_workflow_tradeoffs.png)

Hình trên tóm tắt ba quyết định chính trong quy trình ứng dụng: (1) chọn cường độ điều chuẩn bằng RMSE trên tập validation, (2) kiểm tra độ lớn hệ số sau khi co rút, và (3) đánh giá độ ổn định khi chọn biến qua tần suất bootstrap.

**Điểm kiểm tra quyết định 2**:
- Nếu chỉ tối ưu RMSE trên tập huấn luyện, mô hình thường bị đẩy vào vùng quá khớp.
- Chỉ khi tối ưu RMSE trên tập validation và giữ tập test cho bước cuối cùng, ta mới có cơ sở đáng tin cậy để đánh giá khả năng khái quát hóa.

## 7. Danh sách kiểm tra tinh chỉnh: Từ đánh đổi đến hành động

Khi cần chọn độ phức tạp mô hình trong bài toán hồi quy hoặc phân lớp:

1. Chọn thước đo phù hợp với mục tiêu bài toán thay vì dùng metric một cách hình thức.
2. Dùng lưới giá trị hợp lý cho cường độ điều chuẩn hoặc độ rộng tiên nghiệm thay vì quét quá rộng thiếu kiểm soát.
3. Theo dõi đồng thời khoảng cách giữa train và validation cùng độ ổn định qua các fold.
4. Kết hợp hiệu năng ngoài mẫu với kiểm tra dự báo hậu nghiệm để phát hiện sai lệch cấu trúc mô hình (model misspecification).
5. Chốt mô hình dựa trên lập luận có thể giải thích được, chứ không chỉ dựa vào điểm số cao nhất đơn thuần.

## Tóm tắt

Sự đánh đổi giữa độ lệch và phương sai cho thấy sai số dự báo không thể được đánh giá chỉ bằng độ khớp trên tập huấn luyện. **Độ lệch (bias)** phản ánh cái giá của một mô hình quá đơn giản, còn **phương sai (variance)** phản ánh cái giá của một mô hình quá nhạy với dữ liệu huấn luyện. Công thức $$\text{MSE}=\text{Bias}^2+\text{Variance}+\text{Irreducible Error}$$ nhắc ta rằng mô hình tốt là mô hình cân bằng được hai xu hướng đối nghịch này. Điều chuẩn là công cụ thực hành để điều chỉnh điểm cân bằng đó, và trong thống kê Bayes, chính độ mạnh của phân phối tiên nghiệm đảm nhiệm vai trò ấy.

Điểm cốt lõi cần ghi nhớ là một mô hình khớp rất sát tập huấn luyện chưa chắc là mô hình tốt; mô hình tốt phải khái quát hóa hiệu quả trên dữ liệu mới.

Bài tiếp theo: **Chọn biến (Feature Selection)** — hoàn tất nghiên cứu tình huống bằng kiểm tra độ ổn định (stability selection) và diễn giải có xét đến độ bất định.


## Giải thích: Tính trực tiếp ba thành phần của MSE để chọn độ phức tạp tối ưu

Khi so sánh 3 mô hình có độ phức tạp tăng dần trên cùng một bài toán có nhiễu nền $$\sigma_\varepsilon = 2.0$$ (tức $$\sigma_\varepsilon^2 = 4.0$$), hãy đọc bảng phân rã theo 3 bước:

1. **Tính $$\mathrm{Bias}^2$$:** Đo sai lệch hệ thống trung bình so với hàm thật $$f(x_0)$$.
2. **Tính $$\mathrm{Variance}$$:** Đo độ dao động của dự báo khi thay đổi tập huấn luyện.
3. **Cộng với nhiễu không thể khử $$\sigma_\varepsilon^2$$:** Chọn mô hình cực tiểu hóa **tổng** cả ba thành phần, chứ không chọn mô hình có Bias = 0!

### Ví dụ tính toán làm từng bước: Chọn giữa Mô hình đơn giản, Vừa phải và Phức tạp

Giả sử hàm thật tại $$x_0$$ là $$f(x_0) = 10.0$$ và nhiễu đo lường có phương sai $$\sigma_\varepsilon^2 = 4.0$$. Kết quả đánh giá ba mô hình:

| Mô hình | $$\mathrm{Bias}$$ | $$\mathrm{Bias}^2$$ | $$\mathrm{Variance}$$ | Nhiễu nền $$\sigma_\varepsilon^2$$ | Tổng MSE dự báo |
| --- | --- | --- | --- | --- | --- |
| Mô hình 1 (Quá đơn giản) | $$-3.0$$ | $$9.00$$ | $$0.50$$ | $$4.00$$ | $$13.50$$ |
| Mô hình 2 (Điều chuẩn vừa phải) | $$-1.0$$ | $$1.00$$ | $$1.50$$ | $$4.00$$ | **$$6.50$$** (tối ưu) |
| Mô hình 3 (Quá phức tạp) | $$0.0$$ | $$0.00$$ | $$6.00$$ | $$4.00$$ | $$10.00$$ |

Dù Mô hình 3 hoàn toàn không chệch ($$\mathrm{Bias} = 0$$), phương sai quá lớn ($$6.00$$) khiến tổng sai số dự báo của nó ($$10.00$$) thua xa Mô hình 2 ($$6.50$$). Đồng thời, không một mô hình nào có thể kéo tổng MSE xuống dưới $$4.00$$ vì nhiễu nền không thể khử.

**Hiểu lầm cần tránh:** Cố gắng tăng độ phức tạp hoặc chạy thêm vòng lặp để kéo lỗi tập huấn luyện xuống gần 0 — khi lỗi huấn luyện thấp hơn cả $$\sigma_\varepsilon^2 = 4.00$$, đó chính là bằng chứng chắc chắn mô hình đang học thuộc nhiễu!

**Kiểm tra nhanh:** Nếu bạn thu thập thêm dữ liệu gấp 4 lần cho Mô hình 3 khiến phương sai của nó giảm 4 lần (từ $$6.00$$ xuống $$1.50$$) trong khi Bias vẫn bằng $$0$$, tổng MSE mới của Mô hình 3 sẽ là $$0 + 1.50 + 4.00 = 5.50$$ — vượt qua Mô hình 2. Điều này giải thích vì sao cỡ mẫu lớn cho phép dùng mô hình phức tạp hơn.

---

## Video tham khảo

- [Machine Learning Fundamentals: Bias and Variance](https://www.youtube.com/watch?v=EuBBz3bI-aA) — StatQuest with Josh Starmer, English. **Xem trước**. Giải thích sự khác biệt giữa mô hình quá đơn giản bị lệch hệ thống và mô hình quá linh hoạt dao động theo mẫu.
- [[Proof] MSE = Variance + Bias²](https://www.youtube.com/watch?v=qmVT35gFW-Q) — math et al, English. Chứng minh hệ thức phân rã MSE thành bình phương độ lệch cộng phương sai.
- [Machine Learning Fundamentals: Cross Validation](https://www.youtube.com/watch?v=fSytzGwwBVw) — StatQuest with Josh Starmer, English. Trình bày kiểm định chéo như cách ước lượng sai số ngoài mẫu, hỗ trợ phần đường cong học và chọn độ phức tạp.

## Bài tập

**Bài tập 1**: Tự cài đặt phép phân rã độ lệch – phương sai từ đầu và kiểm chứng hệ thức $$\text{MSE} = \text{Bias}^2 + \text{Variance}$$ (trên phần sai số của hàm dự đoán).

**Bài tập 2**: Sinh dữ liệu, tính độ lệch và phương sai cho các mô hình có độ phức tạp khác nhau, rồi tìm mức độ phức tạp tối ưu.

**Bài tập 3**: Dùng hồi quy Ridge với nhiều giá trị $$\lambda$$ khác nhau, vẽ đường cong độ lệch – phương sai và tìm $$\lambda$$ tối ưu.

**Bài tập 4**: Xây dựng các mô hình Bayes với nhiều độ lệch chuẩn tiên nghiệm khác nhau, tính phương sai hậu nghiệm và liên hệ với sự đánh đổi độ lệch – phương sai.

**Bài tập 5**: Trên một tập dữ liệu thực, chia tập train/test, minh họa hiện tượng quá khớp bằng đa thức bậc cao và khắc phục bằng điều chuẩn.

## Tài liệu tham khảo

**Hastie, T., Tibshirani, R., & Friedman, J. (2009).** *The Elements of Statistical Learning* (2nd Edition). Springer.
- Chapter 7: Model Assessment and Selection

**James, G., et al. (2013).** *An Introduction to Statistical Learning*. Springer.
- Chapter 2: Statistical Learning

---

*Bài học tiếp theo: [7.3 Feature Selection]({{ site.baseurl }}/contents/vi/chapter07/07_03_feature_selection/)*
