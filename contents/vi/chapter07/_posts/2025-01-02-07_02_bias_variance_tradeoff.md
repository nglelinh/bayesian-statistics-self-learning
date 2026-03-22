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

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu sâu về **bias-variance tradeoff** (đánh đổi giữa độ lệch và độ dao động), một trong những ý tưởng nền tảng nhất của machine learning và statistics. Bài học sẽ giải thích vì sao mô hình quá đơn giản thường có **high bias**, vì sao mô hình quá phức tạp thường có **high variance**, và vì sao mục tiêu thực sự của model selection không phải là đẩy một thành phần về thấp nhất có thể, mà là tìm điểm cân bằng khiến sai số tổng thể nhỏ nhất. Đây là cơ sở trực tiếp để hiểu regularization, overfitting, và cả logic của việc chọn mô hình.

## Giới thiệu: Hai Loại Error

Khi một mô hình dự đoán sai, sai số đó thường không đến từ một nguyên nhân duy nhất. Một phần sai số có thể đến từ việc mô hình quá đơn giản nên bỏ sót cấu trúc thật của dữ liệu; đó là **bias** (độ lệch). Một phần khác có thể đến từ việc mô hình quá nhạy với dữ liệu huấn luyện, khiến chỉ cần thay mẫu một chút là dự đoán dao động mạnh; đó là **variance** (độ dao động). Điều cốt lõi là hai thành phần này thường kéo ngược nhau: giảm bias thường làm variance tăng, còn ép variance xuống quá mạnh thường làm bias tăng lên.

## 1. Bias và Variance: Định nghĩa

### 1.1. Mathematical Definitions

Giả sử chúng ta train model nhiều lần trên different datasets từ cùng một distribution.

**Bias**: Sai lệch giữa **average prediction** và **true value**
$$
\text{Bias}[\hat{f}(x)] = \mathbb{E}[\hat{f}(x)] - f(x)
$$

**Variance**: Variability của predictions across datasets
$$
\text{Variance}[\hat{f}(x)] = \mathbb{E}[(\hat{f}(x) - \mathbb{E}[\hat{f}(x)])^2]
$$

**Total Error**:
$$
\mathbb{E}[(y - \hat{f}(x))^2] = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}
$$

### 1.2. Intuitive Understanding

![Bias-Variance Demonstration](../../../img/chapter_img/chapter07/bias_variance_demonstration.png)

Hình minh họa cho trực giác này rất rõ. Với mô hình bậc 1, các đường fit từ nhiều tập dữ liệu khác nhau khá gần nhau, nghĩa là variance thấp, nhưng hầu hết đều lệch xa quy luật thật, nghĩa là bias cao; đây là trạng thái underfitting điển hình. Với mô hình bậc 3, mức độ linh hoạt vừa đủ để bám sát quy luật thật hơn mà chưa dao động quá nhiều giữa các mẫu, nên bias giảm xuống trong khi variance vẫn còn kiểm soát được; đó là vùng cân bằng tốt nhất của trade-off. Với mô hình bậc 10, đường trung bình có thể đã gần quy luật thật hơn, tức bias thấp hơn, nhưng từng mô hình riêng lẻ lại dao động mạnh theo từng mẫu huấn luyện, nghĩa là variance tăng vọt. Vì vậy, việc nhìn 50 training sets khác nhau như 50 phiên bản khác nhau của cùng một bài toán là cách trực quan nhất để hiểu variance: nó đo mức “rung lắc” của dự đoán khi dữ liệu thay đổi.

## 2. Decomposition: MSE = Bias² + Variance + Noise

![MSE Decomposition](../../../img/chapter_img/chapter07/mse_decomposition.png)

Khi nhìn vào decomposition của MSE, ta thấy ngay vì sao việc chọn mô hình không thể dựa trên một tiêu chí đơn lẻ. Ở vùng độ phức tạp thấp, chẳng hạn bậc 1 hoặc 2, thành phần $$\text{Bias}^2$$ còn lớn vì mô hình quá đơn giản để mô tả dữ liệu, dù variance khi đó khá thấp. Khi độ phức tạp tăng lên vùng trung gian, hai thành phần này bắt đầu cân bằng hơn và tổng MSE đạt mức nhỏ nhất; đó là “sweet spot” thực sự của mô hình. Nhưng khi tiếp tục tăng độ phức tạp, bias có thể giảm thêm một chút trong khi variance tăng rất mạnh, làm MSE tăng trở lại. Biểu đồ stacked ở bên phải đặc biệt hữu ích vì nó cho thấy trực quan rằng mục tiêu không phải là tối thiểu hóa riêng bias hay riêng variance, mà là tối thiểu hóa tổng sai số dự báo.

## 3. Regularization và Bias-Variance

Regularization chính là chiếc núm điều khiển trade-off này. Khi regularization yếu, tức $$\lambda$$ nhỏ, mô hình được phép linh hoạt hơn nên bias có xu hướng thấp nhưng variance lại cao. Khi regularization mạnh, tức $$\lambda$$ lớn, mô hình bị ép đơn giản hơn nên variance giảm, nhưng bias lại tăng.

![Regularization Bias-Variance](../../../img/chapter_img/chapter07/regularization_bias_variance.png)

Ví dụ với polynomial bậc 10 cho thấy điểm này rất rõ. Khi $$\lambda=0.001$$, regularization quá yếu nên mô hình dao động mạnh, biểu hiện ở variance rất lớn và hiện tượng overfitting rõ rệt. Khi tăng dần lên $$0.1$$ rồi $$1$$, variance giảm xuống đáng kể và mô hình bước vào vùng cân bằng tốt hơn. Nếu tiếp tục tăng lên $$10$$ hay $$100$$, mô hình bắt đầu bị bó quá mạnh, các dự đoán trở nên gần như phẳng, variance thấp nhưng bias tăng cao, tức quay lại vùng underfitting. Bài học ở đây là $$\lambda$$ không phải tham số “càng lớn càng an toàn”; nó phải được chọn sao cho bias và variance đạt một mức cân bằng tốt nhất cho mục tiêu dự báo.

## 4. Bayesian Perspective

Trong Bayesian statistics, vai trò của regularization được chuyển thành vai trò của **prior strength** (độ mạnh của tiên nghiệm). Priors yếu để dữ liệu quyết định nhiều hơn nên mô hình linh hoạt hơn nhưng cũng dao động hơn; priors mạnh ràng buộc mô hình nhiều hơn nên variance giảm, nhưng đổi lại bias có thể tăng nếu prior quá cứng.

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

## Tóm tắt

Bias-variance tradeoff cho thấy sai số dự báo không thể được hiểu chỉ bằng một thước đo đơn giản về “độ khớp”. **Bias** phản ánh cái giá của việc dùng một mô hình quá đơn giản, còn **variance** phản ánh cái giá của việc dùng một mô hình quá nhạy với dữ liệu huấn luyện. Công thức $$\text{MSE}=\text{Bias}^2+\text{Variance}+\text{Irreducible Error}$$ nhắc ta rằng mô hình tốt là mô hình cân bằng được hai lực đối nghịch này. Regularization là công cụ thực hành để điều chỉnh điểm cân bằng đó, còn trong Bayesian statistics, chính độ mạnh của prior đảm nhiệm vai trò ấy.

Điểm cần nhớ nhất là một mô hình fit training data thật đẹp chưa chắc là một mô hình tốt; mô hình tốt là mô hình khái quát hóa tốt trên dữ liệu mới.

Bài tiếp theo: **Feature Selection**.

## Bài tập

**Bài tập 1**: Implement bias-variance decomposition from scratch. Verify MSE = Bias² + Variance.

**Bài tập 2**: Generate data. Compute bias-variance for models with different complexities. Find optimal.

**Bài tập 3**: Use Ridge với different λ. Plot bias-variance curve. Find optimal λ.

**Bài tập 4**: Bayesian models với different prior SDs. Compute posterior variance. Relate to bias-variance.

**Bài tập 5**: Real data. Split train/test. Show overfitting với high-degree polynomial. Fix với regularization.

## Tài liệu Tham khảo

**Hastie, T., Tibshirani, R., & Friedman, J. (2009).** *The Elements of Statistical Learning* (2nd Edition). Springer.
- Chapter 7: Model Assessment and Selection

**James, G., et al. (2013).** *An Introduction to Statistical Learning*. Springer.
- Chapter 2: Statistical Learning

---

*Bài học tiếp theo: [7.3 Feature Selection](/vi/chapter07/feature-selection/)*
