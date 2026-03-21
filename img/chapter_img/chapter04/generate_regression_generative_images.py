#!/usr/bin/env python3
"""
Generate images for Chapter 04.01: Bayesian Linear Regression - Generative Model
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

# Random seed for reproducibility
np.random.seed(42)

# True parameters
true_alpha = 50  # kg (intercept)
true_beta = 0.7  # kg/cm (slope)
true_sigma = 5   # kg (noise)

# Generate data
n = 50
height = np.random.uniform(150, 190, n)  # cm
weight = true_alpha + true_beta * height + np.random.normal(0, true_sigma, n)  # kg

height_line = np.linspace(height.min(), height.max(), 100)
weight_line = true_alpha + true_beta * height_line

print("Generating Chapter 04.01 images...")

# ============================================================================
# Image 1: Generative Story (4 panels)
# ============================================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Panel 1: Data-generating process
axes[0, 0].scatter(height, weight, s=80, alpha=0.6, edgecolors='black')
axes[0, 0].plot(height_line, weight_line, 'r-', linewidth=3, 
               label=f'True: y = {true_alpha:.1f} + {true_beta:.2f}x')

# Show uncertainty bands
for i in [1, 2]:
    axes[0, 0].fill_between(height_line, 
                            weight_line - i*true_sigma,
                            weight_line + i*true_sigma,
                            alpha=0.15, color='red')

axes[0, 0].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0, 0].set_title('Data-Generating Process\n' +
                     f'μ = {true_alpha} + {true_beta}·x, σ = {true_sigma}',
                     fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=11)
axes[0, 0].grid(alpha=0.3)

# Panel 2: Generative story text
axes[0, 1].axis('off')
mu_170 = true_alpha + true_beta * 170
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
║    • Người cao 170cm: μ = {mu_170:.1f} kg                  ║
║    • Nhưng cân nặng thực tế dao động ±{true_sigma}kg              ║
║    • 68% trong [{mu_170 - true_sigma:.1f}, {mu_170 + true_sigma:.1f}]                    ║
║    • 95% trong [{mu_170 - 2*true_sigma:.1f}, {mu_170 + 2*true_sigma:.1f}]                    ║
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

# Panel 3: Distribution of y for specific x
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
axes[1, 0].legend(fontsize=11)
axes[1, 0].grid(alpha=0.3)

# Panel 4: Residuals
residuals = weight - (true_alpha + true_beta * height)
axes[1, 1].hist(residuals, bins=15, density=True, alpha=0.7,
               color='skyblue', edgecolor='black', label='Observed Residuals')
x_resid = np.linspace(residuals.min(), residuals.max(), 1000)
axes[1, 1].plot(x_resid, stats.norm(0, true_sigma).pdf(x_resid),
               'r-', linewidth=3, label=f'Theoretical: N(0, {true_sigma})')
axes[1, 1].set_xlabel('Residual (kg)', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1, 1].set_title('Residuals Distribution\n' +
                     'Should be ~ Normal(0, σ)',
                     fontsize=14, fontweight='bold')
axes[1, 1].legend(fontsize=11)
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('regression_generative_story.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("✓ Saved: regression_generative_story.png")
plt.close()

# ============================================================================
# Image 2: Frequentist vs Bayesian Comparison
# ============================================================================
from scipy.stats import linregress

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Frequentist: Point estimate
slope_freq, intercept_freq, r_value, p_value, std_err = linregress(height, weight)

axes[0].scatter(height, weight, s=80, alpha=0.6, edgecolors='black')
axes[0].plot(height_line, intercept_freq + slope_freq * height_line,
            'r-', linewidth=3, label=f'OLS: y = {intercept_freq:.1f} + {slope_freq:.2f}x')
axes[0].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0].set_title('Frequentist: Point Estimate\n' +
                 f'R² = {r_value**2:.3f}, p < 0.001',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Bayesian: Uncertainty
axes[1].scatter(height, weight, s=80, alpha=0.6, edgecolors='black',
               label='Observed Data')
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
axes[1].set_title('Bayesian: Uncertainty Quantification\n' +
                 'Posterior distribution of regression lines',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('regression_frequentist_vs_bayesian.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✓ Saved: regression_frequentist_vs_bayesian.png")
plt.close()

# ============================================================================
# Image 3: Parameter Interpretation (3 panels)
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Panel 1: Intercept (α) after centering
x_centered = height - height.mean()
axes[0].scatter(x_centered, weight, s=80, alpha=0.6, edgecolors='black')
axes[0].axvline(0, color='red', linestyle='--', linewidth=2, alpha=0.5)
axes[0].axhline(weight.mean(), color='red', linestyle='--', linewidth=2, alpha=0.5,
               label=f'α ≈ {weight.mean():.1f} kg (mean weight)')
axes[0].set_xlabel('Height - Mean Height (cm)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0].set_title('Intercept (α) after Centering\n' +
                 'α = mean weight at mean height',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Panel 2: Slope (β)
axes[1].scatter(height, weight, s=80, alpha=0.6, edgecolors='black')
# Draw slope interpretation
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
axes[1].set_title(f'Slope (β) = {true_beta:.2f} kg/cm\n' +
                 'Weight increase per 1 cm height',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)

# Panel 3: Noise (σ)
axes[2].scatter(height, weight, s=80, alpha=0.6, edgecolors='black')
axes[2].plot(height_line, true_alpha + true_beta * height_line, 'r-', linewidth=3)
axes[2].fill_between(height_line,
                     true_alpha + true_beta * height_line - true_sigma,
                     true_alpha + true_beta * height_line + true_sigma,
                     alpha=0.3, color='red', label=f'μ ± σ ({true_sigma} kg)')
axes[2].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[2].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[2].set_title(f'Noise (σ) = {true_sigma:.1f} kg\n' +
                 'Individual variability',
                 fontsize=14, fontweight='bold')
axes[2].legend(fontsize=11)
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('regression_parameter_interpretation.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✓ Saved: regression_parameter_interpretation.png")
plt.close()

print("\n" + "="*70)
print("COMPLETE: All Chapter 04.01 images generated successfully!")
print("="*70)
print(f"\nGenerated 3 images:")
print("  1. regression_generative_story.png - 4-panel generative model explanation")
print("  2. regression_frequentist_vs_bayesian.png - Comparison of approaches")
print("  3. regression_parameter_interpretation.png - α, β, σ interpretation")
