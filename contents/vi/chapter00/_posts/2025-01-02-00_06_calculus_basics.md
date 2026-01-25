---
layout: post
title: "00-06: Giải tích Cơ bản"
chapter: '00'
order: 6
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu

Bài học này giới thiệu các khái niệm giải tích cần thiết cho Bayesian Statistics, bao gồm đạo hàm, tích phân, và tối ưu hóa.

## 1. Đạo hàm (Derivatives)

### 1.1. Định nghĩa

**Đạo hàm** đo tốc độ thay đổi của hàm số:

$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

**Ý nghĩa hình học**: Độ dốc của tiếp tuyến tại điểm $$x$$.

```python
import numpy as np
import matplotlib.pyplot as plt

# Hàm số
def f(x):
    return x**2

# Đạo hàm (giải tích)
def f_prime(x):
    return 2*x

# Đạo hàm số (numerical)
def numerical_derivative(f, x, h=1e-5):
    return (f(x + h) - f(x)) / h

# Vẽ hàm và tiếp tuyến
x = np.linspace(-3, 3, 100)
y = f(x)

x0 = 1.5
y0 = f(x0)
slope = f_prime(x0)

# Tiếp tuyến: y - y0 = slope * (x - x0)
tangent_y = y0 + slope * (x - x0)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2, label='f(x) = x²')
plt.plot(x, tangent_y, 'r--', linewidth=2, label=f'Tiếp tuyến tại x={x0}')
plt.scatter([x0], [y0], color='red', s=100, zorder=5)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Đạo hàm là Độ dốc của Tiếp tuyến')
plt.legend()
plt.grid(alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.axvline(x=0, color='k', linewidth=0.5)
plt.show()

# So sánh đạo hàm giải tích vs số
x_test = 2.0
analytical = f_prime(x_test)
numerical = numerical_derivative(f, x_test)
print(f"Đạo hàm tại x={x_test}:")
print(f"  Giải tích: {analytical}")
print(f"  Số: {numerical:.10f}")
```

### 1.2. Quy tắc Đạo hàm Cơ bản

| Hàm | Đạo hàm |
|-----|---------|
| $$c$$ (hằng số) | $$0$$ |
| $$x^n$$ | $$nx^{n-1}$$ |
| $$e^x$$ | $$e^x$$ |
| $$\ln(x)$$ | $$\frac{1}{x}$$ |
| $$\sin(x)$$ | $$\cos(x)$$ |
| $$\cos(x)$$ | $$-\sin(x)$$ |

**Quy tắc tổng**: $$(f + g)' = f' + g'$$

**Quy tắc tích**: $$(fg)' = f'g + fg'$$

**Quy tắc thương**: $$\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}$$

**Quy tắc chuỗi** (Chain rule): $$(f(g(x)))' = f'(g(x)) \cdot g'(x)$$

```python
# Ví dụ: f(x) = (x² + 1)³
def f(x):
    return (x**2 + 1)**3

# Đạo hàm bằng chain rule:
# f'(x) = 3(x² + 1)² · 2x = 6x(x² + 1)²
def f_prime(x):
    return 6*x * (x**2 + 1)**2

# Kiểm tra
x_test = 1.0
analytical = f_prime(x_test)
numerical = numerical_derivative(f, x_test)
print(f"\nf(x) = (x² + 1)³ tại x={x_test}:")
print(f"  Giải tích: {analytical}")
print(f"  Số: {numerical:.10f}")
```

### 1.3. Đạo hàm Riêng (Partial Derivatives)

Cho hàm nhiều biến $$f(x, y)$$, đạo hàm riêng theo $$x$$:

$$\frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x+h, y) - f(x, y)}{h}$$

(giữ $$y$$ cố định)

```python
# Hàm 2 biến: f(x, y) = x²y + y³
def f(x, y):
    return x**2 * y + y**3

# Đạo hàm riêng
def df_dx(x, y):
    return 2*x*y

def df_dy(x, y):
    return x**2 + 3*y**2

# Vẽ hàm 3D
from mpl_toolkits.mplot3d import Axes3D

x = np.linspace(-2, 2, 50)
y = np.linspace(-2, 2, 50)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig = plt.figure(figsize=(14, 5))

# Surface plot
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('f(x, y)')
ax1.set_title('f(x, y) = x²y + y³')

# Contour plot với gradient
ax2 = fig.add_subplot(122)
contour = ax2.contour(X, Y, Z, levels=15, cmap='viridis')
ax2.clabel(contour, inline=True, fontsize=8)

# Vẽ gradient tại một số điểm
x_points = np.linspace(-1.5, 1.5, 8)
y_points = np.linspace(-1.5, 1.5, 8)
for xi in x_points:
    for yi in y_points:
        dx = df_dx(xi, yi)
        dy = df_dy(xi, yi)
        ax2.quiver(xi, yi, dx, dy, color='red', scale=50, width=0.003)

ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_title('Contour và Gradient')
ax2.set_aspect('equal')

plt.tight_layout()
plt.show()

# Tính tại điểm cụ thể
x0, y0 = 1, 2
print(f"\nTại (x, y) = ({x0}, {y0}):")
print(f"  f = {f(x0, y0)}")
print(f"  ∂f/∂x = {df_dx(x0, y0)}")
print(f"  ∂f/∂y = {df_dy(x0, y0)}")
```

### 1.4. Gradient

**Gradient** là vector của tất cả đạo hàm riêng:

$$\nabla f = \begin{bmatrix} \frac{\partial f}{\partial x_1} \\ \frac{\partial f}{\partial x_2} \\ \vdots \\ \frac{\partial f}{\partial x_n} \end{bmatrix}$$

**Ý nghĩa**: Hướng tăng nhanh nhất của hàm số.

```python
def gradient_f(x, y):
    return np.array([df_dx(x, y), df_dy(x, y)])

x0, y0 = 1, 1
grad = gradient_f(x0, y0)
print(f"\nGradient tại ({x0}, {y0}): {grad}")
print(f"Độ lớn: {np.linalg.norm(grad):.4f}")
```

## 2. Tích phân (Integrals)

### 2.1. Tích phân Xác định

**Ý nghĩa**: Diện tích dưới đường cong.

$$\int_a^b f(x) dx$$

```python
# Hàm số
def f(x):
    return x**2

# Tích phân giải tích: ∫x² dx = x³/3
def F(x):
    return x**3 / 3

# Tích phân từ 0 đến 2
a, b = 0, 2
integral_analytical = F(b) - F(a)

# Tích phân số (numerical)
from scipy import integrate
integral_numerical, error = integrate.quad(f, a, b)

print(f"Tích phân ∫₀² x² dx:")
print(f"  Giải tích: {integral_analytical:.6f}")
print(f"  Số: {integral_numerical:.6f}")

# Vẽ
x = np.linspace(0, 3, 100)
y = f(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2, label='f(x) = x²')

# Tô vùng tích phân
x_fill = np.linspace(a, b, 100)
y_fill = f(x_fill)
plt.fill_between(x_fill, y_fill, alpha=0.3, color='blue', 
                label=f'Diện tích = {integral_analytical:.2f}')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Tích phân = Diện tích dưới đường cong')
plt.legend()
plt.grid(alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.axvline(x=0, color='k', linewidth=0.5)
plt.show()
```

### 2.2. Tích phân trong Xác suất

**PDF** (Probability Density Function) phải thỏa:

$$\int_{-\infty}^{\infty} f(x) dx = 1$$

**Xác suất**:

$$P(a \leq X \leq b) = \int_a^b f(x) dx$$

```python
from scipy import stats

# Normal distribution
mu, sigma = 0, 1
x = np.linspace(-4, 4, 1000)
pdf = stats.norm.pdf(x, mu, sigma)

# Tính P(-1 ≤ X ≤ 1)
a, b = -1, 1
prob, _ = integrate.quad(lambda x: stats.norm.pdf(x, mu, sigma), a, b)

plt.figure(figsize=(10, 6))
plt.plot(x, pdf, 'b-', linewidth=2, label='N(0, 1)')

# Tô vùng xác suất
x_fill = np.linspace(a, b, 100)
pdf_fill = stats.norm.pdf(x_fill, mu, sigma)
plt.fill_between(x_fill, pdf_fill, alpha=0.3, color='blue',
                label=f'P(-1 ≤ X ≤ 1) = {prob:.4f}')

plt.xlabel('x')
plt.ylabel('Mật độ')
plt.title('Xác suất = Diện tích dưới PDF')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# So sánh với CDF
prob_cdf = stats.norm.cdf(b, mu, sigma) - stats.norm.cdf(a, mu, sigma)
print(f"\nP(-1 ≤ X ≤ 1):")
print(f"  Tích phân: {prob:.6f}")
print(f"  CDF: {prob_cdf:.6f}")
```

### 2.3. Tích phân Đa biến

$$\int \int f(x, y) \, dx \, dy$$

```python
# Hàm 2 biến
def f(x, y):
    return x * y

# Tích phân trên [0,1] × [0,2]
result, error = integrate.dblquad(f, 0, 2, 0, 1)
print(f"\n∫₀¹ ∫₀² xy dy dx = {result:.6f}")

# Giải tích: ∫₀¹ x dx · ∫₀² y dy = [x²/2]₀¹ · [y²/2]₀² = 0.5 · 2 = 1
analytical = 0.5 * 2
print(f"Giải tích: {analytical}")
```

## 3. Tối ưu hóa (Optimization)

### 3.1. Cực trị

**Điều kiện cần** (Necessary condition):

$$f'(x) = 0$$

**Điều kiện đủ** (Sufficient condition):
- $$f''(x) > 0$$: Cực tiểu (minimum)
- $$f''(x) < 0$$: Cực đại (maximum)

```python
# Hàm số: f(x) = x³ - 6x² + 9x + 1
def f(x):
    return x**3 - 6*x**2 + 9*x + 1

def f_prime(x):
    return 3*x**2 - 12*x + 9

def f_double_prime(x):
    return 6*x - 12

# Tìm điểm tới hạn: f'(x) = 0
# 3x² - 12x + 9 = 0
# x² - 4x + 3 = 0
# (x-1)(x-3) = 0
critical_points = [1, 3]

x = np.linspace(-1, 5, 200)
y = f(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2, label='f(x)')

for xc in critical_points:
    yc = f(xc)
    f2 = f_double_prime(xc)
    
    if f2 > 0:
        marker = 'v'  # Minimum
        label = f'Min tại x={xc}'
        color = 'green'
    else:
        marker = '^'  # Maximum
        label = f'Max tại x={xc}'
        color = 'red'
    
    plt.scatter([xc], [yc], s=200, marker=marker, color=color, 
               label=label, zorder=5, edgecolor='black', linewidth=2)
    
    print(f"\nx = {xc}:")
    print(f"  f(x) = {yc:.4f}")
    print(f"  f'(x) = {f_prime(xc):.4f}")
    print(f"  f''(x) = {f2:.4f}")
    print(f"  → {'Cực tiểu' if f2 > 0 else 'Cực đại'}")

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Tìm Cực trị')
plt.legend()
plt.grid(alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.show()
```

### 3.2. Gradient Descent

**Thuật toán** tìm minimum:

$$x_{n+1} = x_n - \alpha \nabla f(x_n)$$

với $$\alpha$$ là learning rate.

```python
# Hàm 2 biến: f(x, y) = x² + y²
def f(x, y):
    return x**2 + y**2

def gradient(x, y):
    return np.array([2*x, 2*y])

# Gradient descent
def gradient_descent(x0, y0, alpha=0.1, n_iter=20):
    path = [(x0, y0)]
    x, y = x0, y0
    
    for i in range(n_iter):
        grad = gradient(x, y)
        x = x - alpha * grad[0]
        y = y - alpha * grad[1]
        path.append((x, y))
    
    return np.array(path)

# Chạy từ điểm khởi đầu
x0, y0 = 3, 2
path = gradient_descent(x0, y0, alpha=0.1, n_iter=20)

# Vẽ
x = np.linspace(-4, 4, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

plt.figure(figsize=(10, 8))
contour = plt.contour(X, Y, Z, levels=20, cmap='viridis')
plt.clabel(contour, inline=True, fontsize=8)

# Vẽ đường đi
plt.plot(path[:, 0], path[:, 1], 'ro-', linewidth=2, markersize=8,
        label='Gradient Descent')
plt.scatter([0], [0], s=300, marker='*', color='gold', 
           edgecolor='black', linewidth=2, label='Minimum', zorder=5)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Gradient Descent')
plt.legend()
plt.grid(alpha=0.3)
plt.axis('equal')
plt.show()

print("\nGradient Descent:")
print(f"Bắt đầu: ({x0}, {y0}), f = {f(x0, y0):.4f}")
print(f"Kết thúc: ({path[-1, 0]:.6f}, {path[-1, 1]:.6f}), f = {f(path[-1, 0], path[-1, 1]):.6f}")
```

### 3.3. Maximum Likelihood Estimation (MLE)

**Ví dụ**: Ước lượng tham số $$\mu$$ của Normal distribution.

**Likelihood**:

$$L(\mu) = \prod_{i=1}^{n} \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x_i - \mu)^2}{2\sigma^2}\right)$$

**Log-likelihood**:

$$\ell(\mu) = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^{n}(x_i - \mu)^2$$

**Tìm maximum**: $$\frac{d\ell}{d\mu} = 0$$

$$\Rightarrow \hat{\mu} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

```python
# Dữ liệu
np.random.seed(42)
true_mu = 5
sigma = 2
data = np.random.normal(true_mu, sigma, 100)

# Log-likelihood function
def log_likelihood(mu, data, sigma):
    n = len(data)
    return -n/2 * np.log(2*np.pi*sigma**2) - 1/(2*sigma**2) * np.sum((data - mu)**2)

# Vẽ log-likelihood
mu_range = np.linspace(3, 7, 100)
ll_values = [log_likelihood(mu, data, sigma) for mu in mu_range]

# MLE
mu_mle = data.mean()

plt.figure(figsize=(10, 6))
plt.plot(mu_range, ll_values, 'b-', linewidth=2, label='Log-likelihood')
plt.axvline(mu_mle, color='red', linestyle='--', linewidth=2, 
           label=f'MLE: μ̂ = {mu_mle:.3f}')
plt.axvline(true_mu, color='green', linestyle='--', linewidth=2,
           label=f'True: μ = {true_mu}')
plt.xlabel('μ')
plt.ylabel('Log-likelihood')
plt.title('Maximum Likelihood Estimation')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print(f"\nTrue μ: {true_mu}")
print(f"MLE μ̂: {mu_mle:.4f}")
print(f"Sample mean: {data.mean():.4f}")
```

## 4. Ứng dụng trong Bayesian Statistics

### 4.1. Posterior Mode (MAP)

**Maximum A Posteriori** (MAP): Tìm mode của posterior.

$$\hat{\theta}_{MAP} = \arg\max_\theta p(\theta \mid \mathbf{x})$$

Tương đương:

$$\hat{\theta}_{MAP} = \arg\max_\theta [\log p(\mathbf{x} \mid \theta) + \log p(\theta)]$$

### 4.2. Laplace Approximation

Xấp xỉ posterior bằng Normal distribution tại mode:

$$p(\theta \mid \mathbf{x}) \approx \mathcal{N}\left(\hat{\theta}, \left[-\frac{d^2 \log p(\theta \mid \mathbf{x})}{d\theta^2}\bigg|_{\hat{\theta}}\right]^{-1}\right)$$

```python
# Ví dụ: Beta posterior
# Prior: Beta(2, 2)
# Likelihood: Binomial(n, theta)
# Data: 7 successes in 10 trials

alpha_prior, beta_prior = 2, 2
n_success, n_total = 7, 10

# Posterior: Beta(alpha_prior + n_success, beta_prior + n_total - n_success)
alpha_post = alpha_prior + n_success
beta_post = beta_prior + n_total - n_success

# Log posterior (unnormalized)
def log_posterior(theta):
    if theta <= 0 or theta >= 1:
        return -np.inf
    log_prior = (alpha_prior - 1) * np.log(theta) + (beta_prior - 1) * np.log(1 - theta)
    log_lik = n_success * np.log(theta) + (n_total - n_success) * np.log(1 - theta)
    return log_prior + log_lik

# MAP (mode)
theta_map = (alpha_post - 1) / (alpha_post + beta_post - 2)

# Laplace approximation
# Tính đạo hàm bậc 2
def log_posterior_second_deriv(theta):
    return -(alpha_post - 1) / theta**2 - (beta_post - 1) / (1 - theta)**2

variance_laplace = -1 / log_posterior_second_deriv(theta_map)
std_laplace = np.sqrt(variance_laplace)

# Vẽ
theta = np.linspace(0.01, 0.99, 200)
posterior = stats.beta.pdf(theta, alpha_post, beta_post)
laplace_approx = stats.norm.pdf(theta, theta_map, std_laplace)

plt.figure(figsize=(10, 6))
plt.plot(theta, posterior, 'b-', linewidth=2, label='True Posterior (Beta)')
plt.plot(theta, laplace_approx, 'r--', linewidth=2, label='Laplace Approximation (Normal)')
plt.axvline(theta_map, color='green', linestyle='--', 
           label=f'MAP: θ̂ = {theta_map:.3f}')
plt.xlabel('θ')
plt.ylabel('Mật độ')
plt.title('Laplace Approximation')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print(f"\nMAP: {theta_map:.4f}")
print(f"Laplace std: {std_laplace:.4f}")
print(f"True std: {np.sqrt(alpha_post * beta_post / ((alpha_post + beta_post)**2 * (alpha_post + beta_post + 1))):.4f}")
```

## Bài tập

1. **Đạo hàm**: Tính đạo hàm của:
   - $$f(x) = 3x^4 - 2x^2 + 5$$
   - $$g(x) = e^{x^2}$$
   - $$h(x) = \ln(x^2 + 1)$$

2. **Đạo hàm riêng**: Cho $$f(x, y) = x^2y + xy^2$$. Tính $$\frac{\partial f}{\partial x}$$ và $$\frac{\partial f}{\partial y}$$.

3. **Tích phân**: Tính:
   - $$\int_0^1 x^2 dx$$
   - $$\int_1^e \frac{1}{x} dx$$
   - $$\int_{-\infty}^{\infty} e^{-x^2} dx$$ (gợi ý: $$\sqrt{\pi}$$)

4. **Tối ưu**: Tìm cực trị của $$f(x) = x^3 - 3x + 1$$.

5. **MLE**: Cho dữ liệu từ Exponential($$\lambda$$). Tìm MLE của $$\lambda$$.
   - Likelihood: $$L(\lambda) = \prod_{i=1}^{n} \lambda e^{-\lambda x_i}$$
   - Gợi ý: $$\hat{\lambda} = \frac{n}{\sum x_i}$$

## Tài liệu tham khảo

1. **Stewart, J. (2015).** *Calculus: Early Transcendentals*. Cengage Learning.
2. **3Blue1Brown - Essence of Calculus** - https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr
3. **SciPy Integrate** - https://docs.scipy.org/doc/scipy/reference/integrate.html

---

*Bài học này hoàn thành phần kiến thức cơ bản. Bạn đã sẵn sàng cho Bayesian Statistics!*

