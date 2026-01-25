---
layout: post
title: "Bài 9.3: Multilevel Regression - Varying Intercepts & Slopes"
chapter: '09'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter09
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **multilevel regression** - sự kết hợp mạnh mẽ giữa hierarchical models và regression. Bạn sẽ học cách model varying intercepts (baseline khác nhau giữa các nhóm), varying slopes (effect khác nhau giữa các nhóm), và quan trọng nhất, correlation giữa intercepts và slopes. Đây là công cụ thiết yếu cho phân tích dữ liệu có cấu trúc phức tạp.

## Giới thiệu: From Group Means to Group Regressions

### Từ Eight Schools đến Multilevel Regression

Trong Eight Schools problem (Bài 9.2), chúng ta chỉ estimate **group means** - mỗi school có một effect $$\theta_j$$, không có predictors. Đây là **varying intercepts without predictors**.

**Thực tế phức tạp hơn**: Thường có **predictors** ảnh hưởng đến outcome!

**Examples**:
- **Students in schools**: Test score ~ study time + school
  - Question: Study time effect same across schools?
- **Patients in hospitals**: Recovery time ~ treatment dose + hospital
  - Question: Treatment effect same across hospitals?
- **Products in stores**: Sales ~ price + store
  - Question: Price sensitivity same across stores?

**Multilevel regression** cho phép:
1. **Varying intercepts**: Mỗi nhóm có baseline khác nhau
2. **Varying slopes**: Effect của predictor khác nhau giữa các nhóm
3. **Correlation**: Intercepts và slopes có thể correlated

## 1. Varying Intercepts Model - Different Baselines, Same Slope

### 1.1. Motivating Example: Students in Schools

**Scenario**: Bạn nghiên cứu mối quan hệ giữa **study time** (hours/week) và **test score** cho học sinh từ 5 trường khác nhau.

**Hypothesis**:
- Study time có positive effect (more study → higher score)
- **BUT**: Schools có quality khác nhau → different baselines
- Effect của study time **same** across schools (1 hour study = same benefit everywhere)

**Model structure**:
$$
\begin{align}
y_i &\sim \text{Normal}(\mu_i, \sigma) \\
\mu_i &= \alpha_{j[i]} + \beta x_i \\
\alpha_j &\sim \text{Normal}(\mu_\alpha, \sigma_\alpha) && \text{(Varying intercepts)} \\
\beta &\sim \text{Normal}(0, 5) && \text{(Common slope)} \\
\mu_\alpha &\sim \text{Normal}(70, 20) \\
\sigma_\alpha &\sim \text{HalfNormal}(10) \\
\sigma &\sim \text{HalfNormal}(10)
\end{align}
$$

**Interpretation**:
- $$\alpha_j$$: Baseline score for school $$j$$ (when study time = 0)
- $$\beta$$: Effect of study time (same for all schools)
- $$\mu_\alpha$$: Average baseline across schools
- $$\sigma_\alpha$$: Variability in baselines

### 1.2. Generate Synthetic Data

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
import pandas as pd

# Set seed
np.random.seed(42)

# Settings
n_schools = 5
n_per_school = 30
school_names = ['Lincoln', 'Washington', 'Jefferson', 'Roosevelt', 'Kennedy']

# True parameters
true_mu_alpha = 70
true_sigma_alpha = 8
true_intercepts = np.random.normal(true_mu_alpha, true_sigma_alpha, n_schools)
true_beta = 2.5  # Same slope for all
true_sigma = 6

# Generate data
schools = []
study_time = []
test_scores = []

for j in range(n_schools):
    for i in range(n_per_school):
        schools.append(j)
        time = np.random.uniform(0, 10)
        score = true_intercepts[j] + true_beta * time + np.random.normal(0, true_sigma)
        study_time.append(time)
        test_scores.append(score)

schools = np.array(schools)
study_time = np.array(study_time)
test_scores = np.array(test_scores)

# Create DataFrame
df = pd.DataFrame({
    'school': schools,
    'school_name': [school_names[j] for j in schools],
    'study_time': study_time,
    'test_score': test_scores
})

print("=" * 70)
print("DATA: STUDENTS IN SCHOOLS")
print("=" * 70)
print(f"\nTotal students: {len(df)}")
print(f"Students per school: {n_per_school}")
print(f"\nTrue parameters:")
print(f"  Population mean baseline (μ_α): {true_mu_alpha}")
print(f"  Between-school SD (σ_α): {true_sigma_alpha}")
print(f"  Common slope (β): {true_beta}")
print(f"  Within-school SD (σ): {true_sigma}")
print("\nSchool baselines:")
for j in range(n_schools):
    print(f"  {school_names[j]}: {true_intercepts[j]:.2f}")
print("=" * 70)
```

### 1.3. Visualize Data

```python
# Visualize: Parallel lines (different intercepts, same slope)
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Raw data
ax = axes[0]
colors = plt.cm.Set2(np.linspace(0, 1, n_schools))
for j in range(n_schools):
    mask = schools == j
    ax.scatter(study_time[mask], test_scores[mask], s=60, alpha=0.6,
              label=school_names[j], edgecolors='black', linewidths=0.5,
              color=colors[j])
    # True regression line
    x_line = np.array([0, 10])
    y_line = true_intercepts[j] + true_beta * x_line
    ax.plot(x_line, y_line, '--', linewidth=2, color=colors[j], alpha=0.7)

ax.set_xlabel('Study Time (hours/week)', fontsize=13, fontweight='bold')
ax.set_ylabel('Test Score', fontsize=13, fontweight='bold')
ax.set_title('DATA: Different Baselines, Same Slope\n(True model shown)',
            fontsize=15, fontweight='bold')
ax.legend(fontsize=11, loc='upper left')
ax.grid(alpha=0.3, linestyle='--')

# Plot 2: School means
ax = axes[1]
school_means = [test_scores[schools == j].mean() for j in range(n_schools)]
school_sds = [test_scores[schools == j].std() for j in range(n_schools)]
ax.bar(range(n_schools), school_means, yerr=school_sds, capsize=5,
      alpha=0.7, edgecolor='black', linewidth=1.5, color=colors)
ax.axhline(true_mu_alpha, color='red', linestyle='--', linewidth=2,
          label=f'Population mean (μ_α={true_mu_alpha})')
ax.set_xticks(range(n_schools))
ax.set_xticklabels(school_names, rotation=15)
ax.set_ylabel('Mean Test Score', fontsize=13, fontweight='bold')
ax.set_title('School Means (ignoring study time)',
            fontsize=15, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(alpha=0.3, linestyle='--', axis='y')

plt.tight_layout()
plt.savefig('varying_intercepts_data.png', dpi=150, bbox_inches='tight')
plt.show()
```

### 1.4. Fit Varying Intercepts Model

```python
# Varying intercepts model
with pm.Model() as varying_intercepts_model:
    # Hyperpriors (population level)
    mu_alpha = pm.Normal('mu_alpha', mu=70, sigma=20)
    sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=10)
    
    # Varying intercepts (school level)
    alpha = pm.Normal('alpha', mu=mu_alpha, sigma=sigma_alpha, shape=n_schools)
    
    # Common slope
    beta = pm.Normal('beta', mu=0, sigma=5)
    
    # Observation level
    sigma = pm.HalfNormal('sigma', sigma=10)
    mu = alpha[schools] + beta * study_time
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=test_scores)
    
    # Sample
    trace_vi = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                        return_inferencedata=True, target_accept=0.95)

# Diagnostics
print("\n" + "=" * 70)
print("MCMC DIAGNOSTICS")
print("=" * 70)
print(az.summary(trace_vi, var_names=['mu_alpha', 'sigma_alpha', 'beta', 'sigma', 'alpha']))
print("=" * 70)

# Extract posteriors
alpha_post = trace_vi.posterior['alpha'].values.reshape(-1, n_schools)
beta_post = trace_vi.posterior['beta'].values.flatten()
mu_alpha_post = trace_vi.posterior['mu_alpha'].values.flatten()
sigma_alpha_post = trace_vi.posterior['sigma_alpha'].values.flatten()

print("\n" + "=" * 70)
print("VARYING INTERCEPTS MODEL RESULTS")
print("=" * 70)
print(f"\n📊 POPULATION-LEVEL:")
print(f"   μ_α (mean baseline): {mu_alpha_post.mean():.2f} ± {mu_alpha_post.std():.2f}")
print(f"      [True: {true_mu_alpha}]")
print(f"   σ_α (between-school SD): {sigma_alpha_post.mean():.2f} ± {sigma_alpha_post.std():.2f}")
print(f"      [True: {true_sigma_alpha}]")
print(f"   β (common slope): {beta_post.mean():.2f} ± {beta_post.std():.2f}")
print(f"      [True: {true_beta}]")

print(f"\n🏫 SCHOOL-LEVEL INTERCEPTS:")
print("-" * 70)
print(f"{'School':<15} {'Posterior Mean':<18} {'True':<10}")
print("-" * 70)
for j in range(n_schools):
    print(f"{school_names[j]:<15} {alpha_post[:, j].mean():<18.2f} {true_intercepts[j]:<10.2f}")

print("\n✅ INTERPRETATION:")
print(f"   • All schools have same slope: {beta_post.mean():.2f} points per hour")
print(f"   • But different baselines (intercepts)")
print(f"   • {school_names[np.argmax(alpha_post.mean(axis=0))]} has highest baseline")
print(f"   • {school_names[np.argmin(alpha_post.mean(axis=0))]} has lowest baseline")
print("=" * 70)
```

### 1.5. Visualize Posterior Predictions

```python
# Posterior predictive lines
fig, ax = plt.subplots(figsize=(12, 7))

# Plot data
for j in range(n_schools):
    mask = schools == j
    ax.scatter(study_time[mask], test_scores[mask], s=60, alpha=0.5,
              color=colors[j], edgecolors='black', linewidths=0.5)

# Plot posterior regression lines
x_line = np.linspace(0, 10, 100)
for j in range(n_schools):
    # Sample 100 posterior lines
    for i in np.random.choice(len(alpha_post), 100):
        y_line = alpha_post[i, j] + beta_post[i] * x_line
        ax.plot(x_line, y_line, color=colors[j], alpha=0.02)
    
    # Posterior mean line
    y_mean = alpha_post[:, j].mean() + beta_post.mean() * x_line
    ax.plot(x_line, y_mean, color=colors[j], linewidth=3,
           label=school_names[j])

ax.set_xlabel('Study Time (hours/week)', fontsize=13, fontweight='bold')
ax.set_ylabel('Test Score', fontsize=13, fontweight='bold')
ax.set_title('VARYING INTERCEPTS MODEL\nParallel lines (same slope, different intercepts)',
            fontsize=15, fontweight='bold')
ax.legend(fontsize=11, loc='upper left')
ax.grid(alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()
```

## 2. Varying Slopes Model - Same Baseline, Different Slopes

**Scenario**: Giờ giả sử tất cả schools có **same baseline**, nhưng **study time effect khác nhau**.

**Model**:
$$
\begin{align}
\mu_i &= \alpha + \beta_{j[i]} x_i \\
\beta_j &\sim \text{Normal}(\mu_\beta, \sigma_\beta)
\end{align}
$$

Tôi sẽ implement ngắn gọn vì pattern tương tự:

```python
# Generate data with varying slopes
np.random.seed(43)
true_alpha = 70
true_slopes = np.array([1.5, 2.0, 2.5, 3.0, 3.5])  # Different slopes

schools_vs = []
study_time_vs = []
test_scores_vs = []

for j in range(n_schools):
    for i in range(n_per_school):
        schools_vs.append(j)
        time = np.random.uniform(0, 10)
        score = true_alpha + true_slopes[j] * time + np.random.normal(0, true_sigma)
        study_time_vs.append(time)
        test_scores_vs.append(score)

schools_vs = np.array(schools_vs)
study_time_vs = np.array(study_time_vs)
test_scores_vs = np.array(test_scores_vs)

# Fit varying slopes model
with pm.Model() as varying_slopes_model:
    # Common intercept
    alpha = pm.Normal('alpha', mu=70, sigma=20)
    
    # Hyperpriors for slopes
    mu_beta = pm.Normal('mu_beta', mu=0, sigma=5)
    sigma_beta = pm.HalfNormal('sigma_beta', sigma=2)
    
    # Varying slopes
    beta = pm.Normal('beta', mu=mu_beta, sigma=sigma_beta, shape=n_schools)
    
    # Observation model
    sigma = pm.HalfNormal('sigma', sigma=10)
    mu = alpha + beta[schools_vs] * study_time_vs
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=test_scores_vs)
    
    trace_vs = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                        return_inferencedata=True, target_accept=0.95)

# Extract
beta_vs_post = trace_vs.posterior['beta'].values.reshape(-1, n_schools)

print("\n" + "=" * 70)
print("VARYING SLOPES MODEL")
print("=" * 70)
print(f"\nCommon intercept: {trace_vs.posterior['alpha'].values.flatten().mean():.2f}")
print(f"[True: {true_alpha}]")
print(f"\nSchool-specific slopes:")
for j in range(n_schools):
    print(f"  {school_names[j]}: {beta_vs_post[:, j].mean():.2f} [True: {true_slopes[j]:.2f}]")
print("\n→ Different schools have different study time effects!")
print("=" * 70)
```

## 3. Varying Intercepts AND Slopes - Most Flexible

**Key insight**: Intercepts và slopes có thể **correlated**!

**Example**: Schools với high baseline (good quality) có thể have **flatter slopes** (ceiling effect) hoặc **steeper slopes** (better teaching amplifies effort).

**Model with correlation**:
$$
\begin{bmatrix} \alpha_j \\ \beta_j \end{bmatrix} \sim \text{MVNormal}\left(
\begin{bmatrix} \mu_\alpha \\ \mu_\beta \end{bmatrix}, \Sigma
\right)
$$

where $$\Sigma$$ is covariance matrix with correlation $$\rho$$.

### 3.1. Implementation

```python
# Fit varying intercepts AND slopes (with correlation)
with pm.Model() as varying_both_model:
    # Hyperpriors for means
    mu_alpha = pm.Normal('mu_alpha', mu=70, sigma=20)
    mu_beta = pm.Normal('mu_beta', mu=0, sigma=5)
    
    # Hyperpriors for SDs
    sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=10)
    sigma_beta = pm.HalfNormal('sigma_beta', sigma=2)
    
    # Correlation
    rho = pm.Uniform('rho', lower=-1, upper=1)
    
    # Covariance matrix
    cov = pm.math.stack([[sigma_alpha**2, 
                          rho * sigma_alpha * sigma_beta],
                         [rho * sigma_alpha * sigma_beta, 
                          sigma_beta**2]])
    
    # Multivariate normal for (alpha, beta) jointly
    effects = pm.MvNormal('effects', 
                         mu=pm.math.stack([mu_alpha, mu_beta]),
                         cov=cov,
                         shape=(n_schools, 2))
    
    alpha = effects[:, 0]
    beta = effects[:, 1]
    
    # Observation model
    sigma = pm.HalfNormal('sigma', sigma=10)
    mu = alpha[schools] + beta[schools] * study_time
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=test_scores)
    
    trace_vb = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                        return_inferencedata=True, target_accept=0.95)

# Extract correlation
rho_post = trace_vb.posterior['rho'].values.flatten()

print("\n" + "=" * 70)
print("VARYING INTERCEPTS AND SLOPES (with correlation)")
print("=" * 70)
print(f"\nCorrelation (ρ): {rho_post.mean():.3f} ± {rho_post.std():.3f}")
print(f"89% HDI: {az.hdi(rho_post, hdi_prob=0.89)}")

if rho_post.mean() > 0.1:
    print("\n✅ POSITIVE CORRELATION:")
    print("   Schools with higher baselines tend to have steeper slopes")
    print("   → Good schools amplify study time effect")
elif rho_post.mean() < -0.1:
    print("\n✅ NEGATIVE CORRELATION:")
    print("   Schools with higher baselines tend to have flatter slopes")
    print("   → Ceiling effect: less room for improvement")
else:
    print("\n✅ NO CORRELATION:")
    print("   Baseline and slope are independent")
print("=" * 70)
```

### 3.2. Visualize Correlation

```python
# Visualize posterior correlation
effects_post = trace_vb.posterior['effects'].values.reshape(-1, n_schools, 2)
alpha_vb = effects_post[:, :, 0]
beta_vb = effects_post[:, :, 1]

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Posterior samples of (alpha, beta) for each school
ax = axes[0]
for j in range(n_schools):
    ax.scatter(alpha_vb[:, j], beta_vb[:, j], s=5, alpha=0.3,
              color=colors[j], label=school_names[j])
ax.set_xlabel('Intercept (α)', fontsize=13, fontweight='bold')
ax.set_ylabel('Slope (β)', fontsize=13, fontweight='bold')
ax.set_title(f'POSTERIOR: Intercepts vs Slopes\nρ = {rho_post.mean():.3f}',
            fontsize=15, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(alpha=0.3, linestyle='--')

# Plot 2: Posterior regression lines
ax = axes[1]
x_line = np.linspace(0, 10, 100)
for j in range(n_schools):
    # Sample 100 lines
    for i in np.random.choice(len(alpha_vb), 100):
        y_line = alpha_vb[i, j] + beta_vb[i, j] * x_line
        ax.plot(x_line, y_line, color=colors[j], alpha=0.02)
    
    # Posterior mean
    y_mean = alpha_vb[:, j].mean() + beta_vb[:, j].mean() * x_line
    ax.plot(x_line, y_mean, color=colors[j], linewidth=3,
           label=school_names[j])
    
    # Data
    mask = schools == j
    ax.scatter(study_time[mask], test_scores[mask], s=40, alpha=0.4,
              color=colors[j], edgecolors='black', linewidths=0.5)

ax.set_xlabel('Study Time (hours/week)', fontsize=13, fontweight='bold')
ax.set_ylabel('Test Score', fontsize=13, fontweight='bold')
ax.set_title('VARYING INTERCEPTS AND SLOPES\nNon-parallel lines',
            fontsize=15, fontweight='bold')
ax.legend(fontsize=10, loc='upper left')
ax.grid(alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('varying_both.png', dpi=150, bbox_inches='tight')
plt.show()
```

## Tóm tắt

Multilevel regression extends hierarchical models to include predictors:

**Three models**:
1. **Varying intercepts**: Different baselines, same slope
   - Use when: Groups differ in level, but effect is same
2. **Varying slopes**: Same baseline, different slopes
   - Use when: Effect differs across groups
3. **Varying both**: Most flexible, allows correlation
   - Use when: Both baselines and effects differ

**Key concepts**:
- **Partial pooling** applies to both intercepts and slopes
- **Correlation** between intercepts and slopes reveals structure
- **Shrinkage** prevents overfitting for small groups

**Applications**:
- Students in schools
- Patients in hospitals
- Products in stores
- Repeated measures (subjects over time)

**Next**: Chapter 10 - Bayesian Workflow (diagnostics, reporting, sensitivity analysis)

## Bài tập

**Bài tập 1**: Fit varying intercepts model. Interpret population mean và between-group SD.

**Bài tập 2**: Fit varying slopes model. Which group has strongest effect?

**Bài tập 3**: Fit varying both. Estimate correlation. Is it positive or negative? Interpret.

**Bài tập 4**: Real data (students in schools). Compare all three models using LOO. Which wins?

**Bài tập 5**: Predict for new group using hierarchical model. Quantify uncertainty.

## Tài liệu Tham khảo

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.
- Chapters 11-13: Multilevel regression

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 13: Models with Memory
- Chapter 14: Adventures in Covariance

---

*Chương tiếp theo: [Chapter 10: Bayesian Workflow & Best Practices](/vi/chapter10/)*
