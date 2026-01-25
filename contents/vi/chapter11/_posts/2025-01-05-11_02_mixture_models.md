---
layout: post
title: "Bài 11.2: Mixture Models - Clustering & Heterogeneity"
chapter: '11'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter11
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **finite mixture models** - powerful tool cho modeling heterogeneous populations. Bạn sẽ hiểu mixture distributions, latent class membership, và soft clustering. Đây là essential method khi data comes from multiple subpopulations.

## Giới thiệu: Heterogeneous Populations

**Problem**: Data from multiple groups, but group membership unknown.

**Examples**:
- Heights: Men vs women (but gender not recorded)
- Customers: Casual vs loyal vs churning
- Gene expression: Different cell types

**Solution**: **Mixture model** - model data as coming from K components.

## 1. Mixture Distribution

**Finite mixture**:
$$
p(y) = \sum_{k=1}^K \pi_k p_k(y | \theta_k)
$$

where:
- $$\pi_k$$: Mixing weights ($$\sum \pi_k = 1$$)
- $$p_k(y \mid \theta_k)$$: Component distributions

**Example: Mixture of 2 Normals**:
$$
y \sim \pi_1 \text{Normal}(\mu_1, \sigma_1) + \pi_2 \text{Normal}(\mu_2, \sigma_2)
$$

## 2. Latent Class Membership

**Latent variable** $$z_i \in \{1, ..., K\}$$: Which component generated $$y_i$$?

**Generative process**:
1. Sample class: $$z_i \sim \text{Categorical}(\pi)$$
2. Sample data: $$y_i \sim p_{z_i}(y \mid \theta_{z_i})$$

## 3. Mixture Model in PyMC

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az

# Generate data from 2 components
np.random.seed(42)
n1, n2 = 100, 80
y1 = np.random.normal(0, 1, n1)
y2 = np.random.normal(5, 1.5, n2)
y_data = np.concatenate([y1, y2])

# Mixture model
with pm.Model() as mixture_model:
    # Mixing weights
    π = pm.Dirichlet('π', a=np.ones(2))
    
    # Component parameters
    μ = pm.Normal('μ', mu=0, sigma=10, shape=2)
    σ = pm.HalfNormal('σ', sigma=5, shape=2)
    
    # Mixture likelihood
    components = [pm.Normal.dist(mu=μ[i], sigma=σ[i]) for i in range(2)]
    y_obs = pm.Mixture('y_obs', w=π, comp_dists=components, observed=y_data)
    
    # Sample
    trace = pm.sample(1000, tune=500, chains=2, random_seed=42,
                     return_inferencedata=True, progressbar=False)

print("=" * 70)
print("MIXTURE MODEL")
print("=" * 70)
print("\nIdentified 2 components in data")
print("Can cluster observations by posterior probability")
print("\nPosterior estimates:")
print(az.summary(trace, var_names=['π', 'μ', 'σ']))
print("=" * 70)

# Visualize
fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(y_data, bins=40, alpha=0.5, density=True, edgecolor='black',
       label='Observed data')

# Plot fitted mixture
μ_post = trace.posterior['μ'].values.reshape(-1, 2).mean(axis=0)
σ_post = trace.posterior['σ'].values.reshape(-1, 2).mean(axis=0)
π_post = trace.posterior['π'].values.reshape(-1, 2).mean(axis=0)

x_range = np.linspace(-5, 10, 200)
mixture_pdf = (π_post[0] * scipy.stats.norm.pdf(x_range, μ_post[0], σ_post[0]) +
               π_post[1] * scipy.stats.norm.pdf(x_range, μ_post[1], σ_post[1]))
ax.plot(x_range, mixture_pdf, 'r-', linewidth=3, label='Fitted mixture')

ax.set_xlabel('y', fontsize=13, fontweight='bold')
ax.set_ylabel('Density', fontsize=13, fontweight='bold')
ax.set_title('MIXTURE MODEL: Two Components Identified',
            fontsize=15, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

## Tóm tắt

**Mixture models**:
- **Heterogeneity**: Model multiple subpopulations
- **Latent classes**: Unknown group membership
- **Clustering**: Soft assignment via posterior probabilities
- **Flexibility**: Can model complex distributions
- **Challenge**: Label switching, choosing K

**Applications**: Customer segmentation, anomaly detection, density estimation.

**Key insight**: Mixture models reveal hidden structure in data!

## Bài tập

**Bài tập 1**: Fit mixture with K=2, 3, 4. Compare using LOO. Which K best?

**Bài tập 2**: Real data (e.g., Old Faithful). Fit mixture. Interpret components.

**Bài tập 3**: Cluster observations by posterior probability. Visualize.

## Tài liệu Tham khảo

**McLachlan, G., & Peel, D. (2000).** *Finite Mixture Models*. Wiley.

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 12: Monsters and Mixtures

---

**🎉🎊 COURSE COMPLETE! 🎊🎉**

**Congratulations!** Bạn đã hoàn thành toàn bộ Bayesian Statistics course!

**What you've learned**:
- Bayesian inference fundamentals
- MCMC sampling
- Regression models (linear, GLM, hierarchical)
- Model comparison & evaluation
- Bayesian workflow
- Advanced topics (GP, mixtures)

**Next steps**:
- Apply to real projects
- Read *Statistical Rethinking* (McElreath)
- Explore Stan, PyMC documentation
- Join Bayesian community!

**Thank you for learning! 🚀📊🎓**
