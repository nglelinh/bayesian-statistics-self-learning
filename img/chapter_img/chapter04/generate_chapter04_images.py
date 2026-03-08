#!/usr/bin/env python3
"""
Generate images for Chapter 04 - Linear Regression

Bài học:
- 4.1: Bayesian Linear Regression - Generative Model
- 4.2: Priors for Regression

Hình ảnh:
1. linear_regression_generative.png - Data-generating process
2. frequentist_vs_bayesian_regression.png - So sánh hai approaches
3. parameter_interpretation.png - Ý nghĩa α, β, σ
4. standardization_comparison.png - Raw vs Standardized data
5. prior_selection.png - Weakly informative priors
6. prior_predictive_check.png - Prior predictive distributions

Tác giả: Nguyen Le Linh
Ngày: 11/01/2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# Seed for reproducibility
np.random.seed(42)

print("="*70)
print("GENERATING IMAGES FOR CHAPTER 04 - LINEAR REGRESSION")
print("="*70)

# ============================================================================
# IMAGE 1: Linear Regression Generative Model
# ============================================================================
print("\n1. Generating linear_regression_generative.png...")

# True parameters
true_alpha = 50  # kg
true_beta = 0.7  # kg/cm
true_sigma = 5   # kg

# Generate data
n = 50
height = np.random.uniform(150, 190, n)
weight = true_alpha + true_beta * height + np.random.normal(0, true_sigma, n)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Data-generating process
axes[0, 0].scatter(height, weight, s=80, alpha=0.6, edgecolors='black', color='steelblue')
height_line = np.linspace(height.min(), height.max(), 100)
weight_line = true_alpha + true_beta * height_line
axes[0, 0].plot(height_line, weight_line, 'r-', linewidth=3, 
               label=f'True: y = {true_alpha:.1f} + {true_beta:.2f}x')

# Uncertainty bands
for i in [1, 2]:
    axes[0, 0].fill_between(height_line, 
                            weight_line - i*true_sigma,
                            weight_line + i*true_sigma,
                            alpha=0.15, color='red',
                            label=f'±{i}σ' if i == 1 else None)

axes[0, 0].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0, 0].set_title('Data-Generating Process\n' +
                     f'μ = {true_alpha} + {true_beta}·x, σ = {true_sigma}',
                     fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(alpha=0.3)

# 2. Generative story
axes[0, 1].axis('off')
story = f"""
╔═══════════════════════════════════════════════════════════╗
║           GENERATIVE STORY: HEIGHT → WEIGHT              ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Bước 1: Mối quan hệ tuyến tính                           ║
║    μᵢ = α + β·xᵢ                                          ║
║    α = {true_alpha:.1f} kg (intercept)                             ║
║    β = {true_beta:.2f} kg/cm (slope)                              ║
║                                                           ║
║  Bước 2: Mỗi người dao động xung quanh μᵢ                 ║
║    yᵢ ~ Normal(μᵢ, σ)                                     ║
║    σ = {true_sigma:.1f} kg (noise)                                ║
║                                                           ║
║  Ý nghĩa:                                                 ║
║    • Người cao 170cm: μ = {true_alpha + true_beta*170:.1f} kg                  ║
║    • Nhưng cân nặng thực tế dao động ±{true_sigma}kg              ║
║    • 68% trong [{true_alpha + true_beta*170 - true_sigma:.1f}, {true_alpha + true_beta*170 + true_sigma:.1f}]                    ║
║    • 95% trong [{true_alpha + true_beta*170 - 2*true_sigma:.1f}, {true_alpha + true_beta*170 + 2*true_sigma:.1f}]                    ║
║                                                           ║
║  Điều chúng ta KHÔNG biết:                                ║
║    → α, β, σ là UNKNOWN                                   ║
║    → Cần estimate từ data                                 ║
║    → Bayesian: Posterior distribution!                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
axes[0, 1].text(0.5, 0.5, story, fontsize=9.5, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9))

# 3. Distribution for specific x
x_example = 170
mu_example = true_alpha + true_beta * x_example
y_range = np.linspace(mu_example - 4*true_sigma, mu_example + 4*true_sigma, 1000)
y_pdf = stats.norm(mu_example, true_sigma).pdf(y_range)

axes[1, 0].plot(y_pdf, y_range, linewidth=3, color='blue')
axes[1, 0].fill_betweenx(y_range, 0, y_pdf, alpha=0.3, color='blue')
axes[1, 0].axhline(mu_example, color='red', linestyle='--', linewidth=2,
                   label=f'μ = {mu_example:.1f} kg')
axes[1, 0].axhline(mu_example - true_sigma, color='orange', linestyle=':', linewidth=2)
axes[1, 0].axhline(mu_example + true_sigma, color='orange', linestyle=':', linewidth=2,
                   label=f'μ ± σ')
axes[1, 0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Probability Density', fontsize=12, fontweight='bold')
axes[1, 0].set_title(f'Distribution of Weight\nfor Height = {x_example} cm',
                     fontsize=14, fontweight='bold')
axes[1, 0].legend(fontsize=10)
axes[1, 0].grid(alpha=0.3)

# 4. Residuals
residuals = weight - (true_alpha + true_beta * height)
axes[1, 1].hist(residuals, bins=15, density=True, alpha=0.7,
               color='skyblue', edgecolor='black', label='Observed Residuals')
x_resid = np.linspace(residuals.min(), residuals.max(), 1000)
axes[1, 1].plot(x_resid, stats.norm(0, true_sigma).pdf(x_resid),
               'r-', linewidth=3, label=f'Theoretical: N(0, {true_sigma})')
axes[1, 1].set_xlabel('Residual (kg)', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1, 1].set_title('Residuals Distribution\nShould be ~ Normal(0, σ)',
                     fontsize=14, fontweight='bold')
axes[1, 1].legend(fontsize=10)
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('linear_regression_generative.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: linear_regression_generative.png")

# ============================================================================
# IMAGE 2: Frequentist vs Bayesian Regression
# ============================================================================
print("\n2. Generating frequentist_vs_bayesian_regression.png...")

from scipy.stats import linregress
slope_freq, intercept_freq, r_value, p_value, std_err = linregress(height, weight)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Frequentist
axes[0].scatter(height, weight, s=80, alpha=0.6, edgecolors='black', color='steelblue')
axes[0].plot(height_line, intercept_freq + slope_freq * height_line,
            'r-', linewidth=3, label=f'OLS: y = {intercept_freq:.1f} + {slope_freq:.2f}x')
axes[0].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0].set_title('Frequentist: Point Estimate\n' +
                 f'R² = {r_value**2:.3f}, p < 0.001',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Bayesian
axes[1].scatter(height, weight, s=80, alpha=0.6, edgecolors='black',
               color='steelblue', label='Observed Data')
# Simulate posterior samples
n_samples = 100
alpha_samples = np.random.normal(intercept_freq, 5, n_samples)
beta_samples = np.random.normal(slope_freq, 0.05, n_samples)

for i in range(n_samples):
    axes[1].plot(height_line, alpha_samples[i] + beta_samples[i] * height_line,
                'b-', alpha=0.05, linewidth=1)

axes[1].plot(height_line, intercept_freq + slope_freq * height_line,
            'r-', linewidth=3, label='Posterior Mean')
axes[1].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[1].set_title('Bayesian: Uncertainty Quantification\nPosterior distribution of regression lines',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('frequentist_vs_bayesian_regression.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: frequentist_vs_bayesian_regression.png")

# ============================================================================
# IMAGE 3: Parameter Interpretation
# ============================================================================
print("\n3. Generating parameter_interpretation.png...")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. Intercept (α) with centering
x_centered = height - height.mean()
axes[0].scatter(x_centered, weight, s=80, alpha=0.6, edgecolors='black', color='steelblue')
axes[0].axvline(0, color='red', linestyle='--', linewidth=2, alpha=0.5)
axes[0].axhline(weight.mean(), color='red', linestyle='--', linewidth=2, alpha=0.5,
               label=f'α ≈ {weight.mean():.1f} kg (mean weight)')
axes[0].set_xlabel('Height - Mean Height (cm)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0].set_title('Intercept (α) after Centering\nα = mean weight at mean height',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=10)
axes[0].grid(alpha=0.3)

# 2. Slope (β)
axes[1].scatter(height, weight, s=80, alpha=0.6, edgecolors='black', color='steelblue')
x1, x2 = 170, 171
y1 = true_alpha + true_beta * x1
y2 = true_alpha + true_beta * x2
axes[1].plot([x1, x2], [y1, y1], 'r-', linewidth=2)
axes[1].plot([x2, x2], [y1, y2], 'r-', linewidth=2)
axes[1].annotate('', xy=(x2, y1), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
axes[1].annotate('', xy=(x2, y2), xytext=(x2, y1),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
axes[1].text(x1 + 0.5, y1 - 2, '+1 cm', fontsize=11, color='red', fontweight='bold')
axes[1].text(x2 + 0.5, (y1 + y2)/2, f'+{true_beta:.2f} kg', fontsize=11, 
            color='red', fontweight='bold')
axes[1].plot(height_line, true_alpha + true_beta * height_line, 'b-', linewidth=2)
axes[1].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[1].set_title(f'Slope (β) = {true_beta:.2f} kg/cm\nWeight increase per 1 cm height',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)

# 3. Noise (σ)
axes[2].scatter(height, weight, s=80, alpha=0.6, edgecolors='black', color='steelblue')
axes[2].plot(height_line, true_alpha + true_beta * height_line, 'r-', linewidth=3)
axes[2].fill_between(height_line,
                     true_alpha + true_beta * height_line - true_sigma,
                     true_alpha + true_beta * height_line + true_sigma,
                     alpha=0.3, color='red', label=f'μ ± σ ({true_sigma} kg)')
axes[2].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[2].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[2].set_title(f'Noise (σ) = {true_sigma:.1f} kg\nIndividual variability',
                 fontsize=14, fontweight='bold')
axes[2].legend(fontsize=10)
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('parameter_interpretation.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: parameter_interpretation.png")

# ============================================================================
# IMAGE 4: Standardization Comparison
# ============================================================================
print("\n4. Generating standardization_comparison.png...")

# Standardize
height_std = (height - height.mean()) / height.std()
weight_std = (weight - weight.mean()) / weight.std()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Raw data
axes[0].scatter(height, weight, s=80, alpha=0.6, edgecolors='black', color='steelblue')
axes[0].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0].set_title('Raw Data\n' +
                 f'Height: [{height.min():.0f}, {height.max():.0f}] cm\n' +
                 f'Weight: [{weight.min():.0f}, {weight.max():.0f}] kg',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)

# Standardized
axes[1].scatter(height_std, weight_std, s=80, alpha=0.6, edgecolors='black', color='green')
axes[1].axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
axes[1].axvline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
axes[1].set_xlabel('Height (standardized)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Weight (standardized)', fontsize=12, fontweight='bold')
axes[1].set_title('Standardized Data\nBoth: mean=0, SD=1',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('standardization_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: standardization_comparison.png")

# ============================================================================
# IMAGE 5: Prior Selection
# ============================================================================
print("\n5. Generating prior_selection.png...")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

theta_range = np.linspace(-6, 6, 1000)

# Priors for intercept
priors_alpha = [
    (stats.norm(0, 5), 'N(0, 5)', 'Too wide', 'red'),
    (stats.norm(0, 1), 'N(0, 1)', 'Weakly informative ✓', 'green'),
    (stats.norm(0, 0.1), 'N(0, 0.1)', 'Too narrow', 'orange')
]

for ax, (prior, label, title, color) in zip(axes[0], priors_alpha):
    pdf = prior.pdf(theta_range)
    ax.plot(theta_range, pdf, linewidth=3, color=color)
    ax.fill_between(theta_range, pdf, alpha=0.3, color=color)
    ax.set_xlabel('α', fontsize=12, fontweight='bold')
    ax.set_ylabel('Density', fontsize=12, fontweight='bold')
    ax.set_title(f'{title}\nα ~ {label}', fontsize=13, fontweight='bold')
    ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.grid(alpha=0.3)

# Priors for slope
for ax, (prior, label, title, color) in zip(axes[1], priors_alpha):
    pdf = prior.pdf(theta_range)
    ax.plot(theta_range, pdf, linewidth=3, color=color)
    ax.fill_between(theta_range, pdf, alpha=0.3, color=color)
    ax.set_xlabel('β', fontsize=12, fontweight='bold')
    ax.set_ylabel('Density', fontsize=12, fontweight='bold')
    ax.set_title(f'{title}\nβ ~ {label}', fontsize=13, fontweight='bold')
    ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.grid(alpha=0.3)

plt.suptitle('Prior Selection: Weakly Informative Priors', fontsize=16, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('prior_selection.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: prior_selection.png")

# ============================================================================
# IMAGE 6: Prior Predictive Check
# ============================================================================
print("\n6. Generating prior_predictive_check.png...")

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
axes[0].set_title('Prior Predictive: β ~ N(0, 1)\nWeakly informative ✓',
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
axes[1].set_title('Prior Predictive: β ~ N(0, 5)\nToo wide - slopes vô lý ✗',
                 fontsize=14, fontweight='bold', color='red')
axes[1].set_ylim(-6, 6)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('prior_predictive_check.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: prior_predictive_check.png")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*70)
print("✓ CHAPTER 04 IMAGES GENERATED SUCCESSFULLY!")
print("="*70)
print("\nGenerated images:")
print("  1. linear_regression_generative.png")
print("  2. frequentist_vs_bayesian_regression.png")
print("  3. parameter_interpretation.png")
print("  4. standardization_comparison.png")
print("  5. prior_selection.png")
print("  6. prior_predictive_check.png")
print("\nTotal: 6 images")
print("Location: img/chapter_img/chapter04/")
print("="*70)
