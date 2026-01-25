#!/usr/bin/env python3
"""
Script để tạo các hình ảnh minh họa cho Bài 0.8: P-values và Kiểm định Giả thuyết

Sử dụng:
    python3 generate_images.py

Yêu cầu:
    - numpy
    - matplotlib
    - scipy
    - seaborn

Tác giả: Nguyen Le Linh
Ngày: 10/01/2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import os

# Cấu hình style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
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

def generate_pvalue_ttest_illustration():
    """Hình 1: Minh họa P-value trong Kiểm định T"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Parameters từ ví dụ
    df = 24  # degrees of freedom
    t_obs = 2.02
    x = np.linspace(-4, 4, 1000)
    y = stats.t.pdf(x, df)
    
    # Vẽ phân phối t
    ax.plot(x, y, 'b-', linewidth=2, label='Phân phối t (df=24)')
    ax.axvline(0, color='gray', linestyle='--', alpha=0.5)
    
    # Tô vùng p-value (hai đuôi)
    x_right = x[x >= t_obs]
    y_right = stats.t.pdf(x_right, df)
    ax.fill_between(x_right, y_right, alpha=0.3, color='red', label=f'Vùng p-value (phải)')
    
    x_left = x[x <= -t_obs]
    y_left = stats.t.pdf(x_left, df)
    ax.fill_between(x_left, y_left, alpha=0.3, color='red', label=f'Vùng p-value (trái)')
    
    # Đánh dấu giá trị t quan sát
    ax.axvline(t_obs, color='red', linestyle='-', linewidth=2, label=f't quan sát = {t_obs}')
    ax.axvline(-t_obs, color='red', linestyle='-', linewidth=2)
    
    # Tính p-value
    p_value = 2 * (1 - stats.t.cdf(t_obs, df))
    ax.text(0, 0.35, f'p-value = {p_value:.4f}', 
            fontsize=14, ha='center', 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    ax.set_xlabel('Giá trị t', fontsize=12)
    ax.set_ylabel('Mật độ xác suất', fontsize=12)
    ax.set_title('Minh họa P-value trong Kiểm định T\n(Ví dụ: Chiều cao trung bình)', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_figure('pvalue_ttest_illustration.png')

def generate_effect_size_vs_sample_size():
    """Hình 2: So sánh Kích thước Hiệu ứng và Kích thước Mẫu"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Bên trái: Hiệu ứng nhỏ, mẫu lớn
    n_large = 1000
    effect_small = 0.5
    np.random.seed(42)
    group1_large = np.random.normal(175.0, 7, n_large)
    group2_large = np.random.normal(175.0 + effect_small, 7, n_large)
    
    axes[0].hist(group1_large, bins=30, alpha=0.6, label='Quần thể A', color='blue', density=True)
    axes[0].hist(group2_large, bins=30, alpha=0.6, label='Quần thể B', color='red', density=True)
    axes[0].axvline(group1_large.mean(), color='blue', linestyle='--', linewidth=2)
    axes[0].axvline(group2_large.mean(), color='red', linestyle='--', linewidth=2)
    
    t_stat, p_val = stats.ttest_ind(group1_large, group2_large)
    axes[0].set_title(f'Hiệu ứng nhỏ (0.5 cm), Mẫu lớn (n={n_large})\np-value = {p_val:.4f} ("có ý nghĩa")', 
                      fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Chiều cao (cm)', fontsize=11)
    axes[0].set_ylabel('Mật độ', fontsize=11)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Bên phải: Hiệu ứng lớn, mẫu nhỏ
    n_small = 20
    effect_large = 5
    group1_small = np.random.normal(175.0, 7, n_small)
    group2_small = np.random.normal(175.0 + effect_large, 7, n_small)
    
    axes[1].hist(group1_small, bins=10, alpha=0.6, label='Quần thể C', color='green', density=True)
    axes[1].hist(group2_small, bins=10, alpha=0.6, label='Quần thể D', color='orange', density=True)
    axes[1].axvline(group1_small.mean(), color='green', linestyle='--', linewidth=2)
    axes[1].axvline(group2_small.mean(), color='orange', linestyle='--', linewidth=2)
    
    t_stat2, p_val2 = stats.ttest_ind(group1_small, group2_small)
    axes[1].set_title(f'Hiệu ứng lớn (5 cm), Mẫu nhỏ (n={n_small})\np-value = {p_val2:.4f}', 
                      fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Chiều cao (cm)', fontsize=11)
    axes[1].set_ylabel('Mật độ', fontsize=11)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_figure('effect_size_vs_sample_size.png')

def generate_multiple_testing_problem():
    """Hình 3: Vấn đề Multiple Testing (P-hacking)"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    np.random.seed(123)
    n_tests = 20
    alpha = 0.05
    
    # Mô phỏng 20 kiểm định khi H0 đúng (không có hiệu ứng thực sự)
    p_values = []
    for i in range(n_tests):
        group1 = np.random.normal(0, 1, 30)
        group2 = np.random.normal(0, 1, 30)
        _, p = stats.ttest_ind(group1, group2)
        p_values.append(p)
    
    # Vẽ biểu đồ cột
    colors = ['red' if p < alpha else 'blue' for p in p_values]
    bars = ax.bar(range(1, n_tests+1), p_values, color=colors, alpha=0.7, edgecolor='black')
    
    # Thêm đường ngưỡng
    ax.axhline(y=alpha, color='red', linestyle='--', linewidth=2, label=f'Ngưỡng α = {alpha}')
    
    # Đánh dấu kết quả có ý nghĩa
    significant_count = sum(1 for p in p_values if p < alpha)
    ax.text(10.5, 0.85, f'Số kiểm định "có ý nghĩa": {significant_count}/{n_tests}\n(Tất cả đều là False Positives!)', 
            fontsize=13, ha='center', 
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    ax.set_xlabel('Số thứ tự kiểm định', fontsize=12)
    ax.set_ylabel('P-value', fontsize=12)
    ax.set_title('Vấn đề Multiple Testing: P-hacking\n(20 kiểm định khi H₀ đúng - không có hiệu ứng thực sự)', 
                 fontsize=14, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    expected_false_positives = n_tests * alpha
    ax.text(10.5, 0.15, f'Số False Positives kỳ vọng: {expected_false_positives:.1f}', 
            fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    plt.tight_layout()
    save_figure('multiple_testing_problem.png')

def generate_confidence_vs_credible_intervals():
    """Hình 4: So sánh Confidence Intervals và Credible Intervals"""
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # Mô phỏng confidence intervals
    np.random.seed(456)
    true_mean = 5.0
    n_samples = 30
    n_experiments = 50
    
    ci_lower = []
    ci_upper = []
    contains_true = []
    
    for i in range(n_experiments):
        sample = np.random.normal(true_mean, 2, n_samples)
        mean = np.mean(sample)
        se = stats.sem(sample)
        ci = stats.t.interval(0.95, n_samples-1, loc=mean, scale=se)
        ci_lower.append(ci[0])
        ci_upper.append(ci[1])
        contains_true.append(ci[0] <= true_mean <= ci[1])
    
    # Vẽ confidence intervals
    for i in range(n_experiments):
        color = 'blue' if contains_true[i] else 'red'
        axes[0].plot([i, i], [ci_lower[i], ci_upper[i]], color=color, alpha=0.6, linewidth=2)
        axes[0].plot(i, (ci_lower[i] + ci_upper[i])/2, 'o', color=color, markersize=4)
    
    axes[0].axhline(y=true_mean, color='green', linestyle='--', linewidth=2, label='Giá trị thật')
    coverage = sum(contains_true) / n_experiments * 100
    axes[0].set_title(f'Khoảng Tin cậy 95% (Frequentist)\n{coverage:.0f}% khoảng chứa giá trị thật', 
                      fontsize=13, fontweight='bold')
    axes[0].set_xlabel('Thí nghiệm', fontsize=11)
    axes[0].set_ylabel('Giá trị', fontsize=11)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    axes[0].text(25, true_mean + 2, 
                 'Diễn giải: "95% các khoảng sẽ chứa\ngiá trị thật nếu lặp lại nhiều lần"',
                 fontsize=10, ha='center',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Mô phỏng Bayesian credible interval
    observed_data = np.random.normal(true_mean, 2, n_samples)
    posterior_mean = np.mean(observed_data)
    posterior_std = 2 / np.sqrt(n_samples)
    
    x = np.linspace(posterior_mean - 4*posterior_std, posterior_mean + 4*posterior_std, 1000)
    posterior = stats.norm.pdf(x, posterior_mean, posterior_std)
    
    axes[1].plot(x, posterior, 'b-', linewidth=2, label='Phân phối Posterior')
    axes[1].fill_between(x, posterior, alpha=0.3, color='blue')
    
    # Tính credible interval
    credible_lower = stats.norm.ppf(0.025, posterior_mean, posterior_std)
    credible_upper = stats.norm.ppf(0.975, posterior_mean, posterior_std)
    
    # Tô vùng credible interval
    x_credible = x[(x >= credible_lower) & (x <= credible_upper)]
    y_credible = stats.norm.pdf(x_credible, posterior_mean, posterior_std)
    axes[1].fill_between(x_credible, y_credible, alpha=0.5, color='green', label='Khoảng Credible 95%')
    
    axes[1].axvline(true_mean, color='red', linestyle='--', linewidth=2, label='Giá trị thật')
    axes[1].axvline(credible_lower, color='green', linestyle=':', linewidth=2)
    axes[1].axvline(credible_upper, color='green', linestyle=':', linewidth=2)
    
    axes[1].set_title('Khoảng Credible 95% (Bayesian)\nCho một thí nghiệm cụ thể', 
                      fontsize=13, fontweight='bold')
    axes[1].set_xlabel('Giá trị tham số', fontsize=11)
    axes[1].set_ylabel('Mật độ Posterior', fontsize=11)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    axes[1].text(posterior_mean, max(posterior)*0.7, 
                 f'Diễn giải: "Có 95% xác suất\ntham số nằm trong [{credible_lower:.2f}, {credible_upper:.2f}]"',
                 fontsize=10, ha='center',
                 bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    plt.tight_layout()
    save_figure('confidence_vs_credible_intervals.png')

def generate_pvalue_misinterpretations():
    """Hình 5: Các Hiểu lầm Phổ biến về P-values"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Subplot 1: P-value không phải là P(H0|data)
    ax = axes[0, 0]
    categories = ['P(data|H₀)\n(P-value)', 'P(H₀|data)\n(Điều ta muốn)']
    ax.bar(categories, [0.05, 0.05], color=['blue', 'gray'], alpha=0.7, edgecolor='black', linewidth=2)
    ax.bar(categories[1], 0.05, color='white', hatch='///', edgecolor='red', linewidth=2)
    ax.set_ylabel('Xác suất', fontsize=11)
    ax.set_title('Hiểu lầm 1: P-value ≠ P(H₀|data)', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 0.1)
    ax.text(0, 0.055, 'p=0.05', ha='center', fontsize=11, fontweight='bold')
    ax.text(1, 0.025, '???', ha='center', fontsize=20, fontweight='bold', color='red')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Subplot 2: P-value nhỏ không có nghĩa là hiệu ứng lớn
    ax = axes[0, 1]
    sample_sizes = [10, 50, 100, 500, 1000]
    effect_size = 0.3
    p_values_sim = []
    
    np.random.seed(789)
    for n in sample_sizes:
        group1 = np.random.normal(0, 1, n)
        group2 = np.random.normal(effect_size, 1, n)
        _, p = stats.ttest_ind(group1, group2)
        p_values_sim.append(p)
    
    ax.plot(sample_sizes, p_values_sim, 'o-', linewidth=2, markersize=8, color='purple')
    ax.axhline(y=0.05, color='red', linestyle='--', linewidth=2, label='α = 0.05')
    ax.set_xlabel('Kích thước mẫu', fontsize=11)
    ax.set_ylabel('P-value', fontsize=11)
    ax.set_title(f'Hiểu lầm 2: P-value nhỏ ≠ Hiệu ứng lớn\n(Effect size cố định = {effect_size})', 
                 fontsize=12, fontweight='bold')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.text(200, 0.2, 'Với mẫu lớn,\nhiệu ứng nhỏ cũng\n"có ý nghĩa"', 
            fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Subplot 3: P-value lớn không chứng minh H0 đúng
    ax = axes[1, 0]
    sample_sizes_small = [5, 10, 15, 20, 25, 30]
    effect_size_large = 0.8
    p_values_small_n = []
    
    np.random.seed(321)
    for n in sample_sizes_small:
        group1 = np.random.normal(0, 1, n)
        group2 = np.random.normal(effect_size_large, 1, n)
        _, p = stats.ttest_ind(group1, group2)
        p_values_small_n.append(p)
    
    ax.plot(sample_sizes_small, p_values_small_n, 's-', linewidth=2, markersize=8, color='orange')
    ax.axhline(y=0.05, color='red', linestyle='--', linewidth=2, label='α = 0.05')
    ax.set_xlabel('Kích thước mẫu', fontsize=11)
    ax.set_ylabel('P-value', fontsize=11)
    ax.set_title(f'Hiểu lầm 3: P-value lớn ≠ H₀ đúng\n(Effect size thực = {effect_size_large})', 
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.text(15, 0.15, 'Với mẫu nhỏ,\nhiệu ứng lớn có thể\n"không có ý nghĩa"', 
            fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Subplot 4: Ngưỡng α = 0.05 là tùy ý
    ax = axes[1, 1]
    p_values_range = np.linspace(0.001, 0.1, 100)
    colors_decision = ['red' if p < 0.05 else 'blue' for p in p_values_range]
    
    for i, p in enumerate(p_values_range):
        ax.scatter(p, 1 if p < 0.05 else 0, c=colors_decision[i], s=30, alpha=0.6)
    
    ax.axvline(x=0.05, color='black', linestyle='--', linewidth=3, label='Ngưỡng α = 0.05')
    ax.axvline(x=0.049, color='green', linestyle=':', linewidth=2, alpha=0.7)
    ax.axvline(x=0.051, color='purple', linestyle=':', linewidth=2, alpha=0.7)
    
    ax.set_xlabel('P-value', fontsize=11)
    ax.set_ylabel('Quyết định', fontsize=11)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Không bác bỏ H₀', 'Bác bỏ H₀'])
    ax.set_title('Hiểu lầm 4: Ngưỡng α = 0.05 là tùy ý', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='x')
    ax.text(0.05, 0.5, 'p=0.049 vs p=0.051\nKhác biệt nhỏ,\nkết luận hoàn toàn khác!', 
            fontsize=9, ha='center',
            bbox=dict(boxstyle='round', facecolor='pink', alpha=0.8))
    
    plt.tight_layout()
    save_figure('pvalue_misinterpretations.png')

def generate_sample_size_calculation():
    """Hình 6: Tính toán Kích thước Mẫu"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Tính kích thước mẫu cần thiết cho các effect sizes khác nhau
    effect_sizes = np.linspace(0.1, 2.0, 50)
    alpha = 0.05
    power = 0.80
    sigma = 7
    
    # Công thức xấp xỉ cho two-sample t-test
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    sample_sizes_needed = []
    for delta in effect_sizes:
        n = 2 * ((z_alpha + z_beta) * sigma / delta)**2
        sample_sizes_needed.append(int(np.ceil(n)))
    
    ax.plot(effect_sizes, sample_sizes_needed, linewidth=3, color='darkblue')
    ax.fill_between(effect_sizes, sample_sizes_needed, alpha=0.3, color='blue')
    
    # Đánh dấu các điểm cụ thể
    small_effect = 0.5
    small_effect_n = int(2 * ((z_alpha + z_beta) * sigma / small_effect)**2)
    ax.plot(small_effect, small_effect_n, 'ro', markersize=12, label=f'Hiệu ứng nhỏ (0.5 cm): n≈{small_effect_n}')
    
    medium_effect = 2.0
    medium_effect_n = int(2 * ((z_alpha + z_beta) * sigma / medium_effect)**2)
    ax.plot(medium_effect, medium_effect_n, 'go', markersize=12, label=f'Hiệu ứng lớn (2.0 cm): n≈{medium_effect_n}')
    
    ax.set_xlabel('Kích thước hiệu ứng (cm)', fontsize=12)
    ax.set_ylabel('Kích thước mẫu cần thiết (mỗi nhóm)', fontsize=12)
    ax.set_title(f'Kích thước Mẫu Cần thiết để Phát hiện Hiệu ứng\n(α={alpha}, Power={power}, σ={sigma} cm)', 
                 fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(True, alpha=0.3)
    
    ax.text(0.8, 500, 'Hiệu ứng nhỏ cần\nmẫu rất lớn!', 
            fontsize=11, ha='center',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    plt.tight_layout()
    save_figure('sample_size_calculation.png')

def main():
    """Hàm chính để tạo tất cả các hình ảnh"""
    print('='*60)
    print('BẮT ĐẦU TẠO HÌNH ẢNH MINH HỌA')
    print('='*60)
    print()
    
    print('Phần 1/3: Tạo hình ảnh cơ bản về p-values')
    generate_pvalue_ttest_illustration()
    generate_effect_size_vs_sample_size()
    print('✓ Hoàn thành phần 1/3\n')
    
    print('Phần 2/3: Tạo hình ảnh về vấn đề và so sánh')
    generate_multiple_testing_problem()
    generate_confidence_vs_credible_intervals()
    print('✓ Hoàn thành phần 2/3\n')
    
    print('Phần 3/3: Tạo hình ảnh về hiểu lầm và tính toán')
    generate_pvalue_misinterpretations()
    generate_sample_size_calculation()
    print('✓ Hoàn thành phần 3/3\n')
    
    print('='*60)
    print('TẤT CẢ HÌNH ẢNH ĐÃ ĐƯỢC TẠO THÀNH CÔNG!')
    print('='*60)
    print()
    print('Danh sách các file đã tạo:')
    print('1. pvalue_ttest_illustration.png')
    print('2. effect_size_vs_sample_size.png')
    print('3. multiple_testing_problem.png')
    print('4. confidence_vs_credible_intervals.png')
    print('5. pvalue_misinterpretations.png')
    print('6. sample_size_calculation.png')
    print()
    print(f'Thư mục output: {OUTPUT_DIR}')

if __name__ == '__main__':
    main()
