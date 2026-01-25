---
layout: post
title: "Bài 9.1: Hierarchical Models - Khi Dữ liệu Có Cấu trúc Nhóm"
chapter: '09'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter09
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu sâu về **hierarchical models** (còn gọi là multilevel models hay mixed-effects models) - một trong những công cụ mạnh mặ nhất trong Bayesian statistics. Bạn sẽ hiểu tại sao grouped data cần hierarchical structure, khái niệm partial pooling, và hiện tượng shrinkage. Quan trọng hơn, bạn sẽ thấy hierarchical models không chỉ là kỹ thuật thống kê, mà là cách tự nhiên để mô hình hóa thế giới có cấu trúc phân cấp.

## Giới thiệu: Vấn đề Thực tế với Grouped Data

### Câu chuyện Động lực

Hãy tưởng tượng bạn là nhà nghiên cứu giáo dục, được giao nhiệm vụ đánh giá hiệu quả của một chương trình can thiệp mới nhằm cải thiện điểm thi toán cho học sinh trung học. Chương trình này được triển khai ở **10 trường học** khác nhau trong thành phố. Sau một năm, bạn thu thập được điểm thi của học sinh từ các trường này.

**Dữ liệu của bạn có structure**:
- **Level 1** (Observation level): Mỗi học sinh có một điểm thi
- **Level 2** (Group level): Các học sinh được nhóm theo trường học
- Mỗi trường có **số lượng học sinh khác nhau**: Trường A có 50 học sinh, trường B chỉ có 8 học sinh, trường C có 35 học sinh, v.v.

**Câu hỏi nghiên cứu**: Chương trình can thiệp có hiệu quả không? Hiệu quả có khác nhau giữa các trường không?

**Thách thức**: Làm sao bạn estimate effect cho mỗi trường một cách hợp lý, đặc biệt khi:
- Một số trường có **sample size rất nhỏ** (8 học sinh)
- Một số trường có **sample size lớn** (50 học sinh)
- Các trường có thể có **true effects khác nhau** (do quality of teachers, student demographics, etc.)

Đây chính là lúc **hierarchical models** tỏa sáng.

## 1. Ba Cách Tiếp cận: Complete, No, và Partial Pooling

Trước khi đi vào hierarchical models, hãy xem xét ba cách tiếp cận khác nhau để phân tích grouped data. Chúng ta sẽ thấy hai cách đầu tiên có vấn đề nghiêm trọng, và cách thứ ba (partial pooling) là giải pháp tối ưu.

### 1.1. Tạo Dữ liệu Mô phỏng

Để minh họa rõ ràng, chúng ta sẽ tạo synthetic data với known true effects, sau đó so sánh các phương pháp.

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
import pandas as pd

# Set seed for reproducibility
np.random.seed(42)

# Thiết lập: 10 trường học
n_schools = 10

# True effects cho mỗi trường (unknown trong thực tế)
# Giả sử population mean = 8, between-school SD = 2
true_population_mean = 8.0
true_between_school_sd = 2.0
true_effects = np.random.normal(true_population_mean, 
                                true_between_school_sd, 
                                n_schools)

# Sample sizes khác nhau cho mỗi trường (realistic)
sample_sizes = np.array([8, 12, 15, 20, 25, 30, 35, 40, 45, 50])

# Within-school SD (measurement noise)
true_within_school_sd = 3.0

# Generate observations
schools = []
scores = []
for j in range(n_schools):
    n_j = sample_sizes[j]
    # Học sinh ở trường j có scores ~ Normal(true_effects[j], 3)
    school_scores = np.random.normal(true_effects[j], 
                                     true_within_school_sd, 
                                     n_j)
    schools.extend([j] * n_j)
    scores.extend(school_scores)

schools = np.array(schools)
scores = np.array(scores)

# Tạo DataFrame để dễ visualize
df = pd.DataFrame({
    'school': schools,
    'score': scores
})

print("=" * 70)
print("DỮ LIỆU MÔ PHỎNG: 10 TRƯỜNG HỌC")
print("=" * 70)
print(f"\nTrue population mean: {true_population_mean:.2f}")
print(f"True between-school SD: {true_between_school_sd:.2f}")
print(f"True within-school SD: {true_within_school_sd:.2f}")
print("\nChi tiết từng trường:")
print("-" * 70)
print(f"{'School':<8} {'n':<6} {'Observed Mean':<15} {'True Effect':<12}")
print("-" * 70)
for j in range(n_schools):
    mask = schools == j
    obs_mean = scores[mask].mean()
    print(f"{j:<8} {sample_sizes[j]:<6} {obs_mean:<15.2f} {true_effects[j]:<12.2f}")
print("=" * 70)
```

**Output mẫu**:
```
======================================================================
DỮ LIỆU MÔ PHỎNG: 10 TRƯỜNG HỌC
======================================================================

True population mean: 8.00
True between-school SD: 2.00
True within-school SD: 3.00

Chi tiết từng trường:
----------------------------------------------------------------------
School   n      Observed Mean   True Effect 
----------------------------------------------------------------------
0        8      7.23            6.99        
1        12     9.45            9.82        
2        15     8.12            7.87        
3        20     10.34           10.15       
4        25     6.78            6.45        
5        30     8.91            8.76        
6        35     7.45            7.32        
7        40     9.12            8.98        
8        45     5.89            6.12        
9        50     10.23           10.01       
======================================================================
```

**Quan sát quan trọng**:
- Trường 0 chỉ có 8 học sinh → observed mean có thể không chính xác
- Trường 9 có 50 học sinh → observed mean gần với true effect hơn
- Có variability giữa các trường (true effects từ ~6 đến ~10)

### 1.2. Approach 1: Complete Pooling (Bỏ qua Nhóm)

**Ý tưởng**: Treat tất cả observations như đến từ một population duy nhất, **bỏ qua** thông tin về trường học.

**Model**:
$$
y_i \sim \text{Normal}(\mu, \sigma)
$$

Chỉ có một mean $$\mu$$ cho tất cả học sinh, bất kể trường nào.

```python
# Complete pooling: Tính mean và SD cho toàn bộ data
pooled_mean = scores.mean()
pooled_std = scores.std()

print("\n" + "=" * 70)
print("APPROACH 1: COMPLETE POOLING")
print("=" * 70)
print(f"\nEstimated overall mean: {pooled_mean:.2f}")
print(f"Estimated overall SD: {pooled_std:.2f}")
print(f"\n→ Tất cả trường đều được gán cùng một estimate: {pooled_mean:.2f}")
print("\n❌ VẤN ĐỀ:")
print("   • Bỏ qua differences giữa các trường")
print("   • Không capture heterogeneity")
print("   • Underfit: Model quá đơn giản")
print("   • Không trả lời câu hỏi: 'Trường nào tốt hơn?'")
print("=" * 70)
```

**Vấn đề**:
- **Underfitting**: Model quá đơn giản, không capture được variability giữa các trường
- **Loss of information**: Bỏ qua group structure
- **Không realistic**: Giả định tất cả trường giống hệt nhau

### 1.3. Approach 2: No Pooling (Ước lượng Riêng biệt)

**Ý tưởng**: Fit **separate model** cho mỗi trường, hoàn toàn **độc lập**.

**Model**:
$$
y_{ij} \sim \text{Normal}(\theta_j, \sigma)
$$

Mỗi trường $$j$$ có riêng mean $$\theta_j$$, không có connection giữa các trường.

```python
# No pooling: Tính separate mean cho mỗi trường
no_pool_means = []
no_pool_stds = []

print("\n" + "=" * 70)
print("APPROACH 2: NO POOLING")
print("=" * 70)
print("\nEstimates cho từng trường (mean ± SE):")
print("-" * 70)
print(f"{'School':<8} {'n':<6} {'Estimate':<15} {'SE':<10} {'True':<10}")
print("-" * 70)

for j in range(n_schools):
    mask = schools == j
    school_scores = scores[mask]
    mean_j = school_scores.mean()
    se_j = school_scores.std() / np.sqrt(sample_sizes[j])
    
    no_pool_means.append(mean_j)
    no_pool_stds.append(se_j)
    
    print(f"{j:<8} {sample_sizes[j]:<6} {mean_j:<15.2f} {se_j:<10.2f} {true_effects[j]:<10.2f}")

no_pool_means = np.array(no_pool_means)
no_pool_stds = np.array(no_pool_stds)

print("\n❌ VẤN ĐỀ:")
print("   • Trường có n nhỏ → SE rất lớn → Estimate không reliable")
print("   • Không 'borrow strength' từ các trường khác")
print("   • Overfit: Quá tin vào data từ small groups")
print("   • Extreme estimates cho small schools")
print("=" * 70)
```

**Output mẫu**:
```
======================================================================
APPROACH 2: NO POOLING
======================================================================

Estimates cho từng trường (mean ± SE):
----------------------------------------------------------------------
School   n      Estimate        SE         True      
----------------------------------------------------------------------
0        8      7.23            1.06       6.99      
1        12     9.45            0.87       9.82      
2        15     8.12            0.77       7.87      
3        20     10.34           0.67       10.15     
4        25     6.78            0.60       6.45      
5        30     8.91            0.55       8.76      
6        35     7.45            0.51       7.32      
7        40     9.12            0.47       8.98      
8        45     5.89            0.45       6.12      
9        50     10.23           0.42       10.01     

❌ VẤN ĐỀ:
   • Trường có n nhỏ → SE rất lớn → Estimate không reliable
   • Không 'borrow strength' từ các trường khác
   • Overfit: Quá tin vào data từ small groups
   • Extreme estimates cho small schools
======================================================================
```

**Vấn đề**:
- **High uncertainty** cho small groups (School 0: SE = 1.06)
- **Overfitting**: Estimates có thể quá extreme cho small schools
- **No information sharing**: Trường A không học gì từ trường B

### 1.4. Visualize So sánh Complete vs No Pooling

```python
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Complete Pooling
axes[0].axhline(pooled_mean, color='red', linewidth=3, 
               label='Complete pooling estimate', zorder=2)
axes[0].scatter(range(n_schools), true_effects, s=150, color='green',
               label='True effects', zorder=5, edgecolors='black', 
               marker='*', linewidths=2)
for j in range(n_schools):
    axes[0].text(j, true_effects[j] + 0.3, f'n={sample_sizes[j]}',
                ha='center', fontsize=9, fontweight='bold')
axes[0].set_xlabel('School', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Test Score', fontsize=13, fontweight='bold')
axes[0].set_title('COMPLETE POOLING\n❌ Ignores school differences',
                 fontsize=15, fontweight='bold', color='darkred')
axes[0].legend(fontsize=11, loc='upper left')
axes[0].grid(alpha=0.3, linestyle='--')
axes[0].set_ylim(4, 12)

# Plot 2: No Pooling
axes[1].errorbar(range(n_schools), no_pool_means, yerr=no_pool_stds*1.96,
                fmt='o', capsize=5, markersize=10, linewidth=2,
                label='No pooling estimates (95% CI)', color='orange')
axes[1].scatter(range(n_schools), true_effects, s=150, color='green',
               label='True effects', zorder=5, edgecolors='black',
               marker='*', linewidths=2)
for j in range(n_schools):
    axes[1].text(j, true_effects[j] + 0.3, f'n={sample_sizes[j]}',
                ha='center', fontsize=9, fontweight='bold')
axes[1].set_xlabel('School', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Test Score', fontsize=13, fontweight='bold')
axes[1].set_title('NO POOLING\n❌ High uncertainty for small schools',
                 fontsize=15, fontweight='bold', color='darkorange')
axes[1].legend(fontsize=11, loc='upper left')
axes[1].grid(alpha=0.3, linestyle='--')
axes[1].set_ylim(4, 12)

plt.tight_layout()
plt.savefig('pooling_comparison.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n→ Cả hai approaches đều có vấn đề!")
print("→ Chúng ta cần một giải pháp BALANCED...")
```

## 2. Hierarchical Model: Partial Pooling - The Best of Both Worlds

**Ý tưởng then chốt**: Các trường khác nhau, nhưng chúng **không hoàn toàn độc lập**. Chúng đều là trường học trong cùng một thành phố, cùng một hệ thống giáo dục, nên chúng có **something in common**.

**Hierarchical model** mô hình hóa điều này bằng cách giả định:
- Mỗi trường có **own effect** $$\theta_j$$
- Nhưng các effects này đến từ một **common distribution**: $$\theta_j \sim \text{Normal}(\mu, \tau)$$

### 2.1. Model Structure

**Hierarchical model** có **nhiều levels**:

**Level 1 (Observation level)**: Điểm của học sinh
$$
y_{ij} \sim \text{Normal}(\theta_j, \sigma)
$$
- $$y_{ij}$$: Score của học sinh $$i$$ ở trường $$j$$
- $$\theta_j$$: True effect của trường $$j$$
- $$\sigma$$: Within-school variability (measurement noise)

**Level 2 (Group level)**: School effects
$$
\theta_j \sim \text{Normal}(\mu, \tau)
$$
- $$\theta_j$$: Effect của trường $$j$$ (random variable!)
- $$\mu$$: **Population mean** (average effect across all schools)
- $$\tau$$: **Between-school SD** (얼마나 schools vary?)

**Level 3 (Population level)**: Hyperpriors
$$
\begin{align}
\mu &\sim \text{Normal}(0, 10) \\
\tau &\sim \text{HalfNormal}(5) \\
\sigma &\sim \text{HalfNormal}(5)
\end{align}
$$

**Interpretation**:
- $$\mu$$: "Average school effect in the population"
- $$\tau$$: "How much schools differ from each other"
- $$\sigma$$: "How much students differ within a school"

### 2.2. Fit Hierarchical Model với PyMC

```python
# Hierarchical model
with pm.Model() as hierarchical_model:
    # Level 3: Hyperpriors (population parameters)
    mu = pm.Normal('mu', mu=0, sigma=10)  # Population mean
    tau = pm.HalfNormal('tau', sigma=5)   # Between-school SD
    
    # Level 2: School-level parameters
    # theta[j] ~ Normal(mu, tau) for j = 0, 1, ..., 9
    theta = pm.Normal('theta', mu=mu, sigma=tau, shape=n_schools)
    
    # Level 1: Observation-level
    sigma = pm.HalfNormal('sigma', sigma=5)  # Within-school SD
    y_obs = pm.Normal('y_obs', mu=theta[schools], sigma=sigma, 
                     observed=scores)
    
    # Sample posterior
    trace = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                     return_inferencedata=True, 
                     target_accept=0.95)

# Diagnostics
print("\n" + "=" * 70)
print("MCMC DIAGNOSTICS")
print("=" * 70)
print(az.summary(trace, var_names=['mu', 'tau', 'sigma', 'theta']))
print("=" * 70)
```

### 2.3. Extract và Interpret Results

```python
# Extract posterior samples
theta_samples = trace.posterior['theta'].values.reshape(-1, n_schools)
theta_means = theta_samples.mean(axis=0)
theta_stds = theta_samples.std(axis=0)
theta_hdi = az.hdi(trace, var_names=['theta'], hdi_prob=0.89)

mu_samples = trace.posterior['mu'].values.flatten()
mu_mean = mu_samples.mean()
mu_std = mu_samples.std()

tau_samples = trace.posterior['tau'].values.flatten()
tau_mean = tau_samples.mean()
tau_std = tau_samples.std()

sigma_mean = trace.posterior['sigma'].values.flatten().mean()

print("\n" + "=" * 70)
print("HIERARCHICAL MODEL RESULTS (Partial Pooling)")
print("=" * 70)
print(f"\n📊 POPULATION-LEVEL PARAMETERS:")
print(f"   μ (population mean): {mu_mean:.2f} ± {mu_std:.2f}")
print(f"      [True value: {true_population_mean:.2f}]")
print(f"   τ (between-school SD): {tau_mean:.2f} ± {tau_std:.2f}")
print(f"      [True value: {true_between_school_sd:.2f}]")
print(f"   σ (within-school SD): {sigma_mean:.2f}")
print(f"      [True value: {true_within_school_sd:.2f}]")

print(f"\n🏫 SCHOOL-LEVEL ESTIMATES:")
print("-" * 70)
print(f"{'School':<8} {'n':<6} {'Partial Pool':<15} {'No Pool':<15} {'True':<10}")
print("-" * 70)
for j in range(n_schools):
    print(f"{j:<8} {sample_sizes[j]:<6} " +
          f"{theta_means[j]:<15.2f} " +
          f"{no_pool_means[j]:<15.2f} " +
          f"{true_effects[j]:<10.2f}")

print("\n✅ QUAN SÁT:")
print("   • Partial pooling estimates gần true values hơn no pooling")
print("   • Đặc biệt tốt cho small schools (n=8, 12, 15)")
print("   • Uncertainty được quantify properly")
print("=" * 70)
```

## 3. Shrinkage: Hiện tượng Kỳ diệu của Partial Pooling

**Shrinkage** là hiện tượng then chốt của hierarchical models: Estimates cho small groups được **"kéo về"** (shrink toward) population mean.

### 3.1. Quantify Shrinkage

```python
# Tính shrinkage: Khoảng cách từ no-pooling đến partial-pooling
shrinkage = np.abs(no_pool_means - theta_means)

print("\n" + "=" * 70)
print("SHRINKAGE ANALYSIS")
print("=" * 70)
print(f"{'School':<8} {'n':<6} {'No Pool':<12} {'→':<3} {'Partial Pool':<12} {'Shrinkage':<12}")
print("-" * 70)
for j in range(n_schools):
    direction = "←" if no_pool_means[j] > theta_means[j] else "→"
    print(f"{j:<8} {sample_sizes[j]:<6} {no_pool_means[j]:<12.2f} {direction:<3} " +
          f"{theta_means[j]:<12.2f} {shrinkage[j]:<12.2f}")

print(f"\n→ Correlation between sample size and shrinkage:")
corr = np.corrcoef(sample_sizes, shrinkage)[0, 1]
print(f"   r = {corr:.3f}")
print(f"\n✅ SMALLER n → MORE SHRINKAGE!")
print("=" * 70)
```

### 3.2. Visualize Shrinkage Effect

```python
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: All three approaches comparison
axes[0, 0].scatter(range(n_schools), true_effects, s=200, color='green',
                  label='True effects', zorder=5, edgecolors='black', 
                  marker='*', linewidths=2)
axes[0, 0].scatter(range(n_schools), [pooled_mean]*n_schools, s=120,
                  label='Complete pooling', alpha=0.7, 
                  edgecolors='black', linewidths=1.5)
axes[0, 0].scatter(range(n_schools), no_pool_means, s=120,
                  label='No pooling', alpha=0.7,
                  edgecolors='black', linewidths=1.5)
axes[0, 0].scatter(range(n_schools), theta_means, s=120,
                  label='Partial pooling (Hierarchical)', alpha=0.7,
                  edgecolors='black', linewidths=1.5, color='purple')
axes[0, 0].axhline(mu_mean, color='red', linestyle='--', linewidth=2,
                  alpha=0.7, label=f'Population mean (μ={mu_mean:.2f})')
axes[0, 0].set_xlabel('School', fontsize=13, fontweight='bold')
axes[0, 0].set_ylabel('Test Score', fontsize=13, fontweight='bold')
axes[0, 0].set_title('COMPARISON: Three Approaches',
                    fontsize=15, fontweight='bold')
axes[0, 0].legend(fontsize=10, loc='upper left')
axes[0, 0].grid(alpha=0.3, linestyle='--')

# Plot 2: Shrinkage visualization (arrows)
for j in range(n_schools):
    # Arrow from no-pooling to partial-pooling
    axes[0, 1].annotate('', xy=(theta_means[j], j), 
                       xytext=(no_pool_means[j], j),
                       arrowprops=dict(arrowstyle='->', lw=2, 
                                     color='blue', alpha=0.6))
    axes[0, 1].scatter(no_pool_means[j], j, s=120, color='orange',
                      edgecolors='black', zorder=3, linewidths=1.5)
    axes[0, 1].scatter(theta_means[j], j, s=120, color='purple',
                      edgecolors='black', zorder=3, linewidths=1.5)
    axes[0, 1].scatter(true_effects[j], j, s=180, color='green',
                      marker='*', edgecolors='black', zorder=4, linewidths=2)
    # Annotate sample size
    axes[0, 1].text(no_pool_means[j] - 0.5, j, f'n={sample_sizes[j]}',
                   ha='right', va='center', fontsize=9, fontweight='bold')

axes[0, 1].axvline(mu_mean, color='red', linestyle='--', linewidth=2,
                  label=f'Population mean (μ={mu_mean:.2f})', alpha=0.7)
axes[0, 1].set_xlabel('Test Score', fontsize=13, fontweight='bold')
axes[0, 1].set_ylabel('School', fontsize=13, fontweight='bold')
axes[0, 1].set_title('SHRINKAGE: No Pooling → Partial Pooling',
                    fontsize=15, fontweight='bold')
axes[0, 1].legend(['Pop. mean', 'No pooling', 'Partial pooling', 'True'],
                 fontsize=10, loc='upper right')
axes[0, 1].grid(alpha=0.3, linestyle='--')

# Plot 3: Shrinkage vs Sample Size
axes[1, 0].scatter(sample_sizes, shrinkage, s=150, alpha=0.7,
                  edgecolors='black', linewidths=1.5)
for j in range(n_schools):
    axes[1, 0].text(sample_sizes[j] + 1, shrinkage[j], f'{j}',
                   fontsize=10, fontweight='bold')
# Fit line
z = np.polyfit(sample_sizes, shrinkage, 1)
p = np.poly1d(z)
axes[1, 0].plot(sample_sizes, p(sample_sizes), "r--", linewidth=2, alpha=0.7)
axes[1, 0].set_xlabel('Sample Size (n)', fontsize=13, fontweight='bold')
axes[1, 0].set_ylabel('Shrinkage Amount', fontsize=13, fontweight='bold')
axes[1, 0].set_title(f'Shrinkage vs Sample Size (r={corr:.3f})',
                    fontsize=15, fontweight='bold')
axes[1, 0].grid(alpha=0.3, linestyle='--')

# Plot 4: Posterior distributions for selected schools
selected_schools = [0, 4, 9]  # Small, medium, large
colors = ['red', 'orange', 'blue']
for idx, j in enumerate(selected_schools):
    theta_j_samples = trace.posterior['theta'].values[:, :, j].flatten()
    axes[1, 1].hist(theta_j_samples, bins=50, alpha=0.5, 
                   label=f'School {j} (n={sample_sizes[j]})',
                   color=colors[idx], density=True, edgecolor='black')
    axes[1, 1].axvline(theta_means[j], color=colors[idx], 
                      linestyle='--', linewidth=2)
    axes[1, 1].axvline(true_effects[j], color=colors[idx], 
                      linestyle=':', linewidth=2, alpha=0.7)

axes[1, 1].axvline(mu_mean, color='black', linestyle='--', 
                  linewidth=2, label='Population mean')
axes[1, 1].set_xlabel('Test Score (θ)', fontsize=13, fontweight='bold')
axes[1, 1].set_ylabel('Posterior Density', fontsize=13, fontweight='bold')
axes[1, 1].set_title('Posterior Distributions: Small vs Large Schools',
                    fontsize=15, fontweight='bold')
axes[1, 1].legend(fontsize=10)
axes[1, 1].grid(alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('hierarchical_shrinkage.png', dpi=150, bbox_inches='tight')
plt.show()
```

### 3.3. Giải thích Shrinkage

**Tại sao shrinkage xảy ra?**

Hierarchical model **combines two sources of information**:
1. **Data from the school itself** (likelihood)
2. **Information from other schools** (prior $$\theta_j \sim \text{Normal}(\mu, \tau)$$)

**Bayesian updating**:
$$
\text{Posterior} \propto \text{Likelihood} \times \text{Prior}
$$

- **School với n lớn**: Likelihood mạnh → posterior gần với observed data → ít shrinkage
- **School với n nhỏ**: Likelihood yếu → prior có ảnh hưởng lớn → nhiều shrinkage về $$\mu$$

**Analogy**: Bạn đánh giá một nhà hàng mới:
- Nếu bạn đã ăn ở đó **50 lần** (n lớn) → bạn tin vào kinh nghiệm của mình
- Nếu bạn chỉ ăn **1 lần** (n nhỏ) → bạn sẽ tham khảo reviews chung (population mean)

## 4. Tại sao Hierarchical Models Tốt hơn?

### 4.1. Benefits

**1. Regularization tự động**:
- Prevents overfitting cho small groups
- Extreme estimates được "kéo về" reasonable values

**2. Borrowing strength**:
- Small groups học từ large groups
- Information sharing across groups

**3. Proper uncertainty quantification**:
- Accounts for both within-group và between-group variability
- Credible intervals realistic hơn

**4. Interpretability**:
- Population-level effects ($$\mu, \tau$$)
- Group-level effects ($$\theta_j$$)
- Có thể answer nhiều types of questions

**5. Prediction cho new groups**:
- Có thể predict cho trường mới (chưa có data)
- Use posterior của $$\mu, \tau$$

### 4.2. Khi nào dùng Hierarchical Models?

✅ **Dùng khi**:
- Data có **group structure** (students in schools, patients in hospitals, measurements over time)
- **Repeated measures** (multiple observations per subject)
- **Small sample sizes** cho một số groups
- Muốn **generalize** to new groups
- Quan tâm đến **both** group-level và population-level effects

❌ **Không cần thiết khi**:
- Không có group structure
- Tất cả groups có sample size rất lớn và bằng nhau
- Chỉ quan tâm đến overall effect (không quan tâm group differences)

## 5. Predict cho New School

Một advantage lớn của hierarchical models: Có thể predict cho **new school** chưa có data!

```python
# Predict cho trường mới (School 10)
# Không có data, nhưng biết nó là một trường trong cùng population

# Posterior predictive: θ_new ~ Normal(μ, τ)
theta_new_samples = np.random.normal(mu_samples, tau_samples)

theta_new_mean = theta_new_samples.mean()
theta_new_hdi = az.hdi(theta_new_samples, hdi_prob=0.89)

print("\n" + "=" * 70)
print("PREDICTION CHO NEW SCHOOL (chưa có data)")
print("=" * 70)
print(f"\nPosterior predictive for θ_new:")
print(f"   Mean: {theta_new_mean:.2f}")
print(f"   89% HDI: [{theta_new_hdi[0]:.2f}, {theta_new_hdi[1]:.2f}]")
print(f"\n→ Best guess: Trường mới có effect ~ {theta_new_mean:.2f}")
print(f"→ Uncertainty lớn vì chưa có data!")
print("=" * 70)

# Visualize
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(theta_new_samples, bins=50, alpha=0.7, edgecolor='black', density=True)
ax.axvline(theta_new_mean, color='red', linestyle='--', linewidth=2,
          label=f'Mean: {theta_new_mean:.2f}')
ax.axvline(theta_new_hdi[0], color='blue', linestyle=':', linewidth=2)
ax.axvline(theta_new_hdi[1], color='blue', linestyle=':', linewidth=2,
          label=f'89% HDI')
ax.set_xlabel('Predicted Effect for New School', fontsize=13, fontweight='bold')
ax.set_ylabel('Posterior Density', fontsize=13, fontweight='bold')
ax.set_title('Posterior Predictive Distribution for New School',
            fontsize=15, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()
```

**Interpretation**: Không có data về trường mới, nhưng hierarchical model cho chúng ta một **reasonable prior** based on population distribution!

## Tóm tắt

Hierarchical models cho grouped data:

**Ba approaches**:
- **Complete pooling**: Bỏ qua groups → underfits
- **No pooling**: Separate estimates → overfits small groups
- **Partial pooling** (Hierarchical): ✅ Best of both worlds

**Model structure**:
- **Level 1**: Observations $$y_{ij} \sim \text{Normal}(\theta_j, \sigma)$$
- **Level 2**: Group effects $$\theta_j \sim \text{Normal}(\mu, \tau)$$
- **Level 3**: Hyperpriors on $$\mu, \tau, \sigma$$

**Shrinkage**:
- Small groups shrink more toward population mean
- Automatic regularization
- Borrowing strength across groups

**Benefits**:
- Proper uncertainty quantification
- Prevents overfitting
- Interpretable (population + group levels)
- Can predict for new groups

**Key insight**: Hierarchical models naturally balance group-specific information với population-level information. Đây là cách tự nhiên để model thế giới có structure!

## Bài tập

**Bài tập 1: Simulation Study**
Generate grouped data với different between-group variability ($$\tau$$ = 0.5, 2, 5). Fit hierarchical models. How does shrinkage change with $$\tau$$?

**Bài tập 2: Sample Size Effect**
Generate data với sample sizes từ 5 đến 100. Plot shrinkage vs sample size. At what n does shrinkage become negligible?

**Bài tập 3: Model Comparison**
Fit complete pooling, no pooling, và partial pooling models. Compare using WAIC/LOO. Which wins?

**Bài tập 4: Real Data**
Find grouped data (e.g., students in schools, patients in hospitals). Fit hierarchical model. Interpret $$\mu, \tau$$, và school-specific effects.

**Bài tập 5: Prediction**
Using your hierarchical model from Exercise 4, predict effect for a new group. Quantify uncertainty. Compare with no-pooling approach.

## Tài liệu Tham khảo

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.
- Chapters 11-13: Multilevel modeling

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 13: Models with Memory (Hierarchical models)

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 5: Hierarchical models

---

*Bài học tiếp theo: [9.2 Pooling Strategies - Eight Schools Problem](/vi/chapter09/pooling/)*
