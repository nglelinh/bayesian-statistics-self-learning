#!/usr/bin/env python3
"""
Generate posterior visualization images for Lesson 2.4
These replace code blocks in the markdown file
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import os

# Setup
output_dir = os.path.dirname(os.path.abspath(__file__))
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

print("="*80)
print("  GENERATING POSTERIOR VISUALIZATION IMAGES FOR LESSON 2.4")
print("="*80)

# Image 1: Bayes Theorem - Four Panel Visualization
def create_bayes_theorem_four_panel():
    """Show Prior, Likelihood, Prior×Likelihood, and Posterior"""
    n, k = 10, 7
    theta = np.linspace(0, 1, 1000)
    
    # Prior: Beta(2, 2)
    alpha_prior, beta_prior = 2, 2
    prior_dist = stats.beta(alpha_prior, beta_prior)
    prior_pdf = prior_dist.pdf(theta)
    
    # Likelihood: Binomial(10, θ)
    likelihood = stats.binom.pmf(k, n, theta)
    
    # Posterior: Beta(9, 5)
    alpha_post = alpha_prior + k
    beta_post = beta_prior + (n - k)
    posterior_dist = stats.beta(alpha_post, beta_post)
    posterior_pdf = posterior_dist.pdf(theta)
    
    # Unnormalized posterior
    unnormalized_posterior = prior_pdf * likelihood
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Prior
    axes[0, 0].plot(theta, prior_pdf, linewidth=3, color='blue')
    axes[0, 0].fill_between(theta, prior_pdf, alpha=0.3, color='blue')
    axes[0, 0].axvline(prior_dist.mean(), color='red', linestyle='--', linewidth=2,
                       label=f'Mean = {prior_dist.mean():.2f}')
    axes[0, 0].set_xlabel('θ', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Mật độ', fontsize=12, fontweight='bold')
    axes[0, 0].set_title('① PRIOR: P(θ)\nNiềm tin ban đầu', 
                         fontsize=14, fontweight='bold')
    axes[0, 0].legend(fontsize=11)
    axes[0, 0].grid(alpha=0.3)
    axes[0, 0].text(0.5, max(prior_pdf)*0.6, 
                    f'Beta({alpha_prior}, {beta_prior})\n"Đồng xu có thể công bằng"',
                    ha='center', fontsize=11,
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # 2. Likelihood
    axes[0, 1].plot(theta, likelihood, linewidth=3, color='green')
    axes[0, 1].fill_between(theta, likelihood, alpha=0.3, color='green')
    axes[0, 1].axvline(k/n, color='red', linestyle='--', linewidth=2,
                       label=f'MLE = {k/n:.2f}')
    axes[0, 1].set_xlabel('θ', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('Likelihood', fontsize=12, fontweight='bold')
    axes[0, 1].set_title(f'② LIKELIHOOD: P(data | θ)\nDữ liệu quan sát', 
                         fontsize=14, fontweight='bold')
    axes[0, 1].legend(fontsize=11)
    axes[0, 1].grid(alpha=0.3)
    axes[0, 1].text(0.7, max(likelihood)*0.6, 
                    f'Binomial({n}, θ)\nDữ liệu: {k}/{n} ngửa',
                    ha='center', fontsize=11,
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # 3. Prior × Likelihood
    axes[1, 0].plot(theta, unnormalized_posterior, linewidth=3, color='orange')
    axes[1, 0].fill_between(theta, unnormalized_posterior, alpha=0.3, color='orange')
    axes[1, 0].set_xlabel('θ', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Prior × Likelihood', fontsize=12, fontweight='bold')
    axes[1, 0].set_title('③ PRIOR × LIKELIHOOD\n(Chưa chuẩn hóa)', 
                         fontsize=14, fontweight='bold')
    axes[1, 0].grid(alpha=0.3)
    
    integral_unnorm = np.trapezoid(unnormalized_posterior, theta)
    axes[1, 0].text(0.5, max(unnormalized_posterior)*0.6, 
                    f'∫ = {integral_unnorm:.4f} ≠ 1\nCần chuẩn hóa!',
                    ha='center', fontsize=11,
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # 4. Posterior
    axes[1, 1].plot(theta, posterior_pdf, linewidth=3, color='purple')
    axes[1, 1].fill_between(theta, posterior_pdf, alpha=0.3, color='purple')
    axes[1, 1].axvline(posterior_dist.mean(), color='red', linestyle='--', linewidth=2,
                       label=f'Mean = {posterior_dist.mean():.2f}')
    
    ci_lower, ci_upper = posterior_dist.ppf([0.025, 0.975])
    axes[1, 1].axvspan(ci_lower, ci_upper, alpha=0.2, color='yellow',
                       label=f'95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]')
    
    axes[1, 1].set_xlabel('θ', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('Mật độ', fontsize=12, fontweight='bold')
    axes[1, 1].set_title('④ POSTERIOR: P(θ | data)\nNiềm tin cập nhật', 
                         fontsize=14, fontweight='bold')
    axes[1, 1].legend(fontsize=11, loc='upper left')
    axes[1, 1].grid(alpha=0.3)
    axes[1, 1].text(0.7, max(posterior_pdf)*0.6, 
                    f'Beta({alpha_post}, {beta_post})\nKết hợp Prior & Data',
                    ha='center', fontsize=11,
                    bbox=dict(boxstyle='round', facecolor='plum', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bayes_theorem_four_panel.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 2: Posterior probability calculations
def create_posterior_probability_calculations():
    """Show probability calculations from posterior"""
    posterior_dist = stats.beta(9, 5)
    theta = np.linspace(0, 1, 1000)
    pdf = posterior_dist.pdf(theta)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # P(θ in [0.6, 0.7])
    mask1 = (theta >= 0.6) & (theta <= 0.7)
    prob1 = posterior_dist.cdf(0.7) - posterior_dist.cdf(0.6)
    
    axes[0].plot(theta, pdf, linewidth=3, color='purple')
    axes[0].fill_between(theta, pdf, alpha=0.3, color='purple')
    axes[0].fill_between(theta[mask1], pdf[mask1], alpha=0.6, color='red',
                         label=f'P(0.6 ≤ θ ≤ 0.7) = {prob1:.3f}')
    axes[0].axvline(0.6, color='red', linestyle='--', alpha=0.7)
    axes[0].axvline(0.7, color='red', linestyle='--', alpha=0.7)
    axes[0].set_xlabel('θ', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Mật độ Posterior', fontsize=12, fontweight='bold')
    axes[0].set_title('Xác suất trong Khoảng', fontsize=13, fontweight='bold')
    axes[0].legend(fontsize=11)
    axes[0].grid(alpha=0.3)
    
    # P(θ > 0.5)
    mask2 = theta > 0.5
    prob2 = 1 - posterior_dist.cdf(0.5)
    
    axes[1].plot(theta, pdf, linewidth=3, color='purple')
    axes[1].fill_between(theta, pdf, alpha=0.3, color='purple')
    axes[1].fill_between(theta[mask2], pdf[mask2], alpha=0.6, color='green',
                         label=f'P(θ > 0.5) = {prob2:.3f}')
    axes[1].axvline(0.5, color='green', linestyle='--', linewidth=2, alpha=0.7)
    axes[1].set_xlabel('θ', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Mật độ Posterior', fontsize=12, fontweight='bold')
    axes[1].set_title('Xác suất Lớn hơn Ngưỡng', fontsize=13, fontweight='bold')
    axes[1].legend(fontsize=11)
    axes[1].grid(alpha=0.3)
    
    # P(θ > 0.8)
    mask3 = theta > 0.8
    prob3 = 1 - posterior_dist.cdf(0.8)
    
    axes[2].plot(theta, pdf, linewidth=3, color='purple')
    axes[2].fill_between(theta, pdf, alpha=0.3, color='purple')
    axes[2].fill_between(theta[mask3], pdf[mask3], alpha=0.6, color='orange',
                         label=f'P(θ > 0.8) = {prob3:.3f}')
    axes[2].axvline(0.8, color='orange', linestyle='--', linewidth=2, alpha=0.7)
    axes[2].set_xlabel('θ', fontsize=12, fontweight='bold')
    axes[2].set_ylabel('Mật độ Posterior', fontsize=12, fontweight='bold')
    axes[2].set_title('Xác suất Giả thuyết Cụ thể', fontsize=13, fontweight='bold')
    axes[2].legend(fontsize=11)
    axes[2].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'posterior_probability_calculations.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 3: Point estimates comparison
def create_point_estimates_comparison():
    """Compare different point estimates"""
    posterior_dist = stats.beta(9, 5)
    theta = np.linspace(0, 1, 1000)
    pdf = posterior_dist.pdf(theta)
    
    # Calculate point estimates
    mean_est = posterior_dist.mean()
    median_est = posterior_dist.median()
    mode_est = (posterior_dist.args[0] - 1) / (posterior_dist.args[0] + posterior_dist.args[1] - 2)
    
    plt.figure(figsize=(12, 6))
    plt.plot(theta, pdf, linewidth=3, color='purple', label='Posterior: Beta(9, 5)')
    plt.fill_between(theta, pdf, alpha=0.3, color='purple')
    
    plt.axvline(mean_est, color='red', linestyle='--', linewidth=2.5,
                label=f'Mean = {mean_est:.3f}')
    plt.axvline(median_est, color='green', linestyle='--', linewidth=2.5,
                label=f'Median = {median_est:.3f}')
    plt.axvline(mode_est, color='blue', linestyle='--', linewidth=2.5,
                label=f'Mode (MAP) = {mode_est:.3f}')
    
    plt.xlabel('θ', fontsize=12, fontweight='bold')
    plt.ylabel('Mật độ Posterior', fontsize=12, fontweight='bold')
    plt.title('Ước lượng Điểm từ Posterior\n(Mean, Median, Mode)', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'posterior_point_estimates.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 4: Credible intervals
def create_credible_intervals():
    """Show different credible intervals"""
    posterior_dist = stats.beta(9, 5)
    theta = np.linspace(0, 1, 1000)
    pdf = posterior_dist.pdf(theta)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Equal-tailed 95% CI
    ci_lower, ci_upper = posterior_dist.ppf([0.025, 0.975])
    mask1 = (theta >= ci_lower) & (theta <= ci_upper)
    
    axes[0].plot(theta, pdf, linewidth=3, color='purple')
    axes[0].fill_between(theta, pdf, alpha=0.3, color='purple')
    axes[0].fill_between(theta[mask1], pdf[mask1], alpha=0.6, color='yellow',
                         label=f'95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]')
    axes[0].axvline(ci_lower, color='red', linestyle='--', linewidth=2)
    axes[0].axvline(ci_upper, color='red', linestyle='--', linewidth=2)
    axes[0].set_xlabel('θ', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Mật độ Posterior', fontsize=12, fontweight='bold')
    axes[0].set_title('95% Equal-Tailed Credible Interval\n(2.5% ở mỗi đuôi)', 
                      fontsize=13, fontweight='bold')
    axes[0].legend(fontsize=11)
    axes[0].grid(alpha=0.3)
    
    # 90% CI
    ci_lower_90, ci_upper_90 = posterior_dist.ppf([0.05, 0.95])
    mask2 = (theta >= ci_lower_90) & (theta <= ci_upper_90)
    
    axes[1].plot(theta, pdf, linewidth=3, color='purple')
    axes[1].fill_between(theta, pdf, alpha=0.3, color='purple')
    axes[1].fill_between(theta[mask2], pdf[mask2], alpha=0.6, color='lightgreen',
                         label=f'90% CI: [{ci_lower_90:.3f}, {ci_upper_90:.3f}]')
    axes[1].axvline(ci_lower_90, color='green', linestyle='--', linewidth=2)
    axes[1].axvline(ci_upper_90, color='green', linestyle='--', linewidth=2)
    axes[1].set_xlabel('θ', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Mật độ Posterior', fontsize=12, fontweight='bold')
    axes[1].set_title('90% Credible Interval\n(5% ở mỗi đuôi)', 
                      fontsize=13, fontweight='bold')
    axes[1].legend(fontsize=11)
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'posterior_credible_intervals.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 5: Sequential updating demonstration
def create_sequential_updating():
    """Show sequential Bayesian updating"""
    # Start with weak prior
    alpha_prior = 2
    beta_prior = 2
    
    # Batches of data: (n, k)
    data_batches = [(5, 3), (5, 4), (10, 7), (20, 15)]
    
    theta = np.linspace(0, 1, 1000)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Initial prior
    current_alpha = alpha_prior
    current_beta = beta_prior
    
    for idx, (n, k) in enumerate(data_batches):
        ax = axes[idx // 2, idx % 2]
        
        # Current prior (before this data)
        prior_dist = stats.beta(current_alpha, current_beta)
        prior_pdf = prior_dist.pdf(theta)
        
        # Update with new data
        current_alpha += k
        current_beta += (n - k)
        
        # New posterior
        posterior_dist = stats.beta(current_alpha, current_beta)
        posterior_pdf = posterior_dist.pdf(theta)
        
        # Plot
        ax.plot(theta, prior_pdf, 'b--', linewidth=2, label='Prior (trước)', alpha=0.7)
        ax.fill_between(theta, prior_pdf, alpha=0.2, color='blue')
        
        ax.plot(theta, posterior_pdf, 'r-', linewidth=3, label='Posterior (sau)')
        ax.fill_between(theta, posterior_pdf, alpha=0.3, color='red')
        
        ax.axvline(k/n, color='green', linestyle=':', linewidth=2, 
                   label=f'MLE = {k/n:.2f}', alpha=0.7)
        
        ax.set_xlabel('θ', fontsize=12, fontweight='bold')
        ax.set_ylabel('Mật độ', fontsize=12, fontweight='bold')
        ax.set_title(f'Bước {idx+1}: Thêm {k}/{n} thành công\nPosterior: Beta({current_alpha}, {current_beta})', 
                     fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        ax.set_xlim(0, 1)
    
    plt.suptitle('Cập nhật Tuần tự (Sequential Updating)\nPosterior hôm nay = Prior ngày mai', 
                 fontsize=15, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sequential_updating.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 6: Prior strength vs data strength
def create_prior_vs_data_strength():
    """Compare prior influence with different data amounts"""
    theta = np.linspace(0, 1, 1000)
    
    # Strong prior: Beta(20, 20) centered at 0.5
    alpha_prior_strong = 20
    beta_prior_strong = 20
    
    # Data scenarios
    scenarios = [
        ("Ít dữ liệu", 5, 4),
        ("Trung bình", 20, 16),
        ("Nhiều dữ liệu", 100, 80)
    ]
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    for idx, (label, n, k) in enumerate(scenarios):
        ax = axes[idx]
        
        # Prior
        prior_dist = stats.beta(alpha_prior_strong, beta_prior_strong)
        prior_pdf = prior_dist.pdf(theta)
        
        # Posterior
        alpha_post = alpha_prior_strong + k
        beta_post = beta_prior_strong + (n - k)
        posterior_dist = stats.beta(alpha_post, beta_post)
        posterior_pdf = posterior_dist.pdf(theta)
        
        # Plot
        ax.plot(theta, prior_pdf, 'b--', linewidth=2, label='Prior: Beta(20, 20)', alpha=0.7)
        ax.fill_between(theta, prior_pdf, alpha=0.2, color='blue')
        
        ax.plot(theta, posterior_pdf, 'r-', linewidth=3, 
                label=f'Posterior: Beta({alpha_post}, {beta_post})')
        ax.fill_between(theta, posterior_pdf, alpha=0.3, color='red')
        
        ax.axvline(k/n, color='green', linestyle=':', linewidth=2, 
                   label=f'MLE = {k/n:.2f}', alpha=0.7)
        ax.axvline(0.5, color='blue', linestyle=':', linewidth=2, alpha=0.5)
        
        ax.set_xlabel('θ', fontsize=12, fontweight='bold')
        ax.set_ylabel('Mật độ', fontsize=12, fontweight='bold')
        ax.set_title(f'{label}: n={n}, k={k}\nPosterior mean = {posterior_dist.mean():.3f}', 
                     fontsize=12, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)
        ax.set_xlim(0, 1)
    
    plt.suptitle('Ảnh hưởng của Prior vs Dữ liệu\nDữ liệu nhiều → Prior ít ảnh hưởng', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'prior_vs_data_strength.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Main execution
if __name__ == "__main__":
    print("\n[1/6] Creating Bayes theorem four panel...")
    create_bayes_theorem_four_panel()
    print("✅ Created: bayes_theorem_four_panel.png")
    
    print("\n[2/6] Creating posterior probability calculations...")
    create_posterior_probability_calculations()
    print("✅ Created: posterior_probability_calculations.png")
    
    print("\n[3/6] Creating point estimates comparison...")
    create_point_estimates_comparison()
    print("✅ Created: posterior_point_estimates.png")
    
    print("\n[4/6] Creating credible intervals...")
    create_credible_intervals()
    print("✅ Created: posterior_credible_intervals.png")
    
    print("\n[5/6] Creating sequential updating...")
    create_sequential_updating()
    print("✅ Created: sequential_updating.png")
    
    print("\n[6/6] Creating prior vs data strength...")
    create_prior_vs_data_strength()
    print("✅ Created: prior_vs_data_strength.png")
    
    print("\n" + "="*80)
    print("  ✅ ALL 6 POSTERIOR VISUALIZATION IMAGES CREATED SUCCESSFULLY!")
    print("="*80)
    print("\nImages saved to:", output_dir)
    print("\nReady to replace code blocks in 02_04_posterior.md!")
