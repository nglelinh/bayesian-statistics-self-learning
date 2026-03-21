#!/usr/bin/env python3
"""
Generate prior distributions comparison (Normal vs Laplace)
Replaces code block at line 140 in 07_01_regularization_priors.md
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

beta_vals = np.linspace(-3, 3, 200)

# Normal (Ridge)
normal_prior = stats.norm.pdf(beta_vals, 0, 1)

# Laplace (Lasso)
laplace_prior = stats.laplace.pdf(beta_vals, 0, 0.7)

# Uniform (no regularization)
uniform_prior = np.ones_like(beta_vals) * 0.3

# Create figure with 3 panels
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Panel 1: Normal prior (Ridge)
axes[0].plot(beta_vals, normal_prior, 'b-', linewidth=3)
axes[0].fill_between(beta_vals, normal_prior, alpha=0.3, color='blue')
axes[0].axvline(0, color='red', linestyle='--', linewidth=2, alpha=0.5)
axes[0].set_xlabel('β', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('NORMAL PRIOR\n(Ridge / L2 Regularization)\nβ ~ Normal(0, σ²)',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)
axes[0].text(0, max(normal_prior)*0.6, 'Prefers small β\nGaussian tails\n(Shrinks coefficients)',
            ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
axes[0].set_ylim(0, max(normal_prior)*1.1)

# Panel 2: Laplace prior (Lasso)
axes[1].plot(beta_vals, laplace_prior, 'g-', linewidth=3)
axes[1].fill_between(beta_vals, laplace_prior, alpha=0.3, color='green')
axes[1].axvline(0, color='red', linestyle='--', linewidth=2, alpha=0.5)
axes[1].set_xlabel('β', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('LAPLACE PRIOR\n(Lasso / L1 Regularization)\nβ ~ Laplace(0, b)',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)
axes[1].text(0, max(laplace_prior)*0.6, 'Sharp peak at 0\nHeavy tails\n(Sets many β to 0)',
            ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
axes[1].set_ylim(0, max(laplace_prior)*1.1)

# Panel 3: Comparison
axes[2].plot(beta_vals, normal_prior, 'b-', linewidth=3, label='Normal (Ridge)')
axes[2].plot(beta_vals, laplace_prior, 'g-', linewidth=3, label='Laplace (Lasso)')
axes[2].plot(beta_vals, uniform_prior, 'r--', linewidth=2, label='Uniform (No reg.)',
            alpha=0.7)
axes[2].axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
axes[2].set_xlabel('β', fontsize=12, fontweight='bold')
axes[2].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[2].set_title('COMPARISON\nNormal vs Laplace vs Uniform',
                 fontsize=14, fontweight='bold')
axes[2].legend(fontsize=11, loc='upper right')
axes[2].grid(alpha=0.3)
axes[2].set_ylim(0, max(laplace_prior)*1.1)

# Add annotation comparing characteristics
axes[2].annotate('Laplace has sharper\npeak → more sparsity',
                xy=(0, max(laplace_prior)), xytext=(-1.5, max(laplace_prior)*0.8),
                arrowprops=dict(arrowstyle='->', color='green', lw=2),
                fontsize=9, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

plt.suptitle('Regularization Priors: Ridge (L2) vs Lasso (L1)',
            fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('regularization_priors.png', dpi=300, bbox_inches='tight',
            facecolor='white')
print("✓ Generated: regularization_priors.png")
print("  - Normal prior: Ridge/L2 regularization (shrinks coefficients)")
print("  - Laplace prior: Lasso/L1 regularization (sparse, sets many to 0)")
print("  - Laplace has sharper peak → stronger sparsity inducing")

plt.close()
