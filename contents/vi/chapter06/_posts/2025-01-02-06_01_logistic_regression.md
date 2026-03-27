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

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **Logistic Regression** (hồi quy logistic) như một mô hình nền tảng cho các **binary outcomes** (biến kết quả nhị phân) như yes/no, success/failure, hay 0/1. Trọng tâm của bài không chỉ là thay một công thức hồi quy khác, mà là hiểu vì sao linear regression không phù hợp với dữ liệu nhị phân, vì sao ta cần **link function** (hàm liên kết), và vì sao hệ số của mô hình phải được diễn giải thông qua **odds ratio** (tỷ số odds) thay vì theo trực giác tuyến tính thông thường. Đây cũng là cánh cửa đầu tiên để đi vào họ **Generalized Linear Models (GLMs)**, tức các mô hình tuyến tính tổng quát.

## Giới thiệu: Vấn đề của Linear Regression cho Binary Data

Giả sử chúng ta muốn dự đoán một người có mua sản phẩm hay không, có vượt qua kỳ thi hay không, hoặc có mắc bệnh hay không. Trong tất cả các ví dụ này, **outcome** (biến kết quả) chỉ nhận hai giá trị, nghĩa là $$y \in \{0,1\}$$. Câu hỏi tự nhiên là liệu ta có thể dùng luôn linear regression quen thuộc hay không.

$$
y = \alpha + \beta x + \epsilon
$$

Vấn đề xuất hiện ngay lập tức: linear regression có thể dự đoán bất kỳ giá trị nào trên trục số thực, từ âm vô cùng đến dương vô cùng, trong khi xác suất lại bắt buộc phải nằm trong đoạn $$[0,1]$$. Điều này cho thấy ta cần một mô hình vẫn giữ được phần dự báo tuyến tính ở bên trong, nhưng có cơ chế biến đổi kết quả cuối cùng thành một xác suất hợp lệ.

## 1. Tại sao Linear Regression Không Hoạt động

![Logistic Regression Basics]({{ site.baseurl }}/img/chapter_img/chapter06/logistic_regression_basics.png)

Đối với dữ liệu nhị phân, khó khăn cốt lõi của linear regression nằm ở chỗ mô hình này không biết rằng đầu ra của ta phải là xác suất. Ở panel bên trái, đường hồi quy tuyến tính có thể cho ra các dự đoán nhỏ hơn 0 hoặc lớn hơn 1, tức là những giá trị vô nghĩa nếu ta hiểu chúng là probability. Ở panel bên phải, logistic regression khắc phục điểm này bằng cách dùng **logistic function** (hàm logistic) để biến một **linear predictor** (bộ dự báo tuyến tính) thành xác suất hợp lệ, nhờ đó mọi dự đoán đều luôn nằm trong khoảng $$[0,1]$$.

## 2. Logistic Regression: Generative Model

![Link Functions Comparison]({{ site.baseurl }}/img/chapter_img/chapter06/link_functions_comparison.png)

### 2.1. Link Function

Ý tưởng trung tâm của logistic regression là vẫn xây dựng một biểu thức tuyến tính ở tầng bên trong, nhưng sau đó đi qua một **link function** (hàm liên kết) để bảo đảm đầu ra cuối cùng là xác suất.

**Logit link function**:
$$
\text{logit}(p) = \log\left(\frac{p}{1-p}\right) = \alpha + \beta x
$$

**Inverse** (logistic function):
$$
p = \frac{1}{1 + e^{-(\alpha + \beta x)}} = \frac{e^{\alpha + \beta x}}{1 + e^{\alpha + \beta x}}
$$

### 2.2. Generative Story

Ta có thể đọc mô hình theo đúng tinh thần **generative story** (câu chuyện sinh dữ liệu) như sau. Trước hết, từ biến dự báo $$x$$ ta tạo ra một đại lượng tuyến tính $$\eta=\alpha+\beta x$$. Tiếp theo, đại lượng này được biến đổi qua hàm logistic để cho ra xác suất $$p=\text{logistic}(\eta)$$. Cuối cùng, quan sát nhị phân được sinh ra theo phân phối Bernoulli, tức $$y\sim\text{Bernoulli}(p)$$. Cách viết này giúp ta thấy logistic regression không phải là một “mẹo biến đổi công thức”, mà là một mô hình xác suất hoàn chỉnh.

### 2.3. Quy tắc phân lớp Bayes từ prior-likelihood-posterior

Cho lớp $$c_i$$ và đặc trưng $$x$$, xác suất hậu nghiệm lớp có dạng:

$$
P(c_i\mid x)=\frac{P(x\mid c_i)P(c_i)}{\sum_j P(x\mid c_j)P(c_j)}
\propto P(x\mid c_i)P(c_i).
$$

Với mất mát 0-1, quy tắc phân lớp tối ưu là chọn lớp có posterior lớn nhất:

$$
\hat c(x)=\arg\max_i\;P(c_i\mid x).
$$

Điểm này là cầu nối trực tiếp từ Bayes theorem (Chapter 1-2) sang bài toán phân lớp ở Buổi 8.

### 2.4. Ví dụ Session 8: prior-shift trong phân lớp trái cây

Giả sử có 2 lớp: Táo ($$c_1$$) và Cam ($$c_2$$). Cùng một đặc trưng $$x$$ cho likelihood ratio:

$$
\frac{P(x\mid c_1)}{P(x\mid c_2)}=2.
$$

**Bối cảnh A** (siêu thị miền ôn đới): $$P(c_1)=0.8,\;P(c_2)=0.2$$.

Khi đó posterior odds:

$$
\frac{P(c_1\mid x)}{P(c_2\mid x)}=2\times\frac{0.8}{0.2}=8.
$$

**Bối cảnh B** (chợ miền nhiệt đới): $$P(c_1)=0.2,\;P(c_2)=0.8$$.

Khi đó:

$$
\frac{P(c_1\mid x)}{P(c_2\mid x)}=2\times\frac{0.2}{0.8}=0.5.
$$

Kết luận: cùng một bằng chứng cảm biến $$x$$ nhưng thay prior lớp có thể đảo quyết định phân lớp.

### 2.5. Từ posterior sang decision rule tối thiểu rủi ro

Khi chi phí sai khác nhau, không nên dùng ngưỡng 0.5 cố định. Với tập hành động $$a$$, chọn:

$$
a^*(x)=\arg\min_a\sum_i L(a,c_i)P(c_i\mid x).
$$

#### Ví dụ hai lớp, ba hành động (có reject)

Hai trạng thái thật: $$c_1, c_2$$. Ba hành động: chọn $$c_1$$, chọn $$c_2$$, hoặc **reject** (trì hoãn để đo thêm).

Trong ví dụ minh họa này, ta giả sử **loss matrix** (ma trận mất mát) được chọn theo cách rất đơn giản: dự đoán đúng thì chi phí bằng 0, dự đoán nhầm thì chi phí bằng 10, còn quyết định **reject** thì chịu chi phí bằng 3 vì phải đo thêm hoặc chờ thêm thông tin.

Giả sử posterior tại một điểm $$x$$ là $$P(c_1\mid x)=0.55,\;P(c_2\mid x)=0.45$$.

Khi đó:

$$
R(a=c_1\mid x)=10\cdot 0.45=4.5,
$$

$$
R(a=c_2\mid x)=10\cdot 0.55=5.5,
$$

$$
R(a=\text{reject}\mid x)=3.
$$

Nên hành động tối ưu là reject vì rủi ro kỳ vọng thấp nhất. Đây là ví dụ chuẩn "two-class/three-action" của Buổi 8.

### 2.6. Dạng discriminant và log-discriminant

Trong thực hành, ta thường so sánh trực tiếp discriminant:

$$
g_i(x)=\log P(x\mid c_i)+\log P(c_i),
$$

và chọn lớp có $$g_i(x)$$ lớn nhất.

Vì log là phép biến đổi đơn điệu, việc tối đa hóa posterior tương đương tối đa hóa log-discriminant, đồng thời ổn định số học tốt hơn khi xác suất rất nhỏ.

### 2.7. Trường hợp Gaussian: biên tuyến tính hay bậc hai

Nếu $$P(x\mid c_i)$$ là Gaussian đa biến, thì hình dạng của biên quyết định phụ thuộc vào cấu trúc covariance. Khi các lớp dùng **covariance chung** với $$\Sigma_i=\Sigma$$, biên quyết định sẽ là tuyến tính, gần với trực giác của LDA. Ngược lại, khi mỗi lớp có covariance riêng, tức $$\Sigma_i$$ khác nhau, biên quyết định thường trở thành bậc hai, gần với trực giác của QDA. Cách nhìn này đặc biệt hữu ích vì nó nối quy tắc posterior ở mức xác suất với hình học của biên phân lớp trong không gian đặc trưng.

![Logistic Function Parameters]({{ site.baseurl }}/img/chapter_img/chapter06/logistic_function_parameters.png)

Hình này giúp ta đọc logistic function một cách trực quan hơn. Ở panel bên trái, hàm $$p=\frac{1}{1+e^{-\eta}}$$ có dạng chữ S quen thuộc, đi qua điểm $$p=0.5$$ khi $$\eta=0$$ và tiệm cận dần về 0 và 1 ở hai đầu. Ở panel giữa, thay đổi $$\alpha$$, tức **intercept** (hệ số chặn), chủ yếu làm đường cong dịch sang trái hoặc sang phải, nên có thể hiểu như việc thay đổi mức xác suất nền. Ở panel bên phải, thay đổi $$\beta$$, tức **slope** (độ dốc), làm đường cong thoải hơn hoặc dốc hơn, qua đó phản ánh độ mạnh của mối liên hệ giữa biến dự báo và xác suất của biến kết quả.

## 3. Bayesian Logistic Regression trong PyMC

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

## 4. Interpretation: Odds Ratios

### 4.1. Odds vs Probability

Để diễn giải logistic regression đúng cách, ta cần phân biệt **probability** (xác suất) với **odds**. Xác suất được viết là $$p=P(y=1)$$, còn odds được định nghĩa bởi $$\text{odds}=\frac{p}{1-p}$$. Khi $$p=0.5$$ thì odds bằng 1, nghĩa là hai khả năng cân bằng nhau; khi $$p=0.8$$ thì odds bằng 4, tức khả năng xảy ra biến cố lớn gấp bốn lần khả năng không xảy ra; còn khi $$p=0.2$$ thì odds chỉ bằng 0.25, nghĩa là khả năng không xảy ra biến cố cao hơn nhiều.

![Odds vs Probability]({{ site.baseurl }}/img/chapter_img/chapter06/odds_probability_relationship.png)

Hình minh họa cho thấy mối liên hệ giữa probability, odds, và **log-odds** (log của odds). Ở panel bên trái, khi probability tăng từ 0.2 lên 0.5 rồi 0.8 thì odds thay đổi theo cách phi tuyến từ 0.25 lên 1 rồi 4. Điều này nhắc ta rằng odds nhỏ hơn 1 tương ứng với biến cố ít có khả năng xảy ra hơn, còn odds lớn hơn 1 tương ứng với biến cố có khả năng xảy ra hơn. Ở panel bên phải, khi lấy log của odds, điểm $$p=0.5$$ trở thành 0, các xác suất nhỏ hơn 0.5 cho log-odds âm, và các xác suất lớn hơn 0.5 cho log-odds dương. Chính trên thang log-odds này mà logistic regression trở lại dạng tuyến tính quen thuộc: $$\text{logit}(p)=\alpha+\beta x$$.

### 4.2. Interpreting β

**On log-odds scale**:
$$
\log\left(\frac{p}{1-p}\right) = \alpha + \beta x
$$

Vì vậy, trên thang log-odds, mỗi khi $$x$$ tăng thêm 1 đơn vị thì log-odds tăng thêm $$\beta$$ đơn vị.

**On odds scale**:
$$
\text{odds} = e^{\alpha + \beta x}
$$

Nếu quay trở lại thang odds, ta thấy mỗi lần $$x$$ tăng 1 đơn vị thì odds sẽ được nhân với $$e^\beta$$. Đây chính là **odds ratio** (tỷ số odds), và cũng là cách diễn giải thực tế nhất cho hệ số của logistic regression.

### 4.3. Một ví dụ cụ thể: từ log-odds sang xác suất dự đoán

Giả sử posterior mean của mô hình cho ta phương trình:

$$
\log\left(\frac{p}{1-p}\right) = -0.4 + 1.1x
$$

trong đó $$x$$ là điểm đánh giá đã được standardize. Ta có thể đọc mô hình theo từng bước:

- Nếu $$x=0$$ thì log-odds bằng $$-0.4$$, suy ra odds là $$e^{-0.4}\approx 0.67$$, nên xác suất là $$p=\frac{0.67}{1+0.67}\approx 0.40$$.
- Nếu $$x=1$$ thì log-odds bằng $$0.7$$, suy ra odds là $$e^{0.7}\approx 2.01$$, nên xác suất tăng lên khoảng $$0.67$$.
- Nếu $$x=2$$ thì log-odds bằng $$1.8$$, suy ra odds là $$e^{1.8}\approx 6.05$$, nên xác suất lên khoảng $$0.86$$.

Điểm rất hay bị đọc nhầm là hệ số $$\beta=1.1$$ không có nghĩa là xác suất tăng cố định 1.1 đơn vị hay tăng 110 điểm phần trăm. Ý đúng là: mỗi khi $$x$$ tăng thêm 1 đơn vị thì **odds** được nhân với $$e^{1.1}\approx 3$$. Vì logistic regression là tuyến tính trên thang log-odds nhưng phi tuyến trên thang xác suất, nên cùng tăng 1 đơn vị của $$x$$ có thể làm xác suất nhảy khác nhau tùy điểm xuất phát: từ $$0.40$$ lên $$0.67$$ là tăng khoảng 27 điểm phần trăm, còn từ $$0.67$$ lên $$0.86$$ là tăng khoảng 19 điểm phần trăm.

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

## 5. Posterior Predictive Checks

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

Logistic regression là câu trả lời tự nhiên khi biến kết quả chỉ có hai trạng thái. Vấn đề mà nó giải quyết là linear regression không thể bảo đảm dự đoán nằm trong khoảng $$[0,1]$$, còn lời giải của nó là dùng **logit link** để nối một cấu trúc tuyến tính bên trong với một xác suất hợp lệ ở đầu ra. Mô hình cốt lõi có dạng $$\log\left(\frac{p}{1-p}\right)=\alpha+\beta x$$, và hệ số nên được đọc qua **odds ratio** $$e^\beta$$ thay vì theo trực giác “tăng bao nhiêu đơn vị của $$y$$” như ở linear regression. Trong PyMC, điều này được triển khai một cách rất trực tiếp bằng phân phối `pm.Bernoulli` kết hợp với `pm.math.invlogit`.

Điểm quan trọng nhất cần giữ lại là tư duy của GLM: ta vẫn bắt đầu bằng một phần tuyến tính, nhưng dùng một hàm liên kết phù hợp để xử lý những biến kết quả không còn tuân theo mô hình Gaussian quen thuộc.

Bài tiếp theo: **Poisson Regression** cho count data.

## Bài tập

**Bài tập 1**: Generate binary data. Fit logistic regression. Interpret odds ratio.

**Bài tập 2**: Compare predictions của linear vs logistic regression. Visualize differences.

**Bài tập 3**: Multiple predictors logistic regression. Interpret each coefficient.

**Bài tập 4**: Real data - predict customer churn (0/1) từ usage features.

**Bài tập 5**: Posterior predictive checks. Compute accuracy, sensitivity, specificity.

## Tài liệu Tham khảo

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.
- Chapter 5: Logistic regression

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 10: Big Entropy and the Generalized Linear Model

---

*Bài học tiếp theo: [6.2 Poisson Regression](/vi/chapter06/poisson-regression/)*
