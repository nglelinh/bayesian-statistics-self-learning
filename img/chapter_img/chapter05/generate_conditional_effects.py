#!/usr/bin/env python3
"""
Generate conditional effects visualization for interaction model
Replaces code block at line 159 in 05_04_interaction_effects.md
"""

import numpy as np
import matplotlib.pyplot as plt

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# Simulate posterior samples (based on interaction model)
np.random.seed(42)
n_samples = 8000

# Posterior samples for parameters
beta1_samples = np.random.normal(0.6, 0.15, n_samples)  # Main effect of x1
beta3_samples = np.random.normal(0.8, 0.2, n_samples)   # Interaction effect

# Conditional effects
effect_x2_0 = beta1_samples  # Effect when x2=0
effect_x2_1 = beta1_samples + beta3_samples  # Effect when x2=1

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Left panel: Conditional effects
axes[0].hist(effect_x2_0, bins=50, density=True, alpha=0.7,
            label='x₂ = 0 (Control)', edgecolor='black', color='#3498db')
axes[0].hist(effect_x2_1, bins=50, density=True, alpha=0.7,
            label='x₂ = 1 (Treatment)', edgecolor='black', color='#e67e22')
axes[0].axvline(effect_x2_0.mean(), color='blue', linewidth=2, linestyle='--')
axes[0].axvline(effect_x2_1.mean(), color='darkorange', linewidth=2, linestyle='--')
axes[0].set_xlabel('Effect of x₁ on y', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('CONDITIONAL EFFECTS\n' +
                 f'Control: {effect_x2_0.mean():.2f}\n' +
                 f'Treatment: {effect_x2_1.mean():.2f}',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')
axes[0].set_xlim(-0.2, 2.2)

# Right panel: Difference (interaction)
difference = effect_x2_1 - effect_x2_0  # This equals beta3
axes[1].hist(difference, bins=50, density=True, alpha=0.7,
            color='#27ae60', edgecolor='black')
axes[1].axvline(difference.mean(), color='red', linewidth=3,
               label=f'Mean = {difference.mean():.2f}')
axes[1].axvline(0, color='black', linestyle='--', linewidth=2,
               label='No interaction')
axes[1].set_xlabel('Difference in Effects', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('INTERACTION = DIFFERENCE\n' +
                 'β₃ = Effect(x₂=1) - Effect(x₂=0)',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3, axis='y')
axes[1].set_xlim(-0.2, 1.8)

plt.tight_layout()
plt.savefig('conditional_effects.png', dpi=300, bbox_inches='tight',
            facecolor='white')
print("✓ Generated: conditional_effects.png")
print(f"  - Effect when x₂=0 (Control): {effect_x2_0.mean():.3f}")
print(f"  - Effect when x₂=1 (Treatment): {effect_x2_1.mean():.3f}")
print(f"  - Interaction (Difference): {difference.mean():.3f}")

plt.close()
