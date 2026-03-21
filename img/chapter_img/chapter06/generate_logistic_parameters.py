#!/usr/bin/env python3
"""
Generate logistic function parameter effects visualization
Replaces code block at line 133 in 06_01_logistic_regression.md
"""

import numpy as np
import matplotlib.pyplot as plt

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# Generate x values
x_vals = np.linspace(-6, 6, 200)

# Create figure with 3 panels
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Panel 1: Basic logistic function
p_vals = 1 / (1 + np.exp(-x_vals))
axes[0].plot(x_vals, p_vals, 'b-', linewidth=3)
axes[0].axhline(0.5, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[0].axvline(0, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[0].set_xlabel('η = α + βx', fontsize=12, fontweight='bold')
axes[0].set_ylabel('p = P(y=1)', fontsize=12, fontweight='bold')
axes[0].set_title('LOGISTIC FUNCTION\np = 1/(1+e⁻ᶯ)',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)
axes[0].text(0.2, 0.5, 'η=0 → p=0.5', fontsize=11, ha='left', va='bottom',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
axes[0].set_ylim(-0.05, 1.05)

# Panel 2: Effect of α (intercept) - shifts curve left/right
colors = ['#e74c3c', '#3498db', '#27ae60']
alphas = [-2, 0, 2]
for alpha, color in zip(alphas, colors):
    p = 1 / (1 + np.exp(-(alpha + x_vals)))
    axes[1].plot(x_vals, p, linewidth=2.5, label=f'α = {alpha}', color=color)
    # Mark the inflection point (where p=0.5)
    axes[1].plot(-alpha, 0.5, 'o', markersize=8, color=color)
    
axes[1].axhline(0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
axes[1].set_xlabel('x', fontsize=12, fontweight='bold')
axes[1].set_ylabel('P(y=1)', fontsize=12, fontweight='bold')
axes[1].set_title('EFFECT OF α (Intercept)\nShifts curve horizontally',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11, loc='upper left')
axes[1].grid(alpha=0.3)
axes[1].set_ylim(-0.05, 1.05)
axes[1].annotate('', xy=(-2, 0.5), xytext=(0, 0.5),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
axes[1].text(-1, 0.55, 'Shift', fontsize=10, ha='center')

# Panel 3: Effect of β (slope) - changes steepness
betas = [0.5, 1, 2]
colors3 = ['#9b59b6', '#3498db', '#e67e22']
for beta, color in zip(betas, colors3):
    p = 1 / (1 + np.exp(-(beta * x_vals)))
    axes[2].plot(x_vals, p, linewidth=2.5, label=f'β = {beta}', color=color)
    
axes[2].axhline(0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
axes[2].axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
axes[2].set_xlabel('x', fontsize=12, fontweight='bold')
axes[2].set_ylabel('P(y=1)', fontsize=12, fontweight='bold')
axes[2].set_title('EFFECT OF β (Slope)\nSteeper = stronger effect',
                 fontsize=14, fontweight='bold')
axes[2].legend(fontsize=11, loc='upper left')
axes[2].grid(alpha=0.3)
axes[2].set_ylim(-0.05, 1.05)
axes[2].annotate('Steeper', xy=(1, 0.75), xytext=(2, 0.85),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))

plt.tight_layout()
plt.savefig('logistic_function_parameters.png', dpi=300, bbox_inches='tight',
            facecolor='white')
print("✓ Generated: logistic_function_parameters.png")
print("  - Basic logistic function with inflection point at η=0")
print("  - α effect: Shifts curve horizontally (changes baseline probability)")
print("  - β effect: Changes steepness (strength of effect)")

plt.close()
