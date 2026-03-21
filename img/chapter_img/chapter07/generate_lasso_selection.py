#!/usr/bin/env python3
"""
Generate Lasso feature selection visualization
Shows Lasso with different alpha values for sparse feature selection
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Set font
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

# Set random seed
np.random.seed(42)

# Generate sparse data
n = 100
p = 20

X = np.random.randn(n, p)
true_coef = np.zeros(p)
true_coef[:5] = [2, -1.5, 3, -2, 1]  # Only first 5 non-zero
y = X @ true_coef + np.random.randn(n)

# Standardize
X_z = (X - X.mean(axis=0)) / X.std(axis=0)
y_z = (y - y.mean()) / y.std()

# Manual Lasso implementation using coordinate descent
def lasso_coordinate_descent(X, y, alpha, max_iter=1000, tol=1e-4):
    """Fit Lasso using coordinate descent"""
    n, p = X.shape
    coef = np.zeros(p)
    
    for iteration in range(max_iter):
        coef_old = coef.copy()
        
        for j in range(p):
            # Compute partial residual
            r_j = y - X @ coef + coef[j] * X[:, j]
            rho_j = X[:, j] @ r_j
            
            # Soft-thresholding
            if rho_j < -alpha:
                coef[j] = (rho_j + alpha) / (X[:, j] @ X[:, j])
            elif rho_j > alpha:
                coef[j] = (rho_j - alpha) / (X[:, j] @ X[:, j])
            else:
                coef[j] = 0
        
        # Check convergence
        if np.max(np.abs(coef - coef_old)) < tol:
            break
    
    return coef

# Lasso with different alphas
alphas = [0.001, 0.01, 0.1, 0.5]

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.ravel()

for idx, alpha in enumerate(alphas):
    coef = lasso_coordinate_descent(X_z, y_z, alpha)
    
    # Plot
    x_pos = np.arange(p)
    width = 0.35
    
    axes[idx].bar(x_pos - width/2, true_coef, width, alpha=0.5, 
                  label='True', edgecolor='black', color='blue')
    axes[idx].bar(x_pos + width/2, coef, width, alpha=0.7, 
                  label='Lasso', edgecolor='black', color='red')
    axes[idx].axhline(0, color='black', linestyle='--', linewidth=2, alpha=0.5)
    axes[idx].set_xlabel('Feature Index', fontsize=12, fontweight='bold')
    axes[idx].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
    
    n_selected = np.sum(np.abs(coef) > 0.01)
    axes[idx].set_title(f'Lasso: α = {alpha}\nNon-zero: {n_selected}/{p}',
                       fontsize=14, fontweight='bold')
    axes[idx].legend(fontsize=11)
    axes[idx].grid(alpha=0.3, axis='y')
    axes[idx].set_ylim(-3.5, 3.5)

plt.tight_layout()
plt.savefig('lasso_feature_selection.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Generated: lasso_feature_selection.png")

# Print summary
print("\nLASSO FEATURE SELECTION:")
for alpha in alphas:
    coef = lasso_coordinate_descent(X_z, y_z, alpha)
    n_selected = np.sum(np.abs(coef) > 0.01)
    print(f"  α = {alpha}: {n_selected} features selected")
print("\n→ Higher α → more sparsity (fewer features)")
