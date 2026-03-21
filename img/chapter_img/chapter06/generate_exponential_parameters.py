#!/usr/bin/env python3
"""
Generate exponential function parameter effects visualization for Poisson regression
Replaces code block at line 133 in 06_02_poisson_regression.md
"""

import numpy as np
import matplotlib.pyplot as plt

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# Generate x values
x_vals = np.linspace(-3, 3, 200)

# Create figure with 3 panels
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Panel 1: Basic exponential function
lambda_vals = np.exp(x_vals)
axes[0].plot(x_vals, lambda_vals, 'b-', linewidth=3)
axes[0].axhline(1, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[0].axvline(0, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[0].set_xlabel('η = α + βx', fontsize=12, fontweight='bold')
axes[0].set_ylabel('λ = E[y]', fontsize=12, fontweight='bold')
axes[0].set_title('EXPONENTIAL FUNCTION\nλ = e^η',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)
axes[0].set_ylim(0, 20)
axes[0].text(0.2, 1, 'η=0 → λ=1', fontsize=11, ha='left', va='bottom',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
axes[0].fill_between(x_vals, 0, lambda_vals, alpha=0.2, color='blue')

# Panel 2: Effect of α (intercept) - shifts baseline rate
colors = ['#e74c3c', '#3498db', '#27ae60']
alphas = [-1, 0, 1]
for alpha, color in zip(alphas, colors):
    lambda_curve = np.exp(alpha + 0.5*x_vals)
    axes[1].plot(x_vals, lambda_curve, linewidth=2.5, label=f'α = {alpha}', color=color)
    # Mark the rate at x=0
    axes[1].plot(0, np.exp(alpha), 'o', markersize=8, color=color)
    
axes[1].axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
axes[1].set_xlabel('x', fontsize=12, fontweight='bold')
axes[1].set_ylabel('λ = E[y]', fontsize=12, fontweight='bold')
axes[1].set_title('EFFECT OF α (Intercept)\nShifts baseline rate',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11, loc='upper left')
axes[1].grid(alpha=0.3)
axes[1].set_ylim(0, 20)
axes[1].text(-2, 15, 'Higher α → Higher baseline', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

# Panel 3: Effect of β (slope) - changes growth rate
betas = [0.2, 0.5, 1]
colors3 = ['#9b59b6', '#3498db', '#e67e22']
for beta, color in zip(betas, colors3):
    lambda_curve = np.exp(beta * x_vals)
    axes[2].plot(x_vals, lambda_curve, linewidth=2.5, label=f'β = {beta}', color=color)
    
axes[2].axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
axes[2].axhline(1, color='gray', linestyle='--', linewidth=1, alpha=0.5)
axes[2].set_xlabel('x', fontsize=12, fontweight='bold')
axes[2].set_ylabel('λ = E[y]', fontsize=12, fontweight='bold')
axes[2].set_title('EFFECT OF β (Slope)\nSteeper = stronger effect',
                 fontsize=14, fontweight='bold')
axes[2].legend(fontsize=11, loc='upper left')
axes[2].grid(alpha=0.3)
axes[2].set_ylim(0, 20)
axes[2].annotate('Exponential growth\nfaster with larger β',
                xy=(1.5, 10), xytext=(0.5, 15),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig('exponential_function_parameters.png', dpi=300, bbox_inches='tight',
            facecolor='white')
print("✓ Generated: exponential_function_parameters.png")
print("  - Basic exponential function λ = e^η")
print("  - α effect: Shifts baseline rate (multiplicative shift)")
print("  - β effect: Changes growth rate (stronger = steeper curve)")

plt.close()
