---
layout: post
title: "Bài 5.4: Interaction Effects - Khi Effects Phụ thuộc Nhau"
chapter: '05'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter05
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu về **interaction effects** - một trong những concepts quan trọng nhất trong modeling. Bạn sẽ học khi nào cần interactions, cách model chúng trong PyMC, và cách interpret results. Đây là bước quan trọng để hiểu rằng thế giới thực hiếm khi "additive" - effects thường phụ thuộc vào context.

## Giới thiệu: Thế giới Không Phải Lúc nào cũng Additive

Trong các bài trước, chúng ta giả định:

$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \epsilon
$$

Điều này có nghĩa: **Effect của $$x_1$$ không phụ thuộc vào $$x_2$$** (và ngược lại).

Nhưng trong thực tế:
- Effect của **exercise** lên **weight loss** phụ thuộc vào **diet**
- Effect của **study time** lên **test score** phụ thuộc vào **prior knowledge**
- Effect của **marketing** lên **sales** phụ thuộc vào **product quality**

Đây là **interaction effects**.

## 1. Additive vs Interactive Models

![Interaction Effects]({{ site.baseurl }}/img/chapter_img/chapter05/interaction_effects.png)

### 1.1. Visualization

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Generate data
np.random.seed(42)
n = 100

# Continuous predictor
x1 = np.random.uniform(0, 10, n)
# Binary predictor (e.g., treatment vs control)
x2 = np.random.binomial(1, 0.5, n)

# ADDITIVE: y = 2 + 0.5*x1 + 3*x2
y_additive = 2 + 0.5*x1 + 3*x2 + np.random.normal(0, 1, n)

# INTERACTIVE: y = 2 + 0.5*x1 + 3*x2 + 0.8*(x1*x2)
y_interactive = 2 + 0.5*x1 + 3*x2 + 0.8*(x1*x2) + np.random.normal(0, 1, n)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Additive model
mask0 = x2 == 0
mask1 = x2 == 1

axes[0].scatter(x1[mask0], y_additive[mask0], s=60, alpha=0.6, 
               label='x₂ = 0 (Control)', edgecolors='black')
axes[0].scatter(x1[mask1], y_additive[mask1], s=60, alpha=0.6, 
               label='x₂ = 1 (Treatment)', edgecolors='black')

# Fit lines
lr0 = LinearRegression().fit(x1[mask0].reshape(-1, 1), y_additive[mask0])
lr1 = LinearRegression().fit(x1[mask1].reshape(-1, 1), y_additive[mask1])

x_line = np.linspace(0, 10, 100)
axes[0].plot(x_line, lr0.predict(x_line.reshape(-1, 1)),
            'b-', linewidth=3, label=f'Slope₀ = {lr0.coef_[0]:.2f}')
axes[0].plot(x_line, lr1.predict(x_line.reshape(-1, 1)),
            'orange', linewidth=3, label=f'Slope₁ = {lr1.coef_[0]:.2f}')

axes[0].set_xlabel('x₁', fontsize=12, fontweight='bold')
axes[0].set_ylabel('y', fontsize=12, fontweight='bold')
axes[0].set_title('ADDITIVE MODEL\n' +
                 'y = α + β₁x₁ + β₂x₂\n' +
                 'Parallel lines (same slopes!)',
                 fontsize=14, fontweight='bold', color='blue')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Interactive model
axes[1].scatter(x1[mask0], y_interactive[mask0], s=60, alpha=0.6,
               label='x₂ = 0 (Control)', edgecolors='black')
axes[1].scatter(x1[mask1], y_interactive[mask1], s=60, alpha=0.6,
               label='x₂ = 1 (Treatment)', edgecolors='black')

lr0_int = LinearRegression().fit(x1[mask0].reshape(-1, 1), y_interactive[mask0])
lr1_int = LinearRegression().fit(x1[mask1].reshape(-1, 1), y_interactive[mask1])

axes[1].plot(x_line, lr0_int.predict(x_line.reshape(-1, 1)),
            'b-', linewidth=3, label=f'Slope₀ = {lr0_int.coef_[0]:.2f}')
axes[1].plot(x_line, lr1_int.predict(x_line.reshape(-1, 1)),
            'orange', linewidth=3, label=f'Slope₁ = {lr1_int.coef_[0]:.2f}')

axes[1].set_xlabel('x₁', fontsize=12, fontweight='bold')
axes[1].set_ylabel('y', fontsize=12, fontweight='bold')
axes[1].set_title('INTERACTIVE MODEL\n' +
                 'y = α + β₁x₁ + β₂x₂ + β₃(x₁×x₂)\n' +
                 'Different slopes!',
                 fontsize=14, fontweight='bold', color='red')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("=" * 70)
print("ADDITIVE vs INTERACTIVE")
print("=" * 70)
print("\nADDITIVE MODEL:")
print(f"  Control slope: {lr0.coef_[0]:.2f}")
print(f"  Treatment slope: {lr1.coef_[0]:.2f}")
print("  → Same slopes (parallel lines)")
print("  → Effect of x₁ same for both groups")

print("\nINTERACTIVE MODEL:")
print(f"  Control slope: {lr0_int.coef_[0]:.2f}")
print(f"  Treatment slope: {lr1_int.coef_[0]:.2f}")
print("  → Different slopes!")
print("  → Effect of x₁ depends on x₂")
print("=" * 70)
```

### 1.2. Mathematical Form

**Additive**:
$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \epsilon
$$

**Interactive**:
$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \beta_3 (x_1 \times x_2) + \epsilon
$$

**Interpretation của $$\beta_3$$**:
- $$\beta_3$$ = change in slope of $$x_1$$ khi $$x_2$$ tăng 1 đơn vị
- Hoặc: change in slope of $$x_2$$ khi $$x_1$$ tăng 1 đơn vị
- **Symmetric**: interaction giữa $$x_1$$ và $$x_2$$ = interaction giữa $$x_2$$ và $$x_1$$

## 2. Bayesian Interaction Model trong PyMC

```python
import pymc as pm
import arviz as az

# Standardize predictors
x1_z = (x1 - x1.mean()) / x1.std()
x2_z = x2  # Binary, no need to standardize
y_z = (y_interactive - y_interactive.mean()) / y_interactive.std()

# Interaction term
interaction = x1_z * x2_z

# Fit model
with pm.Model() as model_interaction:
    # Priors
    alpha = pm.Normal('alpha', 0, 1)
    beta1 = pm.Normal('beta1', 0, 1)  # Main effect of x1
    beta2 = pm.Normal('beta2', 0, 1)  # Main effect of x2
    beta3 = pm.Normal('beta3', 0, 1)  # Interaction effect
    sigma = pm.HalfNormal('sigma', 1)
    
    # Linear model with interaction
    mu = alpha + beta1*x1_z + beta2*x2_z + beta3*interaction
    
    # Likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    # Sample
    trace = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                         return_inferencedata=True)

# Summary
print("\n" + "=" * 70)
print("POSTERIOR SUMMARY")
print("=" * 70)
summary = az.summary(trace, var_names=['alpha', 'beta1', 'beta2', 'beta3'])
print(summary)
print("=" * 70)

# Visualize posteriors
az.plot_posterior(trace, var_names=['beta1', 'beta2', 'beta3'],
                 figsize=(16, 5))
plt.suptitle('Posterior Distributions', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# Extract
beta3_samples = trace.posterior['beta3'].values.flatten()

print("\nINTERACTION EFFECT (β₃):")
print(f"  Mean: {beta3_samples.mean():.3f}")
print(f"  95% CI: [{np.percentile(beta3_samples, 2.5):.3f}, " +
      f"{np.percentile(beta3_samples, 97.5):.3f}]")

if np.percentile(beta3_samples, 2.5) > 0:
    print("  → Significant positive interaction!")
    print("  → Effect of x₁ stronger when x₂ = 1")
elif np.percentile(beta3_samples, 97.5) < 0:
    print("  → Significant negative interaction!")
    print("  → Effect of x₁ weaker when x₂ = 1")
else:
    print("  → No clear interaction (CI includes 0)")
```

## 3. Interpretation: Conditional Effects

Với interaction, effect của $$x_1$$ phụ thuộc vào $$x_2$$:

$$
\frac{\partial y}{\partial x_1} = \beta_1 + \beta_3 x_2
$$

**Khi $$x_2 = 0$$** (control):
$$
\frac{\partial y}{\partial x_1} = \beta_1
$$

**Khi $$x_2 = 1$$** (treatment):
$$
\frac{\partial y}{\partial x_1} = \beta_1 + \beta_3
$$

```python
# Compute conditional effects
beta1_samples = trace.posterior['beta1'].values.flatten()
beta3_samples = trace.posterior['beta3'].values.flatten()

# Effect of x1 when x2=0
effect_x2_0 = beta1_samples

# Effect of x1 when x2=1
effect_x2_1 = beta1_samples + beta3_samples

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Conditional effects
axes[0].hist(effect_x2_0, bins=50, density=True, alpha=0.7,
            label='x₂ = 0 (Control)', edgecolor='black')
axes[0].hist(effect_x2_1, bins=50, density=True, alpha=0.7,
            label='x₂ = 1 (Treatment)', edgecolor='black')
axes[0].axvline(effect_x2_0.mean(), color='blue', linewidth=2, linestyle='--')
axes[0].axvline(effect_x2_1.mean(), color='orange', linewidth=2, linestyle='--')
axes[0].set_xlabel('Effect of x₁ on y', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('CONDITIONAL EFFECTS\n' +
                 f'Control: {effect_x2_0.mean():.2f}\n' +
                 f'Treatment: {effect_x2_1.mean():.2f}',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')

# Difference
difference = effect_x2_1 - effect_x2_0  # This equals beta3!
axes[1].hist(difference, bins=50, density=True, alpha=0.7,
            color='green', edgecolor='black')
axes[1].axvline(difference.mean(), color='red', linewidth=3,
               label=f'Mean = {difference.mean():.2f}')
axes[1].axvline(0, color='black', linestyle='--', linewidth=2)
axes[1].set_xlabel('Difference in Effects', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('INTERACTION = DIFFERENCE\n' +
                 'β₃ = Effect(x₂=1) - Effect(x₂=0)',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("CONDITIONAL EFFECTS")
print("=" * 70)
print(f"\nEffect of x₁ when x₂ = 0: {effect_x2_0.mean():.3f}")
print(f"Effect of x₁ when x₂ = 1: {effect_x2_1.mean():.3f}")
print(f"Difference (β₃): {difference.mean():.3f}")
print("=" * 70)
```

## 4. Khi nào Cần Interactions?

### 4.1. Theory-Driven

Nếu theory gợi ý effects phụ thuộc nhau → include interaction.

### 4.2. Exploratory

Plot data by groups. Nếu slopes khác nhau → có thể cần interaction.

### 4.3. Model Comparison

So sánh model với và không có interaction (Chapter 06: Model Comparison).

## 5. Continuous × Continuous Interactions

Interactions không chỉ với binary variables:

$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \beta_3 (x_1 \times x_2) + \epsilon
$$

**Interpretation phức tạp hơn** → visualize!

```python
# Example: Continuous × Continuous
np.random.seed(42)
n = 200

x1_cont = np.random.uniform(0, 10, n)
x2_cont = np.random.uniform(0, 10, n)
y_cont = 2 + 0.5*x1_cont + 0.3*x2_cont + 0.1*(x1_cont*x2_cont) + np.random.normal(0, 2, n)

# Visualize with 3D plot
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(14, 6))

# 3D scatter
ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(x1_cont, x2_cont, y_cont, c=y_cont, cmap='viridis', s=30, alpha=0.6)
ax1.set_xlabel('x₁', fontsize=11, fontweight='bold')
ax1.set_ylabel('x₂', fontsize=11, fontweight='bold')
ax1.set_zlabel('y', fontsize=11, fontweight='bold')
ax1.set_title('Continuous × Continuous Interaction\n' +
             'y = α + β₁x₁ + β₂x₂ + β₃(x₁×x₂)',
             fontsize=13, fontweight='bold')

# Contour plot
ax2 = fig.add_subplot(122)
contour = ax2.tricontourf(x1_cont, x2_cont, y_cont, levels=15, cmap='viridis')
ax2.set_xlabel('x₁', fontsize=11, fontweight='bold')
ax2.set_ylabel('x₂', fontsize=11, fontweight='bold')
ax2.set_title('Contour Plot\nEffect depends on both x₁ and x₂',
             fontsize=13, fontweight='bold')
plt.colorbar(contour, ax=ax2, label='y')

plt.tight_layout()
plt.show()
```

## Tóm tắt và Kết nối

Interaction effects xảy ra khi effect của một predictor phụ thuộc vào predictor khác:

- **Model**: $$y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \beta_3 (x_1 \times x_2) + \epsilon$$
- **Interpretation**: $$\beta_3$$ = change in slope
- **Conditional effects**: Effect phụ thuộc vào context
- **Visualization**: Essential cho interpretation!

**Key insight**: Thế giới thực hiếm khi additive. Always consider interactions khi có theoretical reasons!

**Chapter 05 Complete!** Chúng ta đã học:
- Multiple predictors (5.1)
- Confounding & DAGs (5.2)
- Multicollinearity (5.3)
- Interactions (5.4)

Bài tiếp theo: **Chapter 06 - Model Comparison** 🚀

## Bài tập

**Bài tập 1: Detect Interaction**
Generate data với và không có interaction. Visualize và identify which is which.

**Bài tập 2: Fit và Interpret**
Fit interaction model. Compute conditional effects cho different values of $$x_2$$.

**Bài tập 3: Continuous × Continuous**
Fit model với continuous × continuous interaction. Visualize với contour plot.

**Bài tập 4: Real Example**
Scenario: Effect of study time on test score, với prior knowledge.
(a) Argue why interaction makes sense
(b) Fit model
(c) Interpret results

**Bài tập 5: Model Comparison**
Compare additive vs interactive model. Which fits better? (Hint: use posterior predictive checks)

## Tài liệu Tham khảo

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.
- Chapter 4: Linear regression - interactions

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 8: Conditional Manatees

---

*Chương tiếp theo: [Chapter 06: Model Comparison](/vi/chapter06/)*
