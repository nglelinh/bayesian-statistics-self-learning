#!/usr/bin/env python3
"""
Generate overfitting demonstration
Replaces code block at line 30 in 07_01_regularization_priors.md
"""

import numpy as np
import matplotlib.pyplot as plt

# Simple polynomial features implementation
def polynomial_features(x, degree):
    """Generate polynomial features up to given degree"""
    n = len(x)
    X = np.ones((n, degree + 1))
    for i in range(1, degree + 1):
        X[:, i] = x ** i
    return X

# Simple linear regression using least squares
def fit_linear_regression(X, y):
    """Fit linear regression using normal equation"""
    coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
    return coeffs

def predict(X, coeffs):
    """Predict using linear model"""
    return X @ coeffs

# Simple train_test_split
def train_test_split_simple(x, y, test_size=0.3, random_state=42):
    """Simple train-test split"""
    np.random.seed(random_state)
    n = len(x)
    n_test = int(n * test_size)
    indices = np.random.permutation(n)
    test_idx = indices[:n_test]
    train_idx = indices[n_test:]
    return x[train_idx], x[test_idx], y[train_idx], y[test_idx]

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# Generate data
np.random.seed(42)
n = 25
x = np.random.uniform(0, 10, n)
y_true = 2 + 0.5*x + np.random.normal(0, 2, n)

# Split train/test
x_train, x_test, y_train, y_test = train_test_split_simple(
    x, y_true, test_size=0.3, random_state=42
)

# Fit models with different polynomial degrees
degrees = [1, 3, 10, 15]
x_plot = np.linspace(0, 10, 200)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.ravel()

for idx, degree in enumerate(degrees):
    # Transform
    X_train_poly = polynomial_features(x_train, degree)
    X_test_poly = polynomial_features(x_test, degree)
    X_plot_poly = polynomial_features(x_plot, degree)
    
    # Fit
    coeffs = fit_linear_regression(X_train_poly, y_train)
    
    # Predict
    y_pred_train = predict(X_train_poly, coeffs)
    y_pred_test = predict(X_test_poly, coeffs)
    y_plot = predict(X_plot_poly, coeffs)
    
    # Compute errors
    train_rmse = np.sqrt(np.mean((y_train - y_pred_train)**2))
    test_rmse = np.sqrt(np.mean((y_test - y_pred_test)**2))
    
    # Plot
    axes[idx].scatter(x_train, y_train, s=100, alpha=0.7, label='Train',
                     edgecolors='black', zorder=3, color='#3498db')
    axes[idx].scatter(x_test, y_test, s=100, alpha=0.7, label='Test',
                     edgecolors='black', zorder=3, color='#e74c3c')
    axes[idx].plot(x_plot, y_plot, 'g-', linewidth=3, label='Fit', zorder=2)
    
    # Title with error
    color = 'green' if degree <= 3 else 'red'
    axes[idx].set_title(f'Degree = {degree}\n' +
                       f'Train RMSE = {train_rmse:.2f}, Test RMSE = {test_rmse:.2f}',
                       fontsize=13, fontweight='bold', color=color)
    axes[idx].set_xlabel('x', fontsize=11, fontweight='bold')
    axes[idx].set_ylabel('y', fontsize=11, fontweight='bold')
    axes[idx].legend(fontsize=10, loc='upper left')
    axes[idx].grid(alpha=0.3)
    axes[idx].set_ylim(-5, 15)
    
    # Add annotation
    if degree == 1:
        axes[idx].text(5, -3, 'UNDERFIT: Too simple', fontsize=10, ha='center',
                      bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    elif degree == 3:
        axes[idx].text(5, -3, 'GOOD FIT: Just right', fontsize=10, ha='center',
                      bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    elif degree >= 10:
        axes[idx].text(5, -3, 'OVERFIT: Too complex', fontsize=10, ha='center',
                      bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))

plt.suptitle('Overfitting Demonstration: Model Complexity vs Generalization',
            fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('overfitting_demonstration.png', dpi=300, bbox_inches='tight',
            facecolor='white')
print("✓ Generated: overfitting_demonstration.png")
print(f"  - Training samples: {len(x_train)}, Test samples: {len(x_test)}")
print("  - Degree 1: Underfit (too simple)")
print("  - Degree 3: Good fit (balanced)")
print("  - Degree 10+: Overfit (memorizes training data)")

plt.close()
