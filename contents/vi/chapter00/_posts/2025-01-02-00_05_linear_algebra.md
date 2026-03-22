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

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vì sao đại số tuyến tính là hạ tầng toán học của mô hình thống kê Bayes: dữ liệu được biểu diễn dưới dạng vector-ma trận, tham số hồi quy được viết thành toán tử tuyến tính, và nhiều thuật toán suy luận dựa trực tiếp vào các phép biến đổi tuyến tính. Bạn cũng sẽ đọc được ý nghĩa hình học của các công thức thay vì chỉ thao tác ký hiệu.

## Giới thiệu: từ công thức rời rạc đến cấu trúc tuyến tính

Khi số biến tăng, việc viết mô hình bằng từng phương trình riêng lẻ trở nên khó theo dõi. Đại số tuyến tính giải quyết vấn đề này bằng cách gom các đại lượng vào vector và ma trận, giúp ta nhìn mô hình như một cấu trúc thống nhất. Đây là bước chuyển quan trọng vì hầu hết mô hình Bayes hiện đại (hồi quy tuyến tính, GLM, mô hình phân cấp) đều được hiện thực hiệu quả trên cấu trúc này.

Về mặt phương pháp luận, bạn có thể xem bài này như phần "ngôn ngữ hình thức" cho các chương mô hình hóa: nếu chương 0.7 cung cấp công cụ lập trình, thì bài này cung cấp khuôn toán học để diễn đạt và suy luận.

## Cầu nối sang suy luận Bayesian

Nhiều biểu thức Bayesian cơ bản có thể viết gọn bằng đại số tuyến tính. Chẳng hạn mô hình hồi quy Gaussian:

$$
\mathbf{y}=\mathbf{X}\boldsymbol{\beta}+\boldsymbol{\epsilon},\qquad
\boldsymbol{\epsilon}\sim\mathcal{N}(\mathbf{0},\sigma^2\mathbf{I}).
$$

Biểu diễn này cho phép ta tách rõ ba thành phần: dữ liệu $$\mathbf{X}$$, tham số $$\boldsymbol{\beta}$$, và cấu trúc nhiễu. Khi đi tiếp sang posterior inference, các đối tượng này sẽ xuất hiện lặp lại trong cả công thức lẫn mã tính toán.

## 1. Vectors (Vectơ)

### 1.1. Định nghĩa

**Vector** là một mảng số có thứ tự. Có thể biểu diễn điểm trong không gian hoặc hướng.

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

#### Nhân Scalar

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
- Nếu $$\mathbf{x} \cdot \mathbf{y} = 0$$: 2 vectors vuông góc (orthogonal)
- Nếu $$\mathbf{x} \cdot \mathbf{y} > 0$$: Góc nhọn
- Nếu $$\mathbf{x} \cdot \mathbf{y} < 0$$: Góc tù

#### Độ dài (Norm)

**Euclidean norm (L2 norm)**:

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

**Matrix** là mảng 2 chiều các số.

$$\mathbf{A} = \begin{bmatrix} 
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix}$$

**Kích thước**: $$m \times n$$ (m hàng, n cột)

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

### 2.2. Phép toán với Matrices

#### Cộng/Trừ (cùng kích thước)

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print("A + B =")
print(A + B)

print("\nA - B =")
print(A - B)
```

#### Nhân Scalar

```python
c = 2
print("2A =")
print(c * A)
```

#### Nhân Ma trận

**Điều kiện**: Số cột của A = Số hàng của B

Nếu $$\mathbf{A}$$ là $$m \times n$$ và $$\mathbf{B}$$ là $$n \times p$$, thì $$\mathbf{C} = \mathbf{AB}$$ là $$m \times p$$:

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

Cho ma trận vuông $$\mathbf{A}$$ ($$n \times n$$), ma trận nghịch đảo $$\mathbf{A}^{-1}$$ thỏa:

$$\mathbf{A} \mathbf{A}^{-1} = \mathbf{A}^{-1} \mathbf{A} = \mathbf{I}$$

**Lưu ý**: Không phải ma trận nào cũng có nghịch đảo (singular matrix).

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

Cho ma trận vuông $$\mathbf{A}$$:

**2×2**:

$$\det(\mathbf{A}) = \begin{vmatrix} a & b \\ c & d \end{vmatrix} = ad - bc$$

**Tính chất**:
- $$\det(\mathbf{A}) \neq 0$$: Ma trận khả nghịch
- $$\det(\mathbf{A}) = 0$$: Ma trận singular

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

Hệ phương trình:

$$\begin{cases}
a_{11}x_1 + a_{12}x_2 + \cdots + a_{1n}x_n = b_1 \\
a_{21}x_1 + a_{22}x_2 + \cdots + a_{2n}x_n = b_2 \\
\vdots \\
a_{m1}x_1 + a_{m2}x_2 + \cdots + a_{mn}x_n = b_m
\end{cases}$$

**Dạng ma trận**: $$\mathbf{Ax} = \mathbf{b}$$

**Nghiệm** (nếu A khả nghịch): $$\mathbf{x} = \mathbf{A}^{-1}\mathbf{b}$$

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

## 4. Eigenvalues và Eigenvectors

Cho ma trận vuông $$\mathbf{A}$$, nếu:

$$\mathbf{A}\mathbf{v} = \lambda \mathbf{v}$$

thì $$\lambda$$ là **eigenvalue** và $$\mathbf{v}$$ là **eigenvector** tương ứng.

**Ý nghĩa**: Vector $$\mathbf{v}$$ chỉ bị scale (không đổi hướng) khi nhân với $$\mathbf{A}$$.

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

## 5. Ứng dụng trong Statistics

### 5.1. Covariance Matrix

Cho dữ liệu $$\mathbf{X}$$ ($$n \times p$$), ma trận covariance:

$$\mathbf{\Sigma} = \frac{1}{n-1} \mathbf{X}^T \mathbf{X}$$

(sau khi center dữ liệu)

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

### 5.2. Linear Regression

Mô hình: $$\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}$$

**Nghiệm OLS** (Ordinary Least Squares):

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
| Dot product | $$\mathbf{x} \cdot \mathbf{y}$$ | $$\sum_{i=1}^{n} x_i y_i$$ |
| Norm | $$\|\mathbf{x}\|$$ | $$\sqrt{\sum_{i=1}^{n} x_i^2}$$ |
| Matrix multiplication | $$\mathbf{AB}$$ | $$c_{ij} = \sum_{k} a_{ik}b_{kj}$$ |
| Transpose | $$\mathbf{A}^T$$ | $$(\mathbf{A}^T)_{ij} = a_{ji}$$ |
| Inverse | $$\mathbf{A}^{-1}$$ | $$\mathbf{AA}^{-1} = \mathbf{I}$$ |
| Determinant | $$\det(\mathbf{A})$$ | Scalar value |
| Eigenvalue | $$\lambda$$ | $$\mathbf{Av} = \lambda\mathbf{v}$$ |

## Bài tập

1. **Vectors**: Cho $$\mathbf{v} = [2, 3, -1]$$ và $$\mathbf{w} = [1, -2, 4]$$. Tính:
   - $$\mathbf{v} + \mathbf{w}$$
   - $$\mathbf{v} \cdot \mathbf{w}$$
   - $$\|\mathbf{v}\|$$
   - Góc giữa $$\mathbf{v}$$ và $$\mathbf{w}$$

2. **Matrices**: Cho $$\mathbf{A} = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$$ và $$\mathbf{B} = \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}$$. Tính:
   - $$\mathbf{A} + \mathbf{B}$$
   - $$\mathbf{AB}$$
   - $$\mathbf{A}^T$$
   - $$\mathbf{A}^{-1}$$
   - $$\det(\mathbf{A})$$

3. **Hệ phương trình**: Giải hệ:
   $$\begin{cases} 3x + 2y = 7 \\ x - y = 1 \end{cases}$$

4. **Eigenvalues**: Tìm eigenvalues và eigenvectors của $$\mathbf{A} = \begin{bmatrix} 3 & 1 \\ 1 & 3 \end{bmatrix}$$

5. **Linear Regression**: Tạo dữ liệu $$y = 3x_1 - 2x_2 + \epsilon$$ với 100 samples. Ước lượng $$\beta$$ bằng công thức OLS.

## Tài liệu tham khảo

1. **Strang, G. (2016).** *Introduction to Linear Algebra*. Wellesley-Cambridge Press.
2. **3Blue1Brown - Essence of Linear Algebra** - https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab
3. **NumPy Linear Algebra** - https://numpy.org/doc/stable/reference/routines.linalg.html

---

*Bài học này kết thúc phần kiến thức cơ bản. Bạn đã sẵn sàng bắt đầu khóa học Bayesian Statistics!*


---

*Bài học tiếp theo: [0.9 Giải tích Cơ bản](/vi/chapter00/calculus-basics/)*
