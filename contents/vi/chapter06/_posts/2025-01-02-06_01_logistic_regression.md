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

## Mục tiêu học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **hồi quy logistic (logistic regression)** như một mô hình nền tảng cho các **biến kết quả nhị phân (binary outcomes)** như có/không, thành công/thất bại, hay 0/1. Trọng tâm của bài không chỉ là thay một công thức hồi quy khác, mà là hiểu vì sao hồi quy tuyến tính không phù hợp với dữ liệu nhị phân, vì sao ta cần **hàm liên kết (link function)**, và vì sao hệ số của mô hình phải được diễn giải thông qua **tỷ số odds (odds ratio)** thay vì theo trực giác tuyến tính thông thường. Đây cũng là bước mở đầu để tiếp cận họ **mô hình tuyến tính tổng quát (Generalized Linear Models — GLMs)**.

## Giới thiệu: Hạn chế của hồi quy tuyến tính với dữ liệu nhị phân

Giả sử chúng ta muốn dự đoán một người có mua sản phẩm hay không, có vượt qua kỳ thi hay không, hoặc có mắc bệnh hay không. Trong tất cả các ví dụ này, biến kết quả chỉ nhận hai giá trị, nghĩa là $$y \in \{0,1\}$$. Câu hỏi tự nhiên là liệu ta có thể dùng trực tiếp mô hình hồi quy tuyến tính quen thuộc hay không:

$$
y = \alpha + \beta x + \epsilon
$$

Vấn đề xuất hiện ngay lập tức: hồi quy tuyến tính có thể dự đoán bất kỳ giá trị nào trên trục số thực, từ âm vô cùng đến dương vô cùng, trong khi xác suất bắt buộc phải nằm trong đoạn $$[0,1]$$. Do đó, ta cần một mô hình vẫn giữ được phần dự báo tuyến tính ở bên trong, nhưng có cơ chế biến đổi đầu ra thành một xác suất hợp lệ.

## 1. Vì sao hồi quy tuyến tính không phù hợp

![Logistic Regression Basics]({{ site.baseurl }}/img/chapter_img/chapter06/logistic_regression_basics.png)

Đối với dữ liệu nhị phân, hạn chế cốt lõi của hồi quy tuyến tính nằm ở chỗ mô hình này không bị ràng buộc để đầu ra là một xác suất. Ở hình bên trái, đường hồi quy tuyến tính có thể cho ra các dự đoán nhỏ hơn 0 hoặc lớn hơn 1, vốn không có ý nghĩa khi diễn giải dưới dạng xác suất. Ở hình bên phải, hồi quy logistic khắc phục nhược điểm này bằng cách dùng **hàm logistic (logistic function)** để chuyển **bộ dự báo tuyến tính (linear predictor)** thành xác suất hợp lệ, bảo đảm mọi giá trị dự đoán đều nằm trong đoạn $$[0,1]$$.

## 2. Hồi quy logistic dưới góc nhìn mô hình sinh

![Link Functions Comparison]({{ site.baseurl }}/img/chapter_img/chapter06/link_functions_comparison.png)

### 2.1. Hàm liên kết (Link Function)

Ý tưởng trung tâm của hồi quy logistic là vẫn xây dựng một biểu thức tuyến tính ở tầng bên trong, sau đó đi qua một **hàm liên kết (link function)** để bảo đảm đầu ra cuối cùng là xác suất.

**Hàm liên kết logit (Logit link function)**:
$$
\text{logit}(p) = \log\left(\frac{p}{1-p}\right) = \alpha + \beta x
$$

**Hàm ngược (hàm logistic)**:
$$
p = \frac{1}{1 + e^{-(\alpha + \beta x)}} = \frac{e^{\alpha + \beta x}}{1 + e^{\alpha + \beta x}}
$$

### 2.2. Câu chuyện sinh dữ liệu (Generative Story)

Ta có thể đọc mô hình theo đúng tinh thần **câu chuyện sinh dữ liệu (generative story)** qua ba bước. Trước hết, từ biến dự báo $$x$$, ta tạo ra một đại lượng tuyến tính $$\eta=\alpha+\beta x$$. Tiếp theo, đại lượng này được biến đổi qua hàm logistic để cho ra xác suất $$p=\text{logistic}(\eta)$$. Cuối cùng, quan sát nhị phân được sinh ra theo phân phối Bernoulli, tức $$y\sim\text{Bernoulli}(p)$$. Cách viết này cho thấy hồi quy logistic không phải là một mẹo biến đổi công thức rời rạc, mà là một mô hình xác suất hoàn chỉnh.

### 2.3. Quy tắc phân lớp Bayes từ tiên nghiệm, hợp lý đến hậu nghiệm

Cho lớp $$c_i$$ và đặc trưng $$x$$, xác suất hậu nghiệm của lớp có dạng:

$$
P(c_i\mid x)=\frac{P(x\mid c_i)P(c_i)}{\sum_j P(x\mid c_j)P(c_j)}
\propto P(x\mid c_i)P(c_i).
$$

Với hàm mất mát 0-1, quy tắc phân lớp tối ưu là chọn lớp có xác suất hậu nghiệm lớn nhất:

$$
\hat c(x)=\arg\max_i\;P(c_i\mid x).
$$

Đây là cầu nối trực tiếp từ định lý Bayes (Chương 1–2) sang bài toán phân lớp.

### 2.4. Ví dụ về dịch chuyển tiên nghiệm (prior-shift) trong phân lớp trái cây

Giả sử có 2 lớp: Táo ($$c_1$$) và Cam ($$c_2$$). Cùng một đặc trưng $$x$$ cho tỷ số hợp lý (likelihood ratio):

$$
\frac{P(x\mid c_1)}{P(x\mid c_2)}=2.
$$

Trong **bối cảnh A** (siêu thị miền ôn đới), xác suất tiên nghiệm là $$P(c_1)=0.8,\;P(c_2)=0.2$$. Khi đó, tỷ số odds hậu nghiệm bằng:

$$
\frac{P(c_1\mid x)}{P(c_2\mid x)}=2\times\frac{0.8}{0.2}=8.
$$

Trong **bối cảnh B** (chợ miền nhiệt đới), xác suất tiên nghiệm là $$P(c_1)=0.2,\;P(c_2)=0.8$$. Khi đó:

$$
\frac{P(c_1\mid x)}{P(c_2\mid x)}=2\times\frac{0.2}{0.8}=0.5.
$$

Như vậy, cùng một bằng chứng cảm biến $$x$$ nhưng sự thay đổi của xác suất tiên nghiệm giữa các lớp có thể làm đảo ngược hoàn toàn quyết định phân lớp.

### 2.5. Từ hậu nghiệm sang quy tắc quyết định tối thiểu rủi ro

Khi chi phí của các loại sai lầm không giống nhau, ta không nên dùng ngưỡng 0.5 cố định. Với tập hành động $$a$$, quy tắc tối ưu là chọn hành động có rủi ro kỳ vọng thấp nhất:

$$
a^*(x)=\arg\min_a\sum_i L(a,c_i)P(c_i\mid x).
$$

#### Ví dụ hai lớp, ba hành động (có tùy chọn từ chối phân lớp)

Xét hai trạng thái thật là $$c_1, c_2$$ và ba hành động: chọn $$c_1$$, chọn $$c_2$$, hoặc **từ chối (reject)** để đo thêm thông tin. Trong ví dụ minh họa này, ta giả sử **ma trận mất mát (loss matrix)** được chọn đơn giản: dự đoán đúng chịu chi phí 0, dự đoán nhầm chịu chi phí 10, còn quyết định **reject** chịu chi phí 3 do phải đo bổ sung hoặc chờ thêm dữ liệu.

Giả sử xác suất hậu nghiệm tại một điểm $$x$$ là $$P(c_1\mid x)=0.55,\;P(c_2\mid x)=0.45$$. Khi đó, rủi ro kỳ vọng của từng hành động là:

$$
R(a=c_1\mid x)=10\cdot 0.45=4.5,
$$

$$
R(a=c_2\mid x)=10\cdot 0.55=5.5,
$$

$$
R(a=\text{reject}\mid x)=3.
$$

Hành động tối ưu trong trường hợp này là reject vì có rủi ro kỳ vọng thấp nhất. Đây là ví dụ chuẩn về bài toán quyết định hai lớp, ba hành động.

### 2.6. Hàm phân biệt (discriminant) và log-discriminant

Trong thực hành, ta thường so sánh trực tiếp hàm phân biệt dạng log:

$$
g_i(x)=\log P(x\mid c_i)+\log P(c_i),
$$

và chọn lớp có giá trị $$g_i(x)$$ lớn nhất. Vì hàm log là phép biến đổi đơn điệu tăng, tối đa hóa xác suất hậu nghiệm tương đương với tối đa hóa log-discriminant, đồng thời ổn định hơn về mặt tính toán số khi xác suất rất nhỏ.

### 2.7. Trường hợp Gaussian: biên quyết định tuyến tính hay bậc hai

Nếu $$P(x\mid c_i)$$ là phân phối Gaussian đa biến, hình dạng của biên quyết định phụ thuộc vào cấu trúc ma trận hiệp phương sai (covariance). Khi các lớp dùng **chung một ma trận hiệp phương sai** với $$\Sigma_i=\Sigma$$, biên quyết định sẽ là tuyến tính, gần với trực giác của phân tích biệt thức tuyến tính (LDA). Ngược lại, khi mỗi lớp có ma trận hiệp phương sai riêng ($$\Sigma_i$$ khác nhau), biên quyết định thường có dạng bậc hai, gần với trực giác của QDA. Cách nhìn này nối trực tiếp quy tắc hậu nghiệm ở mức xác suất với hình học của biên phân lớp trong không gian đặc trưng.

![Logistic Function Parameters]({{ site.baseurl }}/img/chapter_img/chapter06/logistic_function_parameters.png)

Hình trên giúp ta quan sát vai trò của các tham số trong hàm logistic. Ở hình bên trái, hàm $$p=\frac{1}{1+e^{-\eta}}$$ có dạng chữ S, đi qua điểm $$p=0.5$$ khi $$\eta=0$$ và tiệm cận dần về 0 và 1 ở hai đầu. Ở hình giữa, thay đổi **hệ số chặn (intercept)** $$\alpha$$ chủ yếu làm đường cong dịch sang trái hoặc sang phải, phản ánh sự thay đổi của mức xác suất nền. Ở hình bên phải, thay đổi **độ dốc (slope)** $$\beta$$ làm đường cong thoải hơn hoặc dốc hơn, phản ánh độ mạnh của mối liên hệ giữa biến dự báo và xác suất của biến kết quả.

## 3. Hồi quy logistic Bayes trong PyMC

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

### Thử nghiệm: Hậu nghiệm của hồi quy logistic là cả một họ đường cong

Thêm từng điểm dữ liệu để quan sát hậu nghiệm được tính chính xác trên lưới (a, b), từ đó đọc tỷ số odds exp(b) cùng khoảng tin cậy 95%.

<div class="interactive-demo" markdown="1">
<div data-demo="glm-explainer" data-lang="vi" data-tab="logistic"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 4. Diễn giải hệ số: Tỷ số Odds (Odds Ratios)

### 4.1. Odds và xác suất

Để diễn giải hồi quy logistic đúng cách, ta cần phân biệt **xác suất (probability)** với **odds**. Xác suất được viết là $$p=P(y=1)$$, còn odds được định nghĩa bởi $$\text{odds}=\frac{p}{1-p}$$. Khi $$p=0.5$$ thì odds bằng 1, nghĩa là hai khả năng cân bằng nhau; khi $$p=0.8$$ thì odds bằng 4, tức khả năng xảy ra biến cố lớn gấp bốn lần khả năng không xảy ra; còn khi $$p=0.2$$ thì odds chỉ bằng 0.25, nghĩa là khả năng không xảy ra biến cố cao hơn nhiều.

![Odds vs Probability]({{ site.baseurl }}/img/chapter_img/chapter06/odds_probability_relationship.png)

Hình minh họa cho thấy mối liên hệ giữa xác suất, odds và **log-odds**. Ở hình bên trái, khi xác suất tăng từ 0.2 lên 0.5 rồi 0.8, odds thay đổi phi tuyến từ 0.25 lên 1 rồi 4: odds nhỏ hơn 1 ứng với biến cố ít có khả năng xảy ra hơn, còn odds lớn hơn 1 ứng với biến cố dễ xảy ra hơn. Ở hình bên phải, khi lấy log của odds, điểm $$p=0.5$$ tương ứng với 0, các xác suất nhỏ hơn 0.5 cho log-odds âm, và các xác suất lớn hơn 0.5 cho log-odds dương. Chính trên thang log-odds này, hồi quy logistic trở lại dạng tuyến tính quen thuộc: $$\text{logit}(p)=\alpha+\beta x$$.

### 4.2. Diễn giải hệ số $$\beta$$

**Trên thang log-odds**:
$$
\log\left(\frac{p}{1-p}\right) = \alpha + \beta x
$$

Trên thang log-odds, mỗi khi $$x$$ tăng thêm 1 đơn vị thì log-odds tăng thêm $$\beta$$ đơn vị.

**Trên thang odds**:
$$
\text{odds} = e^{\alpha + \beta x}
$$

Khi quay trở lại thang odds, mỗi lần $$x$$ tăng 1 đơn vị thì odds được nhân với $$e^\beta$$. Đại lượng $$e^\beta$$ này là **tỷ số odds (odds ratio)**, và cũng là cách diễn giải thực tế nhất cho hệ số của hồi quy logistic.

### 4.3. Ví dụ cụ thể: Từ log-odds sang xác suất dự đoán

Giả sử trung bình hậu nghiệm của mô hình cho phương trình:

$$
\log\left(\frac{p}{1-p}\right) = -0.4 + 1.1x
$$

trong đó $$x$$ là điểm đánh giá đã được chuẩn hóa. Ta có thể tính lần lượt theo từng giá trị của $$x$$:

- Nếu $$x=0$$ thì log-odds bằng $$-0.4$$, suy ra odds là $$e^{-0.4}\approx 0.67$$, nên xác suất là $$p=\frac{0.67}{1+0.67}\approx 0.40$$.
- Nếu $$x=1$$ thì log-odds bằng $$0.7$$, suy ra odds là $$e^{0.7}\approx 2.01$$, nên xác suất tăng lên khoảng $$0.67$$.
- Nếu $$x=2$$ thì log-odds bằng $$1.8$$, suy ra odds là $$e^{1.8}\approx 6.05$$, nên xác suất tăng lên khoảng $$0.86$$.

Một nhầm lẫn phổ biến là hiểu $$\beta=1.1$$ thành xác suất tăng cố định 1.1 đơn vị hoặc 110 điểm phần trăm. Cách hiểu đúng là: mỗi khi $$x$$ tăng thêm 1 đơn vị, **odds** được nhân với $$e^{1.1}\approx 3$$. Vì hồi quy logistic tuyến tính trên thang log-odds nhưng phi tuyến trên thang xác suất, cùng một mức tăng 1 đơn vị của $$x$$ tạo ra mức thay đổi xác suất khác nhau tùy điểm xuất phát: từ $$0.40$$ lên $$0.67$$ là tăng khoảng 27 điểm phần trăm, còn từ $$0.67$$ lên $$0.86$$ là tăng khoảng 19 điểm phần trăm.

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

## 5. Kiểm tra dự báo hậu nghiệm (Posterior Predictive Checks)

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

Hồi quy logistic là lựa chọn tự nhiên khi biến kết quả chỉ có hai trạng thái. Thay vì dùng hồi quy tuyến tính vốn không thể bảo đảm dự đoán nằm trong đoạn $$[0,1]$$, mô hình sử dụng **hàm liên kết logit** để nối cấu trúc tuyến tính bên trong với xác suất hợp lệ ở đầu ra. Phương trình cốt lõi có dạng $$\log\left(\frac{p}{1-p}\right)=\alpha+\beta x$$, và hệ số nên được diễn giải qua **tỷ số odds** $$e^\beta$$ thay vì theo mức tăng cộng trên $$y$$ như ở hồi quy tuyến tính. Trong PyMC, mô hình được triển khai trực tiếp bằng phân phối `pm.Bernoulli` kết hợp với `pm.math.invlogit`.

Điểm cốt lõi cần nắm là tư duy của GLM: giữ lại phần dự báo tuyến tính, đồng thời chọn hàm liên kết và phân phối phù hợp để xử lý những biến kết quả không tuân theo giả định Gaussian.

Bài tiếp theo: **Hồi quy Poisson (Poisson Regression)** cho dữ liệu đếm.

## Video tham khảo

- [StatQuest: Logistic Regression](https://www.youtube.com/watch?v=yIYKR4sgzI8) — StatQuest with Josh Starmer, English. **Xem trước**. Trình bày cách hồi quy logistic dự đoán xác suất cho biến kết quả nhị phân 0/1.
- [Odds and Log(Odds), Clearly Explained!!!](https://www.youtube.com/watch?v=ARfXDSkQf1Y) — StatQuest with Josh Starmer, English. Giải thích odds và log-odds, hỗ trợ cách đọc hệ số trên thang logit thay vì thang xác suất.
- [Statistical Rethinking 2023 - 04 - Categories & Curves](https://www.youtube.com/watch?v=F0N4b7K_iYQ) — Richard McElreath, English. Trình bày đường cong logistic trong khuôn khổ mô hình Bayes, kết nối công thức với câu chuyện sinh dữ liệu.

## Bài tập

**Bài tập 1**: Sinh dữ liệu nhị phân, khớp mô hình hồi quy logistic và diễn giải tỷ số odds.

**Bài tập 2**: So sánh dự đoán của hồi quy tuyến tính và hồi quy logistic, đồng thời trực quan hóa sự khác biệt.

**Bài tập 3**: Xây dựng mô hình hồi quy logistic với nhiều biến dự báo và diễn giải từng hệ số.

**Bài tập 4**: Áp dụng trên dữ liệu thực để dự đoán tình trạng rời bỏ của khách hàng (0/1) từ các đặc trưng mức độ sử dụng.

**Bài tập 5**: Thực hiện kiểm tra dự báo hậu nghiệm (posterior predictive checks) và tính các chỉ số accuracy, sensitivity, specificity.

## Tài liệu tham khảo

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.
- Chapter 5: Logistic regression

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 10: Big Entropy and the Generalized Linear Model

---

*Bài học tiếp theo: [6.2 Poisson Regression]({{ site.baseurl }}/contents/vi/chapter06/06_02_poisson_regression/)*
