#!/usr/bin/env python3
"""
Script để tạo các hình ảnh minh họa cho Chapter 01: Bayesian Inference Basics

Sử dụng:
    python3 generate_chapter01_images.py

Yêu cầu:
    - numpy
    - matplotlib
    - scipy
    - seaborn

Tác giả: Nguyen Le Linh
Ngày: 11/01/2026
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

def generate_bayes_theorem_visualization():
    """Hình 1: Minh họa Định lý Bayes - Prior, Likelihood, Posterior"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Ví dụ: Đồng xu với prior Beta(2,2), data: 7 Ngửa trong 10 lần
    theta = np.linspace(0, 1, 1000)
    
    # Prior: Beta(2, 2)
    prior = stats.beta(2, 2).pdf(theta)
    axes[0, 0].plot(theta, prior, 'b-', linewidth=3, label='Prior: Beta(2, 2)')
    axes[0, 0].fill_between(theta, prior, alpha=0.3, color='blue')
    axes[0, 0].set_xlabel('θ (Xác suất ra Ngửa)', fontsize=11)
    axes[0, 0].set_ylabel('Mật độ', fontsize=11)
    axes[0, 0].set_title('PRIOR - Niềm tin Ban đầu\n"Trước khi toss đồng xu"', 
                         fontsize=12, fontweight='bold')
    axes[0, 0].legend(fontsize=10)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].text(0.5, max(prior)*0.8, 
                    'Tin rằng đồng xu\ngần công bằng', 
                    ha='center', fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Likelihood: Binomial(n=10, k=7)
    n_trials = 10
    n_success = 7
    likelihood = theta**n_success * (1-theta)**(n_trials-n_success)
    likelihood = likelihood / np.max(likelihood)  # Normalize for visualization
    
    axes[0, 1].plot(theta, likelihood, 'g-', linewidth=3, label=f'Likelihood: {n_success}/{n_trials} Ngửa')
    axes[0, 1].fill_between(theta, likelihood, alpha=0.3, color='green')
    axes[0, 1].set_xlabel('θ (Xác suất ra Ngửa)', fontsize=11)
    axes[0, 1].set_ylabel('Likelihood (chuẩn hóa)', fontsize=11)
    axes[0, 1].set_title('LIKELIHOOD - Bằng chứng từ Dữ liệu\n"Quan sát 7 Ngửa trong 10 lần"', 
                         fontsize=12, fontweight='bold')
    axes[0, 1].legend(fontsize=10)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].text(0.7, max(likelihood)*0.8, 
                    'Dữ liệu gợi ý\nθ cao hơn 0.5', 
                    ha='center', fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Posterior: Beta(2+7, 2+3) = Beta(9, 5)
    posterior = stats.beta(9, 5).pdf(theta)
    axes[1, 0].plot(theta, posterior, 'r-', linewidth=3, label='Posterior: Beta(9, 5)')
    axes[1, 0].fill_between(theta, posterior, alpha=0.3, color='red')
    axes[1, 0].set_xlabel('θ (Xác suất ra Ngửa)', fontsize=11)
    axes[1, 0].set_ylabel('Mật độ', fontsize=11)
    axes[1, 0].set_title('POSTERIOR - Niềm tin Cập nhật\n"Sau khi thấy dữ liệu"', 
                         fontsize=12, fontweight='bold')
    axes[1, 0].legend(fontsize=10)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Add credible interval
    ci_lower = stats.beta(9, 5).ppf(0.025)
    ci_upper = stats.beta(9, 5).ppf(0.975)
    axes[1, 0].axvline(ci_lower, color='red', linestyle=':', linewidth=2, alpha=0.7)
    axes[1, 0].axvline(ci_upper, color='red', linestyle=':', linewidth=2, alpha=0.7)
    axes[1, 0].text(0.64, max(posterior)*0.8, 
                    f'95% CI:\n[{ci_lower:.2f}, {ci_upper:.2f}]', 
                    ha='center', fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='pink', alpha=0.8))
    
    # So sánh Prior và Posterior
    axes[1, 1].plot(theta, prior, 'b-', linewidth=2, label='Prior', alpha=0.7)
    axes[1, 1].plot(theta, posterior, 'r-', linewidth=3, label='Posterior')
    axes[1, 1].fill_between(theta, prior, alpha=0.2, color='blue')
    axes[1, 1].fill_between(theta, posterior, alpha=0.3, color='red')
    axes[1, 1].set_xlabel('θ (Xác suất ra Ngửa)', fontsize=11)
    axes[1, 1].set_ylabel('Mật độ', fontsize=11)
    axes[1, 1].set_title('So sánh PRIOR vs POSTERIOR\n"Học tập từ dữ liệu"', 
                         fontsize=12, fontweight='bold')
    axes[1, 1].legend(fontsize=10)
    axes[1, 1].grid(True, alpha=0.3)
    
    # Add arrow showing shift
    prior_mean = 0.5
    post_mean = 9/(9+5)
    axes[1, 1].annotate('', xy=(post_mean, 1.5), xytext=(prior_mean, 1.5),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    axes[1, 1].text((prior_mean + post_mean)/2, 1.7, 'Dữ liệu kéo\nniềm tin', 
                   ha='center', fontsize=9)
    
    plt.tight_layout()
    save_figure('bayes_theorem_visualization.png')

def generate_sequential_updating():
    """Hình 2: Sequential Updating - Cập nhật tuần tự"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    theta = np.linspace(0, 1, 1000)
    
    # Step 0: Prior
    alpha, beta = 2, 2
    prior = stats.beta(alpha, beta).pdf(theta)
    axes[0, 0].plot(theta, prior, 'b-', linewidth=3)
    axes[0, 0].fill_between(theta, prior, alpha=0.3, color='blue')
    axes[0, 0].set_title(f'Bước 0: Prior\nBeta({alpha}, {beta})', 
                        fontsize=11, fontweight='bold')
    axes[0, 0].set_xlabel('θ', fontsize=10)
    axes[0, 0].set_ylabel('Mật độ', fontsize=10)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].text(0.5, max(prior)*0.8, f'Mean = {alpha/(alpha+beta):.2f}', 
                   ha='center', fontsize=10,
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Step 1: After first 5 tosses (4 heads)
    alpha1, beta1 = alpha + 4, beta + 1
    post1 = stats.beta(alpha1, beta1).pdf(theta)
    axes[0, 1].plot(theta, post1, 'g-', linewidth=3)
    axes[0, 1].fill_between(theta, post1, alpha=0.3, color='green')
    axes[0, 1].set_title(f'Bước 1: Sau 5 lần toss (4 Ngửa)\nBeta({alpha1}, {beta1})', 
                        fontsize=11, fontweight='bold')
    axes[0, 1].set_xlabel('θ', fontsize=10)
    axes[0, 1].set_ylabel('Mật độ', fontsize=10)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].text(0.6, max(post1)*0.8, f'Mean = {alpha1/(alpha1+beta1):.2f}', 
                   ha='center', fontsize=10,
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Step 2: After next 5 tosses (2 heads) - sequential
    alpha2, beta2 = alpha1 + 2, beta1 + 3
    post2 = stats.beta(alpha2, beta2).pdf(theta)
    axes[1, 0].plot(theta, post2, 'r-', linewidth=3)
    axes[1, 0].fill_between(theta, post2, alpha=0.3, color='red')
    axes[1, 0].set_title(f'Bước 2: Sau thêm 5 lần (2 Ngửa)\nBeta({alpha2}, {beta2})', 
                        fontsize=11, fontweight='bold')
    axes[1, 0].set_xlabel('θ', fontsize=10)
    axes[1, 0].set_ylabel('Mật độ', fontsize=10)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].text(0.5, max(post2)*0.8, f'Mean = {alpha2/(alpha2+beta2):.2f}', 
                   ha='center', fontsize=10,
                   bbox=dict(boxstyle='round', facecolor='pink', alpha=0.8))
    
    # Compare: Sequential vs Batch
    # Batch: all 10 tosses at once (6 heads, 4 tails)
    alpha_batch, beta_batch = alpha + 6, beta + 4
    post_batch = stats.beta(alpha_batch, beta_batch).pdf(theta)
    
    axes[1, 1].plot(theta, post2, 'r-', linewidth=3, label='Sequential (2 bước)')
    axes[1, 1].plot(theta, post_batch, 'purple', linewidth=2, linestyle='--', 
                   label='Batch (1 bước)')
    axes[1, 1].fill_between(theta, post2, alpha=0.2, color='red')
    axes[1, 1].set_title('So sánh: Sequential vs Batch\n"Kết quả giống nhau!"', 
                        fontsize=11, fontweight='bold')
    axes[1, 1].set_xlabel('θ', fontsize=10)
    axes[1, 1].set_ylabel('Mật độ', fontsize=10)
    axes[1, 1].legend(fontsize=10)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].text(0.5, max(post2)*0.5, 
                   'Thứ tự không quan trọng!\nChỉ có tổng dữ liệu', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    plt.tight_layout()
    save_figure('sequential_updating.png')

def generate_prior_strength_comparison():
    """Hình 3: So sánh Prior mạnh vs yếu"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    theta = np.linspace(0, 1, 1000)
    
    # Same data: 7 heads in 10 tosses
    n_success = 7
    n_trials = 10
    
    # Weak prior: Beta(2, 2)
    weak_prior = stats.beta(2, 2).pdf(theta)
    weak_post = stats.beta(2+n_success, 2+(n_trials-n_success)).pdf(theta)
    
    # Strong prior: Beta(20, 20) - very confident about θ=0.5
    strong_prior = stats.beta(20, 20).pdf(theta)
    strong_post = stats.beta(20+n_success, 20+(n_trials-n_success)).pdf(theta)
    
    # Plot weak prior
    axes[0, 0].plot(theta, weak_prior, 'b-', linewidth=3, label='Prior: Beta(2,2)')
    axes[0, 0].fill_between(theta, weak_prior, alpha=0.3, color='blue')
    axes[0, 0].set_title('WEAK PRIOR\n"Không chắc chắn lắm"', 
                        fontsize=11, fontweight='bold')
    axes[0, 0].set_xlabel('θ', fontsize=10)
    axes[0, 0].set_ylabel('Mật độ', fontsize=10)
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot strong prior
    axes[0, 1].plot(theta, strong_prior, 'b-', linewidth=3, label='Prior: Beta(20,20)')
    axes[0, 1].fill_between(theta, strong_prior, alpha=0.3, color='blue')
    axes[0, 1].set_title('STRONG PRIOR\n"Rất chắc chắn θ ≈ 0.5"', 
                        fontsize=11, fontweight='bold')
    axes[0, 1].set_xlabel('θ', fontsize=10)
    axes[0, 1].set_ylabel('Mật độ', fontsize=10)
    axes[0, 1].legend(fontsize=9)
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot weak prior + posterior
    axes[1, 0].plot(theta, weak_prior, 'b--', linewidth=2, label='Prior', alpha=0.6)
    axes[1, 0].plot(theta, weak_post, 'r-', linewidth=3, label='Posterior')
    axes[1, 0].fill_between(theta, weak_post, alpha=0.3, color='red')
    axes[1, 0].set_title('Weak Prior → Posterior bị ảnh hưởng NHIỀU\n"Dữ liệu chi phối"', 
                        fontsize=11, fontweight='bold')
    axes[1, 0].set_xlabel('θ', fontsize=10)
    axes[1, 0].set_ylabel('Mật độ', fontsize=10)
    axes[1, 0].legend(fontsize=9)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].axvline(0.5, color='gray', linestyle=':', alpha=0.5)
    axes[1, 0].axvline(9/14, color='red', linestyle=':', linewidth=2)
    
    # Plot strong prior + posterior
    axes[1, 1].plot(theta, strong_prior, 'b--', linewidth=2, label='Prior', alpha=0.6)
    axes[1, 1].plot(theta, strong_post, 'r-', linewidth=3, label='Posterior')
    axes[1, 1].fill_between(theta, strong_post, alpha=0.3, color='red')
    axes[1, 1].set_title('Strong Prior → Posterior bị ảnh hưởng ÍT\n"Prior kháng cự"', 
                        fontsize=11, fontweight='bold')
    axes[1, 1].set_xlabel('θ', fontsize=10)
    axes[1, 1].set_ylabel('Mật độ', fontsize=10)
    axes[1, 1].legend(fontsize=9)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].axvline(0.5, color='gray', linestyle=':', alpha=0.5)
    axes[1, 1].axvline(27/47, color='red', linestyle=':', linewidth=2)
    
    plt.tight_layout()
    save_figure('prior_strength_comparison.png')

def generate_frequentist_vs_bayesian_philosophy():
    """Hình 4: So sánh Triết lý Frequentist vs Bayesian"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    np.random.seed(42)
    true_theta = 0.7
    n_experiments = 100
    
    # Frequentist view: θ cố định, data ngẫu nhiên
    theta_fixed = true_theta
    data_samples = np.random.binomial(10, theta_fixed, n_experiments) / 10
    
    axes[0, 0].scatter(range(n_experiments), data_samples, alpha=0.5, s=30, color='blue')
    axes[0, 0].axhline(true_theta, color='red', linestyle='--', linewidth=3, 
                      label=f'θ = {true_theta} (CỐ ĐỊNH)')
    axes[0, 0].set_xlabel('Thí nghiệm', fontsize=10)
    axes[0, 0].set_ylabel('Tỷ lệ quan sát', fontsize=10)
    axes[0, 0].set_title('FREQUENTIST:\nθ cố định, Data ngẫu nhiên', 
                        fontsize=12, fontweight='bold')
    axes[0, 0].legend(fontsize=10)
    axes[0, 0].grid(alpha=0.3)
    axes[0, 0].set_ylim(0, 1)
    axes[0, 0].text(50, 0.9, 
                   '"Nếu lặp lại vô hạn lần,\ntỷ lệ sẽ hội tụ về θ"', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Bayesian view: data cố định, θ ngẫu nhiên
    observed_data = 7/10
    theta_range = np.linspace(0, 1, 1000)
    posterior = stats.beta(2+7, 2+3).pdf(theta_range)
    
    axes[0, 1].plot(theta_range, posterior, linewidth=3, color='green')
    axes[0, 1].fill_between(theta_range, posterior, alpha=0.3, color='green')
    axes[0, 1].axvline(observed_data, color='red', linestyle='--', linewidth=3, 
                      label=f'Data = {observed_data} (CỐ ĐỊNH)')
    axes[0, 1].set_xlabel('θ', fontsize=10)
    axes[0, 1].set_ylabel('Mật độ', fontsize=10)
    axes[0, 1].set_title('BAYESIAN:\nData cố định, θ ngẫu nhiên', 
                        fontsize=12, fontweight='bold')
    axes[0, 1].legend(fontsize=10)
    axes[0, 1].grid(alpha=0.3)
    axes[0, 1].text(0.5, max(posterior)*0.8, 
                   '"Phân phối thể hiện\nsự không chắc chắn về θ"', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Confidence Interval (Frequentist)
    n = 20
    n_success = 14
    p_hat = n_success / n
    se = np.sqrt(p_hat * (1 - p_hat) / n)
    ci_lower = p_hat - 1.96 * se
    ci_upper = p_hat + 1.96 * se
    
    axes[1, 0].axvline(p_hat, color='blue', linewidth=3, label=f'p̂ = {p_hat:.2f}')
    axes[1, 0].axvspan(ci_lower, ci_upper, alpha=0.3, color='blue', 
                      label=f'95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]')
    axes[1, 0].axvline(true_theta, color='red', linestyle='--', linewidth=2, 
                      label=f'True θ = {true_theta}')
    axes[1, 0].set_xlabel('θ', fontsize=10)
    axes[1, 0].set_title('FREQUENTIST: 95% Confidence Interval\n"95% các CI sẽ chứa θ"', 
                        fontsize=11, fontweight='bold')
    axes[1, 0].legend(fontsize=9)
    axes[1, 0].grid(alpha=0.3)
    axes[1, 0].set_xlim(0, 1)
    axes[1, 0].text(0.5, 0.5, 
                   'KHÔNG THỂ NÓI:\n"95% khả năng θ trong khoảng này"', 
                   ha='center', fontsize=9, color='red',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Credible Interval (Bayesian)
    alpha_post = 2 + n_success
    beta_post = 2 + (n - n_success)
    posterior_dist = stats.beta(alpha_post, beta_post)
    credible_lower = posterior_dist.ppf(0.025)
    credible_upper = posterior_dist.ppf(0.975)
    
    theta_range = np.linspace(0, 1, 1000)
    posterior_pdf = posterior_dist.pdf(theta_range)
    
    axes[1, 1].plot(theta_range, posterior_pdf, linewidth=3, color='green', label='Posterior')
    axes[1, 1].fill_between(theta_range, posterior_pdf, alpha=0.3, color='green')
    
    mask = (theta_range >= credible_lower) & (theta_range <= credible_upper)
    axes[1, 1].fill_between(theta_range[mask], posterior_pdf[mask], 
                           alpha=0.6, color='darkgreen', 
                           label=f'95% CI: [{credible_lower:.2f}, {credible_upper:.2f}]')
    axes[1, 1].axvline(true_theta, color='red', linestyle='--', linewidth=2, 
                      label=f'True θ = {true_theta}')
    axes[1, 1].set_xlabel('θ', fontsize=10)
    axes[1, 1].set_ylabel('Mật độ', fontsize=10)
    axes[1, 1].set_title('BAYESIAN: 95% Credible Interval\n"95% khả năng θ trong khoảng này"', 
                        fontsize=11, fontweight='bold')
    axes[1, 1].legend(fontsize=9)
    axes[1, 1].grid(alpha=0.3)
    axes[1, 1].text(0.5, max(posterior_pdf)*0.5, 
                   'CÓ THỂ NÓI:\n"P(θ ∈ CI | data) = 0.95"', 
                   ha='center', fontsize=9, color='green',
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    plt.tight_layout()
    save_figure('frequentist_vs_bayesian_philosophy.png')

def generate_pvalue_vs_posterior_probability():
    """Hình 5: So sánh P-value vs Posterior Probability"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Giả thuyết: θ = 0.5
    null_theta = 0.5
    observed_success = 8
    n_trials = 10
    
    # Frequentist: P-value
    p_value = 1 - stats.binom(n_trials, null_theta).cdf(observed_success - 1)
    
    # Vẽ null distribution
    x = np.arange(0, n_trials + 1)
    null_pmf = stats.binom(n_trials, null_theta).pmf(x)
    
    axes[0, 0].bar(x, null_pmf, alpha=0.5, edgecolor='black', label='Null distribution', color='lightblue')
    axes[0, 0].bar(x[x >= observed_success], null_pmf[x >= observed_success], 
                  alpha=0.7, color='red', edgecolor='black', label='P-value region')
    axes[0, 0].axvline(observed_success, color='red', linestyle='--', linewidth=2)
    axes[0, 0].set_xlabel('Số thành công', fontsize=10)
    axes[0, 0].set_ylabel('Xác suất', fontsize=10)
    axes[0, 0].set_title(f'FREQUENTIST: P-value = {p_value:.4f}\nGiả thuyết H₀: θ = {null_theta}', 
                        fontsize=11, fontweight='bold')
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].grid(alpha=0.3, axis='y')
    axes[0, 0].text(5, max(null_pmf)*0.8, 
                   f'P(data ≥ {observed_success} | H₀)', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Text box explaining p-value
    axes[0, 1].axis('off')
    pvalue_text = f"""
P-VALUE = {p_value:.4f}

DIỄN GIẢI ĐÚNG:
"Nếu H₀ đúng (θ = {null_theta}),
xác suất quan sát ≥ {observed_success} 
thành công là {p_value*100:.2f}%"

KHÔNG THỂ NÓI:
✗ "P(H₀ đúng) = {p_value:.4f}"
✗ "{p_value*100:.1f}% khả năng H₀ đúng"
✗ "P(θ = {null_theta} | data) = {p_value:.4f}"

VẤN ĐỀ:
• P-value = P(data | H₀)
• Chúng ta muốn: P(H₀ | data)
• Hai thứ HOÀN TOÀN KHÁC NHAU!
"""
    axes[0, 1].text(0.5, 0.5, pvalue_text, fontsize=10, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='#ffcccc', alpha=0.8))
    
    # Bayesian: Posterior probability
    theta_range = np.linspace(0, 1, 1000)
    alpha_post = 2 + observed_success
    beta_post = 2 + (n_trials - observed_success)
    posterior_pdf = stats.beta(alpha_post, beta_post).pdf(theta_range)
    
    prob_greater = 1 - stats.beta(alpha_post, beta_post).cdf(null_theta)
    
    axes[1, 0].plot(theta_range, posterior_pdf, linewidth=3, color='green', label='Posterior')
    axes[1, 0].fill_between(theta_range, posterior_pdf, alpha=0.3, color='green')
    
    # Shade θ > 0.5
    mask = theta_range > null_theta
    axes[1, 0].fill_between(theta_range[mask], posterior_pdf[mask], 
                           alpha=0.6, color='darkgreen', 
                           label=f'P(θ > {null_theta} | data) = {prob_greater:.3f}')
    axes[1, 0].axvline(null_theta, color='red', linestyle='--', linewidth=2, 
                      label=f'θ = {null_theta}')
    axes[1, 0].set_xlabel('θ', fontsize=10)
    axes[1, 0].set_ylabel('Mật độ', fontsize=10)
    axes[1, 0].set_title(f'BAYESIAN: Posterior Distribution\nDữ liệu: {observed_success}/{n_trials}', 
                        fontsize=11, fontweight='bold')
    axes[1, 0].legend(fontsize=9)
    axes[1, 0].grid(alpha=0.3)
    
    # Text box explaining posterior
    axes[1, 1].axis('off')
    bayes_text = f"""
POSTERIOR PROBABILITY

P(θ > {null_theta} | data) = {prob_greater:.3f}

DIỄN GIẢI:
"Xác suất θ > {null_theta} là {prob_greater*100:.1f}%"
"Rất có khả năng θ > {null_theta}"

CÓ THỂ NÓI:
✓ "P(θ > {null_theta} | data) = {prob_greater:.3f}"
✓ "Evidence mạnh cho θ > {null_theta}"
✓ "{prob_greater*100:.1f}% tin tưởng θ > {null_theta}"

SO VỚI P-VALUE:
• P-value = {p_value:.4f} (borderline)
• Posterior prob = {prob_greater:.3f} (rõ ràng!)
• Trả lời ĐÚNG câu hỏi quan tâm

ƯU ĐIỂM:
• Xác suất TRỰC TIẾP về θ
• Dễ diễn giải
• Không cần ngưỡng 0.05 tùy ý
"""
    axes[1, 1].text(0.5, 0.5, bayes_text, fontsize=10, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='#ccffcc', alpha=0.8))
    
    plt.tight_layout()
    save_figure('pvalue_vs_posterior_probability.png')

def main():
    """Hàm chính để tạo tất cả các hình ảnh"""
    print('='*60)
    print('BẮT ĐẦU TẠO HÌNH ẢNH CHO CHAPTER 01')
    print('='*60)
    print()
    
    print('Phần 1/5: Định lý Bayes')
    generate_bayes_theorem_visualization()
    print('✓ Hoàn thành phần 1/5\n')
    
    print('Phần 2/5: Sequential Updating')
    generate_sequential_updating()
    print('✓ Hoàn thành phần 2/5\n')
    
    print('Phần 3/5: Prior Strength')
    generate_prior_strength_comparison()
    print('✓ Hoàn thành phần 3/5\n')
    
    print('Phần 4/5: Frequentist vs Bayesian Philosophy')
    generate_frequentist_vs_bayesian_philosophy()
    print('✓ Hoàn thành phần 4/5\n')
    
    print('Phần 5/5: P-value vs Posterior')
    generate_pvalue_vs_posterior_probability()
    print('✓ Hoàn thành phần 5/5\n')
    
    print('='*60)
    print('TẤT CẢ HÌNH ẢNH ĐÃ ĐƯỢC TẠO THÀNH CÔNG!')
    print('='*60)
    print()
    print('Danh sách các file đã tạo:')
    print('1. bayes_theorem_visualization.png')
    print('2. sequential_updating.png')
    print('3. prior_strength_comparison.png')
    print('4. frequentist_vs_bayesian_philosophy.png')
    print('5. pvalue_vs_posterior_probability.png')
    print()
    print(f'Thư mục output: {OUTPUT_DIR}')

if __name__ == '__main__':
    main()
