#!/usr/bin/env python3
"""
Generate prior visualization images for Lesson 2.3
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
print("  GENERATING PRIOR VISUALIZATION IMAGES FOR LESSON 2.3")
print("="*80)

# Image 1: Four types of priors showing different levels of knowledge
def create_three_priors_comparison():
    """Compare different prior strengths"""
    theta = np.linspace(0, 1, 1000)
    
    priors = [
        {
            'name': 'Beta(1, 1) - Không biết gì',
            'dist': stats.beta(1, 1),
            'desc': 'Uniform: Mọi giá trị θ đều có thể như nhau.\nDùng khi: Hoàn toàn không có thông tin.',
            'color': 'gray'
        },
        {
            'name': 'Beta(5, 5) - Tin là khoảng 50%',
            'dist': stats.beta(5, 5),
            'desc': 'Tập trung ở 0.5, nhưng không chắc chắn lắm.\nDùng khi: Có ý tưởng mơ hồ, chưa có dữ liệu cụ thể.',
            'color': 'steelblue'
        },
        {
            'name': 'Beta(20, 80) - Tin là khoảng 20%',
            'dist': stats.beta(20, 80),
            'desc': 'Tập trung ở 0.2, khá chắc chắn.\nDùng khi: Có kinh nghiệm với các trang tương tự.',
            'color': 'darkorange'
        },
        {
            'name': 'Beta(100, 400) - Rất chắc là 20%',
            'dist': stats.beta(100, 400),
            'desc': 'Tập trung chặt chẽ ở 0.2, rất chắc chắn.\nDùng khi: Có nhiều dữ liệu từ các trang gần như giống hệt.',
            'color': 'darkred'
        }
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    for idx, prior_info in enumerate(priors):
        ax = axes[idx // 2, idx % 2]
        
        pdf = prior_info['dist'].pdf(theta)
        ax.plot(theta, pdf, linewidth=3, color=prior_info['color'])
        ax.fill_between(theta, pdf, alpha=0.3, color=prior_info['color'])
        
        # Statistics
        mean = prior_info['dist'].mean()
        std = prior_info['dist'].std()
        ci_lower, ci_upper = prior_info['dist'].ppf([0.025, 0.975])
        
        ax.axvline(mean, color='red', linestyle='--', linewidth=2, 
                   label=f'Mean = {mean:.2f}')
        ax.axvspan(ci_lower, ci_upper, alpha=0.15, color='yellow', 
                   label=f'95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]')
        
        ax.set_xlabel('θ (tỷ lệ chuyển đổi)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Mật độ xác suất prior', fontsize=12, fontweight='bold')
        ax.set_title(f'{prior_info["name"]}\n{prior_info["desc"]}', 
                     fontsize=12, fontweight='bold')
        ax.legend(fontsize=10, loc='upper right')
        ax.grid(alpha=0.3)
        ax.set_xlim(0, 1)
        ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'three_priors.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 2: Prior regularization with small data
def create_prior_regularization_small_data():
    """Show how prior helps with small data"""
    n_flips = 3
    k_heads = 3
    
    theta_grid = np.linspace(0, 1, 1000)
    
    # Likelihood (based on data only)
    likelihood = stats.binom.pmf(k_heads, n_flips, theta_grid)
    
    # Prior: Beta(2, 2) - belief that coin might be fair
    prior_weak = stats.beta(2, 2).pdf(theta_grid)
    
    # Posterior (unnormalized)
    posterior_unnorm = likelihood * prior_weak
    posterior = posterior_unnorm / np.trapz(posterior_unnorm, theta_grid)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Likelihood
    axes[0].plot(theta_grid, likelihood, linewidth=3, color='green')
    axes[0].fill_between(theta_grid, likelihood, alpha=0.3, color='green')
    axes[0].axvline(k_heads / n_flips, color='red', linestyle='--', linewidth=2,
                    label=f'MLE = {k_heads/n_flips:.2f}')
    axes[0].set_title('Likelihood: Chỉ dựa vào Dữ liệu\n(3/3 Ngửa → θ=1.0??)', 
                      fontsize=13, fontweight='bold')
    axes[0].set_xlabel('θ', fontsize=12)
    axes[0].set_ylabel('Likelihood', fontsize=12)
    axes[0].legend(fontsize=11)
    axes[0].grid(alpha=0.3)
    
    # Prior
    axes[1].plot(theta_grid, prior_weak, linewidth=3, color='blue')
    axes[1].fill_between(theta_grid, prior_weak, alpha=0.3, color='blue')
    axes[1].set_title('Prior: Beta(2,2)\n(Niềm tin: đồng xu có thể công bằng)', 
                      fontsize=13, fontweight='bold')
    axes[1].set_xlabel('θ', fontsize=12)
    axes[1].set_ylabel('Mật độ Prior', fontsize=12)
    axes[1].grid(alpha=0.3)
    
    # Posterior
    axes[2].plot(theta_grid, posterior, linewidth=3, color='purple')
    axes[2].fill_between(theta_grid, posterior, alpha=0.3, color='purple')
    posterior_mean = np.trapz(theta_grid * posterior, theta_grid)
    axes[2].axvline(posterior_mean, color='red', linestyle='--', linewidth=2,
                    label=f'Posterior Mean = {posterior_mean:.2f}')
    axes[2].set_title('Posterior: Kết hợp Cả Hai\n(Ước lượng hợp lý hơn!)', 
                      fontsize=13, fontweight='bold')
    axes[2].set_xlabel('θ', fontsize=12)
    axes[2].set_ylabel('Mật độ Posterior', fontsize=12)
    axes[2].legend(fontsize=11)
    axes[2].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'prior_regularization_small_data.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 3: Uninformative priors comparison
def create_uninformative_priors():
    """Compare different uninformative priors"""
    theta = np.linspace(0, 1, 1000)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Beta(1,1) = Uniform
    pdf1 = stats.beta(1, 1).pdf(theta)
    axes[0].plot(theta, pdf1, linewidth=3, color='gray')
    axes[0].fill_between(theta, pdf1, alpha=0.3, color='gray')
    axes[0].set_title('Beta(1, 1) = Uniform\n"Mọi giá trị đều như nhau"', 
                      fontsize=13, fontweight='bold')
    axes[0].set_xlabel('θ', fontsize=12)
    axes[0].set_ylabel('Mật độ', fontsize=12)
    axes[0].grid(alpha=0.3)
    axes[0].set_ylim(0, 3)
    
    # Beta(0.5, 0.5) = Jeffreys
    pdf2 = stats.beta(0.5, 0.5).pdf(theta)
    axes[1].plot(theta, pdf2, linewidth=3, color='steelblue')
    axes[1].fill_between(theta, pdf2, alpha=0.3, color='steelblue')
    axes[1].set_title('Beta(0.5, 0.5) = Jeffreys\n"Ưu tiên các cực trị"', 
                      fontsize=13, fontweight='bold')
    axes[1].set_xlabel('θ', fontsize=12)
    axes[1].set_ylabel('Mật độ', fontsize=12)
    axes[1].grid(alpha=0.3)
    axes[1].set_ylim(0, 3)
    
    # Beta(2, 2) = Weakly informative
    pdf3 = stats.beta(2, 2).pdf(theta)
    axes[2].plot(theta, pdf3, linewidth=3, color='darkorange')
    axes[2].fill_between(theta, pdf3, alpha=0.3, color='darkorange')
    axes[2].set_title('Beta(2, 2) = Weakly Informative\n"Ưu tiên giữa, nhẹ nhàng"', 
                      fontsize=13, fontweight='bold')
    axes[2].set_xlabel('θ', fontsize=12)
    axes[2].set_ylabel('Mật độ', fontsize=12)
    axes[2].grid(alpha=0.3)
    axes[2].set_ylim(0, 3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'uninformative_priors_comparison.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 4: Weakly informative prior example
def create_weakly_informative_example():
    """Show weakly informative prior"""
    theta = np.linspace(0, 1, 1000)
    
    # Beta(5, 5)
    pdf = stats.beta(5, 5).pdf(theta)
    mean = 0.5
    ci_lower, ci_upper = stats.beta(5, 5).ppf([0.025, 0.975])
    
    plt.figure(figsize=(10, 6))
    plt.plot(theta, pdf, linewidth=3, color='steelblue')
    plt.fill_between(theta, pdf, alpha=0.3, color='steelblue')
    plt.axvline(mean, color='red', linestyle='--', linewidth=2, 
                label=f'Mean = {mean:.2f}')
    plt.axvspan(ci_lower, ci_upper, alpha=0.15, color='yellow', 
                label=f'95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]')
    
    plt.xlabel('θ', fontsize=12, fontweight='bold')
    plt.ylabel('Mật độ Prior', fontsize=12, fontweight='bold')
    plt.title('Weakly Informative Prior: Beta(5, 5)\n"Có ý tưởng mơ hồ, nhưng không chắc chắn"', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.xlim(0, 1)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'weakly_informative_prior_example.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 5: Strongly informative prior example  
def create_strongly_informative_example():
    """Show strongly informative prior"""
    theta = np.linspace(0, 1, 1000)
    
    # Beta(80, 20) - strong belief around 0.8
    pdf = stats.beta(80, 20).pdf(theta)
    mean = stats.beta(80, 20).mean()
    ci_lower, ci_upper = stats.beta(80, 20).ppf([0.025, 0.975])
    
    plt.figure(figsize=(10, 6))
    plt.plot(theta, pdf, linewidth=3, color='darkred')
    plt.fill_between(theta, pdf, alpha=0.3, color='darkred')
    plt.axvline(mean, color='red', linestyle='--', linewidth=2, 
                label=f'Mean = {mean:.2f}')
    plt.axvspan(ci_lower, ci_upper, alpha=0.15, color='yellow', 
                label=f'95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]')
    
    plt.xlabel('θ', fontsize=12, fontweight='bold')
    plt.ylabel('Mật độ Prior', fontsize=12, fontweight='bold')
    plt.title('Strongly Informative Prior: Beta(80, 20)\n"Rất chắc chắn dựa trên nhiều dữ liệu trước đó"', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.xlim(0, 1)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'strongly_informative_prior_example.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 6: Prior sensitivity analysis - weak vs strong data
def create_prior_sensitivity_weak_data():
    """Show prior sensitivity with weak data (n=5, k=4)"""
    n, k = 5, 4
    theta_grid = np.linspace(0, 1, 1000)
    
    priors_to_compare = [
        ('Beta(1, 1) - Flat', stats.beta(1, 1), 'gray'),
        ('Beta(2, 2) - Weak', stats.beta(2, 2), 'steelblue'),
        ('Beta(10, 10) - Medium', stats.beta(10, 10), 'darkorange'),
    ]
    
    plt.figure(figsize=(12, 7))
    
    for name, prior_dist, color in priors_to_compare:
        # Prior
        alpha_prior, beta_prior = prior_dist.args
        
        # Posterior (conjugate update)
        alpha_post = alpha_prior + k
        beta_post = beta_prior + (n - k)
        posterior_dist = stats.beta(alpha_post, beta_post)
        
        pdf = posterior_dist.pdf(theta_grid)
        mean = posterior_dist.mean()
        
        plt.plot(theta_grid, pdf, linewidth=3, label=f'{name}: Mean={mean:.2f}', color=color)
        plt.fill_between(theta_grid, pdf, alpha=0.15, color=color)
    
    # Add MLE line
    mle = k / n
    plt.axvline(mle, color='red', linestyle='--', linewidth=2, 
                label=f'MLE = {mle:.2f}')
    
    plt.xlabel('θ', fontsize=12, fontweight='bold')
    plt.ylabel('Mật độ Posterior', fontsize=12, fontweight='bold')
    plt.title(f'Ảnh hưởng của Prior khi Dữ liệu ÍT (n={n}, k={k})\nPrior mạnh ảnh hưởng nhiều!', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.xlim(0, 1)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'prior_sensitivity_weak_data.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 7: Prior sensitivity analysis - strong data
def create_prior_sensitivity_strong_data():
    """Show prior sensitivity with strong data (n=100, k=80)"""
    n, k = 100, 80
    theta_grid = np.linspace(0, 1, 1000)
    
    priors_to_compare = [
        ('Beta(1, 1) - Flat', stats.beta(1, 1), 'gray'),
        ('Beta(2, 2) - Weak', stats.beta(2, 2), 'steelblue'),
        ('Beta(10, 10) - Medium', stats.beta(10, 10), 'darkorange'),
    ]
    
    plt.figure(figsize=(12, 7))
    
    for name, prior_dist, color in priors_to_compare:
        # Prior
        alpha_prior, beta_prior = prior_dist.args
        
        # Posterior (conjugate update)
        alpha_post = alpha_prior + k
        beta_post = beta_prior + (n - k)
        posterior_dist = stats.beta(alpha_post, beta_post)
        
        pdf = posterior_dist.pdf(theta_grid)
        mean = posterior_dist.mean()
        
        plt.plot(theta_grid, pdf, linewidth=3, label=f'{name}: Mean={mean:.2f}', color=color)
        plt.fill_between(theta_grid, pdf, alpha=0.15, color=color)
    
    # Add MLE line
    mle = k / n
    plt.axvline(mle, color='red', linestyle='--', linewidth=2, 
                label=f'MLE = {mle:.2f}')
    
    plt.xlabel('θ', fontsize=12, fontweight='bold')
    plt.ylabel('Mật độ Posterior', fontsize=12, fontweight='bold')
    plt.title(f'Ảnh hưởng của Prior khi Dữ liệu NHIỀU (n={n}, k={k})\nPrior gần như không ảnh hưởng!', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.xlim(0.6, 1.0)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'prior_sensitivity_strong_data.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 8: Prior to Posterior transformation
def create_prior_to_posterior_transformation():
    """Show prior to posterior transformation"""
    n, k = 10, 7
    theta_grid = np.linspace(0, 1, 1000)
    
    # Prior
    prior_dist = stats.beta(2, 2)
    prior_pdf = prior_dist.pdf(theta_grid)
    
    # Likelihood
    likelihood = stats.binom.pmf(k, n, theta_grid)
    likelihood_scaled = likelihood / likelihood.max() * prior_pdf.max()
    
    # Posterior
    posterior_dist = stats.beta(2 + k, 2 + (n - k))
    posterior_pdf = posterior_dist.pdf(theta_grid)
    
    plt.figure(figsize=(12, 7))
    
    plt.plot(theta_grid, prior_pdf, 'b--', linewidth=3, label='Prior: Beta(2,2)', alpha=0.7)
    plt.fill_between(theta_grid, prior_pdf, alpha=0.2, color='blue')
    
    plt.plot(theta_grid, likelihood_scaled, 'g:', linewidth=3, 
             label=f'Likelihood (scaled): {k}/{n}', alpha=0.7)
    
    plt.plot(theta_grid, posterior_pdf, 'r-', linewidth=4, label='Posterior: Beta(9,5)')
    plt.fill_between(theta_grid, posterior_pdf, alpha=0.3, color='red')
    
    # Mark means
    plt.axvline(prior_dist.mean(), color='blue', linestyle=':', alpha=0.5)
    plt.axvline(k/n, color='green', linestyle=':', alpha=0.5)
    plt.axvline(posterior_dist.mean(), color='red', linestyle=':', linewidth=2)
    
    plt.xlabel('θ', fontsize=12, fontweight='bold')
    plt.ylabel('Mật độ', fontsize=12, fontweight='bold')
    plt.title('Prior × Likelihood → Posterior\n"Dữ liệu kéo Prior về phía MLE"', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)
    plt.xlim(0, 1)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'prior_to_posterior.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 9: Prior Predictive Check
def create_prior_predictive_check():
    """Show prior predictive distribution"""
    np.random.seed(42)
    n_sims = 1000
    n_trials = 100
    
    # Step 1: Sample θ from prior Beta(5, 5)
    theta_samples = stats.beta(5, 5).rvs(n_sims)
    
    # Step 2: For each θ, sample data from binomial likelihood
    data_samples = [stats.binom.rvs(n_trials, theta) for theta in theta_samples]
    
    mean_data = np.mean(data_samples)
    ci_lower = np.percentile(data_samples, 2.5)
    ci_upper = np.percentile(data_samples, 97.5)
    
    plt.figure(figsize=(12, 6))
    plt.hist(data_samples, bins=30, edgecolor='black', alpha=0.7, color='skyblue')
    plt.axvline(mean_data, color='red', linestyle='--', linewidth=2,
                label=f'Mean = {mean_data:.1f}')
    plt.axvspan(ci_lower, ci_upper, alpha=0.15, color='yellow',
                label=f'95% CI: [{ci_lower:.0f}, {ci_upper:.0f}]')
    
    plt.xlabel('Số lần thành công (trong 100 lần thử)', fontsize=12, fontweight='bold')
    plt.ylabel('Tần số', fontsize=12, fontweight='bold')
    plt.title('Prior Predictive Distribution: Beta(5,5)\n"Nếu prior này đúng, dữ liệu sẽ trông như thế này"', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'prior_predictive_check.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Main execution
if __name__ == "__main__":
    print("\n[1/9] Creating three priors comparison...")
    create_three_priors_comparison()
    print("✅ Created: three_priors.png")
    
    print("\n[2/9] Creating prior regularization with small data...")
    create_prior_regularization_small_data()
    print("✅ Created: prior_regularization_small_data.png")
    
    print("\n[3/9] Creating uninformative priors comparison...")
    create_uninformative_priors()
    print("✅ Created: uninformative_priors_comparison.png")
    
    print("\n[4/9] Creating weakly informative prior example...")
    create_weakly_informative_example()
    print("✅ Created: weakly_informative_prior_example.png")
    
    print("\n[5/9] Creating strongly informative prior example...")
    create_strongly_informative_example()
    print("✅ Created: strongly_informative_prior_example.png")
    
    print("\n[6/9] Creating prior sensitivity with weak data...")
    create_prior_sensitivity_weak_data()
    print("✅ Created: prior_sensitivity_weak_data.png")
    
    print("\n[7/9] Creating prior sensitivity with strong data...")
    create_prior_sensitivity_strong_data()
    print("✅ Created: prior_sensitivity_strong_data.png")
    
    print("\n[8/9] Creating prior to posterior transformation...")
    create_prior_to_posterior_transformation()
    print("✅ Created: prior_to_posterior.png")
    
    print("\n[9/9] Creating prior predictive check...")
    create_prior_predictive_check()
    print("✅ Created: prior_predictive_check.png")
    
    print("\n" + "="*80)
    print("  ✅ ALL 9 PRIOR VISUALIZATION IMAGES CREATED SUCCESSFULLY!")
    print("="*80)
    print("\nImages saved to:", output_dir)
    print("\nReady to replace code blocks in 02_03_prior.md!")
