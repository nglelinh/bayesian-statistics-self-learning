#!/usr/bin/env python3
"""
Generate images for Chapter 06 - Generalized Linear Models (GLM)

Bài học:
- 6.1: Logistic Regression
- 6.2: Poisson Regression
- 6.3: Model Evaluation

Hình ảnh:
1. logistic_regression_basics.png - Logit link, probability curve
2. poisson_regression_basics.png - Count data, log link
3. link_functions_comparison.png - Identity, Logit, Log links
4. model_evaluation_glm.png - ROC, Confusion matrix, Residuals

Tác giả: Nguyen Le Linh
Ngày: 11/01/2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import expit  # logistic function
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# Seed
np.random.seed(42)

print("="*70)
print("GENERATING IMAGES FOR CHAPTER 06 - GLM")
print("="*70)

# ============================================================================
# IMAGE 1: Logistic Regression Basics
# ============================================================================
print("\n1. Generating logistic_regression_basics.png...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Logistic function
x = np.linspace(-6, 6, 1000)
y_logistic = expit(x)  # 1 / (1 + exp(-x))

axes[0, 0].plot(x, y_logistic, linewidth=3, color='blue')
axes[0, 0].axhline(0.5, color='red', linestyle='--', linewidth=2, alpha=0.5)
axes[0, 0].axvline(0, color='red', linestyle='--', linewidth=2, alpha=0.5)
axes[0, 0].fill_between(x, 0, y_logistic, alpha=0.2, color='blue')
axes[0, 0].set_xlabel('Linear Predictor (β₀ + β₁·x)', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Probability P(y=1)', fontsize=12, fontweight='bold')
axes[0, 0].set_title('Logistic Function\nP(y=1) = 1 / (1 + exp(-(β₀ + β₁·x)))',
                     fontsize=14, fontweight='bold')
axes[0, 0].set_ylim(-0.05, 1.05)
axes[0, 0].grid(alpha=0.3)

# 2. Data example
n = 200
x_data = np.random.uniform(-3, 3, n)
prob_true = expit(0.5 + 1.5 * x_data)
y_data = np.random.binomial(1, prob_true)

axes[0, 1].scatter(x_data[y_data==0], y_data[y_data==0], s=50, alpha=0.5, 
                   color='red', edgecolors='black', label='y=0 (Failure)')
axes[0, 1].scatter(x_data[y_data==1], y_data[y_data==1], s=50, alpha=0.5,
                   color='green', edgecolors='black', label='y=1 (Success)')

x_range = np.linspace(-3, 3, 100)
prob_pred = expit(0.5 + 1.5 * x_range)
axes[0, 1].plot(x_range, prob_pred, 'b-', linewidth=3, label='P(y=1|x)')

axes[0, 1].set_xlabel('Predictor (x)', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Outcome (y) / Probability', fontsize=12, fontweight='bold')
axes[0, 1].set_title('Logistic Regression Example\nBinary outcome with probability curve',
                     fontsize=14, fontweight='bold')
axes[0, 1].legend(fontsize=10)
axes[0, 1].grid(alpha=0.3)

# 3. Interpretation
axes[1, 0].axis('off')
interpretation = """
╔═══════════════════════════════════════════════════════════╗
║           LOGISTIC REGRESSION                             ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Model:                                                   ║
║    logit(p) = log(p/(1-p)) = β₀ + β₁·x                    ║
║    p = P(y=1|x) = 1 / (1 + exp(-(β₀ + β₁·x)))             ║
║                                                           ║
║  Khi nào dùng:                                            ║
║    • Binary outcome (0/1, Yes/No, Success/Fail)           ║
║    • Probability bounded [0, 1]                           ║
║                                                           ║
║  Interpretation của β₁:                                   ║
║    • β₁ > 0: x tăng → P(y=1) tăng                         ║
║    • β₁ < 0: x tăng → P(y=1) giảm                         ║
║    • exp(β₁) = Odds Ratio                                 ║
║                                                           ║
║  Ví dụ:                                                   ║
║    • P(pass exam | study hours)                           ║
║    • P(disease | risk factors)                            ║
║    • P(click | ad features)                               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
axes[1, 0].text(0.5, 0.5, interpretation, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))

# 4. Odds ratio
beta_values = np.linspace(-2, 2, 100)
odds_ratios = np.exp(beta_values)

axes[1, 1].plot(beta_values, odds_ratios, linewidth=3, color='purple')
axes[1, 1].axhline(1, color='red', linestyle='--', linewidth=2, alpha=0.5, label='OR=1 (no effect)')
axes[1, 1].axvline(0, color='red', linestyle='--', linewidth=2, alpha=0.5)
axes[1, 1].fill_between(beta_values, 1, odds_ratios, where=(beta_values>0), 
                        alpha=0.2, color='green', label='Increased odds')
axes[1, 1].fill_between(beta_values, 1, odds_ratios, where=(beta_values<0),
                        alpha=0.2, color='red', label='Decreased odds')
axes[1, 1].set_xlabel('Coefficient (β)', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Odds Ratio (exp(β))', fontsize=12, fontweight='bold')
axes[1, 1].set_title('Odds Ratio Interpretation\nOR = exp(β)',
                     fontsize=14, fontweight='bold')
axes[1, 1].legend(fontsize=10)
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('logistic_regression_basics.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: logistic_regression_basics.png")

# ============================================================================
# IMAGE 2: Poisson Regression Basics
# ============================================================================
print("\n2. Generating poisson_regression_basics.png...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Poisson distribution
lambdas = [1, 3, 5, 10]
colors = ['blue', 'green', 'orange', 'red']
x_pois = np.arange(0, 20)

for lam, color in zip(lambdas, colors):
    pmf = stats.poisson(lam).pmf(x_pois)
    axes[0, 0].plot(x_pois, pmf, 'o-', linewidth=2, markersize=6, 
                    color=color, label=f'λ = {lam}')

axes[0, 0].set_xlabel('Count (y)', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Probability', fontsize=12, fontweight='bold')
axes[0, 0].set_title('Poisson Distribution\nP(y|λ) = (λʸ·exp(-λ)) / y!',
                     fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(alpha=0.3, axis='y')

# 2. Log link
x_log = np.linspace(-2, 2, 100)
lambda_pred = np.exp(1 + 0.8 * x_log)

axes[0, 1].plot(x_log, lambda_pred, linewidth=3, color='blue')
axes[0, 1].fill_between(x_log, 0, lambda_pred, alpha=0.2, color='blue')
axes[0, 1].set_xlabel('Predictor (x)', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Expected Count (λ)', fontsize=12, fontweight='bold')
axes[0, 1].set_title('Log Link Function\nlog(λ) = β₀ + β₁·x  ⟹  λ = exp(β₀ + β₁·x)',
                     fontsize=14, fontweight='bold')
axes[0, 1].grid(alpha=0.3)

# 3. Data example
n = 100
x_count = np.random.uniform(0, 3, n)
lambda_true = np.exp(0.5 + 0.6 * x_count)
y_count = np.random.poisson(lambda_true)

axes[1, 0].scatter(x_count, y_count, s=50, alpha=0.6, edgecolors='black', color='steelblue')
x_range = np.linspace(0, 3, 100)
lambda_fit = np.exp(0.5 + 0.6 * x_range)
axes[1, 0].plot(x_range, lambda_fit, 'r-', linewidth=3, label='E[y|x] = exp(β₀ + β₁·x)')
axes[1, 0].set_xlabel('Predictor (x)', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Count (y)', fontsize=12, fontweight='bold')
axes[1, 0].set_title('Poisson Regression Example\nCount data with exponential mean',
                     fontsize=14, fontweight='bold')
axes[1, 0].legend(fontsize=10)
axes[1, 0].grid(alpha=0.3)

# 4. Interpretation
axes[1, 1].axis('off')
interpretation_poisson = """
╔═══════════════════════════════════════════════════════════╗
║           POISSON REGRESSION                              ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Model:                                                   ║
║    log(λ) = β₀ + β₁·x                                     ║
║    λ = E[y|x] = exp(β₀ + β₁·x)                            ║
║    y ~ Poisson(λ)                                         ║
║                                                           ║
║  Khi nào dùng:                                            ║
║    • Count data (0, 1, 2, 3, ...)                         ║
║    • Non-negative integers                                ║
║    • Rate/frequency data                                  ║
║                                                           ║
║  Interpretation của β₁:                                   ║
║    • exp(β₁) = Multiplicative effect on λ                 ║
║    • β₁ = 0.1 → 10% increase in λ per unit x              ║
║    • β₁ = -0.2 → 18% decrease in λ per unit x             ║
║                                                           ║
║  Ví dụ:                                                   ║
║    • Number of accidents per day                          ║
║    • Number of emails received                            ║
║    • Number of species in area                            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
axes[1, 1].text(0.5, 0.5, interpretation_poisson, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9))

plt.tight_layout()
plt.savefig('poisson_regression_basics.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: poisson_regression_basics.png")

# ============================================================================
# IMAGE 3: Link Functions Comparison
# ============================================================================
print("\n3. Generating link_functions_comparison.png...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

x_link = np.linspace(-3, 3, 1000)

# 1. Identity link (Linear regression)
y_identity = 2 + 1.5 * x_link
axes[0, 0].plot(x_link, y_identity, linewidth=3, color='blue')
axes[0, 0].set_xlabel('x', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('μ = E[y|x]', fontsize=12, fontweight='bold')
axes[0, 0].set_title('Identity Link (Linear Regression)\nμ = β₀ + β₁·x',
                     fontsize=14, fontweight='bold')
axes[0, 0].grid(alpha=0.3)
axes[0, 0].text(0.5, 0.95, 'Range: (-∞, +∞)', transform=axes[0, 0].transAxes,
               fontsize=11, ha='center', va='top',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# 2. Logit link (Logistic regression)
y_logit = expit(0.5 + 1.5 * x_link)
axes[0, 1].plot(x_link, y_logit, linewidth=3, color='green')
axes[0, 1].axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
axes[0, 1].axhline(1, color='red', linestyle='--', linewidth=1, alpha=0.5)
axes[0, 1].set_xlabel('x', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('p = P(y=1|x)', fontsize=12, fontweight='bold')
axes[0, 1].set_title('Logit Link (Logistic Regression)\nlogit(p) = β₀ + β₁·x',
                     fontsize=14, fontweight='bold')
axes[0, 1].set_ylim(-0.1, 1.1)
axes[0, 1].grid(alpha=0.3)
axes[0, 1].text(0.5, 0.95, 'Range: [0, 1]', transform=axes[0, 1].transAxes,
               fontsize=11, ha='center', va='top',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# 3. Log link (Poisson regression)
y_log = np.exp(0.5 + 0.5 * x_link)
axes[1, 0].plot(x_link, y_log, linewidth=3, color='orange')
axes[1, 0].axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
axes[1, 0].set_xlabel('x', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('λ = E[y|x]', fontsize=12, fontweight='bold')
axes[1, 0].set_title('Log Link (Poisson Regression)\nlog(λ) = β₀ + β₁·x',
                     fontsize=14, fontweight='bold')
axes[1, 0].set_ylim(-0.5, 10)
axes[1, 0].grid(alpha=0.3)
axes[1, 0].text(0.5, 0.95, 'Range: [0, +∞)', transform=axes[1, 0].transAxes,
               fontsize=11, ha='center', va='top',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# 4. Summary table
axes[1, 1].axis('off')
summary_table = """
╔═══════════════════════════════════════════════════════════╗
║           LINK FUNCTIONS SUMMARY                          ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Model           Link        Outcome      Range           ║
║  ─────────────────────────────────────────────────────    ║
║                                                           ║
║  Linear          Identity    Continuous   (-∞, +∞)        ║
║  Regression      μ = η                                    ║
║                                                           ║
║  Logistic        Logit       Binary       [0, 1]          ║
║  Regression      logit(p)=η  (0/1)                        ║
║                                                           ║
║  Poisson         Log         Count        [0, +∞)         ║
║  Regression      log(λ) = η  (0,1,2,...)                  ║
║                                                           ║
║  ─────────────────────────────────────────────────────    ║
║                                                           ║
║  Trong đó: η = β₀ + β₁·x₁ + β₂·x₂ + ...                   ║
║           (linear predictor)                              ║
║                                                           ║
║  Link function biến đổi outcome space                     ║
║  thành linear predictor space                             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
axes[1, 1].text(0.5, 0.5, summary_table, fontsize=9.5, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9))

plt.suptitle('Link Functions in GLM', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('link_functions_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: link_functions_comparison.png")

# ============================================================================
# IMAGE 4: Model Evaluation for GLM
# ============================================================================
print("\n4. Generating model_evaluation_glm.png...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. ROC Curve (for logistic regression)
fpr = np.linspace(0, 1, 100)
tpr_good = fpr ** 0.3  # Good model
tpr_random = fpr  # Random classifier

axes[0, 0].plot(fpr, tpr_good, linewidth=3, color='blue', label='Good Model (AUC=0.85)')
axes[0, 0].plot(fpr, tpr_random, 'r--', linewidth=2, label='Random (AUC=0.50)')
axes[0, 0].fill_between(fpr, fpr, tpr_good, alpha=0.2, color='blue')
axes[0, 0].set_xlabel('False Positive Rate', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('True Positive Rate', fontsize=12, fontweight='bold')
axes[0, 0].set_title('ROC Curve\nReceiver Operating Characteristic',
                     fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(alpha=0.3)
axes[0, 0].set_xlim(0, 1)
axes[0, 0].set_ylim(0, 1)

# 2. Confusion Matrix
confusion = np.array([[80, 20], [15, 85]])
sns.heatmap(confusion, annot=True, fmt='d', cmap='Blues', cbar=False,
           xticklabels=['Predicted 0', 'Predicted 1'],
           yticklabels=['Actual 0', 'Actual 1'],
           ax=axes[0, 1], annot_kws={'fontsize': 14, 'fontweight': 'bold'})
axes[0, 1].set_title('Confusion Matrix\nAccuracy = 82.5%',
                     fontsize=14, fontweight='bold')

# 3. Residuals for Poisson
x_res = np.random.uniform(0, 3, 100)
lambda_res = np.exp(0.5 + 0.6 * x_res)
y_res = np.random.poisson(lambda_res)
residuals = y_res - lambda_res

axes[1, 0].scatter(lambda_res, residuals, s=50, alpha=0.6, edgecolors='black', color='steelblue')
axes[1, 0].axhline(0, color='red', linestyle='--', linewidth=2)
axes[1, 0].set_xlabel('Fitted Values (λ)', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Residuals (y - λ)', fontsize=12, fontweight='bold')
axes[1, 0].set_title('Residual Plot (Poisson)\nCheck for patterns',
                     fontsize=14, fontweight='bold')
axes[1, 0].grid(alpha=0.3)

# 4. Evaluation metrics
axes[1, 1].axis('off')
metrics_text = """
╔═══════════════════════════════════════════════════════════╗
║           MODEL EVALUATION METRICS                        ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Logistic Regression:                                     ║
║    • Accuracy = (TP + TN) / Total                         ║
║    • Precision = TP / (TP + FP)                           ║
║    • Recall = TP / (TP + FN)                              ║
║    • F1 Score = 2·(Prec·Rec) / (Prec+Rec)                 ║
║    • AUC-ROC = Area Under ROC Curve                       ║
║                                                           ║
║  Poisson Regression:                                      ║
║    • Deviance = 2·Σ[y·log(y/λ) - (y-λ)]                   ║
║    • Pearson χ² = Σ[(y-λ)²/λ]                             ║
║    • Overdispersion check                                 ║
║                                                           ║
║  General:                                                 ║
║    • Posterior Predictive Checks                          ║
║    • LOO-CV (Leave-One-Out Cross-Validation)              ║
║    • WAIC (Widely Applicable IC)                          ║
║    • Residual plots                                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
axes[1, 1].text(0.5, 0.5, metrics_text, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.suptitle('Model Evaluation for GLM', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('model_evaluation_glm.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: model_evaluation_glm.png")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*70)
print("✓ CHAPTER 06 IMAGES GENERATED SUCCESSFULLY!")
print("="*70)
print("\nGenerated images:")
print("  1. logistic_regression_basics.png")
print("  2. poisson_regression_basics.png")
print("  3. link_functions_comparison.png")
print("  4. model_evaluation_glm.png")
print("\nTotal: 4 images")
print("Location: img/chapter_img/chapter06/")
print("="*70)
