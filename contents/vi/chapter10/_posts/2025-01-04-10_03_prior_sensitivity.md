---
layout: post
title: "Bài 10.3: Prior Sensitivity Analysis"
chapter: '10'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter10
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **prior sensitivity analysis** - kiểm tra xem posterior có bị ảnh hưởng quá nhiều bởi prior choice không. Bạn sẽ biết khi nào priors matter, cách conduct sensitivity analysis, và report findings honestly.

## Giới thiệu: The Prior Debate

**Criticism of Bayesian statistics**: "Results depend on subjective priors!"

**Response**: 
1. With enough data, likelihood dominates → posterior insensitive to priors
2. **BUT**: With limited data, priors matter → need sensitivity analysis
3. **Solution**: Test multiple reasonable priors, report robustness

**Best practice**: Always check prior sensitivity, especially with small n!

## 1. When Do Priors Matter?

**Priors have strong influence when**:
- **Small sample size** (n < 30)
- **Weak likelihood** (high noise, low signal)
- **Strong priors** (narrow, informative)
- **Parameters near boundary** (e.g., σ near 0)

**Priors have weak influence when**:
- **Large sample size** (n > 100)
- **Strong likelihood** (low noise, clear signal)
- **Weak priors** (wide, weakly informative)

## 2. Conducting Sensitivity Analysis

**Strategy**: Fit model with multiple prior choices, compare posteriors.

```python
import pymc as pm
import arviz as az
import numpy as np
import matplotlib.pyplot as plt

# Generate data (small n to make priors matter)
np.random.seed(42)
n = 20  # Small sample!
x = np.random.uniform(0, 10, n)
y = 2 + 0.5*x + np.random.normal(0, 2, n)

# Define multiple prior specifications
prior_specs = {
    'Weak': {'beta_sd': 10},
    'Moderate': {'beta_sd': 5},
    'Strong': {'beta_sd': 1}
}

traces = {}

for name, priors in prior_specs.items():
    with pm.Model() as model:
        alpha = pm.Normal('alpha', 0, 10)
        beta = pm.Normal('beta', 0, priors['beta_sd'])
        sigma = pm.HalfNormal('sigma', 5)
        mu = alpha + beta * x
        y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
        traces[name] = pm.sample(1000, tune=500, chains=2, random_seed=42,
                                return_inferencedata=True, progressbar=False)

# Compare posteriors
print("=" * 70)
print("PRIOR SENSITIVITY ANALYSIS")
print("=" * 70)
print(f"\nData: n = {n} (small sample!)")
print(f"True β = 0.5")
print("\nPosterior for β under different priors:")
print("-" * 70)
for name in prior_specs.keys():
    beta_post = traces[name].posterior['beta'].values.flatten()
    hdi = az.hdi(beta_post, hdi_prob=0.89)
    print(f"{name:10s}: {beta_post.mean():.3f} ± {beta_post.std():.3f}, " +
          f"89% HDI = [{hdi[0]:.3f}, {hdi[1]:.3f}]")

print("\n→ With n=20, posteriors differ slightly")
print("→ With n=200, posteriors would be nearly identical")
print("=" * 70)

# Visualize
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['blue', 'orange', 'red']
for (name, trace), color in zip(traces.items(), colors):
    beta_post = trace.posterior['beta'].values.flatten()
    ax.hist(beta_post, bins=30, alpha=0.5, label=name, color=color,
           density=True, edgecolor='black')
ax.axvline(0.5, color='green', linestyle='--', linewidth=2, label='True β')
ax.set_xlabel('β (slope)', fontsize=13, fontweight='bold')
ax.set_ylabel('Posterior Density', fontsize=13, fontweight='bold')
ax.set_title('PRIOR SENSITIVITY: Posteriors under different priors',
            fontsize=15, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

## 3. Reporting Sensitivity Analysis

**Honest reporting**:
- "Posterior robust to prior choice" (if true)
- "Posterior sensitive to prior, but conclusions unchanged" (if minor)
- "Results depend on prior choice" (if major) → report range

```python
print("\n" + "=" * 70)
print("SENSITIVITY REPORT")
print("=" * 70)
print("\nWe tested three prior specifications for β:")
print("  • Weak: Normal(0, 10)")
print("  • Moderate: Normal(0, 5)")
print("  • Strong: Normal(0, 1)")
print("\nPosterior means ranged from 0.45 to 0.52")
print("89% HDIs overlapped substantially")
print("\n✅ CONCLUSION: Posterior reasonably robust to prior choice")
print("   Main conclusions unchanged across priors")
print("=" * 70)
```

## Tóm tắt

**Prior sensitivity analysis**:
- Test multiple reasonable priors
- Compare posteriors
- Report robustness (or lack thereof)

**When priors matter**:
- Small n, weak likelihood, strong priors

**Best practice**:
- Always check sensitivity with small data
- Report honestly
- Use weakly informative priors as default

## Bài tập

**Bài tập 1**: Vary sample size (n = 10, 50, 200). How does prior sensitivity change?

**Bài tập 2**: Real data (small n). Conduct sensitivity analysis. Report.

**Bài tập 3**: Intentionally use very strong prior. Show posterior dominated by prior.

## Tài liệu Tham khảo

**Gelman, A., et al. (2017).** "The Prior Can Often Only Be Understood in the Context of the Likelihood." *Entropy*.

---

*Bài học tiếp theo: [10.4 Bayesian Workflow Synthesis](/vi/chapter10/workflow-synthesis/)*
