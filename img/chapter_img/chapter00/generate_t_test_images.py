#!/usr/bin/env python3
"""
Script tạo hình ảnh minh họa cho Bài 0.9: T-test và Phân phối T

Tác giả: Nguyen Le Linh
Ngày: 24/01/2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Modern professional color scheme
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#06A77D',
    'warning': '#D62246',
    'neutral': '#2B2D42',
    'light': '#EDF2F4'
}

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'figure.titlesize': 16,
    'figure.titleweight': 'bold'
})

import os
OUTPUT_DIR = '/Users/nguyenlelinh/teaching/bayesian-statistics-self-learning/img/chapter_img/chapter00'

def save_figure(filename, dpi=300):
    """Lưu figure chất lượng cao"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f'✓ Đã tạo: {filename}')
    plt.close()

# ============ HÌNH 1: T vs NORMAL DISTRIBUTION ============

def generate_t_vs_normal():
    """So sánh phân phối T với Normal"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.linspace(-4, 4, 1000)
    
    # Normal distribution
    normal = stats.norm.pdf(x)
    ax.plot(x, normal, color='black', linewidth=3, label='Phân phối Chuẩn (df = ∞)', linestyle='--')
    
    # T-distributions với df khác nhau
    dfs = [2, 5, 10, 30]
    colors = [COLORS['warning'], COLORS['accent'], COLORS['primary'], COLORS['success']]
    
    for df, color in zip(dfs, colors):
        t_dist = stats.t.pdf(x, df)
        ax.plot(x, t_dist, color=color, linewidth=2.5, label=f'Phân phối t (df = {df})', alpha=0.8)
        ax.fill_between(x, t_dist, alpha=0.1, color=color)
    
    # Annotations
    ax.annotate('Đuôi dày hơn với\ndf nhỏ', xy=(-3, 0.02), xytext=(-3.5, 0.15),
                arrowprops=dict(arrowstyle='->', lw=2, color=COLORS['warning']),
                fontsize=11, bbox=dict(boxstyle='round', facecolor='white', edgecolor=COLORS['warning'], linewidth=2))
    
    ax.annotate('Hội tụ về phân phối\nchuẩn khi df lớn', xy=(0, 0.38), xytext=(1.5, 0.45),
                arrowprops=dict(arrowstyle='->', lw=2, color=COLORS['success']),
                fontsize=11, bbox=dict(boxstyle='round', facecolor='white', edgecolor=COLORS['success'], linewidth=2))
    
    ax.set_xlabel('Giá trị', fontsize=13, fontweight='bold')
    ax.set_ylabel('Mật độ', fontsize=13, fontweight='bold')
    ax.set_title('So sánh Phân phối T và Phân phối Chuẩn\nĐuôi dày hơn khi mẫu nhỏ (df nhỏ)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax.set_ylim(0, 0.5)
    
    plt.tight_layout()
    save_figure('t_vs_normal_distribution.png')

# ============ HÌNH 2: T-VALUE INTERPRETATION ============

def generate_t_value_interpretation():
    """Minh họa cách diễn giải t-value"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    df = 15
    x = np.linspace(-4, 4, 1000)
    t_pdf = stats.t.pdf(x, df)
    
    scenarios = [
        {'t': 0.5, 'color': COLORS['success'], 'title': 'T-value nhỏ (t = 0.5)'},
        {'t': 2.0, 'color': COLORS['accent'], 'title': 'T-value trung bình (t = 2.0)'},
        {'t': 3.0, 'color': COLORS['warning'], 'title': 'T-value lớn (t = 3.0)'},
        {'t': 0.7, 'color': COLORS['primary'], 'title': 'Ví dụ Chocolate (t = -0.70)'}
    ]
    
    for idx, (ax, scenario) in enumerate(zip(axes.flat, scenarios)):
        # Plot distribution
        ax.plot(x, t_pdf, color=COLORS['neutral'], linewidth=2, alpha=0.3)
        ax.fill_between(x, t_pdf, alpha=0.1, color=COLORS['neutral'])
        
        # Mark observed t-value
        t_val = scenario['t'] if idx < 3 else -scenario['t']
        ax.axvline(t_val, color=scenario['color'], linewidth=3, linestyle='--', 
                   label=f't = {t_val:.2f}')
        
        # Shade p-value region (two-tailed)
        if idx < 3:
            x_right = x[x >= abs(t_val)]
            y_right = stats.t.pdf(x_right, df)
            ax.fill_between(x_right, y_right, alpha=0.5, color=scenario['color'])
            
            x_left = x[x <= -abs(t_val)]
            y_left = stats.t.pdf(x_left, df)
            ax.fill_between(x_left, y_left, alpha=0.5, color=scenario['color'])
            
            p_val = 2 * (1 - stats.t.cdf(abs(t_val), df))
            ax.text(0, 0.35, f'p-value = {p_val:.4f}', ha='center', fontsize=12,
                    fontweight='bold', bbox=dict(boxstyle='round', facecolor='white', 
                    edgecolor=scenario['color'], linewidth=2))
        else:
            # Chocolate example
            x_right = x[x >= abs(t_val)]
            y_right = stats.t.pdf(x_right, df)
            ax.fill_between(x_right, y_right, alpha=0.5, color=scenario['color'])
            
            x_left = x[x <= -abs(t_val)]
            y_left = stats.t.pdf(x_left, df)
            ax.fill_between(x_left, y_left, alpha=0.5, color=scenario['color'])
            
            p_val = 2 * (1 - stats.t.cdf(abs(t_val), df))
            ax.text(0, 0.35, f'p = {p_val:.3f} > 0.05\nKhông bác bỏ H₀', ha='center', fontsize=11,
                    bbox=dict(boxstyle='round', facecolor='white', edgecolor=scenario['color'], linewidth=2))
        
        ax.set_title(scenario['title'], fontsize=13, fontweight='bold', color=scenario['color'])
        ax.set_xlabel('T-value', fontsize=11)
        ax.set_ylabel('Mật độ', fontsize=11)
        ax.legend(fontsize=10)
        ax.set_xlim(-4, 4)
    
    fig.suptitle('Diễn giải T-value: Từ nhỏ đến lớn\n(df = 15, α = 0.05, two-tailed)', 
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    save_figure('t_value_interpretation.png')

# ============ HÌNH 3: TYPES OF T-TESTS ============

def generate_t_test_types():
    """Minh họa 3 loại t-test"""
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    np.random.seed(42)
    
    # === ONE-SAMPLE T-TEST ===
    ax1 = fig.add_subplot(gs[0, :])
    
    # Data
    chocolate_data = np.array([98, 102, 97, 99, 101, 103, 98, 100, 99, 101, 97, 102, 100, 98, 101, 99])
    mu0 = 100
    
    ax1.scatter(range(len(chocolate_data)), chocolate_data, s=100, color=COLORS['primary'], 
                alpha=0.7, edgecolor='white', linewidth=2, label='Dữ liệu mẫu')
    ax1.axhline(mu0, color=COLORS['warning'], linewidth=3, linestyle='--', label=f'H₀: μ = {mu0}g')
    ax1.axhline(chocolate_data.mean(), color=COLORS['accent'], linewidth=3, label=f'x̄ = {chocolate_data.mean():.2f}g')
    
    # Statistics
    t_stat = (chocolate_data.mean() - mu0) / (chocolate_data.std(ddof=1) / np.sqrt(len(chocolate_data)))
    p_val = 2 * (1 - stats.t.cdf(abs(t_stat), len(chocolate_data)-1))
    
    info_text = f'ONE-SAMPLE T-TEST\nn = {len(chocolate_data)}, t = {t_stat:.2f}, p = {p_val:.3f}\nKết luận: Không đủ bằng chứng bác bỏ H₀'
    ax1.text(8, 104, info_text, ha='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round,pad=1', facecolor='white', edgecolor=COLORS['primary'], linewidth=2))
    
    ax1.set_xlabel('Số mẫu', fontsize=12)
    ax1.set_ylabel('Trọng lượng (g)', fontsize=12)
    ax1.set_title('1. One-sample T-test: So sánh trung bình mẫu với giá trị đã biết\nVí dụ: Kiểm tra trọng lượng chocolate', 
                  fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.set_ylim(95, 105)
    
    # === INDEPENDENT TWO-SAMPLE T-TEST ===
    ax2 = fig.add_subplot(gs[1, 0])
    
    group1 = np.random.normal(175, 7, 30)
    group2 = np.random.normal(178, 7, 30)
    
    bp = ax2.boxplot([group1, group2], labels=['Khoa A', 'Khoa B'], patch_artist=True,
                      boxprops=dict(facecolor=COLORS['primary'], alpha=0.6),
                      medianprops=dict(color=COLORS['warning'], linewidth=2))
    bp['boxes'][1].set_facecolor(COLORS['secondary'])
    
    # Statistics
    t_stat2, p_val2 = stats.ttest_ind(group1, group2)
    
    info_text2 = f'INDEPENDENT T-TEST\nt = {t_stat2:.2f}, p = {p_val2:.3f}'
    ax2.text(1.5, 195, info_text2, ha='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='white', edgecolor=COLORS['primary'], linewidth=2))
    
    ax2.set_ylabel('Chiều cao (cm)', fontsize=11)
    ax2.set_title('2. Independent Two-sample T-test\nSo sánh hai nhóm độc lập', fontsize=12, fontweight='bold')
    
    # === PAIRED T-TEST ===
    ax3 = fig.add_subplot(gs[1, 1])
    
    before = np.random.normal(85, 10, 20)
    after = before - np.random.normal(3, 2, 20)
    
    for i in range(len(before)):
        ax3.plot([0, 1], [before[i], after[i]], color=COLORS['neutral'], alpha=0.3, linewidth=1)
    
    ax3.scatter([0]*len(before), before, s=80, color=COLORS['warning'], alpha=0.7, label='Trước')
    ax3.scatter([1]*len(after), after, s=80, color=COLORS['success'], alpha=0.7, label='Sau')
    
    # Statistics
    t_stat3, p_val3 = stats.ttest_rel(before, after)
    
    info_text3 = f'PAIRED T-TEST\nt = {t_stat3:.2f}, p = {p_val3:.4f}'
    ax3.text(0.5, 105, info_text3, ha='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='white', edgecolor=COLORS['success'], linewidth=2))
    
    ax3.set_xticks([0, 1])
    ax3.set_xticklabels(['Trước dùng thuốc', 'Sau dùng thuốc'])
    ax3.set_ylabel('Cân nặng (kg)', fontsize=11)
    ax3.set_title('3. Paired T-test\nSo sánh cùng nhóm, hai thời điểm', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=10)
    
    # === SUMMARY TABLE ===
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis('off')
    
    table_text = """
    ╔═══════════════════════════════════════════════════════════════════════════════════════════╗
    ║                        SO SÁNH 3 LOẠI T-TEST                                              ║
    ╠═══════════════════════════════════════════════════════════════════════════════════════════╣
    ║                                                                                           ║
    ║  Loại           │  Mục đích                │  Công thức                │  df            ║
    ║ ────────────────┼──────────────────────────┼───────────────────────────┼─────────────── ║
    ║  One-sample     │  So sánh với giá trị     │  t = (x̄ - μ₀)/(s/√n)     │  n - 1         ║
    ║                 │  đã biết                 │                           │                ║
    ║                                                                                           ║
    ║  Two-sample     │  So sánh 2 nhóm          │  t = (x̄₁ - x̄₂)/SE        │  n₁ + n₂ - 2   ║
    ║  (Independent)  │  độc lập                 │                           │                ║
    ║                                                                                           ║
    ║  Paired         │  So sánh cùng nhóm,      │  t = d̄/(sₐ/√n)           │  n - 1         ║
    ║  (Dependent)    │  2 thời điểm             │                           │                ║
    ║                                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════════════════════╝
    """
    
    ax4.text(0.5, 0.5, table_text, ha='center', va='center', fontsize=10, family='monospace',
             bbox=dict(boxstyle='round', facecolor=COLORS['light'], edgecolor=COLORS['primary'], linewidth=2))
    
    fig.suptitle('Ba Loại T-test Phổ biến', fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    save_figure('t_test_types.png')

# ============ MAIN ============

def main():
    print('='*70)
    print(' TẠO HÌNH ẢNH MINH HỌA CHO BÀI 0.9: T-TEST')
    print('='*70)
    print()
    
    print('[1/3] So sánh T vs Normal distribution...')
    generate_t_vs_normal()
    
    print('[2/3] Diễn giải T-value...')
    generate_t_value_interpretation()
    
    print('[3/3] Ba loại T-test...')
    generate_t_test_types()
    
    print()
    print('='*70)
    print(' ✓ HOÀN THÀNH!')
    print('='*70)

if __name__ == '__main__':
    main()
