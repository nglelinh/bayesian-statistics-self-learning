#!/usr/bin/env python3
"""
Generate Lasso cross-validation and regularization path visualization
Shows optimal alpha selection via CV and coefficient paths
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

# Generate sparse data (same as before)
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

# Simple cross-validation
def cross_validate_lasso(X, y, alphas, k=5):
    """Simple k-fold CV for Lasso"""
    n = X.shape[0]
    fold_size = n // k
    cv_errors = []
    
    for alpha in alphas:
        fold_errors = []
        for fold in range(k):
            # Split data
            test_idx = range(fold * fold_size, min((fold + 1) * fold_size, n))
            train_idx = [i for i in range(n) if i not in test_idx]
            
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Fit and predict
            coef = lasso_coordinate_descent(X_train, y_train, alpha)
            y_pred = X_test @ coef
            mse = np.mean((y_test - y_pred)**2)
            fold_errors.append(mse)
        
        cv_errors.append(np.mean(fold_errors))
    
    return np.array(cv_errors)

# Test range of alphas
alphas_path = np.logspace(-3, 0, 30)
cv_errors = cross_validate_lasso(X_z, y_z, alphas_path)
optimal_idx = np.argmin(cv_errors)
optimal_alpha = alphas_path[optimal_idx]

# Get coefficients for optimal alpha
optimal_coef = lasso_coordinate_descent(X_z, y_z, optimal_alpha)

# Get regularization path
coefs_path = []
for alpha in alphas_path:
    coef = lasso_coordinate_descent(X_z, y_z, alpha)
    coefs_path.append(coef)
coefs_path = np.array(coefs_path).T

# Create visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Left: Coefficients with optimal alpha
x_pos = np.arange(p)
width = 0.35

axes[0].bar(x_pos - width/2, true_coef, width, alpha=0.5, 
            label='True', edgecolor='black', color='blue')
axes[0].bar(x_pos + width/2, optimal_coef, width, alpha=0.7,
           label='Lasso (CV)', edgecolor='black', color='green')
axes[0].axhline(0, color='black', linestyle='--', linewidth=2, alpha=0.5)
axes[0].set_xlabel('Feature Index', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
axes[0].set_title(f'LASSO with Optimal α\nα = {optimal_alpha:.4f}',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')

# Right: Regularization path
# Color the first 5 features differently (true non-zero)
for i in range(p):
    if i < 5:
        axes[1].plot(alphas_path, coefs_path[i], '-', alpha=0.8, 
                    linewidth=2.5, color=f'C{i}')
    else:
        axes[1].plot(alphas_path, coefs_path[i], '-', alpha=0.4, 
                    linewidth=1.5, color='gray')

axes[1].axvline(optimal_alpha, color='red', linestyle='--', linewidth=3,
               label=f'Optimal α = {optimal_alpha:.4f}', zorder=10)
axes[1].set_xscale('log')
axes[1].set_xlabel('α (Regularization Strength)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Coefficient', fontsize=12, fontweight='bold')
axes[1].set_title('REGULARIZATION PATH\nCoefficients vs α',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('lasso_cv_regularization_path.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Generated: lasso_cv_regularization_path.png")

# Print results
print(f"\nOptimal α (Cross-Validation): {optimal_alpha:.4f}")
print(f"Selected features: {np.sum(np.abs(optimal_coef) > 0.01)}")
print(f"True relevant features: 5")
print("\n→ CV finds optimal balance between bias and variance")
