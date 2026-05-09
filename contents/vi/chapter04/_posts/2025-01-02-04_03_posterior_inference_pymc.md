---
layout: post
title: "Bài 4.3: Posterior Inference với PyMC - Từ Theory đến Practice"
chapter: '04'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần biết cách biến regression Bayes từ generative story (câu chuyện sinh dữ liệu) thành model chạy được trong PyMC. Bạn cũng cần hiểu một workflow (quy trình làm việc) thực hành cơ bản: chuẩn hóa dữ liệu, viết prior, khai báo likelihood (hàm hợp lý), lấy mẫu posterior, đọc diagnostics (chẩn đoán) và diễn giải kết quả.

> **Ví dụ mini.** Sau khi đã hiểu generative story và biết chọn prior hợp lý, bước tiếp theo là viết model thật trong PyMC để lấy posterior của intercept (hệ số chặn), slope (hệ số dốc) và noise (độ nhiễu). PyMC không thay bạn nghĩ mô hình; nó giúp bạn triển khai mô hình ấy hiệu quả hơn.
>
> **Câu hỏi tự kiểm tra.** Nếu PyMC đã chạy được posterior rồi, vì sao ta vẫn phải nhìn diagnostics trước khi diễn giải kết quả?

## 1. Từ mô hình trên giấy sang mô hình trong code

Ở bài 4.1 và 4.2, ta đã có đủ ba thành phần: generative story (câu chuyện sinh dữ liệu), prior cho các tham số, và trực giác về regression Bayes.

Bài này chủ yếu làm một bước dịch rất thực tế: chuyển từ suy nghĩ thống kê sang một mô hình có thể chạy được trong PyMC.

Workflow tối thiểu ở đây là chuẩn bị dữ liệu, chuẩn hóa nếu cần, khai báo prior, khai báo likelihood, chạy sampler (bộ lấy mẫu), kiểm tra diagnostics (chẩn đoán), rồi mới đọc posterior.

## 2. Tại sao cần MCMC? Vì không có công thức closed-form

### 2.1. Từ conjugacy đến non-conjugacy

Trong Chapter 2, ta đã học về **conjugate priors** (prior liên hợp):

- **Beta-Binomial**: Prior Beta + Likelihood Binomial → Posterior Beta
- **Gamma-Poisson**: Prior Gamma + Likelihood Poisson → Posterior Gamma
- **Normal-Normal**: Prior Normal + Likelihood Normal → Posterior Normal

Với các cặp liên hợp này, ta có **công thức closed-form** (công thức đóng) để tính posterior trực tiếp:

$$
\theta \mid D \sim \text{Beta}(\alpha_0 + k, \beta_0 + n - k)
$$

Chỉ cần thay số vào công thức là xong. **Không cần máy tính mạnh, không cần lấy mẫu.**

### 2.2. Regression Bayesian: không còn công thức đơn giản

Nhưng với **Bayesian regression**, tình huống phức tạp hơn:

$$
\begin{aligned}
\beta_0 &\sim \mathcal{N}(5, 5) \\
\beta_1 &\sim \mathcal{N}(2, 5) \\
\sigma &\sim \text{HalfNormal}(2) \\
y_i &\sim \mathcal{N}(\beta_0 + \beta_1 x_i, \sigma^2)
\end{aligned}
$$

**Vấn đề:**
- Ba tham số ($\beta_0, \beta_1, \sigma$) phải cập nhật **đồng thời**
- Prior là Normal + HalfNormal (không phải conjugate với likelihood)
- Posterior là phân phối **joint** 3 chiều, không có công thức đơn giản

$$
p(\beta_0, \beta_1, \sigma \mid D) = \frac{p(D \mid \beta_0, \beta_1, \sigma) \cdot p(\beta_0) \cdot p(\beta_1) \cdot p(\sigma)}{p(D)}
$$

Với $p(D) = \int\int\int p(D \mid \beta_0, \beta_1, \sigma) \cdot p(\beta_0) \cdot p(\beta_1) \cdot p(\sigma) \, d\beta_0 \, d\beta_1 \, d\sigma$

**Tích phân này không tính được bằng tay!**

### 2.3. MCMC: lấy mẫu thay vì tính công thức

Khi không có công thức closed-form, ta dùng **MCMC (Markov Chain Monte Carlo)**:

> **Ý tưởng cốt lõi:** Thay vì tính toán toán học phức tạp, ta **lấy mẫu** từ posterior.
>
> Giống như khảo sát dư luận: không hỏi cả 10 triệu người, chỉ cần hỏi 4000 người đại diện.

**MCMC hoạt động như sau:**

1. **Bắt đầu** từ một điểm ngẫu nhiên trong không gian tham số
2. **Di chuyển** đến điểm mới theo quy tắc thông minh (ưu tiên vùng có xác suất cao)
3. **Lặp lại** hàng nghìn lần để tạo "chuỗi" các mẫu
4. **Kết quả:** Tập mẫu phản ánh đúng phân phối posterior

**Ví dụ minh họa:**

```python
# Thay vì tính công thức phức tạp:
posterior = complicated_integral(...)  # ❌ Không tính được!

# Ta lấy mẫu:
with pm.Model() as model:
    # Khai báo priors
    beta_0 = pm.Normal('beta_0', mu=5, sigma=5)
    beta_1 = pm.Normal('beta_1', mu=2, sigma=5)
    sigma = pm.HalfNormal('sigma', sigma=2)
    
    # Likelihood
    mu = beta_0 + beta_1 * x
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
    
    # MCMC: lấy 2000 mẫu từ posterior
    trace = pm.sample(2000)  # ← ĐÂY LÀ MCMC!
    
# Kết quả: trace chứa 2000 bộ (β₀, β₁, σ) từ posterior
# Mỗi bộ là một "thế giới có thể" phù hợp với data
```

**Kết quả MCMC:**

| Sample | β₀ | β₁ | σ |
|--------|----|----|---|
| 1 | 6.8 | 2.1 | 0.6 |
| 2 | 6.5 | 2.2 | 0.5 |
| ... | ... | ... | ... |
| 2000 | 6.9 | 2.0 | 0.7 |

Từ 2000 mẫu này, ta tính được:
- **Posterior mean:** Trung bình của các mẫu
- **95% Credible Interval:** Percentile 2.5% và 97.5%
- **Xác suất β₁ > 0:** Đếm bao nhiêu mẫu có β₁ > 0

### 2.4. So sánh conjugacy vs MCMC

| | Conjugate Priors | MCMC (Regression) |
|---|---|---|
| **Prior** | Beta, Gamma, Normal đơn giản | Nhiều priors phức tạp |
| **Likelihood** | Binomial, Poisson, Normal | Normal với nhiều tham số |
| **Posterior** | Công thức closed-form | Không có công thức |
| **Tính toán** | Thay số vào công thức | Lấy mẫu bằng MCMC |
| **Kết quả** | Phân phối chính xác | Xấp xỉ từ mẫu |
| **Ví dụ** | Beta(17, 103) | 2000 samples (β₀, β₁, σ) |
| **Thời gian** | < 1 giây | 10-60 giây |
| **Độ chính xác** | 100% | ~99% (với đủ mẫu) |

### 2.5. PyMC ẩn đi phức tạp của MCMC

Điều tuyệt vời của PyMC là bạn không cần hiểu sâu về:
- Metropolis-Hastings algorithm
- Gibbs sampling
- NUTS (No-U-Turn Sampler)
- Hamiltonian Monte Carlo

Bạn chỉ cần:
1. Khai báo model (priors + likelihood)
2. Gọi `pm.sample()`
3. Kiểm tra diagnostics (R-hat, ESS)
4. Đọc kết quả

**PyMC tự động:**
- Chọn sampler tốt nhất (thường là NUTS)
- Tự động tune (điều chỉnh) trong giai đoạn warm-up
- Song song hóa nhiều chains
- Phát hiện vấn đề và cảnh báo

### 2.6. Tóm tắt: Khi nào dùng MCMC?

| Tình huống | Phương pháp |
|------------|-------------|
| Conjugate priors + 1 tham số | ✅ Công thức closed-form |
| Non-conjugate hoặc nhiều tham số | ✅ MCMC |
| Regression với >2 tham số | ✅ MCMC (PyMC) |
| Hierarchical models | ✅ MCMC |
| Mixture models | ✅ MCMC |

**Quy tắc đơn giản:**
> Nếu bạn không tính được posterior bằng tay trong 5 phút → Dùng MCMC!

## 3. Một regression Bayes đơn giản trong PyMC có cấu trúc ra sao?

Tư duy đúng là luôn bắt đầu từ prior cho $$\alpha$$, prior cho $$\beta$$, prior cho $$\sigma$$, rồi mới đi đến likelihood:

$$
y_i \sim \mathcal{N}(\alpha + \beta x_i,\sigma).
$$

Trong PyMC, bạn chỉ đang viết lại câu chuyện đó bằng code.

Điều quan trọng là code nên phản ánh mô hình, chứ không phải mô hình bị bóp méo chỉ để khớp với một API cụ thể.

### 3.1. Một ví dụ PyMC tối thiểu nhưng chạy được

Giả sử bạn có một dataset rất nhỏ về chiều cao và cân nặng:

```python
import numpy as np
import pymc as pm
import arviz as az

height = np.array([150, 155, 160, 165, 170, 175, 180, 185], dtype=float)
weight = np.array([50, 54, 57, 62, 66, 70, 76, 82], dtype=float)

x_z = (height - height.mean()) / height.std()
y_z = (weight - weight.mean()) / weight.std()

with pm.Model() as reg_model:
    alpha = pm.Normal("alpha", 0, 1)
    beta = pm.Normal("beta", 0, 1)
    sigma = pm.HalfNormal("sigma", 1)

    mu = alpha + beta * x_z
    y_obs = pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y_z)

    idata = pm.sample(
        draws=2000,
        tune=2000,
        chains=4,
        target_accept=0.9,
        random_seed=42,
    )

az.summary(idata, var_names=["alpha", "beta", "sigma"])
```

Điều đáng chú ý là từng khối code đều ánh xạ thẳng sang câu chuyện thống kê:

- `alpha`, `beta`, `sigma` là ba prior cho ba tham số cốt lõi,
- `mu = alpha + beta * x_z` là đường trung bình của hồi quy,
- `y_obs = pm.Normal(...)` là likelihood, tức cách dữ liệu được sinh ra quanh đường trung bình đó,
- `pm.sample(...)` là bước lấy mẫu từ posterior thay vì tìm một ước lượng điểm duy nhất.

Nếu bạn còn giữ được mối liên hệ một-một giữa mô hình trên giấy và đoạn code này, bạn đang đi đúng hướng.

## 4. Vì sao nên chuẩn hóa dữ liệu trước khi fit?

Regression Bayes thường chạy ổn hơn khi biến được scale tốt.

Lợi ích của việc chuẩn hóa là prior dễ chọn hơn, intercept dễ diễn giải hơn, sampler thường hội tụ ổn hơn, và posterior cũng ít bị “méo vì đơn vị đo” hơn.

Vì vậy, trong rất nhiều trường hợp, chuẩn hóa là một bước thực hành nên có.

## 5. Sau khi chạy mẫu, ta đọc gì đầu tiên?

Nhiều người mới học hay nhảy thẳng vào posterior mean và interval. Nhưng thứ nên nhìn đầu tiên thực ra là diagnostics, nghĩa là trace plot (đồ thị vệt mẫu) có ổn không, R-hat có gần 1 không, ESS (số mẫu hiệu dụng) có đủ không, và sampler có phát ra warning (cảnh báo) gì không.

Nếu phần này chưa tốt, mọi diễn giải posterior sau đó đều nên được xem là tạm thời.

## 6. Diễn giải posterior trong regression

Khi model chạy ổn, ta mới quay lại các câu hỏi thống kê.

### 6.1. Intercept

Với dữ liệu đã standardize (chuẩn hóa) hoặc centered (đưa về quanh trung tâm), intercept thường dễ đọc hơn vì nó mô tả giá trị trung bình của $$y$$ khi $$x$$ ở mức trung tâm.

### 6.2. Slope

Posterior của slope cho biết mối quan hệ đang dương hay âm, mạnh hay yếu, và ta chắc đến đâu về điều đó. Điểm hay của Bayes là bạn có thể hỏi trực tiếp xác suất $$\beta > 0$$ là bao nhiêu.

### 6.3. Noise

Posterior của $$\sigma$$ cho biết mức độ dữ liệu phân tán quanh đường hồi quy, tức là model còn bỏ lại bao nhiêu biến thiên chưa giải thích.

### 6.4. Ví dụ Session 7: cập nhật từ prior sang posterior cho tham số hồi quy

Giả sử sau khi fit mô hình tuyến tính một biến với PyMC, ta thu được tóm tắt sau:

- Prior: $$\alpha\sim\mathcal N(60,20),\;\beta\sim\mathcal N(0,2),\;\sigma\sim\text{HalfNormal}(5)$$.
- Posterior summary:
  - $$\alpha\mid D\approx \mathcal N(63.2,\,1.1^2)$$
  - $$\beta\mid D\approx \mathcal N(0.78,\,0.09^2)$$
  - $$\sigma\mid D$$ có trung bình hậu nghiệm khoảng $$2.4$$.

Diễn giải nhanh theo tinh thần Buổi 7:

- dữ liệu đã kéo intercept từ vùng prior quanh 60 lên khoảng 63.2,
- slope dương rõ rệt với bất định nhỏ (SD 0.09),
- độ nhiễu còn lại khoảng 2.4 đơn vị phản hồi.

Nếu cần khoảng hậu nghiệm gần 95% cho slope (xấp xỉ Normal):

$$
0.78\pm 1.96\times 0.09\Rightarrow [0.604,\;0.956].
$$

Khoảng này không cắt 0, nên bằng chứng hậu nghiệm ủng hộ quan hệ dương khá rõ.

## 7. Từ posterior tham số tới dự đoán

Regression Bayes không chỉ để biết slope là bao nhiêu. Nó còn để dự đoán. Chẳng hạn, với một giá trị $$x$$ mới, ta muốn biết cân nặng hoặc điểm thi dự đoán sẽ ở đâu, và khoảng bất định đi kèm với dự đoán đó rộng đến mức nào.

Đây là nơi PyMC rất tiện, vì sau khi đã có posterior draws (các mẫu rút ra từ posterior), ta có thể chuyển thẳng sang posterior predictive (dự báo hậu nghiệm) tương đối tự nhiên.

### 7.1. Một ví dụ cụ thể: dự đoán cho người cao 175 cm

Với model ở trên, giả sử bạn muốn dự đoán cho một người cao 175 cm. Ta có thể lấy trực tiếp posterior draws rồi lan truyền chúng sang dự đoán:

```python
posterior = az.extract(idata, group="posterior")

alpha_draws = posterior["alpha"].values
beta_draws = posterior["beta"].values
sigma_draws = posterior["sigma"].values

x_new_z = (175 - height.mean()) / height.std()

mu_new_z = alpha_draws + beta_draws * x_new_z
y_new_z = np.random.default_rng(42).normal(mu_new_z, sigma_draws)

mu_new = mu_new_z * weight.std() + weight.mean()
y_new = y_new_z * weight.std() + weight.mean()
```

Hai đối tượng ở đây phục vụ hai câu hỏi khác nhau:

- `mu_new` là phân phối cho **giá trị trung bình dự đoán**, tức trung bình cân nặng của nhóm người cao 175 cm theo mô hình.
- `y_new` là phân phối cho **một quan sát mới**, tức cân nặng của một cá nhân cụ thể cao 175 cm.

Giả sử sau khi tóm tắt các mẫu này, bạn thấy:

- trung bình của `mu_new` vào khoảng 71 kg với khoảng 89% khoảng từ 69 đến 73 kg,
- còn `y_new` có khoảng dự đoán 89% rộng hơn, chẳng hạn từ 63 đến 79 kg.

Lúc đó bạn nên đọc kết quả theo đúng ngôn ngữ Bayes:

- mô hình khá chắc về **xu hướng trung bình** ở vùng chiều cao 175 cm,
- nhưng vẫn thành thật rằng **một cá nhân mới** có thể lệch khỏi trung bình khá nhiều.

Đây chính là nơi posterior inference chuyển thành prediction một cách rất tự nhiên: ta không đổi mô hình, chỉ tiếp tục kể câu chuyện sinh dữ liệu thêm một bước nữa.

## 8. Một workflow tối thiểu lành mạnh khi dùng PyMC cho regression

Bạn có thể ghi nhớ workflow (quy trình) này như ba chặng nối tiếp nhau, trong đó mỗi chặng đều có một câu hỏi trung tâm cần được trả lời rõ ràng trước khi sang bước kế tiếp:

### Trước khi chạy

Trước khi chạy, hãy hỏi biến có cần chuẩn hóa không, prior có hợp lý theo đúng thang đo dữ liệu không, và generative story đã thật sự rõ chưa.

### Trong khi chạy

Trong khi chạy, hãy để ý sampler có cảnh báo gì không và giai đoạn warm-up (làm nóng) có đủ hay chưa.

### Sau khi chạy

Sau khi chạy, hãy xem trace plot có ổn không, R-hat và ESS có tốt không, posterior của tham số đang nói gì, và posterior predictive có hợp lý hay không.

### Ghi chú cho bối cảnh biết/không biết phương sai

Trong thực hành PyMC, ta thường suy luận cả $$\sigma$$ nên interval của slope đã phản ánh bất định về nhiễu. Nếu bạn cố định $$\sigma$$ từ trước (bài toán đặc thù), interval cho slope thường hẹp hơn. Khi báo cáo kết quả, nên nêu rõ bạn đang ở kịch bản nào.

## 9. Những lỗi phổ biến của người mới dùng PyMC cho regression

### 9.1. Xem PyMC như hộp đen

Đây là lỗi lớn nhất.

Nếu không hiểu mô hình, bạn sẽ không biết prior đang nói gì, warning đang báo điều gì, và posterior có thật sự đáng tin hay không.

### 9.2. Chỉ đọc posterior mean

Posterior mean là chưa đủ. Bạn cần xem interval (khoảng bất định), xác suất vượt ngưỡng, hình dạng posterior, và cả prediction uncertainty (bất định dự đoán).

### 9.3. Quên model checking

Regression fit xong chưa phải là xong. Bài sau sẽ nhấn mạnh posterior predictive checks (kiểm tra dự báo hậu nghiệm), residual analysis (phân tích phần dư), và prediction quality (chất lượng dự đoán).

## 10. Điều bài này muốn bạn giữ lại

Mục tiêu không phải là nhớ từng dòng API PyMC. Mục tiêu là nhìn thấy regression Bayes có thể được triển khai rất tự nhiên miễn là bạn giữ đúng workflow tư duy. PyMC chỉ là công cụ; phần quan trọng nhất vẫn là câu chuyện mô hình, prior, diagnostics, và cách diễn giải posterior.

> **3 ý cần nhớ.** PyMC giúp triển khai regression Bayes theo đúng cấu trúc prior + likelihood + posterior mà bạn đã học; sau khi fit model, diagnostics luôn phải đi trước việc diễn giải posterior; và giá trị thật của posterior inference không chỉ nằm ở ước lượng tham số mà còn ở khả năng chuyển sang dự đoán và kiểm tra mô hình.

## Câu hỏi tự luyện

1. Hãy liệt kê 5 bước tối thiểu của một workflow regression Bayes với PyMC.
2. Vì sao chuẩn hóa dữ liệu thường giúp cả prior selection lẫn sampling?
3. Nếu posterior của slope trông hợp lý nhưng R-hat chưa tốt, bạn nên làm gì?
4. Trong regression Bayes, tại sao prediction là phần quan trọng không kém estimation?

## Tài liệu tham khảo

- PyMC Documentation.
- ArviZ Documentation.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 4-5.

---

*Bài học tiếp theo: [4.4 Model Checking và Prediction - Đảm bảo Model Tốt](/vi/chapter04/model-checking-prediction/)*
