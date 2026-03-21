#!/usr/bin/env python3
"""
Generate bias-variance demonstration visualization
Shows 3 polynomial models (degrees 1, 3, 10) with multiple predictions from different training sets
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

# Three model complexities
degrees = [1, 3, 10]
titles = ['HIGH BIAS (Underfitting)', 'BALANCED', 'HIGH VARIANCE (Overfitting)']
colors = ['red', 'green', 'orange']

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, (degree, title, color) in enumerate(zip(degrees, titles, colors)):
    predictions = []
    
    # Generate 50 different training sets and fit models
    for _ in range(50):
        x_train = np.random.uniform(0, 10, 20)
        y_train = true_function(x_train) + np.random.normal(0, 1, 20)
        
        coeffs = fit_polynomial(x_train, y_train, degree)
        y_pred = predict_polynomial(x_test, coeffs)
        predictions.append(y_pred)
        
        # Plot individual predictions
        axes[idx].plot(x_test, y_pred, '-', alpha=0.1, color=color, linewidth=1)
    
    predictions = np.array(predictions)
    mean_pred = predictions.mean(axis=0)
    variance = predictions.var(axis=0)
    bias = mean_pred - y_true
    
    # Plot true function and mean prediction
    axes[idx].plot(x_test, y_true, 'b-', linewidth=3, label='True function', zorder=10)
    axes[idx].plot(x_test, mean_pred, 'r--', linewidth=3, label='Mean prediction', zorder=9)
    axes[idx].fill_between(x_test, 
                          mean_pred - np.sqrt(variance),
                          mean_pred + np.sqrt(variance),
                          alpha=0.3, color=color, label='±1 SD')
    
    axes[idx].set_xlabel('x', fontsize=12, fontweight='bold')
    axes[idx].set_ylabel('y', fontsize=12, fontweight='bold')
    axes[idx].set_title(f'{title}\nDegree = {degree}',
                       fontsize=14, fontweight='bold')
    axes[idx].legend(fontsize=10)
    axes[idx].grid(alpha=0.3)
    axes[idx].set_ylim(-2, 18)
    
    # Add text with statistics
    avg_bias = np.abs(bias).mean()
    avg_var = variance.mean()
    axes[idx].text(0.5, 0.95, f'Avg |Bias|: {avg_bias:.2f}\nAvg Variance: {avg_var:.2f}',
                  transform=axes[idx].transAxes, ha='center', va='top',
                  fontsize=11, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

plt.tight_layout()
plt.savefig('bias_variance_demonstration.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Generated: bias_variance_demonstration.png")
