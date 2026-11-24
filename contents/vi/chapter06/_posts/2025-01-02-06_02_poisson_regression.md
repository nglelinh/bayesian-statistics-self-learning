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

Năm 1898, nhà thống kê Ladislaus Bortkiewicz công bố một nghiên cứu kỳ lạ nhưng kinh điển: đếm số binh sĩ Phổ tử vong vì bị ngựa đá trong từng quân đoàn suốt 20 năm. Các con số thu được — toàn số nguyên không âm $$0, 1, 2, 3, 4$$ — khớp khít một cách đáng kinh ngạc với phân phối do Siméon Denis Poisson tìm ra trước đó nửa thế kỷ. Ngày nay, cùng cấu trúc dữ liệu đếm ấy xuất hiện khắp nơi: số ca cấp cứu mỗi ngày, số lỗi phần mềm trên mỗi nghìn dòng mã, hay số đơn hàng đặt mỗi giờ.

Bài học này mở rộng khung GLM sang **hồi quy Poisson Bayes** với hàm liên kết logarit, đồng thời chỉ ra cách chẩn đoán và khắc phục hiện tượng **quá phân tán (overdispersion)** bằng phân phối Negative Binomial.

---

## Mục tiêu học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **hồi quy Poisson (Poisson regression)** như mô hình tiêu chuẩn cho **dữ liệu đếm (count data)**, tức các dữ liệu ghi nhận số lần một sự kiện xảy ra. Bạn sẽ thấy vì sao hồi quy tuyến tính không phù hợp khi biến kết quả chỉ nhận các số nguyên không âm, vì sao **hàm liên kết log (log link function)** giúp mô hình tạo ra dự đoán hợp lệ, và vì sao hệ số của mô hình nên được diễn giải thông qua **tỷ số tốc độ (rate ratio)** thay vì hiệu số cộng đơn giản. Đây là mô hình GLM quan trọng thứ hai sau hồi quy logistic.


## Bản đồ kiến thức nền: Hàm liên kết Log, Exposure Offset và Bài toán Quá phân tán

Làm chủ hồi quy dữ liệu đếm đòi hỏi nắm vững ba trụ cột:

- **Hàm liên kết Log & Tỷ số tốc độ (Rate Ratio):** Trong hồi quy Poisson, $$y_i \sim \text{Poisson}(\lambda_i)$$ với $$\log \lambda_i = \alpha + \beta x_i \iff \lambda_i = e^{\alpha + \beta x_i}$$. Hàm mũ bảo đảm tốc độ kỳ vọng $$\lambda_i$$ luôn dương, và tăng $$x$$ thêm 1 đơn vị sẽ **nhân** số đếm kỳ vọng với $$e^\beta$$ (*Incidence Rate Ratio — IRR*).
- **Biến bù phơi nhiễm (Exposure Offset):** Khi các quan sát có thời gian theo dõi hoặc quy mô khác nhau (ví dụ $$t_i$$ ngày hay $$E_i$$ nghìn người), ta mô hình hóa tốc độ trên một đơn vị phơi nhiễm: $$\log \lambda_i = \log(t_i) + \alpha + \beta x_i$$ (hệ số của $$\log(t_i)$$ cố định bằng 1).
- **Quá phân tán (Overdispersion) & Negative Binomial:** Phân phối Poisson ép chặt $$\mathrm{Var}(y_i) = \mathbb{E}[y_i] = \lambda_i$$. Dữ liệu thực tế thường có phương sai lớn hơn trung bình rất nhiều; nếu giữ nguyên Poisson, khoảng tin cậy hậu nghiệm sẽ hẹp giả tạo. Chuyển sang **Negative Binomial** ($$\mathrm{Var}(y) = \mu + \mu^2/\phi$$) giải quyết triệt để vấn đề này.

---

## Giới thiệu: Dữ liệu đếm trong thực tế

**Dữ liệu đếm (count data)** xuất hiện trong nhiều bối cảnh thực tế, chẳng hạn như số khách đến cửa hàng mỗi giờ, số email nhận được mỗi ngày, số tai nạn trên cao tốc mỗi tháng, số bàn thắng trong một trận bóng đá, hay số đột biến trên một đoạn DNA. Điểm chung của các biến này là $$y \in \{0,1,2,3,\ldots\}$$: chúng là các số nguyên không âm, thường không có chặn trên cố định, và phương sai thường tăng khi giá trị trung bình tăng. Từ đó nảy sinh câu hỏi quen thuộc: liệu ta có thể dùng hồi quy tuyến tính cho loại dữ liệu này hay không?

## 1. Hạn chế của hồi quy tuyến tính với dữ liệu đếm

![Poisson Regression Basics]({{ site.baseurl }}/img/chapter_img/chapter06/poisson_regression_basics.png)

Khó khăn cơ bản của hồi quy tuyến tính trong bối cảnh này là mô hình có thể tạo ra dự đoán âm, trong khi số lần xảy ra của một sự kiện không thể nhỏ hơn 0. Hình minh họa cho thấy ở hình bên trái, đường hồi quy tuyến tính có thể đi vào vùng giá trị âm; còn ở hình bên phải, hồi quy Poisson dùng **hàm liên kết log (log link)** để bảo đảm tham số cường độ $$\lambda$$ luôn dương. Nói cách khác, thay vì dự đoán trực tiếp số đếm, ta mô hình hóa log của tốc độ kỳ vọng để đầu ra luôn phù hợp với bản chất dữ liệu.

## 2. Hồi quy Poisson dưới góc nhìn mô hình sinh

### 2.1. Hàm liên kết log (Log Link Function)

Ý tưởng cốt lõi của hồi quy Poisson là giữ phần tuyến tính ở bên trong, nhưng dùng **hàm liên kết log** để bảo đảm tốc độ kỳ vọng $$\lambda$$ luôn lớn hơn 0.

**Hàm liên kết log**:
$$
\log(\lambda) = \alpha + \beta x
$$

**Hàm ngược (hàm mũ)**:
$$
\lambda = e^{\alpha + \beta x}
$$

### 2.2. Câu chuyện sinh dữ liệu (Generative Story)

Theo ngôn ngữ **câu chuyện sinh dữ liệu (generative story)**, mô hình gồm ba bước. Từ biến dự báo $$x$$, ta tạo ra đại lượng tuyến tính $$\eta=\alpha+\beta x$$. Đại lượng này đi qua hàm mũ để cho tốc độ kỳ vọng $$\lambda=\exp(\eta)$$. Cuối cùng, số đếm quan sát được sinh ra từ phân phối Poisson, tức $$y\sim\text{Poisson}(\lambda)$$. Việc tách rõ ba bước này cho thấy mô hình vừa giữ được cấu trúc tuyến tính thuận tiện cho suy luận, vừa tôn trọng bản chất xác suất của dữ liệu đếm.

Phân phối Poisson có dạng:
$$
P(y = k \mid \lambda) = \frac{\lambda^k e^{-\lambda}}{k!}
$$

Điểm đặc trưng của phân phối này là giá trị trung bình và phương sai đều bằng $$\lambda$$; tính chất này được gọi là **đồng phân tán (equidispersion)**.

![Exponential Function Parameters]({{ site.baseurl }}/img/chapter_img/chapter06/exponential_function_parameters.png)

Hình minh họa cho thấy vai trò của từng tham số trong hàm mũ. Ở hình bên trái, hàm cơ bản $$\lambda=e^\eta$$ luôn dương và đi qua điểm $$\lambda=1$$ khi $$\eta=0$$, thể hiện mức tốc độ nền. Ở hình giữa, thay đổi **hệ số chặn (intercept)** $$\alpha$$ làm dịch chuyển toàn bộ đường cong lên hoặc xuống, qua đó thay đổi mức nền của tốc độ. Ở hình bên phải, thay đổi **độ dốc (slope)** $$\beta$$ làm tốc độ tăng nhanh hơn hoặc chậm hơn theo $$x$$, phản ánh mức độ liên hệ giữa biến dự báo và cường độ xảy ra sự kiện.

## 3. Hồi quy Poisson Bayes trong PyMC

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

### Thử nghiệm: Hậu nghiệm của hồi quy Poisson và tỷ số tốc độ

Thêm từng điểm dữ liệu đếm để quan sát bó đường $$\lambda(x)$$ và tỷ số tốc độ $$\exp(b)$$ thu hẹp dần.

<div class="interactive-demo" markdown="1">
<div data-demo="glm-explainer" data-lang="vi" data-tab="poisson"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 4. Diễn giải hệ số: Tỷ số tốc độ (Rate Ratios)

### 4.1. Tỷ số tốc độ

**Trên thang log**:
$$
\log(\lambda) = \alpha + \beta x
$$

Trên thang log, mỗi khi $$x$$ tăng thêm 1 đơn vị thì log của tốc độ kỳ vọng tăng thêm $$\beta$$ đơn vị.

**Trên thang tốc độ gốc**:
$$
\lambda = e^{\alpha + \beta x}
$$

Khi quay về thang gốc, tốc độ kỳ vọng được nhân với $$e^\beta$$. Đại lượng $$e^\beta$$ này là **tỷ số tốc độ (rate ratio)**, và là cách diễn giải tự nhiên nhất cho hệ số của hồi quy Poisson.

### 4.2. Ví dụ cụ thể: Số lượt ghé quán tăng ra sao

Giả sử trung bình hậu nghiệm của mô hình là:

$$
\log(\lambda)=2.30 + 0.25x
$$

trong đó $$x$$ là số chiến dịch quảng cáo đang chạy trong tuần. Khi đó:

- Nếu $$x=0$$ thì $$\lambda=e^{2.30}\approx 10$$, nghĩa là quán kỳ vọng khoảng 10 lượt ghé mỗi ngày.
- Nếu $$x=1$$ thì $$\lambda=e^{2.55}\approx 12.8$$.
- Nếu $$x=2$$ thì $$\lambda=e^{2.80}\approx 16.4$$.

Ở đây $$e^{0.25}\approx 1.28$$, nên mỗi khi thêm 1 chiến dịch quảng cáo, số lượt ghé kỳ vọng được nhân khoảng 1.28 lần, tức tăng gần 28%. Điều này không có nghĩa là số lượt ghé luôn tăng cố định 0.25 lượt hay 2.8 lượt. Vì tác động trong hồi quy Poisson có tính **nhân** chứ không phải **cộng**, mức tăng tuyệt đối phụ thuộc vào mức nền ban đầu: từ 10 lên 12.8 là tăng khoảng 2.8 lượt, còn từ 12.8 lên 16.4 là tăng khoảng 3.6 lượt.

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

## 5. Kiểm tra dự báo hậu nghiệm (Posterior Predictive Checks)

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

## 6. Quá phân tán (Overdispersion): Khi phương sai lớn hơn trung bình

Một giả định trung tâm của hồi quy Poisson là phương sai bằng trung bình. Trong dữ liệu thực, giả định này thường bị vi phạm khi phương sai lớn hơn trung bình, hiện tượng được gọi là **quá phân tán (overdispersion)**. Khi đó, mô hình Poisson thường tỏ ra quá tự tin và đánh giá thấp độ bất định. Hai hướng xử lý phổ biến là dùng **hồi quy nhị thức âm (Negative Binomial regression)** để cho phép phương sai lớn hơn trung bình một cách linh hoạt, hoặc dùng **Zero-Inflated Poisson** khi dữ liệu có nhiều giá trị 0 vượt quá mức mô hình Poisson thông thường giải thích được.

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

### Thử nghiệm: Poisson hay Negative Binomial?

Từ tỷ số phương sai/trung bình đến kiểm tra dự báo hậu nghiệm: mô hình Poisson bị bác bỏ, trong khi Negative Binomial nắm bắt được độ phân tán của dữ liệu.

<div class="interactive-demo" markdown="1">
<div data-demo="overdisp-explainer" data-lang="vi" data-data="nb"></div>
</div>

## Tóm tắt

Hồi quy Poisson là mô hình tự nhiên cho dữ liệu đếm vì nó khắc phục trực tiếp điểm yếu của hồi quy tuyến tính: dự đoán tuyến tính có thể âm, còn số đếm thì không. Bằng cách dùng **hàm liên kết log** để mô hình hóa $$\log(\lambda)=\alpha+\beta x$$ rồi chuyển về $$\lambda$$ trên thang gốc, hồi quy Poisson bảo đảm tốc độ kỳ vọng luôn dương. Hệ số của mô hình được diễn giải tốt nhất qua **tỷ số tốc độ** $$e^\beta$$, và giả định quan trọng nhất cần kiểm tra là phương sai có xấp xỉ trung bình hay không. Nếu dữ liệu bị quá phân tán, cần chuyển sang các mô hình linh hoạt hơn.

Điểm cốt lõi cần nhớ là hàm liên kết log không chỉ là một phép biến đổi toán học, mà là cơ chế giúp phần tuyến tính của mô hình tương thích với bản chất của dữ liệu đếm và dữ liệu tốc độ.

Bài tiếp theo: **Đánh giá mô hình cho GLMs (Model Evaluation for GLMs)**.


## Khung giải thích (nên đọc chậm): Tính nhanh tốc độ kỳ vọng, Offset và kiểm tra Quá phân tán

Khi xây dựng và đọc mô hình hồi quy Poisson Bayes, hãy kiểm tra chậm rãi 4 bước:

1. **Tính $$\log \lambda$$ từ phương trình tuyến tính** (cộng thêm $$\log(\text{exposure})$$ nếu độ dài quan sát khác nhau).
2. **Lấy hàm mũ $$\lambda = e^{\log\lambda}$$** để đọc số đếm kỳ vọng thực tế.
3. **Diễn giải $$e^\beta$$ theo phần trăm thay đổi nhân tính:** Ví dụ $$e^\beta = 1.25$$ nghĩa là tăng 1 đơn vị $$x$$ làm số đếm kỳ vọng tăng thêm $$25\%$$.
4. **Kiểm tra tỷ số Phương sai / Trung bình (và PPC):** Nếu phương sai phần dư lớn hơn trung bình rõ rệt, cần chuyển sang Negative Binomial.

### Ví dụ tính toán cầm tay chỉ việc: Dự báo số yêu cầu hỗ trợ kỹ thuật theo số người dùng mới

Giả sử mô hình hồi quy Poisson Bayes cho số ticket hỗ trợ mỗi ngày có $$\alpha = 1.5$$ và $$\beta = 0.2$$ (với $$x$$ là số nghìn người dùng mới đăng ký trong ngày):

| Số nghìn người dùng mới $$x$$ | $$\log \lambda = 1.5 + 0.2x$$ | Số ticket kỳ vọng $$\lambda = e^{\log\lambda}$$ | Độ lệch chuẩn Poisson $$\sqrt{\lambda}$$ | Tỷ số so với mức trước |
| --- | --- | --- | --- | --- |
| $$x = 0$$ | $$1.50$$ | $$e^{1.5} \approx 4.48$$ | $$\sqrt{4.48} \approx 2.12$$ | — |
| $$x = 1$$ | $$1.70$$ | $$e^{1.7} \approx 5.47$$ | $$\sqrt{5.47} \approx 2.34$$ | $$e^{0.2} \approx 1.221\; (+22.1\%)$$ |
| $$x = 2$$ | $$1.90$$ | $$e^{1.9} \approx 6.69$$ | $$\sqrt{6.69} \approx 2.59$$ | $$e^{0.2} \approx 1.221\; (+22.1\%)$$ |

Nếu cùng mức $$x = 2$$ nhưng ta theo dõi trong $$t = 3$$ ngày liên tiếp, chỉ cần cộng offset $$\ln(3) \approx 1.099$$: $$\lambda_{\text{3 ngày}} = \exp(1.90 + \ln 3) = 3 \times 6.69 = 20.07$$ ticket.

**Hiểu lầm cần tránh:** Đặt prior phẳng quá rộng (như $$\beta \sim \mathcal{N}(0, 10^2)$$) trong hồi quy Poisson. Vì đi qua hàm mũ $$e^{\beta x}$$, chỉ cần $$\beta = 10$$ và $$x = 2$$ đã sinh ra $$\lambda = e^{20} \approx 4.85 \times 10^8$$ gây tràn số khi lấy mẫu MCMC!

**Kiểm tra nhanh:** Nếu quan sát thực tế tại $$x = 2$$ có trung bình $$\bar y = 6.7$$ nhưng phương sai mẫu $$s^2 = 28.0$$ (gấp hơn 4 lần trung bình), đây là dấu hiệu rõ ràng của **quá phân tán** — cần thay Poisson bằng Negative Binomial.

---

## Video tham khảo

- [Poisson regression - clearly explained](https://www.youtube.com/watch?v=Obpz_Uvo2rQ) — TileStats, English. **Xem trước**. Giải thích hồi quy Poisson cho dữ liệu đếm và lý do đường thẳng tuyến tính không bảo đảm được giá trị không âm.
- [Regression with Count Data: Poisson and Negative Binomial](https://www.youtube.com/watch?v=uGKnoAw-PFQ) — Matthew E. Clapham, English. So sánh mô hình Poisson với Negative Binomial, hỗ trợ phần xử lý khi phương sai lớn hơn trung bình.
- [Statistical Rethinking 2023 - 10 - Counts & Hidden Confounds](https://www.youtube.com/watch?v=jokxu18egu0) — Richard McElreath, English. Trình bày mô hình đếm cùng các biến nhiễu ẩn, phù hợp với cách tiếp cận Poisson như một GLM Bayes.

## Bài tập

**Bài tập 1**: Sinh dữ liệu đếm, khớp mô hình hồi quy Poisson và diễn giải tỷ số tốc độ (rate ratio).

**Bài tập 2**: So sánh dự đoán giữa hồi quy tuyến tính và hồi quy Poisson, sau đó trực quan hóa sự khác biệt.

**Bài tập 3**: Xây dựng mô hình hồi quy Poisson với nhiều biến dự báo và diễn giải từng hệ số.

**Bài tập 4**: Áp dụng trên dữ liệu thực để dự đoán số lượt khách ghé thăm từ các đặc trưng thời gian và thời tiết.

**Bài tập 5**: Kiểm tra hiện tượng quá phân tán (overdispersion); nếu có, thử xây dựng mô hình Negative Binomial để thay thế.

## Tài liệu tham khảo

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.
- Chapter 6: Generalized linear models

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 11: God Spiked the Integers

---

*Bài học tiếp theo: [6.3 Model Evaluation for GLMs]({{ site.baseurl }}/contents/vi/chapter06/06_03_model_evaluation_glm/)*
