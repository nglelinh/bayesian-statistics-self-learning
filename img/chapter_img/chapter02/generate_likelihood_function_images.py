#!/usr/bin/env python3
"""
Generate missing likelihood function images for Lesson 2.2
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
print("  GENERATING LIKELIHOOD FUNCTION IMAGES FOR LESSON 2.2")
print("="*80)

# Image 1: Main Likelihood Function (7/10 coin example)
def create_likelihood_function_main():
    """Main likelihood curve showing MLE"""
    n = 10
    k = 7
    
    theta_grid = np.linspace(0, 1, 1000)
    likelihood = stats.binom.pmf(k, n, theta_grid)
    
    theta_examples = [0.1, 0.5, 0.7]
    likelihood_examples = stats.binom.pmf(k, n, theta_examples)
    
    plt.figure(figsize=(12, 6))
    plt.plot(theta_grid, likelihood, linewidth=3, color='darkgreen', label='Likelihood function')
    plt.fill_between(theta_grid, likelihood, alpha=0.2, color='darkgreen')
    
    for theta_val, lik_val in zip(theta_examples, likelihood_examples):
        plt.scatter(theta_val, lik_val, s=150, zorder=5, 
                    label=f'θ={theta_val}: L={lik_val:.4f}')
        plt.axvline(theta_val, color='gray', linestyle=':', alpha=0.5)
    
    mle = k / n
    plt.axvline(mle, color='red', linestyle='--', linewidth=2, 
                label=f'MLE = {mle:.1f}')
    
    plt.xlabel('θ (xác suất ra mặt Ngửa)', fontsize=13, fontweight='bold')
    plt.ylabel('Likelihood: L(θ | 7 Ngửa trong 10 lần)', fontsize=13, fontweight='bold')
    plt.title('Hàm Likelihood: Đánh giá mức độ hợp lý của các giá trị θ', 
              fontsize=15, fontweight='bold')
    plt.legend(fontsize=10, loc='upper left')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'likelihood_function.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 2: Binomial Likelihood (patient recovery example)
def create_binomial_likelihood_recovery():
    """15 patients, 12 recovered"""
    n_patients = 15
    k_recovered = 12
    
    theta_recovery = np.linspace(0, 1, 1000)
    likelihood_recovery = stats.binom.pmf(k_recovered, n_patients, theta_recovery)
    
    plt.figure(figsize=(10, 6))
    plt.plot(theta_recovery, likelihood_recovery, linewidth=3, color='steelblue')
    plt.fill_between(theta_recovery, likelihood_recovery, alpha=0.3, color='steelblue')
    plt.axvline(k_recovered / n_patients, color='red', linestyle='--', linewidth=2,
                label=f'MLE = {k_recovered/n_patients:.2f}')
    plt.xlabel('θ (xác suất hồi phục)', fontsize=12, fontweight='bold')
    plt.ylabel('Likelihood', fontsize=12, fontweight='bold')
    plt.title(f'Likelihood: {k_recovered} bệnh nhân hồi phục trong {n_patients} người', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'binomial_likelihood_recovery.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 3: Poisson Likelihood (phone calls example)
def create_poisson_likelihood_calls():
    """8 calls per hour"""
    k_calls = 8
    
    lambda_grid = np.linspace(0, 20, 1000)
    likelihood_poisson = stats.poisson.pmf(k_calls, lambda_grid)
    
    plt.figure(figsize=(10, 6))
    plt.plot(lambda_grid, likelihood_poisson, linewidth=3, color='darkorange')
    plt.fill_between(lambda_grid, likelihood_poisson, alpha=0.3, color='darkorange')
    plt.axvline(k_calls, color='red', linestyle='--', linewidth=2,
                label=f'MLE = {k_calls}')
    plt.xlabel('λ (tốc độ cuộc gọi/giờ)', fontsize=12, fontweight='bold')
    plt.ylabel('Likelihood', fontsize=12, fontweight='bold')
    plt.title(f'Likelihood: {k_calls} cuộc gọi quan sát được', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'poisson_likelihood_calls.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 4: Normal Likelihood (height measurements)
def create_normal_likelihood_heights():
    """5 student heights"""
    heights = np.array([165, 170, 168, 172, 169])
    sigma_known = 5
    
    mu_grid = np.linspace(160, 180, 1000)
    likelihood_normal = np.ones_like(mu_grid)
    
    for height in heights:
        likelihood_normal *= stats.norm.pdf(height, mu_grid, sigma_known)
    
    plt.figure(figsize=(10, 6))
    plt.plot(mu_grid, likelihood_normal, linewidth=3, color='purple')
    plt.fill_between(mu_grid, likelihood_normal, alpha=0.3, color='purple')
    plt.axvline(np.mean(heights), color='red', linestyle='--', linewidth=2,
                label=f'MLE (trung bình mẫu) = {np.mean(heights):.1f}')
    plt.xlabel('μ (chiều cao trung bình)', fontsize=12, fontweight='bold')
    plt.ylabel('Likelihood', fontsize=12, fontweight='bold')
    plt.title(f'Likelihood: Chiều cao của {len(heights)} sinh viên', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'normal_likelihood_heights.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Image 5: Likelihood vs Log-Likelihood comparison
def create_likelihood_log_likelihood_comparison():
    """Compare likelihood and log-likelihood for 100 tosses"""
    n_large = 100
    k_large = 60
    
    theta_grid_large = np.linspace(0.3, 0.9, 1000)
    likelihood_large = stats.binom.pmf(k_large, n_large, theta_grid_large)
    log_likelihood_large = stats.binom.logpmf(k_large, n_large, theta_grid_large)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Likelihood
    axes[0].plot(theta_grid_large, likelihood_large, linewidth=3, color='darkgreen')
    axes[0].fill_between(theta_grid_large, likelihood_large, alpha=0.3, color='darkgreen')
    axes[0].axvline(k_large / n_large, color='red', linestyle='--', linewidth=2,
                    label=f'MLE = {k_large/n_large:.2f}')
    axes[0].set_xlabel('θ', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Likelihood', fontsize=12, fontweight='bold')
    axes[0].set_title(f'Likelihood: {k_large} ngửa trong {n_large} lần\n(Lưu ý: giá trị rất nhỏ!)', 
                      fontsize=14, fontweight='bold')
    axes[0].legend(fontsize=11)
    axes[0].grid(alpha=0.3)
    axes[0].ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    # Log-Likelihood
    axes[1].plot(theta_grid_large, log_likelihood_large, linewidth=3, color='darkblue')
    axes[1].fill_between(theta_grid_large, log_likelihood_large, alpha=0.3, color='darkblue')
    axes[1].axvline(k_large / n_large, color='red', linestyle='--', linewidth=2,
                    label=f'MLE = {k_large/n_large:.2f}')
    axes[1].set_xlabel('θ', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Log-Likelihood', fontsize=12, fontweight='bold')
    axes[1].set_title(f'Log-Likelihood: {k_large} ngửa trong {n_large} lần\n(Dễ làm việc hơn!)', 
                      fontsize=14, fontweight='bold')
    axes[1].legend(fontsize=11)
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'likelihood_log_likelihood_comparison.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# Main execution
if __name__ == "__main__":
    print("\n[1/5] Creating main likelihood function...")
    create_likelihood_function_main()
    print("✅ Created: likelihood_function.png")
    
    print("\n[2/5] Creating binomial likelihood (patient recovery)...")
    create_binomial_likelihood_recovery()
    print("✅ Created: binomial_likelihood_recovery.png")
    
    print("\n[3/5] Creating Poisson likelihood (phone calls)...")
    create_poisson_likelihood_calls()
    print("✅ Created: poisson_likelihood_calls.png")
    
    print("\n[4/5] Creating normal likelihood (heights)...")
    create_normal_likelihood_heights()
    print("✅ Created: normal_likelihood_heights.png")
    
    print("\n[5/5] Creating likelihood vs log-likelihood comparison...")
    create_likelihood_log_likelihood_comparison()
    print("✅ Created: likelihood_log_likelihood_comparison.png")
    
    print("\n" + "="*80)
    print("  ✅ ALL 5 LIKELIHOOD FUNCTION IMAGES CREATED SUCCESSFULLY!")
    print("="*80)
    print("\nImages saved to:", output_dir)
    print("\nReady to replace code blocks in the markdown file!")
