---
layout: post
title: "Bài 0.9: Giải tích Cơ bản"
chapter: '00'
order: 9
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

Thống kê Bayes về bản chất là một cuộc đối thoại giữa **hai phép toán giải tích**: *đạo hàm* và *tích phân*. Khi bạn muốn tìm giá trị tham số hợp lý nhất (ước lượng cực đại hợp lý MLE hoặc cực đại hậu nghiệm MAP), bạn lấy đạo hàm và giải phương trình bằng 0. Nhưng khi bạn muốn biết *toàn bộ phân phối hậu nghiệm*, tính xác suất biên $$p(y) = \int p(y \mid 	heta)p(	heta)\,d	heta$$ hay dự báo cho dữ liệu mới, bạn buộc phải đối mặt với **tích phân**.

Chính sự chênh lệch độ khó giữa hai phép toán này — lấy đạo hàm luôn có quy tắc máy móc (lan truyền ngược / autodiff), còn lấy tích phân nhiều chiều hầu như vô phương giải tay — đã sinh ra cả hai nhánh công nghệ lớn nhất của Bayes hiện đại: **MCMC** (dùng lấy mẫu ngẫu nhiên để tính tích phân) và **Variational Inference** (biến bài toán tích phân thành bài toán tối ưu bằng đạo hàm).

---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vai trò của đạo hàm, tích phân và tối ưu hóa trong suy luận thống kê Bayesian. Cụ thể, bạn sẽ nắm cách dùng đạo hàm để phân tích độ nhạy và tìm cực trị, dùng tích phân để chuẩn hóa mật độ và tính xác suất trên miền liên tục, và dùng tối ưu hóa để tìm ước lượng xấp xỉ (như MAP) trước hoặc song song với lấy mẫu hậu nghiệm.

## Bản đồ kiến thức nền: Đạo hàm–Gradient, Tích phân chuẩn hóa và Cầu nối sang HMC / Variational Inference

Ba trụ cột giải tích mà mọi nhà thực hành Bayes cần nắm chắc:

- **Vi phân, Gradient & Ma trận Hessian:** Gradient $$
abla_	heta \log p(	heta \mid y)$$ chỉ hướng tăng nhanh nhất của log-posterior, giúp tìm điểm MAP. Ma trận Hessian $$\mathbf{H} = 
abla^2_	heta \log p(	heta \mid y)$$ đo độ cong tại đỉnh: đỉnh càng nhọn (độ cong âm lớn), phương sai hậu nghiệm càng nhỏ. Trong **Hamiltonian Monte Carlo (HMC / NUTS)** — động cơ mặc định của Stan và PyMC — gradient của log-posterior đóng vai trò "lực hấp dẫn" dẫn đường cho hạt chuyển động mượt mà qua không gian hàng nghìn chiều.
- **Tích phân & Chuẩn hóa (Marginal Likelihood / Evidence):** Mẫu số $$Z = p(y) = \int p(y \mid 	heta)p(	heta)\,d	heta$$ là diện tích dưới đường cong chưa chuẩn hóa. Nếu không chuẩn hóa được bằng giải tích (như prior liên hợp), ta cần tích phân số (Grid), lấy mẫu (MCMC) hoặc cận dưới biến phân (ELBO trong Variational Inference).
- **Biến đổi biến số & Định thức Jacobian:** Khi đổi tham số (ví dụ từ độ lệch chuẩn $$\sigma > 0$$ sang $$\phi = \log \sigma \in \mathbb{R}$$ để tối ưu không ràng buộc), mật độ xác suất phải nhân thêm $$\left\lvert rac{d\sigma}{d\phi} ightvert = e^\phi$$ để bảo toàn tổng xác suất bằng 1.

---

## Giới thiệu: Vì sao giải tích là lõi của thống kê Bayesian liên tục?

Nhiều mô hình Bayesian làm việc với tham số liên tục, trong đó ba thao tác toán học xuất hiện thường xuyên: lấy đạo hàm để tối ưu hàm log-posterior, lấy tích phân để chuẩn hóa phân phối và biên hóa (marginalize) biến ẩn, và dùng gradient để thiết kế các thuật toán tính toán hiệu quả. Vì vậy, giải tích không phải phần phụ trợ mà là công cụ lõi giúp chuyển mô hình xác suất thành suy luận tính toán được.

Trong bài này, mỗi công thức được tiếp cận theo hai tầng: ký hiệu toán học hình thức và ý nghĩa thống kê thực tế. Cách đọc hai tầng này sẽ hỗ trợ trực tiếp cho các chương MCMC, hồi quy Bayesian và kiểm tra mô hình (model checking).

## Khung liên hệ với quy trình Bayesian

Một quy trình Bayesian điển hình có thể tóm gọn như sau:

$$
\text{prior} \times \text{likelihood} \propto \text{posterior (unnormalized)}.
$$

Từ biểu thức này, giải tích tham gia ở hai bước chính:

1. **Đạo hàm**: tìm điểm cực đại của log-posterior (ước lượng MAP, xấp xỉ Laplace).
2. **Tích phân**: chuẩn hóa phân phối hậu nghiệm hoặc tính xác suất và kỳ vọng trên miền liên tục.

## 1. Đạo hàm (Derivatives)

### 1.1. Định nghĩa

**Đạo hàm** đo tốc độ thay đổi tức thời của hàm số:

$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

**Ý nghĩa hình học**: độ dốc của tiếp tuyến với đồ thị tại điểm $$x$$.

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

**Quy tắc hàm hợp (Chain rule)**: $$(f(g(x)))' = f'(g(x)) \cdot g'(x)$$

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

Với hàm nhiều biến $$f(x, y)$$, đạo hàm riêng theo $$x$$ (khi giữ $$y$$ cố định) là:

$$\frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x+h, y) - f(x, y)}{h}$$

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

**Gradient** là vector gồm tất cả các đạo hàm riêng của hàm số:

$$\nabla f = \begin{bmatrix} \frac{\partial f}{\partial x_1} \\ \frac{\partial f}{\partial x_2} \\ \vdots \\ \frac{\partial f}{\partial x_n} \end{bmatrix}$$

**Ý nghĩa**: vector gradient chỉ hướng tăng nhanh nhất của hàm số.

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

**Ý nghĩa hình học**: diện tích (có dấu) giới hạn giữa đồ thị hàm số và trục hoành trên đoạn $$[a, b]$$:

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

Một **hàm mật độ xác suất (PDF)** hợp lệ phải thỏa mãn điều kiện chuẩn hóa:

$$\int_{-\infty}^{\infty} f(x) dx = 1$$

Khi đó, **xác suất** để biến ngẫu nhiên $$X$$ rơi vào đoạn $$[a, b]$$ là:

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

**Điều kiện cần** (necessary condition) để điểm $$x$$ là cực trị của hàm khả vi là:

$$f'(x) = 0$$

**Điều kiện đủ** (sufficient condition) dựa trên đạo hàm bậc hai:
- $$f''(x) > 0$$: điểm cực tiểu (minimum).
- $$f''(x) < 0$$: điểm cực đại (maximum).

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

**Thuật toán** tìm cực tiểu bằng cách cập nhật ngược hướng gradient:

$$x_{n+1} = x_n - \alpha \nabla f(x_n)$$

trong đó $$\alpha$$ là tốc độ học (learning rate).

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

### 3.3. Ước lượng Hợp lý Cực đại (Maximum Likelihood Estimation — MLE)

**Ví dụ**: ước lượng tham số $$\mu$$ của phân phối Normal khi biết $$\sigma$$.

**Hàm hợp lý (Likelihood)**:

$$L(\mu) = \prod_{i=1}^{n} \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x_i - \mu)^2}{2\sigma^2}\right)$$

**Log-likelihood**:

$$\ell(\mu) = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^{n}(x_i - \mu)^2$$

**Tìm cực đại** bằng cách giải $$\frac{d\ell}{d\mu} = 0$$:

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

## 4. Ứng dụng trong Thống kê Bayesian

### 4.1. Điểm Cực đại Hậu nghiệm (MAP)

**Maximum A Posteriori (MAP)** tìm mode (điểm có mật độ lớn nhất) của phân phối hậu nghiệm:

$$\hat{\theta}_{MAP} = \arg\max_\theta p(\theta \mid \mathbf{x})$$

Tương đương trên thang log:

$$\hat{\theta}_{MAP} = \arg\max_\theta [\log p(\mathbf{x} \mid \theta) + \log p(\theta)]$$

### 4.2. Xấp xỉ Laplace (Laplace Approximation)

Xấp xỉ phân phối hậu nghiệm bằng một phân phối Normal đặt tâm tại mode $$\hat{\theta}$$:

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

## Khung giải thích (nên đọc chậm): Từ đạo hàm tìm đỉnh MAP đến xấp xỉ Laplace bằng tay

Hãy đọc chậm chuỗi 4 bước nối liền giải tích 1 với một công cụ cực mạnh của thống kê Bayes là **xấp xỉ Laplace** (Laplace Approximation):

1. **Viết log-posterior chưa chuẩn hóa:** $$g(	heta) = \log p(y \mid 	heta) + \log p(	heta)$$ (bỏ hằng số $$\log p(y)$$ vì đạo hàm của hằng số bằng 0).
2. **Giải $$g'(	heta) = 0$$ để tìm đỉnh $$\hat{	heta}_{	ext{MAP}}$$:** Đây là điểm có mật độ hậu nghiệm cao nhất.
3. **Tính đạo hàm bậc hai $$g''(\hat{	heta}_{	ext{MAP}})$$ để đo độ cong:** Vì là cực đại nên $$g''(\hat{	heta}_{	ext{MAP}}) < 0$$.
4. **Khai triển Taylor bậc 2 quanh đỉnh:** $$g(	heta) pprox g(\hat{	heta}) + rac{1}{2} g''(\hat{	heta})(	heta - \hat{	heta})^2$$. So sánh với log mật độ Chuẩn $$-rac{(	heta - \mu)^2}{2\sigma^2}$$, ta lập tức thu được xấp xỉ hậu nghiệm:
   $$	heta \mid y pprox \mathcal{N}\!\left(\hat{	heta}_{	ext{MAP}},\; rac{-1}{g''(\hat{	heta}_{	ext{MAP}})}ight).$$

### Ví dụ tính toán cầm tay chỉ việc: Tìm MAP và phương sai xấp xỉ Laplace cho mô hình Beta–Binomial

Giả sử bạn dùng prior $$	ext{Beta}(2, 2)$$ và quan sát $$k = 7$$ thành công trong $$n = 10$$ lần thử. Ta đã biết hậu nghiệm chính xác là $$	ext{Beta}(9, 5)$$, nên đây là cơ hội tuyệt vời để kiểm chứng phép tính đạo hàm bằng tay!

- **Bước 1 — Log-posterior chưa chuẩn hóa:**
  $$g(	heta) = 8 \ln 	heta + 4 \ln(1 - 	heta).$$
- **Bước 2 — Lấy đạo hàm bậc 1 và cho bằng 0:**
  $$g'(	heta) = rac{8}{	heta} - rac{4}{1 - 	heta} = 0 \implies 8(1 - 	heta) = 4	heta \implies 12	heta = 8 \implies \hat{	heta}_{	ext{MAP}} = rac{2}{3} pprox 0.6667.$$
- **Bước 3 — Lấy đạo hàm bậc 2 tại $$\hat{	heta} = 2/3$$:**
  $$g''(	heta) = -rac{8}{	heta^2} - rac{4}{(1-	heta)^2}.$$
  Thay $$	heta = 2/3$$ và $$1 - 	heta = 1/3$$:
  $$g''(2/3) = -rac{8}{4/9} - rac{4}{1/9} = -18 - 36 = -54.$$
- **Bước 4 — Suy ra phương sai và độ lệch chuẩn xấp xỉ Laplace:**
  $$\hat{\sigma}^2 = rac{-1}{-54} = rac{1}{54} pprox 0.01852 \implies \hat{\sigma} pprox 0.1361.$$
  Đối chiếu với độ lệch chuẩn chính xác của $$	ext{Beta}(9, 5)$$: $$\sqrt{rac{9 	imes 5}{14^2 	imes 15}} = \sqrt{rac{45}{2940}} pprox 0.1237$$ — chỉ bằng vài dòng đạo hàm tay, ta đã xấp xỉ sát gần đúng!

**Hiểu lầm cần tránh:** Nghĩ rằng tìm được MAP là đã làm xong suy diễn Bayes. MAP chỉ là *một điểm duy nhất*; khi hậu nghiệm đa đỉnh hoặc lệch mạnh, MAP có thể nằm rất xa vùng chứa phần lớn khối lượng xác suất.

**Kiểm tra nhanh:** Nếu cỡ mẫu tăng gấp 10 lần ($$k=70, n=100$$), $$g''(\hat{	heta})$$ lớn gấp khoảng 10 lần, nên độ lệch chuẩn hậu nghiệm thu nhỏ lại khoảng $$\sqrt{10} pprox 3.16$$ lần — đúng quy luật hội tụ $$1/\sqrt{n}$$.

---

## Video tham khảo

- [The paradox of the derivative | Chapter 2, Essence of calculus](https://www.youtube.com/watch?v=9vKqVkMQHKk) — 3Blue1Brown, English. **Xem trước.** Giải thích trực quan đạo hàm như độ nhạy của hàm số khi đầu vào thay đổi nhỏ.
- [Integration and the fundamental theorem of calculus | Chapter 8, Essence of calculus](https://www.youtube.com/watch?v=rfG8ce4nNh0) — 3Blue1Brown, English. Trình bày tích phân như phép cộng dồn các phần tử nhỏ, hỗ trợ chuẩn hóa phân phối và tính xác suất liên tục.
- [Gradient descent, how neural networks learn | Deep Learning Chapter 2](https://www.youtube.com/watch?v=IHZwWFHWa-w) — 3Blue1Brown, English. Minh họa cơ chế đi ngược hướng dốc nhất của gradient descent, áp dụng trực tiếp cho phần tối ưu hóa trong bài.

## Bài tập

1. **Đạo hàm**: Tính đạo hàm của các hàm sau:
   - $$f(x) = 3x^4 - 2x^2 + 5$$
   - $$g(x) = e^{x^2}$$
   - $$h(x) = \ln(x^2 + 1)$$

2. **Đạo hàm riêng**: Cho $$f(x, y) = x^2y + xy^2$$. Tính $$\frac{\partial f}{\partial x}$$ và $$\frac{\partial f}{\partial y}$$.

3. **Tích phân**: Tính các tích phân sau:
   - $$\int_0^1 x^2 dx$$
   - $$\int_1^e \frac{1}{x} dx$$
   - $$\int_{-\infty}^{\infty} e^{-x^2} dx$$ (gợi ý: $$\sqrt{\pi}$$)

4. **Tối ưu hóa**: Tìm cực trị của hàm số $$f(x) = x^3 - 3x + 1$$.

5. **MLE**: Cho dữ liệu lấy mẫu độc lập từ phân phối $$\text{Exponential}(\lambda)$$. Tìm ước lượng MLE của $$\lambda$$:
   - Hàm hợp lý: $$L(\lambda) = \prod_{i=1}^{n} \lambda e^{-\lambda x_i}$$
   - Gợi ý: $$\hat{\lambda} = \frac{n}{\sum x_i}$$

## Tài liệu tham khảo

1. **Stewart, J. (2015).** *Calculus: Early Transcendentals*. Cengage Learning.
2. **3Blue1Brown - Essence of Calculus** - https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr
3. **SciPy Integrate** - https://docs.scipy.org/doc/scipy/reference/integrate.html

---

*Bài học tiếp theo: [0.10 Hàm Mật độ Xác suất (PDF)]({{ site.baseurl }}/contents/vi/chapter00/00_07_probability_density_functions/)*
