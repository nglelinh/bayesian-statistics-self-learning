---
layout: post
title: "00-07: Hàm Mật độ Xác suất (PDF) - Chi tiết"
chapter: '00'
order: 7
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu

Bài học này trình bày **rất chi tiết** về hàm mật độ xác suất (PDF), sự khác biệt với hàm khối xác suất (PMF), và cách hiểu đúng về PDF trong bối cảnh biến ngẫu nhiên liên tục.

## 1. Từ Rời rạc đến Liên tục

### 1.1. Biến Ngẫu nhiên Rời rạc - PMF

Với biến ngẫu nhiên **rời rạc** $$X$$, ta có **Probability Mass Function (PMF)**:

$$P(X = x)$$

**Ví dụ**: Tung xúc xắc

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Xúc xắc công bằng
outcomes = [1, 2, 3, 4, 5, 6]
probabilities = [1/6] * 6

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(outcomes, probabilities, width=0.6, alpha=0.7, edgecolor='black', linewidth=2)

# Tô màu các bars
for bar, prob in zip(bars, probabilities):
    bar.set_color('steelblue')
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
           f'{prob:.3f}',
           ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_xlabel('Giá trị (x)', fontsize=12)
ax.set_ylabel('Xác suất P(X = x)', fontsize=12)
ax.set_title('PMF: Xúc xắc Công bằng', fontsize=14, fontweight='bold')
ax.set_xticks(outcomes)
ax.set_ylim(0, 0.25)
ax.grid(axis='y', alpha=0.3)

# Tổng xác suất
total_prob = sum(probabilities)
ax.text(3.5, 0.22, f'Σ P(X=x) = {total_prob:.1f}', 
       fontsize=12, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

plt.tight_layout()
plt.show()

print("=== PMF - Biến Rời rạc ===")
print(f"P(X = 3) = {probabilities[2]:.4f}")
print(f"P(X = 5) = {probabilities[4]:.4f}")
print(f"Tổng: Σ P(X=x) = {total_prob}")
```

**Tính chất PMF**:
1. $$P(X = x) \geq 0$$ với mọi $$x$$
2. $$\sum_{\text{all } x} P(X = x) = 1$$
3. $$P(X = x)$$ **là xác suất thực sự** (giá trị có nghĩa)

### 1.2. Vấn đề với Biến Liên tục

Giả sử chiều cao người trưởng thành $$X \sim \mathcal{N}(170, 10^2)$$ cm.

**Câu hỏi**: $$P(X = 170)$$ bằng bao nhiêu?

```python
# Chiều cao
mu, sigma = 170, 10

# Thử tính P(X = 170)
# Với biến liên tục, xác suất tại 1 điểm = 0!
print("=== Biến Liên tục ===")
print(f"P(X = 170) = 0")
print(f"P(X = 170.5) = 0")
print(f"P(X = bất kỳ giá trị cụ thể nào) = 0")
```

**Lý do**: Có **vô số** giá trị có thể (170, 170.001, 170.0001, ...). Nếu mỗi giá trị có xác suất > 0, tổng sẽ vô hạn!

**Giải pháp**: Thay vì hỏi xác suất tại 1 điểm, ta hỏi xác suất trong 1 **khoảng**:

$$P(a \leq X \leq b)$$

## 2. Hàm Mật độ Xác suất (PDF)

### 2.1. Định nghĩa Chính thức

Cho biến ngẫu nhiên liên tục $$X$$, **Probability Density Function** $$f(x)$$ thỏa:

$$P(a \leq X \leq b) = \int_a^b f(x) \, dx$$

**Chú ý quan trọng**: 
- $$f(x)$$ **KHÔNG PHẢI** là xác suất!
- $$f(x)$$ là **mật độ** xác suất
- Chỉ có **tích phân** của $$f(x)$$ mới là xác suất

### 2.2. Tại sao gọi là "Mật độ"?

Tương tự **mật độ khối lượng** trong vật lý:
- Mật độ khối lượng $$\rho(x)$$ (kg/m³) không phải là khối lượng
- Khối lượng = $$\int \rho(x) \, dx$$

Tương tự:
- Mật độ xác suất $$f(x)$$ không phải là xác suất
- Xác suất = $$\int f(x) \, dx$$

```python
# Minh họa khái niệm mật độ
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Trái: Mật độ khối lượng
x_mass = np.linspace(0, 10, 100)
density_mass = 2 + 0.5 * np.sin(x_mass)  # kg/m³

axes[0].plot(x_mass, density_mass, 'b-', linewidth=2)
axes[0].fill_between(x_mass, density_mass, alpha=0.3)
axes[0].set_xlabel('Vị trí (m)', fontsize=12)
axes[0].set_ylabel('Mật độ khối lượng ρ(x) (kg/m³)', fontsize=12)
axes[0].set_title('Mật độ Khối lượng\n(Vật lý)', fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)

# Tô vùng từ 3 đến 7
x_fill = x_mass[(x_mass >= 3) & (x_mass <= 7)]
density_fill = 2 + 0.5 * np.sin(x_fill)
axes[0].fill_between(x_fill, density_fill, alpha=0.5, color='red')
axes[0].text(5, 1, 'Khối lượng = ∫₃⁷ ρ(x)dx', 
            fontsize=11, ha='center', 
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

# Phải: Mật độ xác suất
x_prob = np.linspace(-4, 4, 100)
pdf = stats.norm.pdf(x_prob, 0, 1)

axes[1].plot(x_prob, pdf, 'b-', linewidth=2)
axes[1].fill_between(x_prob, pdf, alpha=0.3)
axes[1].set_xlabel('x', fontsize=12)
axes[1].set_ylabel('Mật độ xác suất f(x)', fontsize=12)
axes[1].set_title('Mật độ Xác suất\n(Thống kê)', fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)

# Tô vùng từ -1 đến 1
x_fill = x_prob[(x_prob >= -1) & (x_prob <= 1)]
pdf_fill = stats.norm.pdf(x_fill, 0, 1)
axes[1].fill_between(x_fill, pdf_fill, alpha=0.5, color='red')
prob = stats.norm.cdf(1, 0, 1) - stats.norm.cdf(-1, 0, 1)
axes[1].text(0, 0.15, f'Xác suất = ∫₋₁¹ f(x)dx\n= {prob:.3f}', 
            fontsize=11, ha='center',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.show()
```

### 2.3. Tính chất của PDF

**1. Không âm**: $$f(x) \geq 0$$ với mọi $$x$$

**2. Tích phân = 1**: 

$$\int_{-\infty}^{\infty} f(x) \, dx = 1$$

**3. $$f(x)$$ có thể > 1**: Vì $$f(x)$$ không phải xác suất!

```python
# Ví dụ: PDF có thể > 1
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Ví dụ 1: Normal với sigma nhỏ
x = np.linspace(-2, 2, 200)
pdf1 = stats.norm.pdf(x, 0, 0.3)  # sigma = 0.3

axes[0].plot(x, pdf1, 'b-', linewidth=2)
axes[0].fill_between(x, pdf1, alpha=0.3)
axes[0].axhline(y=1, color='red', linestyle='--', linewidth=2, label='y = 1')
axes[0].set_xlabel('x', fontsize=12)
axes[0].set_ylabel('f(x)', fontsize=12)
axes[0].set_title('N(0, 0.3²): f(0) = {:.2f} > 1'.format(pdf1.max()), 
                 fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Ví dụ 2: Uniform trên [0, 0.5]
x2 = np.linspace(-0.5, 1, 200)
pdf2 = np.where((x2 >= 0) & (x2 <= 0.5), 2, 0)  # f(x) = 2 trên [0, 0.5]

axes[1].plot(x2, pdf2, 'b-', linewidth=2)
axes[1].fill_between(x2, pdf2, alpha=0.3)
axes[1].axhline(y=1, color='red', linestyle='--', linewidth=2, label='y = 1')
axes[1].set_xlabel('x', fontsize=12)
axes[1].set_ylabel('f(x)', fontsize=12)
axes[1].set_title('Uniform[0, 0.5]: f(x) = 2 > 1', 
                 fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(alpha=0.3)
axes[1].set_ylim(-0.2, 2.5)

# Ví dụ 3: Beta với alpha, beta < 1
x3 = np.linspace(0.001, 0.999, 200)
pdf3 = stats.beta.pdf(x3, 0.5, 0.5)

axes[2].plot(x3, pdf3, 'b-', linewidth=2)
axes[2].fill_between(x3, pdf3, alpha=0.3)
axes[2].axhline(y=1, color='red', linestyle='--', linewidth=2, label='y = 1')
axes[2].set_xlabel('x', fontsize=12)
axes[2].set_ylabel('f(x)', fontsize=12)
axes[2].set_title('Beta(0.5, 0.5): f(x) → ∞ tại x=0,1', 
                 fontsize=12, fontweight='bold')
axes[2].legend()
axes[2].grid(alpha=0.3)
axes[2].set_ylim(0, 5)

plt.tight_layout()
plt.show()

# Kiểm tra tích phân = 1
from scipy import integrate

print("=== Kiểm tra ∫f(x)dx = 1 ===")
integral1, _ = integrate.quad(lambda x: stats.norm.pdf(x, 0, 0.3), -np.inf, np.inf)
print(f"N(0, 0.3²): ∫f(x)dx = {integral1:.6f}")

integral2, _ = integrate.quad(lambda x: 2 if 0 <= x <= 0.5 else 0, -np.inf, np.inf)
print(f"Uniform[0, 0.5]: ∫f(x)dx = {integral2:.6f}")

integral3, _ = integrate.quad(lambda x: stats.beta.pdf(x, 0.5, 0.5), 0, 1)
print(f"Beta(0.5, 0.5): ∫f(x)dx = {integral3:.6f}")
```

## 3. Hiểu Sâu về PDF

### 3.1. PDF là Giới hạn của Histogram

Khi số lượng mẫu $$n \to \infty$$ và độ rộng bin $$\Delta x \to 0$$:

$$\text{Histogram} \to \text{PDF}$$

```python
# Minh họa: Histogram → PDF
np.random.seed(42)
mu, sigma = 0, 1

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

sample_sizes = [100, 500, 1000, 5000, 10000, 50000]
bin_counts = [10, 20, 30, 40, 50, 60]

x_theory = np.linspace(-4, 4, 200)
pdf_theory = stats.norm.pdf(x_theory, mu, sigma)

for idx, (n, bins) in enumerate(zip(sample_sizes, bin_counts)):
    samples = np.random.normal(mu, sigma, n)
    
    axes[idx].hist(samples, bins=bins, density=True, alpha=0.7, 
                  edgecolor='black', label=f'Histogram (n={n})')
    axes[idx].plot(x_theory, pdf_theory, 'r-', linewidth=2, label='PDF lý thuyết')
    axes[idx].set_xlabel('x', fontsize=11)
    axes[idx].set_ylabel('Mật độ', fontsize=11)
    axes[idx].set_title(f'n = {n}, bins = {bins}', fontsize=12, fontweight='bold')
    axes[idx].legend()
    axes[idx].grid(alpha=0.3)
    axes[idx].set_xlim(-4, 4)
    axes[idx].set_ylim(0, 0.5)

plt.tight_layout()
plt.show()

print("=== Khi n tăng, histogram tiến đến PDF ===")
```

### 3.2. Xác suất trong Khoảng Nhỏ

Với khoảng nhỏ $$[x, x + \Delta x]$$:

$$P(x \leq X \leq x + \Delta x) \approx f(x) \cdot \Delta x$$

Khi $$\Delta x \to 0$$:

$$f(x) = \lim_{\Delta x \to 0} \frac{P(x \leq X \leq x + \Delta x)}{\Delta x}$$

```python
# Minh họa xấp xỉ
mu, sigma = 0, 1
x0 = 1.0

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

delta_xs = [0.5, 0.1, 0.01]

for idx, dx in enumerate(delta_xs):
    x = np.linspace(-3, 3, 200)
    pdf = stats.norm.pdf(x, mu, sigma)
    
    axes[idx].plot(x, pdf, 'b-', linewidth=2, label='PDF')
    
    # Tô vùng [x0, x0 + dx]
    x_fill = np.linspace(x0, x0 + dx, 100)
    pdf_fill = stats.norm.pdf(x_fill, mu, sigma)
    axes[idx].fill_between(x_fill, pdf_fill, alpha=0.5, color='red', 
                          label=f'P({x0} ≤ X ≤ {x0+dx})')
    
    # Hình chữ nhật xấp xỉ
    rect_height = stats.norm.pdf(x0, mu, sigma)
    axes[idx].add_patch(plt.Rectangle((x0, 0), dx, rect_height, 
                                     fill=False, edgecolor='green', 
                                     linewidth=2, linestyle='--'))
    axes[idx].plot([x0, x0+dx], [rect_height, rect_height], 
                  'g--', linewidth=2, label=f'f({x0})·Δx')
    
    # Tính xác suất
    prob_exact = stats.norm.cdf(x0 + dx, mu, sigma) - stats.norm.cdf(x0, mu, sigma)
    prob_approx = rect_height * dx
    
    axes[idx].set_xlabel('x', fontsize=12)
    axes[idx].set_ylabel('f(x)', fontsize=12)
    axes[idx].set_title(f'Δx = {dx}\nP (exact) = {prob_exact:.6f}\nf(x)·Δx = {prob_approx:.6f}', 
                       fontsize=11, fontweight='bold')
    axes[idx].legend(fontsize=9)
    axes[idx].grid(alpha=0.3)
    axes[idx].set_xlim(-1, 3)

plt.tight_layout()
plt.show()

print("=== Xấp xỉ P(x ≤ X ≤ x+Δx) ≈ f(x)·Δx ===")
for dx in delta_xs:
    prob_exact = stats.norm.cdf(x0 + dx, mu, sigma) - stats.norm.cdf(x0, mu, sigma)
    prob_approx = stats.norm.pdf(x0, mu, sigma) * dx
    error = abs(prob_exact - prob_approx)
    print(f"Δx = {dx:6.2f}: Exact = {prob_exact:.8f}, Approx = {prob_approx:.8f}, Error = {error:.8f}")
```

### 3.3. Đơn vị của PDF

Nếu $$X$$ có đơn vị (ví dụ: cm), thì:
- $$f(x)$$ có đơn vị: **1/cm** (nghịch đảo)
- $$f(x) \cdot dx$$ có đơn vị: **(1/cm) × cm = không đơn vị** (xác suất)

```python
# Ví dụ: Chiều cao (cm)
mu_cm, sigma_cm = 170, 10  # cm

x_cm = np.linspace(140, 200, 200)
pdf_cm = stats.norm.pdf(x_cm, mu_cm, sigma_cm)

# Chuyển sang mét
mu_m, sigma_m = 1.70, 0.10  # m
x_m = x_cm / 100
pdf_m = stats.norm.pdf(x_m, mu_m, sigma_m)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Đơn vị cm
axes[0].plot(x_cm, pdf_cm, 'b-', linewidth=2)
axes[0].fill_between(x_cm, pdf_cm, alpha=0.3)
axes[0].set_xlabel('Chiều cao (cm)', fontsize=12)
axes[0].set_ylabel('f(x) (1/cm)', fontsize=12)
axes[0].set_title(f'PDF với đơn vị cm\nf(170) = {stats.norm.pdf(170, mu_cm, sigma_cm):.4f} (1/cm)', 
                 fontsize=12, fontweight='bold')
axes[0].grid(alpha=0.3)

# Đơn vị m
axes[1].plot(x_m, pdf_m, 'r-', linewidth=2)
axes[1].fill_between(x_m, pdf_m, alpha=0.3)
axes[1].set_xlabel('Chiều cao (m)', fontsize=12)
axes[1].set_ylabel('f(x) (1/m)', fontsize=12)
axes[1].set_title(f'PDF với đơn vị m\nf(1.70) = {stats.norm.pdf(1.70, mu_m, sigma_m):.4f} (1/m)', 
                 fontsize=12, fontweight='bold')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("=== Đơn vị của PDF ===")
print(f"Đơn vị cm: f(170 cm) = {stats.norm.pdf(170, mu_cm, sigma_cm):.6f} (1/cm)")
print(f"Đơn vị m:  f(1.70 m) = {stats.norm.pdf(1.70, mu_m, sigma_m):.6f} (1/m)")
print(f"\nLưu ý: {stats.norm.pdf(170, mu_cm, sigma_cm):.6f} × 100 = {stats.norm.pdf(1.70, mu_m, sigma_m):.6f}")
print("(Vì 1/cm × 100 = 1/m)")

# Xác suất không đổi theo đơn vị
prob_cm = stats.norm.cdf(180, mu_cm, sigma_cm) - stats.norm.cdf(160, mu_cm, sigma_cm)
prob_m = stats.norm.cdf(1.80, mu_m, sigma_m) - stats.norm.cdf(1.60, mu_m, sigma_m)
print(f"\nP(160 cm ≤ X ≤ 180 cm) = {prob_cm:.6f}")
print(f"P(1.60 m ≤ X ≤ 1.80 m) = {prob_m:.6f}")
print("(Xác suất không đổi!)")
```

## 4. So sánh PMF và PDF

```python
# Bảng so sánh
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# PMF - Rời rạc
x_discrete = np.arange(0, 11)
pmf = stats.binom.pmf(x_discrete, 10, 0.5)

axes[0].bar(x_discrete, pmf, width=0.6, alpha=0.7, edgecolor='black', linewidth=2)
axes[0].set_xlabel('x', fontsize=12)
axes[0].set_ylabel('P(X = x)', fontsize=12)
axes[0].set_title('PMF: Binomial(10, 0.5)\nP(X=x) là XÁC SUẤT', 
                 fontsize=13, fontweight='bold')
axes[0].grid(axis='y', alpha=0.3)

# Highlight một giá trị
axes[0].bar([5], [pmf[5]], width=0.6, color='red', alpha=0.7, edgecolor='black', linewidth=2)
axes[0].text(5, pmf[5] + 0.02, f'P(X=5) = {pmf[5]:.3f}', 
            ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

# PDF - Liên tục
x_continuous = np.linspace(-4, 4, 200)
pdf = stats.norm.pdf(x_continuous, 0, 1)

axes[1].plot(x_continuous, pdf, 'b-', linewidth=2)
axes[1].fill_between(x_continuous, pdf, alpha=0.3)
axes[1].set_xlabel('x', fontsize=12)
axes[1].set_ylabel('f(x)', fontsize=12)
axes[1].set_title('PDF: Normal(0, 1)\nf(x) KHÔNG PHẢI xác suất', 
                 fontsize=13, fontweight='bold')
axes[1].grid(alpha=0.3)

# Highlight một điểm
x_point = 0
axes[1].scatter([x_point], [stats.norm.pdf(x_point, 0, 1)], 
               s=200, color='red', zorder=5, edgecolor='black', linewidth=2)
axes[1].text(x_point + 0.5, stats.norm.pdf(x_point, 0, 1), 
            f'f(0) = {stats.norm.pdf(0, 0, 1):.3f}\nNHƯNG P(X=0) = 0!', 
            fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.show()

# Bảng so sánh chi tiết
print("\n" + "="*70)
print("SO SÁNH PMF VÀ PDF".center(70))
print("="*70)
print(f"{'Đặc điểm':<30} | {'PMF (Rời rạc)':<18} | {'PDF (Liên tục)':<18}")
print("-"*70)
print(f"{'Ký hiệu':<30} | {'P(X = x)':<18} | {'f(x)':<18}")
print(f"{'Ý nghĩa':<30} | {'Xác suất':<18} | {'Mật độ xác suất':<18}")
print(f"{'Giá trị':<30} | {'0 ≤ P(X=x) ≤ 1':<18} | {'f(x) ≥ 0 (có thể >1)':<18}")
print(f"{'P(X = x)':<30} | {'Có nghĩa':<18} | {'= 0 (vô nghĩa)':<18}")
print(f"{'Tổng/Tích phân':<30} | {'Σ P(X=x) = 1':<18} | {'∫ f(x)dx = 1':<18}")
print(f"{'Xác suất khoảng':<30} | {'Σ P(X=x)':<18} | {'∫ f(x)dx':<18}")
print(f"{'Đơn vị':<30} | {'Không đơn vị':<18} | {'1/(đơn vị của X)':<18}")
print("="*70)
```

## 5. Các Sai lầm Thường gặp

### 5.1. Sai lầm 1: Nghĩ $$f(x)$$ là xác suất

```python
# SAI: "Xác suất chiều cao = 170 cm là f(170) = 0.04"
mu, sigma = 170, 10
wrong_prob = stats.norm.pdf(170, mu, sigma)
print(f"❌ SAI: P(X = 170) = {wrong_prob:.4f}")
print(f"✓ ĐÚNG: P(X = 170) = 0 (biến liên tục)")
print(f"✓ ĐÚNG: f(170) = {wrong_prob:.4f} là MẬT ĐỘ, không phải xác suất")
```

### 5.2. Sai lầm 2: Nghĩ $$f(x) \leq 1$$

```python
# Ví dụ: Uniform[0, 0.2]
x = np.linspace(-0.1, 0.3, 200)
pdf_uniform = np.where((x >= 0) & (x <= 0.2), 5, 0)

plt.figure(figsize=(10, 6))
plt.plot(x, pdf_uniform, 'b-', linewidth=2)
plt.fill_between(x, pdf_uniform, alpha=0.3)
plt.axhline(y=1, color='red', linestyle='--', linewidth=2, label='y = 1')
plt.xlabel('x', fontsize=12)
plt.ylabel('f(x)', fontsize=12)
plt.title('Uniform[0, 0.2]: f(x) = 5 > 1\nNhưng ∫f(x)dx = 5 × 0.2 = 1 ✓', 
         fontsize=13, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.ylim(0, 6)
plt.show()

print(f"❌ SAI: 'f(x) phải ≤ 1'")
print(f"✓ ĐÚNG: f(x) có thể > 1, miễn ∫f(x)dx = 1")
```

### 5.3. Sai lầm 3: So sánh $$f(x)$$ giữa các phân phối khác đơn vị

```python
# Không nên so sánh trực tiếp f(x) nếu đơn vị khác nhau
print("❌ SAI: So sánh f(170 cm) với f(1.70 m)")
print("✓ ĐÚNG: Chỉ so sánh XÁC SUẤT (không đơn vị)")
```

## 6. Ứng dụng trong Bayesian Statistics

### 6.1. Prior và Posterior là PDF

```python
# Prior: Beta(2, 2)
# Likelihood: Binomial (7 successes in 10 trials)
# Posterior: Beta(9, 5)

theta = np.linspace(0, 1, 200)
prior = stats.beta.pdf(theta, 2, 2)
posterior = stats.beta.pdf(theta, 9, 5)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# PDF
axes[0].plot(theta, prior, 'b-', linewidth=2, label='Prior: Beta(2, 2)')
axes[0].plot(theta, posterior, 'r-', linewidth=2, label='Posterior: Beta(9, 5)')
axes[0].fill_between(theta, posterior, alpha=0.3, color='red')
axes[0].set_xlabel('θ (tỷ lệ thành công)', fontsize=12)
axes[0].set_ylabel('f(θ)', fontsize=12)
axes[0].set_title('Prior và Posterior là PDF\nf(θ) là MẬT ĐỘ tin cậy', 
                 fontsize=13, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# Credible Interval
axes[1].plot(theta, posterior, 'r-', linewidth=2, label='Posterior')
axes[1].fill_between(theta, posterior, alpha=0.3, color='red')

# 95% Credible Interval
lower = stats.beta.ppf(0.025, 9, 5)
upper = stats.beta.ppf(0.975, 9, 5)
theta_ci = theta[(theta >= lower) & (theta <= upper)]
posterior_ci = stats.beta.pdf(theta_ci, 9, 5)
axes[1].fill_between(theta_ci, posterior_ci, alpha=0.5, color='green',
                    label=f'95% CI: [{lower:.3f}, {upper:.3f}]')

axes[1].set_xlabel('θ', fontsize=12)
axes[1].set_ylabel('f(θ)', fontsize=12)
axes[1].set_title('Credible Interval từ Posterior PDF', 
                 fontsize=13, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("=== Bayesian Inference ===")
print(f"Prior mean: {2/(2+2):.3f}")
print(f"Posterior mean: {9/(9+5):.3f}")
print(f"95% Credible Interval: [{lower:.3f}, {upper:.3f}]")
print(f"\nP({lower:.3f} ≤ θ ≤ {upper:.3f}) = 0.95")
```

### 6.2. Likelihood Function

```python
# Data: x = [1.2, 2.3, 1.8, 2.1, 1.9]
# Model: X ~ Normal(μ, σ=0.5)
# Likelihood: L(μ) = ∏ f(xᵢ \mid μ)

data = np.array([1.2, 2.3, 1.8, 2.1, 1.9])
sigma = 0.5

mu_range = np.linspace(0, 4, 200)
likelihood = np.ones_like(mu_range)

for x in data:
    likelihood *= stats.norm.pdf(x, mu_range, sigma)

# Normalize để vẽ
likelihood_normalized = likelihood / np.trapz(likelihood, mu_range)

plt.figure(figsize=(10, 6))
plt.plot(mu_range, likelihood_normalized, 'b-', linewidth=2, label='Likelihood (normalized)')
plt.fill_between(mu_range, likelihood_normalized, alpha=0.3)

# MLE
mu_mle = data.mean()
plt.axvline(mu_mle, color='red', linestyle='--', linewidth=2, 
           label=f'MLE: μ̂ = {mu_mle:.3f}')

plt.xlabel('μ', fontsize=12)
plt.ylabel('L(μ) (normalized)', fontsize=12)
plt.title('Likelihood Function là PDF của tham số\n(sau khi quan sát dữ liệu)', 
         fontsize=13, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.show()

print(f"Data: {data}")
print(f"MLE: μ̂ = {mu_mle:.4f}")
```

## 7. Tóm tắt Quan trọng

```python
# Tạo infographic tóm tắt
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111)
ax.axis('off')

summary_text = """
╔═══════════════════════════════════════════════════════════════════╗
║                  HÀM MẬT ĐỘ XÁC SUẤT (PDF)                       ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  1. ĐỊNH NGHĨA                                                    ║
║     • f(x) là MẬT ĐỘ xác suất, KHÔNG PHẢI xác suất              ║
║     • P(a ≤ X ≤ b) = ∫ₐᵇ f(x)dx                                  ║
║                                                                   ║
║  2. TÍNH CHẤT                                                     ║
║     ✓ f(x) ≥ 0 với mọi x                                         ║
║     ✓ ∫₋∞^∞ f(x)dx = 1                                           ║
║     ✓ f(x) CÓ THỂ > 1 (vì không phải xác suất!)                 ║
║     ✓ P(X = x) = 0 với biến liên tục                            ║
║                                                                   ║
║  3. Ý NGHĨA                                                       ║
║     • f(x) đo "mật độ" xác suất tại x                           ║
║     • f(x) cao → xác suất tập trung quanh x                     ║
║     • P(x ≤ X ≤ x+Δx) ≈ f(x)·Δx (với Δx nhỏ)                   ║
║                                                                   ║
║  4. ĐƠN VỊ                                                        ║
║     • Nếu X có đơn vị U, thì f(x) có đơn vị 1/U                 ║
║     • f(x)·dx không có đơn vị (là xác suất)                     ║
║                                                                   ║
║  5. SO VỚI PMF                                                    ║
║     • PMF: P(X=x) là XÁC SUẤT (0 ≤ P ≤ 1)                       ║
║     • PDF: f(x) là MẬT ĐỘ (có thể > 1)                          ║
║                                                                   ║
║  6. SAI LẦM THƯỜNG GẶP                                            ║
║     ❌ "f(x) là xác suất"                                        ║
║     ❌ "f(x) phải ≤ 1"                                           ║
║     ❌ "P(X = x) = f(x)"                                         ║
║                                                                   ║
║  7. TRONG BAYESIAN                                                ║
║     • Prior p(θ) là PDF                                          ║
║     • Posterior p(θ \mid x) là PDF                                    ║
║     • Likelihood L(θ) ∝ PDF                                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""

ax.text(0.5, 0.5, summary_text, fontsize=11, family='monospace',
       ha='center', va='center',
       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

plt.tight_layout()
plt.show()
```

## Bài tập

1. **Khái niệm**: Giải thích tại sao $$P(X = 170)$$ = 0 với biến liên tục, nhưng $$f(170)$$ có thể khác 0?

2. **Tính toán**: Cho $$f(x) = 2x$$ trên $$[0, 1]$$.
   - Kiểm tra $$\int_0^1 f(x)dx = 1$$
   - Tính $$P(0.2 \leq X \leq 0.5)$$
   - $$f(0.3)$$ có phải là xác suất không?

3. **So sánh**: Tạo 2 phân phối Normal với $$\sigma$$ khác nhau. So sánh $$f(x)$$ tại mean. Giải thích tại sao khác nhau.

4. **Đơn vị**: Chiều cao $$X \sim \mathcal{N}(170 \text{ cm}, 10^2)$$.
   - Tính $$f(170)$$ với đơn vị cm
   - Tính $$f(1.70)$$ với đơn vị m
   - Giải thích mối quan hệ

5. **Bayesian**: Cho Prior Beta(1, 1) và data: 3 successes in 5 trials.
   - Tìm Posterior
   - Vẽ Prior và Posterior PDF
   - Tính 90% Credible Interval

## Tài liệu tham khảo

1. **Wasserman, L. (2004).** *All of Statistics*. Springer. - Chapter 2
2. **Casella & Berger (2002).** *Statistical Inference*. Duxbury. - Chapter 1
3. **Seeing Theory - Probability Distributions** - https://seeing-theory.brown.edu/

---

*Bài học này giải thích chi tiết về PDF. Hiểu đúng PDF là nền tảng cho Bayesian Statistics!*

