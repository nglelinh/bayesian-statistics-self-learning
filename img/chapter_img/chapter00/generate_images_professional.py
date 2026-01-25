#!/usr/bin/env python3
"""
Script tạo hình ảnh minh họa CHUYÊN NGHIỆP cho Bài 0.8: P-values và Kiểm định Giả thuyết

Cải tiến:
- Modern color schemes
- Professional typography
- Better visual hierarchy
- Cleaner layouts
- Publication-quality output

Tác giả: Nguyen Le Linh
Ngày: 24/01/2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import os

# ============ CẤU HÌNH STYLE CHUYÊN NGHIỆP ============

# Color palette - Modern and professional
COLORS = {
    'primary': '#2E86AB',      # Professional blue
    'secondary': '#A23B72',     # Deep magenta
    'accent': '#F18F01',        # Vibrant orange
    'success': '#06A77D',       # Teal green
    'warning': '#D62246',       # Strong red
    'neutral_dark': '#2B2D42',  # Dark navy
    'neutral_light': '#EDF2F4', # Light gray
    'background': '#FFFFFF'     # White
}

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette([COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['success']])

# Font configuration
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'figure.titleweight': 'bold',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'axes.facecolor': COLORS['background'],
    'figure.facecolor': COLORS['background']
})

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_figure(filename, dpi=300):
    """Lưu figure chất lượng cao"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f'✓ Đã tạo: {filename}')
    plt.close()

def add_watermark(ax, text="Bayesian Statistics Course"):
    """Thêm watermark nhẹ"""
    ax.text(0.99, 0.01, text, transform=ax.transAxes,
            fontsize=8, color='gray', alpha=0.3,
            ha='right', va='bottom', style='italic')

# ============ HÌNH 1: P-VALUE TRONG KIỂM ĐỊNH T ============

def generate_pvalue_ttest_professional():
    """Hình 1: Minh họa P-value chuyên nghiệp"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    df = 24
    t_obs = 2.02
    x = np.linspace(-4, 4, 1000)
    y = stats.t.pdf(x, df)
    
    # Main distribution curve
    ax.plot(x, y, color=COLORS['primary'], linewidth=3, label='Phân phối t (df=24)', zorder=3)
    ax.fill_between(x, y, alpha=0.1, color=COLORS['primary'])
    
    # P-value regions - right tail
    x_right = x[x >= t_obs]
    y_right = stats.t.pdf(x_right, df)
    ax.fill_between(x_right, y_right, alpha=0.6, color=COLORS['warning'], 
                    label='P-value region (phải)', edgecolor=COLORS['warning'], linewidth=2)
    
    # P-value regions - left tail
    x_left = x[x <= -t_obs]
    y_left = stats.t.pdf(x_left, df)
    ax.fill_between(x_left, y_left, alpha=0.6, color=COLORS['warning'],
                    label='P-value region (trái)', edgecolor=COLORS['warning'], linewidth=2)
    
    # Observed t-statistic
    ax.axvline(t_obs, color=COLORS['accent'], linestyle='--', linewidth=3, 
              label=f't quan sát = {t_obs}', zorder=4)
    ax.axvline(-t_obs, color=COLORS['accent'], linestyle='--', linewidth=3, zorder=4)
    
    # Central line
    ax.axvline(0, color=COLORS['neutral_dark'], linestyle=':', alpha=0.4, linewidth=2)
    
    # P-value annotation
    p_value = 2 * (1 - stats.t.cdf(t_obs, df))
    ax.annotate(f'P-value = {p_value:.4f}', 
                xy=(t_obs, stats.t.pdf(t_obs, df)), 
                xytext=(t_obs + 0.8, 0.25),
                arrowprops=dict(arrowstyle='->', lw=2, color=COLORS['accent']),
                fontsize=14, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.8', facecolor='white', 
                         edgecolor=COLORS['accent'], linewidth=2))
    
    # Interpretation box
    interpretation = ("P-value cho biết: Nếu H₀ đúng (μ = 170),\n"
                     "xác suất quan sát được |t| ≥ 2.02 là 5.4%")
    ax.text(0, 0.35, interpretation,
            fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=1', facecolor=COLORS['neutral_light'], 
                     edgecolor=COLORS['primary'], linewidth=2, alpha=0.9))
    
    ax.set_xlabel('Giá trị t-statistic', fontsize=13, fontweight='bold')
    ax.set_ylabel('Mật độ xác suất', fontsize=13, fontweight='bold')
    ax.set_title('P-value trong Kiểm định T\nVí dụ: Kiểm định chiều cao trung bình nam sinh viên', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=11, framealpha=0.95)
    ax.set_ylim(0, ax.get_ylim()[1] * 1.1)
    
    add_watermark(ax)
    plt.tight_layout()
    save_figure('pvalue_ttest_illustration.png')

# ============ HÌNH 2: EFFECT SIZE VS SAMPLE SIZE ============

def generate_effect_vs_sample_professional():
    """Hình 2: So sánh Effect Size và Sample Size"""
    fig = plt.figure(figsize=(16, 8))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    np.random.seed(42)
    
    # === CASE 1: Small effect, Large sample ===
    ax1 = fig.add_subplot(gs[0, :])
    n_large = 1000
    effect_small = 0.5
    
    group1 = np.random.normal(175.0, 7, n_large)
    group2 = np.random.normal(175.0 + effect_small, 7, n_large)
    
    # Histogram with KDE
    ax1.hist(group1, bins=40, alpha=0.5, label='Nhóm A (μ = 175 cm)', 
            color=COLORS['primary'], edgecolor='white', density=True)
    ax1.hist(group2, bins=40, alpha=0.5, label='Nhóm B (μ = 175.5 cm)',
            color=COLORS['secondary'], edgecolor='white', density=True)
    
    # Means
    ax1.axvline(group1.mean(), color=COLORS['primary'], linestyle='--', linewidth=3, alpha=0.8)
    ax1.axvline(group2.mean(), color=COLORS['secondary'], linestyle='--', linewidth=3, alpha=0.8)
    
    # Effect size annotation
    ax1.annotate('', xy=(group2.mean(), 0.055), xytext=(group1.mean(), 0.055),
                arrowprops=dict(arrowstyle='<->', lw=3, color=COLORS['accent']))
    ax1.text((group1.mean() + group2.mean())/2, 0.056, 
            f'Δ = {effect_small} cm', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=COLORS['accent'], linewidth=2))
    
    t_stat, p_val = stats.ttest_ind(group1, group2)
    title_text = (f'Hiệu ứng NHỎ, Mẫu LỚN\n'
                 f'Effect size = {effect_small} cm, n = {n_large} mỗi nhóm\n'
                 f'p-value = {p_val:.6f} {"✓ Có ý nghĩa thống kê!" if p_val < 0.05 else "✗ Không có ý nghĩa"}')
    ax1.set_title(title_text, fontsize=14, fontweight='bold', 
                 color=COLORS['success'] if p_val < 0.05 else COLORS['warning'])
    ax1.set_xlabel('Chiều cao (cm)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Mật độ', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=11)
    
    # === CASE 2: Large effect, Small sample ===
    ax2 = fig.add_subplot(gs[1, :])
    n_small = 20
    effect_large = 5
    
    group3 = np.random.normal(175.0, 7, n_small)
    group4 = np.random.normal(175.0 + effect_large, 7, n_small)
    
    # Histogram
    ax2.hist(group3, bins=8, alpha=0.6, label='Nhóm C (μ = 175 cm)',
            color=COLORS['success'], edgecolor='white', density=True)
    ax2.hist(group4, bins=8, alpha=0.6, label='Nhóm D (μ = 180 cm)',
            color=COLORS['accent'], edgecolor='white', density=True)
    
    # Means
    ax2.axvline(group3.mean(), color=COLORS['success'], linestyle='--', linewidth=3, alpha=0.8)
    ax2.axvline(group4.mean(), color=COLORS['accent'], linestyle='--', linewidth=3, alpha=0.8)
    
    # Effect size annotation
    mid_y = 0.05
    ax2.annotate('', xy=(group4.mean(), mid_y), xytext=(group3.mean(), mid_y),
                arrowprops=dict(arrowstyle='<->', lw=3, color=COLORS['warning']))
    ax2.text((group3.mean() + group4.mean())/2, mid_y + 0.002,
            f'Δ = {effect_large} cm', ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor=COLORS['warning'], linewidth=2))
    
    t_stat2, p_val2 = stats.ttest_ind(group3, group4)
    title_text2 = (f'Hiệu ứng LỚN, Mẫu NHỎ\n'
                  f'Effect size = {effect_large} cm, n = {n_small} mỗi nhóm\n'
                  f'p-value = {p_val2:.4f} {"✓ Có ý nghĩa thống kê!" if p_val2 < 0.05 else "⚠ Có thể không có ý nghĩa"}')
    ax2.set_title(title_text2, fontsize=14, fontweight='bold',
                 color=COLORS['success'] if p_val2 < 0.05 else COLORS['warning'])
    ax2.set_xlabel('Chiều cao (cm)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Mật độ', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=11)
    
    # Add main message
    fig.suptitle('Bài học: P-value phụ thuộc vào CẢ effect size VÀ sample size!\n' +
                'Effect size nhỏ + mẫu lớn → p-value nhỏ (nhưng không quan trọng thực tế)',
                fontsize=16, fontweight='bold', y=0.98)
    
    save_figure('effect_size_vs_sample_size.png')

# ============ HÌNH 3: MULTIPLE TESTING ============

def generate_multiple_testing_professional():
    """Hình 3: Multiple Testing Problem - P-hacking"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[2, 1])
    
    np.random.seed(123)
    n_tests = 20
    alpha = 0.05
    
    # Simulation
    p_values = []
    for i in range(n_tests):
        group1 = np.random.normal(0, 1, 30)
        group2 = np.random.normal(0, 1, 30)  # Same distribution - H0 is true!
        _, p = stats.ttest_ind(group1, group2)
        p_values.append(p)
    
    # Plot 1: P-values bar chart
    colors = [COLORS['warning'] if p < alpha else COLORS['primary'] for p in p_values]
    bars = ax1.bar(range(1, n_tests+1), p_values, color=colors, alpha=0.8, 
                   edgecolor='white', linewidth=2)
    
    # Threshold line
    ax1.axhline(y=alpha, color=COLORS['warning'], linestyle='--', linewidth=3, 
               label=f'Ngưỡng α = {alpha}', zorder=10)
    
    # Highlight significant results
    significant_indices = [i+1 for i, p in enumerate(p_values) if p < alpha]
    significant_count = len(significant_indices)
    
    for idx in significant_indices:
        ax1.text(idx, p_values[idx-1] + 0.05, '!', ha='center', fontsize=20,
                color=COLORS['warning'], fontweight='bold')
    
    # Info box
    info_text = (f'Tìm thấy: {significant_count}/{n_tests} "có ý nghĩa"\n'
                f'Nhưng TẤT CẢ đều là False Positives!\n'
                f'(H₀ đúng cho tất cả 20 kiểm định)')
    ax1.text(10.5, 0.75, info_text, fontsize=12, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=1', facecolor='white', 
                     edgecolor=COLORS['warning'], linewidth=3))
    
    expected = n_tests * alpha
    ax1.text(10.5, 0.2, f'Kỳ vọng: {expected:.1f} false positives', 
            fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round,pad=0.7', facecolor=COLORS['neutral_light'], 
                     edgecolor=COLORS['primary'], linewidth=2))
    
    ax1.set_xlabel('Số thứ tự kiểm định', fontsize=12, fontweight='bold')
    ax1.set_ylabel('P-value', fontsize=12, fontweight='bold')
    ax1.set_title('Multiple Testing Problem: Nếu làm 20 kiểm định với α=0.05,\n' +
                 'khoảng 1 kiểm định sẽ cho "có ý nghĩa" ngay cả khi H₀ đúng!',
                 fontsize=14, fontweight='bold', color=COLORS['warning'])
    ax1.set_ylim(0, 1)
    ax1.legend(fontsize=11, loc='upper right')
    
    # Plot 2: Distribution of p-values under H0
    ax2.hist(p_values, bins=20, color=COLORS['primary'], alpha=0.7, 
            edgecolor='white', linewidth=2, density=True)
    ax2.axhline(y=1, color=COLORS['neutral_dark'], linestyle='--', linewidth=2,
               label='Phân phối đều (H₀ đúng)')
    ax2.axvline(x=alpha, color=COLORS['warning'], linestyle='--', linewidth=3)
    
    ax2.set_xlabel('P-value', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Mật độ', fontsize=12, fontweight='bold')
    ax2.set_title('Khi H₀ đúng, p-values có phân phối đều từ 0 đến 1',
                 fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.set_xlim(0, 1)
    
    plt.tight_layout()
    save_figure('multiple_testing_problem.png')

# ============ MAIN ============

def main():
    print('='*70)
    print(' TẠO HÌNH ẢNH MINH HỌA CHUYÊN NGHIỆP - CHAPTER 00')
    print('='*70)
    print()
    
    print('[1/3] P-value trong kiểm định T...')
    generate_pvalue_ttest_professional()
    
    print('[2/3] Effect Size vs Sample Size...')
    generate_effect_vs_sample_professional()
    
    print('[3/3] Multiple Testing Problem...')
    generate_multiple_testing_professional()
    
    print()
    print('='*70)
    print(' ✓ HOÀN THÀNH! Tất cả hình ảnh đã được tạo.')
    print('='*70)
    print(f'\nThư mục output: {OUTPUT_DIR}')

if __name__ == '__main__':
    main()
