---
layout: post
title: "Bài 4.3: Posterior Inference với PyMC - Từ Theory đến Practice"
chapter: '04'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

Trước khi các ngôn ngữ lập trình xác suất (Probabilistic Programming Languages — PPL) như Stan và PyMC ra đời, việc triển khai một mô hình Bayes phi liên hợp đồng nghĩa với việc tự viết hàng trăm dòng mã tính hàm log-hợp lý, tự đạo hàm bằng tay và tự chỉnh bước nhảy Metropolis. Ngày nay, bạn chỉ cần viết đúng bốn dòng mô tả quá trình sinh dữ liệu — và phần mềm sẽ tự động biên dịch đồ thị tính toán, lấy đạo hàm chính xác và chạy NUTS song song nhiều chuỗi. Hiểu những gì diễn ra bên dưới bốn dòng mã đó là ranh giới giữa người *gõ lệnh* và người *làm thống kê Bayes*.

## Mục tiêu học tập

Sau bài này, bạn sẽ biết cách chuyển một mô hình hồi quy tuyến tính Bayes từ công thức trên giấy thành mã nguồn chạy được trong PyMC. Bạn cũng sẽ nắm được quy trình thực hành chuẩn: chuẩn hóa dữ liệu, khai báo phân phối tiên nghiệm và hàm hợp lý, lấy mẫu phân phối hậu nghiệm bằng MCMC, kiểm tra các chỉ số chẩn đoán và diễn giải kết quả.

> **Ví dụ ngắn.** Sau khi đã xác định quá trình sinh dữ liệu và chọn phân phối tiên nghiệm hợp lý, bước tiếp theo là triển khai mô hình trong PyMC để suy luận phân phối hậu nghiệm cho hệ số chặn, hệ số dốc và độ nhiễu. PyMC không thay bạn tư duy về mô hình, mà giúp thực thi tính toán một cách nhất quán và hiệu quả.
>
> **Câu hỏi tự kiểm tra.** Khi PyMC đã chạy xong và trả về mẫu hậu nghiệm, vì sao ta vẫn phải kiểm tra các chỉ số chẩn đoán trước khi diễn giải kết quả?


## Kiến thức cần nhớ: Lập trình xác suất, Vi phân tự động và Sai số Monte Carlo

Bài học này nối liền lý thuyết xác suất trên giấy với thực hành tính toán hiện đại qua ba trụ cột:

- **Đồ thị xác suất và Ngôn ngữ lập trình xác suất (PPL):** Mỗi khối `with pm.Model()` thực chất đang xây dựng một đồ thị có hướng không chu trình (DAG) biểu diễn phân phối đồng thời $$p(y, \theta) = p(y \mid \theta)p(\theta)$$. Tách bạch *đặc tả mô hình* khỏi *thuật toán suy luận* giúp bạn thay đổi giả định phân phối chỉ bằng một dòng lệnh mà không phải viết lại bộ lấy mẫu.
- **Vi phân tự động (Reverse-mode Automatic Differentiation):** Bộ lấy mẫu NUTS cần gradient $$\nabla_\theta \log p(\theta \mid y)$$ tại mỗi bước leapfrog. PyMC (thông qua PyTensor) tính đạo hàm này chính xác đến sai số dấu phẩy động bằng quy tắc dây chuyền trên đồ thị tính toán, thay vì xấp xỉ sai phân hữu hạn.
- **Sai số chuẩn Monte Carlo (MCSE) và biến đổi thang đo:** Vì MCMC trả về tập mẫu hữu hạn có tự tương quan, trung bình mẫu luôn mang sai số mô phỏng $$\text{MCSE} = \mathrm{SD}(\theta \mid D)/\sqrt{\text{ESS}}$$. Hiểu MCSE giúp bạn biết chính xác bao nhiêu mẫu là đủ thay vì đoán mò số `draws`.
## 1. Từ mô hình trên giấy sang mã nguồn

Ở hai bài 4.1 và 4.2, ta đã nắm được ba nền tảng: quá trình sinh dữ liệu, cách chọn phân phối tiên nghiệm và trực giác về hồi quy Bayes. Bài này tập trung vào bước triển khai thực hành: dịch mô hình thống kê thành mã nguồn PyMC theo một quy trình rõ ràng — chuẩn bị và chuẩn hóa dữ liệu, khai báo tiên nghiệm, khai báo hàm hợp lý, chạy bộ lấy mẫu, kiểm tra chẩn đoán rồi mới diễn giải phân phối hậu nghiệm.

## 2. Vì sao cần MCMC? Khi công thức dạng đóng không còn tồn tại

### 2.1. Từ mô hình liên hợp sang mô hình không liên hợp

Ở Chương 2, ta đã làm quen với các **phân phối tiên nghiệm liên hợp (conjugate priors)**:

- **Beta–Binomial:** tiên nghiệm Beta + hàm hợp lý Binomial $$\to$$ hậu nghiệm Beta.
- **Gamma–Poisson:** tiên nghiệm Gamma + hàm hợp lý Poisson $$\to$$ hậu nghiệm Gamma.
- **Normal–Normal:** tiên nghiệm Normal + hàm hợp lý Normal $$\to$$ hậu nghiệm Normal.

Với những cặp liên hợp này, phân phối hậu nghiệm có **công thức dạng đóng (closed-form)**, ví dụ:

$$
\theta \mid D \sim \text{Beta}(\alpha_0 + k, \beta_0 + n - k)
$$

Ta chỉ cần thay số trực tiếp vào công thức mà không cần mô phỏng hay lấy mẫu.

### 2.2. Hồi quy Bayes không còn công thức giải tích đơn giản

Xét một mô hình hồi quy tuyến tính Bayes tiêu chuẩn:

$$
\begin{aligned}
\beta_0 &\sim \mathcal{N}(5, 5) \\
\beta_1 &\sim \mathcal{N}(2, 5) \\
\sigma &\sim \text{HalfNormal}(2) \\
y_i &\sim \mathcal{N}(\beta_0 + \beta_1 x_i, \sigma^2)
\end{aligned}
$$

Trong mô hình này:

- Ba tham số ($$\beta_0, \beta_1, \sigma$$) phải được cập nhật đồng thời.
- Tổ hợp tiên nghiệm Normal và HalfNormal không liên hợp với hàm hợp lý.
- Phân phối hậu nghiệm đồng thời 3 chiều không có công thức dạng đóng:

$$
p(\beta_0, \beta_1, \sigma \mid D) = \frac{p(D \mid \beta_0, \beta_1, \sigma) \cdot p(\beta_0) \cdot p(\beta_1) \cdot p(\sigma)}{p(D)}
$$

với hằng số chuẩn hóa là tích phân 3 chiều:

$$
p(D) = \iiint p(D \mid \beta_0, \beta_1, \sigma) \cdot p(\beta_0) \cdot p(\beta_1) \cdot p(\sigma) \, d\beta_0 \, d\beta_1 \, d\sigma.
$$

Tích phân này không thể tính bằng công thức giải tích thông thường.

### 2.3. MCMC: lấy mẫu thay vì tính tích phân trực tiếp

Khi không có công thức dạng đóng, ta sử dụng **MCMC (Markov Chain Monte Carlo)** để rút mẫu trực tiếp từ phân phối hậu nghiệm.

> **Ý tưởng cốt lõi:** Thay vì giải tích phân nhiều chiều, ta rút một tập mẫu đại diện từ phân phối hậu nghiệm — tương tự như khảo sát một mẫu đại diện gồm vài nghìn người thay vì hỏi toàn bộ hàng triệu dân.

Quy trình MCMC gồm bốn bước:

1. Khởi tạo tại một điểm trong không gian tham số.
2. Dịch chuyển sang điểm mới theo quy tắc xác suất ưu tiên vùng mật độ hậu nghiệm cao.
3. Lặp lại hàng nghìn lần để tạo thành chuỗi mẫu.
4. Dùng tập mẫu thu được để xấp xỉ phân phối hậu nghiệm.

**Ví dụ minh họa trong PyMC:**

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

**Mẫu kết quả thu được từ MCMC:**

| Mẫu | $$\beta_0$$ | $$\beta_1$$ | $$\sigma$$ |
|---|---:|---:|---:|
| 1 | 6.8 | 2.1 | 0.6 |
| 2 | 6.5 | 2.2 | 0.5 |
| ... | ... | ... | ... |
| 2000 | 6.9 | 2.0 | 0.7 |

Từ 2000 bộ mẫu này, ta dễ dàng tính các đại lượng suy luận:

- **Trung bình hậu nghiệm:** trung bình cộng của các mẫu.
- **Khoảng tin cậy hậu nghiệm 95%:** lấy phân vị 2.5% và 97.5% của tập mẫu.
- **Xác suất $$\beta_1 > 0$$:** tỷ lệ số mẫu có giá trị $$\beta_1 > 0$$.

### 2.4. So sánh phương pháp liên hợp và MCMC

| Tiêu chí | Tiên nghiệm liên hợp | MCMC (Hồi quy) |
|---|---|---|
| **Tiên nghiệm** | Beta, Gamma, Normal đơn giản | Linh hoạt cho nhiều phân phối khác nhau |
| **Hàm hợp lý** | Binomial, Poisson, Normal tương thích | Normal hoặc các mô hình nhiều tham số |
| **Hậu nghiệm** | Có công thức dạng đóng | Không có công thức dạng đóng |
| **Cách tính** | Thay số trực tiếp vào công thức | Lấy mẫu mô phỏng bằng MCMC |
| **Bản chất kết quả** | Phân phối giải tích chính xác | Xấp xỉ số hội tụ về phân phối đúng |
| **Ví dụ** | Beta(17, 103) | 2000 bộ mẫu ($$\beta_0, \beta_1, \sigma$$) |
| **Thời gian chạy** | Dưới 1 giây | Vài giây đến vài chục giây |
| **Độ chính xác** | Chính xác giải tích (100%) | Sai số Monte Carlo rất nhỏ khi đủ mẫu |

### 2.5. PyMC tự động hóa phần tính toán của MCMC

Một ưu điểm thực tế của PyMC là bạn không cần tự lập trình lại các thuật toán như Metropolis–Hastings, Gibbs sampling, HMC hay NUTS. Thay vào đó, bạn chỉ cần tập trung vào bốn việc: khai báo mô hình (tiên nghiệm và hàm hợp lý), gọi `pm.sample()`, kiểm tra các chỉ số chẩn đoán ($$\hat{R}$$, ESS) và diễn giải kết quả. PyMC sẽ tự động chọn bộ lấy mẫu phù hợp (thường là NUTS), điều chỉnh tham số trong giai đoạn làm nóng (warm-up), chạy song song nhiều chuỗi và cảnh báo nếu phát hiện vấn đề hội tụ.

### 2.6. Khi nào dùng công thức dạng đóng, khi nào dùng MCMC?

| Tình huống | Phương pháp phù hợp |
|---|---|
| Mô hình liên hợp, ít tham số | Công thức dạng đóng |
| Mô hình không liên hợp hoặc nhiều tham số | MCMC |
| Hồi quy từ 3 tham số trở lên | MCMC (PyMC) |
| Mô hình phân cấp (Hierarchical models) | MCMC |
| Mô hình hỗn hợp (Mixture models) | MCMC |

> **Nguyên tắc thực hành:** Khi phân phối hậu nghiệm không thể tính gọn bằng công thức dạng đóng, hãy sử dụng MCMC.

## 3. Cấu trúc một mô hình hồi quy Bayes tối giản trong PyMC

Khi viết mã trong PyMC, hãy bám sát thứ tự của mô hình thống kê: khai báo tiên nghiệm cho $$\alpha$$, $$\beta$$, $$\sigma$$, rồi khai báo hàm hợp lý:

$$
y_i \sim \mathcal{N}(\alpha + \beta x_i,\sigma).
$$

Mã nguồn cần phản ánh đúng cấu trúc của mô hình toán học, thay vì thay đổi mô hình chỉ để chiều theo cú pháp thư viện.

### 3.1. Ví dụ tối giản chạy được bằng PyMC

Xét một tập dữ liệu nhỏ về chiều cao và cân nặng:

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

Từng khối lệnh trong đoạn mã ánh xạ trực tiếp sang mô hình thống kê:

- `alpha`, `beta`, `sigma` là phân phối tiên nghiệm của ba tham số cốt lõi.
- `mu = alpha + beta * x_z` biểu diễn xu hướng trung bình tuyến tính.
- `y_obs = pm.Normal(...)` là hàm hợp lý mô tả cách dữ liệu dao động quanh đường trung bình.
- `pm.sample(...)` thực hiện lấy mẫu từ phân phối hậu nghiệm thay vì tìm một ước lượng điểm duy nhất.

Giữ được sự tương ứng một-một giữa công thức trên giấy và mã nguồn là dấu hiệu cho thấy bạn đang triển khai mô hình đúng hướng.

## 4. Vì sao nên chuẩn hóa dữ liệu trước khi lấy mẫu?

Chuẩn hóa biến trước khi chạy hồi quy Bayes mang lại bốn lợi ích đồng thời: phân phối tiên nghiệm dễ chọn hơn, hệ số chặn dễ diễn giải hơn, bộ lấy mẫu hội tụ ổn định hơn và phân phối hậu nghiệm ít bị méo do sự chênh lệch đơn vị đo giữa các biến. Vì vậy, chuẩn hóa thường là bước tiền xử lý nên thực hiện trong thực hành.

## 5. Sau khi lấy mẫu, cần đọc gì đầu tiên?

Người mới thường xem ngay trung bình hậu nghiệm và khoảng tin cậy, nhưng thứ cần kiểm tra đầu tiên phải là các **chỉ số chẩn đoán (diagnostics)**: đồ thị vệt mẫu (trace plot) có trộn đều không, $$\hat{R}$$ có gần 1 không, số mẫu hiệu dụng (ESS) có đủ lớn không, và bộ lấy mẫu có phát sinh cảnh báo (như divergence) hay không. Nếu các chỉ số này chưa đạt, mọi diễn giải thống kê phía sau chỉ nên xem là tạm thời.

## 6. Diễn giải phân phối hậu nghiệm trong hồi quy

Khi quá trình lấy mẫu đã đạt yêu cầu chẩn đoán, ta bắt đầu diễn giải từng tham số:

- **Hệ số chặn $$\alpha$$:** với dữ liệu đã chuẩn hóa hoặc dịch tâm, $$\alpha$$ biểu thị giá trị trung bình của $$y$$ tại mức trung tâm của $$x$$.
- **Hệ số dốc $$\beta$$:** phân phối hậu nghiệm của $$\beta$$ cho biết chiều hướng (dương hay âm), độ lớn và mức độ bất định của mối quan hệ; đồng thời cho phép tính trực tiếp các xác suất như $$P(\beta > 0 \mid D)$$.
- **Độ nhiễu $$\sigma$$:** cho biết mức độ phân tán của dữ liệu quanh đường hồi quy, phản ánh phần biến thiên mà mô hình chưa giải thích được.

### 6.1. Ví dụ: cập nhật từ tiên nghiệm sang hậu nghiệm

Giả sử sau khi khớp một mô hình hồi quy tuyến tính một biến bằng PyMC, ta thu được các kết quả sau:

- **Tiên nghiệm:** $$\alpha\sim\mathcal N(60,20),\;\beta\sim\mathcal N(0,2),\;\sigma\sim\text{HalfNormal}(5)$$.
- **Tóm tắt hậu nghiệm:**
  - $$\alpha\mid D\approx \mathcal N(63.2,\,1.1^2)$$
  - $$\beta\mid D\approx \mathcal N(0.78,\,0.09^2)$$
  - $$\sigma\mid D$$ có trung bình hậu nghiệm khoảng $$2.4$$.

Từ kết quả trên, có thể rút ra ba nhận xét: dữ liệu đã kéo hệ số chặn từ vùng tiên nghiệm quanh 60 lên khoảng 63.2; hệ số dốc dương rõ rệt với độ lệch chuẩn nhỏ (0.09); và độ nhiễu còn lại quanh đường hồi quy khoảng 2.4 đơn vị của biến phản hồi.

Nếu tính khoảng hậu nghiệm xấp xỉ 95% cho hệ số dốc theo phân phối Chuẩn:

$$
0.78\pm 1.96\times 0.09\Rightarrow [0.604,\;0.956].
$$

Khoảng này nằm hoàn toàn phía trên 0, cho thấy bằng chứng hậu nghiệm ủng hộ rõ rệt mối quan hệ dương.

### Giải thích: Kiểm tra độ chính xác MCSE và quy đổi ngược hệ số về thang đo gốc

Sau khi PyMC in ra bảng `az.summary`, hai phép tính tay ngắn gọn sau sẽ giúp bạn kiểm soát hoàn toàn chất lượng và ý nghĩa thực tế của kết quả:

1. **Đo sai số mô phỏng bằng MCSE:** Trong ví dụ ở mục 6.1, giả sử hậu nghiệm của hệ số dốc có trung bình $$\bar\beta = 0.78$$, độ lệch chuẩn $$\mathrm{SD} = 0.09$$ và số mẫu hiệu dụng $$\text{ESS} = 900$$. Sai số chuẩn Monte Carlo của ước lượng trung bình là:
   $$\text{MCSE} = \frac{\mathrm{SD}}{\sqrt{\text{ESS}}} = \frac{0.09}{\sqrt{900}} = \frac{0.09}{30} = 0.003.$$
   Con số $$0.003$$ nhỏ hơn 30 lần so với độ bất định thống kê thật ($$0.09$$), nghĩa là chữ số thập phân thứ hai của $$0.78$$ đã rất ổn định. Ngược lại, nếu $$\text{ESS} = 25$$ thì $$\text{MCSE} = 0.09/5 = 0.018$$ (chiếm tới 20% độ lệch chuẩn) — khi đó bạn cần chạy thêm mẫu hoặc kiểm tra lại mô hình.
2. **Quy đổi ngược hệ số từ thang chuẩn hóa về thang gốc:** Với 8 điểm dữ liệu chiều cao–cân nặng ở mục 3.1, ta có $$\bar x = 167.5\text{ cm},\ s_x \approx 11.46\text{ cm}$$ và $$\bar y = 64.625\text{ kg},\ s_y \approx 10.56\text{ kg}$$. Nếu một mẫu hậu nghiệm trên thang chuẩn hóa là $$(\alpha_z, \beta_z, \sigma_z) = (0.00,\ 0.98,\ 0.15)$$, thì trên thang đo gốc:
   - Hệ số dốc: $$\beta_{\text{gốc}} = \beta_z \cdot \frac{s_y}{s_x} = 0.98 \times \frac{10.56}{11.46} \approx 0.903\text{ kg/cm}$$.
   - Độ nhiễu: $$\sigma_{\text{gốc}} = \sigma_z \cdot s_y = 0.15 \times 10.56 \approx 1.58\text{ kg}$$.
   - Hệ số chặn tại mốc chiều cao trung bình $$167.5\text{ cm}$$ là $$\bar y + \alpha_z s_y = 64.625\text{ kg}$$ (có ý nghĩa thực tế trực tiếp, thay vì tại $$0\text{ cm}$$).

Luôn quy đổi từng mẫu hậu nghiệm trước rồi mới lấy trung bình và khoảng tin cậy HDI trên thang gốc để giữ trọn vẹn cấu trúc bất định.

## 7. Chuyển từ suy luận tham số sang dự đoán

Hồi quy Bayes không dừng lại ở việc ước lượng hệ số dốc, mà còn cung cấp dự đoán kèm mức độ bất định cho các quan sát mới. Khi đã có các mẫu rút từ phân phối hậu nghiệm (posterior draws), việc tính phân phối dự báo hậu nghiệm (posterior predictive) trong PyMC diễn ra rất trực tiếp.

### 7.1. Ví dụ minh họa: dự đoán cân nặng cho người cao 175 cm

Với mô hình ở mục 3.1, ta rút các mẫu hậu nghiệm và lan truyền bất định sang dự đoán tại chiều cao 175 cm:

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

Hai biến thu được trả lời hai câu hỏi khác nhau:

- `mu_new` biểu diễn phân phối cho **giá trị trung bình dự đoán** của nhóm người cao 175 cm.
- `y_new` biểu diễn phân phối cho **một quan sát mới** — tức cân nặng của một cá nhân cụ thể cao 175 cm.

Giả sử sau khi tóm tắt mẫu, trung bình của `mu_new` vào khoảng 71 kg với khoảng 89% từ 69 đến 73 kg, còn `y_new` có khoảng dự đoán 89% rộng hơn, từ 63 đến 79 kg. Kết quả này phản ánh đúng tinh thần Bayes: mô hình khá chắc chắn về xu hướng trung bình tại chiều cao 175 cm, nhưng vẫn ghi nhận đầy đủ độ phân tán khi dự đoán cho một cá nhân riêng lẻ.

## 8. Quy trình thực hành tối thiểu với PyMC

Bạn có thể tổ chức quy trình làm việc thành ba giai đoạn nối tiếp nhau:

- **Trước khi chạy:** kiểm tra xem biến có cần chuẩn hóa không, phân phối tiên nghiệm có hợp lý theo thang đo dữ liệu không và quá trình sinh dữ liệu đã được viết rõ ràng chưa.
- **Trong khi chạy:** theo dõi xem bộ lấy mẫu có phát sinh cảnh báo hay không và giai đoạn khởi động (warm-up) đã đủ dài chưa.
- **Sau khi chạy:** kiểm tra trace plot, $$\hat{R}$$ và ESS trước; sau đó mới diễn giải phân phối hậu nghiệm của tham số và kiểm tra phân phối dự báo hậu nghiệm.

### Ghi chú về bối cảnh biết trước và chưa biết phương sai nhiễu

Trong thực hành với PyMC, ta thường suy luận đồng thời $$\sigma$$, nên khoảng tin cậy hậu nghiệm của hệ số dốc đã tự động phản ánh bất định về nhiễu. Nếu cố định trước $$\sigma$$ trong một bài toán đặc thù, khoảng ước lượng của hệ số dốc sẽ hẹp hơn. Do đó, khi báo cáo kết quả, cần nêu rõ $$\sigma$$ được ước lượng hay được cố định.

## 9. Những lỗi thường gặp khi mới dùng PyMC

- **Xem PyMC như hộp đen:** nếu không nắm vững mô hình thống kê phía sau, bạn sẽ khó đánh giá ý nghĩa của tiên nghiệm, không hiểu cảnh báo của bộ lấy mẫu và khó nhận ra khi nào kết quả hậu nghiệm không đáng tin cậy.
- **Chỉ báo cáo trung bình hậu nghiệm:** một con số trung bình không đủ để truyền đạt kết quả Bayes; cần trình bày thêm khoảng bất định, xác suất vượt ngưỡng, hình dạng phân phối và bất định dự đoán.
- **Bỏ qua bước kiểm tra mô hình:** khớp xong mô hình mới là một nửa công việc. Bài tiếp theo sẽ trình bày chi tiết về kiểm tra dự báo hậu nghiệm, phân tích phần dư và đánh giá chất lượng dự đoán.

## 10. Tổng kết bài học

Mục tiêu của bài này không phải là ghi nhớ thuộc lòng từng hàm của PyMC, mà là thấy được sự liền mạch giữa tư duy mô hình hóa và mã nguồn triển khai. PyMC chỉ là công cụ tính toán; phần quyết định chất lượng phân tích vẫn nằm ở cấu trúc mô hình, phân phối tiên nghiệm, chẩn đoán hội tụ và cách diễn giải kết quả.

> **3 ý cần nhớ.** PyMC cho phép triển khai hồi quy Bayes theo đúng cấu trúc tiên nghiệm + hàm hợp lý + hậu nghiệm; sau khi lấy mẫu, chẩn đoán hội tụ luôn phải được kiểm tra trước khi diễn giải tham số; và giá trị đầy đủ của suy luận hậu nghiệm nằm ở cả việc ước lượng tham số lẫn tạo dự đoán có kèm bất định.

## Video tham khảo

- [[114] Getting Started with PyMC (Chris Fonnesbeck)](https://www.youtube.com/watch?v=jrU0UBr2z3k) — Data Umbrella, English. **xem trước**. Hướng dẫn khai báo mô hình và lấy mẫu trong PyMC, khớp với bước chuyển từ mô hình trên giấy sang mã nguồn trong bài.
- [L4: Interpretable Linear Regressions (State of Bayes Lecture Series)](https://www.youtube.com/watch?v=fpS0NjqNHn8) — PyMC Labs, English. Trình bày hồi quy tuyến tính trong PyMC và cách diễn giải hệ số, bổ trợ cho quy trình chuẩn hóa, tiên nghiệm và hàm hợp lý.
- [Chris Fonnesbeck - Probabilistic Python: An Introduction to Bayesian Modeling with PyMC](https://www.youtube.com/watch?v=911d4A1U0BE) — PyData, English. Bài giới thiệu đầy đủ hơn về mô hình hóa Bayes với PyMC, bao gồm cả đặt tiên nghiệm và kiểm tra sau lấy mẫu.

## Câu hỏi tự luyện

1. Hãy liệt kê 5 bước tối thiểu trong một quy trình hồi quy Bayes với PyMC.
2. Vì sao chuẩn hóa dữ liệu hỗ trợ đồng thời cho cả việc chọn phân phối tiên nghiệm lẫn quá trình lấy mẫu?
3. Nếu phân phối hậu nghiệm của hệ số dốc trông hợp lý nhưng chỉ số $$\hat{R}$$ chưa đạt yêu cầu, bạn cần xử lý thế nào?
4. Trong hồi quy Bayes, vì sao bước dự đoán có vai trò quan trọng không kém bước ước lượng tham số?

## Tài liệu tham khảo

- PyMC Documentation.
- ArviZ Documentation.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 4-5.

---

*Bài học tiếp theo: [4.4 Model Checking và Prediction - Đảm bảo Model Tốt]({{ site.baseurl }}/contents/vi/chapter04/04_04_model_checking_prediction/)*
