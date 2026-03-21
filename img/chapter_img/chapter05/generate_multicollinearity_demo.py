#!/usr/bin/env python3
"""
Generate multicollinearity demonstration image
"""

import numpy as np
import matplotlib.pyplot as plt

# Set style
plt.style.use('default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

print("Generating multicollinearity_demo.png...")

# Generate correlated predictors
np.random.seed(42)
n = 100

x1 = np.random.normal(0, 1, n)
x2 = 0.95 * x1 + np.random.normal(0, 0.1, n)  # High correlation with x1

# Outcome depends on both
y = 2 + 3*x1 + 2*x2 + np.random.normal(0, 1, n)

# Visualize correlation
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. x1 vs x2 (high correlation)
axes[0].scatter(x1, x2, s=50, alpha=0.6, edgecolors='black')
corr = np.corrcoef(x1, x2)[0, 1]
axes[0].set_xlabel('x₁', fontsize=12, fontweight='bold')
axes[0].set_ylabel('x₂', fontsize=12, fontweight='bold')
axes[0].set_title(f'Predictors Correlation\nr = {corr:.3f} (HIGH!)',
                 fontsize=14, fontweight='bold', color='red')
axes[0].grid(alpha=0.3)

# 2. Both predict y well individually
axes[1].scatter(x1, y, s=50, alpha=0.6, label='x₁ vs y', edgecolors='black', color='blue')
axes[1].scatter(x2, y, s=50, alpha=0.6, label='x₂ vs y', edgecolors='black', color='orange')
axes[1].set_xlabel('Predictor', fontsize=12, fontweight='bold')
axes[1].set_ylabel('y', fontsize=12, fontweight='bold')
axes[1].set_title('Both Predictors Correlate with y\n' +
                 'Hard to separate their effects!',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

# 3. Problem illustration
axes[2].axis('off')
problem = """
╔═══════════════════════════════════════════════╗
║        MULTICOLLINEARITY PROBLEM              ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  Khi x₁ và x₂ correlate cao:                  ║
║                                               ║
║  Vấn đề:                                      ║
║    • Không thể tách biệt effects              ║
║    • Coefficients có high uncertainty         ║
║    • Interpretation khó khăn                  ║
║                                               ║
║  Tại sao?                                     ║
║    Khi x₁ tăng, x₂ cũng tăng                  ║
║    → Effect của x₁ hay x₂?                    ║
║    → Model không biết!                        ║
║                                               ║
║  Lưu ý:                                       ║
║    • Predictions vẫn tốt                      ║
║    • Chỉ interpretation bị ảnh hưởng          ║
║                                               ║
╚═══════════════════════════════════════════════╝
"""
axes[2].text(0.5, 0.5, problem, fontsize=10, family='monospace',
            ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.savefig('multicollinearity_demo.png', dpi=300, bbox_inches='tight', facecolor='white')
print(f"  ✓ Saved: multicollinearity_demo.png")
print(f"  Correlation: r = {corr:.3f}")
plt.close()

print("\n✅ Image generated successfully!")
