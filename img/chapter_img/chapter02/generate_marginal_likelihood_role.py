"""
Generate illustration for marginal likelihood P(D) role in Bayesian inference
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Vai trò của P(D) trong Bayesian Inference', fontsize=16, fontweight='bold', y=0.98)

# ==========================================
# Panel 1: Two different priors
# ==========================================
ax = axes[0, 0]

theta_grid = np.linspace(0, 1, 500)

# Prior 1: Beta(20, 80) - strong belief around 0.2
prior1 = stats.beta.pdf(theta_grid, 20, 80)

# Prior 2: Beta(5, 5) - weak belief around 0.5  
prior2 = stats.beta.pdf(theta_grid, 5, 5)

ax.plot(theta_grid, prior1, 'b-', linewidth=2.5, label='Prior 1: Beta(20, 80)\ntin mạnh θ ≈ 0.2')
ax.plot(theta_grid, prior2, 'g-', linewidth=2.5, label='Prior 2: Beta(5, 5)\ntin yếu θ ≈ 0.5')
ax.axvline(0.3, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Dữ liệu thực: 15/50 = 0.3')

ax.set_xlabel('θ')
ax.set_ylabel('Mật độ')
ax.set_title('(a) Hai prior khác nhau', fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3)

# ==========================================
# Panel 2: Likelihood for observed data
# ==========================================
ax = axes[0, 1]

# Data: 15 successes out of 50 trials
n_obs = 50
k_obs = 15

# Likelihood: Binomial(15 | 50, theta)
likelihood = stats.binom.pmf(k_obs, n_obs, theta_grid)
# Normalize for visualization
likelihood_normalized = likelihood / likelihood.max()

ax.plot(theta_grid, likelihood_normalized, 'orange', linewidth=3, label=f'Likelihood\nBinom(k={k_obs} | n={n_obs}, θ)')
ax.axvline(k_obs/n_obs, color='red', linestyle='--', linewidth=2, alpha=0.7, label=f'MLE = {k_obs/n_obs}')

ax.set_xlabel('θ')
ax.set_ylabel('Likelihood (chuẩn hóa)')
ax.set_title('(b) Likelihood từ dữ liệu quan sát', fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3)

# ==========================================
# Panel 3: Marginal likelihood calculation
# ==========================================
ax = axes[1, 0]

# Calculate P(D|M) for each prior (using Beta-Binomial conjugacy)
# P(D|M) = Beta(k+a, n-k+b) / Beta(a,b) * Binomial coefficient
from scipy.special import beta as beta_func

def marginal_likelihood_beta_binomial(k, n, a, b):
    """Marginal likelihood for Beta-Binomial model"""
    from scipy.special import comb
    return comb(n, k) * beta_func(k+a, n-k+b) / beta_func(a, b)

ml1 = marginal_likelihood_beta_binomial(k_obs, n_obs, 20, 80)
ml2 = marginal_likelihood_beta_binomial(k_obs, n_obs, 5, 5)

bayes_factor = ml1 / ml2

# Visualize as bar chart
models = ['Prior 1\nBeta(20,80)', 'Prior 2\nBeta(5,5)']
ml_values = [ml1, ml2]
colors = ['blue', 'green']

bars = ax.bar(models, ml_values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, ml_values)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'P(D|M) = {val:.6f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Marginal Likelihood P(D)', fontsize=12)
ax.set_title(f'(c) P(D) đo prior giải thích dữ liệu tốt cỡ nào\nBayes Factor = {bayes_factor:.2f}', 
             fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# Add text box with interpretation
textstr = f'Prior 1 giải thích dữ liệu\ntốt hơn Prior 2\n{bayes_factor:.1f} lần'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.5, 0.7, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', bbox=props, ha='center')

# ==========================================
# Panel 4: Role summary diagram
# ==========================================
ax = axes[1, 1]
ax.axis('off')

# Create a text summary with colors
summary_text = """
VAI TRÒ CỦA P(D) - MARGINAL LIKELIHOOD

1️⃣  CHUẨN HÓA POSTERIOR
   P(θ|D) = P(D|θ)P(θ) / P(D)
   
   → Đảm bảo ∫ P(θ|D) dθ = 1
   
   
2️⃣  ĐO PRIOR GIẢI THÍCH DATA
   P(D) = ∫ P(D|θ)P(θ) dθ
   
   • P(D) cao → prior "dự đoán đúng"
   • P(D) thấp → prior không phù hợp
   
   
3️⃣  SO SÁNH MÔ HÌNH
   Bayes Factor = P(D|M₁) / P(D|M₂)
   
   → Tự động cân bằng fit và complexity
   
   
4️⃣  CẬP NHẬT MIXTURE WEIGHTS
   w̃ₖ = wₖ · P(D|Mₖ) / Σⱼ wⱼ·P(D|Mⱼ)
   
   → Data "chọn" component phù hợp
"""

ax.text(0.05, 0.95, summary_text, transform=ax.transAxes,
        fontsize=12, verticalalignment='top', family='monospace',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3, pad=1))

# Add formulas in box at bottom
formula_text = "P(D) = ∫ P(D|θ)P(θ) dθ"
ax.text(0.5, 0.05, formula_text, transform=ax.transAxes,
        fontsize=14, ha='center', va='bottom', fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5, pad=0.5))

plt.tight_layout()
plt.savefig('marginal_likelihood_role.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("Generated: marginal_likelihood_role.png")
plt.show()
