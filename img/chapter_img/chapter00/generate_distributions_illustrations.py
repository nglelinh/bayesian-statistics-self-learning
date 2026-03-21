#!/usr/bin/env python3
"""
Generate illustration images for common probability distributions
for lesson 00_02_common_distributions
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory if needed
import os
os.makedirs('distributions', exist_ok=True)

# Vietnamese font support (optional, falls back to default if not available)
try:
    plt.rcParams['font.family'] = 'DejaVu Sans'
except:
    pass

plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

def save_figure(filename):
    """Helper function to save figures"""
    plt.tight_layout()
    plt.savefig(f'distributions/{filename}', dpi=150, bbox_inches='tight')
    print(f"✓ Saved: distributions/{filename}")
    plt.close()


# ============================================================================
# 1. BERNOULLI DISTRIBUTION
# ============================================================================
def plot_bernoulli():
    """Plot Bernoulli distribution for different p values"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    p_values = [0.3, 0.5, 0.8]
    
    for ax, p in zip(axes, p_values):
        # Plot PMF
        x = [0, 1]
        probs = [1-p, p]
        
        bars = ax.bar(x, probs, width=0.4, alpha=0.7, edgecolor='black', linewidth=2)
        bars[0].set_color('#e74c3c')  # Red for failure
        bars[1].set_color('#2ecc71')  # Green for success
        
        # Annotations
        ax.text(0, (1-p)/2, f'{1-p:.1f}', ha='center', va='center', 
                fontsize=14, fontweight='bold', color='white')
        ax.text(1, p/2, f'{p:.1f}', ha='center', va='center',
                fontsize=14, fontweight='bold', color='white')
        
        ax.set_xlabel('Kết quả (0=Thất bại, 1=Thành công)', fontsize=12)
        ax.set_ylabel('Xác suất P(X=x)', fontsize=12)
        ax.set_title(f'Bernoulli(p={p})', fontsize=14, fontweight='bold')
        ax.set_xticks([0, 1])
        ax.set_ylim([0, 1.1])
        ax.grid(axis='y', alpha=0.3)
    
    fig.suptitle('Phân phối Bernoulli - Thí nghiệm Nhị phân', 
                 fontsize=16, fontweight='bold', y=1.02)
    save_figure('bernoulli_distribution.png')


# ============================================================================
# 2. BINOMIAL DISTRIBUTION
# ============================================================================
def plot_binomial():
    """Plot Binomial distribution for different n and p values"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    scenarios = [
        (10, 0.5, 'n=10, p=0.5 (Đồng xu cân bằng)'),
        (20, 0.5, 'n=20, p=0.5 (Nhiều lần thử)'),
        (20, 0.3, 'n=20, p=0.3 (Lệch trái)'),
        (20, 0.7, 'n=20, p=0.7 (Lệch phải)')
    ]
    
    for ax, (n, p, title) in zip(axes.flat, scenarios):
        x = np.arange(0, n+1)
        pmf = stats.binom.pmf(x, n, p)
        
        bars = ax.bar(x, pmf, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # Color gradient based on value
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(bars)))
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        # Mark mean
        mean = n * p
        ax.axvline(mean, color='red', linestyle='--', linewidth=2, 
                   label=f'Trung bình = {mean:.1f}')
        
        ax.set_xlabel('Số lần thành công (k)', fontsize=11)
        ax.set_ylabel('Xác suất P(X=k)', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
    
    fig.suptitle('Phân phối Binomial - Đếm Số lần Thành công', 
                 fontsize=16, fontweight='bold')
    save_figure('binomial_distribution.png')


# ============================================================================
# 3. POISSON DISTRIBUTION
# ============================================================================
def plot_poisson():
    """Plot Poisson distribution for different lambda values"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    lambdas = [1, 3, 6, 10]
    titles = [
        'λ=1 (Sự kiện rất hiếm)',
        'λ=3 (Sự kiện hiếm)',
        'λ=6 (Sự kiện trung bình)',
        'λ=10 (Sự kiện thường xuyên)'
    ]
    
    for ax, lam, title in zip(axes.flat, lambdas, titles):
        x = np.arange(0, max(25, lam*3))
        pmf = stats.poisson.pmf(x, lam)
        
        bars = ax.bar(x, pmf, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # Color gradient
        colors = plt.cm.plasma(np.linspace(0.2, 0.9, len(bars)))
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        # Mark mean = variance
        ax.axvline(lam, color='red', linestyle='--', linewidth=2,
                   label=f'λ = μ = σ² = {lam}')
        
        ax.set_xlabel('Số sự kiện (k)', fontsize=11)
        ax.set_ylabel('Xác suất P(X=k)', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        ax.set_xlim([-0.5, min(25, lam*3)])
    
    fig.suptitle('Phân phối Poisson - Đếm Sự kiện Hiếm', 
                 fontsize=16, fontweight='bold')
    save_figure('poisson_distribution.png')


# ============================================================================
# 4. NORMAL (GAUSSIAN) DISTRIBUTION
# ============================================================================
def plot_normal():
    """Plot Normal distribution with 68-95-99.7 rule"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left: Different parameters
    ax = axes[0]
    x = np.linspace(-10, 10, 1000)
    
    params = [(0, 1, 'μ=0, σ=1 (Standard Normal)'),
              (0, 2, 'μ=0, σ=2 (Rộng hơn)'),
              (2, 1, 'μ=2, σ=1 (Dịch phải)')]
    
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    
    for (mu, sigma, label), color in zip(params, colors):
        pdf = stats.norm.pdf(x, mu, sigma)
        ax.plot(x, pdf, linewidth=3, label=label, color=color)
        ax.fill_between(x, pdf, alpha=0.2, color=color)
    
    ax.set_xlabel('Giá trị x', fontsize=12)
    ax.set_ylabel('Mật độ xác suất f(x)', fontsize=12)
    ax.set_title('Phân phối Chuẩn với Tham số Khác nhau', 
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    
    # Right: 68-95-99.7 rule
    ax = axes[1]
    mu, sigma = 0, 1
    x = np.linspace(-4, 4, 1000)
    pdf = stats.norm.pdf(x, mu, sigma)
    
    ax.plot(x, pdf, linewidth=3, color='black', label='Phân phối Chuẩn')
    
    # Fill areas
    # 68% (1 sigma)
    x1 = x[(x >= -1) & (x <= 1)]
    ax.fill_between(x1, stats.norm.pdf(x1, mu, sigma), 
                     alpha=0.3, color='green', label='68% (±1σ)')
    
    # 95% (2 sigma)
    x2 = x[(x >= -2) & (x <= 2)]
    ax.fill_between(x2, stats.norm.pdf(x2, mu, sigma),
                     alpha=0.2, color='orange', label='95% (±2σ)')
    
    # 99.7% (3 sigma)
    x3 = x[(x >= -3) & (x <= 3)]
    ax.fill_between(x3, stats.norm.pdf(x3, mu, sigma),
                     alpha=0.1, color='red', label='99.7% (±3σ)')
    
    # Mark standard deviations
    for i in range(-3, 4):
        ax.axvline(i, color='gray', linestyle='--', alpha=0.5, linewidth=1)
        ax.text(i, -0.02, f'{i}σ', ha='center', fontsize=10)
    
    ax.set_xlabel('Độ lệch chuẩn từ trung bình', fontsize=12)
    ax.set_ylabel('Mật độ xác suất', fontsize=12)
    ax.set_title('Quy tắc 68-95-99.7', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    ax.set_ylim(bottom=-0.03)
    
    fig.suptitle('Phân phối Chuẩn (Gaussian)', 
                 fontsize=16, fontweight='bold', y=1.02)
    save_figure('normal_distribution.png')


# ============================================================================
# 5. BETA DISTRIBUTION
# ============================================================================
def plot_beta():
    """Plot Beta distribution for different alpha and beta values"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    scenarios = [
        (1, 1, 'α=1, β=1 (Đồng nhất)'),
        (2, 2, 'α=2, β=2 (Đối xứng, ít chắc chắn)'),
        (5, 5, 'α=5, β=5 (Đối xứng, chắc chắn hơn)'),
        (2, 5, 'α=2, β=5 (Lệch trái)'),
        (5, 2, 'α=5, β=2 (Lệch phải)'),
        (0.5, 0.5, 'α=0.5, β=0.5 (Hình chữ U)')
    ]
    
    x = np.linspace(0.001, 0.999, 1000)
    
    for ax, (alpha, beta, title) in zip(axes.flat, scenarios):
        pdf = stats.beta.pdf(x, alpha, beta)
        
        ax.plot(x, pdf, linewidth=3, color='#9b59b6')
        ax.fill_between(x, pdf, alpha=0.3, color='#9b59b6')
        
        # Mark mean
        mean = alpha / (alpha + beta)
        ax.axvline(mean, color='red', linestyle='--', linewidth=2,
                   label=f'Trung bình = {mean:.2f}')
        
        ax.set_xlabel('Xác suất p', fontsize=11)
        ax.set_ylabel('Mật độ f(p)', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        ax.set_xlim([0, 1])
    
    fig.suptitle('Phân phối Beta - Mô hình hóa Xác suất', 
                 fontsize=16, fontweight='bold')
    save_figure('beta_distribution.png')


# ============================================================================
# 6. EXPONENTIAL DISTRIBUTION
# ============================================================================
def plot_exponential():
    """Plot Exponential distribution for different lambda values"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left: Different rates
    ax = axes[0]
    x = np.linspace(0, 5, 1000)
    
    lambdas = [0.5, 1.0, 2.0]
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    
    for lam, color in zip(lambdas, colors):
        pdf = stats.expon.pdf(x, scale=1/lam)
        ax.plot(x, pdf, linewidth=3, label=f'λ={lam}', color=color)
        ax.fill_between(x, pdf, alpha=0.2, color=color)
        
        # Mark mean
        mean = 1/lam
        ax.axvline(mean, color=color, linestyle='--', alpha=0.7,
                   label=f'μ={mean:.1f}')
    
    ax.set_xlabel('Thời gian chờ đợi (t)', fontsize=12)
    ax.set_ylabel('Mật độ f(t)', fontsize=12)
    ax.set_title('Phân phối Mũ với Tham số Khác nhau',
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=10, ncol=2)
    ax.grid(alpha=0.3)
    
    # Right: Memoryless property illustration
    ax = axes[1]
    lam = 1.0
    x = np.linspace(0, 5, 1000)
    pdf = stats.expon.pdf(x, scale=1/lam)
    
    ax.plot(x, pdf, linewidth=3, color='#2c3e50', label='Phân phối gốc')
    ax.fill_between(x, pdf, alpha=0.2, color='#2c3e50')
    
    # Shifted distribution (memoryless)
    shift = 1.0
    x_shifted = x[x >= shift] - shift
    pdf_shifted = stats.expon.pdf(x_shifted, scale=1/lam)
    ax.plot(x[x >= shift], pdf_shifted, linewidth=3, linestyle='--',
            color='#e74c3c', label=f'Sau khi chờ {shift}s (giống hệt!)')
    
    ax.axvline(shift, color='gray', linestyle=':', alpha=0.7, linewidth=2)
    ax.text(shift, ax.get_ylim()[1]*0.9, 'Đã chờ 1s', 
            ha='center', fontsize=11, bbox=dict(boxstyle='round', facecolor='wheat'))
    
    ax.set_xlabel('Thời gian (t)', fontsize=12)
    ax.set_ylabel('Mật độ f(t)', fontsize=12)
    ax.set_title('Tính Không Nhớ của Phân phối Mũ',
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    
    fig.suptitle('Phân phối Mũ - Thời gian Chờ đợi', 
                 fontsize=16, fontweight='bold', y=1.02)
    save_figure('exponential_distribution.png')


# ============================================================================
# 7. GAMMA DISTRIBUTION
# ============================================================================
def plot_gamma():
    """Plot Gamma distribution for different alpha and beta values"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    scenarios = [
        (1, 1, 'α=1, β=1 (Giống Exponential)'),
        (2, 1, 'α=2, β=1 (Thời gian cho 2 sự kiện)'),
        (3, 2, 'α=3, β=2'),
        (5, 1, 'α=5, β=1')
    ]
    
    x = np.linspace(0.01, 15, 1000)
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    
    for ax, (alpha, beta, title), color in zip(axes.flat, scenarios, colors):
        pdf = stats.gamma.pdf(x, a=alpha, scale=1/beta)
        
        ax.plot(x, pdf, linewidth=3, color=color)
        ax.fill_between(x, pdf, alpha=0.3, color=color)
        
        # Mark mean
        mean = alpha / beta
        ax.axvline(mean, color='red', linestyle='--', linewidth=2,
                   label=f'Trung bình = {mean:.2f}')
        
        ax.set_xlabel('Giá trị x', fontsize=11)
        ax.set_ylabel('Mật độ f(x)', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        ax.set_xlim([0, 15])
    
    fig.suptitle('Phân phối Gamma - Tổng quát hóa Phân phối Mũ',
                 fontsize=16, fontweight='bold')
    save_figure('gamma_distribution.png')


# ============================================================================
# 8. COMPARISON CHART - All distributions overview
# ============================================================================
def plot_distributions_overview():
    """Create a summary comparison of all distributions"""
    fig = plt.figure(figsize=(18, 12))
    
    # Create a table-like layout
    info = [
        ['Phân phối', 'Loại', 'Tham số', 'Support', 'Ứng dụng điển hình'],
        ['Bernoulli', 'Rời rạc', 'p ∈ (0,1)', '{0, 1}', 'Thí nghiệm nhị phân đơn lẻ'],
        ['Binomial', 'Rời rạc', 'n ∈ ℕ, p ∈ (0,1)', '{0,1,...,n}', 'Đếm số thành công trong n lần thử'],
        ['Poisson', 'Rời rạc', 'λ > 0', '{0,1,2,...}', 'Đếm sự kiện hiếm'],
        ['Normal', 'Liên tục', 'μ ∈ ℝ, σ² > 0', '(-∞, ∞)', 'Sai số đo lường, CLT'],
        ['Beta', 'Liên tục', 'α > 0, β > 0', '(0, 1)', 'Mô hình hóa xác suất (prior)'],
        ['Exponential', 'Liên tục', 'λ > 0', '(0, ∞)', 'Thời gian chờ sự kiện đầu tiên'],
        ['Gamma', 'Liên tục', 'α > 0, β > 0', '(0, ∞)', 'Thời gian chờ k sự kiện, prior'],
    ]
    
    # Create table
    ax = fig.add_subplot(111)
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=info[1:], colLabels=info[0],
                     cellLoc='left', loc='center',
                     colWidths=[0.15, 0.1, 0.2, 0.15, 0.4])
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 3)
    
    # Style header
    for i in range(len(info[0])):
        table[(0, i)].set_facecolor('#3498db')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(info)):
        for j in range(len(info[0])):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#ecf0f1')
            else:
                table[(i, j)].set_facecolor('white')
    
    plt.title('Tổng quan Các Phân phối Xác suất Quan trọng',
              fontsize=18, fontweight='bold', pad=20)
    
    save_figure('distributions_overview.png')


# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == '__main__':
    print("\n" + "="*60)
    print("Generating illustrations for Common Probability Distributions")
    print("="*60 + "\n")
    
    print("1. Generating Bernoulli distribution...")
    plot_bernoulli()
    
    print("2. Generating Binomial distribution...")
    plot_binomial()
    
    print("3. Generating Poisson distribution...")
    plot_poisson()
    
    print("4. Generating Normal distribution...")
    plot_normal()
    
    print("5. Generating Beta distribution...")
    plot_beta()
    
    print("6. Generating Exponential distribution...")
    plot_exponential()
    
    print("7. Generating Gamma distribution...")
    plot_gamma()
    
    print("8. Generating distributions overview...")
    plot_distributions_overview()
    
    print("\n" + "="*60)
    print("✓ All illustrations generated successfully!")
    print("✓ Images saved in: distributions/")
    print("="*60 + "\n")
