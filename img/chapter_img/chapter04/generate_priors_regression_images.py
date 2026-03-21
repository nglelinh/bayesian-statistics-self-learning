#!/usr/bin/env python3
"""
Generate images for Chapter 04.02: Priors for Regression
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Set style
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

# Random seed
np.random.seed(42)

print("Generating Chapter 04.02 images...")

# Generate example data
n = 50
height = np.random.uniform(150, 190, n)  # cm
weight = 50 + 0.7 * height + np.random.normal(0, 5, n)  # kg

# Standardize
height_std = (height - height.mean()) / height.std()
weight_std = (weight - weight.mean()) / weight.std()

# ============================================================================
# Image 1: Standardization Comparison (already exists, skip)
# ============================================================================
# File: standardization_comparison.png already exists

# ============================================================================
# Image 2: Prior for Intercept (α)
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

theta_range = np.linspace(-6, 6, 1000)

priors = [
    (stats.norm(0, 5), 'N(0, 5)', 'Too wide', 'red'),
    (stats.norm(0, 1), 'N(0, 1)', 'Weakly informative ✓', 'green'),
    (stats.norm(0, 0.1), 'N(0, 0.1)', 'Too narrow', 'orange')
]

for ax, (prior, label, title, color) in zip(axes, priors):
    pdf = prior.pdf(theta_range)
    ax.plot(theta_range, pdf, linewidth=3, color=color)
    ax.fill_between(theta_range, pdf, alpha=0.3, color=color)
    ax.set_xlabel('α', fontsize=12, fontweight='bold')
    ax.set_ylabel('Density', fontsize=12, fontweight='bold')
    ax.set_title(f'{title}\nα ~ {label}', fontsize=13, fontweight='bold')
    ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('prior_intercept_comparison.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✓ Saved: prior_intercept_comparison.png")
plt.close()

# ============================================================================
# Image 3: Prior for Slope (β)
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

priors_beta = [
    (stats.norm(0, 5), 'N(0, 5)', 'Too wide', 'red'),
    (stats.norm(0, 1), 'N(0, 1)', 'Weakly informative ✓', 'green'),
    (stats.norm(0, 0.2), 'N(0, 0.2)', 'Too narrow', 'orange')
]

for ax, (prior, label, title, color) in zip(axes, priors_beta):
    pdf = prior.pdf(theta_range)
    ax.plot(theta_range, pdf, linewidth=3, color=color)
    ax.fill_between(theta_range, pdf, alpha=0.3, color=color)
    ax.set_xlabel('β', fontsize=12, fontweight='bold')
    ax.set_ylabel('Density', fontsize=12, fontweight='bold')
    ax.set_title(f'{title}\nβ ~ {label}', fontsize=13, fontweight='bold')
    ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('prior_slope_comparison.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✓ Saved: prior_slope_comparison.png")
plt.close()

# ============================================================================
# Image 4: Prior Predictive Check
# ============================================================================
n_samples = 100
x_range = np.linspace(-3, 3, 100)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Prior 1: N(0, 1) - Weakly informative
alpha_samples = np.random.normal(0, 1, n_samples)
beta_samples = np.random.normal(0, 1, n_samples)

for i in range(n_samples):
    y_pred = alpha_samples[i] + beta_samples[i] * x_range
    axes[0].plot(x_range, y_pred, 'b-', alpha=0.1, linewidth=1)

axes[0].set_xlabel('x (standardized)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('y (standardized)', fontsize=12, fontweight='bold')
axes[0].set_title('Prior Predictive: β ~ N(0, 1)\n' +
                 'Weakly informative ✓',
                 fontsize=14, fontweight='bold', color='green')
axes[0].set_ylim(-6, 6)
axes[0].grid(alpha=0.3)

# Prior 2: N(0, 5) - Too wide
beta_samples_wide = np.random.normal(0, 5, n_samples)

for i in range(n_samples):
    y_pred = alpha_samples[i] + beta_samples_wide[i] * x_range
    axes[1].plot(x_range, y_pred, 'r-', alpha=0.1, linewidth=1)

axes[1].set_xlabel('x (standardized)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('y (standardized)', fontsize=12, fontweight='bold')
axes[1].set_title('Prior Predictive: β ~ N(0, 5)\n' +
                 'Too wide - cho phép slopes vô lý ✗',
                 fontsize=14, fontweight='bold', color='red')
axes[1].set_ylim(-6, 6)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('prior_predictive_slopes.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✓ Saved: prior_predictive_slopes.png")
plt.close()

# ============================================================================
# Image 5: Prior for Noise (σ)
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sigma_range = np.linspace(0, 5, 1000)

# HalfNormal(1)
prior_sigma = stats.halfnorm(0, 1).pdf(sigma_range)
axes[0].plot(sigma_range, prior_sigma, linewidth=3, color='blue')
axes[0].fill_between(sigma_range, prior_sigma, alpha=0.3, color='blue')
axes[0].set_xlabel('σ', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('Prior for σ\nσ ~ HalfNormal(1)',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)

# Interpretation
axes[1].axis('off')
interpretation = """
╔═══════════════════════════════════════════════════════════╗
║              PRIOR FOR NOISE (σ)                          ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  σ ~ HalfNormal(1)                                        ║
║                                                           ║
║  Ý nghĩa:                                                 ║
║    • σ > 0 (must be positive)                             ║
║    • 95% mass trong [0, 2]                                ║
║    • Cho phép flexibility hợp lý                          ║
║                                                           ║
║  Với standardized data:                                   ║
║    • σ < 0.5: Model fit rất tốt                           ║
║    • σ ≈ 1:   Model fit trung bình                        ║
║    • σ > 2:   Model fit kém                               ║
║                                                           ║
║  Tại sao HalfNormal?                                      ║
║    • Weakly informative                                   ║
║    • Tránh σ quá lớn (overfitting)                        ║
║    • Computational stability                              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[1].text(0.5, 0.5, interpretation, fontsize=10, family='monospace',
               ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9))

plt.tight_layout()
plt.savefig('prior_noise_halfnormal.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✓ Saved: prior_noise_halfnormal.png")
plt.close()

# ============================================================================
# Image 6: Prior Sensitivity Analysis
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# True posterior (assumed)
beta_true = 0.7
beta_range = np.linspace(-1, 2, 1000)

# Different priors
priors_to_test = [
    (stats.norm(0, 0.5), 'N(0, 0.5)', 'narrow'),
    (stats.norm(0, 1), 'N(0, 1)', 'weakly informative'),
    (stats.norm(0, 2), 'N(0, 2)', 'wide')
]

# Simulate posteriors (simplified: prior + likelihood)
for prior, label, desc in priors_to_test:
    # Simplified posterior (not exact)
    posterior = stats.norm(beta_true, 0.1).pdf(beta_range) * prior.pdf(beta_range)
    posterior = posterior / np.trapz(posterior, beta_range)
    
    axes[0].plot(beta_range, posterior, linewidth=2, label=f'Prior: {label}')

axes[0].axvline(beta_true, color='red', linestyle='--', linewidth=2,
               label=f'True β = {beta_true}')
axes[0].set_xlabel('β', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Posterior Density', fontsize=12, fontweight='bold')
axes[0].set_title('Prior Sensitivity Analysis\n' +
                 'Posterior với priors khác nhau',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Summary
axes[1].axis('off')
summary = """
╔═══════════════════════════════════════════════════════════╗
║           PRIOR SENSITIVITY ANALYSIS                      ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Câu hỏi:                                                 ║
║    Posterior có thay đổi nhiều khi prior thay đổi?       ║
║                                                           ║
║  Nếu YES (sensitive):                                     ║
║    • Data ít hoặc weak                                    ║
║    • Prior có ảnh hưởng lớn                               ║
║    • Cần cẩn thận chọn prior                              ║
║    • Report sensitivity analysis                          ║
║                                                           ║
║  Nếu NO (robust):                                         ║
║    • Data nhiều và strong                                 ║
║    • Prior ít ảnh hưởng                                   ║
║    • Posterior chủ yếu từ likelihood                      ║
║    • Prior choice ít quan trọng                           ║
║                                                           ║
║  Best practice:                                           ║
║    → LUÔN kiểm tra prior sensitivity                      ║
║    → Report kết quả với multiple priors                   ║
║    → Nếu sensitive, justify prior choice                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[1].text(0.5, 0.5, summary, fontsize=10, family='monospace',
               ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.savefig('prior_sensitivity_analysis.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✓ Saved: prior_sensitivity_analysis.png")
plt.close()

print("\n" + "="*70)
print("COMPLETE: All Chapter 04.02 images generated successfully!")
print("="*70)
print(f"\nGenerated 5 images:")
print("  1. prior_intercept_comparison.png - α prior comparison")
print("  2. prior_slope_comparison.png - β prior comparison")
print("  3. prior_predictive_slopes.png - Prior predictive check")
print("  4. prior_noise_halfnormal.png - σ prior with interpretation")
print("  5. prior_sensitivity_analysis.png - Sensitivity analysis")
print("\nNote: standardization_comparison.png already exists")
