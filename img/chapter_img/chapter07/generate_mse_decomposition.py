#!/usr/bin/env python3
"""
Generate MSE decomposition visualization
Shows how MSE = Bias² + Variance changes with model complexity
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

# Manual linear regression (no sklearn)
def fit_polynomial(x_train, y_train, degree):
    """Fit polynomial using least squares"""
    X = create_polynomial_features(x_train, degree)
    coeffs = np.linalg.lstsq(X, y_train, rcond=None)[0]
    return coeffs

def predict_polynomial(x_test, coeffs):
    """Predict using polynomial coefficients"""
    degree = len(coeffs) - 1
    X = create_polynomial_features(x_test, degree)
    return X @ coeffs

# Generate test data
x_test = np.linspace(0, 10, 100)
y_true = true_function(x_test)

# Compute bias-variance decomposition for different polynomial degrees
degrees_range = range(1, 16)
biases = []
variances = []
mses = []

for degree in degrees_range:
    predictions = []
    
    # Generate 100 different training sets
    for _ in range(100):
        x_train = np.random.uniform(0, 10, 20)
        y_train = true_function(x_train) + np.random.normal(0, 1, 20)
        
        coeffs = fit_polynomial(x_train, y_train, degree)
        y_pred = predict_polynomial(x_test, coeffs)
        predictions.append(y_pred)
    
    predictions = np.array(predictions)
    mean_pred = predictions.mean(axis=0)
    
    # Compute bias² and variance
    bias_sq = ((mean_pred - y_true)**2).mean()
    variance = predictions.var(axis=0).mean()
    mse = ((predictions - y_true)**2).mean()
    
    biases.append(bias_sq)
    variances.append(variance)
    mses.append(mse)

# Create visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Left plot: Decomposition curves
axes[0].plot(degrees_range, biases, 'r-o', linewidth=3, markersize=8, label='Bias²')
axes[0].plot(degrees_range, variances, 'b-s', linewidth=3, markersize=8, label='Variance')
axes[0].plot(degrees_range, mses, 'g-^', linewidth=3, markersize=8, label='MSE (Total)')
axes[0].axvline(3, color='orange', linestyle='--', linewidth=2, alpha=0.7,
               label='Optimal complexity')
axes[0].set_xlabel('Model Complexity (Polynomial Degree)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Error', fontsize=12, fontweight='bold')
axes[0].set_title('BIAS-VARIANCE DECOMPOSITION\nMSE = Bias² + Variance',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Right plot: Stacked area chart
axes[1].fill_between(degrees_range, 0, biases, alpha=0.5, color='red', label='Bias²')
axes[1].fill_between(degrees_range, biases, np.array(biases) + np.array(variances),
                    alpha=0.5, color='blue', label='Variance')
axes[1].plot(degrees_range, mses, 'g-', linewidth=3, label='Total MSE')
axes[1].axvline(3, color='orange', linestyle='--', linewidth=2, alpha=0.7)
axes[1].set_xlabel('Model Complexity (Polynomial Degree)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Error', fontsize=12, fontweight='bold')
axes[1].set_title('STACKED VIEW\nFinding the Sweet Spot',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('mse_decomposition.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Generated: mse_decomposition.png")

# Print optimal complexity info
optimal_idx = np.argmin(mses)
optimal_degree = list(degrees_range)[optimal_idx]
print(f"  Optimal degree: {optimal_degree}")
print(f"  Bias²: {biases[optimal_idx]:.3f}")
print(f"  Variance: {variances[optimal_idx]:.3f}")
print(f"  MSE: {mses[optimal_idx]:.3f}")
