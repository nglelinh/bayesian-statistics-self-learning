---
layout: post
title: "Bài 3.5: MCMC Diagnostics - Đảm bảo Chất lượng Mẫu"
chapter: '03'
order: 5
owner: Nguyen Le Linh
lang: vi
categories:
- chapter03
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ biết cách **chẩn đoán chất lượng mẫu MCMC** - một kỹ năng thiết yếu trong thực hành Bayesian. Bạn sẽ học cách nhận biết các vấn đề phổ biến (convergence issues, high autocorrelation, poor mixing) thông qua các công cụ chẩn đoán như trace plots, R-hat, và Effective Sample Size. Quan trọng hơn, bạn sẽ hiểu **tại sao** các vấn đề này xảy ra và **làm thế nào** để khắc phục chúng.

## Giới thiệu: Vấn đề của "Tin tưởng Mù quáng"

Hãy tưởng tượng bạn vừa chạy xong một thuật toán MCMC với 10,000 mẫu. Bạn tính posterior mean, vẽ histogram, và cảm thấy hài lòng với kết quả. Nhưng có một câu hỏi quan trọng:

**Làm sao bạn biết các mẫu này đáng tin cậy?**

MCMC không phải là phép màu. Nó có thể thất bại theo nhiều cách:
- Chuỗi chưa hội tụ về posterior
- Chuỗi bị kẹt ở một vùng nhỏ của không gian tham số
- Các mẫu có autocorrelation cao, không đủ độc lập
- Proposal distribution không phù hợp

Nếu bạn không kiểm tra, bạn có thể đưa ra kết luận sai lầm dựa trên mẫu kém chất lượng. Đây là lý do tại sao **MCMC diagnostics** (chẩn đoán MCMC) là một phần không thể thiếu trong workflow Bayesian.

Trong bài này, chúng ta sẽ học các công cụ chẩn đoán chính:
1. **Trace plots**: Visual inspection
2. **R-hat**: Convergence diagnostic
3. **Effective Sample Size (ESS)**: Đo lường độc lập của mẫu
4. **Autocorrelation**: Phụ thuộc giữa các mẫu
5. **Multiple chains**: Kiểm tra robustness

## 1. Trace Plots: Visual Inspection

![MCMC Diagnostics: Good vs Bad Traces]({{ site.baseurl }}/img/chapter_img/chapter03/mcmc_diagnostics.png)

**Trace plot** là công cụ chẩn đoán đơn giản nhưng cực kỳ hữu ích. Nó vẽ giá trị của tham số theo iteration.

### 1.1. "Fuzzy Caterpillar" - Dấu hiệu Tốt

Một trace plot tốt trông giống như một **"fuzzy caterpillar"** (con sâu bướm lông xù):
- Dao động ngẫu nhiên quanh một giá trị trung bình
- Không có xu hướng (trend)
- Khám phá đều không gian tham số
- Stationary (phân phối không thay đổi theo thời gian)

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Minh họa các loại trace plots
np.random.seed(42)

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# 1. GOOD: Fuzzy caterpillar
good_chain = np.random.normal(0.7, 0.05, 1000)
axes[0, 0].plot(good_chain, linewidth=1, alpha=0.7, color='blue')
axes[0, 0].axhline(0.7, color='red', linestyle='--', linewidth=2, alpha=0.5)
axes[0, 0].set_title('✓ TỐT: Fuzzy Caterpillar', 
                     fontsize=13, fontweight='bold', color='green')
axes[0, 0].set_xlabel('Iteration', fontsize=11)
axes[0, 0].set_ylabel('θ', fontsize=11)
axes[0, 0].grid(alpha=0.3)

# 2. BAD: Trend (chưa hội tụ)
trend_chain = np.linspace(0.3, 0.9, 1000) + np.random.normal(0, 0.02, 1000)
axes[0, 1].plot(trend_chain, linewidth=1, alpha=0.7, color='red')
axes[0, 1].set_title('✗ XẤU: Trend (Chưa hội tụ)', 
                     fontsize=13, fontweight='bold', color='red')
axes[0, 1].set_xlabel('Iteration', fontsize=11)
axes[0, 1].set_ylabel('θ', fontsize=11)
axes[0, 1].grid(alpha=0.3)

# 3. BAD: Stuck (bị kẹt)
stuck_chain = np.concatenate([
    np.ones(400) * 0.3 + np.random.normal(0, 0.01, 400),
    np.ones(200) * 0.8 + np.random.normal(0, 0.01, 200),
    np.ones(400) * 0.3 + np.random.normal(0, 0.01, 400)
])
axes[0, 2].plot(stuck_chain, linewidth=1, alpha=0.7, color='red')
axes[0, 2].set_title('✗ XẤU: Stuck (Bị kẹt)', 
                     fontsize=13, fontweight='bold', color='red')
axes[0, 2].set_xlabel('Iteration', fontsize=11)
axes[0, 2].set_ylabel('θ', fontsize=11)
axes[0, 2].grid(alpha=0.3)

# Giải thích
explanations = [
"""
✓ FUZZY CATERPILLAR

Dấu hiệu tốt:
  • Dao động ngẫu nhiên
  • Không có xu hướng
  • Khám phá đều
  • Stationary

→ Chuỗi đã hội tụ!
→ Có thể tin tưởng mẫu
""",
"""
✗ TREND

Vấn đề:
  • Có xu hướng tăng/giảm
  • Chưa đạt stationary
  • Chưa hội tụ về posterior

Giải pháp:
  → Chạy thêm iterations
  → Tăng burn-in period
  → Kiểm tra initial values
""",
"""
✗ STUCK

Vấn đề:
  • Bị kẹt ở một vùng
  • Không khám phá đủ
  • Poor mixing

Giải pháp:
  → Tăng proposal SD (MH)
  → Dùng HMC thay vì MH
  → Kiểm tra model specification
"""
]

colors = ['lightgreen', '#ffcccc', '#ffcccc']
for i, (ax, exp, color) in enumerate(zip(axes[1, :], explanations, colors)):
    ax.axis('off')
    ax.text(0.5, 0.5, exp, ha='center', va='center', 
            fontsize=10, family='monospace',
            bbox=dict(boxstyle='round', facecolor=color, alpha=0.9))

plt.tight_layout()
plt.show()

print("=" * 70)
print("TRACE PLOT DIAGNOSTICS")
print("=" * 70)
print("\n✓ TỐT (Fuzzy Caterpillar):")
print("  - Chuỗi dao động ngẫu nhiên quanh mean")
print("  - Stationary, đã hội tụ")
print("\n✗ XẤU (Trend):")
print("  - Có xu hướng → chưa hội tụ")
print("  - Cần chạy thêm iterations")
print("\n✗ XẤU (Stuck):")
print("  - Bị kẹt → poor mixing")
print("  - Cần điều chỉnh thuật toán")
print("=" * 70)
```

### 1.2. Ví dụ Thực tế: So sánh MH với Proposal khác nhau

```python
# Posterior: Beta(9, 5)
def log_posterior(theta):
    if theta <= 0 or theta >= 1:
        return -np.inf
    return 8 * np.log(theta) + 4 * np.log(1 - theta)

def metropolis_hastings(log_posterior, initial, n_samples, proposal_sd):
    samples = np.zeros(n_samples)
    samples[0] = initial
    n_accepted = 0
    
    for t in range(n_samples - 1):
        current = samples[t]
        proposed = current + np.random.normal(0, proposal_sd)
        
        log_r = log_posterior(proposed) - log_posterior(current)
        
        if np.log(np.random.uniform()) < log_r:
            samples[t + 1] = proposed
            n_accepted += 1
        else:
            samples[t + 1] = current
    
    return samples, n_accepted / (n_samples - 1)

# Chạy với proposal SD khác nhau
np.random.seed(42)
n_samples = 2000

chains = {}
for sd in [0.01, 0.1, 0.5]:
    samples, acc_rate = metropolis_hastings(log_posterior, 0.5, n_samples, sd)
    chains[sd] = {'samples': samples, 'acc_rate': acc_rate}

# Vẽ trace plots
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, sd in enumerate([0.01, 0.1, 0.5]):
    samples = chains[sd]['samples']
    acc_rate = chains[sd]['acc_rate']
    
    axes[idx].plot(samples, linewidth=1, alpha=0.7)
    axes[idx].axhline(stats.beta(9, 5).mean(), color='red', 
                      linestyle='--', linewidth=2, alpha=0.5, label='True Mean')
    axes[idx].set_title(f'Proposal SD = {sd}\nAccept Rate = {acc_rate:.2%}',
                       fontsize=12, fontweight='bold')
    axes[idx].set_xlabel('Iteration', fontsize=11)
    axes[idx].set_ylabel('θ', fontsize=11)
    axes[idx].legend(fontsize=10)
    axes[idx].grid(alpha=0.3)
    
    # Color code
    if 0.2 <= acc_rate <= 0.5:
        axes[idx].set_facecolor('#e8f5e9')  # Green tint - good
    else:
        axes[idx].set_facecolor('#ffebee')  # Red tint - not ideal

plt.tight_layout()
plt.show()

print("\nSO SÁNH PROPOSAL SD:")
print("-" * 70)
for sd in [0.01, 0.1, 0.5]:
    acc_rate = chains[sd]['acc_rate']
    if 0.2 <= acc_rate <= 0.5:
        status = "✓ TỐT"
    else:
        status = "✗ CẦN CẢI THIỆN"
    print(f"SD = {sd:4.2f} | Accept Rate = {acc_rate:.2%} | {status}")
```

## 2. R-hat (Gelman-Rubin Statistic): Convergence Diagnostic

![Convergence Diagnostics: R-hat & ESS]({{ site.baseurl }}/img/chapter_img/chapter03/convergence_diagnostics.png)

**R-hat** (còn gọi là Gelman-Rubin statistic hoặc potential scale reduction factor) là một trong những convergence diagnostic quan trọng nhất.

### 2.1. Ý tưởng: So sánh Within-chain vs Between-chain Variance

R-hat dựa trên ý tưởng đơn giản nhưng mạnh mẽ:

**Nếu chuỗi đã hội tụ**: Variance giữa các chains (between-chain) ≈ Variance trong mỗi chain (within-chain)

**Nếu chuỗi chưa hội tụ**: Between-chain variance > Within-chain variance (các chains ở các vùng khác nhau)

### 2.2. Công thức R-hat

Giả sử chúng ta có $$M$$ chains, mỗi chain có $$N$$ mẫu (sau burn-in).

**Within-chain variance**:
$$W = \frac{1}{M} \sum_{m=1}^{M} s_m^2$$

Trong đó $$s_m^2$$ là variance của chain $$m$$.

**Between-chain variance**:
$$B = \frac{N}{M-1} \sum_{m=1}^{M} (\bar{\theta}_m - \bar{\theta})^2$$

Trong đó $$\bar{\theta}_m$$ là mean của chain $$m$$, $$\bar{\theta}$$ là overall mean.

**R-hat**:
$$\hat{R} = \sqrt{\frac{\frac{N-1}{N}W + \frac{1}{N}B}{W}}$$

### 2.3. Diễn giải R-hat

- **R-hat ≈ 1.0**: Các chains đã hội tụ ✓
- **R-hat > 1.01**: Cảnh báo, có thể chưa hội tụ ⚠️
- **R-hat > 1.1**: Chưa hội tụ, không nên tin tưởng mẫu ✗

**Quy tắc thực hành**: R-hat < 1.01 cho tất cả các tham số.

```python
# Implement R-hat
def compute_rhat(chains):
    """
    Compute R-hat for multiple chains
    
    Parameters:
    -----------
    chains : list of arrays
        List of MCMC chains (each is 1D array)
    
    Returns:
    --------
    rhat : float
        R-hat statistic
    """
    M = len(chains)  # Number of chains
    N = len(chains[0])  # Length of each chain
    
    # Chain means
    chain_means = np.array([np.mean(chain) for chain in chains])
    overall_mean = np.mean(chain_means)
    
    # Within-chain variance
    W = np.mean([np.var(chain, ddof=1) for chain in chains])
    
    # Between-chain variance
    B = N / (M - 1) * np.sum((chain_means - overall_mean)**2)
    
    # Variance estimate
    var_plus = ((N - 1) / N) * W + (1 / N) * B
    
    # R-hat
    rhat = np.sqrt(var_plus / W)
    
    return rhat

# Ví dụ: Chạy 4 chains với initial values khác nhau
np.random.seed(42)
n_chains = 4
n_samples = 2000
initial_values = [0.2, 0.4, 0.6, 0.8]

chains_list = []
for init in initial_values:
    samples, _ = metropolis_hastings(log_posterior, init, n_samples, proposal_sd=0.1)
    chains_list.append(samples[500:])  # Discard burn-in

# Compute R-hat
rhat = compute_rhat(chains_list)

# Vẽ
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# Trace plots của tất cả chains
for i, chain in enumerate(chains_list):
    axes[0].plot(chain, linewidth=1, alpha=0.7, label=f'Chain {i+1}')
axes[0].axhline(stats.beta(9, 5).mean(), color='red', 
               linestyle='--', linewidth=2, alpha=0.5, label='True Mean')
axes[0].set_xlabel('Iteration (after burn-in)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('θ', fontsize=12, fontweight='bold')
axes[0].set_title(f'Multiple Chains\nR-hat = {rhat:.4f}', 
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=10, ncol=2)
axes[0].grid(alpha=0.3)

# Histograms của tất cả chains
for i, chain in enumerate(chains_list):
    axes[1].hist(chain, bins=30, alpha=0.5, density=True, label=f'Chain {i+1}')
theta_grid = np.linspace(0, 1, 1000)
axes[1].plot(theta_grid, stats.beta(9, 5).pdf(theta_grid), 
            'r-', linewidth=3, label='True Posterior')
axes[1].set_xlabel('θ', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('Posterior Distributions\nTất cả chains nên giống nhau', 
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=10)
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("=" * 70)
print("R-HAT DIAGNOSTIC")
print("=" * 70)
print(f"\nR-hat = {rhat:.4f}")
if rhat < 1.01:
    print("✓ TỐT: Các chains đã hội tụ!")
elif rhat < 1.1:
    print("⚠ CẢNH BÁO: Có thể chưa hội tụ, cần kiểm tra thêm")
else:
    print("✗ XẤU: Chưa hội tụ, không nên tin tưởng mẫu!")
print("\nQuy tắc: R-hat < 1.01 cho tất cả tham số")
print("=" * 70)
```

## 3. Effective Sample Size (ESS): Đo lường Độc lập

MCMC samples không phải là independent samples - chúng có **autocorrelation** (tương quan với chính nó ở các lag khác nhau). Điều này có nghĩa là 10,000 MCMC samples không "đáng giá" bằng 10,000 independent samples.

**Effective Sample Size (ESS)** đo lường số lượng **independent samples tương đương** mà MCMC samples cung cấp.

### 3.1. Công thức ESS

$$\text{ESS} = \frac{N}{1 + 2\sum_{k=1}^{\infty} \rho_k}$$

Trong đó:
- $$N$$: Số mẫu MCMC
- $$\rho_k$$: Autocorrelation tại lag $$k$$

**Diễn giải**:
- **ESS ≈ N**: Mẫu gần như độc lập ✓
- **ESS << N**: Mẫu có autocorrelation cao, cần nhiều mẫu hơn ⚠️

**Quy tắc thực hành**: ESS > 400 cho inference đáng tin cậy.

```python
# Compute ESS
def compute_ess(chain):
    """
    Compute Effective Sample Size
    
    Parameters:
    -----------
    chain : array
        MCMC chain
    
    Returns:
    --------
    ess : float
        Effective sample size
    """
    N = len(chain)
    
    # Compute autocorrelation
    mean = np.mean(chain)
    var = np.var(chain)
    
    # Autocorrelation function
    acf = np.correlate(chain - mean, chain - mean, mode='full')[N-1:] / (var * N)
    
    # Sum until autocorrelation becomes negligible
    # (or use a cutoff)
    max_lag = min(N // 2, 100)
    rho_sum = np.sum(acf[1:max_lag])
    
    ess = N / (1 + 2 * rho_sum)
    
    return ess

# So sánh ESS với proposal SD khác nhau
print("\n" + "=" * 70)
print("EFFECTIVE SAMPLE SIZE (ESS)")
print("=" * 70)
print(f"\n{'Proposal SD':<15} {'Accept Rate':<15} {'ESS':<10} {'ESS/N':<10} {'Đánh giá'}")
print("-" * 70)

for sd in [0.01, 0.1, 0.5]:
    samples = chains[sd]['samples'][500:]  # After burn-in
    acc_rate = chains[sd]['acc_rate']
    ess = compute_ess(samples)
    ess_ratio = ess / len(samples)
    
    if ess_ratio > 0.5:
        assessment = "✓ Tốt"
    elif ess_ratio > 0.2:
        assessment = "⚠ Chấp nhận được"
    else:
        assessment = "✗ Kém"
    
    print(f"{sd:<15.2f} {acc_rate:<15.2%} {ess:<10.0f} {ess_ratio:<10.2%} {assessment}")

print("\nQuy tắc: ESS > 400 cho inference đáng tin cậy")
print("=" * 70)
```

## 4. Autocorrelation: Phụ thuộc giữa Mẫu

**Autocorrelation** đo lường mức độ tương quan giữa $$\theta^{(t)}$$ và $$\theta^{(t+k)}$$ (với lag $$k$$).

### 4.1. Autocorrelation Function (ACF)

$$\rho_k = \frac{\text{Cov}(\theta^{(t)}, \theta^{(t+k)})}{\text{Var}(\theta^{(t)})}$$

**Diễn giải**:
- $$\rho_0 = 1$$: Luôn luôn (correlation với chính nó)
- $$\rho_k \to 0$$ nhanh: Low autocorrelation, mẫu gần độc lập ✓
- $$\rho_k \to 0$$ chậm: High autocorrelation, cần nhiều mẫu hơn ⚠️

```python
from statsmodels.graphics.tsaplots import plot_acf

# Vẽ autocorrelation
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, sd in enumerate([0.01, 0.1, 0.5]):
    samples = chains[sd]['samples'][500:]
    
    plot_acf(samples, lags=50, ax=axes[idx], alpha=0.05)
    axes[idx].set_title(f'Autocorrelation\nProposal SD = {sd}',
                       fontsize=12, fontweight='bold')
    axes[idx].set_xlabel('Lag', fontsize=11)
    axes[idx].set_ylabel('Autocorrelation', fontsize=11)
    axes[idx].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\nAUTOCORRELATION ANALYSIS:")
print("-" * 70)
print("• SD = 0.01: High autocorrelation → Proposal quá nhỏ")
print("• SD = 0.1:  Low autocorrelation  → Tốt!")
print("• SD = 0.5:  Medium autocorrelation → Chấp nhận được")
```

## 5. Burn-in Period: Loại bỏ Giai đoạn Khởi động

**Burn-in** (hay warm-up) là giai đoạn đầu của chuỗi MCMC, khi chuỗi chưa hội tụ về posterior.

### 5.1. Tại sao cần Burn-in?

- Initial value có thể xa true posterior
- Chuỗi cần thời gian để "tìm" vùng high posterior
- Mẫu trong giai đoạn này không đại diện cho posterior

### 5.2. Bao nhiêu Burn-in là đủ?

Không có quy tắc cứng nhắc, nhưng:
- Xem trace plot: Khi nào chuỗi "ổn định"?
- Thường: 10-50% số iterations đầu
- HMC thường cần ít burn-in hơn MH

```python
# Minh họa burn-in
np.random.seed(42)
samples_far_init, _ = metropolis_hastings(log_posterior, 0.01, 3000, 0.1)

fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# Full chain
axes[0].plot(samples_far_init, linewidth=1, alpha=0.7)
axes[0].axhline(stats.beta(9, 5).mean(), color='red', 
               linestyle='--', linewidth=2, alpha=0.5, label='True Mean')
axes[0].axvline(500, color='orange', linestyle='--', linewidth=2, 
               label='Burn-in cutoff')
axes[0].fill_between([0, 500], 0, 1, alpha=0.2, color='orange')
axes[0].set_xlabel('Iteration', fontsize=12, fontweight='bold')
axes[0].set_ylabel('θ', fontsize=12, fontweight='bold')
axes[0].set_title('Full Chain với Burn-in Period\n' +
                 'Initial value = 0.01 (xa true mean)',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# After burn-in
axes[1].plot(samples_far_init[500:], linewidth=1, alpha=0.7)
axes[1].axhline(stats.beta(9, 5).mean(), color='red', 
               linestyle='--', linewidth=2, alpha=0.5, label='True Mean')
axes[1].set_xlabel('Iteration (after burn-in)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('θ', fontsize=12, fontweight='bold')
axes[1].set_title('After Burn-in\nChuỗi đã ổn định',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\nBURN-IN PERIOD:")
print("-" * 70)
print(f"Mean (full chain):        {np.mean(samples_far_init):.4f}")
print(f"Mean (after burn-in):     {np.mean(samples_far_init[500:]):.4f}")
print(f"True mean:                {stats.beta(9, 5).mean():.4f}")
print("\n→ Sau burn-in, estimate chính xác hơn nhiều!")
```

## Tóm tắt và Workflow Thực hành

### Checklist Chẩn đoán MCMC

Khi bạn chạy MCMC, hãy kiểm tra theo thứ tự:

1. **Trace plots** ✓
   - Fuzzy caterpillar? Không có trend/stuck?

2. **R-hat** (nếu chạy multiple chains) ✓
   - R-hat < 1.01 cho tất cả tham số?

3. **Effective Sample Size** ✓
   - ESS > 400 cho mỗi tham số?

4. **Autocorrelation** ✓
   - ACF giảm nhanh về 0?

5. **Burn-in** ✓
   - Đã loại bỏ giai đoạn khởi động?

### Nếu Có Vấn đề

| Vấn đề | Nguyên nhân | Giải pháp |
|--------|-------------|-----------|
| Trend trong trace plot | Chưa hội tụ | Chạy thêm iterations, tăng burn-in |
| Stuck | Poor mixing | Tăng proposal SD (MH), dùng HMC |
| R-hat > 1.01 | Chưa hội tụ | Chạy thêm iterations |
| ESS thấp | High autocorrelation | Tăng proposal SD, dùng HMC, thinning |
| ACF giảm chậm | High autocorrelation | Điều chỉnh proposal, dùng HMC |

## Tóm tắt và Kết nối

MCMC diagnostics là thiết yếu để đảm bảo kết quả đáng tin cậy:

- **Trace plots**: Visual inspection - fuzzy caterpillar là tốt
- **R-hat**: Convergence diagnostic - < 1.01 là tốt
- **ESS**: Đo lường độc lập - > 400 là đủ
- **Autocorrelation**: Phụ thuộc giữa mẫu - giảm nhanh là tốt
- **Burn-in**: Loại bỏ giai đoạn khởi động

Trong bài tiếp theo, chúng ta sẽ học cách sử dụng **PyMC** - một công cụ mạnh mẽ tự động thực hiện MCMC và diagnostics cho chúng ta.

## Bài tập

**Bài tập 1: Trace Plot Interpretation**
Cho các trace plots sau (tưởng tượng hoặc vẽ):
(a) Trend tăng dần
(b) Fuzzy caterpillar
(c) Stuck ở hai vùng
Với mỗi trường hợp, chẩn đoán vấn đề và đề xuất giải pháp.

**Bài tập 2: Compute R-hat**
(a) Chạy 3 chains với initial values: 0.2, 0.5, 0.8
(b) Compute R-hat manually
(c) Nếu R-hat = 1.15, bạn sẽ làm gì?

**Bài tập 3: ESS Analysis**
(a) Chạy MH với proposal SD = 0.01, 0.1, 0.5
(b) Compute ESS cho mỗi trường hợp
(c) So sánh ESS/N ratio. Proposal nào tốt nhất?

**Bài tập 4: Burn-in**
(a) Chạy MH với initial value = 0.01 (xa true mean)
(b) Vẽ trace plot và running mean
(c) Ước lượng burn-in period cần thiết
(d) So sánh posterior mean với và không có burn-in

**Bài tập 5: Comprehensive Diagnostics**
Chạy một MCMC chain và thực hiện full diagnostics:
(a) Trace plot
(b) R-hat (chạy multiple chains)
(c) ESS
(d) Autocorrelation plot
(e) Viết báo cáo ngắn: Mẫu có đáng tin cậy không? Tại sao?

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 11.4: Inference and assessing convergence

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 7.5: MCMC representativeness, accuracy, and efficiency

### Supplementary Reading:

**Gelman, A., & Rubin, D. B. (1992).** *Inference from iterative simulation using multiple sequences*. Statistical Science, 7(4), 457-472.
- Bài báo gốc về R-hat statistic

**Vehtari, A., Gelman, A., Simpson, D., Carpenter, B., & Bürkner, P. C. (2021).** *Rank-normalization, folding, and localization: An improved R-hat for assessing convergence of MCMC*. Bayesian Analysis, 16(2), 667-718.
- Phiên bản cải tiến của R-hat

---

*Bài học tiếp theo: [3.6 PyMC Implementation - MCMC trong Thực tế](/vi/chapter03/pymc-implementation/)*
