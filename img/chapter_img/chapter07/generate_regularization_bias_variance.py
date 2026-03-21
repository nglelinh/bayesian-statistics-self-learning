#!/usr/bin/env python3
"""
Generate regularization bias-variance visualization
Shows Ridge regression with different lambda values (degree 10 polynomial)
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

# True function
def true_function(x):
    return 2 + 0.5 * x + 0.2 * x**2 - 0.01 * x**3

# Manual polynomial features implementation (no sklearn)
def create_polynomial_features(x, degree):
    """Create polynomial features up to given degree"""
    n = len(x)
    X = np.ones((n, degree + 1))
    for i in range(1, degree + 1):
        X[:, i] = x ** i
    return X

# Manual Ridge regression (no sklearn)
def fit_ridge(x_train, y_train, degree, alpha):
    """Fit Ridge regression using closed-form solution"""
    X = create_polynomial_features(x_train, degree)
    n_features = X.shape[1]
    
    # Ridge regression: (X^T X + alpha * I) coeffs = X^T y
    XTX = X.T @ X
    identity = np.eye(n_features)
    identity[0, 0] = 0  # Don't regularize intercept
    
    coeffs = np.linalg.solve(XTX + alpha * identity, X.T @ y_train)
    return coeffs

def predict_polynomial(x_test, coeffs):
    """Predict using polynomial coefficients"""
    degree = len(coeffs) - 1
    X = create_polynomial_features(x_test, degree)
    return X @ coeffs

# Generate test data
x_test = np.linspace(0, 10, 100)
y_true = true_function(x_test)

# Test different regularization strengths
alphas = [0.001, 0.1, 1, 10, 100]
degree = 10  # High degree polynomial

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.ravel()

for idx, alpha in enumerate(alphas):
    predictions = []
    
    # Generate 50 different training sets
    for _ in range(50):
        x_train = np.random.uniform(0, 10, 20)
        y_train = true_function(x_train) + np.random.normal(0, 1, 20)
        
        coeffs = fit_ridge(x_train, y_train, degree, alpha)
        y_pred = predict_polynomial(x_test, coeffs)
        predictions.append(y_pred)
        
        # Plot individual predictions
        axes[idx].plot(x_test, y_pred, '-', alpha=0.1, color='orange', linewidth=1)
    
    predictions = np.array(predictions)
    mean_pred = predictions.mean(axis=0)
    bias_sq = ((mean_pred - y_true)**2).mean()
    variance = predictions.var(axis=0).mean()
    
    # Plot true function and mean prediction
    axes[idx].plot(x_test, y_true, 'b-', linewidth=3, label='True', zorder=10)
    axes[idx].plot(x_test, mean_pred, 'r--', linewidth=3, label='Mean pred', zorder=9)
    axes[idx].set_xlabel('x', fontsize=11, fontweight='bold')
    axes[idx].set_ylabel('y', fontsize=11, fontweight='bold')
    axes[idx].set_title(f'λ = {alpha}\nBias²={bias_sq:.2f}, Var={variance:.2f}',
                       fontsize=13, fontweight='bold')
    axes[idx].legend(fontsize=10)
    axes[idx].grid(alpha=0.3)
    axes[idx].set_ylim(-2, 18)

# Hide the last subplot (we only have 5 plots)
axes[-1].axis('off')

plt.tight_layout()
plt.savefig('regularization_bias_variance.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Generated: regularization_bias_variance.png")
print("\nRegularization effects:")
print("  λ = 0.001: Low bias, high variance (overfitting)")
print("  λ = 0.1:   Balanced")
print("  λ = 1:     Balanced")
print("  λ = 10:    Higher bias, lower variance")
print("  λ = 100:   High bias, low variance (underfitting)")
