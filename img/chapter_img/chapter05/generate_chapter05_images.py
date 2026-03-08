#!/usr/bin/env python3
"""
Generate images for Chapter 05 - Multivariate Regression

Bài học:
- 5.1: Multiple Predictors
- 5.2: Confounding and DAGs
- 5.3: Multicollinearity
- 5.4: Interaction Effects

Hình ảnh:
1. multiple_predictors_visualization.png - 3D visualization
2. confounding_dags.png - DAG examples và Simpson's paradox
3. multicollinearity_effects.png - Correlation và VIF
4. interaction_effects.png - Interaction visualization

Tác giả: Nguyen Le Linh
Ngày: 11/01/2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# Seed
np.random.seed(42)

print("="*70)
print("GENERATING IMAGES FOR CHAPTER 05 - MULTIVARIATE REGRESSION")
print("="*70)

# ============================================================================
# IMAGE 1: Multiple Predictors Visualization
# ============================================================================
print("\n1. Generating multiple_predictors_visualization.png...")

# Generate data
n = 100
true_alpha = 50
true_beta_height = 0.5
true_beta_age = 0.3
true_sigma = 3

height = np.random.uniform(150, 190, n)
age = np.random.uniform(20, 60, n)
weight = true_alpha + true_beta_height * height + true_beta_age * age + np.random.normal(0, true_sigma, n)

fig = plt.figure(figsize=(18, 6))

# 1. Weight vs Height (colored by age)
ax1 = fig.add_subplot(131)
scatter1 = ax1.scatter(height, weight, s=50, alpha=0.6, c=age, cmap='viridis',
                       edgecolors='black')
ax1.set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
ax1.set_title('Weight vs Height\n(Color = Age)', fontsize=14, fontweight='bold')
ax1.grid(alpha=0.3)
cbar1 = plt.colorbar(scatter1, ax=ax1)
cbar1.set_label('Age (years)', fontsize=11)

# 2. Weight vs Age (colored by height)
ax2 = fig.add_subplot(132)
scatter2 = ax2.scatter(age, weight, s=50, alpha=0.6, c=height, cmap='plasma',
                       edgecolors='black')
ax2.set_xlabel('Age (years)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
ax2.set_title('Weight vs Age\n(Color = Height)', fontsize=14, fontweight='bold')
ax2.grid(alpha=0.3)
cbar2 = plt.colorbar(scatter2, ax=ax2)
cbar2.set_label('Height (cm)', fontsize=11)

# 3. 3D visualization
ax3 = fig.add_subplot(133, projection='3d')
ax3.scatter(height, age, weight, s=30, alpha=0.6, c=weight, cmap='coolwarm',
           edgecolors='black')
ax3.set_xlabel('Height (cm)', fontsize=11, fontweight='bold')
ax3.set_ylabel('Age (years)', fontsize=11, fontweight='bold')
ax3.set_zlabel('Weight (kg)', fontsize=11, fontweight='bold')
ax3.set_title('3D: Weight vs Height & Age', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('multiple_predictors_visualization.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: multiple_predictors_visualization.png")

# ============================================================================
# IMAGE 2: Confounding and DAGs
# ============================================================================
print("\n2. Generating confounding_dags.png...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. DAG: Confounding
axes[0, 0].axis('off')
dag_confounding = """
╔═══════════════════════════════════════════════════════════╗
║              CONFOUNDING - DAG                            ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║                    Confounder (Z)                         ║
║                      /         \\                          ║
║                     /           \\                         ║
║                    ↓             ↓                        ║
║              Treatment (X)  →  Outcome (Y)                ║
║                                                           ║
║  Ví dụ:                                                   ║
║    Z = Socioeconomic Status                               ║
║    X = Education                                          ║
║    Y = Income                                             ║
║                                                           ║
║  Vấn đề:                                                  ║
║    • Z ảnh hưởng cả X và Y                                ║
║    • Nếu không control Z → bias estimate của X→Y          ║
║                                                           ║
║  Giải pháp:                                               ║
║    • Include Z trong model                                ║
║    • Y ~ X + Z (multiple regression)                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
axes[0, 0].text(0.5, 0.5, dag_confounding, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

# 2. Simpson's Paradox
np.random.seed(123)
n_group = 50

# Group A
x_a = np.random.uniform(0, 5, n_group)
y_a = 10 - 0.5 * x_a + np.random.normal(0, 0.5, n_group)

# Group B
x_b = np.random.uniform(5, 10, n_group)
y_b = 12 - 0.5 * x_b + np.random.normal(0, 0.5, n_group)

# Combined
x_all = np.concatenate([x_a, x_b])
y_all = np.concatenate([y_a, y_b])

axes[0, 1].scatter(x_a, y_a, s=60, alpha=0.7, color='blue', edgecolors='black', label='Group A')
axes[0, 1].scatter(x_b, y_b, s=60, alpha=0.7, color='red', edgecolors='black', label='Group B')

# Within-group trends (negative)
slope_a, intercept_a = np.polyfit(x_a, y_a, 1)
slope_b, intercept_b = np.polyfit(x_b, y_b, 1)
axes[0, 1].plot(x_a, intercept_a + slope_a * x_a, 'b--', linewidth=2, alpha=0.7)
axes[0, 1].plot(x_b, intercept_b + slope_b * x_b, 'r--', linewidth=2, alpha=0.7)

# Overall trend (positive!)
slope_all, intercept_all = np.polyfit(x_all, y_all, 1)
x_range = np.linspace(0, 10, 100)
axes[0, 1].plot(x_range, intercept_all + slope_all * x_range, 'k-', linewidth=3,
               label=f'Overall (slope={slope_all:.2f})')

axes[0, 1].set_xlabel('X', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Y', fontsize=12, fontweight='bold')
axes[0, 1].set_title("Simpson's Paradox\nWithin-group: negative, Overall: positive!",
                     fontsize=14, fontweight='bold')
axes[0, 1].legend(fontsize=10)
axes[0, 1].grid(alpha=0.3)

# 3. Collider Bias
axes[1, 0].axis('off')
dag_collider = """
╔═══════════════════════════════════════════════════════════╗
║              COLLIDER BIAS - DAG                          ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║              X  →  Collider (Z)  ←  Y                     ║
║                                                           ║
║  Ví dụ:                                                   ║
║    X = Talent                                             ║
║    Y = Beauty                                             ║
║    Z = Hollywood Star (collider)                          ║
║                                                           ║
║  Vấn đề:                                                  ║
║    • Nếu control Z → tạo ra spurious correlation X-Y      ║
║    • Trong Hollywood: talent ↔ beauty (negative!)         ║
║    • Nhưng trong population: independent                  ║
║                                                           ║
║  Giải pháp:                                               ║
║    • KHÔNG control collider                               ║
║    • Y ~ X (không include Z)                              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
axes[1, 0].text(0.5, 0.5, dag_collider, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.9))

# 4. Mediation
axes[1, 1].axis('off')
dag_mediation = """
╔═══════════════════════════════════════════════════════════╗
║              MEDIATION - DAG                              ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║              X  →  Mediator (M)  →  Y                     ║
║                                                           ║
║  Ví dụ:                                                   ║
║    X = Exercise                                           ║
║    M = Fitness                                            ║
║    Y = Health                                             ║
║                                                           ║
║  Effects:                                                 ║
║    • Total effect: X → Y                                  ║
║    • Direct effect: X → Y (controlling M)                 ║
║    • Indirect effect: X → M → Y                           ║
║                                                           ║
║  Câu hỏi:                                                 ║
║    • Control M hay không?                                 ║
║    • Phụ thuộc research question!                         ║
║      - Total effect: không control M                      ║
║      - Direct effect: control M                           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
axes[1, 1].text(0.5, 0.5, dag_mediation, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9))

plt.suptitle('Confounding, DAGs, and Causal Inference', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('confounding_dags.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: confounding_dags.png")

# ============================================================================
# IMAGE 3: Multicollinearity Effects
# ============================================================================
print("\n3. Generating multicollinearity_effects.png...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Generate correlated predictors
n = 100
x1 = np.random.normal(0, 1, n)

# Low correlation
x2_low = x1 * 0.2 + np.random.normal(0, 1, n) * 0.98
corr_low = np.corrcoef(x1, x2_low)[0, 1]

# High correlation (multicollinearity!)
x2_high = x1 * 0.95 + np.random.normal(0, 1, n) * 0.31
corr_high = np.corrcoef(x1, x2_high)[0, 1]

# 1. Low correlation
axes[0, 0].scatter(x1, x2_low, s=50, alpha=0.6, edgecolors='black', color='green')
axes[0, 0].set_xlabel('X₁', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('X₂', fontsize=12, fontweight='bold')
axes[0, 0].set_title(f'Low Correlation\nr = {corr_low:.2f} ✓',
                     fontsize=14, fontweight='bold', color='green')
axes[0, 0].grid(alpha=0.3)

# 2. High correlation
axes[0, 1].scatter(x1, x2_high, s=50, alpha=0.6, edgecolors='black', color='red')
axes[0, 1].set_xlabel('X₁', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('X₂', fontsize=12, fontweight='bold')
axes[0, 1].set_title(f'High Correlation (Multicollinearity!)\nr = {corr_high:.2f} ✗',
                     fontsize=14, fontweight='bold', color='red')
axes[0, 1].grid(alpha=0.3)

# 3. Effect on posterior uncertainty
beta1_low = np.random.normal(0.5, 0.1, 10000)
beta2_low = np.random.normal(0.3, 0.1, 10000)

beta1_high = np.random.normal(0.5, 0.3, 10000)
beta2_high = 0.8 - beta1_high + np.random.normal(0, 0.05, 10000)

axes[1, 0].scatter(beta1_low, beta2_low, s=1, alpha=0.3, color='green')
axes[1, 0].set_xlabel('β₁', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('β₂', fontsize=12, fontweight='bold')
axes[1, 0].set_title('Posterior: Low Correlation\nNarrow, Independent ✓',
                     fontsize=14, fontweight='bold', color='green')
axes[1, 0].grid(alpha=0.3)

axes[1, 1].scatter(beta1_high, beta2_high, s=1, alpha=0.3, color='red')
axes[1, 1].set_xlabel('β₁', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('β₂', fontsize=12, fontweight='bold')
axes[1, 1].set_title('Posterior: High Correlation\nWide, Negatively Correlated ✗',
                     fontsize=14, fontweight='bold', color='red')
axes[1, 1].grid(alpha=0.3)

plt.suptitle('Multicollinearity Effects on Posterior', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('multicollinearity_effects.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: multicollinearity_effects.png")

# ============================================================================
# IMAGE 4: Interaction Effects
# ============================================================================
print("\n4. Generating interaction_effects.png...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Generate data with interaction
x = np.linspace(0, 10, 50)
group_a = 2 + 0.5 * x + np.random.normal(0, 0.5, 50)
group_b = 1 + 1.5 * x + np.random.normal(0, 0.5, 50)

# 1. No interaction (parallel lines)
axes[0, 0].scatter(x, group_a, s=50, alpha=0.6, color='blue', edgecolors='black', label='Group A')
axes[0, 0].plot(x, 2 + 0.5 * x, 'b-', linewidth=3)
axes[0, 0].scatter(x, group_b, s=50, alpha=0.6, color='red', edgecolors='black', label='Group B')
axes[0, 0].plot(x, 3 + 0.5 * x, 'r-', linewidth=3)
axes[0, 0].set_xlabel('X', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Y', fontsize=12, fontweight='bold')
axes[0, 0].set_title('No Interaction\nParallel slopes (same effect)',
                     fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(alpha=0.3)

# 2. With interaction (different slopes)
axes[0, 1].scatter(x, group_a, s=50, alpha=0.6, color='blue', edgecolors='black', label='Group A')
axes[0, 1].plot(x, 2 + 0.5 * x, 'b-', linewidth=3, label='Slope = 0.5')
axes[0, 1].scatter(x, group_b, s=50, alpha=0.6, color='red', edgecolors='black', label='Group B')
axes[0, 1].plot(x, 1 + 1.5 * x, 'r-', linewidth=3, label='Slope = 1.5')
axes[0, 1].set_xlabel('X', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Y', fontsize=12, fontweight='bold')
axes[0, 1].set_title('With Interaction\nDifferent slopes (effect depends on group)',
                     fontsize=14, fontweight='bold')
axes[0, 1].legend(fontsize=10)
axes[0, 1].grid(alpha=0.3)

# 3. Model comparison
axes[1, 0].axis('off')
model_comparison = """
╔═══════════════════════════════════════════════════════════╗
║           MODEL COMPARISON                                ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Model 1: No Interaction                                  ║
║    Y = β₀ + β₁·X + β₂·Group                               ║
║                                                           ║
║    • β₁: Effect của X (same for both groups)              ║
║    • β₂: Difference between groups                        ║
║    • Parallel lines                                       ║
║                                                           ║
║  Model 2: With Interaction                                ║
║    Y = β₀ + β₁·X + β₂·Group + β₃·(X × Group)              ║
║                                                           ║
║    • β₁: Effect của X trong Group A                       ║
║    • β₃: Difference in slopes                             ║
║    • Non-parallel lines                                   ║
║                                                           ║
║  Interpretation:                                          ║
║    • β₃ = 0: No interaction                               ║
║    • β₃ ≠ 0: Effect của X phụ thuộc Group                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
axes[1, 0].text(0.5, 0.5, model_comparison, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))

# 4. Continuous interaction
x_cont = np.linspace(0, 10, 100)
z_values = [0, 5, 10]
colors = ['blue', 'green', 'red']

for z, color in zip(z_values, colors):
    y_cont = 1 + 0.5 * x_cont + 0.1 * z * x_cont
    axes[1, 1].plot(x_cont, y_cont, linewidth=3, color=color, label=f'Z = {z}')

axes[1, 1].set_xlabel('X', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Y', fontsize=12, fontweight='bold')
axes[1, 1].set_title('Continuous Interaction\nY = β₀ + β₁·X + β₂·Z + β₃·(X×Z)',
                     fontsize=14, fontweight='bold')
axes[1, 1].legend(fontsize=10)
axes[1, 1].grid(alpha=0.3)

plt.suptitle('Interaction Effects', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('interaction_effects.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: interaction_effects.png")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*70)
print("✓ CHAPTER 05 IMAGES GENERATED SUCCESSFULLY!")
print("="*70)
print("\nGenerated images:")
print("  1. multiple_predictors_visualization.png")
print("  2. confounding_dags.png")
print("  3. multicollinearity_effects.png")
print("  4. interaction_effects.png")
print("\nTotal: 4 images")
print("Location: img/chapter_img/chapter05/")
print("="*70)
