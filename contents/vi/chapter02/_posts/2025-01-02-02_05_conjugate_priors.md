---
layout: post
title: "Bài 2.5: Conjugate Priors - Prior Liên hợp"
chapter: '02'
order: 5
owner: Nguyen Le Linh
lang: vi
categories:
- chapter02
lesson_type: required
---

## Mục tiêu

Bài học này giải thích **conjugate priors** - các prior đặc biệt làm cho posterior có cùng dạng với prior, cho phép tính toán giải tích thay vì phải dùng phương pháp số.

## 1. Conjugate Prior là gì?

### 1.1. Định nghĩa

**Conjugate prior** là prior mà khi kết hợp với likelihood cụ thể, cho ra posterior **cùng họ phân phối** với prior.

$$\text{Prior: } p(\theta) \in \mathcal{F}$$
$$\text{Likelihood: } p(D \mid \theta)$$
$$\text{Posterior: } p(\theta \mid D) \in \mathcal{F}$$

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Minh họa: Beta-Binomial conjugacy
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

theta = np.linspace(0, 1, 1000)

# Ví dụ 1: Ít dữ liệu
prior1 = stats.beta(2, 2)
n1, k1 = 5, 3
posterior1 = stats.beta(2 + k1, 2 + n1 - k1)

axes[0, 0].plot(theta, prior1.pdf(theta), linewidth=2, label='Prior: Beta(2, 2)', linestyle='--')
axes[0, 0].plot(theta, posterior1.pdf(theta), linewidth=3, label=f'Posterior: Beta({2+k1}, {2+n1-k1})')
axes[0, 0].set_xlabel('θ', fontsize=11)
axes[0, 0].set_ylabel('Mật độ', fontsize=11)
axes[0, 0].set_title(f'Ít dữ liệu: {k1}/{n1}\nPrior và Posterior CÙNG HỌ (Beta)', 
                    fontsize=12, fontweight='bold')
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(alpha=0.3)

# Ví dụ 2: Nhiều dữ liệu
n2, k2 = 50, 35
posterior2 = stats.beta(2 + k2, 2 + n2 - k2)

axes[0, 1].plot(theta, prior1.pdf(theta), linewidth=2, label='Prior: Beta(2, 2)', linestyle='--', alpha=0.5)
axes[0, 1].plot(theta, posterior2.pdf(theta), linewidth=3, label=f'Posterior: Beta({2+k2}, {2+n2-k2})')
axes[0, 1].set_xlabel('θ', fontsize=11)
axes[0, 1].set_ylabel('Mật độ', fontsize=11)
axes[0, 1].set_title(f'Nhiều dữ liệu: {k2}/{n2}\nVẫn CÙNG HỌ (Beta)', 
                    fontsize=12, fontweight='bold')
axes[0, 1].legend(fontsize=10)
axes[0, 1].grid(alpha=0.3)

# Ví dụ 3: Rất nhiều dữ liệu
n3, k3 = 500, 350
posterior3 = stats.beta(2 + k3, 2 + n3 - k3)

axes[0, 2].plot(theta, prior1.pdf(theta), linewidth=2, label='Prior: Beta(2, 2)', linestyle='--', alpha=0.3)
axes[0, 2].plot(theta, posterior3.pdf(theta), linewidth=3, label=f'Posterior: Beta({2+k3}, {2+n3-k3})')
axes[0, 2].set_xlabel('θ', fontsize=11)
axes[0, 2].set_ylabel('Mật độ', fontsize=11)
axes[0, 2].set_title(f'RẤT nhiều dữ liệu: {k3}/{n3}\nVẫn CÙNG HỌ (Beta)', 
                    fontsize=12, fontweight='bold')
axes[0, 2].legend(fontsize=10)
axes[0, 2].grid(alpha=0.3)

# Giải thích
axes[1, 0].axis('off')
explanation = """
╔═══════════════════════════════════════════════════════════╗
║              CONJUGATE PRIOR                              ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Định nghĩa:                                              ║
║    Prior và Posterior CÙNG HỌ phân phối                   ║
║                                                           ║
║  Ví dụ: Beta-Binomial                                     ║
║    Prior: Beta(α, β)                                      ║
║    Likelihood: Binomial(n, θ)                             ║
║    Posterior: Beta(α+k, β+n-k)                            ║
║                                                           ║
║  Lợi ích:                                                 ║
║    ✓ Tính toán GIẢI TÍCH                                  ║
║    ✓ Không cần MCMC                                       ║
║    ✓ Nhanh, chính xác                                     ║
║    ✓ Dễ cập nhật tuần tự                                  ║
║                                                           ║
║  Hạn chế:                                                 ║
║    • Chỉ có một số cặp conjugate                          ║
║    • Có thể không linh hoạt                               ║
║    • Model phức tạp → không conjugate                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[1, 0].text(0.5, 0.5, explanation, fontsize=9, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Công thức cập nhật
axes[1, 1].axis('off')
formula = """
    CÔNG THỨC CẬP NHẬT
    
    Prior:
      Beta(α, β)
    
    Dữ liệu:
      k thành công trong n thử
    
    Posterior:
      Beta(α + k, β + n - k)
    
    ─────────────────────────────
    
    Diễn giải:
      α: "số thành công giả"
      β: "số thất bại giả"
      
      α + k: thành công thực + giả
      β + (n-k): thất bại thực + giả
    
    ─────────────────────────────
    
    Ví dụ:
      Prior: Beta(2, 2)
        → 2 thành công, 2 thất bại
      Data: 35/50
        → 35 thành công, 15 thất bại
      Posterior: Beta(37, 17)
        → 37 thành công, 17 thất bại
"""

axes[1, 1].text(0.5, 0.5, formula, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Tham số hiệu dụng
axes[1, 2].axis('off')
effective = f"""
THAM SỐ HIỆU DỤNG

Prior: Beta(α, β)
  n_eff = α + β
  "Kích thước mẫu hiệu dụng"

Ví dụ:
  Beta(2, 2): n_eff = 4
  Beta(10, 10): n_eff = 20
  Beta(100, 100): n_eff = 200

→ n_eff càng lớn
  → Prior càng mạnh
  → Cần nhiều dữ liệu để vượt qua

Dữ liệu: n = {n2}
Prior: n_eff = 4
→ Dữ liệu mạnh hơn nhiều!

Posterior:
  Mean = (α+k)/(α+β+n)
       = {posterior2.mean():.3f}
  ≈ k/n = {k2/n2:.3f}
"""

axes[1, 2].text(0.5, 0.5, effective, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

plt.tight_layout()
plt.show()
```

![Conjugate Prior: Beta-Binomial]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_prior_beta_binomial.png)

```python
print("=== CONJUGATE PRIOR: BETA-BINOMIAL ===")
print(f"\nPrior: Beta(2, 2)")
print(f"  n_eff = {2 + 2}")
print(f"\nVí dụ 1: {k1}/{n1}")
print(f"  Posterior: Beta({2+k1}, {2+n1-k1})")
print(f"  Mean: {posterior1.mean():.3f}")
print(f"\nVí dụ 2: {k2}/{n2}")
print(f"  Posterior: Beta({2+k2}, {2+n2-k2})")
print(f"  Mean: {posterior2.mean():.3f}")
print(f"\nVí dụ 3: {k3}/{n3}")
print(f"  Posterior: Beta({2+k3}, {2+n3-k3})")
print(f"  Mean: {posterior3.mean():.3f}")
```

## 2. Các Cặp Conjugate Phổ biến

### 2.1. Bảng Tổng hợp

```python
# Bảng conjugate priors
fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('off')

conjugate_table = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                    CÁC CẶP CONJUGATE PRIOR PHỔ BIẾN                        ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  1. BETA - BINOMIAL                                                        ║
║     Tham số: θ ∈ [0, 1] (xác suất)                                        ║
║     Prior: Beta(α, β)                                                     ║
║     Likelihood: Binomial(n, θ)                                            ║
║     Posterior: Beta(α + k, β + n - k)                                     ║
║     Ứng dụng: Tỷ lệ, xác suất, A/B testing                                ║
║                                                                           ║
║  2. NORMAL - NORMAL (σ² biết)                                             ║
║     Tham số: μ ∈ ℝ (mean)                                                 ║
║     Prior: Normal(μ₀, σ₀²)                                                ║
║     Likelihood: Normal(μ, σ²)                                             ║
║     Posterior: Normal(μ₁, σ₁²)                                            ║
║       μ₁ = (μ₀/σ₀² + Σxᵢ/σ²) / (1/σ₀² + n/σ²)                            ║
║       1/σ₁² = 1/σ₀² + n/σ²                                                ║
║     Ứng dụng: Chiều cao, cân nặng, nhiệt độ                               ║
║                                                                           ║
║  3. GAMMA - POISSON                                                        ║
║     Tham số: λ > 0 (rate)                                                 ║
║     Prior: Gamma(α, β)                                                    ║
║     Likelihood: Poisson(λ)                                                ║
║     Posterior: Gamma(α + Σxᵢ, β + n)                                      ║
║     Ứng dụng: Số sự kiện, số lỗi, traffic                                 ║
║                                                                           ║
║  4. GAMMA - EXPONENTIAL                                                    ║
║     Tham số: λ > 0 (rate)                                                 ║
║     Prior: Gamma(α, β)                                                    ║
║     Likelihood: Exponential(λ)                                            ║
║     Posterior: Gamma(α + n, β + Σxᵢ)                                      ║
║     Ứng dụng: Thời gian chờ, lifetime                                     ║
║                                                                           ║
║  5. INVERSE-GAMMA - NORMAL (μ biết)                                        ║
║     Tham số: σ² > 0 (variance)                                            ║
║     Prior: Inverse-Gamma(α, β)                                            ║
║     Likelihood: Normal(μ, σ²)                                             ║
║     Posterior: Inverse-Gamma(α + n/2, β + Σ(xᵢ-μ)²/2)                     ║
║     Ứng dụng: Ước lượng variance                                          ║
║                                                                           ║
║  6. DIRICHLET - MULTINOMIAL                                                ║
║     Tham số: (θ₁, ..., θₖ) (probabilities)                                ║
║     Prior: Dirichlet(α₁, ..., αₖ)                                         ║
║     Likelihood: Multinomial(n, θ)                                         ║
║     Posterior: Dirichlet(α₁+n₁, ..., αₖ+nₖ)                               ║
║     Ứng dụng: Phân loại nhiều lớp, topic modeling                         ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

ax.text(0.5, 0.5, conjugate_table, fontsize=9, family='monospace',
       ha='center', va='center',
       bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))

plt.tight_layout()
plt.show()
```

### 2.2. Ví dụ: Normal-Normal

```python
# Ví dụ chi tiết: Normal-Normal conjugacy
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Giả sử: Đo chiều cao, σ = 10 cm (biết)
sigma = 10
true_mu = 170

# Prior: Normal(165, 15²)
mu0, sigma0 = 165, 15
prior_normal = stats.norm(mu0, sigma0)

# Dữ liệu
np.random.seed(42)
n = 20
data = np.random.normal(true_mu, sigma, n)
sample_mean = data.mean()

# Posterior: Normal(μ₁, σ₁²)
# Precision (inverse variance)
precision0 = 1 / sigma0**2
precision_likelihood = n / sigma**2
precision1 = precision0 + precision_likelihood
sigma1 = np.sqrt(1 / precision1)

mu1 = (mu0 * precision0 + sample_mean * n / sigma**2) / precision1
posterior_normal = stats.norm(mu1, sigma1)

# Vẽ
mu_grid = np.linspace(150, 190, 1000)

axes[0, 0].plot(mu_grid, prior_normal.pdf(mu_grid), linewidth=2, 
               label=f'Prior: N({mu0}, {sigma0}²)', linestyle='--')
axes[0, 0].plot(mu_grid, posterior_normal.pdf(mu_grid), linewidth=3, 
               label=f'Posterior: N({mu1:.1f}, {sigma1:.1f}²)')
axes[0, 0].axvline(sample_mean, color='red', linestyle=':', linewidth=2, 
                  label=f'Sample mean = {sample_mean:.1f}')
axes[0, 0].axvline(true_mu, color='green', linestyle=':', linewidth=2, 
                  label=f'True μ = {true_mu}', alpha=0.5)
axes[0, 0].set_xlabel('μ (chiều cao, cm)', fontsize=11)
axes[0, 0].set_ylabel('Mật độ', fontsize=11)
axes[0, 0].set_title(f'Normal-Normal Conjugacy\nn = {n}, σ = {sigma} (biết)', 
                    fontsize=12, fontweight='bold')
axes[0, 0].legend(fontsize=9)
axes[0, 0].grid(alpha=0.3)

# Công thức
axes[0, 1].axis('off')
formula_normal = f"""
NORMAL-NORMAL CONJUGACY

Prior:
  μ ~ Normal({mu0}, {sigma0}²)
  Precision: 1/σ₀² = {precision0:.6f}

Likelihood:
  xᵢ ~ Normal(μ, {sigma}²)
  n = {n}
  x̄ = {sample_mean:.2f}
  Precision: n/σ² = {precision_likelihood:.6f}

Posterior:
  μ ~ Normal({mu1:.2f}, {sigma1:.2f}²)
  
  Precision: 1/σ₁² = 1/σ₀² + n/σ²
           = {precision0:.6f} + {precision_likelihood:.6f}
           = {precision1:.6f}
  
  σ₁ = √(1/{precision1:.6f}) = {sigma1:.2f}
  
  μ₁ = (μ₀/σ₀² + nx̄/σ²) / (1/σ₀² + n/σ²)
     = {mu1:.2f}

→ Posterior là TRUNG BÌNH CÓ TRỌNG SỐ
  của prior mean và sample mean!
"""

axes[0, 1].text(0.5, 0.5, formula_normal, fontsize=9, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Ảnh hưởng của n
axes[1, 0].plot(mu_grid, prior_normal.pdf(mu_grid), linewidth=2, 
               label='Prior', linestyle='--', alpha=0.5)

for n_sim in [5, 20, 50, 100]:
    data_sim = np.random.normal(true_mu, sigma, n_sim)
    sample_mean_sim = data_sim.mean()
    
    precision_sim = precision0 + n_sim / sigma**2
    sigma_sim = np.sqrt(1 / precision_sim)
    mu_sim = (mu0 * precision0 + sample_mean_sim * n_sim / sigma**2) / precision_sim
    
    post_sim = stats.norm(mu_sim, sigma_sim)
    axes[1, 0].plot(mu_grid, post_sim.pdf(mu_grid), linewidth=2, 
                   label=f'n={n_sim}: μ={mu_sim:.1f}, σ={sigma_sim:.1f}')

axes[1, 0].axvline(true_mu, color='green', linestyle=':', linewidth=2, 
                  label=f'True μ = {true_mu}', alpha=0.5)
axes[1, 0].set_xlabel('μ', fontsize=11)
axes[1, 0].set_ylabel('Mật độ', fontsize=11)
axes[1, 0].set_title('Ảnh hưởng của Kích thước Mẫu\nPosterior hội tụ về true μ', 
                    fontsize=12, fontweight='bold')
axes[1, 0].legend(fontsize=9)
axes[1, 0].grid(alpha=0.3)

# Trọng số
n_range = np.arange(1, 101)
weight_prior = precision0 / (precision0 + n_range / sigma**2)
weight_data = (n_range / sigma**2) / (precision0 + n_range / sigma**2)

axes[1, 1].plot(n_range, weight_prior, linewidth=2, label='Trọng số Prior')
axes[1, 1].plot(n_range, weight_data, linewidth=2, label='Trọng số Data')
axes[1, 1].set_xlabel('Kích thước mẫu (n)', fontsize=11)
axes[1, 1].set_ylabel('Trọng số', fontsize=11)
axes[1, 1].set_title('Trọng số Prior vs Data\nData càng nhiều → trọng số càng lớn', 
                    fontsize=12, fontweight='bold')
axes[1, 1].legend(fontsize=10)
axes[1, 1].grid(alpha=0.3)
axes[1, 1].set_ylim(0, 1)

plt.tight_layout()
plt.show()

print("\n=== NORMAL-NORMAL CONJUGACY ===")
print(f"\nPrior: N({mu0}, {sigma0}²)")
print(f"Data: n={n}, x̄={sample_mean:.2f}, σ={sigma}")
print(f"Posterior: N({mu1:.2f}, {sigma1:.2f}²)")
print(f"\nTrọng số:")
print(f"  Prior: {weight_prior[n-1]:.3f}")
print(f"  Data: {weight_data[n-1]:.3f}")
print(f"\nPosterior mean = {weight_prior[n-1]:.3f} × {mu0} + {weight_data[n-1]:.3f} × {sample_mean:.2f}")
print(f"                = {mu1:.2f}")
```

### 2.3. Ví dụ: Gamma-Poisson

```python
# Ví dụ: Gamma-Poisson conjugacy
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Giả sử: Số lỗi trong code
# Prior: Gamma(2, 1) → E[λ] = 2 lỗi/1000 dòng
alpha_prior, beta_prior = 2, 1
prior_gamma = stats.gamma(alpha_prior, scale=1/beta_prior)

# Dữ liệu: Quan sát 10 files, tổng 25 lỗi
n_files = 10
total_errors = 25

# Posterior: Gamma(α + Σxᵢ, β + n)
alpha_post = alpha_prior + total_errors
beta_post = beta_prior + n_files
posterior_gamma = stats.gamma(alpha_post, scale=1/beta_post)

# Vẽ
lambda_grid = np.linspace(0, 8, 1000)

axes[0, 0].plot(lambda_grid, prior_gamma.pdf(lambda_grid), linewidth=2, 
               label=f'Prior: Gamma({alpha_prior}, {beta_prior})', linestyle='--')
axes[0, 0].plot(lambda_grid, posterior_gamma.pdf(lambda_grid), linewidth=3, 
               label=f'Posterior: Gamma({alpha_post}, {beta_post})')
axes[0, 0].axvline(total_errors/n_files, color='red', linestyle=':', linewidth=2, 
                  label=f'MLE = {total_errors/n_files:.2f}')
axes[0, 0].set_xlabel('λ (lỗi/file)', fontsize=11)
axes[0, 0].set_ylabel('Mật độ', fontsize=11)
axes[0, 0].set_title(f'Gamma-Poisson Conjugacy\n{total_errors} lỗi trong {n_files} files', 
                    fontsize=12, fontweight='bold')
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(alpha=0.3)

# Công thức
axes[0, 1].axis('off')
formula_gamma = f"""
GAMMA-POISSON CONJUGACY

Prior:
  λ ~ Gamma({alpha_prior}, {beta_prior})
  E[λ] = α/β = {alpha_prior/beta_prior:.2f}
  Var[λ] = α/β² = {alpha_prior/beta_prior**2:.2f}

Likelihood:
  xᵢ ~ Poisson(λ)
  n = {n_files} files
  Σxᵢ = {total_errors} lỗi

Posterior:
  λ ~ Gamma(α + Σxᵢ, β + n)
    = Gamma({alpha_post}, {beta_post})
  
  E[λ] = {alpha_post}/{beta_post} = {alpha_post/beta_post:.2f}
  Var[λ] = {alpha_post}/{beta_post**2} = {alpha_post/beta_post**2:.2f}

95% CI: [{posterior_gamma.ppf(0.025):.2f}, 
         {posterior_gamma.ppf(0.975):.2f}]

→ Kỳ vọng ~{alpha_post/beta_post:.1f} lỗi/file
"""

axes[0, 1].text(0.5, 0.5, formula_gamma, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# Posterior Predictive: Số lỗi trong file mới
# Negative Binomial
from scipy.special import comb, gamma as gamma_func

def negative_binomial_pmf(k, r, p):
    """Negative Binomial PMF"""
    return comb(k + r - 1, k) * (1 - p)**r * p**k

# Posterior predictive cho Gamma-Poisson là Negative Binomial
# với r = α_post, p = 1/(1 + β_post)
r = alpha_post
p = 1 / (1 + beta_post)

k_range = np.arange(0, 15)
ppd = [negative_binomial_pmf(k, r, p) for k in k_range]

axes[1, 0].bar(k_range, ppd, alpha=0.7, edgecolor='black')
axes[1, 0].axvline(alpha_post/beta_post, color='red', linestyle='--', linewidth=2,
                  label=f'E[k] = {alpha_post/beta_post:.2f}')
axes[1, 0].set_xlabel('k (số lỗi trong file MỚI)', fontsize=11)
axes[1, 0].set_ylabel('Xác suất', fontsize=11)
axes[1, 0].set_title('Posterior Predictive\nDự đoán số lỗi trong file mới', 
                    fontsize=12, fontweight='bold')
axes[1, 0].legend(fontsize=10)
axes[1, 0].grid(alpha=0.3, axis='y')

# Giải thích
axes[1, 1].axis('off')
interpretation = """
╔═══════════════════════════════════════════════════════════╗
║           DIỄN GIẢI                                       ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Prior:                                                   ║
║    Tin là ~2 lỗi/file                                     ║
║    Không chắc lắm (variance lớn)                          ║
║                                                           ║
║  Data:                                                    ║
║    25 lỗi trong 10 files                                  ║
║    → ~2.5 lỗi/file                                        ║
║                                                           ║
║  Posterior:                                               ║
║    E[λ] = 2.45 lỗi/file                                   ║
║    → Giữa prior (2) và data (2.5)                         ║
║    → Chắc chắn hơn (variance nhỏ hơn)                     ║
║                                                           ║
║  Dự đoán file mới:                                        ║
║    Kỳ vọng ~2.45 lỗi                                      ║
║    Nhưng có thể 0-10 lỗi                                  ║
║    → Kết hợp uncertainty về λ                             ║
║      và randomness của Poisson                            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[1, 1].text(0.5, 0.5, interpretation, fontsize=9, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.show()

print("\n=== GAMMA-POISSON CONJUGACY ===")
print(f"\nPrior: Gamma({alpha_prior}, {beta_prior})")
print(f"  E[λ] = {alpha_prior/beta_prior:.2f}")
print(f"\nData: {total_errors} lỗi trong {n_files} files")
print(f"  Sample mean = {total_errors/n_files:.2f}")
print(f"\nPosterior: Gamma({alpha_post}, {beta_post})")
print(f"  E[λ] = {alpha_post/beta_post:.2f}")
print(f"  95% CI = [{posterior_gamma.ppf(0.025):.2f}, {posterior_gamma.ppf(0.975):.2f}]")
```

## 3. Khi nào KHÔNG dùng Conjugate Prior?

### 3.1. Hạn chế

```python
# Minh họa: Khi conjugate prior không phù hợp
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

theta = np.linspace(0, 1, 1000)

# Tình huống: Biết chắc θ ∈ [0.2, 0.4]
# Beta conjugate không thể biểu diễn tốt

# Thử Beta(20, 30) - gần nhất
beta_conjugate = stats.beta(20, 30)

# Prior lý tưởng: Uniform trên [0.2, 0.4]
def ideal_prior(theta):
    return np.where((theta >= 0.2) & (theta <= 0.4), 1/0.2, 0)

axes[0, 0].plot(theta, beta_conjugate.pdf(theta), linewidth=2, 
               label='Beta(20, 30) - Conjugate')
axes[0, 0].plot(theta, ideal_prior(theta), linewidth=2, 
               label='Uniform[0.2, 0.4] - Lý tưởng', linestyle='--')
axes[0, 0].set_xlabel('θ', fontsize=11)
axes[0, 0].set_ylabel('Mật độ', fontsize=11)
axes[0, 0].set_title('Prior Conjugate vs Lý tưởng\nConjugate KHÔNG thể biểu diễn tốt!', 
                    fontsize=12, fontweight='bold')
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(alpha=0.3)
axes[0, 0].set_ylim(0, 10)

# Giải thích
axes[0, 1].axis('off')
explanation1 = """
╔═══════════════════════════════════════════════════════════╗
║         KHI NÀO KHÔNG DÙNG CONJUGATE?                     ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  1. Prior phức tạp                                        ║
║     • Multimodal                                          ║
║     • Truncated                                           ║
║     • Mixture                                             ║
║     → Conjugate không biểu diễn được                      ║
║                                                           ║
║  2. Likelihood phức tạp                                   ║
║     • Không có conjugate                                  ║
║     • Ví dụ: Logistic regression                          ║
║              Neural networks                              ║
║                                                           ║
║  3. Model phức tạp                                        ║
║     • Hierarchical                                        ║
║     • Nhiều tham số phụ thuộc                             ║
║     → Không có conjugate đơn giản                         ║
║                                                           ║
║  GIẢI PHÁP:                                               ║
║    → Dùng MCMC (sẽ học ở bài sau)                         ║
║    → Grid approximation                                   ║
║    → Variational inference                                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

axes[0, 1].text(0.5, 0.5, explanation1, fontsize=9, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='#ffcccc', alpha=0.8))

# Ví dụ: Mixture prior
# Prior: 50% tin θ~0.3, 50% tin θ~0.7
mixture_prior = 0.5 * stats.beta(30, 70).pdf(theta) + 0.5 * stats.beta(70, 30).pdf(theta)

axes[1, 0].plot(theta, mixture_prior, linewidth=3, label='Mixture Prior (lý tưởng)')
axes[1, 0].plot(theta, stats.beta(50, 50).pdf(theta), linewidth=2, 
               label='Beta(50, 50) - Conjugate', linestyle='--', alpha=0.7)
axes[1, 0].set_xlabel('θ', fontsize=11)
axes[1, 0].set_ylabel('Mật độ', fontsize=11)
axes[1, 0].set_title('Mixture Prior\nConjugate KHÔNG thể biểu diễn bimodal!', 
                    fontsize=12, fontweight='bold')
axes[1, 0].legend(fontsize=10)
axes[1, 0].grid(alpha=0.3)

# Decision tree
axes[1, 1].axis('off')
decision = """
    NÊN DÙNG CONJUGATE PRIOR?
    
    ┌─────────────────────────┐
    │ Prior đơn giản?         │
    │ (unimodal, standard)    │
    └────────┬────────────────┘
             │
        ┌────┴────┐
        │         │
       YES       NO → MCMC
        │
    ┌───┴────────────────────┐
    │ Likelihood đơn giản?   │
    │ (có conjugate?)        │
    └────────┬───────────────┘
             │
        ┌────┴────┐
        │         │
       YES       NO → MCMC
        │
    ┌───┴────────────────────┐
    │ Model đơn giản?        │
    │ (ít tham số)           │
    └────────┬───────────────┘
             │
        ┌────┴────┐
        │         │
       YES       NO → MCMC
        │
        ▼
    ✓ DÙNG CONJUGATE!
      • Nhanh
      • Chính xác
      • Dễ hiểu
"""

axes[1, 1].text(0.5, 0.5, decision, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))

plt.tight_layout()
plt.show()
```

![Tổng hợp các Conjugate Families]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_families.png)

## Tóm tắt

```python
# Infographic tóm tắt
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111)
ax.axis('off')

summary = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                   CONJUGATE PRIORS - TÓM TẮT                               ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  1. ĐỊNH NGHĨA                                                             ║
║     Prior và Posterior CÙNG HỌ phân phối                                  ║
║     → Tính toán GIẢI TÍCH, không cần MCMC                                 ║
║                                                                           ║
║  2. CÁC CẶP PHỔ BIẾN                                                       ║
║     • Beta - Binomial: Xác suất, tỷ lệ                                    ║
║     • Normal - Normal: Mean (σ² biết)                                     ║
║     • Gamma - Poisson: Count data                                         ║
║     • Gamma - Exponential: Thời gian                                      ║
║     • Inverse-Gamma - Normal: Variance (μ biết)                           ║
║     • Dirichlet - Multinomial: Nhiều lớp                                  ║
║                                                                           ║
║  3. LỢI ÍCH                                                                ║
║     ✓ Tính toán nhanh, chính xác                                          ║
║     ✓ Dễ cập nhật tuần tự                                                 ║
║     ✓ Diễn giải rõ ràng                                                   ║
║     ✓ Không cần MCMC                                                      ║
║                                                                           ║
║  4. HẠN CHẾ                                                                ║
║     • Chỉ có một số cặp conjugate                                         ║
║     • Prior phức tạp → không biểu diễn được                               ║
║     • Model phức tạp → không có conjugate                                 ║
║                                                                           ║
║  5. KHI NÀO DÙNG?                                                          ║
║     ✓ Model đơn giản                                                      ║
║     ✓ Prior standard                                                      ║
║     ✓ Cần tính nhanh                                                      ║
║     ✓ Giảng dạy, minh họa                                                 ║
║                                                                           ║
║  6. KHI NÀO KHÔNG DÙNG?                                                    ║
║     → Model phức tạp → MCMC                                               ║
║     → Prior phức tạp → MCMC                                               ║
║     → Likelihood không standard → MCMC                                    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

ax.text(0.5, 0.5, summary, fontsize=10, family='monospace',
       ha='center', va='center',
       bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))

plt.tight_layout()
plt.show()
```

## Bài tập

1. **Beta-Binomial**: Bắt đầu với prior Beta(5, 5). Quan sát 30 lần tung, thấy 18 ngửa. Tính posterior và 95% credible interval.

2. **Normal-Normal**: Prior N(100, 20²), dữ liệu: n=15, x̄=110, σ=10 (biết). Tính posterior mean và variance.

3. **Gamma-Poisson**: Prior Gamma(3, 2), quan sát [2, 5, 3, 4, 6] sự kiện. Tính posterior và dự đoán số sự kiện tiếp theo.

4. **Cập nhật tuần tự**: Với Beta(2, 2), cập nhật tuần tự với dữ liệu: ngày 1 (5/10), ngày 2 (7/10), ngày 3 (6/10). Vẽ posterior sau mỗi ngày.

5. **So sánh**: Khi nào nên dùng conjugate prior? Khi nào nên dùng MCMC? Cho ví dụ cụ thể.

## Tài liệu tham khảo

1. **McElreath, R. (2020).** *Statistical Rethinking* (2nd Ed.). Chapter 2.
2. **Gelman, A., et al. (2013).** *Bayesian Data Analysis* (3rd Ed.). Chapter 2.
3. **Murphy, K. P. (2012).** *Machine Learning: A Probabilistic Perspective*. Chapter 3.

---

## Tài liệu tham khảo

### Primary:
- **McElreath, R. (2020).** *Statistical Rethinking* (2nd Ed.)
  - Chapter 2-3: Bayesian updating, conjugate families
  - Focus on: Beta-Binomial conjugacy, analytical posteriors

### Secondary:

#### Gelman et al. - Bayesian Data Analysis (3rd Edition):
- **Chapter 2.4**: Binomial model (Beta prior)
- **Chapter 2.5**: Poisson model (Gamma prior)
- **Chapter 2.6**: Normal model with known variance
- Focus on: Conjugate prior families, analytical solutions

#### Kruschke - Doing Bayesian Data Analysis (2015):
- **Chapter 6**: Inferring a Binomial Probability via Exact Mathematical Analysis
- Focus on: Beta-Binomial model, conjugate updating, sequential updating

**Lưu ý**: Gelman/Kruschke sử dụng R/Stan, nhưng conjugate prior concepts hoàn toàn tương đương với Python/SciPy implementation.

---

*Bài học tiếp theo: [2.6 Grid Approximation - Phương pháp Lưới](/vi/chapter02/grid-approximation/)*

