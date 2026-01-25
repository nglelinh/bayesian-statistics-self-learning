---
layout: post
title: "Bài 7.2: Bias-Variance Tradeoff - Cốt lõi của Model Selection"
chapter: '07'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter07
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu sâu về **bias-variance tradeoff** - một trong những concepts quan trọng nhất trong machine learning và statistics. Bạn sẽ học tại sao simple models có high bias, complex models có high variance, và làm sao tìm sweet spot ở giữa. Đây là foundation để hiểu regularization và model selection.

## Giới thiệu: Hai Loại Error

Khi model dự đoán sai, có hai nguyên nhân:

1. **Bias**: Model quá simple → không capture được pattern
2. **Variance**: Model quá complex → học noise thay vì signal

**Tradeoff**: Giảm bias → tăng variance (và ngược lại).

## 1. Bias và Variance: Định nghĩa

### 1.1. Mathematical Definitions

Giả sử chúng ta train model nhiều lần trên different datasets từ cùng một distribution.

**Bias**: Sai lệch giữa **average prediction** và **true value**
$$
\text{Bias}[\hat{f}(x)] = \mathbb{E}[\hat{f}(x)] - f(x)
$$

**Variance**: Variability của predictions across datasets
$$
\text{Variance}[\hat{f}(x)] = \mathbb{E}[(\hat{f}(x) - \mathbb{E}[\hat{f}(x)])^2]
$$

**Total Error**:
$$
\mathbb{E}[(y - \hat{f}(x))^2] = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}
$$

### 1.2. Intuitive Understanding

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# True function
def true_function(x):
    return 2 + 0.5*x + 0.1*x**2

# Generate multiple datasets and fit models
np.random.seed(42)
n_datasets = 50
n_points = 20
x_test = np.linspace(0, 10, 100)
y_true = true_function(x_test)

# Different model complexities
degrees = [1, 3, 15]
titles = ['HIGH BIAS\n(Underfitting)', 'BALANCED\n(Good Fit)', 'HIGH VARIANCE\n(Overfitting)']
colors = ['red', 'green', 'orange']

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, (degree, title, color) in enumerate(zip(degrees, titles, colors)):
    predictions = []
    
    for _ in range(n_datasets):
        # Generate training data
        x_train = np.random.uniform(0, 10, n_points)
        y_train = true_function(x_train) + np.random.normal(0, 1, n_points)
        
        # Fit model
        poly = PolynomialFeatures(degree=degree)
        X_train_poly = poly.fit_transform(x_train.reshape(-1, 1))
        X_test_poly = poly.transform(x_test.reshape(-1, 1))
        
        lr = LinearRegression().fit(X_train_poly, y_train)
        y_pred = lr.predict(X_test_poly)
        predictions.append(y_pred)
        
        # Plot individual fits (faint)
        axes[idx].plot(x_test, y_pred, '-', alpha=0.1, color=color, linewidth=1)
    
    # Compute bias and variance
    predictions = np.array(predictions)
    mean_pred = predictions.mean(axis=0)
    bias = mean_pred - y_true
    variance = predictions.var(axis=0)
    
    # Plot
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
    
    # Add text
    avg_bias = np.abs(bias).mean()
    avg_var = variance.mean()
    axes[idx].text(0.5, 0.95, f'Avg |Bias|: {avg_bias:.2f}\nAvg Variance: {avg_var:.2f}',
                  transform=axes[idx].transAxes, ha='center', va='top',
                  fontsize=11, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

plt.tight_layout()
plt.show()

print("=" * 70)
print("BIAS-VARIANCE TRADEOFF")
print("=" * 70)
print("\nHIGH BIAS (Underfitting):")
print("  • Simple model")
print("  • Predictions close together (low variance)")
print("  • But far from truth (high bias)")

print("\nBALANCED:")
print("  • Medium complexity")
print("  • Reasonable variance")
print("  • Low bias")

print("\nHIGH VARIANCE (Overfitting):")
print("  • Complex model")
print("  • Predictions spread out (high variance)")
print("  • Mean close to truth (low bias)")
print("  • But individual predictions unreliable!")
print("=" * 70)
```

## 2. Decomposition: MSE = Bias² + Variance + Noise

```python
# Compute bias-variance decomposition
degrees_range = range(1, 16)
biases = []
variances = []
mses = []

for degree in degrees_range:
    predictions = []
    
    for _ in range(100):
        x_train = np.random.uniform(0, 10, 20)
        y_train = true_function(x_train) + np.random.normal(0, 1, 20)
        
        poly = PolynomialFeatures(degree=degree)
        X_train_poly = poly.fit_transform(x_train.reshape(-1, 1))
        X_test_poly = poly.transform(x_test.reshape(-1, 1))
        
        lr = LinearRegression().fit(X_train_poly, y_train)
        y_pred = lr.predict(X_test_poly)
        predictions.append(y_pred)
    
    predictions = np.array(predictions)
    mean_pred = predictions.mean(axis=0)
    
    # Bias and Variance
    bias_sq = ((mean_pred - y_true)**2).mean()
    variance = predictions.var(axis=0).mean()
    mse = ((predictions - y_true)**2).mean()
    
    biases.append(bias_sq)
    variances.append(variance)
    mses.append(mse)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Decomposition
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

# Stacked area
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
plt.show()

print("\n" + "=" * 70)
print("OPTIMAL COMPLEXITY")
print("=" * 70)
optimal_idx = np.argmin(mses)
optimal_degree = degrees_range[optimal_idx]
print(f"\nOptimal degree: {optimal_degree}")
print(f"  Bias²: {biases[optimal_idx]:.3f}")
print(f"  Variance: {variances[optimal_idx]:.3f}")
print(f"  MSE: {mses[optimal_idx]:.3f}")
print("\n→ Sweet spot balances bias and variance!")
print("=" * 70)
```

## 3. Regularization và Bias-Variance

**Regularization** controls bias-variance tradeoff:
- **Weak regularization** (λ small): Low bias, high variance
- **Strong regularization** (λ large): High bias, low variance

```python
from sklearn.linear_model import Ridge

# Test different regularization strengths
alphas = [0.001, 0.1, 1, 10, 100]
degree = 10  # High degree polynomial

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.ravel()

for idx, alpha in enumerate(alphas):
    predictions = []
    
    for _ in range(50):
        x_train = np.random.uniform(0, 10, 20)
        y_train = true_function(x_train) + np.random.normal(0, 1, 20)
        
        poly = PolynomialFeatures(degree=degree)
        X_train_poly = poly.fit_transform(x_train.reshape(-1, 1))
        X_test_poly = poly.transform(x_test.reshape(-1, 1))
        
        ridge = Ridge(alpha=alpha).fit(X_train_poly, y_train)
        y_pred = ridge.predict(X_test_poly)
        predictions.append(y_pred)
        
        axes[idx].plot(x_test, y_pred, '-', alpha=0.1, color='orange', linewidth=1)
    
    predictions = np.array(predictions)
    mean_pred = predictions.mean(axis=0)
    bias_sq = ((mean_pred - y_true)**2).mean()
    variance = predictions.var(axis=0).mean()
    
    axes[idx].plot(x_test, y_true, 'b-', linewidth=3, label='True', zorder=10)
    axes[idx].plot(x_test, mean_pred, 'r--', linewidth=3, label='Mean pred', zorder=9)
    axes[idx].set_xlabel('x', fontsize=11, fontweight='bold')
    axes[idx].set_ylabel('y', fontsize=11, fontweight='bold')
    axes[idx].set_title(f'λ = {alpha}\nBias²={bias_sq:.2f}, Var={variance:.2f}',
                       fontsize=13, fontweight='bold')
    axes[idx].legend(fontsize=10)
    axes[idx].grid(alpha=0.3)
    axes[idx].set_ylim(-2, 18)

axes[-1].axis('off')

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("REGULARIZATION EFFECT")
print("=" * 70)
print("\nWeak regularization (λ small):")
print("  → Low bias, HIGH variance")
print("  → Overfitting")

print("\nStrong regularization (λ large):")
print("  → HIGH bias, low variance")
print("  → Underfitting")

print("\nOptimal regularization:")
print("  → Balanced bias-variance")
print("=" * 70)
```

## 4. Bayesian Perspective

Trong Bayesian statistics:
- **Prior strength** controls bias-variance
- **Weak priors**: High variance (flexible, data-driven)
- **Strong priors**: High bias (rigid, prior-driven)

```python
import pymc as pm
import arviz as az

# Generate data
np.random.seed(42)
n = 30
x_data = np.random.uniform(0, 10, n)
y_data = true_function(x_data) + np.random.normal(0, 1, n)

x_data_z = (x_data - x_data.mean()) / x_data.std()
y_data_z = (y_data - y_data.mean()) / y_data.std()

# Different prior strengths
prior_sds = [0.1, 0.5, 2, 10]

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.ravel()

for idx, prior_sd in enumerate(prior_sds):
    with pm.Model() as model:
        alpha = pm.Normal('alpha', 0, 1)
        beta = pm.Normal('beta', 0, prior_sd)  # Varying prior strength
        sigma = pm.HalfNormal('sigma', 1)
        
        mu = alpha + beta * x_data_z
        y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_data_z)
        
        trace = pm.sample(500, tune=200, chains=2, random_seed=42,
                         return_inferencedata=True, progressbar=False)
    
    # Posterior predictions
    alpha_samples = trace.posterior['alpha'].values.flatten()
    beta_samples = trace.posterior['beta'].values.flatten()
    
    # Plot
    x_plot_z = (x_test - x_data.mean()) / x_data.std()
    for i in range(min(100, len(alpha_samples))):
        y_plot_z = alpha_samples[i] + beta_samples[i] * x_plot_z
        y_plot = y_plot_z * y_data.std() + y_data.mean()
        axes[idx].plot(x_test, y_plot, '-', alpha=0.05, color='orange')
    
    axes[idx].scatter(x_data, y_data, s=60, alpha=0.7, edgecolors='black',
                     label='Data', zorder=5)
    axes[idx].plot(x_test, y_true, 'b-', linewidth=3, label='True', zorder=4)
    axes[idx].set_xlabel('x', fontsize=11, fontweight='bold')
    axes[idx].set_ylabel('y', fontsize=11, fontweight='bold')
    
    if prior_sd < 1:
        title_color = 'red'
        subtitle = '(High Bias)'
    elif prior_sd > 5:
        title_color = 'orange'
        subtitle = '(High Variance)'
    else:
        title_color = 'green'
        subtitle = '(Balanced)'
    
    axes[idx].set_title(f'Prior SD = {prior_sd} {subtitle}',
                       fontsize=13, fontweight='bold', color=title_color)
    axes[idx].legend(fontsize=10)
    axes[idx].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## Tóm tắt

Bias-Variance Tradeoff:

- **Bias**: Error from overly simple model
- **Variance**: Error from sensitivity to training data
- **MSE = Bias² + Variance + Irreducible Error**
- **Regularization**: Controls tradeoff
- **Goal**: Find sweet spot that minimizes total error

**Key insight**: Perfect fit on training data ≠ good model. Balance is key!

Bài tiếp theo: **Feature Selection**.

## Bài tập

**Bài tập 1**: Implement bias-variance decomposition from scratch. Verify MSE = Bias² + Variance.

**Bài tập 2**: Generate data. Compute bias-variance for models with different complexities. Find optimal.

**Bài tập 3**: Use Ridge với different λ. Plot bias-variance curve. Find optimal λ.

**Bài tập 4**: Bayesian models với different prior SDs. Compute posterior variance. Relate to bias-variance.

**Bài tập 5**: Real data. Split train/test. Show overfitting với high-degree polynomial. Fix với regularization.

## Tài liệu Tham khảo

**Hastie, T., Tibshirani, R., & Friedman, J. (2009).** *The Elements of Statistical Learning* (2nd Edition). Springer.
- Chapter 7: Model Assessment and Selection

**James, G., et al. (2013).** *An Introduction to Statistical Learning*. Springer.
- Chapter 2: Statistical Learning

---

*Bài học tiếp theo: [7.3 Feature Selection](/vi/chapter07/feature-selection/)*
