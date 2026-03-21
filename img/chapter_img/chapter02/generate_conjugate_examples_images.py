#!/usr/bin/env python3
"""
Generate detailed conjugate prior examples images for Chapter 02
- Normal-Normal conjugacy
- Gamma-Poisson conjugacy
- When NOT to use conjugate priors
- Summary infographic
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import comb

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.dpi'] = 300

# ============================================================================
# Image 1: Normal-Normal Conjugacy (detailed example)
# ============================================================================
def generate_normal_normal_conjugacy():
    """Generate detailed Normal-Normal conjugacy visualization"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Setup: Measuring heights, σ = 10 cm (known)
    sigma = 10
    true_mu = 170
    
    # Prior: Normal(165, 15²)
    mu0, sigma0 = 165, 15
    prior_normal = stats.norm(mu0, sigma0)
    
    # Data
    np.random.seed(42)
    n = 20
    data = np.random.normal(true_mu, sigma, n)
    sample_mean = data.mean()
    
    # Posterior: Normal(μ₁, σ₁²)
    # Precision (inverse variance)
    precision0 = 1 / sigma0**2
    precision_likelihood = n / sigma**2
    precision1 = precision0 + precision_likelihood
    sigma1 = np.sqrt(1 / precision1)
    
    mu1 = (mu0 * precision0 + sample_mean * n / sigma**2) / precision1
    posterior_normal = stats.norm(mu1, sigma1)
    
    # Plot 1: Prior and Posterior
    mu_grid = np.linspace(150, 190, 1000)
    
    axes[0, 0].plot(mu_grid, prior_normal.pdf(mu_grid), linewidth=2, 
                   label=f'Prior: N({mu0}, {sigma0}²)', linestyle='--')
    axes[0, 0].plot(mu_grid, posterior_normal.pdf(mu_grid), linewidth=3, 
                   label=f'Posterior: N({mu1:.1f}, {sigma1:.1f}²)')
    axes[0, 0].axvline(sample_mean, color='red', linestyle=':', linewidth=2, 
                      label=f'Sample mean = {sample_mean:.1f}')
    axes[0, 0].axvline(true_mu, color='green', linestyle=':', linewidth=2, 
                      label=f'True μ = {true_mu}', alpha=0.5)
    axes[0, 0].set_xlabel('μ (chiều cao, cm)', fontsize=11)
    axes[0, 0].set_ylabel('Mật độ', fontsize=11)
    axes[0, 0].set_title(f'Normal-Normal Conjugacy\nn = {n}, σ = {sigma} (biết)', 
                        fontsize=12, fontweight='bold')
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].grid(alpha=0.3)
    
    # Plot 2: Formula explanation
    axes[0, 1].axis('off')
    formula_normal = f"""NORMAL-NORMAL CONJUGACY

Prior:
  μ ~ Normal({mu0}, {sigma0}²)
  Precision: 1/σ₀² = {precision0:.6f}

Likelihood:
  xᵢ ~ Normal(μ, {sigma}²)
  n = {n}
  x̄ = {sample_mean:.2f}
  Precision: n/σ² = {precision_likelihood:.6f}

Posterior:
  μ ~ Normal({mu1:.2f}, {sigma1:.2f}²)
  
  Precision: 1/σ₁² = 1/σ₀² + n/σ²
           = {precision0:.6f} + {precision_likelihood:.6f}
           = {precision1:.6f}
  
  σ₁ = √(1/{precision1:.6f}) = {sigma1:.2f}
  
  μ₁ = (μ₀/σ₀² + nx̄/σ²) / (1/σ₀² + n/σ²)
     = {mu1:.2f}

→ Posterior là TRUNG BÌNH CÓ TRỌNG SỐ
  của prior mean và sample mean!
"""
    
    axes[0, 1].text(0.5, 0.5, formula_normal, fontsize=9, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Plot 3: Effect of sample size
    axes[1, 0].plot(mu_grid, prior_normal.pdf(mu_grid), linewidth=2, 
                   label='Prior', linestyle='--', alpha=0.5)
    
    for n_sim in [5, 20, 50, 100]:
        data_sim = np.random.normal(true_mu, sigma, n_sim)
        sample_mean_sim = data_sim.mean()
        
        precision_sim = precision0 + n_sim / sigma**2
        sigma_sim = np.sqrt(1 / precision_sim)
        mu_sim = (mu0 * precision0 + sample_mean_sim * n_sim / sigma**2) / precision_sim
        
        post_sim = stats.norm(mu_sim, sigma_sim)
        axes[1, 0].plot(mu_grid, post_sim.pdf(mu_grid), linewidth=2, 
                       label=f'n={n_sim}: μ={mu_sim:.1f}, σ={sigma_sim:.1f}')
    
    axes[1, 0].axvline(true_mu, color='green', linestyle=':', linewidth=2, 
                      label=f'True μ = {true_mu}', alpha=0.5)
    axes[1, 0].set_xlabel('μ', fontsize=11)
    axes[1, 0].set_ylabel('Mật độ', fontsize=11)
    axes[1, 0].set_title('Ảnh hưởng của Kích thước Mẫu\nPosterior hội tụ về true μ', 
                        fontsize=12, fontweight='bold')
    axes[1, 0].legend(fontsize=9)
    axes[1, 0].grid(alpha=0.3)
    
    # Plot 4: Prior vs Data weights
    n_range = np.arange(1, 101)
    weight_prior = precision0 / (precision0 + n_range / sigma**2)
    weight_data = (n_range / sigma**2) / (precision0 + n_range / sigma**2)
    
    axes[1, 1].plot(n_range, weight_prior, linewidth=2, label='Trọng số Prior')
    axes[1, 1].plot(n_range, weight_data, linewidth=2, label='Trọng số Data')
    axes[1, 1].set_xlabel('Kích thước mẫu (n)', fontsize=11)
    axes[1, 1].set_ylabel('Trọng số', fontsize=11)
    axes[1, 1].set_title('Trọng số Prior vs Data\nData càng nhiều → trọng số càng lớn', 
                        fontsize=12, fontweight='bold')
    axes[1, 1].legend(fontsize=10)
    axes[1, 1].grid(alpha=0.3)
    axes[1, 1].set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig('normal_normal_conjugacy_detailed.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print("✓ Generated: normal_normal_conjugacy_detailed.png")
    plt.close()

# ============================================================================
# Image 2: Gamma-Poisson Conjugacy (detailed example)
# ============================================================================
def generate_gamma_poisson_conjugacy():
    """Generate detailed Gamma-Poisson conjugacy visualization"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Setup: Number of bugs in code
    # Prior: Gamma(2, 1) → E[λ] = 2 bugs/1000 lines
    alpha_prior, beta_prior = 2, 1
    prior_gamma = stats.gamma(alpha_prior, scale=1/beta_prior)
    
    # Data: Observed 10 files, total 25 bugs
    n_files = 10
    total_errors = 25
    
    # Posterior: Gamma(α + Σxᵢ, β + n)
    alpha_post = alpha_prior + total_errors
    beta_post = beta_prior + n_files
    posterior_gamma = stats.gamma(alpha_post, scale=1/beta_post)
    
    # Plot 1: Prior and Posterior
    lambda_grid = np.linspace(0, 8, 1000)
    
    axes[0, 0].plot(lambda_grid, prior_gamma.pdf(lambda_grid), linewidth=2, 
                   label=f'Prior: Gamma({alpha_prior}, {beta_prior})', linestyle='--')
    axes[0, 0].plot(lambda_grid, posterior_gamma.pdf(lambda_grid), linewidth=3, 
                   label=f'Posterior: Gamma({alpha_post}, {beta_post})')
    axes[0, 0].axvline(total_errors/n_files, color='red', linestyle=':', linewidth=2, 
                      label=f'MLE = {total_errors/n_files:.2f}')
    axes[0, 0].set_xlabel('λ (lỗi/file)', fontsize=11)
    axes[0, 0].set_ylabel('Mật độ', fontsize=11)
    axes[0, 0].set_title(f'Gamma-Poisson Conjugacy\n{total_errors} lỗi trong {n_files} files', 
                        fontsize=12, fontweight='bold')
    axes[0, 0].legend(fontsize=10)
    axes[0, 0].grid(alpha=0.3)
    
    # Plot 2: Formula explanation
    axes[0, 1].axis('off')
    formula_gamma = f"""GAMMA-POISSON CONJUGACY

Prior:
  λ ~ Gamma({alpha_prior}, {beta_prior})
  E[λ] = α/β = {alpha_prior/beta_prior:.2f}
  Var[λ] = α/β² = {alpha_prior/beta_prior**2:.2f}

Likelihood:
  xᵢ ~ Poisson(λ)
  n = {n_files} files
  Σxᵢ = {total_errors} lỗi

Posterior:
  λ ~ Gamma(α + Σxᵢ, β + n)
    = Gamma({alpha_post}, {beta_post})
  
  E[λ] = {alpha_post}/{beta_post} = {alpha_post/beta_post:.2f}
  Var[λ] = {alpha_post}/{beta_post**2} = {alpha_post/beta_post**2:.2f}

95% CI: [{posterior_gamma.ppf(0.025):.2f}, 
         {posterior_gamma.ppf(0.975):.2f}]

→ Kỳ vọng ~{alpha_post/beta_post:.1f} lỗi/file
"""
    
    axes[0, 1].text(0.5, 0.5, formula_gamma, fontsize=10, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Plot 3: Posterior Predictive (Negative Binomial)
    def negative_binomial_pmf(k, r, p):
        """Negative Binomial PMF"""
        return comb(k + r - 1, k) * (1 - p)**r * p**k
    
    # Posterior predictive for Gamma-Poisson is Negative Binomial
    # with r = α_post, p = 1/(1 + β_post)
    r = alpha_post
    p = 1 / (1 + beta_post)
    
    k_range = np.arange(0, 15)
    ppd = [negative_binomial_pmf(k, r, p) for k in k_range]
    
    axes[1, 0].bar(k_range, ppd, alpha=0.7, edgecolor='black')
    axes[1, 0].axvline(alpha_post/beta_post, color='red', linestyle='--', linewidth=2,
                      label=f'E[k] = {alpha_post/beta_post:.2f}')
    axes[1, 0].set_xlabel('k (số lỗi trong file MỚI)', fontsize=11)
    axes[1, 0].set_ylabel('Xác suất', fontsize=11)
    axes[1, 0].set_title('Posterior Predictive Distribution\nDự đoán số lỗi trong file mới', 
                        fontsize=12, fontweight='bold')
    axes[1, 0].legend(fontsize=10)
    axes[1, 0].grid(alpha=0.3, axis='y')
    
    # Plot 4: Sequential updating
    axes[1, 1].plot(lambda_grid, prior_gamma.pdf(lambda_grid), linewidth=2, 
                   label=f'Prior: Gamma({alpha_prior}, {beta_prior})', linestyle='--', alpha=0.5)
    
    # Simulate sequential observations
    observations = [3, 2, 5, 2, 1, 3, 4, 2, 1, 2]  # 10 files with bugs
    alpha_seq = alpha_prior
    beta_seq = beta_prior
    
    for i, obs in enumerate([5, 10]):  # Show after 5 and 10 files
        alpha_seq_temp = alpha_prior + sum(observations[:obs])
        beta_seq_temp = beta_prior + obs
        post_seq = stats.gamma(alpha_seq_temp, scale=1/beta_seq_temp)
        axes[1, 1].plot(lambda_grid, post_seq.pdf(lambda_grid), linewidth=2,
                       label=f'Sau {obs} files: Gamma({alpha_seq_temp}, {beta_seq_temp})')
    
    axes[1, 1].set_xlabel('λ', fontsize=11)
    axes[1, 1].set_ylabel('Mật độ', fontsize=11)
    axes[1, 1].set_title('Sequential Updating\nPosterior càng hẹp khi có thêm dữ liệu', 
                        fontsize=12, fontweight='bold')
    axes[1, 1].legend(fontsize=9)
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('gamma_poisson_conjugacy_detailed.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: gamma_poisson_conjugacy_detailed.png")
    plt.close()

# ============================================================================
# Image 3: When NOT to use Conjugate Priors
# ============================================================================
def generate_conjugate_limitations():
    """Generate visualization of conjugate prior limitations"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    theta = np.linspace(0, 1, 1000)
    
    # Situation 1: Known θ ∈ [0.2, 0.4]
    # Beta conjugate cannot represent well
    
    # Try Beta(20, 30) - closest
    beta_conjugate = stats.beta(20, 30)
    
    # Ideal prior: Uniform on [0.2, 0.4]
    def ideal_prior(theta):
        return np.where((theta >= 0.2) & (theta <= 0.4), 1/0.2, 0)
    
    axes[0, 0].plot(theta, beta_conjugate.pdf(theta), linewidth=2, 
                   label='Beta(20, 30) - Conjugate')
    axes[0, 0].plot(theta, ideal_prior(theta), linewidth=2, 
                   label='Uniform[0.2, 0.4] - Lý tưởng', linestyle='--')
    axes[0, 0].set_xlabel('θ', fontsize=11)
    axes[0, 0].set_ylabel('Mật độ', fontsize=11)
    axes[0, 0].set_title('Prior Conjugate vs Lý tưởng\nConjugate KHÔNG thể biểu diễn tốt!', 
                        fontsize=12, fontweight='bold')
    axes[0, 0].legend(fontsize=10)
    axes[0, 0].grid(alpha=0.3)
    axes[0, 0].set_ylim(0, 10)
    
    # Plot 2: Explanation
    axes[0, 1].axis('off')
    explanation1 = """╔═══════════════════════════════════════════════════════════╗
║         KHI NÀO KHÔNG DÙNG CONJUGATE?                     ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  1. Prior phức tạp                                        ║
║     • Multimodal                                          ║
║     • Truncated                                           ║
║     • Mixture                                             ║
║     → Conjugate không biểu diễn được                      ║
║                                                           ║
║  2. Likelihood phức tạp                                   ║
║     • Không có conjugate                                  ║
║     • Ví dụ: Logistic regression                          ║
║              Neural networks                              ║
║                                                           ║
║  3. Model phức tạp                                        ║
║     • Hierarchical                                        ║
║     • Nhiều tham số phụ thuộc                             ║
║     → Không có conjugate đơn giản                         ║
║                                                           ║
║  GIẢI PHÁP:                                               ║
║    → Dùng MCMC (sẽ học ở bài sau)                         ║
║    → Grid approximation                                   ║
║    → Variational inference                                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    
    axes[0, 1].text(0.5, 0.5, explanation1, fontsize=9, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='#ffcccc', alpha=0.8))
    
    # Plot 3: Mixture prior example
    # Prior: 50% believe θ~0.3, 50% believe θ~0.7
    mixture_prior = 0.5 * stats.beta(30, 70).pdf(theta) + 0.5 * stats.beta(70, 30).pdf(theta)
    
    axes[1, 0].plot(theta, mixture_prior, linewidth=3, label='Mixture Prior (lý tưởng)')
    axes[1, 0].plot(theta, stats.beta(50, 50).pdf(theta), linewidth=2, 
                   label='Beta(50, 50) - Conjugate', linestyle='--', alpha=0.7)
    axes[1, 0].set_xlabel('θ', fontsize=11)
    axes[1, 0].set_ylabel('Mật độ', fontsize=11)
    axes[1, 0].set_title('Mixture Prior\nConjugate KHÔNG thể biểu diễn bimodal!', 
                        fontsize=12, fontweight='bold')
    axes[1, 0].legend(fontsize=10)
    axes[1, 0].grid(alpha=0.3)
    
    # Plot 4: Decision tree
    axes[1, 1].axis('off')
    decision = """    NÊN DÙNG CONJUGATE PRIOR?
    
    ┌─────────────────────────┐
    │ Prior đơn giản?         │
    │ (unimodal, standard)    │
    └────────┬────────────────┘
             │
        ┌────┴────┐
        │         │
       YES       NO → MCMC
        │
    ┌───┴────────────────────┐
    │ Likelihood standard?   │
    │ (Binomial, Normal,     │
    │  Poisson, etc.)        │
    └────────┬───────────────┘
             │
        ┌────┴────┐
        │         │
       YES       NO → MCMC
        │
    ┌───┴────────────────────┐
    │ Model đơn giản?        │
    │ (1 tham số, không      │
    │  hierarchical)         │
    └────────┬───────────────┘
             │
        ┌────┴────┐
        │         │
       YES       NO → MCMC
        │
        ▼
    ✓ DÙNG CONJUGATE!
    
    → Tiết kiệm thời gian
    → Chính xác 100%
"""
    
    axes[1, 1].text(0.5, 0.5, decision, fontsize=9, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('conjugate_prior_limitations.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: conjugate_prior_limitations.png")
    plt.close()

# ============================================================================
# Image 4: Summary Infographic
# ============================================================================
def generate_conjugate_summary():
    """Generate summary infographic for conjugate priors"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    summary = """╔═══════════════════════════════════════════════════════════════════════════╗
║                   CONJUGATE PRIORS - TÓM TẮT                               ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  1. ĐỊNH NGHĨA                                                             ║
║     Prior và Posterior CÙNG HỌ phân phối                                  ║
║     → Tính toán GIẢI TÍCH, không cần MCMC                                 ║
║                                                                           ║
║  2. CÁC CẶP PHỔ BIẾN                                                       ║
║     • Beta - Binomial: Xác suất, tỷ lệ                                    ║
║     • Normal - Normal: Mean (σ² biết)                                     ║
║     • Gamma - Poisson: Count data                                         ║
║     • Gamma - Exponential: Thời gian                                      ║
║     • Inverse-Gamma - Normal: Variance (μ biết)                           ║
║     • Dirichlet - Multinomial: Nhiều lớp                                  ║
║                                                                           ║
║  3. LỢI ÍCH                                                                ║
║     ✓ Tính toán nhanh, chính xác                                          ║
║     ✓ Dễ cập nhật tuần tự                                                 ║
║     ✓ Diễn giải rõ ràng                                                   ║
║     ✓ Không cần MCMC                                                      ║
║                                                                           ║
║  4. HẠN CHẾ                                                                ║
║     • Chỉ có một số cặp conjugate                                         ║
║     • Prior phức tạp → không biểu diễn được                               ║
║     • Model phức tạp → không có conjugate                                 ║
║                                                                           ║
║  5. KHI NÀO DÙNG?                                                          ║
║     ✓ Model đơn giản                                                      ║
║     ✓ Prior standard                                                      ║
║     ✓ Cần tính nhanh                                                      ║
║     ✓ Giảng dạy, minh họa                                                 ║
║                                                                           ║
║  6. KHI NÀO KHÔNG DÙNG?                                                    ║
║     → Model phức tạp → MCMC                                               ║
║     → Prior phức tạp → MCMC                                               ║
║     → Likelihood không standard → MCMC                                    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""
    
    ax.text(0.5, 0.5, summary, fontsize=10, family='monospace',
           ha='center', va='center',
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('conjugate_priors_summary.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: conjugate_priors_summary.png")
    plt.close()

# ============================================================================
# Main execution
# ============================================================================
if __name__ == "__main__":
    print("Generating conjugate prior example images for Chapter 02...")
    print("=" * 70)
    
    generate_normal_normal_conjugacy()
    generate_gamma_poisson_conjugacy()
    generate_conjugate_limitations()
    generate_conjugate_summary()
    
    print("=" * 70)
    print("✓ All conjugate prior example images generated successfully!")
    print("\nGenerated files:")
    print("  1. normal_normal_conjugacy_detailed.png")
    print("  2. gamma_poisson_conjugacy_detailed.png")
    print("  3. conjugate_prior_limitations.png")
    print("  4. conjugate_priors_summary.png")
