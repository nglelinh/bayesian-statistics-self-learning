#!/usr/bin/env python3
"""
Script để tạo các hình ảnh minh họa cho Chapter 02: Probability Updating

Sử dụng:
    python3 generate_chapter02_images.py

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

def generate_probability_distributions_family():
    """Hình 1: Họ phân phối xác suất - Beta, Normal, Gamma"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    x = np.linspace(0, 1, 1000)
    
    # Beta distributions với các tham số khác nhau
    beta_params = [
        (2, 2, 'Beta(2, 2)\nĐồng nhất yếu'),
        (5, 2, 'Beta(5, 2)\nLệch phải'),
        (2, 5, 'Beta(2, 5)\nLệch trái'),
        (10, 10, 'Beta(10, 10)\nTập trung'),
        (0.5, 0.5, 'Beta(0.5, 0.5)\nU-shaped'),
        (1, 1, 'Beta(1, 1)\nĐồng nhất')
    ]
    
    for idx, (alpha, beta, label) in enumerate(beta_params):
        ax = axes[idx // 3, idx % 3]
        y = stats.beta(alpha, beta).pdf(x)
        ax.plot(x, y, linewidth=3, color='blue')
        ax.fill_between(x, y, alpha=0.3, color='blue')
        ax.set_title(label, fontsize=11, fontweight='bold')
        ax.set_xlabel('θ', fontsize=10)
        ax.set_ylabel('Mật độ', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Add mean line
        mean = alpha / (alpha + beta)
        ax.axvline(mean, color='red', linestyle='--', linewidth=2, alpha=0.7)
        ax.text(mean, max(y)*0.9, f'Mean={mean:.2f}', 
               ha='center', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.suptitle('Họ Phân phối Beta - Linh hoạt cho Xác suất [0,1]', 
                 fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    save_figure('beta_distribution_family.png')

def generate_conjugate_prior_beta_binomial():
    """Hình 2: Conjugate Prior - Beta-Binomial"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    theta = np.linspace(0, 1, 1000)
    
    # Prior: Beta(2, 2)
    alpha_prior, beta_prior = 2, 2
    prior = stats.beta(alpha_prior, beta_prior).pdf(theta)
    
    axes[0, 0].plot(theta, prior, 'b-', linewidth=3, label=f'Beta({alpha_prior}, {beta_prior})')
    axes[0, 0].fill_between(theta, prior, alpha=0.3, color='blue')
    axes[0, 0].set_title('PRIOR\n"Niềm tin ban đầu"', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('θ', fontsize=10)
    axes[0, 0].set_ylabel('Mật độ', fontsize=10)
    axes[0, 0].legend(fontsize=10)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].text(0.5, max(prior)*0.8, 
                   'Tin rằng θ ≈ 0.5\nvới độ không chắc chắn vừa phải', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Data: 7 successes in 10 trials
    n_trials = 10
    n_success = 7
    
    # Likelihood
    likelihood = theta**n_success * (1-theta)**(n_trials-n_success)
    likelihood = likelihood / np.max(likelihood)  # Normalize for visualization
    
    axes[0, 1].plot(theta, likelihood, 'g-', linewidth=3, label=f'{n_success}/{n_trials} thành công')
    axes[0, 1].fill_between(theta, likelihood, alpha=0.3, color='green')
    axes[0, 1].set_title('LIKELIHOOD\n"Bằng chứng từ dữ liệu"', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('θ', fontsize=10)
    axes[0, 1].set_ylabel('Likelihood (chuẩn hóa)', fontsize=10)
    axes[0, 1].legend(fontsize=10)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].text(0.7, max(likelihood)*0.8, 
                   'Dữ liệu gợi ý\nθ cao (nhiều thành công)', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Posterior: Beta(2+7, 2+3) = Beta(9, 5)
    alpha_post = alpha_prior + n_success
    beta_post = beta_prior + (n_trials - n_success)
    posterior = stats.beta(alpha_post, beta_post).pdf(theta)
    
    axes[1, 0].plot(theta, posterior, 'r-', linewidth=3, label=f'Beta({alpha_post}, {beta_post})')
    axes[1, 0].fill_between(theta, posterior, alpha=0.3, color='red')
    axes[1, 0].set_title('POSTERIOR\n"Niềm tin cập nhật"', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('θ', fontsize=10)
    axes[1, 0].set_ylabel('Mật độ', fontsize=10)
    axes[1, 0].legend(fontsize=10)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Add credible interval
    ci_lower = stats.beta(alpha_post, beta_post).ppf(0.025)
    ci_upper = stats.beta(alpha_post, beta_post).ppf(0.975)
    axes[1, 0].axvline(ci_lower, color='red', linestyle=':', linewidth=2, alpha=0.7)
    axes[1, 0].axvline(ci_upper, color='red', linestyle=':', linewidth=2, alpha=0.7)
    axes[1, 0].text(0.64, max(posterior)*0.8, 
                   f'95% CI:\n[{ci_lower:.2f}, {ci_upper:.2f}]', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='pink', alpha=0.8))
    
    # Compare all three
    axes[1, 1].plot(theta, prior, 'b-', linewidth=2, label='Prior', alpha=0.7)
    axes[1, 1].plot(theta, likelihood, 'g--', linewidth=2, label='Likelihood (scaled)', alpha=0.7)
    axes[1, 1].plot(theta, posterior, 'r-', linewidth=3, label='Posterior')
    axes[1, 1].fill_between(theta, posterior, alpha=0.2, color='red')
    axes[1, 1].set_title('SO SÁNH: Prior → Likelihood → Posterior\n"Conjugacy: Beta × Binomial = Beta"', 
                        fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('θ', fontsize=10)
    axes[1, 1].set_ylabel('Mật độ', fontsize=10)
    axes[1, 1].legend(fontsize=10)
    axes[1, 1].grid(True, alpha=0.3)
    
    # Add arrow showing update
    prior_mean = alpha_prior / (alpha_prior + beta_prior)
    post_mean = alpha_post / (alpha_post + beta_post)
    axes[1, 1].annotate('', xy=(post_mean, 1.5), xytext=(prior_mean, 1.5),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    axes[1, 1].text((prior_mean + post_mean)/2, 1.7, 'Cập nhật', 
                   ha='center', fontsize=9)
    
    plt.tight_layout()
    save_figure('conjugate_prior_beta_binomial.png')

def generate_grid_approximation():
    """Hình 3: Grid Approximation"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    # Data
    n_success = 6
    n_trials = 9
    
    # Different grid sizes
    grid_sizes = [5, 10, 20, 50, 100, 1000]
    
    for idx, n_grid in enumerate(grid_sizes):
        ax = axes[idx // 3, idx % 3]
        
        # Define grid
        theta_grid = np.linspace(0, 1, n_grid)
        
        # Prior (uniform)
        prior = np.ones(n_grid) / n_grid
        
        # Likelihood
        likelihood = stats.binom(n_trials, theta_grid).pmf(n_success)
        
        # Posterior (unnormalized)
        posterior_unnorm = prior * likelihood
        
        # Normalize
        posterior = posterior_unnorm / np.sum(posterior_unnorm)
        
        # Plot
        if n_grid <= 20:
            ax.bar(theta_grid, posterior, width=1/n_grid*0.8, 
                  alpha=0.7, edgecolor='black', color='red')
        else:
            ax.plot(theta_grid, posterior, 'r-', linewidth=2)
            ax.fill_between(theta_grid, posterior, alpha=0.3, color='red')
        
        # True posterior (Beta)
        theta_cont = np.linspace(0, 1, 1000)
        true_posterior = stats.beta(1+n_success, 1+(n_trials-n_success)).pdf(theta_cont)
        ax.plot(theta_cont, true_posterior, 'b--', linewidth=2, alpha=0.7, 
               label='True posterior')
        
        ax.set_title(f'Grid size = {n_grid}', fontsize=11, fontweight='bold')
        ax.set_xlabel('θ', fontsize=10)
        ax.set_ylabel('Posterior', fontsize=10)
        ax.grid(True, alpha=0.3)
        if idx == 0:
            ax.legend(fontsize=9)
        
        # Add text about accuracy
        if n_grid < 50:
            accuracy = 'Thô'
        elif n_grid < 200:
            accuracy = 'Tốt'
        else:
            accuracy = 'Rất tốt'
        ax.text(0.5, max(posterior)*0.9, accuracy, 
               ha='center', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.suptitle(f'Grid Approximation với Grid Sizes Khác nhau\nData: {n_success}/{n_trials} thành công', 
                 fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    save_figure('grid_approximation.png')

def generate_prior_data_tradeoff():
    """Hình 4: Prior-Data Tradeoff"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    theta = np.linspace(0, 1, 1000)
    
    # Scenario 1: Weak prior, little data
    axes[0, 0].set_title('Weak Prior + Ít Dữ liệu\n"Posterior rất không chắc chắn"', 
                        fontsize=11, fontweight='bold')
    prior1 = stats.beta(2, 2).pdf(theta)
    post1 = stats.beta(2+3, 2+2).pdf(theta)  # 3 success in 5 trials
    
    axes[0, 0].plot(theta, prior1, 'b--', linewidth=2, label='Prior: Beta(2,2)', alpha=0.7)
    axes[0, 0].plot(theta, post1, 'r-', linewidth=3, label='Posterior: Beta(5,4)')
    axes[0, 0].fill_between(theta, post1, alpha=0.3, color='red')
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_xlabel('θ', fontsize=10)
    axes[0, 0].set_ylabel('Mật độ', fontsize=10)
    axes[0, 0].text(0.5, max(post1)*0.7, 'Data: 3/5\nPosterior rộng', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Scenario 2: Weak prior, much data
    axes[0, 1].set_title('Weak Prior + Nhiều Dữ liệu\n"Data chi phối"', 
                        fontsize=11, fontweight='bold')
    prior2 = stats.beta(2, 2).pdf(theta)
    post2 = stats.beta(2+60, 2+40).pdf(theta)  # 60 success in 100 trials
    
    axes[0, 1].plot(theta, prior2, 'b--', linewidth=2, label='Prior: Beta(2,2)', alpha=0.7)
    axes[0, 1].plot(theta, post2, 'r-', linewidth=3, label='Posterior: Beta(62,42)')
    axes[0, 1].fill_between(theta, post2, alpha=0.3, color='red')
    axes[0, 1].legend(fontsize=9)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].set_xlabel('θ', fontsize=10)
    axes[0, 1].set_ylabel('Mật độ', fontsize=10)
    axes[0, 1].text(0.6, max(post2)*0.7, 'Data: 60/100\nPosterior hẹp, gần data', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Scenario 3: Strong prior, little data
    axes[1, 0].set_title('Strong Prior + Ít Dữ liệu\n"Prior chi phối"', 
                        fontsize=11, fontweight='bold')
    prior3 = stats.beta(20, 20).pdf(theta)
    post3 = stats.beta(20+3, 20+2).pdf(theta)  # 3 success in 5 trials
    
    axes[1, 0].plot(theta, prior3, 'b--', linewidth=2, label='Prior: Beta(20,20)', alpha=0.7)
    axes[1, 0].plot(theta, post3, 'r-', linewidth=3, label='Posterior: Beta(23,22)')
    axes[1, 0].fill_between(theta, post3, alpha=0.3, color='red')
    axes[1, 0].legend(fontsize=9)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_xlabel('θ', fontsize=10)
    axes[1, 0].set_ylabel('Mật độ', fontsize=10)
    axes[1, 0].text(0.5, max(post3)*0.7, 'Data: 3/5\nPosterior gần prior', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Scenario 4: Strong prior, much data
    axes[1, 1].set_title('Strong Prior + Nhiều Dữ liệu\n"Thỏa hiệp"', 
                        fontsize=11, fontweight='bold')
    prior4 = stats.beta(20, 20).pdf(theta)
    post4 = stats.beta(20+60, 20+40).pdf(theta)  # 60 success in 100 trials
    
    axes[1, 1].plot(theta, prior4, 'b--', linewidth=2, label='Prior: Beta(20,20)', alpha=0.7)
    axes[1, 1].plot(theta, post4, 'r-', linewidth=3, label='Posterior: Beta(80,60)')
    axes[1, 1].fill_between(theta, post4, alpha=0.3, color='red')
    axes[1, 1].legend(fontsize=9)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_xlabel('θ', fontsize=10)
    axes[1, 1].set_ylabel('Mật độ', fontsize=10)
    axes[1, 1].text(0.57, max(post4)*0.7, 'Data: 60/100\nPosterior giữa prior và data', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='pink', alpha=0.8))
    
    plt.tight_layout()
    save_figure('prior_data_tradeoff.png')

def generate_posterior_predictive():
    """Hình 5: Posterior Predictive Distribution"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Observed data: 7 success in 10 trials
    n_obs = 10
    k_obs = 7
    
    # Posterior: Beta(2+7, 2+3) = Beta(9, 5)
    alpha_post = 2 + k_obs
    beta_post = 2 + (n_obs - k_obs)
    
    # Plot posterior
    theta = np.linspace(0, 1, 1000)
    posterior = stats.beta(alpha_post, beta_post).pdf(theta)
    
    axes[0, 0].plot(theta, posterior, 'r-', linewidth=3)
    axes[0, 0].fill_between(theta, posterior, alpha=0.3, color='red')
    axes[0, 0].set_title(f'Posterior sau {n_obs} quan sát\nBeta({alpha_post}, {beta_post})', 
                        fontsize=11, fontweight='bold')
    axes[0, 0].set_xlabel('θ', fontsize=10)
    axes[0, 0].set_ylabel('Mật độ', fontsize=10)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].text(0.64, max(posterior)*0.8, 
                   f'Observed: {k_obs}/{n_obs}', 
                   ha='center', fontsize=10,
                   bbox=dict(boxstyle='round', facecolor='pink', alpha=0.8))
    
    # Posterior predictive for next 10 trials
    n_new = 10
    k_new = np.arange(0, n_new + 1)
    
    # Calculate posterior predictive
    post_pred = np.zeros(n_new + 1)
    for k in k_new:
        # Beta-Binomial formula
        post_pred[k] = (stats.beta(alpha_post + k, beta_post + n_new - k).pdf(0.5) / 
                       stats.beta(alpha_post, beta_post).pdf(0.5))
    
    # Normalize
    post_pred = post_pred / np.sum(post_pred)
    
    axes[0, 1].bar(k_new, post_pred, alpha=0.7, edgecolor='black', color='green')
    axes[0, 1].set_title(f'Posterior Predictive\nCho {n_new} thử nghiệm tiếp theo', 
                        fontsize=11, fontweight='bold')
    axes[0, 1].set_xlabel('Số thành công', fontsize=10)
    axes[0, 1].set_ylabel('Xác suất', fontsize=10)
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    axes[0, 1].text(5, max(post_pred)*0.9, 
                   'Dự đoán có tính đến\nsự không chắc chắn về θ', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Compare with point estimate prediction
    theta_point = alpha_post / (alpha_post + beta_post)
    point_pred = stats.binom(n_new, theta_point).pmf(k_new)
    
    axes[1, 0].bar(k_new - 0.2, post_pred, width=0.4, alpha=0.7, 
                  label='Posterior Predictive', color='green', edgecolor='black')
    axes[1, 0].bar(k_new + 0.2, point_pred, width=0.4, alpha=0.7, 
                  label=f'Point estimate (θ={theta_point:.2f})', color='blue', edgecolor='black')
    axes[1, 0].set_title('So sánh: Posterior Predictive vs Point Estimate', 
                        fontsize=11, fontweight='bold')
    axes[1, 0].set_xlabel('Số thành công', fontsize=10)
    axes[1, 0].set_ylabel('Xác suất', fontsize=10)
    axes[1, 0].legend(fontsize=9)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    axes[1, 0].text(5, max(post_pred)*0.9, 
                   'Posterior Predictive rộng hơn\n(tính đến uncertainty)', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Uncertainty propagation
    axes[1, 1].axis('off')
    uncertainty_text = """
POSTERIOR PREDICTIVE DISTRIBUTION

Công thức:
P(ỹ | y) = ∫ P(ỹ | θ) P(θ | y) dθ

Ý nghĩa:
• Dự đoán dữ liệu mới (ỹ)
• Tính đến uncertainty về θ
• Trung bình hóa qua posterior

So với Point Estimate:
• Point: Chỉ dùng θ̂ = E[θ|y]
• Posterior Pred: Dùng toàn bộ posterior
• → Posterior Pred rộng hơn
• → Honest về uncertainty

Ứng dụng:
✓ Model checking
✓ Forecasting
✓ Decision making
✓ Uncertainty quantification
"""
    axes[1, 1].text(0.5, 0.5, uncertainty_text, fontsize=10, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
    
    plt.tight_layout()
    save_figure('posterior_predictive.png')

def generate_conjugate_families():
    """Hình 6: Các Conjugate Families phổ biến"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Beta-Binomial
    axes[0, 0].axis('off')
    beta_binom_text = """
╔═══════════════════════════════════════════╗
║      BETA-BINOMIAL CONJUGACY              ║
╠═══════════════════════════════════════════╣
║                                           ║
║  Prior:      Beta(α, β)                   ║
║  Likelihood: Binomial(n, θ)               ║
║  Posterior:  Beta(α+k, β+n-k)             ║
║                                           ║
║  Ứng dụng:                                ║
║    • Tỷ lệ chuyển đổi                     ║
║    • Xác suất thành công                  ║
║    • Click-through rate                   ║
║                                           ║
║  Ưu điểm:                                 ║
║    ✓ Closed-form posterior                ║
║    ✓ Dễ cập nhật tuần tự                  ║
║    ✓ Trực quan                            ║
║                                           ║
╚═══════════════════════════════════════════╝
"""
    axes[0, 0].text(0.5, 0.5, beta_binom_text, fontsize=9, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Normal-Normal
    axes[0, 1].axis('off')
    normal_text = """
╔═══════════════════════════════════════════╗
║      NORMAL-NORMAL CONJUGACY              ║
╠═══════════════════════════════════════════╣
║                                           ║
║  Prior:      N(μ₀, σ₀²)                   ║
║  Likelihood: N(μ, σ²) [σ² known]          ║
║  Posterior:  N(μ₁, σ₁²)                   ║
║                                           ║
║  Công thức:                               ║
║    μ₁ = (σ²μ₀ + nσ₀²x̄)/(σ² + nσ₀²)       ║
║    σ₁² = (σ²σ₀²)/(σ² + nσ₀²)             ║
║                                           ║
║  Ứng dụng:                                ║
║    • Chiều cao, cân nặng                  ║
║    • Nhiệt độ, áp suất                    ║
║    • Measurement errors                   ║
║                                           ║
╚═══════════════════════════════════════════╝
"""
    axes[0, 1].text(0.5, 0.5, normal_text, fontsize=9, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Gamma-Poisson
    axes[1, 0].axis('off')
    gamma_text = """
╔═══════════════════════════════════════════╗
║      GAMMA-POISSON CONJUGACY              ║
╠═══════════════════════════════════════════╣
║                                           ║
║  Prior:      Gamma(α, β)                  ║
║  Likelihood: Poisson(λ)                   ║
║  Posterior:  Gamma(α+Σx, β+n)             ║
║                                           ║
║  Ứng dụng:                                ║
║    • Count data                           ║
║    • Event rates                          ║
║    • Website traffic                      ║
║    • Số lỗi trong code                    ║
║                                           ║
║  Ưu điểm:                                 ║
║    ✓ Natural cho count data               ║
║    ✓ Flexible shape                       ║
║                                           ║
╚═══════════════════════════════════════════╝
"""
    axes[1, 0].text(0.5, 0.5, gamma_text, fontsize=9, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Summary
    axes[1, 1].axis('off')
    summary_text = """
╔═══════════════════════════════════════════╗
║      TẠI SAO CONJUGACY QUAN TRỌNG?        ║
╠═══════════════════════════════════════════╣
║                                           ║
║  Lợi ích:                                 ║
║    ✓ Posterior có dạng closed-form        ║
║    ✓ Không cần MCMC                       ║
║    ✓ Tính toán nhanh                      ║
║    ✓ Dễ hiểu, dễ giải thích               ║
║    ✓ Sequential updating đơn giản         ║
║                                           ║
║  Hạn chế:                                 ║
║    • Chỉ áp dụng cho một số models        ║
║    • Prior bị giới hạn bởi conjugacy      ║
║    • Không linh hoạt cho complex models   ║
║                                           ║
║  Khi nào dùng:                            ║
║    → Simple models                        ║
║    → Teaching/learning                    ║
║    → Quick prototyping                    ║
║    → Real-time updating                   ║
║                                           ║
║  Khi nào không dùng:                      ║
║    → Complex hierarchical models          ║
║    → Non-standard likelihoods             ║
║    → Need flexible priors                 ║
║                                           ║
╚═══════════════════════════════════════════╝
"""
    axes[1, 1].text(0.5, 0.5, summary_text, fontsize=8, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
    
    plt.tight_layout()
    save_figure('conjugate_families.png')

def main():
    """Hàm chính để tạo tất cả các hình ảnh"""
    print('='*60)
    print('BẮT ĐẦU TẠO HÌNH ẢNH CHO CHAPTER 02')
    print('='*60)
    print()
    
    print('Phần 1/6: Beta Distribution Family')
    generate_probability_distributions_family()
    print('✓ Hoàn thành phần 1/6\n')
    
    print('Phần 2/6: Conjugate Prior - Beta-Binomial')
    generate_conjugate_prior_beta_binomial()
    print('✓ Hoàn thành phần 2/6\n')
    
    print('Phần 3/6: Grid Approximation')
    generate_grid_approximation()
    print('✓ Hoàn thành phần 3/6\n')
    
    print('Phần 4/6: Prior-Data Tradeoff')
    generate_prior_data_tradeoff()
    print('✓ Hoàn thành phần 4/6\n')
    
    print('Phần 5/6: Posterior Predictive')
    generate_posterior_predictive()
    print('✓ Hoàn thành phần 5/6\n')
    
    print('Phần 6/6: Conjugate Families')
    generate_conjugate_families()
    print('✓ Hoàn thành phần 6/6\n')
    
    print('='*60)
    print('TẤT CẢ HÌNH ẢNH ĐÃ ĐƯỢC TẠO THÀNH CÔNG!')
    print('='*60)
    print()
    print('Danh sách các file đã tạo:')
    print('1. beta_distribution_family.png')
    print('2. conjugate_prior_beta_binomial.png')
    print('3. grid_approximation.png')
    print('4. prior_data_tradeoff.png')
    print('5. posterior_predictive.png')
    print('6. conjugate_families.png')
    print()
    print(f'Thư mục output: {OUTPUT_DIR}')

if __name__ == '__main__':
    main()
