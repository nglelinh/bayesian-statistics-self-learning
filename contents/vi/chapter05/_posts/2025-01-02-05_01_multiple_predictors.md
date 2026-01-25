---
layout: post
title: "Bài 5.1: Multiple Regression - Từ Một đến Nhiều Predictors"
chapter: '05'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter05
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu cách mở rộng Bayesian linear regression từ **một predictor** sang **nhiều predictors**. Bạn sẽ học được ý nghĩa của coefficients trong multiple regression - chúng khác với simple regression như thế nào và tại sao. Quan trọng hơn, bạn sẽ hiểu rằng mỗi coefficient đo lường effect của một predictor **khi giữ các predictors khác cố định** - một khái niệm cốt lõi trong causal inference.

## Giới thiệu: Thế giới Thực Có Nhiều Factors

Trong Chapter 04, chúng ta học về simple linear regression:

$$y = \alpha + \beta x + \epsilon$$

Nhưng trong thực tế, outcomes thường phụ thuộc vào **nhiều factors**, không chỉ một:

- **Cân nặng** phụ thuộc vào: Chiều cao, Tuổi, Giới tính, Hoạt động thể chất, ...
- **Thu nhập** phụ thuộc vào: Học vấn, Kinh nghiệm, Ngành nghề, Khu vực, ...
- **Điểm thi** phụ thuộc vào: Số giờ học, IQ, Động lực, Chất lượng giảng dạy, ...

**Multiple regression** cho phép chúng ta model nhiều predictors cùng lúc:

$$y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_k x_k + \epsilon$$

Nhưng điều này không chỉ đơn giản là "thêm variables". Ý nghĩa của coefficients thay đổi hoàn toàn!

## 1. Ý nghĩa của Coefficients: "Holding Others Constant"

![Multiple Predictors Visualization]({{ site.baseurl }}/img/chapter_img/chapter05/multiple_predictors_visualization.png)

### 1.1. Simple vs Multiple Regression

Hãy xem một ví dụ cụ thể:

**Bài toán**: Dự đoán **cân nặng** từ **chiều cao** và **tuổi**.

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
from scipy import stats
import seaborn as sns

# Generate synthetic data
np.random.seed(42)
n = 100

# True parameters
true_alpha = 50  # kg
true_beta_height = 0.5  # kg/cm
true_beta_age = 0.3  # kg/year
true_sigma = 3  # kg

# Predictors
height = np.random.uniform(150, 190, n)  # cm
age = np.random.uniform(20, 60, n)  # years

# Outcome
weight = (true_alpha + 
          true_beta_height * height + 
          true_beta_age * age + 
          np.random.normal(0, true_sigma, n))

# Visualize
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. Weight vs Height (ignoring age)
axes[0].scatter(height, weight, s=50, alpha=0.6, c=age, cmap='viridis',
               edgecolors='black')
axes[0].set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[0].set_title('Weight vs Height\n(Color = Age)',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)
cbar = plt.colorbar(axes[0].collections[0], ax=axes[0])
cbar.set_label('Age (years)', fontsize=11)

# 2. Weight vs Age (ignoring height)
axes[1].scatter(age, weight, s=50, alpha=0.6, c=height, cmap='plasma',
               edgecolors='black')
axes[1].set_xlabel('Age (years)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Weight (kg)', fontsize=12, fontweight='bold')
axes[1].set_title('Weight vs Age\n(Color = Height)',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)
cbar = plt.colorbar(axes[1].collections[0], ax=axes[1])
cbar.set_label('Height (cm)', fontsize=11)

# 3. 3D visualization
from mpl_toolkits.mplot3d import Axes3D
ax3d = fig.add_subplot(133, projection='3d')
ax3d.scatter(height, age, weight, s=30, alpha=0.6, edgecolors='black')
ax3d.set_xlabel('Height (cm)', fontsize=11, fontweight='bold')
ax3d.set_ylabel('Age (years)', fontsize=11, fontweight='bold')
ax3d.set_zlabel('Weight (kg)', fontsize=11, fontweight='bold')
ax3d.set_title('3D: Weight vs Height & Age',
              fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()

print("=" * 70)
print("DATA GENERATION")
print("=" * 70)
print(f"\nTrue Model:")
print(f"  Weight = {true_alpha} + {true_beta_height}·Height + {true_beta_age}·Age + ε")
print(f"  σ = {true_sigma} kg")
print(f"\nInterpretation:")
print(f"  - Mỗi cm chiều cao tăng → +{true_beta_height} kg (holding age constant)")
print(f"  - Mỗi năm tuổi tăng → +{true_beta_age} kg (holding height constant)")
print("=" * 70)
```

### 1.2. "Holding Others Constant" - Ý nghĩa Quan trọng

Trong **multiple regression**:

$$\beta_1$$ = Effect của $$x_1$$ trên $$y$$, **giữ $$x_2, x_3, \ldots$$ cố định**

Đây là khác biệt quan trọng với simple regression:
- **Simple**: $$\beta$$ = tổng effect (bao gồm cả indirect effects qua other variables)
- **Multiple**: $$\beta_1$$ = direct effect (controlling for other variables)

## 2. Bayesian Multiple Regression với PyMC

### 2.1. Model Specification

```python
# Standardize data (remember Chapter 04!)
height_mean, height_std = height.mean(), height.std()
age_mean, age_std = age.mean(), age.std()
weight_mean, weight_std = weight.mean(), weight.std()

height_z = (height - height_mean) / height_std
age_z = (age - age_mean) / age_std
weight_z = (weight - weight_mean) / weight_std

# Bayesian Multiple Regression
with pm.Model() as multiple_regression:
    # Priors (weakly informative)
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta_height = pm.Normal('beta_height', mu=0, sigma=1)
    beta_age = pm.Normal('beta_age', mu=0, sigma=1)
    sigma = pm.HalfNormal('sigma', sigma=1)
    
    # Linear model with MULTIPLE predictors
    mu = alpha + beta_height * height_z + beta_age * age_z
    
    # Likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=weight_z)
    
    # Sample
    trace = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                     return_inferencedata=True)

# Summary
print("\n" + "=" * 70)
print("POSTERIOR SUMMARY")
print("=" * 70)
summary = az.summary(trace, var_names=['alpha', 'beta_height', 'beta_age', 'sigma'])
print(summary)
print("=" * 70)

# Check diagnostics
print("\nDIAGNOSTICS:")
print("-" * 70)
for var in ['alpha', 'beta_height', 'beta_age', 'sigma']:
    rhat = summary.loc[var, 'r_hat']
    ess = summary.loc[var, 'ess_bulk']
    print(f"{var:15} R-hat={rhat:.4f} {'✓' if rhat < 1.01 else '✗'}  " +
          f"ESS={ess:>6.0f} {'✓' if ess > 400 else '✗'}")
print("-" * 70)
```

### 2.2. Interpret Posterior

```python
# Extract posterior samples
alpha_samples = trace.posterior['alpha'].values.flatten()
beta_height_samples = trace.posterior['beta_height'].values.flatten()
beta_age_samples = trace.posterior['beta_age'].values.flatten()
sigma_samples = trace.posterior['sigma'].values.flatten()

# Transform back to original scale
beta_height_orig = beta_height_samples * (weight_std / height_std)
beta_age_orig = beta_age_samples * (weight_std / age_std)

# Visualize posteriors
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Beta_height
axes[0, 0].hist(beta_height_orig, bins=50, density=True, alpha=0.7,
               color='skyblue', edgecolors='black')
axes[0, 0].axvline(beta_height_orig.mean(), color='red', linewidth=2,
                  label=f'Mean = {beta_height_orig.mean():.3f}')
axes[0, 0].axvline(true_beta_height, color='green', linestyle='--', linewidth=2,
                  label=f'True = {true_beta_height:.3f}')
axes[0, 0].set_xlabel('β_height (kg/cm)', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0, 0].set_title('Posterior: Effect of Height\n(holding age constant)',
                     fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=11)
axes[0, 0].grid(alpha=0.3, axis='y')

# Beta_age
axes[0, 1].hist(beta_age_orig, bins=50, density=True, alpha=0.7,
               color='lightgreen', edgecolors='black')
axes[0, 1].axvline(beta_age_orig.mean(), color='red', linewidth=2,
                  label=f'Mean = {beta_age_orig.mean():.3f}')
axes[0, 1].axvline(true_beta_age, color='green', linestyle='--', linewidth=2,
                  label=f'True = {true_beta_age:.3f}')
axes[0, 1].set_xlabel('β_age (kg/year)', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0, 1].set_title('Posterior: Effect of Age\n(holding height constant)',
                     fontsize=14, fontweight='bold')
axes[0, 1].legend(fontsize=11)
axes[0, 1].grid(alpha=0.3, axis='y')

# Joint posterior (scatter)
axes[1, 0].scatter(beta_height_orig, beta_age_orig, s=1, alpha=0.3)
axes[1, 0].axvline(true_beta_height, color='green', linestyle='--', linewidth=2)
axes[1, 0].axhline(true_beta_age, color='green', linestyle='--', linewidth=2)
axes[1, 0].set_xlabel('β_height (kg/cm)', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('β_age (kg/year)', fontsize=12, fontweight='bold')
axes[1, 0].set_title('Joint Posterior\nβ_height vs β_age',
                     fontsize=14, fontweight='bold')
axes[1, 0].grid(alpha=0.3)

# Interpretation
axes[1, 1].axis('off')
interp = f"""
POSTERIOR INTERPRETATION

β_height (holding age constant):
  Mean: {beta_height_orig.mean():.3f} kg/cm
  95% CI: [{np.percentile(beta_height_orig, 2.5):.3f}, 
           {np.percentile(beta_height_orig, 97.5):.3f}]
  
  → Mỗi cm chiều cao tăng
    cân nặng tăng ~{beta_height_orig.mean():.3f} kg
    (khi age không đổi)

β_age (holding height constant):
  Mean: {beta_age_orig.mean():.3f} kg/year
  95% CI: [{np.percentile(beta_age_orig, 2.5):.3f}, 
           {np.percentile(beta_age_orig, 97.5):.3f}]
  
  → Mỗi năm tuổi tăng
    cân nặng tăng ~{beta_age_orig.mean():.3f} kg
    (khi height không đổi)

→ Cả hai effects đều positive!
"""

axes[1, 1].text(0.5, 0.5, interp, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.show()
```

## 3. Matrix Notation: Elegant và Scalable

Với nhiều predictors, matrix notation giúp code gọn gàng hơn:

$$\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}$$

Trong đó:
- $$\mathbf{y}$$: Vector outcomes ($$n \times 1$$)
- $$\mathbf{X}$$: Design matrix ($$n \times k$$)
- $$\boldsymbol{\beta}$$: Vector coefficients ($$k \times 1$$)

```python
# Matrix formulation
X_standardized = np.column_stack([height_z, age_z])

with pm.Model() as matrix_regression:
    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1, shape=2)  # Vector of 2 coefficients
    sigma = pm.HalfNormal('sigma', sigma=1)
    
    # Linear model (matrix multiplication)
    mu = alpha + pm.math.dot(X_standardized, beta)
    
    # Likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=weight_z)
    
    # Sample
    trace_matrix = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                            return_inferencedata=True)

print("\nMATRIX FORMULATION:")
print("-" * 70)
print("✓ Cleaner code")
print("✓ Scales to many predictors")
print("✓ Same results as explicit formulation")
print("-" * 70)
```

## Tóm tắt và Kết nối

Multiple regression mở rộng simple regression:

- **Model**: $$y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \cdots + \epsilon$$
- **Coefficients**: Mỗi $$\beta_j$$ = effect của $$x_j$$ **holding others constant**
- **Implementation**: PyMC với multiple priors
- **Matrix notation**: Elegant và scalable

**Key insight**: Coefficients trong multiple regression có ý nghĩa khác simple regression - chúng đo lường **direct effects**, không phải total effects.

Trong các bài tiếp theo, chúng ta sẽ học:
- **Bài 5.2**: Confounding và DAGs - khi nào cần control for variables
- **Bài 5.3**: Multicollinearity - vấn đề khi predictors correlate
- **Bài 5.4**: Interactions - khi effects phụ thuộc nhau

## Bài tập

**Bài tập 1: Three Predictors**
Generate data với 3 predictors và fit multiple regression.
(a) Interpret mỗi coefficient
(b) Compare với simple regressions
(c) Coefficients có khác nhau không?

**Bài tập 2: Holding Constant**
(a) Giải thích "holding others constant" bằng lời
(b) Tại sao điều này quan trọng?
(c) Cho ví dụ khi không hold constant dẫn đến sai lầm

**Bài tập 3: Matrix Formulation**
(a) Implement regression với 5 predictors using matrix notation
(b) Verify kết quả giống explicit formulation
(c) Code nào gọn hơn?

**Bài tập 4: Standardization**
(a) Tại sao standardization quan trọng trong multiple regression?
(b) Coefficients có comparable không khi không standardize?
(c) Transform back to original scale

**Bài tập 5: Predictions**
Cho new data: Height=170cm, Age=30 years.
(a) Predict weight với uncertainty
(b) 95% credible interval
(c) Visualize posterior predictive distribution

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Hill, J., & Vehtari, A. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 10: Linear regression with multiple predictors

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 5: The Many Variables & The Spurious Waffles

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis* (2nd Edition). Academic Press.
- Chapter 18: Metric Predicted Variable with Multiple Metric Predictors

---

*Bài học tiếp theo: [5.2 Confounding và DAGs](/vi/chapter05/confounding-dags/)*
