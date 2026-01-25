---
layout: post
title: "Bài 2.6: Grid Approximation - Xấp xỉ Lưới"
chapter: '02'
order: 6
owner: Nguyen Le Linh
lang: vi
categories:
- chapter02
lesson_type: required
---

## Mục tiêu

Bài học này giới thiệu **grid approximation** - phương pháp đơn giản nhất để tính posterior khi không có conjugate prior hoặc công thức giải tích. Đây là nền tảng để hiểu các phương pháp phức tạp hơn như MCMC.

## 1. Grid Approximation là gì?

![Grid Approximation - Phương pháp Xấp xỉ Grid]({{ site.baseurl }}/img/chapter_img/chapter02/grid_approximation.png)

### 1.1. Ý tưởng Cơ bản

**Grid Approximation** chia không gian tham số thành **lưới** các điểm rời rạc, tính posterior tại mỗi điểm.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Minh họa: Grid approximation cơ bản
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Dữ liệu: 6 ngửa trong 9 lần tung
n, k = 9, 6

# Prior: Beta(1, 1) = Uniform
def prior(theta):
    return stats.beta(1, 1).pdf(theta)

# Likelihood: Binomial
def likelihood(theta, k, n):
    return stats.binom.pmf(k, n, theta)

# Grid với độ phân giải khác nhau
grid_sizes = [5, 20, 100]

for idx, grid_size in enumerate(grid_sizes):
    ax = axes[0, idx]
    
    # Tạo grid
    theta_grid = np.linspace(0, 1, grid_size)
    
    # Tính prior, likelihood, posterior tại mỗi điểm
    prior_vals = np.array([prior(theta) for theta in theta_grid])
    likelihood_vals = np.array([likelihood(theta, k, n) for theta in theta_grid])
    
    # Posterior (chưa chuẩn hóa)
    posterior_unnorm = prior_vals * likelihood_vals
    
    # Chuẩn hóa (tích phân bằng tổng)
    posterior_vals = posterior_unnorm / np.sum(posterior_unnorm)
    
    # Vẽ
    ax.bar(theta_grid, posterior_vals, width=1/grid_size, alpha=0.7, 
          edgecolor='black', linewidth=1)
    ax.set_xlabel('θ', fontsize=11)
    ax.set_ylabel('P(θ \mid data)', fontsize=11)
    ax.set_title(f'Grid size = {grid_size}\n{"Thô" if grid_size == 5 else "Trung bình" if grid_size == 20 else "Mịn"}', 
                fontsize=12, fontweight='bold')
    ax.grid(alpha=0.3, axis='y')
    ax.set_xlim(0, 1)

# So sánh với posterior chính xác
theta_fine = np.linspace(0, 1, 1000)
posterior_exact = stats.beta(1 + k, 1 + n - k).pdf(theta_fine)

for idx, grid_size in enumerate(grid_sizes):
    ax = axes[1, idx]
    
    # Grid approximation
    theta_grid = np.linspace(0, 1, grid_size)
    prior_vals = np.array([prior(theta) for theta in theta_grid])
    likelihood_vals = np.array([likelihood(theta, k, n) for theta in theta_grid])
    posterior_unnorm = prior_vals * likelihood_vals
    posterior_vals = posterior_unnorm / np.sum(posterior_unnorm)
    
    # Vẽ cả hai
    ax.plot(theta_fine, posterior_exact, linewidth=3, color='red', 
           label='Chính xác (Beta)', alpha=0.7)
    ax.bar(theta_grid, posterior_vals, width=1/grid_size, alpha=0.5, 
          edgecolor='black', linewidth=1, label=f'Grid ({grid_size} điểm)')
    ax.set_xlabel('θ', fontsize=11)
    ax.set_ylabel('P(θ \mid data)', fontsize=11)
    ax.set_title(f'So sánh: Grid vs Chính xác\nGrid size = {grid_size}', 
                fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3, axis='y')
    ax.set_xlim(0, 1)

plt.tight_layout()
plt.show()

print("=== GRID APPROXIMATION ===")
print(f"\nDữ liệu: {k}/{n} ngửa")
print(f"\nPosterior chính xác: Beta({1+k}, {1+n-k})")
print(f"  Mean: {stats.beta(1+k, 1+n-k).mean():.4f}")
print(f"\nGrid approximation:")
for grid_size in grid_sizes:
    theta_grid = np.linspace(0, 1, grid_size)
    prior_vals = np.array([prior(theta) for theta in theta_grid])
    likelihood_vals = np.array([likelihood(theta, k, n) for theta in theta_grid])
    posterior_unnorm = prior_vals * likelihood_vals
    posterior_vals = posterior_unnorm / np.sum(posterior_unnorm)
    mean_grid = np.sum(theta_grid * posterior_vals)
    print(f"  Grid {grid_size:3d}: Mean = {mean_grid:.4f}")
```

![Grid Approximation Concept](https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Riemann_sum_convergence.png/800px-Riemann_sum_convergence.png)
*Nguồn: Wikipedia - Riemann Sum (ý tưởng tương tự)*

### 1.2. Thuật toán Grid Approximation

```python
# Thuật toán chi tiết
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Dữ liệu
n, k = 9, 6
grid_size = 50
theta_grid = np.linspace(0, 1, grid_size)

# Bước 1: Prior
prior_vals = np.array([prior(theta) for theta in theta_grid])
axes[0, 0].bar(theta_grid, prior_vals, width=1/grid_size, alpha=0.7, 
              edgecolor='black', color='blue')
axes[0, 0].set_xlabel('θ', fontsize=11)
axes[0, 0].set_ylabel('P(θ)', fontsize=11)
axes[0, 0].set_title('Bước 1: Tính Prior tại mỗi điểm grid', 
                    fontsize=12, fontweight='bold')
axes[0, 0].grid(alpha=0.3, axis='y')

# Bước 2: Likelihood
likelihood_vals = np.array([likelihood(theta, k, n) for theta in theta_grid])
axes[0, 1].bar(theta_grid, likelihood_vals, width=1/grid_size, alpha=0.7, 
              edgecolor='black', color='green')
axes[0, 1].set_xlabel('θ', fontsize=11)
axes[0, 1].set_ylabel('L(θ \mid data)', fontsize=11)
axes[0, 1].set_title(f'Bước 2: Tính Likelihood\nData: {k}/{n}', 
                    fontsize=12, fontweight='bold')
axes[0, 1].grid(alpha=0.3, axis='y')

# Bước 3: Nhân
posterior_unnorm = prior_vals * likelihood_vals
axes[1, 0].bar(theta_grid, posterior_unnorm, width=1/grid_size, alpha=0.7, 
              edgecolor='black', color='orange')
axes[1, 0].set_xlabel('θ', fontsize=11)
axes[1, 0].set_ylabel('Prior × Likelihood', fontsize=11)
axes[1, 0].set_title('Bước 3: Nhân Prior × Likelihood\n(Chưa chuẩn hóa)', 
                    fontsize=12, fontweight='bold')
axes[1, 0].grid(alpha=0.3, axis='y')

# Bước 4: Chuẩn hóa
posterior_vals = posterior_unnorm / np.sum(posterior_unnorm)
axes[1, 1].bar(theta_grid, posterior_vals, width=1/grid_size, alpha=0.7, 
              edgecolor='black', color='red')
axes[1, 1].set_xlabel('θ', fontsize=11)
axes[1, 1].set_ylabel('P(θ \mid data)', fontsize=11)
axes[1, 1].set_title(f'Bước 4: Chuẩn hóa\nΣ P(θ \mid data) = {np.sum(posterior_vals):.4f}', 
                    fontsize=12, fontweight='bold')
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# Code minh họa
print("\n=== THUẬT TOÁN GRID APPROXIMATION ===")
print("""
# Bước 1: Định nghĩa grid
theta_grid = np.linspace(0, 1, grid_size)

# Bước 2: Tính prior tại mỗi điểm
prior_vals = [prior(theta) for theta in theta_grid]

# Bước 3: Tính likelihood tại mỗi điểm
likelihood_vals = [likelihood(theta, data) for theta in theta_grid]

# Bước 4: Nhân prior × likelihood
posterior_unnorm = prior_vals * likelihood_vals

# Bước 5: Chuẩn hóa (tổng = 1)
posterior_vals = posterior_unnorm / np.sum(posterior_unnorm)
""")
```

## 2. Sử dụng Grid Approximation

### 2.1. Tính các Thống kê

```python
# Tính các thống kê từ grid approximation
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Grid approximation
grid_size = 1000
theta_grid = np.linspace(0, 1, grid_size)
prior_vals = np.array([prior(theta) for theta in theta_grid])
likelihood_vals = np.array([likelihood(theta, k, n) for theta in theta_grid])
posterior_unnorm = prior_vals * likelihood_vals
posterior_vals = posterior_unnorm / np.sum(posterior_unnorm)

# 1. Mean, Median, Mode
mean_post = np.sum(theta_grid * posterior_vals)
median_post = theta_grid[np.argmin(np.abs(np.cumsum(posterior_vals) - 0.5))]
mode_post = theta_grid[np.argmax(posterior_vals)]

axes[0, 0].bar(theta_grid, posterior_vals, width=1/grid_size, alpha=0.7, 
              edgecolor='none', color='blue')
axes[0, 0].axvline(mean_post, color='red', linestyle='--', linewidth=2, 
                  label=f'Mean = {mean_post:.3f}')
axes[0, 0].axvline(median_post, color='green', linestyle='--', linewidth=2, 
                  label=f'Median = {median_post:.3f}')
axes[0, 0].axvline(mode_post, color='orange', linestyle='--', linewidth=2, 
                  label=f'Mode = {mode_post:.3f}')
axes[0, 0].set_xlabel('θ', fontsize=11)
axes[0, 0].set_ylabel('P(θ \mid data)', fontsize=11)
axes[0, 0].set_title('Posterior: Mean, Median, Mode', 
                    fontsize=12, fontweight='bold')
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(alpha=0.3, axis='y')

# 2. Credible Interval
cumsum_post = np.cumsum(posterior_vals)
ci_lower_idx = np.argmin(np.abs(cumsum_post - 0.025))
ci_upper_idx = np.argmin(np.abs(cumsum_post - 0.975))
ci_lower = theta_grid[ci_lower_idx]
ci_upper = theta_grid[ci_upper_idx]

axes[0, 1].bar(theta_grid, posterior_vals, width=1/grid_size, alpha=0.7, 
              edgecolor='none', color='blue')
axes[0, 1].bar(theta_grid[(theta_grid >= ci_lower) & (theta_grid <= ci_upper)], 
              posterior_vals[(theta_grid >= ci_lower) & (theta_grid <= ci_upper)],
              width=1/grid_size, alpha=0.7, edgecolor='none', color='yellow')
axes[0, 1].axvline(ci_lower, color='red', linestyle='--', linewidth=2)
axes[0, 1].axvline(ci_upper, color='red', linestyle='--', linewidth=2)
axes[0, 1].set_xlabel('θ', fontsize=11)
axes[0, 1].set_ylabel('P(θ \mid data)', fontsize=11)
axes[0, 1].set_title(f'95% Credible Interval\n[{ci_lower:.3f}, {ci_upper:.3f}]', 
                    fontsize=12, fontweight='bold')
axes[0, 1].grid(alpha=0.3, axis='y')

# 3. Xác suất của một khoảng
prob_interval = np.sum(posterior_vals[(theta_grid >= 0.5) & (theta_grid <= 0.8)])

axes[1, 0].bar(theta_grid, posterior_vals, width=1/grid_size, alpha=0.7, 
              edgecolor='none', color='blue')
axes[1, 0].bar(theta_grid[(theta_grid >= 0.5) & (theta_grid <= 0.8)], 
              posterior_vals[(theta_grid >= 0.5) & (theta_grid <= 0.8)],
              width=1/grid_size, alpha=0.7, edgecolor='none', color='green')
axes[1, 0].set_xlabel('θ', fontsize=11)
axes[1, 0].set_ylabel('P(θ \mid data)', fontsize=11)
axes[1, 0].set_title(f'P(0.5 ≤ θ ≤ 0.8 \mid data) = {prob_interval:.3f}', 
                    fontsize=12, fontweight='bold')
axes[1, 0].grid(alpha=0.3, axis='y')

# 4. Sampling từ posterior
n_samples = 10000
samples = np.random.choice(theta_grid, size=n_samples, p=posterior_vals)

axes[1, 1].hist(samples, bins=50, density=True, alpha=0.7, 
               edgecolor='black', label='Samples')
axes[1, 1].plot(theta_grid, posterior_vals * grid_size, linewidth=2, 
               color='red', label='True posterior')
axes[1, 1].set_xlabel('θ', fontsize=11)
axes[1, 1].set_ylabel('Mật độ', fontsize=11)
axes[1, 1].set_title(f'Sampling từ Posterior\n(n = {n_samples:,})', 
                    fontsize=12, fontweight='bold')
axes[1, 1].legend(fontsize=10)
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\n=== THỐNG KÊ TỪ GRID APPROXIMATION ===")
print(f"\nDữ liệu: {k}/{n}")
print(f"Grid size: {grid_size}")
print(f"\nPosterior:")
print(f"  Mean: {mean_post:.4f}")
print(f"  Median: {median_post:.4f}")
print(f"  Mode: {mode_post:.4f}")
print(f"  95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"\nXác suất:")
print(f"  P(0.5 ≤ θ ≤ 0.8 \mid data) = {prob_interval:.4f}")
print(f"\nSamples:")
print(f"  Mean: {samples.mean():.4f}")
print(f"  SD: {samples.std():.4f}")
```

### 2.2. Posterior Predictive

```python
# Posterior Predictive từ grid approximation
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Dự đoán: Số ngửa trong 10 lần tung mới
n_new = 10
k_new_range = np.arange(0, n_new + 1)

# Posterior predictive: P(k_new \mid data) = Σ P(k_new \mid θ) P(θ \mid data)
ppd = np.zeros(len(k_new_range))
for i, k_new in enumerate(k_new_range):
    # Tại mỗi k_new, tính tổng trên tất cả θ
    for j, theta in enumerate(theta_grid):
        ppd[i] += stats.binom.pmf(k_new, n_new, theta) * posterior_vals[j]

# Vẽ
axes[0].bar(k_new_range, ppd, alpha=0.7, edgecolor='black')
axes[0].axvline(ppd @ k_new_range, color='red', linestyle='--', linewidth=2,
               label=f'E[k] = {ppd @ k_new_range:.2f}')
axes[0].set_xlabel(f'k (số ngửa trong {n_new} lần tung MỚI)', fontsize=11)
axes[0].set_ylabel('P(k \mid data)', fontsize=11)
axes[0].set_title(f'Posterior Predictive Distribution\nDự đoán dữ liệu mới', 
                 fontsize=12, fontweight='bold')
axes[0].legend(fontsize=10)
axes[0].grid(alpha=0.3, axis='y')

# So sánh với công thức Beta-Binomial
from scipy.special import comb, beta as beta_func

def beta_binomial_pmf(k, n, alpha, beta_param):
    return (comb(n, k) * 
            beta_func(k + alpha, n - k + beta_param) / 
            beta_func(alpha, beta_param))

alpha_post, beta_post = 1 + k, 1 + n - k
ppd_exact = [beta_binomial_pmf(k_new, n_new, alpha_post, beta_post) 
             for k_new in k_new_range]

axes[1].bar(k_new_range, ppd, alpha=0.7, edgecolor='black', label='Grid approx')
axes[1].plot(k_new_range, ppd_exact, 'ro-', markersize=8, linewidth=2, 
            label='Chính xác (Beta-Binomial)')
axes[1].set_xlabel(f'k (số ngửa trong {n_new} lần tung)', fontsize=11)
axes[1].set_ylabel('P(k \mid data)', fontsize=11)
axes[1].set_title('So sánh: Grid Approx vs Chính xác\nRất gần nhau!', 
                 fontsize=12, fontweight='bold')
axes[1].legend(fontsize=10)
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\n=== POSTERIOR PREDICTIVE ===")
print(f"\nDự đoán {n_new} lần tung mới:")
print(f"  E[k] (grid): {ppd @ k_new_range:.2f}")
print(f"  E[k] (exact): {np.array(ppd_exact) @ k_new_range:.2f}")
print(f"\nSai số: {abs((ppd @ k_new_range) - (np.array(ppd_exact) @ k_new_range)):.4f}")
```

## 3. Ưu và Nhược điểm

### 3.1. So sánh với các Phương pháp khác

```python
# So sánh các phương pháp
fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('off')

comparison = """
╔═══════════════════════════════════════════════════════════════════════════╗
║              SO SÁNH CÁC PHƯƠNG PHÁP TÍNH POSTERIOR                        ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  1. CONJUGATE PRIOR (Giải tích)                                            ║
║     ✓ Chính xác 100%                                                      ║
║     ✓ Nhanh nhất                                                          ║
║     ✓ Dễ hiểu                                                             ║
║     ✗ Chỉ có một số trường hợp                                            ║
║     ✗ Không linh hoạt                                                     ║
║                                                                           ║
║  2. GRID APPROXIMATION                                                     ║
║     ✓ Đơn giản, dễ hiểu                                                   ║
║     ✓ Linh hoạt (bất kỳ prior/likelihood)                                 ║
║     ✓ Chính xác với grid đủ mịn                                           ║
║     ✗ Chậm với nhiều tham số                                              ║
║     ✗ Curse of dimensionality                                             ║
║     → Chỉ dùng cho 1-2 tham số                                            ║
║                                                                           ║
║  3. MCMC (Markov Chain Monte Carlo)                                        ║
║     ✓ Mạnh nhất                                                           ║
║     ✓ Hoạt động với nhiều tham số                                         ║
║     ✓ Linh hoạt                                                           ║
║     ✗ Phức tạp                                                            ║
║     ✗ Cần kiểm tra convergence                                            ║
║     → Phương pháp chuẩn cho model phức tạp                                ║
║                                                                           ║
║  4. VARIATIONAL INFERENCE                                                  ║
║     ✓ Nhanh hơn MCMC                                                      ║
║     ✓ Scalable                                                            ║
║     ✗ Xấp xỉ (có thể sai)                                                 ║
║     ✗ Khó implement                                                       ║
║     → Dùng cho big data                                                   ║
║                                                                           ║
║  KHI NÀO DÙNG GÌ?                                                          ║
║    • 1 tham số, học tập → Grid Approximation                              ║
║    • Có conjugate → Conjugate Prior                                       ║
║    • Model phức tạp → MCMC                                                ║
║    • Big data → Variational Inference                                     ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

ax.text(0.5, 0.5, comparison, fontsize=9, family='monospace',
       ha='center', va='center',
       bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))

plt.tight_layout()
plt.show()
```

### 3.2. Curse of Dimensionality

```python
# Minh họa: Curse of dimensionality
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Số điểm cần thiết theo số chiều
dims = np.arange(1, 11)
points_per_dim = 100
total_points = points_per_dim ** dims

axes[0].semilogy(dims, total_points, 'o-', linewidth=2, markersize=8)
axes[0].set_xlabel('Số tham số', fontsize=11)
axes[0].set_ylabel('Số điểm grid (log scale)', fontsize=11)
axes[0].set_title('Curse of Dimensionality\nSố điểm tăng MŨ theo số tham số!', 
                 fontsize=12, fontweight='bold')
axes[0].grid(alpha=0.3)

# Annotations
for i, (dim, points) in enumerate(zip(dims[:5], total_points[:5])):
    axes[0].annotate(f'{points:,}', 
                    xy=(dim, points), xytext=(dim+0.3, points*2),
                    fontsize=9, ha='left')

# Bảng
axes[1].axis('off')
table_data = """
╔═══════════════════════════════════════════════════════════╗
║        CURSE OF DIMENSIONALITY                            ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Giả sử: 100 điểm mỗi chiều                               ║
║                                                           ║
║  1 tham số:  100¹ = 100 điểm                              ║
║    → Dễ dàng!                                             ║
║                                                           ║
║  2 tham số:  100² = 10,000 điểm                           ║
║    → Vẫn OK                                               ║
║                                                           ║
║  3 tham số:  100³ = 1,000,000 điểm                        ║
║    → Bắt đầu chậm                                         ║
║                                                           ║
║  4 tham số:  100⁴ = 100,000,000 điểm                      ║
║    → RẤT chậm!                                            ║
║                                                           ║
║  5 tham số:  100⁵ = 10,000,000,000 điểm                   ║
║    → KHÔNG khả thi!                                       ║
║                                                           ║
║  ──────────────────────────────────────────────────────  ║
║                                                           ║
║  KẾT LUẬN:                                                ║
║    Grid Approximation CHỈ dùng cho:                       ║
║      • 1 tham số: Tốt                                     ║
║      • 2 tham số: OK                                      ║
║      • 3+ tham số: KHÔNG khả thi                          ║
║                                                           ║
║    → Cần MCMC cho model phức tạp!                         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[1].text(0.5, 0.5, table_data, fontsize=9, family='monospace',
            ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='#ffcccc', alpha=0.8))

plt.tight_layout()
plt.show()

print("\n=== CURSE OF DIMENSIONALITY ===")
print(f"\n100 điểm mỗi chiều:")
for dim in range(1, 6):
    points = 100 ** dim
    print(f"  {dim} tham số: {points:,} điểm")
```

## 4. Ví dụ Thực hành

### 4.1. Ví dụ: Prior Không Conjugate

```python
# Ví dụ: Prior mixture (không conjugate)
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Dữ liệu
n, k = 20, 12

# Prior: Mixture của 2 Beta
# 60% tin θ ~ 0.3, 40% tin θ ~ 0.7
def prior_mixture(theta):
    return 0.6 * stats.beta(30, 70).pdf(theta) + 0.4 * stats.beta(70, 30).pdf(theta)

# Grid approximation
grid_size = 1000
theta_grid = np.linspace(0, 1, grid_size)

prior_vals = np.array([prior_mixture(theta) for theta in theta_grid])
likelihood_vals = np.array([likelihood(theta, k, n) for theta in theta_grid])
posterior_unnorm = prior_vals * likelihood_vals
posterior_vals = posterior_unnorm / np.sum(posterior_unnorm)

# 1. Prior
axes[0, 0].plot(theta_grid, prior_vals, linewidth=2, color='blue')
axes[0, 0].fill_between(theta_grid, prior_vals, alpha=0.3, color='blue')
axes[0, 0].set_xlabel('θ', fontsize=11)
axes[0, 0].set_ylabel('Mật độ', fontsize=11)
axes[0, 0].set_title('Prior: Mixture (Bimodal)\nKHÔNG conjugate!', 
                    fontsize=12, fontweight='bold')
axes[0, 0].grid(alpha=0.3)

# 2. Likelihood
axes[0, 1].plot(theta_grid, likelihood_vals, linewidth=2, color='green')
axes[0, 1].fill_between(theta_grid, likelihood_vals, alpha=0.3, color='green')
axes[0, 1].axvline(k/n, color='red', linestyle='--', linewidth=2, label=f'MLE={k/n:.2f}')
axes[0, 1].set_xlabel('θ', fontsize=11)
axes[0, 1].set_ylabel('L(θ \mid data)', fontsize=11)
axes[0, 1].set_title(f'Likelihood: {k}/{n} ngửa', 
                    fontsize=12, fontweight='bold')
axes[0, 1].legend(fontsize=10)
axes[0, 1].grid(alpha=0.3)

# 3. Posterior
axes[1, 0].plot(theta_grid, posterior_vals, linewidth=3, color='red')
axes[1, 0].fill_between(theta_grid, posterior_vals, alpha=0.3, color='red')

mean_post = np.sum(theta_grid * posterior_vals)
ci_lower = theta_grid[np.argmin(np.abs(np.cumsum(posterior_vals) - 0.025))]
ci_upper = theta_grid[np.argmin(np.abs(np.cumsum(posterior_vals) - 0.975))]

axes[1, 0].axvline(mean_post, color='darkred', linestyle='--', linewidth=2,
                  label=f'Mean={mean_post:.3f}')
axes[1, 0].set_xlabel('θ', fontsize=11)
axes[1, 0].set_ylabel('P(θ \mid data)', fontsize=11)
axes[1, 0].set_title(f'Posterior\nMean={mean_post:.3f}, 95% CI=[{ci_lower:.3f}, {ci_upper:.3f}]', 
                    fontsize=12, fontweight='bold')
axes[1, 0].legend(fontsize=10)
axes[1, 0].grid(alpha=0.3)

# 4. So sánh tất cả
axes[1, 1].plot(theta_grid, prior_vals/max(prior_vals), linewidth=2, 
               label='Prior (scaled)', linestyle='--', alpha=0.7)
axes[1, 1].plot(theta_grid, likelihood_vals/max(likelihood_vals), linewidth=2, 
               label='Likelihood (scaled)', alpha=0.7)
axes[1, 1].plot(theta_grid, posterior_vals/max(posterior_vals), linewidth=3, 
               label='Posterior (scaled)', alpha=0.7)
axes[1, 1].axvline(k/n, color='red', linestyle=':', linewidth=2, alpha=0.5)
axes[1, 1].set_xlabel('θ', fontsize=11)
axes[1, 1].set_ylabel('Giá trị (scaled)', fontsize=11)
axes[1, 1].set_title('So sánh: Prior, Likelihood, Posterior', 
                    fontsize=12, fontweight='bold')
axes[1, 1].legend(fontsize=10)
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\n=== PRIOR MIXTURE (KHÔNG CONJUGATE) ===")
print(f"\nPrior: 60% × Beta(30,70) + 40% × Beta(70,30)")
print(f"  → Bimodal, không conjugate")
print(f"\nDữ liệu: {k}/{n}")
print(f"\nPosterior (từ grid approximation):")
print(f"  Mean: {mean_post:.4f}")
print(f"  95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"\n→ Grid approximation cho phép dùng BẤT KỲ prior nào!")
```

## Tóm tắt

```python
# Infographic tóm tắt
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111)
ax.axis('off')

summary = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                  GRID APPROXIMATION - TÓM TẮT                              ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  1. Ý TƯỞNG                                                                ║
║     Chia không gian tham số thành lưới, tính posterior tại mỗi điểm       ║
║                                                                           ║
║  2. THUẬT TOÁN                                                             ║
║     ① Tạo grid: θ₁, θ₂, ..., θₙ                                           ║
║     ② Tính prior: p(θᵢ)                                                   ║
║     ③ Tính likelihood: p(D \mid θᵢ)                                          ║
║     ④ Nhân: p(θᵢ \mid D) ∝ p(D \mid θᵢ) p(θᵢ)                                   ║
║     ⑤ Chuẩn hóa: Σ p(θᵢ \mid D) = 1                                          ║
║                                                                           ║
║  3. ƯU ĐIỂM                                                                ║
║     ✓ Đơn giản, dễ hiểu                                                   ║
║     ✓ Linh hoạt (bất kỳ prior/likelihood)                                 ║
║     ✓ Chính xác với grid đủ mịn                                           ║
║     ✓ Dễ tính thống kê (mean, CI, etc.)                                   ║
║     ✓ Dễ sample từ posterior                                              ║
║                                                                           ║
║  4. NHƯỢC ĐIỂM                                                             ║
║     ✗ Curse of dimensionality                                             ║
║     ✗ Chỉ dùng cho 1-2 tham số                                            ║
║     ✗ Chậm với grid lớn                                                   ║
║                                                                           ║
║  5. KHI NÀO DÙNG?                                                          ║
║     ✓ Học tập, minh họa                                                   ║
║     ✓ 1 tham số                                                           ║
║     ✓ Prior không conjugate                                               ║
║     ✓ Kiểm tra kết quả MCMC                                               ║
║                                                                           ║
║  6. KHI NÀO KHÔNG DÙNG?                                                    ║
║     ✗ 3+ tham số → MCMC                                                   ║
║     ✗ Cần tốc độ → Conjugate (nếu có)                                     ║
║     ✗ Production → MCMC hoặc Variational                                  ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

ax.text(0.5, 0.5, summary, fontsize=10, family='monospace',
       ha='center', va='center',
       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.3))

plt.tight_layout()
plt.show()
```

## Bài tập

1. **Cơ bản**: Dùng grid approximation (100 điểm) để tính posterior với prior Beta(3, 3) và dữ liệu 15/25. So sánh với công thức conjugate.

2. **Prior mixture**: Dùng prior = 0.5 × Beta(10, 30) + 0.5 × Beta(30, 10) với dữ liệu 20/40. Tính posterior mean và 95% CI.

3. **Độ phân giải**: So sánh grid approximation với grid size = 10, 50, 100, 500, 1000. Vẽ biểu đồ sai số so với conjugate.

4. **Posterior predictive**: Từ posterior ở bài 1, tính posterior predictive cho 20 lần tung mới.

5. **2D grid**: (Thách thức) Implement grid approximation 2D cho model Normal với cả μ và σ² chưa biết. Dùng grid 50×50.

## Tài liệu tham khảo

1. **McElreath, R. (2020).** *Statistical Rethinking* (2nd Ed.). Chapter 2-3.
2. **Kruschke, J. (2014).** *Doing Bayesian Data Analysis*. Chapter 6.
3. **Gelman, A., et al. (2013).** *Bayesian Data Analysis* (3rd Ed.). Chapter 3.

---

## Tài liệu tham khảo

### Primary:
- **McElreath, R. (2020).** *Statistical Rethinking* (2nd Ed.)
  - Chapter 2: Small Worlds and Large Worlds (grid approximation)
  - Focus on: Computational posterior approximation, discrete grids

### Secondary:

#### Gelman et al. - Bayesian Data Analysis (3rd Edition):
- **Chapter 3.7**: Numerical integration
- **Appendix C**: Computation in R and Stan
- Focus on: Numerical methods for posterior computation

#### Kruschke - Doing Bayesian Data Analysis (2015):
- **Chapter 6**: Grid approximation for simple models
- Focus on: Discrete approximation, computational methods

**Lưu ý**: Gelman/Kruschke sử dụng R/Stan, nhưng grid approximation concepts hoàn toàn tương đương với Python/NumPy implementation.

---

*Kết thúc Chapter 02. Bài học tiếp theo: [Chapter 03 - Sampling, Monte Carlo, và MCMC](/vi/chapter03/)*

