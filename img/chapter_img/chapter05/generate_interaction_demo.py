#!/usr/bin/env python3
"""
Generate interaction effects demonstration image
"""

import numpy as np
import matplotlib.pyplot as plt

def linear_fit(X, y):
    """Simple linear regression"""
    X_mean = np.mean(X)
    y_mean = np.mean(y)
    b = np.sum((X - X_mean) * (y - y_mean)) / np.sum((X - X_mean)**2)
    a = y_mean - b * X_mean
    return a, b

# Set style
plt.style.use('default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

print("Generating interaction_demo.png...")

# Generate data
np.random.seed(42)
n = 100

# Continuous predictor
x1 = np.random.uniform(0, 10, n)
# Binary predictor (e.g., treatment vs control)
x2 = np.random.binomial(1, 0.5, n)

# ADDITIVE: y = 2 + 0.5*x1 + 3*x2
y_additive = 2 + 0.5*x1 + 3*x2 + np.random.normal(0, 1, n)

# INTERACTIVE: y = 2 + 0.5*x1 + 3*x2 + 0.8*(x1*x2)
y_interactive = 2 + 0.5*x1 + 3*x2 + 0.8*(x1*x2) + np.random.normal(0, 1, n)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Additive model
mask0 = x2 == 0
mask1 = x2 == 1

axes[0].scatter(x1[mask0], y_additive[mask0], s=60, alpha=0.6, 
               label='x₂ = 0 (Control)', edgecolors='black', color='blue')
axes[0].scatter(x1[mask1], y_additive[mask1], s=60, alpha=0.6, 
               label='x₂ = 1 (Treatment)', edgecolors='black', color='orange')

# Fit lines
a0, b0 = linear_fit(x1[mask0], y_additive[mask0])
a1, b1 = linear_fit(x1[mask1], y_additive[mask1])

x_line = np.linspace(0, 10, 100)
axes[0].plot(x_line, a0 + b0 * x_line,
            'b-', linewidth=3, label=f'Slope₀ = {b0:.2f}')
axes[0].plot(x_line, a1 + b1 * x_line,
            'orange', linewidth=3, label=f'Slope₁ = {b1:.2f}')

axes[0].set_xlabel('x₁', fontsize=12, fontweight='bold')
axes[0].set_ylabel('y', fontsize=12, fontweight='bold')
axes[0].set_title('ADDITIVE MODEL\n' +
                 'y = α + β₁x₁ + β₂x₂\n' +
                 'Parallel lines (same slopes!)',
                 fontsize=14, fontweight='bold', color='blue')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Interactive model
axes[1].scatter(x1[mask0], y_interactive[mask0], s=60, alpha=0.6,
               label='x₂ = 0 (Control)', edgecolors='black', color='blue')
axes[1].scatter(x1[mask1], y_interactive[mask1], s=60, alpha=0.6,
               label='x₂ = 1 (Treatment)', edgecolors='black', color='orange')

a0_int, b0_int = linear_fit(x1[mask0], y_interactive[mask0])
a1_int, b1_int = linear_fit(x1[mask1], y_interactive[mask1])

axes[1].plot(x_line, a0_int + b0_int * x_line,
            'b-', linewidth=3, label=f'Slope₀ = {b0_int:.2f}')
axes[1].plot(x_line, a1_int + b1_int * x_line,
            'orange', linewidth=3, label=f'Slope₁ = {b1_int:.2f}')

axes[1].set_xlabel('x₁', fontsize=12, fontweight='bold')
axes[1].set_ylabel('y', fontsize=12, fontweight='bold')
axes[1].set_title('INTERACTIVE MODEL\n' +
                 'y = α + β₁x₁ + β₂x₂ + β₃(x₁×x₂)\n' +
                 'Different slopes!',
                 fontsize=14, fontweight='bold', color='red')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('interaction_demo.png', dpi=300, bbox_inches='tight', facecolor='white')
print(f"  ✓ Saved: interaction_demo.png")
print(f"\nADDITIVE MODEL:")
print(f"  Control slope: {b0:.2f}")
print(f"  Treatment slope: {b1:.2f}")
print(f"  → Same slopes (parallel lines)")

print(f"\nINTERACTIVE MODEL:")
print(f"  Control slope: {b0_int:.2f}")
print(f"  Treatment slope: {b1_int:.2f}")
print(f"  → Different slopes!")
plt.close()

print("\n✅ Image generated successfully!")
