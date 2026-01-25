---
layout: post
title: "Bài 3.3: Metropolis-Hastings - Thuật toán MCMC Elegant và Mạnh mẽ"
chapter: '03'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter03
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu sâu sắc về **thuật toán Metropolis-Hastings** - một trong những thuật toán elegant và quan trọng nhất trong thống kê tính toán. Bạn sẽ không chỉ biết cách implement thuật toán, mà còn hiểu được ý tưởng thiên tài đằng sau nó: làm thế nào để tạo ra một Markov chain có phân phối dừng chính xác là posterior, ngay cả khi chúng ta chỉ biết posterior đến một hằng số nhân. Bạn sẽ học cách điều chỉnh thuật toán để có hiệu suất tốt và chẩn đoán các vấn đề phổ biến.

## Giới thiệu: Bài toán Tưởng chừng Không thể Giải

Hãy nhớ lại vấn đề chúng ta đang đối mặt:

**Mục tiêu**: Lấy mẫu từ posterior $$P(\theta \mid D)$$

**Những gì chúng ta biết**:
- Likelihood: $$P(D \mid \theta)$$
- Prior: $$P(\theta)$$
- Posterior tỷ lệ với: $$P(\theta \mid D) \propto P(D \mid \theta) P(\theta)$$

**Những gì chúng ta KHÔNG biết**:
- Evidence: $$P(D) = \int P(D \mid \theta) P(\theta) \, d\theta$$ (hằng số chuẩn hóa)
- Cách lấy mẫu trực tiếp từ $$P(\theta \mid D)$$

Trong hầu hết các trường hợp thực tế, posterior có dạng phức tạp: nhiều chiều, multimodal, không có tên gọi. Không có hàm `rvs()` sẵn có. Làm thế nào chúng ta có thể lấy mẫu từ một phân phối mà chúng ta chỉ biết "hình dạng" của nó, không biết chính xác giá trị?

Đây là lúc **Metropolis-Hastings** xuất hiện như một giải pháp thiên tài. Thuật toán này, được phát minh bởi Nicholas Metropolis và cộng sự năm 1953 (và mở rộng bởi W.K. Hastings năm 1970), cho phép chúng ta xây dựng một Markov chain mà:
1. Chỉ cần biết posterior đến một hằng số nhân
2. Có phân phối dừng chính xác là posterior
3. Đơn giản để implement

Đây là một trong những ý tưởng mạnh mẽ nhất trong thống kê tính toán, và nó đã mở ra cánh cửa cho suy diễn Bayesian hiện đại.

## 1. Ý tưởng Cốt lõi: Proposal và Acceptance

![Metropolis-Hastings Algorithm]({{ site.baseurl }}/img/chapter_img/chapter03/metropolis_hastings.png)

Metropolis-Hastings hoạt động theo một nguyên tắc đơn giản nhưng mạnh mẽ: **đề xuất và chấp nhận** (propose and accept).

### 1.1. Quy trình Tổng quát

Giả sử chúng ta đang ở trạng thái hiện tại $$\theta^{(t)}$$. Để tạo ra trạng thái tiếp theo $$\theta^{(t+1)}$$:

**Bước 1: Proposal (Đề xuất)**
- Đề xuất một trạng thái mới $$\theta^*$$ từ một **proposal distribution** (phân phối đề xuất) $$q(\theta^* \mid \theta^{(t)})$$

**Bước 2: Acceptance (Chấp nhận)**
- Tính **acceptance probability** (xác suất chấp nhận):
$$\alpha = \min\left(1, \frac{P(\theta^* \mid D)}{P(\theta^{(t)} \mid D)} \cdot \frac{q(\theta^{(t)} \mid \theta^*)}{q(\theta^* \mid \theta^{(t)})}\right)$$

- Chấp nhận $$\theta^*$$ với xác suất $$\alpha$$:
  - Nếu chấp nhận: $$\theta^{(t+1)} = \theta^*$$
  - Nếu từ chối: $$\theta^{(t+1)} = \theta^{(t)}$$ (ở lại trạng thái cũ)

### 1.2. Tại sao Công thức này Hoạt động?

Điều kỳ diệu ở đây là: **chúng ta không cần biết hằng số chuẩn hóa** $$P(D)$$!

Lý do: Khi tính tỷ lệ posterior, hằng số chuẩn hóa bị triệt tiêu:

$$\frac{P(\theta^* \mid D)}{P(\theta^{(t)} \mid D)} = \frac{P(D \mid \theta^*) P(\theta^*) / P(D)}{P(D \mid \theta^{(t)}) P(\theta^{(t)}) / P(D)} = \frac{P(D \mid \theta^*) P(\theta^*)}{P(D \mid \theta^{(t)}) P(\theta^{(t)})}$$

Chúng ta chỉ cần tính likelihood và prior - những thứ chúng ta biết!

### 1.3. Trực quan: "Đi lên đồi, Đôi khi Đi xuống"

Hãy nghĩ về Metropolis-Hastings như một người leo núi trong sương mù:
- **Proposal**: Đề xuất một bước đi ngẫu nhiên
- **Acceptance**: Quyết định có nên đi hay không
  - Nếu bước đi **lên cao hơn** (posterior cao hơn): **luôn chấp nhận**
  - Nếu bước đi **xuống thấp hơn**: **đôi khi chấp nhận** (tỷ lệ phụ thuộc vào độ giảm)

Việc đôi khi chấp nhận các bước đi xuống là quan trọng - nó cho phép thuật toán khám phá toàn bộ không gian tham số, không bị kẹt ở một đỉnh local.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Minh họa: Trực quan về Metropolis-Hastings
np.random.seed(42)

# Target distribution: Mixture of two Betas (bimodal)
def target_pdf(theta):
    return 0.6 * stats.beta(8, 4).pdf(theta) + 0.4 * stats.beta(4, 8).pdf(theta)

def target_unnormalized(theta):
    # Giả sử đây là posterior chưa chuẩn hóa
    return 0.6 * stats.beta(8, 4).pdf(theta) + 0.4 * stats.beta(4, 8).pdf(theta)

theta_grid = np.linspace(0, 1, 1000)
target_values = target_pdf(theta_grid)

# Vẽ minh họa
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Target distribution
axes[0, 0].plot(theta_grid, target_values, linewidth=3, color='blue')
axes[0, 0].fill_between(theta_grid, target_values, alpha=0.3, color='blue')
axes[0, 0].set_xlabel('θ', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Posterior Density', fontsize=12, fontweight='bold')
axes[0, 0].set_title('Target Posterior (Bimodal)\n' +
                     'Muốn lấy mẫu từ phân phối này',
                     fontsize=14, fontweight='bold')
axes[0, 0].grid(alpha=0.3)

# 2. Proposal và Acceptance
current = 0.3
proposed = 0.7

axes[0, 1].plot(theta_grid, target_values, linewidth=3, color='blue', alpha=0.5)
axes[0, 1].fill_between(theta_grid, target_values, alpha=0.2, color='blue')

# Current state
axes[0, 1].scatter([current], [target_pdf(current)], s=300, color='green', 
                   marker='o', zorder=5, edgecolors='black', linewidths=2,
                   label=f'Current: θ⁽ᵗ⁾ = {current:.2f}')
axes[0, 1].axvline(current, color='green', linestyle='--', alpha=0.5)

# Proposed state
axes[0, 1].scatter([proposed], [target_pdf(proposed)], s=300, color='orange', 
                   marker='*', zorder=5, edgecolors='black', linewidths=2,
                   label=f'Proposed: θ* = {proposed:.2f}')
axes[0, 1].axvline(proposed, color='orange', linestyle='--', alpha=0.5)

# Arrow
axes[0, 1].annotate('', xy=(proposed, target_pdf(proposed)), 
                    xytext=(current, target_pdf(current)),
                    arrowprops=dict(arrowstyle='->', lw=3, color='red'))

ratio = target_pdf(proposed) / target_pdf(current)
accept_prob = min(1, ratio)

axes[0, 1].set_xlabel('θ', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Posterior Density', fontsize=12, fontweight='bold')
axes[0, 1].set_title(f'Proposal và Acceptance\n' +
                     f'Ratio = {ratio:.2f}, Accept Prob = {accept_prob:.2f}',
                     fontsize=14, fontweight='bold')
axes[0, 1].legend(fontsize=11, loc='upper left')
axes[0, 1].grid(alpha=0.3)

# 3. Acceptance Rule
axes[1, 0].axis('off')
rule = f"""
╔═══════════════════════════════════════════════════════════╗
║           METROPOLIS-HASTINGS ACCEPTANCE RULE             ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Current: θ⁽ᵗ⁾ = {current:.2f}                                    ║
║  Proposed: θ* = {proposed:.2f}                                    ║
║                                                           ║
║  ──────────────────────────────────────────────────────  ║
║                                                           ║
║  Bước 1: Tính Ratio                                       ║
║    r = P(θ* \mid D) / P(θ⁽ᵗ⁾ \mid D)                                ║
║      = {ratio:.4f}                                           ║
║                                                           ║
║  Bước 2: Acceptance Probability                           ║
║    α = min(1, r) = {accept_prob:.4f}                             ║
║                                                           ║
║  Bước 3: Quyết định                                       ║
║    • Nếu r ≥ 1 (đi lên): LUÔN chấp nhận                  ║
║    • Nếu r < 1 (đi xuống): Chấp nhận với xác suất r      ║
║                                                           ║
║  ──────────────────────────────────────────────────────  ║
║                                                           ║
║  Trong ví dụ này:                                         ║
║    → r = {ratio:.2f} {'≥' if ratio >= 1 else '<'} 1                                        ║
║    → {'LUÔN chấp nhận!' if ratio >= 1 else f'Chấp nhận với xác suất {ratio:.2f}'}                              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[1, 0].text(0.5, 0.5, rule, fontsize=10, family='monospace',
               ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

# 4. Ý nghĩa
axes[1, 1].axis('off')
meaning = """
╔═══════════════════════════════════════════════════════════╗
║              TẠI SAO CÔNG THỨC NÀY HOẠT ĐỘNG?            ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  1. ĐI LÊN (r ≥ 1): LUÔN chấp nhận                       ║
║     → Di chuyển đến vùng có posterior cao hơn            ║
║     → Hợp lý!                                             ║
║                                                           ║
║  2. ĐI XUỐNG (r < 1): ĐÔI KHI chấp nhận                  ║
║     → Cho phép khám phá không gian tham số                ║
║     → Tránh kẹt ở local maximum                          ║
║     → Xác suất chấp nhận ∝ mức độ giảm                   ║
║                                                           ║
║  ──────────────────────────────────────────────────────  ║
║                                                           ║
║  KẾT QUẢ:                                                 ║
║    • Chuỗi dành nhiều thời gian ở vùng posterior cao     ║
║    • Nhưng vẫn khám phá được toàn bộ không gian          ║
║    • Phân phối dừng = Posterior!                          ║
║                                                           ║
║  ──────────────────────────────────────────────────────  ║
║                                                           ║
║  ĐIỀU KỲ DIỆU:                                            ║
║    → KHÔNG cần biết hằng số chuẩn hóa P(D)!              ║
║    → Chỉ cần tính likelihood và prior!                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[1, 1].text(0.5, 0.5, meaning, fontsize=10, family='monospace',
               ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9))

plt.tight_layout()
plt.show()
```

## 2. Thuật toán Metropolis-Hastings: Công thức Đầy đủ

Bây giờ hãy viết ra thuật toán một cách chính xác:

### 2.1. Thuật toán Tổng quát

**Input**:
- Target distribution (posterior): $$P(\theta \mid D) \propto P(D \mid \theta) P(\theta)$$
- Proposal distribution: $$q(\theta^* \mid \theta^{(t)})$$
- Số mẫu: $$S$$
- Điểm khởi đầu: $$\theta^{(0)}$$

**Output**:
- Chuỗi mẫu: $$\theta^{(1)}, \theta^{(2)}, \ldots, \theta^{(S)}$$

**Quy trình**:

```
For t = 0 to S-1:
    1. Proposal: Sample θ* ~ q(· | θ⁽ᵗ⁾)
    
    2. Compute acceptance ratio:
       r = [P(D \mid θ*) P(θ*) / P(D \mid θ⁽ᵗ⁾) P(θ⁽ᵗ⁾)] × [q(θ⁽ᵗ⁾ \mid θ*) / q(θ* \mid θ⁽ᵗ⁾)]
    
    3. Compute acceptance probability:
       α = min(1, r)
    
    4. Accept or reject:
       u ~ Uniform(0, 1)
       If u < α:
           θ⁽ᵗ⁺¹⁾ = θ*     (accept)
       Else:
           θ⁽ᵗ⁺¹⁾ = θ⁽ᵗ⁾   (reject, stay)
```

### 2.2. Metropolis Algorithm: Trường hợp Đặc biệt

Khi proposal distribution là **symmetric** (đối xứng), tức là:

$$q(\theta^* \mid \theta^{(t)}) = q(\theta^{(t)} \mid \theta^*)$$

Thì tỷ lệ proposal bị triệt tiêu, và acceptance ratio đơn giản hóa thành:

$$r = \frac{P(\theta^* \mid D)}{P(\theta^{(t)} \mid D)}$$

Đây là **Metropolis algorithm** - phiên bản đơn giản hơn của Metropolis-Hastings.

**Ví dụ proposal symmetric**: Normal distribution centered tại trạng thái hiện tại:
$$q(\theta^* \mid \theta^{(t)}) = \mathcal{N}(\theta^{(t)}, \sigma^2)$$

## 3. Implementation: Từ Lý thuyết đến Code

Hãy implement Metropolis-Hastings từ đầu để hiểu rõ cách nó hoạt động.

### 3.1. Ví dụ Đơn giản: Beta Posterior

Trước tiên, hãy thử với một posterior đơn giản mà chúng ta biết câu trả lời (Beta), để kiểm tra thuật toán.

```python
# Ví dụ: Beta posterior (Beta-Binomial)
# Data: 7 heads in 10 flips
# Prior: Beta(2, 2)
# Posterior: Beta(9, 5) - chúng ta biết đây là câu trả lời đúng!

def log_posterior_beta(theta, alpha=9, beta=5):
    """Log posterior (unnormalized)"""
    if theta <= 0 or theta >= 1:
        return -np.inf
    return (alpha - 1) * np.log(theta) + (beta - 1) * np.log(1 - theta)

def metropolis_hastings(log_posterior, initial, n_samples, proposal_sd=0.1):
    """
    Metropolis-Hastings with symmetric Normal proposal
    
    Parameters:
    -----------
    log_posterior : function
        Log of unnormalized posterior
    initial : float
        Starting value
    n_samples : int
        Number of samples to generate
    proposal_sd : float
        Standard deviation of proposal distribution
    
    Returns:
    --------
    samples : array
        MCMC samples
    acceptance_rate : float
        Proportion of accepted proposals
    """
    samples = np.zeros(n_samples)
    samples[0] = initial
    n_accepted = 0
    
    for t in range(n_samples - 1):
        # Current state
        current = samples[t]
        
        # Step 1: Proposal (symmetric Normal)
        proposed = current + np.random.normal(0, proposal_sd)
        
        # Step 2: Compute log acceptance ratio
        log_r = log_posterior(proposed) - log_posterior(current)
        # Note: proposal ratio = 1 (symmetric)
        
        # Step 3: Acceptance probability
        log_alpha = min(0, log_r)  # log(min(1, r))
        
        # Step 4: Accept or reject
        if np.log(np.random.uniform()) < log_alpha:
            samples[t + 1] = proposed  # Accept
            n_accepted += 1
        else:
            samples[t + 1] = current  # Reject
    
    acceptance_rate = n_accepted / (n_samples - 1)
    return samples, acceptance_rate

# Run Metropolis-Hastings
np.random.seed(42)
n_samples_mh = 10000
initial_value = 0.5

samples_mh, accept_rate = metropolis_hastings(
    log_posterior_beta, 
    initial_value, 
    n_samples_mh, 
    proposal_sd=0.1
)

# True posterior
true_posterior = stats.beta(9, 5)

# Vẽ kết quả
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Trace plot
axes[0, 0].plot(samples_mh[:500], linewidth=1, alpha=0.7, color='blue')
axes[0, 0].axhline(true_posterior.mean(), color='red', linestyle='--', linewidth=2,
                   label=f'True Mean = {true_posterior.mean():.3f}')
axes[0, 0].set_xlabel('Iteration', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('θ', fontsize=12, fontweight='bold')
axes[0, 0].set_title(f'Trace Plot (first 500 iterations)\n' +
                     f'Acceptance Rate = {accept_rate:.2%}',
                     fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=11)
axes[0, 0].grid(alpha=0.3)

# 2. Histogram vs True posterior
burn_in = 1000
axes[0, 1].hist(samples_mh[burn_in:], bins=50, density=True, alpha=0.7,
                color='skyblue', edgecolor='black', label='MCMC Samples')
axes[0, 1].plot(theta_grid, true_posterior.pdf(theta_grid), linewidth=3,
                color='red', label='True Posterior: Beta(9,5)')
axes[0, 1].set_xlabel('θ', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0, 1].set_title(f'Posterior Distribution (after burn-in={burn_in})\n' +
                     'MCMC samples ≈ True posterior!',
                     fontsize=14, fontweight='bold')
axes[0, 1].legend(fontsize=11)
axes[0, 1].grid(alpha=0.3, axis='y')

# 3. Running mean
running_mean = np.cumsum(samples_mh) / np.arange(1, n_samples_mh + 1)
axes[1, 0].plot(running_mean, linewidth=2, color='blue', label='Running Mean')
axes[1, 0].axhline(true_posterior.mean(), color='red', linestyle='--', linewidth=2,
                   label=f'True Mean = {true_posterior.mean():.3f}')
axes[1, 0].set_xlabel('Iteration', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Running Mean', fontsize=12, fontweight='bold')
axes[1, 0].set_title('Convergence of Posterior Mean\n' +
                     'Running mean hội tụ về true mean',
                     fontsize=14, fontweight='bold')
axes[1, 0].legend(fontsize=11)
axes[1, 0].grid(alpha=0.3)
axes[1, 0].set_xlim(0, n_samples_mh)

# 4. Autocorrelation
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(samples_mh[burn_in:], lags=50, ax=axes[1, 1], alpha=0.05)
axes[1, 1].set_xlabel('Lag', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Autocorrelation', fontsize=12, fontweight='bold')
axes[1, 1].set_title('Autocorrelation Plot\n' +
                     'Mẫu có autocorrelation (phụ thuộc)',
                     fontsize=14, fontweight='bold')
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("=" * 70)
print("METROPOLIS-HASTINGS RESULTS")
print("=" * 70)
print(f"Number of samples: {n_samples_mh}")
print(f"Burn-in: {burn_in}")
print(f"Acceptance rate: {accept_rate:.2%}")
print(f"\nPosterior Mean:")
print(f"  MCMC estimate: {np.mean(samples_mh[burn_in:]):.4f}")
print(f"  True value:    {true_posterior.mean():.4f}")
print(f"  Error:         {abs(np.mean(samples_mh[burn_in:]) - true_posterior.mean()):.4f}")
print(f"\nPosterior SD:")
print(f"  MCMC estimate: {np.std(samples_mh[burn_in:]):.4f}")
print(f"  True value:    {true_posterior.std():.4f}")
print(f"\n→ Metropolis-Hastings HOẠT ĐỘNG!")
print("=" * 70)
```

### 3.2. Ví dụ Phức tạp hơn: Bimodal Posterior

Bây giờ hãy thử với một posterior phức tạp hơn - bimodal (hai đỉnh):

```python
# Bimodal posterior: Mixture of two Betas
def log_posterior_bimodal(theta):
    """Log of unnormalized bimodal posterior"""
    if theta <= 0 or theta >= 1:
        return -np.inf
    
    # Mixture: 0.6 * Beta(8,4) + 0.4 * Beta(4,8)
    p1 = stats.beta(8, 4).pdf(theta)
    p2 = stats.beta(4, 8).pdf(theta)
    mixture = 0.6 * p1 + 0.4 * p2
    
    return np.log(mixture + 1e-10)  # Add small constant to avoid log(0)

# Run MH
samples_bimodal, accept_rate_bimodal = metropolis_hastings(
    log_posterior_bimodal,
    initial_value=0.5,
    n_samples=20000,
    proposal_sd=0.1
)

# True bimodal posterior
def true_bimodal_pdf(theta):
    return 0.6 * stats.beta(8, 4).pdf(theta) + 0.4 * stats.beta(4, 8).pdf(theta)

# Vẽ
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Trace plot
axes[0].plot(samples_bimodal[:1000], linewidth=1, alpha=0.7, color='blue')
axes[0].set_xlabel('Iteration', fontsize=12, fontweight='bold')
axes[0].set_ylabel('θ', fontsize=12, fontweight='bold')
axes[0].set_title(f'Trace Plot: Bimodal Posterior\n' +
                  f'Chuỗi "nhảy" giữa hai modes',
                  fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)

# Histogram
burn_in_bi = 2000
axes[1].hist(samples_bimodal[burn_in_bi:], bins=60, density=True, alpha=0.7,
             color='skyblue', edgecolor='black', label='MCMC Samples')
axes[1].plot(theta_grid, true_bimodal_pdf(theta_grid), linewidth=3,
             color='red', label='True Bimodal Posterior')
axes[1].set_xlabel('θ', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title(f'Bimodal Posterior Distribution\n' +
                  f'Acceptance Rate = {accept_rate_bimodal:.2%}',
                  fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print(f"\nBimodal Posterior:")
print(f"  Acceptance rate: {accept_rate_bimodal:.2%}")
print(f"  → MH có thể handle posterior phức tạp (bimodal)!")
```

## 4. Tuning Metropolis-Hastings: Proposal Distribution

Hiệu suất của Metropolis-Hastings phụ thuộc rất nhiều vào **proposal distribution**. Nếu proposal quá hẹp hoặc quá rộng, thuật toán sẽ không hiệu quả.

### 4.1. Acceptance Rate: Chỉ số Quan trọng

**Acceptance rate** (tỷ lệ chấp nhận) là tỷ lệ các proposal được chấp nhận.

- **Acceptance rate quá cao (> 90%)**: Proposal quá hẹp, chuỗi di chuyển chậm (slow mixing)
- **Acceptance rate quá thấp (< 10%)**: Proposal quá rộng, nhiều proposal bị từ chối, chuỗi ít di chuyển
- **Acceptance rate lý tưởng**: Khoảng **20-50%** (theo kinh nghiệm)

```python
# So sánh các proposal khác nhau
proposal_sds = [0.01, 0.05, 0.1, 0.5, 1.0]
results = {}

for sd in proposal_sds:
    samples, accept_rate = metropolis_hastings(
        log_posterior_beta,
        initial_value=0.5,
        n_samples=5000,
        proposal_sd=sd
    )
    results[sd] = {'samples': samples, 'accept_rate': accept_rate}

# Vẽ so sánh
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

for idx, sd in enumerate(proposal_sds):
    row = idx // 3
    col = idx % 3
    
    samples = results[sd]['samples']
    accept_rate = results[sd]['accept_rate']
    
    # Trace plot
    axes[row, col].plot(samples[:500], linewidth=1, alpha=0.7)
    axes[row, col].set_title(f'Proposal SD = {sd}\n' +
                             f'Accept Rate = {accept_rate:.2%}',
                             fontsize=12, fontweight='bold')
    axes[row, col].set_xlabel('Iteration', fontsize=10)
    axes[row, col].set_ylabel('θ', fontsize=10)
    axes[row, col].grid(alpha=0.3)
    
    # Color code by acceptance rate
    if accept_rate < 0.15 or accept_rate > 0.8:
        axes[row, col].set_facecolor('#ffcccc')  # Red tint - not good
    else:
        axes[row, col].set_facecolor('#ccffcc')  # Green tint - good

# Hide last subplot
axes[1, 2].axis('off')
explanation = """
TUNING PROPOSAL DISTRIBUTION:

• SD quá nhỏ (0.01):
  → Accept rate quá cao
  → Chuỗi di chuyển CHẬM

• SD quá lớn (1.0):
  → Accept rate quá thấp
  → Nhiều proposal bị TỪ CHỐI

• SD vừa phải (0.05-0.1):
  → Accept rate lý tưởng (20-50%)
  → Chuỗi di chuyển HIỆU QUẢ
"""
axes[1, 2].text(0.5, 0.5, explanation, fontsize=11, family='monospace',
       ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.show()

print("\nSO SÁNH CÁC PROPOSAL SD:")
print("=" * 70)
print(f"{'Proposal SD':<15} {'Accept Rate':<15} {'Đánh giá'}")
print("=" * 70)
for sd in proposal_sds:
    accept_rate = results[sd]['accept_rate']
    if accept_rate < 0.15:
        assessment = "❌ Quá thấp (proposal quá rộng)"
    elif accept_rate > 0.8:
        assessment = "❌ Quá cao (proposal quá hẹp)"
    else:
        assessment = "✓ Tốt!"
    print(f"{sd:<15} {accept_rate:<15.2%} {assessment}")
print("=" * 70)
```

### 4.2. Adaptive Metropolis

Một cải tiến của Metropolis-Hastings là **Adaptive Metropolis**, tự động điều chỉnh proposal distribution dựa trên acceptance rate.

Ý tưởng:
- Nếu acceptance rate quá cao: tăng proposal SD
- Nếu acceptance rate quá thấp: giảm proposal SD

(Chúng ta sẽ không implement chi tiết ở đây, nhưng đây là một kỹ thuật quan trọng trong thực tế)

## Tóm tắt và Kết nối

Metropolis-Hastings là một thuật toán elegant và mạnh mẽ:

- **Ý tưởng**: Propose và accept - đi lên luôn chấp nhận, đi xuống đôi khi chấp nhận
- **Điều kỳ diệu**: Chỉ cần biết posterior đến một hằng số nhân
- **Detailed balance**: Đảm bảo phân phối dừng = posterior
- **Implementation**: Đơn giản, có thể code từ đầu
- **Tuning**: Acceptance rate lý tưởng khoảng 20-50%

Metropolis-Hastings là nền tảng cho nhiều thuật toán MCMC hiện đại hơn. Trong các bài tiếp theo, chúng ta sẽ học:
- **Hamiltonian Monte Carlo**: Sử dụng gradient để di chuyển hiệu quả hơn
- **MCMC Diagnostics**: Cách kiểm tra chất lượng mẫu
- **PyMC**: Công cụ thực hành MCMC trong Python

## Bài tập

**Bài tập 1: Implement Metropolis-Hastings**
(a) Implement MH từ đầu cho posterior Beta(5, 2).
(b) Chạy với 10,000 mẫu, proposal SD = 0.1.
(c) Vẽ trace plot, histogram, và so sánh với true posterior.
(d) Tính posterior mean và 95% credible interval.

**Bài tập 2: Tuning Proposal**
Sử dụng cùng posterior từ Bài tập 1.
(a) Thử các proposal SD: 0.01, 0.05, 0.1, 0.3, 0.5.
(b) Tính acceptance rate cho mỗi trường hợp.
(c) Vẽ trace plots và so sánh.
(d) Proposal SD nào tốt nhất? Tại sao?

**Bài tập 3: Bimodal Posterior**
Implement MH cho posterior: 0.5 * Beta(3,8) + 0.5 * Beta(8,3).
(a) Chạy với 20,000 mẫu.
(b) Vẽ trace plot. Chuỗi có "nhảy" giữa hai modes không?
(c) Nếu không, thử tăng proposal SD.
(d) Tính tỷ lệ mẫu ở mỗi mode. So sánh với true weights (0.5, 0.5).

**Bài tập 4: Burn-in**
(a) Chạy MH với initial value = 0.1 (xa true mean).
(b) Vẽ running mean theo iteration.
(c) Ước lượng burn-in period cần thiết.
(d) So sánh posterior mean với và không có burn-in.

**Bài tập 5: Suy ngẫm về MH**
Viết một đoạn văn ngắn (200-300 từ) thảo luận:
(a) Tại sao MH là "elegant"? Điều kỳ diệu của nó là gì?
(b) Ưu điểm và nhược điểm của MH so với sampling trực tiếp?
(c) Thách thức lớn nhất khi sử dụng MH trong thực tế là gì?

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 11: Basics of Markov chain simulation
- Chapter 12: Computationally efficient Markov chain simulation

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 7: Markov Chain Monte Carlo

### Supplementary Reading:

**Robert, C. P., & Casella, G. (2004).** *Monte Carlo Statistical Methods* (2nd Edition). Springer.
- Chapter 7: The Metropolis-Hastings Algorithm

**Metropolis, N., Rosenbluth, A. W., Rosenbluth, M. N., Teller, A. H., & Teller, E. (1953).** *Equation of state calculations by fast computing machines*. The Journal of Chemical Physics, 21(6), 1087-1092.
- Bài báo gốc giới thiệu Metropolis algorithm

**Hastings, W. K. (1970).** *Monte Carlo sampling methods using Markov chains and their applications*. Biometrika, 57(1), 97-109.
- Bài báo mở rộng thành Metropolis-Hastings

---

*Bài học tiếp theo: [3.4 Hamiltonian Monte Carlo - MCMC Hiện đại](/vi/chapter03/hamiltonian-monte-carlo/)*
