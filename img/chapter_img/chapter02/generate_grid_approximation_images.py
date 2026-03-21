#!/usr/bin/env python3
"""
Generate grid approximation images for Chapter 02
Covers all conceptual visualizations for grid approximation method
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import comb, beta as beta_func

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.dpi'] = 300

# Helper functions
def prior(theta):
    """Uniform prior Beta(1,1)"""
    return stats.beta(1, 1).pdf(theta)

def likelihood(theta, k, n):
    """Binomial likelihood"""
    return stats.binom.pmf(k, n, theta)

# ============================================================================
# Image 1: Grid Approximation Basics (different resolutions + comparison)
# ============================================================================
def generate_grid_basics():
    """Generate basic grid approximation with different resolutions"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Data: 6 heads in 9 flips
    n, k = 9, 6
    
    # Grid with different resolutions
    grid_sizes = [5, 20, 100]
    
    for idx, grid_size in enumerate(grid_sizes):
        ax = axes[0, idx]
        
        # Create grid
        theta_grid = np.linspace(0, 1, grid_size)
        
        # Compute prior, likelihood, posterior at each point
        prior_vals = np.array([prior(theta) for theta in theta_grid])
        likelihood_vals = np.array([likelihood(theta, k, n) for theta in theta_grid])
        
        # Posterior (unnormalized)
        posterior_unnorm = prior_vals * likelihood_vals
        
        # Normalize (integral = sum)
        posterior_vals = posterior_unnorm / np.sum(posterior_unnorm)
        
        # Plot
        ax.bar(theta_grid, posterior_vals, width=1/grid_size, alpha=0.7, 
              edgecolor='black', linewidth=1)
        ax.set_xlabel('θ', fontsize=11)
        ax.set_ylabel('P(θ | data)', fontsize=11)
        ax.set_title(f'Grid size = {grid_size}\n{"Thô" if grid_size == 5 else "Trung bình" if grid_size == 20 else "Mịn"}', 
                    fontsize=12, fontweight='bold')
        ax.grid(alpha=0.3, axis='y')
        ax.set_xlim(0, 1)
    
    # Compare with exact posterior
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
        
        # Plot both
        ax.plot(theta_fine, posterior_exact, linewidth=3, color='red', 
               label='Chính xác (Beta)', alpha=0.7)
        ax.bar(theta_grid, posterior_vals, width=1/grid_size, alpha=0.5, 
              edgecolor='black', linewidth=1, label=f'Grid ({grid_size} điểm)')
        ax.set_xlabel('θ', fontsize=11)
        ax.set_ylabel('P(θ | data)', fontsize=11)
        ax.set_title(f'So sánh: Grid vs Chính xác\nGrid size = {grid_size}', 
                    fontsize=12, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3, axis='y')
        ax.set_xlim(0, 1)
    
    plt.tight_layout()
    plt.savefig('grid_approximation_basics.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: grid_approximation_basics.png")
    plt.close()

# ============================================================================
# Image 2: Computing Statistics from Grid
# ============================================================================
def generate_grid_statistics():
    """Generate visualization of computing statistics from grid"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Data
    n, k = 9, 6
    
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
    axes[0, 0].set_ylabel('P(θ | data)', fontsize=11)
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
    axes[0, 1].set_ylabel('P(θ | data)', fontsize=11)
    axes[0, 1].set_title(f'95% Credible Interval\n[{ci_lower:.3f}, {ci_upper:.3f}]', 
                        fontsize=12, fontweight='bold')
    axes[0, 1].grid(alpha=0.3, axis='y')
    
    # 3. Probability of an interval
    prob_interval = np.sum(posterior_vals[(theta_grid >= 0.5) & (theta_grid <= 0.8)])
    
    axes[1, 0].bar(theta_grid, posterior_vals, width=1/grid_size, alpha=0.7, 
                  edgecolor='none', color='blue')
    axes[1, 0].bar(theta_grid[(theta_grid >= 0.5) & (theta_grid <= 0.8)], 
                  posterior_vals[(theta_grid >= 0.5) & (theta_grid <= 0.8)],
                  width=1/grid_size, alpha=0.7, edgecolor='none', color='green')
    axes[1, 0].set_xlabel('θ', fontsize=11)
    axes[1, 0].set_ylabel('P(θ | data)', fontsize=11)
    axes[1, 0].set_title(f'P(0.5 ≤ θ ≤ 0.8 | data) = {prob_interval:.3f}', 
                        fontsize=12, fontweight='bold')
    axes[1, 0].grid(alpha=0.3, axis='y')
    
    # 4. Sampling from posterior
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
    plt.savefig('grid_statistics_computation.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: grid_statistics_computation.png")
    plt.close()

# ============================================================================
# Image 3: Posterior Predictive from Grid
# ============================================================================
def generate_posterior_predictive():
    """Generate posterior predictive distribution from grid"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Data
    n, k = 9, 6
    
    # Grid approximation
    grid_size = 1000
    theta_grid = np.linspace(0, 1, grid_size)
    prior_vals = np.array([prior(theta) for theta in theta_grid])
    likelihood_vals = np.array([likelihood(theta, k, n) for theta in theta_grid])
    posterior_unnorm = prior_vals * likelihood_vals
    posterior_vals = posterior_unnorm / np.sum(posterior_unnorm)
    
    # Predict: Number of heads in 10 new flips
    n_new = 10
    k_new_range = np.arange(0, n_new + 1)
    
    # Posterior predictive: P(k_new | data) = Σ P(k_new | θ) P(θ | data)
    ppd = np.zeros(len(k_new_range))
    for i, k_new in enumerate(k_new_range):
        # For each k_new, sum over all θ
        for j, theta in enumerate(theta_grid):
            ppd[i] += stats.binom.pmf(k_new, n_new, theta) * posterior_vals[j]
    
    # Plot
    axes[0].bar(k_new_range, ppd, alpha=0.7, edgecolor='black')
    axes[0].axvline(ppd @ k_new_range, color='red', linestyle='--', linewidth=2,
                   label=f'E[k] = {ppd @ k_new_range:.2f}')
    axes[0].set_xlabel(f'k (số ngửa trong {n_new} lần tung MỚI)', fontsize=11)
    axes[0].set_ylabel('P(k | data)', fontsize=11)
    axes[0].set_title(f'Posterior Predictive Distribution\nDự đoán dữ liệu mới', 
                     fontsize=12, fontweight='bold')
    axes[0].legend(fontsize=10)
    axes[0].grid(alpha=0.3, axis='y')
    
    # Compare with exact Beta-Binomial formula
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
    axes[1].set_ylabel('P(k | data)', fontsize=11)
    axes[1].set_title('So sánh: Grid Approx vs Chính xác\nRất gần nhau!', 
                     fontsize=12, fontweight='bold')
    axes[1].legend(fontsize=10)
    axes[1].grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('grid_posterior_predictive.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: grid_posterior_predictive.png")
    plt.close()

# ============================================================================
# Image 4: Comparison with Other Methods
# ============================================================================
def generate_method_comparison():
    """Generate comparison table of methods"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')
    
    comparison = """╔═══════════════════════════════════════════════════════════════════════════╗
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
║  ─────────────────────────────────────────────────────────────────────── ║
║                                                                           ║
║  LỰA CHỌN PHƯƠNG PHÁP:                                                     ║
║                                                                           ║
║    Có conjugate prior?                                                    ║
║      ├─ YES → Dùng CONJUGATE (nhanh nhất!)                                ║
║      └─ NO → Tiếp tục...                                                  ║
║                                                                           ║
║    Số tham số ≤ 2?                                                        ║
║      ├─ YES → Dùng GRID (đơn giản, trực quan)                             ║
║      └─ NO → Dùng MCMC (duy nhất khả thi)                                 ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""
    
    ax.text(0.5, 0.5, comparison, fontsize=9, family='monospace',
           ha='center', va='center',
           bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('methods_comparison_grid.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: methods_comparison_grid.png")
    plt.close()

# ============================================================================
# Image 5: Curse of Dimensionality
# ============================================================================
def generate_curse_dimensionality():
    """Generate curse of dimensionality visualization"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Number of points needed by dimension
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
    
    # Table
    axes[1].axis('off')
    table_data = """╔═══════════════════════════════════════════════════════════╗
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
    plt.savefig('curse_of_dimensionality.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: curse_of_dimensionality.png")
    plt.close()

# ============================================================================
# Image 6: Non-Conjugate Prior Example (Mixture)
# ============================================================================
def generate_mixture_prior_example():
    """Generate non-conjugate mixture prior example"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Data
    n, k = 20, 12
    
    # Prior: Mixture of 2 Betas
    # 60% believe θ ~ 0.3, 40% believe θ ~ 0.7
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
    axes[0, 1].set_ylabel('L(θ | data)', fontsize=11)
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
    axes[1, 0].set_ylabel('P(θ | data)', fontsize=11)
    axes[1, 0].set_title(f'Posterior\nMean={mean_post:.3f}, 95% CI=[{ci_lower:.3f}, {ci_upper:.3f}]', 
                        fontsize=12, fontweight='bold')
    axes[1, 0].legend(fontsize=10)
    axes[1, 0].grid(alpha=0.3)
    
    # 4. Compare all
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
    plt.savefig('grid_mixture_prior_example.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: grid_mixture_prior_example.png")
    plt.close()

# ============================================================================
# Image 7: Summary Infographic
# ============================================================================
def generate_grid_summary():
    """Generate summary infographic for grid approximation"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    summary = """╔═══════════════════════════════════════════════════════════════════════════╗
║                  GRID APPROXIMATION - TÓM TẮT                              ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  1. Ý TƯỞNG                                                                ║
║     Chia không gian tham số thành lưới, tính posterior tại mỗi điểm       ║
║                                                                           ║
║  2. THUẬT TOÁN                                                             ║
║     ① Tạo grid: θ₁, θ₂, ..., θₙ                                           ║
║     ② Tính prior: p(θᵢ)                                                   ║
║     ③ Tính likelihood: p(D | θᵢ)                                          ║
║     ④ Nhân: p(θᵢ | D) ∝ p(D | θᵢ) p(θᵢ)                                   ║
║     ⑤ Chuẩn hóa: Σ p(θᵢ | D) = 1                                          ║
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
    plt.savefig('grid_approximation_summary.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: grid_approximation_summary.png")
    plt.close()

# ============================================================================
# Main execution
# ============================================================================
if __name__ == "__main__":
    print("Generating grid approximation images for Chapter 02...")
    print("=" * 70)
    
    generate_grid_basics()
    generate_grid_statistics()
    generate_posterior_predictive()
    generate_method_comparison()
    generate_curse_dimensionality()
    generate_mixture_prior_example()
    generate_grid_summary()
    
    print("=" * 70)
    print("✓ All grid approximation images generated successfully!")
    print("\nGenerated files:")
    print("  1. grid_approximation_basics.png")
    print("  2. grid_statistics_computation.png")
    print("  3. grid_posterior_predictive.png")
    print("  4. methods_comparison_grid.png")
    print("  5. curse_of_dimensionality.png")
    print("  6. grid_mixture_prior_example.png")
    print("  7. grid_approximation_summary.png")
