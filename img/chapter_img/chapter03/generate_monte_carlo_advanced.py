#!/usr/bin/env python3
"""
Script để tạo các hình ảnh minh họa nâng cao cho Chapter 03: Monte Carlo & Sampling

Các visualizations mới:
1. Curse of Dimensionality - chi tiết hơn
2. Monte Carlo Integration - convergence
3. Importance Sampling
4. Law of Large Numbers visualization
5. Central Limit Theorem for MCMC
6. Effective Sample Size

Sử dụng:
    python3 generate_monte_carlo_advanced.py

Yêu cầu:
    - numpy
    - matplotlib
    - scipy
    - seaborn

Tác giả: Nguyen Le Linh
Ngày: 09/03/2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.integrate import quad
import seaborn as sns
import os
import math

# Cấu hình style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# Tạo thư mục output nếu chưa tồn tại
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_figure(filename):
    """Lưu figure với đường dẫn đầy đủ"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f'✓ Đã tạo: {filename}')
    plt.close()

def generate_curse_of_dimensionality_detailed():
    """Hình 1: Curse of Dimensionality - Chi tiết"""
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Panel 1: Grid points explosion
    ax1 = fig.add_subplot(gs[0, :2])
    dimensions = np.arange(1, 11)
    points_per_dim = 10
    total_points = points_per_dim ** dimensions
    
    ax1.semilogy(dimensions, total_points, 'o-', linewidth=3, markersize=12,
                 color='darkred', markerfacecolor='red', markeredgewidth=2)
    ax1.set_xlabel('Số chiều (Dimensions)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Số điểm lưới (log scale)', fontsize=13, fontweight='bold')
    ax1.set_title('Curse of Dimensionality: Grid Points Explode\n10 điểm/chiều', 
                  fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(dimensions)
    
    # Annotations cho một số điểm
    for i in [2, 4, 6, 8, 9]:
        ax1.annotate(f'{total_points[i]:,.0f}', 
                     xy=(dimensions[i], total_points[i]),
                     xytext=(dimensions[i]+0.3, total_points[i]*3),
                     fontsize=10, ha='left',
                     arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                     bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.8))
    
    # Panel 2: Computational cost
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.axis('off')
    text1 = """
╔════════════════════════════╗
║   COMPUTATIONAL COST       ║
╠════════════════════════════╣
║                            ║
║  1D:  10 điểm              ║
║  2D:  100 điểm             ║
║  3D:  1,000 điểm           ║
║  4D:  10,000 điểm          ║
║  5D:  100,000 điểm         ║
║  10D: 10 tỷ điểm!          ║
║                            ║
║  → KHÔNG KHẢ THI!          ║
║                            ║
╚════════════════════════════╝
"""
    ax2.text(0.5, 0.5, text1, fontsize=10, family='monospace',
             ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.9))
    
    # Panel 3-5: Volume concentration
    # 1D case
    ax3 = fig.add_subplot(gs[1, 0])
    x = np.linspace(-3, 3, 1000)
    ax3.plot(x, stats.norm.pdf(x), 'b-', linewidth=3, label='N(0,1)')
    ax3.fill_between(x, stats.norm.pdf(x), alpha=0.3, color='blue')
    ax3.axvline(0, color='red', linestyle='--', linewidth=2, label='Mean')
    ax3.set_title('1D: Density ở Center', fontsize=11, fontweight='bold')
    ax3.set_xlabel('x', fontsize=10)
    ax3.set_ylabel('Density', fontsize=10)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    # 2D case - contour
    ax4 = fig.add_subplot(gs[1, 1])
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2)/2) / (2*np.pi)
    
    contour = ax4.contourf(X, Y, Z, levels=20, cmap='Blues')
    ax4.plot(0, 0, 'r*', markersize=20, label='Mean')
    ax4.set_title('2D: Density vẫn ở Center', fontsize=11, fontweight='bold')
    ax4.set_xlabel('x₁', fontsize=10)
    ax4.set_ylabel('x₂', fontsize=10)
    ax4.legend(fontsize=9)
    ax4.set_aspect('equal')
    
    # High-D: Radial distance distribution
    ax5 = fig.add_subplot(gs[1, 2])
    dims = [1, 2, 5, 10, 20]
    colors = plt.cm.viridis(np.linspace(0, 1, len(dims)))
    r = np.linspace(0, 6, 1000)
    
    for d, color in zip(dims, colors):
        # Chi distribution for radial distance
        pdf = stats.chi(df=d).pdf(r)
        ax5.plot(r, pdf, linewidth=2.5, label=f'{d}D', color=color)
    
    ax5.set_title('High-D: Mass ở Shell!', fontsize=11, fontweight='bold')
    ax5.set_xlabel('Khoảng cách từ origin', fontsize=10)
    ax5.set_ylabel('Density', fontsize=10)
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3)
    ax5.text(4, 0.5, 'Càng nhiều chiều,\nđỉnh càng xa origin', 
             fontsize=9, ha='center',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Panel 6: Sampling coverage in high-D
    ax6 = fig.add_subplot(gs[2, :])
    
    # Simulate coverage
    n_samples = [10, 100, 1000, 10000]
    dimensions = [1, 2, 3, 5, 10]
    
    # Calculate "coverage" (very rough estimate)
    coverage = np.zeros((len(n_samples), len(dimensions)))
    for i, n in enumerate(n_samples):
        for j, d in enumerate(dimensions):
            # Rough estimate: coverage ~ (n / volume)^(1/d)
            # Volume of unit ball ~ π^(d/2) / Gamma(d/2 + 1)
            volume = np.pi**(d/2) / math.factorial(d//2) if d <= 10 else 1e10
            coverage[i, j] = min(1.0, (n / volume)**(1/d))
    
    x_pos = np.arange(len(dimensions))
    width = 0.2
    
    for i, (n, color) in enumerate(zip(n_samples, ['lightblue', 'skyblue', 'cornflowerblue', 'royalblue'])):
        ax6.bar(x_pos + i*width, coverage[i, :], width, 
                label=f'{n} samples', alpha=0.8, color=color, edgecolor='black')
    
    ax6.set_xlabel('Số chiều', fontsize=13, fontweight='bold')
    ax6.set_ylabel('Coverage (tỷ lệ không gian được cover)', fontsize=13, fontweight='bold')
    ax6.set_title('Grid Approximation: Coverage Suy Giảm với High-D\n' + 
                  'Cùng số samples, coverage giảm theo chiều!', 
                  fontsize=14, fontweight='bold')
    ax6.set_xticks(x_pos + width * 1.5)
    ax6.set_xticklabels([f'{d}D' for d in dimensions])
    ax6.legend(fontsize=10, loc='upper right')
    ax6.grid(True, alpha=0.3, axis='y')
    ax6.set_ylim([0, 1.1])
    
    # Add warning box
    ax6.text(2.5, 0.95, 
             '⚠️ CẢNH BÁO: Trong high-D, random samples cover RẤT ÍT không gian!\n' +
             'Grid approximation HOÀN TOÀN THẤT BẠI!', 
             fontsize=11, ha='center', va='top', color='darkred',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow', 
                      edgecolor='red', linewidth=3, alpha=0.9))
    
    save_figure('curse_of_dimensionality_detailed.png')

def generate_monte_carlo_integration_convergence():
    """Hình 2: Monte Carlo Integration - Convergence"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    # Target function: ∫₀¹ x² dx = 1/3
    def f(x):
        return x**2
    
    true_integral = 1/3
    
    # Sample sizes to test
    n_samples_list = [10, 50, 100, 500, 1000, 5000]
    n_replications = 1000  # Số lần lặp để ước lượng phân phối
    
    np.random.seed(42)
    
    for idx, n_samples in enumerate(n_samples_list):
        ax = axes[idx // 3, idx % 3]
        
        # Monte Carlo estimates from multiple replications
        estimates = []
        for _ in range(n_replications):
            samples = np.random.uniform(0, 1, n_samples)
            mc_estimate = np.mean(f(samples))
            estimates.append(mc_estimate)
        
        estimates = np.array(estimates)
        
        # Plot histogram
        ax.hist(estimates, bins=50, density=True, alpha=0.7, 
                color='skyblue', edgecolor='black')
        
        # True value
        ax.axvline(true_integral, color='red', linestyle='--', linewidth=3,
                   label=f'True = {true_integral:.4f}')
        
        # Sample mean
        mean_estimate = np.mean(estimates)
        ax.axvline(mean_estimate, color='green', linestyle='-', linewidth=2,
                   label=f'Mean = {mean_estimate:.4f}')
        
        # Theoretical Normal (CLT)
        std_estimate = np.std(estimates)
        x_range = np.linspace(estimates.min(), estimates.max(), 200)
        theoretical = stats.norm.pdf(x_range, true_integral, std_estimate)
        ax.plot(x_range, theoretical, 'purple', linewidth=2.5, 
                label='Theoretical N')
        
        ax.set_title(f'N = {n_samples} samples\nStd = {std_estimate:.4f}', 
                     fontsize=11, fontweight='bold')
        ax.set_xlabel('MC Estimate', fontsize=10)
        ax.set_ylabel('Density', fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        
        # Add RMSE
        rmse = np.sqrt(np.mean((estimates - true_integral)**2))
        ax.text(0.95, 0.95, f'RMSE: {rmse:.4f}', 
                transform=ax.transAxes, fontsize=9, ha='right', va='top',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    plt.suptitle('Monte Carlo Integration: Convergence với Sample Size\n' + 
                 'Target: ∫₀¹ x² dx = 1/3 | Error giảm theo 1/√N', 
                 fontsize=15, fontweight='bold')
    plt.tight_layout()
    save_figure('monte_carlo_integration_convergence.png')

def generate_law_of_large_numbers():
    """Hình 3: Law of Large Numbers cho MCMC"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    np.random.seed(42)
    
    # Target: Beta(2, 5) distribution
    true_mean = 2 / (2 + 5)
    
    # Generate MCMC samples (simple Metropolis)
    n_samples = 10000
    samples = [0.3]  # Initial value
    
    for _ in range(n_samples - 1):
        current = samples[-1]
        proposal = current + np.random.normal(0, 0.1)
        
        # Reject if out of bounds
        if proposal < 0 or proposal > 1:
            samples.append(current)
            continue
        
        # Metropolis acceptance
        current_density = stats.beta(2, 5).pdf(current)
        proposal_density = stats.beta(2, 5).pdf(proposal)
        
        acceptance_ratio = proposal_density / current_density
        if np.random.rand() < acceptance_ratio:
            samples.append(proposal)
        else:
            samples.append(current)
    
    samples = np.array(samples)
    
    # Panel 1: Running mean
    running_mean = np.cumsum(samples) / np.arange(1, len(samples) + 1)
    
    axes[0, 0].plot(running_mean, linewidth=2, color='blue', alpha=0.7)
    axes[0, 0].axhline(true_mean, color='red', linestyle='--', linewidth=3,
                       label=f'True mean = {true_mean:.3f}')
    axes[0, 0].set_xlabel('Iteration', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Running Mean', fontsize=12, fontweight='bold')
    axes[0, 0].set_title('Law of Large Numbers\nRunning Mean → True Mean', 
                         fontsize=13, fontweight='bold')
    axes[0, 0].legend(fontsize=11)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_xlim([0, n_samples])
    
    # Panel 2: Error convergence
    error = np.abs(running_mean - true_mean)
    
    axes[0, 1].semilogy(error, linewidth=2, color='darkred', alpha=0.7)
    axes[0, 1].set_xlabel('Iteration', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('|Error| (log scale)', fontsize=12, fontweight='bold')
    axes[0, 1].set_title('Error Convergence\nError → 0 as N → ∞', 
                         fontsize=13, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3, which='both')
    axes[0, 1].set_xlim([0, n_samples])
    
    # Add 1/sqrt(n) reference line
    x_ref = np.linspace(100, n_samples, 100)
    y_ref = 0.1 / np.sqrt(x_ref)
    axes[0, 1].plot(x_ref, y_ref, 'g--', linewidth=2, 
                    label='~ 1/√N', alpha=0.7)
    axes[0, 1].legend(fontsize=11)
    
    # Panel 3: Histogram of samples vs true density
    axes[1, 0].hist(samples[1000:], bins=50, density=True, alpha=0.7,
                    color='skyblue', edgecolor='black', label='MCMC samples')
    
    x_range = np.linspace(0, 1, 200)
    true_density = stats.beta(2, 5).pdf(x_range)
    axes[1, 0].plot(x_range, true_density, 'r-', linewidth=3,
                    label='True Beta(2,5)')
    
    axes[1, 0].axvline(true_mean, color='red', linestyle='--', linewidth=2,
                       label=f'True mean')
    axes[1, 0].axvline(np.mean(samples[1000:]), color='blue', linestyle='--', 
                       linewidth=2, label='Sample mean')
    
    axes[1, 0].set_xlabel('θ', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Density', fontsize=12, fontweight='bold')
    axes[1, 0].set_title('Sample Distribution vs True Distribution\n' + 
                         'Empirical → True as N → ∞', 
                         fontsize=13, fontweight='bold')
    axes[1, 0].legend(fontsize=10)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Panel 4: Convergence by batch
    batch_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    batch_means = []
    batch_stds = []
    
    for batch_size in batch_sizes:
        if batch_size <= len(samples):
            batch_samples = samples[:batch_size]
            batch_means.append(np.mean(batch_samples))
            batch_stds.append(np.std(batch_samples) / np.sqrt(batch_size))
    
    axes[1, 1].errorbar(batch_sizes[:len(batch_means)], batch_means, 
                        yerr=batch_stds, fmt='o-', linewidth=2, markersize=8,
                        capsize=5, capthick=2, color='blue', alpha=0.7,
                        label='Batch mean ± SE')
    axes[1, 1].axhline(true_mean, color='red', linestyle='--', linewidth=3,
                       label=f'True mean = {true_mean:.3f}')
    axes[1, 1].set_xscale('log')
    axes[1, 1].set_xlabel('Batch Size (log scale)', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('Estimate', fontsize=12, fontweight='bold')
    axes[1, 1].set_title('Mean Estimate vs Sample Size\n' + 
                         'Uncertainty ∝ 1/√N', 
                         fontsize=13, fontweight='bold')
    axes[1, 1].legend(fontsize=11)
    axes[1, 1].grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    save_figure('law_of_large_numbers_mcmc.png')

def generate_effective_sample_size():
    """Hình 4: Effective Sample Size - Autocorrelation Effect"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    np.random.seed(42)
    n_samples = 2000
    
    # Generate 3 chains with different autocorrelation
    # Chain 1: Low autocorr (good mixing)
    samples_good = [0.5]
    for _ in range(n_samples - 1):
        samples_good.append(samples_good[-1] + np.random.normal(0, 0.5))
    samples_good = np.clip(samples_good, 0, 1)
    
    # Chain 2: Medium autocorr
    samples_medium = [0.5]
    for _ in range(n_samples - 1):
        samples_medium.append(0.7 * samples_medium[-1] + np.random.normal(0, 0.2))
    samples_medium = np.clip(samples_medium, 0, 1)
    
    # Chain 3: High autocorr (poor mixing)
    samples_poor = [0.5]
    for _ in range(n_samples - 1):
        samples_poor.append(0.95 * samples_poor[-1] + np.random.normal(0, 0.05))
    samples_poor = np.clip(samples_poor, 0, 1)
    
    chains = [
        (samples_good, 'Good Mixing', 'green'),
        (samples_medium, 'Medium Mixing', 'orange'),
        (samples_poor, 'Poor Mixing', 'red')
    ]
    
    for idx, (samples, label, color) in enumerate(chains):
        # Trace plot
        axes[0, idx].plot(samples, linewidth=1, alpha=0.7, color=color)
        axes[0, idx].set_title(f'{label}\nN = {len(samples)}', 
                               fontsize=11, fontweight='bold')
        axes[0, idx].set_xlabel('Iteration', fontsize=10)
        axes[0, idx].set_ylabel('Value', fontsize=10)
        axes[0, idx].grid(True, alpha=0.3)
        
        # Autocorrelation plot
        max_lag = 100
        autocorr = np.correlate(samples - np.mean(samples), 
                                samples - np.mean(samples), mode='full')
        autocorr = autocorr[len(autocorr)//2:len(autocorr)//2 + max_lag]
        autocorr = autocorr / autocorr[0]
        
        axes[1, idx].bar(range(max_lag), autocorr, alpha=0.7, 
                         color=color, edgecolor='black', width=1)
        axes[1, idx].axhline(0, color='black', linestyle='-', linewidth=1)
        axes[1, idx].axhline(0.1, color='red', linestyle='--', linewidth=2,
                            label='Threshold = 0.1')
        axes[1, idx].set_xlabel('Lag', fontsize=10)
        axes[1, idx].set_ylabel('Autocorrelation', fontsize=10)
        axes[1, idx].set_title(f'Autocorrelation', fontsize=11, fontweight='bold')
        axes[1, idx].grid(True, alpha=0.3)
        axes[1, idx].set_ylim([-0.2, 1.1])
        
        # Calculate ESS
        # ESS ≈ N / (1 + 2 * sum of autocorrelations)
        ess = len(samples) / (1 + 2 * np.sum(autocorr[1:][autocorr[1:] > 0]))
        
        axes[1, idx].text(0.95, 0.95, 
                          f'ESS ≈ {ess:.0f}\n({ess/len(samples)*100:.1f}% of N)', 
                          transform=axes[1, idx].transAxes,
                          fontsize=10, ha='right', va='top',
                          bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
        
        if idx == 0:
            axes[1, idx].legend(fontsize=9)
    
    plt.suptitle('Effective Sample Size (ESS): Autocorrelation Matters!\n' + 
                 'High autocorrelation → Low ESS → Need more samples', 
                 fontsize=15, fontweight='bold')
    plt.tight_layout()
    save_figure('effective_sample_size_autocorrelation.png')

def main():
    """Hàm chính để tạo tất cả các hình ảnh"""
    print('='*70)
    print('BẮT ĐẦU TẠO HÌNH ẢNH NÂNG CAO CHO CHAPTER 03')
    print('='*70)
    print()
    
    print('Phần 1/4: Curse of Dimensionality (Chi tiết)')
    generate_curse_of_dimensionality_detailed()
    print('✓ Hoàn thành phần 1/4\n')
    
    print('Phần 2/4: Monte Carlo Integration Convergence')
    generate_monte_carlo_integration_convergence()
    print('✓ Hoàn thành phần 2/4\n')
    
    print('Phần 3/4: Law of Large Numbers')
    generate_law_of_large_numbers()
    print('✓ Hoàn thành phần 3/4\n')
    
    print('Phần 4/4: Effective Sample Size')
    generate_effective_sample_size()
    print('✓ Hoàn thành phần 4/4\n')
    
    print('='*70)
    print('TẤT CẢ HÌNH ẢNH ĐÃ ĐƯỢC TẠO THÀNH CÔNG!')
    print('='*70)
    print()
    print('Danh sách các file đã tạo:')
    print('1. curse_of_dimensionality_detailed.png')
    print('2. monte_carlo_integration_convergence.png')
    print('3. law_of_large_numbers_mcmc.png')
    print('4. effective_sample_size_autocorrelation.png')
    print()
    print(f'Thư mục output: {OUTPUT_DIR}')

if __name__ == '__main__':
    main()
