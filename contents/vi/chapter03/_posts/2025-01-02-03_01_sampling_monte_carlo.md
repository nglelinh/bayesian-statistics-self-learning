---
layout: post
title: "Bài 3.1: Từ Tích phân Khó đến Sampling - Nền tảng Monte Carlo"
chapter: '03'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter03
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu sâu sắc tại sao **sampling** (lấy mẫu) là giải pháp cốt lõi cho tính toán Bayesian hiện đại. Bạn sẽ không chỉ biết cách sử dụng **phương pháp Monte Carlo**, mà còn hiểu được ý tưởng đằng sau nó: thay vì cố gắng tính toán các tích phân phức tạp một cách trực tiếp, chúng ta lấy mẫu từ phân phối posterior và sử dụng các mẫu đó để ước lượng bất kỳ đại lượng nào chúng ta quan tâm. Bạn sẽ nhận ra rằng sampling không chỉ là một "trick" tính toán, mà là một cách tư duy mạnh mẽ về suy luận thống kê.

## Giới thiệu: Khi Toán học Trở nên Quá Khó

Trong Chapter 02, chúng ta đã học cách tính posterior thông qua định lý Bayes:

$$P(\theta \mid D) = \frac{P(D \mid \theta) \cdot P(\theta)}{P(D)}$$

Trong các ví dụ đơn giản (như Beta-Binomial), chúng ta may mắn có **công thức đóng** (closed-form solution) cho posterior. Chúng ta biết chính xác posterior là phân phối Beta với các tham số cụ thể, và có thể tính toán bất kỳ thứ gì chúng ta muốn: mean, median, credible intervals, v.v.

Nhưng trong thực tế, hầu hết các vấn đề Bayesian **không có công thức đóng**. Hãy xem xét một vài ví dụ:

- **Mô hình hồi quy logistic Bayesian**: Posterior không có dạng phân phối chuẩn nào.
- **Mô hình phân cấp (hierarchical models)**: Posterior là tích phân đa chiều phức tạp.
- **Mô hình hỗn hợp (mixture models)**: Posterior có nhiều mode, không có công thức đơn giản.

Trong những trường hợp này, chúng ta cần tính các tích phân như:

$$E[f(\theta) \mid D] = \int f(\theta) \cdot P(\theta \mid D) \, d\theta$$

Ví dụ:
- Posterior mean: $$E[\theta \mid D] = \int \theta \cdot P(\theta \mid D) \, d\theta$$
- Posterior variance: $$\text{Var}[\theta \mid D] = \int (\theta - E[\theta \mid D])^2 \cdot P(\theta \mid D) \, d\theta$$
- Xác suất: $$P(\theta > c \mid D) = \int_{c}^{\infty} P(\theta \mid D) \, d\theta$$

Vấn đề là: **Làm thế nào chúng ta tính những tích phân này khi không có công thức đóng?**

Đây chính là lúc **sampling** và **phương pháp Monte Carlo** xuất hiện như những công cụ cứu cánh. Thay vì cố gắng tính tích phân trực tiếp, chúng ta sẽ **lấy mẫu** từ posterior và sử dụng các mẫu đó để **ước lượng** bất kỳ đại lượng nào chúng ta cần.

## 1. Vấn đề của Tích phân Trực tiếp: Curse of Dimensionality

Trước khi đi vào giải pháp, hãy hiểu rõ tại sao tích phân trực tiếp lại khó đến vậy.

### 1.1. Grid Approximation: Ý tưởng Đơn giản nhưng Không Khả thi

Một cách tiếp cận tự nhiên để tính tích phân là **grid approximation** (xấp xỉ lưới):

1. Chia không gian tham số thành một lưới các điểm.
2. Tính posterior tại mỗi điểm trên lưới.
3. Xấp xỉ tích phân bằng tổng trên lưới.

Ví dụ, với một tham số $$\theta \in [0, 1]$$, chúng ta có thể chia thành 100 điểm: $$\theta_1 = 0.01, \theta_2 = 0.02, \ldots, \theta_{100} = 1.0$$. Khi đó:

$$E[\theta \mid D] \approx \sum_{i=1}^{100} \theta_i \cdot P(\theta_i \mid D) \cdot \Delta\theta$$

Với một tham số, phương pháp này hoạt động tốt. Nhưng điều gì xảy ra khi chúng ta có **nhiều tham số**?

```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Curse of Dimensionality
dimensions = np.arange(1, 11)
points_per_dimension = 100  # 100 điểm trên mỗi chiều

total_points = points_per_dimension ** dimensions

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Vẽ số điểm cần thiết
axes[0].semilogy(dimensions, total_points, 'o-', linewidth=3, markersize=12, 
                 color='darkred', markerfacecolor='red', markeredgewidth=2)
axes[0].set_xlabel('Số tham số (Dimensions)', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Số điểm lưới cần thiết (log scale)', fontsize=13, fontweight='bold')
axes[0].set_title('Curse of Dimensionality: Grid Approximation\n' +
                  'Số điểm tăng theo cấp số mũ!', 
                  fontsize=15, fontweight='bold')
axes[0].grid(alpha=0.3, linestyle='--')
axes[0].set_xticks(dimensions)

# Annotations
for i in [0, 2, 4, 6, 8]:
    axes[0].annotate(f'{total_points[i]:,.0f} điểm', 
                     xy=(dimensions[i], total_points[i]), 
                     xytext=(dimensions[i]+0.5, total_points[i]*5),
                     fontsize=11, ha='left',
                     arrowprops=dict(arrowstyle='->', color='red', lw=2),
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

# Giải thích
axes[1].axis('off')
explanation = """
╔═══════════════════════════════════════════════════════════╗
║          TẠI SAO GRID APPROXIMATION THẤT BẠI?             ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  VÍ DỤ: 100 điểm trên mỗi chiều                           ║
║                                                           ║
║  • 1 tham số:   100¹ = 100 điểm           ✓ OK           ║
║  • 2 tham số:   100² = 10,000 điểm        ✓ OK           ║
║  • 3 tham số:   100³ = 1,000,000 điểm     ⚠ Chậm         ║
║  • 5 tham số:   100⁵ = 10,000,000,000     ✗ Không khả thi║
║  • 10 tham số:  100¹⁰ = 10²⁰ điểm         ✗ Vô lý!       ║
║                                                           ║
║  ──────────────────────────────────────────────────────  ║
║                                                           ║
║  VẤN ĐỀ:                                                  ║
║    → Số điểm tăng theo CẤP SỐ MŨ với số tham số          ║
║    → Bộ nhớ và thời gian tính toán BỘC PHÁT              ║
║    → Không thể áp dụng cho mô hình thực tế                ║
║                                                           ║
║  GIẢI PHÁP:                                               ║
║    → SAMPLING: Lấy mẫu thông minh từ posterior           ║
║    → Không cần tính toán trên toàn bộ lưới               ║
║    → Khả thi với hàng trăm, hàng nghìn tham số!          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[1].text(0.5, 0.5, explanation, fontsize=11, family='monospace',
            ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.show()

print("=" * 70)
print("CURSE OF DIMENSIONALITY")
print("=" * 70)
for d, n in zip(dimensions[:6], total_points[:6]):
    memory_mb = n * 8 / (1024**2)  # Giả sử mỗi số float64 = 8 bytes
    print(f"{d} tham số: {n:>15,} điểm → {memory_mb:>10,.1f} MB bộ nhớ")
print("\n→ Grid approximation KHÔNG khả thi với nhiều tham số!")
print("=" * 70)
```

Biểu đồ trên cho thấy rõ ràng **curse of dimensionality**: số điểm cần thiết tăng theo cấp số mũ với số tham số. Với chỉ 10 tham số và 100 điểm trên mỗi chiều, chúng ta cần $$10^{20}$$ điểm - một con số vô lý!

### 1.2. Tại sao Không thể Tính Tích phân Giải tích?

Một câu hỏi tự nhiên là: "Tại sao không dùng các phương pháp tích phân giải tích hoặc số học (numerical integration) như Simpson's rule, Gaussian quadrature?"

Câu trả lời là:
- **Các phương pháp này cũng bị curse of dimensionality**: Chúng cần đánh giá hàm tại nhiều điểm, và số điểm tăng theo cấp số mũ.
- **Posterior thường có hình dạng phức tạp**: Nhiều mode, không đối xứng, có tương quan giữa các tham số.
- **Không có công thức đóng cho evidence** $$P(D)$$: Chúng ta cần tích phân trên toàn bộ không gian tham số để tính hằng số chuẩn hóa.

Vậy chúng ta cần một cách tiếp cận hoàn toàn khác.

## 2. Giải pháp: Sampling và Phương pháp Monte Carlo

Ý tưởng cốt lõi của phương pháp Monte Carlo cực kỳ đơn giản và mạnh mẽ:

> **Thay vì tính tích phân trực tiếp, hãy lấy mẫu từ phân phối và sử dụng các mẫu đó để ước lượng.**

### 2.1. Ý tưởng Cơ bản

Giả sử chúng ta muốn tính:

$$E[f(\theta) \mid D] = \int f(\theta) \cdot P(\theta \mid D) \, d\theta$$

Nếu chúng ta có thể **lấy mẫu** từ posterior $$P(\theta \mid D)$$:

$$\theta^{(1)}, \theta^{(2)}, \ldots, \theta^{(S)} \sim P(\theta \mid D)$$

Thì theo **luật số lớn** (Law of Large Numbers), chúng ta có thể ước lượng kỳ vọng bằng **trung bình mẫu**:

$$E[f(\theta) \mid D] \approx \frac{1}{S} \sum_{s=1}^{S} f(\theta^{(s)})$$

Và ước lượng này sẽ **hội tụ** về giá trị thực khi $$S \to \infty$$.

### 2.2. Tại sao Sampling Hoạt động?

Hãy hiểu tại sao phương pháp này lại hiệu quả:

**Luật Số Lớn (Law of Large Numbers)**:
Nếu $$\theta^{(1)}, \theta^{(2)}, \ldots, \theta^{(S)}$$ là các mẫu độc lập từ phân phối $$P(\theta \mid D)$$, thì:

$$\frac{1}{S} \sum_{s=1}^{S} f(\theta^{(s)}) \xrightarrow{S \to \infty} E[f(\theta) \mid D]$$

**Định lý Giới hạn Trung tâm (Central Limit Theorem)**:
Sai số của ước lượng giảm theo $$\sqrt{S}$$:

$$\text{SE} \approx \frac{\sigma}{\sqrt{S}}$$

trong đó $$\sigma$$ là độ lệch chuẩn của $$f(\theta)$$ dưới posterior.

**Ý nghĩa**: Chúng ta có thể kiểm soát độ chính xác bằng cách tăng số mẫu $$S$$, và độ chính xác **không phụ thuộc vào số chiều** (số tham số)!

```python
# Minh họa: Law of Large Numbers
np.random.seed(42)

# Giả sử posterior là Beta(9, 5) (từ ví dụ trước)
from scipy import stats
posterior = stats.beta(9, 5)

# True mean
true_mean = posterior.mean()

# Lấy mẫu với số lượng tăng dần
sample_sizes = [10, 50, 100, 500, 1000, 5000, 10000]
estimates = []
std_errors = []

for S in sample_sizes:
    samples = posterior.rvs(S)
    estimate = np.mean(samples)
    std_error = np.std(samples) / np.sqrt(S)
    estimates.append(estimate)
    std_errors.append(std_error)

# Vẽ
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Hội tụ của ước lượng
axes[0].plot(sample_sizes, estimates, 'o-', linewidth=3, markersize=10, 
             color='blue', label='Monte Carlo Estimate')
axes[0].axhline(true_mean, color='red', linestyle='--', linewidth=2,
                label=f'True Mean = {true_mean:.4f}')
axes[0].fill_between(sample_sizes, 
                     np.array(estimates) - 1.96*np.array(std_errors),
                     np.array(estimates) + 1.96*np.array(std_errors),
                     alpha=0.3, color='blue', label='95% CI')
axes[0].set_xlabel('Số mẫu (S)', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Ước lượng Mean', fontsize=13, fontweight='bold')
axes[0].set_title('Law of Large Numbers: Ước lượng Hội tụ về Giá trị Thực\n' +
                  'Khi số mẫu tăng', 
                  fontsize=15, fontweight='bold')
axes[0].set_xscale('log')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Standard Error giảm theo sqrt(S)
theoretical_se = np.array([posterior.std() / np.sqrt(S) for S in sample_sizes])
axes[1].loglog(sample_sizes, std_errors, 'o-', linewidth=3, markersize=10,
               color='green', label='Empirical SE')
axes[1].loglog(sample_sizes, theoretical_se, '--', linewidth=2,
               color='orange', label='Theoretical SE ∝ 1/√S')
axes[1].set_xlabel('Số mẫu (S)', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Standard Error', fontsize=13, fontweight='bold')
axes[1].set_title('Central Limit Theorem: SE giảm theo √S\n' +
                  'Độ chính xác tăng với nhiều mẫu hơn',
                  fontsize=15, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3, which='both')

plt.tight_layout()
plt.show()

print("\nHỘI TỤ CỦA MONTE CARLO ESTIMATE:")
print("=" * 70)
print(f"{'Số mẫu':<12} {'Estimate':<12} {'Std Error':<12} {'95% CI'}")
print("=" * 70)
for S, est, se in zip(sample_sizes, estimates, std_errors):
    ci_lower = est - 1.96*se
    ci_upper = est + 1.96*se
    print(f"{S:<12} {est:<12.4f} {se:<12.4f} [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"\nTrue Mean: {true_mean:.4f}")
print("=" * 70)
```

Biểu đồ trên cho thấy hai điều quan trọng:
1. **Ước lượng hội tụ về giá trị thực** khi số mẫu tăng (Law of Large Numbers)
2. **Standard error giảm theo $$1/\sqrt{S}$$** (Central Limit Theorem)

### 2.3. Ưu điểm Vượt trội của Sampling

So với grid approximation, sampling có những ưu điểm vượt trội:

1. **Không bị curse of dimensionality**: Độ chính xác chỉ phụ thuộc vào số mẫu $$S$$, không phụ thuộc vào số tham số.
2. **Linh hoạt**: Có thể ước lượng bất kỳ đại lượng nào từ cùng một tập mẫu.
3. **Dễ song song hóa**: Các mẫu có thể được sinh độc lập trên nhiều CPU/GPU.
4. **Tự động tập trung vào vùng quan trọng**: Mẫu tập trung ở nơi posterior có mật độ cao.

## 3. Monte Carlo Estimation: Từ Mẫu đến Suy luận

Khi chúng ta đã có các mẫu từ posterior, chúng ta có thể ước lượng bất kỳ đại lượng nào chúng ta quan tâm.

### 3.1. Ước lượng Posterior Mean

$$E[\theta \mid D] \approx \frac{1}{S} \sum_{s=1}^{S} \theta^{(s)}$$

### 3.2. Ước lượng Posterior Variance

$$\text{Var}[\theta \mid D] \approx \frac{1}{S-1} \sum_{s=1}^{S} (\theta^{(s)} - \bar{\theta})^2$$

### 3.3. Ước lượng Xác suất

$$P(\theta > c \mid D) \approx \frac{1}{S} \sum_{s=1}^{S} \mathbb{1}(\theta^{(s)} > c)$$

trong đó $$\mathbb{1}(\cdot)$$ là hàm indicator (bằng 1 nếu điều kiện đúng, 0 nếu sai).

### 3.4. Ước lượng Credible Intervals

Credible interval X% có thể được ước lượng bằng cách sắp xếp các mẫu và lấy các quantiles:

```python
# Ví dụ: Ước lượng các đại lượng từ mẫu
np.random.seed(123)
S = 10000
samples = posterior.rvs(S)

# Posterior mean
post_mean_mc = np.mean(samples)
post_mean_true = posterior.mean()

# Posterior variance
post_var_mc = np.var(samples, ddof=1)
post_var_true = posterior.var()

# Probability θ > 0.7
prob_greater_07_mc = np.mean(samples > 0.7)
prob_greater_07_true = 1 - posterior.cdf(0.7)

# 95% Credible Interval
ci_lower_mc, ci_upper_mc = np.percentile(samples, [2.5, 97.5])
ci_lower_true, ci_upper_true = posterior.ppf([0.025, 0.975])

# Vẽ histogram với các ước lượng
plt.figure(figsize=(14, 7))
plt.hist(samples, bins=50, density=True, alpha=0.7, color='skyblue', 
         edgecolor='black', label='Monte Carlo Samples')

# True posterior
theta_grid = np.linspace(0, 1, 1000)
plt.plot(theta_grid, posterior.pdf(theta_grid), linewidth=3, color='red',
         label='True Posterior')

# Annotations
plt.axvline(post_mean_mc, color='blue', linestyle='--', linewidth=2,
            label=f'MC Mean = {post_mean_mc:.4f}')
plt.axvline(post_mean_true, color='red', linestyle=':', linewidth=2,
            label=f'True Mean = {post_mean_true:.4f}')
plt.axvspan(ci_lower_mc, ci_upper_mc, alpha=0.2, color='yellow',
            label=f'MC 95% CI: [{ci_lower_mc:.3f}, {ci_upper_mc:.3f}]')

plt.xlabel('θ', fontsize=13, fontweight='bold')
plt.ylabel('Mật độ', fontsize=13, fontweight='bold')
plt.title(f'Monte Carlo Estimation với {S:,} mẫu\n' +
          'Ước lượng rất gần với giá trị thực!',
          fontsize=15, fontweight='bold')
plt.legend(fontsize=11, loc='upper left')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

print("\nSO SÁNH MONTE CARLO VS GIÁTRỊ THỰC:")
print("=" * 70)
print(f"{'Đại lượng':<30} {'Monte Carlo':<15} {'True Value':<15} {'Error'}")
print("=" * 70)
print(f"{'Posterior Mean':<30} {post_mean_mc:<15.6f} {post_mean_true:<15.6f} {abs(post_mean_mc - post_mean_true):.6f}")
print(f"{'Posterior Variance':<30} {post_var_mc:<15.6f} {post_var_true:<15.6f} {abs(post_var_mc - post_var_true):.6f}")
print(f"{'P(θ > 0.7 \mid D)':<30} {prob_greater_07_mc:<15.6f} {prob_greater_07_true:<15.6f} {abs(prob_greater_07_mc - prob_greater_07_true):.6f}")
print(f"{'95% CI Lower':<30} {ci_lower_mc:<15.6f} {ci_lower_true:<15.6f} {abs(ci_lower_mc - ci_lower_true):.6f}")
print(f"{'95% CI Upper':<30} {ci_upper_mc:<15.6f} {ci_upper_true:<15.6f} {abs(ci_upper_mc - ci_upper_true):.6f}")
print("=" * 70)
print(f"\n→ Với {S:,} mẫu, Monte Carlo ước lượng CỰC KỲ CHÍNH XÁC!")
```

## 4. Vấn đề Còn Lại: Làm thế nào Lấy Mẫu từ Posterior?

Phương pháp Monte Carlo rất mạnh mẽ, nhưng nó dựa trên một giả định quan trọng: **chúng ta có thể lấy mẫu từ posterior** $$P(\theta \mid D)$$.

Trong ví dụ Beta-Binomial ở trên, chúng ta may mắn vì posterior là phân phối Beta, và Python (SciPy) có sẵn hàm để lấy mẫu từ Beta. Nhưng trong hầu hết các trường hợp thực tế:

- **Posterior không có dạng chuẩn**: Chúng ta không biết nó là phân phối gì.
- **Không có hàm `rvs()` sẵn**: Không có công cụ trực tiếp để lấy mẫu.
- **Chỉ biết posterior đến một hằng số**: $$P(\theta \mid D) \propto P(D \mid \theta) P(\theta)$$, không biết $$P(D)$$.

Vậy làm thế nào chúng ta lấy mẫu từ một phân phối mà chúng ta không biết công thức đầy đủ?

Đây chính là câu hỏi mà **Markov Chain Monte Carlo (MCMC)** trả lời. MCMC là một họ các thuật toán cho phép chúng ta lấy mẫu từ posterior ngay cả khi chúng ta chỉ biết nó đến một hằng số nhân.

Trong các bài học tiếp theo, chúng ta sẽ khám phá:
- **Bài 3.2**: Markov Chains - nền tảng toán học của MCMC
- **Bài 3.3**: Metropolis-Hastings - thuật toán MCMC cơ bản nhất
- **Bài 3.4**: Hamiltonian Monte Carlo - thuật toán MCMC hiện đại và hiệu quả
- **Bài 3.5**: MCMC Diagnostics - cách kiểm tra chất lượng mẫu
- **Bài 3.6**: PyMC - công cụ thực hành MCMC trong Python

## Tóm tắt và Kết nối

Trong bài học này, chúng ta đã khám phá nền tảng của tính toán Bayesian hiện đại:

- **Vấn đề**: Tích phân posterior phức tạp, không có công thức đóng, grid approximation bị curse of dimensionality.
- **Giải pháp**: **Sampling** và **phương pháp Monte Carlo** - lấy mẫu từ posterior và sử dụng mẫu để ước lượng.
- **Lý thuyết**: Law of Large Numbers và Central Limit Theorem đảm bảo ước lượng hội tụ và có thể kiểm soát độ chính xác.
- **Ưu điểm**: Không bị curse of dimensionality, linh hoạt, dễ song song hóa.
- **Vấn đề còn lại**: Làm thế nào lấy mẫu từ posterior khi không có công thức đóng? → MCMC!

Sampling không chỉ là một "trick" tính toán; nó là một cách tư duy mạnh mẽ về suy luận thống kê. Thay vì cố gắng tóm tắt posterior bằng một vài con số (như mean, variance), chúng ta có thể **giữ lại toàn bộ phân phối** dưới dạng các mẫu, và sử dụng chúng để trả lời bất kỳ câu hỏi nào về tham số.

Trong bài học tiếp theo, chúng ta sẽ bắt đầu hành trình vào thế giới MCMC, nơi chúng ta học cách tạo ra những mẫu kỳ diệu này.

## Bài tập

**Bài tập 1: Monte Carlo Estimation Cơ bản**
Giả sử posterior là Normal(5, 2²).
(a) Lấy 1000 mẫu từ posterior.
(b) Ước lượng posterior mean, variance, và 95% credible interval từ mẫu.
(c) So sánh với giá trị thực (analytical).
(d) Lặp lại với 10, 100, 10000 mẫu. Quan sát sự hội tụ.

**Bài tập 2: Ước lượng Xác suất**
Sử dụng cùng posterior từ Bài tập 1.
(a) Ước lượng $$P(\theta > 6 \mid D)$$ bằng Monte Carlo.
(b) Ước lượng $$P(4 < \theta < 7 \mid D)$$.
(c) So sánh với giá trị thực tính từ CDF.
(d) Vẽ histogram của mẫu và đánh dấu các vùng xác suất.

**Bài tập 3: Curse of Dimensionality**
(a) Tính số điểm cần thiết cho grid approximation với 100 điểm/chiều cho 1, 2, 5, 10, 20 tham số.
(b) Ước lượng bộ nhớ cần thiết (giả sử mỗi số float64 = 8 bytes).
(c) So sánh với Monte Carlo: 10,000 mẫu cần bao nhiêu bộ nhớ cho mỗi trường hợp?
(d) Giải thích tại sao Monte Carlo khả thi hơn.

**Bài tập 4: Standard Error và Convergence**
Với posterior Beta(9, 5):
(a) Lấy 100 mẫu, tính posterior mean và standard error.
(b) Lặp lại 1000 lần, tạo 1000 ước lượng khác nhau.
(c) Vẽ histogram của 1000 ước lượng. Nó có hình dạng gì?
(d) Tính standard deviation của 1000 ước lượng. So sánh với theoretical SE = $$\sigma/\sqrt{100}$$.

**Bài tập 5: Suy ngẫm về Sampling**
Viết một đoạn văn ngắn (200-300 từ) thảo luận:
(a) Tại sao sampling là "game changer" cho Bayesian statistics?
(b) Ưu điểm của sampling so với grid approximation là gì?
(c) Vấn đề lớn nhất còn lại (hint: làm thế nào lấy mẫu từ posterior phức tạp)?
(d) Bạn nghĩ MCMC sẽ giải quyết vấn đề này như thế nào?

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 10: Introduction to Bayesian computation
- Chapter 11: Basics of Markov chain simulation

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 7: Markov Chain Monte Carlo

### Supplementary Reading:

**McElreath, R. (2020).** *Statistical Rethinking: A Bayesian Course with Examples in R and Stan* (2nd Edition). CRC Press.
- Chapter 9: Markov Chain Monte Carlo

**Robert, C. P., & Casella, G. (2004).** *Monte Carlo Statistical Methods* (2nd Edition). Springer.
- Chapter 3: Monte Carlo Integration

---

*Bài học tiếp theo: [3.2 Markov Chains - Nền tảng Toán học của MCMC](/vi/chapter03/markov-chain/)*
