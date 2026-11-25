---
layout: post
title: "Bài 0.8: Đại số Tuyến tính Cơ bản"
chapter: '00'
order: 8
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

Khi mô hình thống kê chỉ có một tham số $$	heta$$, ta có thể viết mọi thứ bằng đại số phổ thông. Nhưng đời thực hiếm khi dừng ở một biến: hồi quy đa biến có hàng chục hệ số $$oldsymbol{eta}$$, phân phối Chuẩn đa biến có cả ma trận hiệp phương sai $$oldsymbol{\Sigma}$$, và mạng nơ-ron Bayes có hàng nghìn trọng số tương tác chéo. Đại số tuyến tính chính là chiếc kính viễn vọng giúp nén hàng nghìn phương trình lộn xộn thành một dòng gọn sắc: $$\mathbf{y} = \mathbf{X}oldsymbol{eta} + oldsymbol{arepsilon}$$.

Trong thống kê Bayes, đại số tuyến tính còn mang ý nghĩa hình học trực tiếp: **trị riêng và vector riêng của ma trận hiệp phương sai cho ta biết các trục chính của "đám mây bất định" hậu nghiệm**, quyết định tốc độ hội tụ của mọi thuật toán MCMC.

---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vì sao đại số tuyến tính là nền tảng toán học của mô hình thống kê Bayesian: dữ liệu được biểu diễn dưới dạng vector và ma trận, tham số hồi quy được viết thành toán tử tuyến tính, và nhiều thuật toán suy diễn dựa trực tiếp vào các phép biến đổi tuyến tính. Bạn cũng sẽ nắm được ý nghĩa hình học của các phép toán thay vì chỉ thao tác ký hiệu.

## Kiến thức cần nhớ: Không gian vector, Ma trận xác định dương và Hồi quy Bayes đa biến

Ba trụ cột đại số tuyến tính thiết yếu cho suy diễn Bayes:

- **Tích ma trận & Chiếu trực giao (Linear Maps & Projections):** Ma trận thiết kế $$\mathbf{X}$$ ánh xạ vector tham số $$oldsymbol{eta}$$ sang không gian dự đoán $$\hat{\mathbf{y}} = \mathbf{X}oldsymbol{eta}$$. Nghiệm bình phương tối thiểu cổ điển $$\hat{oldsymbol{eta}}_{	ext{OLS}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$ thực chất là phép chiếu trực giao vector dữ liệu $$\mathbf{y}$$ xuống không gian cột của $$\mathbf{X}$$.
- **Ma trận đối xứng xác định dương & Phân rã phổ (SPD Matrices & Eigendecomposition):** Mọi ma trận hiệp phương sai $$oldsymbol{\Sigma}$$ và ma trận độ chính xác $$oldsymbol{\Lambda} = oldsymbol{\Sigma}^{-1}$$ hợp lệ đều đối xứng và bán xác định dương (mọi trị riêng $$\lambda_i \ge 0$$). Phân rã Cholesky $$oldsymbol{\Sigma} = \mathbf{L}\mathbf{L}^T$$ là công cụ cốt lõi để sinh mẫu Chuẩn đa biến và tính log-determinant ổn định mà không cần nghịch đảo ma trận trực tiếp.
- **Cầu nối sang Hồi quy Tuyến tính Bayes (Ridge = Gaussian Prior):** Khi đặt prior Chuẩn $$oldsymbol{eta} \sim \mathcal{N}(\mathbf{0}, 	au^2 \mathbf{I})$$, ma trận độ chính xác hậu nghiệm trở thành $$\mathbf{X}^T\mathbf{X}/\sigma^2 + \mathbf{I}/	au^2$$. Phép cộng $$\lambda \mathbf{I}$$ vào đường chéo làm tăng mọi trị riêng thêm $$\lambda > 0$$, giúp ma trận **luôn khả nghịch** ngay cả khi dữ liệu bị đa cộng tuyến!

---

## Giới thiệu: Từ công thức rời rạc đến cấu trúc tuyến tính

Khi số biến tăng lên, việc viết mô hình bằng từng phương trình riêng lẻ trở nên rườm rà và khó theo dõi. Đại số tuyến tính giải quyết vấn đề này bằng cách gom các đại lượng vào vector và ma trận, giúp nhìn mô hình như một cấu trúc gọn gàng và thống nhất. Hầu hết mô hình Bayesian hiện đại — từ hồi quy tuyến tính, GLM đến mô hình phân cấp — đều được biểu diễn và tính toán hiệu quả trên nền tảng này.

Nếu Bài 0.7 cung cấp công cụ lập trình bằng Python, thì bài học này cung cấp ngôn ngữ toán học tương ứng cho các chương mô hình hóa phía sau.

## Cầu nối sang suy luận Bayesian

Nhiều mô hình Bayesian cơ bản có thể viết gọn bằng ký hiệu ma trận. Chẳng hạn, mô hình hồi quy Gaussian được viết là:

$$
\mathbf{y}=\mathbf{X}\boldsymbol{\beta}+\boldsymbol{\epsilon},\qquad
\boldsymbol{\epsilon}\sim\mathcal{N}(\mathbf{0},\sigma^2\mathbf{I}).
$$

Cách viết này tách rõ ba thành phần: ma trận dữ liệu $$\mathbf{X}$$, vector tham số $$\boldsymbol{\beta}$$ và cấu trúc nhiễu $$\boldsymbol{\epsilon}$$. Khi sang bước suy diễn hậu nghiệm, các đối tượng này sẽ xuất hiện xuyên suốt cả trong công thức lẫn mã tính toán.

## 1. Vectors (Vectơ)

### 1.1. Định nghĩa

**Vector** là một mảng số có thứ tự, có thể dùng để biểu diễn một điểm hoặc một hướng trong không gian.

**Vector cột** (thường dùng):

$$\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}$$

**Vector hàng**:

$$\mathbf{x}^T = \begin{bmatrix} x_1 & x_2 & \cdots & x_n \end{bmatrix}$$

```python
import numpy as np
import matplotlib.pyplot as plt

# Tạo vectors
v = np.array([3, 4])  # Vector 2D
w = np.array([1, 2, 3])  # Vector 3D

print(f"v = {v}")
print(f"Số chiều (dimension): {v.shape}")
print(f"Độ dài (length): {len(v)}")
```

### 1.2. Trực quan hóa Vectors

```python
# Vẽ vectors trong 2D
fig, ax = plt.subplots(figsize=(8, 8))

vectors = {
    'v': np.array([3, 4]),
    'w': np.array([2, 1]),
    'u': np.array([-1, 3])
}

colors = ['red', 'blue', 'green']

for (name, vec), color in zip(vectors.items(), colors):
    ax.quiver(0, 0, vec[0], vec[1], angles='xy', scale_units='xy', scale=1,
             color=color, width=0.01, label=name)
    ax.text(vec[0]*0.5, vec[1]*0.5, name, fontsize=12, fontweight='bold')

ax.set_xlim(-2, 5)
ax.set_ylim(-1, 5)
ax.set_xlabel('x₁')
ax.set_ylabel('x₂')
ax.set_title('Vectors trong không gian 2D')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend()
ax.set_aspect('equal')
plt.show()
```

### 1.3. Phép toán với Vectors

#### Cộng/Trừ Vectors

$$\mathbf{x} + \mathbf{y} = \begin{bmatrix} x_1 + y_1 \\ x_2 + y_2 \\ \vdots \\ x_n + y_n \end{bmatrix}$$

```python
v = np.array([3, 4])
w = np.array([2, 1])

# Cộng
v_plus_w = v + w
print(f"v + w = {v_plus_w}")

# Trừ
v_minus_w = v - w
print(f"v - w = {v_minus_w}")

# Trực quan hóa
fig, ax = plt.subplots(figsize=(8, 8))

# Vector v (đỏ)
ax.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1,
         color='red', width=0.01, label='v')

# Vector w (xanh dương)
ax.quiver(0, 0, w[0], w[1], angles='xy', scale_units='xy', scale=1,
         color='blue', width=0.01, label='w')

# Vector v+w (xanh lá)
ax.quiver(0, 0, v_plus_w[0], v_plus_w[1], angles='xy', scale_units='xy', scale=1,
         color='green', width=0.015, label='v+w')

# Vẽ hình bình hành
ax.plot([v[0], v_plus_w[0]], [v[1], v_plus_w[1]], 'k--', alpha=0.3)
ax.plot([w[0], v_plus_w[0]], [w[1], v_plus_w[1]], 'k--', alpha=0.3)

ax.set_xlim(-1, 6)
ax.set_ylim(-1, 6)
ax.set_xlabel('x₁')
ax.set_ylabel('x₂')
ax.set_title('Phép cộng Vectors')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend()
ax.set_aspect('equal')
plt.show()
```

#### Nhân với số vô hướng (Scalar)

$$c \mathbf{x} = \begin{bmatrix} c x_1 \\ c x_2 \\ \vdots \\ c x_n \end{bmatrix}$$

```python
v = np.array([3, 4])

# Nhân với scalars khác nhau
fig, ax = plt.subplots(figsize=(8, 8))

scalars = [0.5, 1, 1.5, 2, -1]
colors = ['orange', 'red', 'blue', 'green', 'purple']

for scalar, color in zip(scalars, colors):
    scaled = scalar * v
    ax.quiver(0, 0, scaled[0], scaled[1], angles='xy', scale_units='xy', scale=1,
             color=color, width=0.01, label=f'{scalar}v')

ax.set_xlim(-5, 8)
ax.set_ylim(-5, 10)
ax.set_xlabel('x₁')
ax.set_ylabel('x₂')
ax.set_title('Nhân Vector với Scalar')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend()
ax.set_aspect('equal')
plt.show()
```

#### Tích Vô hướng (Dot Product)

$$\mathbf{x} \cdot \mathbf{y} = \sum_{i=1}^{n} x_i y_i = x_1 y_1 + x_2 y_2 + \cdots + x_n y_n$$

**Ý nghĩa hình học**:

$$\mathbf{x} \cdot \mathbf{y} = \|\mathbf{x}\| \|\mathbf{y}\| \cos(\theta)$$

```python
v = np.array([3, 4])
w = np.array([2, 1])

# Dot product
dot_product = np.dot(v, w)
print(f"v · w = {dot_product}")

# Hoặc
dot_product2 = v @ w
print(f"v @ w = {dot_product2}")

# Tính góc giữa 2 vectors
norm_v = np.linalg.norm(v)
norm_w = np.linalg.norm(w)
cos_theta = dot_product / (norm_v * norm_w)
theta_rad = np.arccos(cos_theta)
theta_deg = np.degrees(theta_rad)

print(f"\n||v|| = {norm_v:.2f}")
print(f"||w|| = {norm_w:.2f}")
print(f"Góc giữa v và w: {theta_deg:.2f}°")
```

**Tính chất quan trọng**:
- Nếu $$\mathbf{x} \cdot \mathbf{y} = 0$$: hai vector vuông góc (orthogonal).
- Nếu $$\mathbf{x} \cdot \mathbf{y} > 0$$: góc giữa hai vector là góc nhọn.
- Nếu $$\mathbf{x} \cdot \mathbf{y} < 0$$: góc giữa hai vector là góc tù.

#### Độ dài (Norm)

**Chuẩn Euclid (L2 norm)**:

$$\|\mathbf{x}\| = \sqrt{\sum_{i=1}^{n} x_i^2} = \sqrt{\mathbf{x} \cdot \mathbf{x}}$$

```python
v = np.array([3, 4])
norm = np.linalg.norm(v)
print(f"||v|| = {norm}")  # 5.0

# Vector đơn vị (unit vector)
v_unit = v / norm
print(f"Vector đơn vị: {v_unit}")
print(f"Độ dài: {np.linalg.norm(v_unit)}")  # 1.0
```

## 2. Matrices (Ma trận)

### 2.1. Định nghĩa

**Ma trận (matrix)** là một mảng số hai chiều:

$$\mathbf{A} = \begin{bmatrix} 
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix}$$

**Kích thước**: $$m \times n$$ ($$m$$ hàng, $$n$$ cột).

```python
# Tạo matrices
A = np.array([[1, 2, 3],
              [4, 5, 6]])

B = np.array([[1, 2],
              [3, 4],
              [5, 6]])

print(f"A shape: {A.shape}")  # (2, 3)
print(f"B shape: {B.shape}")  # (3, 2)

# Ma trận đặc biệt
I = np.eye(3)  # Ma trận đơn vị 3x3
Z = np.zeros((2, 4))  # Ma trận 0
O = np.ones((3, 2))  # Ma trận 1
```

### 2.2. Phép toán với Ma trận

#### Cộng/Trừ (cùng kích thước)

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print("A + B =")
print(A + B)

print("\nA - B =")
print(A - B)
```

#### Nhân với số vô hướng

```python
c = 2
print("2A =")
print(c * A)
```

#### Nhân Ma trận

**Điều kiện**: số cột của $$\mathbf{A}$$ phải bằng số hàng của $$\mathbf{B}$$. Nếu $$\mathbf{A}$$ có kích thước $$m \times n$$ và $$\mathbf{B}$$ có kích thước $$n \times p$$, thì $$\mathbf{C} = \mathbf{AB}$$ có kích thước $$m \times p$$ với phần tử:

$$c_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}$$

```python
A = np.array([[1, 2, 3],
              [4, 5, 6]])  # 2x3

B = np.array([[1, 2],
              [3, 4],
              [5, 6]])  # 3x2

C = A @ B  # 2x2
print("A @ B =")
print(C)

# Lưu ý: Nhân ma trận không giao hoán
# A @ B ≠ B @ A (thường)
```

#### Chuyển vị (Transpose)

$$(\mathbf{A}^T)_{ij} = a_{ji}$$

```python
A = np.array([[1, 2, 3],
              [4, 5, 6]])

A_T = A.T
print("A^T =")
print(A_T)

# Tính chất: (A^T)^T = A
print("\n(A^T)^T = A?", np.array_equal(A_T.T, A))
```

### 2.3. Ma trận Nghịch đảo

Với ma trận vuông $$\mathbf{A}$$ kích thước $$n \times n$$, ma trận nghịch đảo $$\mathbf{A}^{-1}$$ (nếu tồn tại) thỏa mãn:

$$\mathbf{A} \mathbf{A}^{-1} = \mathbf{A}^{-1} \mathbf{A} = \mathbf{I}$$

**Lưu ý**: không phải ma trận vuông nào cũng khả nghịch; những ma trận không có nghịch đảo được gọi là ma trận suy biến (singular matrix).

```python
A = np.array([[1, 2],
              [3, 4]])

# Tính nghịch đảo
A_inv = np.linalg.inv(A)
print("A^(-1) =")
print(A_inv)

# Kiểm tra
I_check = A @ A_inv
print("\nA @ A^(-1) =")
print(I_check)

# Ma trận không khả nghịch
singular = np.array([[1, 2],
                     [2, 4]])  # Hàng 2 = 2 * Hàng 1

try:
    singular_inv = np.linalg.inv(singular)
except np.linalg.LinAlgError:
    print("\nMa trận singular không có nghịch đảo!")
```

### 2.4. Định thức (Determinant)

Cho ma trận vuông $$\mathbf{A}$$, với trường hợp $$2 \times 2$$:

$$\det(\mathbf{A}) = \begin{vmatrix} a & b \\ c & d \end{vmatrix} = ad - bc$$

**Tính chất**:
- $$\det(\mathbf{A}) \neq 0$$: ma trận khả nghịch.
- $$\det(\mathbf{A}) = 0$$: ma trận suy biến (không khả nghịch).

```python
A = np.array([[1, 2],
              [3, 4]])

det_A = np.linalg.det(A)
print(f"det(A) = {det_A}")

# Ma trận singular
singular = np.array([[1, 2],
                     [2, 4]])
det_singular = np.linalg.det(singular)
print(f"det(singular) = {det_singular:.10f}")  # ≈ 0
```

## 3. Hệ Phương trình Tuyến tính

Xét hệ phương trình tuyến tính:

$$\begin{cases}
a_{11}x_1 + a_{12}x_2 + \cdots + a_{1n}x_n = b_1 \\
a_{21}x_1 + a_{22}x_2 + \cdots + a_{2n}x_n = b_2 \\
\vdots \\
a_{m1}x_1 + a_{m2}x_2 + \cdots + a_{mn}x_n = b_m
\end{cases}$$

**Dạng ma trận**: $$\mathbf{Ax} = \mathbf{b}$$.

**Nghiệm** (khi $$\mathbf{A}$$ vuông và khả nghịch): $$\mathbf{x} = \mathbf{A}^{-1}\mathbf{b}$$. Trong tính toán số, nên dùng `np.linalg.solve` thay vì tính trực tiếp ma trận nghịch đảo để nhanh và ổn định hơn.

```python
# Hệ phương trình:
# 2x + 3y = 8
# 5x + 4y = 13

A = np.array([[2, 3],
              [5, 4]])

b = np.array([8, 13])

# Giải bằng nghịch đảo
x = np.linalg.inv(A) @ b
print(f"Nghiệm (dùng inv): x = {x}")

# Giải bằng solve (hiệu quả hơn)
x_solve = np.linalg.solve(A, b)
print(f"Nghiệm (dùng solve): x = {x_solve}")

# Kiểm tra
print(f"Kiểm tra Ax = b: {np.allclose(A @ x, b)}")
```

## 4. Trị riêng và Vector riêng (Eigenvalues và Eigenvectors)

Cho ma trận vuông $$\mathbf{A}$$, nếu tồn tại số $$\lambda$$ và vector khác không $$\mathbf{v}$$ sao cho:

$$\mathbf{A}\mathbf{v} = \lambda \mathbf{v}$$

thì $$\lambda$$ được gọi là **trị riêng (eigenvalue)** và $$\mathbf{v}$$ là **vector riêng (eigenvector)** tương ứng.

**Ý nghĩa hình học**: khi chịu phép biến đổi tuyến tính $$\mathbf{A}$$, vector $$\mathbf{v}$$ không đổi phương mà chỉ bị co giãn theo hệ số $$\lambda$$.

```python
A = np.array([[4, 2],
              [1, 3]])

# Tính eigenvalues và eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

print("Eigenvalues:")
print(eigenvalues)

print("\nEigenvectors:")
print(eigenvectors)

# Kiểm tra
for i in range(len(eigenvalues)):
    lambda_i = eigenvalues[i]
    v_i = eigenvectors[:, i]
    
    Av = A @ v_i
    lambda_v = lambda_i * v_i
    
    print(f"\nEigenvalue {i+1}: λ = {lambda_i:.4f}")
    print(f"Av = {Av}")
    print(f"λv = {lambda_v}")
    print(f"Khớp? {np.allclose(Av, lambda_v)}")
```

## 5. Ứng dụng trong Thống kê

### 5.1. Ma trận Hiệp phương sai (Covariance Matrix)

Với ma trận dữ liệu $$\mathbf{X}$$ kích thước $$n \times p$$ đã được căn tâm (trừ đi trung bình từng cột), ma trận hiệp phương sai mẫu được tính bằng:

$$\mathbf{\Sigma} = \frac{1}{n-1} \mathbf{X}^T \mathbf{X}$$

```python
# Tạo dữ liệu
np.random.seed(42)
n = 100
X = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], n)

# Tính covariance matrix
cov_matrix = np.cov(X.T)
print("Covariance Matrix:")
print(cov_matrix)

# Trực quan hóa
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Scatter plot
axes[0].scatter(X[:, 0], X[:, 1], alpha=0.6)
axes[0].set_xlabel('X₁')
axes[0].set_ylabel('X₂')
axes[0].set_title('Dữ liệu')
axes[0].grid(alpha=0.3)
axes[0].set_aspect('equal')

# Covariance matrix heatmap
import seaborn as sns
sns.heatmap(cov_matrix, annot=True, cmap='coolwarm', center=0, 
           square=True, ax=axes[1])
axes[1].set_title('Covariance Matrix')

plt.tight_layout()
plt.show()
```

### 5.2. Hồi quy Tuyến tính (Linear Regression)

Xét mô hình $$\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}$$. **Nghiệm bình phương tối thiểu thông thường (OLS — Ordinary Least Squares)** là:

$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$

```python
# Tạo dữ liệu
np.random.seed(42)
n = 100
X = np.random.normal(0, 1, (n, 2))
true_beta = np.array([2, -1])
y = X @ true_beta + np.random.normal(0, 0.5, n)

# Thêm intercept
X_with_intercept = np.column_stack([np.ones(n), X])

# Tính beta
beta_hat = np.linalg.inv(X_with_intercept.T @ X_with_intercept) @ X_with_intercept.T @ y

print("True beta:", true_beta)
print("Estimated beta:", beta_hat[1:])  # Bỏ intercept
print("Intercept:", beta_hat[0])

# Predictions
y_pred = X_with_intercept @ beta_hat

# Visualize
plt.figure(figsize=(8, 6))
plt.scatter(y, y_pred, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', linewidth=2)
plt.xlabel('True y')
plt.ylabel('Predicted y')
plt.title('Linear Regression: True vs Predicted')
plt.grid(alpha=0.3)
plt.show()

# R-squared
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - y.mean())**2)
r_squared = 1 - ss_res/ss_tot
print(f"\nR² = {r_squared:.4f}")
```

## 6. Tóm tắt Công thức Quan trọng

| Phép toán | Ký hiệu | Công thức |
|-----------|---------|-----------|
| Tích vô hướng (Dot product) | $$\mathbf{x} \cdot \mathbf{y}$$ | $$\sum_{i=1}^{n} x_i y_i$$ |
| Chuẩn (Norm) | $$\|\mathbf{x}\|$$ | $$\sqrt{\sum_{i=1}^{n} x_i^2}$$ |
| Nhân ma trận | $$\mathbf{AB}$$ | $$c_{ij} = \sum_{k} a_{ik}b_{kj}$$ |
| Chuyển vị (Transpose) | $$\mathbf{A}^T$$ | $$(\mathbf{A}^T)_{ij} = a_{ji}$$ |
| Nghịch đảo (Inverse) | $$\mathbf{A}^{-1}$$ | $$\mathbf{AA}^{-1} = \mathbf{I}$$ |
| Định thức (Determinant) | $$\det(\mathbf{A})$$ | Giá trị vô hướng |
| Trị riêng (Eigenvalue) | $$\lambda$$ | $$\mathbf{Av} = \lambda\mathbf{v}$$ |

## Giải thích: Hình học của ma trận hiệp phương sai và Hồi quy Bayes tính tay 2×2

Tại sao trị riêng của $$oldsymbol{\Sigma}$$ lại quan trọng đến vậy trong thống kê Bayes? Hãy đi chậm qua 4 bước:

1. **Dạng toàn phương (Quadratic Form):** Trong mật độ Chuẩn đa biến $$\expigl(-rac{1}{2}(\mathbf{x}-oldsymbol{\mu})^Toldsymbol{\Sigma}^{-1}(\mathbf{x}-oldsymbol{\mu})igr)$$, các đường đồng mức xác suất là những **hình elip** (hoặc ellipsoid nhiều chiều).
2. **Hướng và bán trục của elip:** Các vector riêng của $$oldsymbol{\Sigma}$$ chỉ phương các trục chính của elip, còn căn bậc hai trị riêng $$\sqrt{\lambda_i}$$ chính là độ dài bán trục (độ lệch chuẩn dọc theo phương đó).
3. **Số điều kiện (Condition Number):** Tỷ số $$\lambda_{\max}/\lambda_{\min}$$ càng lớn thì elip hậu nghiệm càng dẹt như điếu xì gà — khiến bộ lấy mẫu Metropolis–Hastings nhảy bước đều bị kẹt (hoặc bước quá lớn đụng tường, hoặc bước quá nhỏ đi mãi không tới).
4. **Cộng độ chính xác ở dạng ma trận:** Cập nhật Normal–Normal đa biến hoàn toàn tương tự 1 chiều, chỉ thay số vô hướng bằng ma trận: $$oldsymbol{\Lambda}_{	ext{post}} = oldsymbol{\Lambda}_0 + rac{1}{\sigma^2}\mathbf{X}^T\mathbf{X}$$.

### Ví dụ tính toán làm từng bước: Giải trị riêng ma trận hiệp phương sai 2×2 và cập nhật Ridge–Bayes

Xét hai tham số $$(eta_1, eta_2)$$ có ma trận hiệp phương sai hậu nghiệm:
$$oldsymbol{\Sigma} = egin{pmatrix} 5 & 3 \ 3 & 5 \end{pmatrix}.$$

- **Bước 1 — Tìm trị riêng từ phương trình đặc trưng $$\det(oldsymbol{\Sigma} - \lambda \mathbf{I}) = 0$$:**
  $$(5 - \lambda)^2 - 9 = 0 \implies 5 - \lambda = \pm 3 \implies \lambda_1 = 8,\quad \lambda_2 = 2.$$
  Vì cả hai trị riêng đều dương, $$oldsymbol{\Sigma}$$ là ma trận xác định dương hợp lệ.
- **Bước 2 — Tìm vector riêng đơn vị và ý nghĩa hình học:**
  - Với $$\lambda_1 = 8$$: $$(-3)v_1 + 3v_2 = 0 \implies \mathbf{u}_1 = rac{1}{\sqrt{2}}egin{pmatrix}1 \ 1\end{pmatrix}$$. Độ lệch chuẩn dọc trục chéo này là $$\sqrt{8} pprox 2.83$$.
  - Với $$\lambda_2 = 2$$: $$3v_1 + 3v_2 = 0 \implies \mathbf{u}_2 = rac{1}{\sqrt{2}}egin{pmatrix}1 \ -1\end{pmatrix}$$. Độ lệch chuẩn dọc trục vuông góc chỉ là $$\sqrt{2} pprox 1.41$$.
- **Bước 3 — Tính hệ số tương quan để đối chiếu:**
  $$
ho = rac{\Sigma_{12}}{\sqrt{\Sigma_{11}\Sigma_{22}}} = rac{3}{\sqrt{5 	imes 5}} = rac{3}{5} = 0.60.$$
  Đám mây hậu nghiệm nghiêng $$45^\circ$$, dài gấp $$\sqrt{8/2} = 2$$ lần bề ngang.

**Hiểu lầm cần tránh:** Tính nghịch đảo tường minh `np.linalg.inv(A) @ b` trong mã thực tế; cách chuẩn về mặt số học là giải hệ tuyến tính `np.linalg.solve(A, b)` hoặc phân rã Cholesky để tránh khuếch đại sai số làm tròn.

**Kiểm tra nhanh:** Định thức $$\det(oldsymbol{\Sigma}) = 5 	imes 5 - 3 	imes 3 = 16$$, khớp hoàn toàn với tích hai trị riêng $$\lambda_1 \lambda_2 = 8 	imes 2 = 16$$; vết $$	ext{tr}(oldsymbol{\Sigma}) = 5 + 5 = 10$$, khớp với tổng $$\lambda_1 + \lambda_2 = 8 + 2 = 10$$.

---

## Video tham khảo

- [Vectors | Chapter 1, Essence of linear algebra](https://www.youtube.com/watch?v=fNk_zzaMoSs) — 3Blue1Brown, English. **Xem trước.** Giúp hình dung vector như đối tượng hình học trước khi dùng để biểu diễn dữ liệu và tham số.
- [Matrix multiplication as composition | Chapter 4, Essence of linear algebra](https://www.youtube.com/watch?v=XkY2DOUCWMU) — 3Blue1Brown, English. Giải thích phép nhân ma trận như phép hợp các biến đổi tuyến tính, gắn với cách viết mô hình hồi quy.
- [Eigenvectors and eigenvalues | Chapter 14, Essence of linear algebra](https://www.youtube.com/watch?v=PFDu9oVAE-g) — 3Blue1Brown, English. Trình bày trực quan về trị riêng và vector riêng để hiểu cấu trúc hình học của ma trận.

## Bài tập

1. **Vectors**: Cho $$\mathbf{v} = [2, 3, -1]$$ và $$\mathbf{w} = [1, -2, 4]$$. Tính:
   - $$\mathbf{v} + \mathbf{w}$$
   - $$\mathbf{v} \cdot \mathbf{w}$$
   - $$\|\mathbf{v}\|$$
   - Góc giữa $$\mathbf{v}$$ và $$\mathbf{w}$$

2. **Ma trận**: Cho $$\mathbf{A} = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$$ và $$\mathbf{B} = \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}$$. Tính:
   - $$\mathbf{A} + \mathbf{B}$$
   - $$\mathbf{AB}$$
   - $$\mathbf{A}^T$$
   - $$\mathbf{A}^{-1}$$
   - $$\det(\mathbf{A})$$

3. **Hệ phương trình**: Giải hệ:
   $$\begin{cases} 3x + 2y = 7 \\ x - y = 1 \end{cases}$$

4. **Trị riêng và vector riêng**: Tìm trị riêng và vector riêng của $$\mathbf{A} = \begin{bmatrix} 3 & 1 \\ 1 & 3 \end{bmatrix}$$.

5. **Hồi quy tuyến tính**: Sinh 100 quan sát theo mô hình $$y = 3x_1 - 2x_2 + \epsilon$$ rồi ước lượng $$\boldsymbol{\beta}$$ bằng công thức OLS.

## Tài liệu tham khảo

1. **Strang, G. (2016).** *Introduction to Linear Algebra*. Wellesley-Cambridge Press.
2. **3Blue1Brown - Essence of Linear Algebra** - https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab
3. **NumPy Linear Algebra** - https://numpy.org/doc/stable/reference/routines.linalg.html

---

*Bài học tiếp theo: [0.9 Giải tích Cơ bản]({{ site.baseurl }}/contents/vi/chapter00/00_06_calculus_basics/)*
