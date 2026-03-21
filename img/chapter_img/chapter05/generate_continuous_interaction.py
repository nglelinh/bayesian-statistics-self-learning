#!/usr/bin/env python3
"""
Generate continuous × continuous interaction visualization
Replaces code block at line 240 in 05_04_interaction_effects.md
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# Generate data
np.random.seed(42)
n = 200

x1_cont = np.random.uniform(0, 10, n)
x2_cont = np.random.uniform(0, 10, n)
y_cont = 2 + 0.5*x1_cont + 0.3*x2_cont + 0.1*(x1_cont*x2_cont) + np.random.normal(0, 2, n)

# Create figure
fig = plt.figure(figsize=(14, 6))

# Left panel: 3D scatter
ax1 = fig.add_subplot(121, projection='3d')
scatter = ax1.scatter(x1_cont, x2_cont, y_cont, c=y_cont, cmap='viridis',
                      s=30, alpha=0.6, edgecolors='black', linewidth=0.5)
ax1.set_xlabel('x₁', fontsize=11, fontweight='bold', labelpad=8)
ax1.set_ylabel('x₂', fontsize=11, fontweight='bold', labelpad=8)
ax1.set_zlabel('y', fontsize=11, fontweight='bold', labelpad=8)
ax1.set_title('Continuous × Continuous Interaction\n' +
             'y = α + β₁x₁ + β₂x₂ + β₃(x₁×x₂)',
             fontsize=13, fontweight='bold', pad=15)
ax1.view_init(elev=20, azim=45)
fig.colorbar(scatter, ax=ax1, shrink=0.5, aspect=10, pad=0.1)

# Right panel: Contour plot
ax2 = fig.add_subplot(122)
contour = ax2.tricontourf(x1_cont, x2_cont, y_cont, levels=15, cmap='viridis')
ax2.scatter(x1_cont, x2_cont, c='white', s=10, alpha=0.3, edgecolors='black', linewidth=0.3)
ax2.set_xlabel('x₁', fontsize=11, fontweight='bold')
ax2.set_ylabel('x₂', fontsize=11, fontweight='bold')
ax2.set_title('Contour Plot\nEffect depends on both x₁ and x₂',
             fontsize=13, fontweight='bold')
plt.colorbar(contour, ax=ax2, label='y')
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('continuous_interaction.png', dpi=300, bbox_inches='tight',
            facecolor='white')
print("✓ Generated: continuous_interaction.png")
print(f"  - Number of observations: {n}")
print(f"  - x₁ range: [{x1_cont.min():.1f}, {x1_cont.max():.1f}]")
print(f"  - x₂ range: [{x2_cont.min():.1f}, {x2_cont.max():.1f}]")
print(f"  - y range: [{y_cont.min():.1f}, {y_cont.max():.1f}]")
print(f"  - True parameters: α=2, β₁=0.5, β₂=0.3, β₃=0.1")

plt.close()
