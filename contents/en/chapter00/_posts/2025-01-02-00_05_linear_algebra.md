---
layout: post
title: "Lesson 0.8: Basic Linear Algebra"
chapter: '00'
order: 8
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

One-parameter coin flips only take you so far. The moment you model real-world data—predicting house prices from 10 features, modeling correlated gene expressions, or running a **Multivariate Normal** Bayesian regression—scalars turn into vectors and matrices, and variance turns into a **covariance matrix $$\Sigma$$**.

This lesson builds the exact geometric and matrix intuition you need for multi-parameter Bayesian models: dot products, linear transformations, **positive-definite covariance matrices**, **eigenvalues/eigenvectors** (which reveal the principal axes of a correlated posterior!), and **Cholesky decomposition** (the engine that samples correlated Gaussian draws!).

---

## Background Knowledge Map: How Linear Algebra Powers Multi-Parameter Bayes

Four linear-algebra ideas reappear constantly across Bayesian regression and MCMC:

1. **Design Matrix $$\mathbf{X}$$ & Linear Predictors $$\mathbf{X}oldsymbol{eta}$$:** Packs $$n$$ observations and $$p$$ predictors into one matrix multiply, turning regression into vector geometry.
2. **Symmetric Positive-Definite (SPD) Covariance & Precision Matrices:** A valid covariance matrix $$\Sigma$$ is symmetric with all eigenvalues $$> 0$$. Its inverse $$\Lambda = \Sigma^{-1}$$ (the **precision matrix**) adds linearly in Multivariate Normal Bayesian updating!
3. **Eigenvalues & Posterior Geometry:** The eigenvectors of $$\Sigma$$ point along the principal axes of the elliptical posterior contour, and the square roots of the eigenvalues give the standard deviations along those axes—explaining why highly correlated parameters create narrow "diagonal bananas/ridges" that slow down naive MCMC!
4. **Cholesky Decomposition ($$\Sigma = L L^T$$):** The matrix square root of a covariance matrix—multiplying standard independent Normal draws $$\mathbf{z} \sim \mathcal{N}(\mathbf{0}, I)$$ by $$L$$ instantly generates correlated draws $$oldsymbol{\mu} + L\mathbf{z} \sim \mathcal{N}(oldsymbol{\mu}, \Sigma)$$!

---

## Learning objectives

After this lesson, you will understand why linear algebra is the mathematical infrastructure of Bayesian statistical models: data is represented as vectors and matrices, regression parameters are written as linear operators, and many inference algorithms rely directly on linear transformations. You will also be able to read the geometric meaning of formulas instead of just manipulating symbols.

## Introduction: from scattered formulas to linear structure

As the number of variables grows, writing a model with individual equations becomes hard to follow. Linear algebra solves this problem by gathering quantities into vectors and matrices, helping us see the model as a unified structure. This is an important step because most modern Bayesian models (linear regression, GLMs, hierarchical models) are implemented efficiently on this structure.

Methodologically, you can regard this lesson as the "formal language" for the modeling chapters: if lesson 0.7 provides the programming tools, this lesson provides the mathematical framework for expressing and reasoning.

## A bridge to Bayesian inference

Many basic Bayesian expressions can be written compactly with linear algebra. For example the Gaussian regression model:

$$
\mathbf{y}=\mathbf{X}\boldsymbol{\beta}+\boldsymbol{\epsilon},\qquad
\boldsymbol{\epsilon}\sim\mathcal{N}(\mathbf{0},\sigma^2\mathbf{I}).
$$

This representation lets us clearly separate three components: the data $$\mathbf{X}$$, the parameters $$\boldsymbol{\beta}$$, and the noise structure. As we move on to posterior inference, these objects will appear repeatedly in both formulas and computation code.

## 1. Vectors

### 1.1. Definition

A **vector** is an ordered array of numbers. It can represent a point in space or a direction.

**Column vector** (commonly used):

$$\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}$$

**Row vector**:

$$\mathbf{x}^T = \begin{bmatrix} x_1 & x_2 & \cdots & x_n \end{bmatrix}$$

```python
import numpy as np
import matplotlib.pyplot as plt

# Create vectors
v = np.array([3, 4])  # Vector 2D
w = np.array([1, 2, 3])  # Vector 3D

print(f"v = {v}")
print(f"Dimension: {v.shape}")
print(f"Length: {len(v)}")
```

### 1.2. Visualizing Vectors

```python
# Plot vectors in 2D
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
ax.set_title('Vectors in 2D space')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend()
ax.set_aspect('equal')
plt.show()
```

### 1.3. Operations with Vectors

#### Vector Addition/Subtraction

$$\mathbf{x} + \mathbf{y} = \begin{bmatrix} x_1 + y_1 \\ x_2 + y_2 \\ \vdots \\ x_n + y_n \end{bmatrix}$$

```python
v = np.array([3, 4])
w = np.array([2, 1])

# Add
v_plus_w = v + w
print(f"v + w = {v_plus_w}")

# Subtract
v_minus_w = v - w
print(f"v - w = {v_minus_w}")

# Visualize
fig, ax = plt.subplots(figsize=(8, 8))

# Vector v (red)
ax.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1,
         color='red', width=0.01, label='v')

# Vector w (blue)
ax.quiver(0, 0, w[0], w[1], angles='xy', scale_units='xy', scale=1,
         color='blue', width=0.01, label='w')

# Vector v+w (green)
ax.quiver(0, 0, v_plus_w[0], v_plus_w[1], angles='xy', scale_units='xy', scale=1,
         color='green', width=0.015, label='v+w')

# Draw the parallelogram
ax.plot([v[0], v_plus_w[0]], [v[1], v_plus_w[1]], 'k--', alpha=0.3)
ax.plot([w[0], v_plus_w[0]], [w[1], v_plus_w[1]], 'k--', alpha=0.3)

ax.set_xlim(-1, 6)
ax.set_ylim(-1, 6)
ax.set_xlabel('x₁')
ax.set_ylabel('x₂')
ax.set_title('Vector Addition')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend()
ax.set_aspect('equal')
plt.show()
```

#### Scalar Multiplication

$$c \mathbf{x} = \begin{bmatrix} c x_1 \\ c x_2 \\ \vdots \\ c x_n \end{bmatrix}$$

```python
v = np.array([3, 4])

# Multiply by different scalars
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
ax.set_title('Multiplying a Vector by a Scalar')
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.legend()
ax.set_aspect('equal')
plt.show()
```

#### Dot Product

$$\mathbf{x} \cdot \mathbf{y} = \sum_{i=1}^{n} x_i y_i = x_1 y_1 + x_2 y_2 + \cdots + x_n y_n$$

**Geometric meaning**:

$$\mathbf{x} \cdot \mathbf{y} = \|\mathbf{x}\| \|\mathbf{y}\| \cos(\theta)$$

```python
v = np.array([3, 4])
w = np.array([2, 1])

# Dot product
dot_product = np.dot(v, w)
print(f"v · w = {dot_product}")

# Or
dot_product2 = v @ w
print(f"v @ w = {dot_product2}")

# Compute the angle between 2 vectors
norm_v = np.linalg.norm(v)
norm_w = np.linalg.norm(w)
cos_theta = dot_product / (norm_v * norm_w)
theta_rad = np.arccos(cos_theta)
theta_deg = np.degrees(theta_rad)

print(f"\n||v|| = {norm_v:.2f}")
print(f"||w|| = {norm_w:.2f}")
print(f"Angle between v and w: {theta_deg:.2f}°")
```

**Important properties**:
- If $$\mathbf{x} \cdot \mathbf{y} = 0$$: the 2 vectors are perpendicular (orthogonal)
- If $$\mathbf{x} \cdot \mathbf{y} > 0$$: Acute angle
- If $$\mathbf{x} \cdot \mathbf{y} < 0$$: Obtuse angle

#### Length (Norm)

**Euclidean norm (L2 norm)**:

$$\|\mathbf{x}\| = \sqrt{\sum_{i=1}^{n} x_i^2} = \sqrt{\mathbf{x} \cdot \mathbf{x}}$$

```python
v = np.array([3, 4])
norm = np.linalg.norm(v)
print(f"||v|| = {norm}")  # 5.0

# Unit vector
v_unit = v / norm
print(f"Unit vector: {v_unit}")
print(f"Length: {np.linalg.norm(v_unit)}")  # 1.0
```

## 2. Matrices

### 2.1. Definition

A **matrix** is a 2-dimensional array of numbers.

$$\mathbf{A} = \begin{bmatrix} 
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix}$$

**Size**: $$m \times n$$ (m rows, n columns)

```python
# Create matrices
A = np.array([[1, 2, 3],
              [4, 5, 6]])

B = np.array([[1, 2],
              [3, 4],
              [5, 6]])

print(f"A shape: {A.shape}")  # (2, 3)
print(f"B shape: {B.shape}")  # (3, 2)

# Special matrices
I = np.eye(3)  # 3x3 identity matrix
Z = np.zeros((2, 4))  # Zero matrix
O = np.ones((3, 2))  # Matrix of ones
```

### 2.2. Operations with Matrices

#### Addition/Subtraction (same size)

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print("A + B =")
print(A + B)

print("\nA - B =")
print(A - B)
```

#### Scalar Multiplication

```python
c = 2
print("2A =")
print(c * A)
```

#### Matrix Multiplication

**Condition**: The number of columns of A = the number of rows of B

If $$\mathbf{A}$$ is $$m \times n$$ and $$\mathbf{B}$$ is $$n \times p$$, then $$\mathbf{C} = \mathbf{AB}$$ is $$m \times p$$:

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

# Note: Matrix multiplication is not commutative
# A @ B ≠ B @ A (usually)
```

#### Transpose

$$(\mathbf{A}^T)_{ij} = a_{ji}$$

```python
A = np.array([[1, 2, 3],
              [4, 5, 6]])

A_T = A.T
print("A^T =")
print(A_T)

# Property: (A^T)^T = A
print("\n(A^T)^T = A?", np.array_equal(A_T.T, A))
```

### 2.3. The Inverse Matrix

Given a square matrix $$\mathbf{A}$$ ($$n \times n$$), the inverse matrix $$\mathbf{A}^{-1}$$ satisfies:

$$\mathbf{A} \mathbf{A}^{-1} = \mathbf{A}^{-1} \mathbf{A} = \mathbf{I}$$

**Note**: Not every matrix has an inverse (singular matrix).

```python
A = np.array([[1, 2],
              [3, 4]])

# Compute the inverse
A_inv = np.linalg.inv(A)
print("A^(-1) =")
print(A_inv)

# Check
I_check = A @ A_inv
print("\nA @ A^(-1) =")
print(I_check)

# Non-invertible matrix
singular = np.array([[1, 2],
                     [2, 4]])  # Row 2 = 2 * Row 1

try:
    singular_inv = np.linalg.inv(singular)
except np.linalg.LinAlgError:
    print("\nA singular matrix has no inverse!")
```

### 2.4. Determinant

Given a square matrix $$\mathbf{A}$$:

**2×2**:

$$\det(\mathbf{A}) = \begin{vmatrix} a & b \\ c & d \end{vmatrix} = ad - bc$$

**Properties**:
- $$\det(\mathbf{A}) \neq 0$$: the matrix is invertible
- $$\det(\mathbf{A}) = 0$$: the matrix is singular

```python
A = np.array([[1, 2],
              [3, 4]])

det_A = np.linalg.det(A)
print(f"det(A) = {det_A}")

# Singular matrix
singular = np.array([[1, 2],
                     [2, 4]])
det_singular = np.linalg.det(singular)
print(f"det(singular) = {det_singular:.10f}")  # ≈ 0
```

## 3. Systems of Linear Equations

The system of equations:

$$\begin{cases}
a_{11}x_1 + a_{12}x_2 + \cdots + a_{1n}x_n = b_1 \\
a_{21}x_1 + a_{22}x_2 + \cdots + a_{2n}x_n = b_2 \\
\vdots \\
a_{m1}x_1 + a_{m2}x_2 + \cdots + a_{mn}x_n = b_m
\end{cases}$$

**Matrix form**: $$\mathbf{Ax} = \mathbf{b}$$

**Solution** (if A is invertible): $$\mathbf{x} = \mathbf{A}^{-1}\mathbf{b}$$

```python
# System of equations:
# 2x + 3y = 8
# 5x + 4y = 13

A = np.array([[2, 3],
              [5, 4]])

b = np.array([8, 13])

# Solve using the inverse
x = np.linalg.inv(A) @ b
print(f"Solution (using inv): x = {x}")

# Solve using solve (more efficient)
x_solve = np.linalg.solve(A, b)
print(f"Solution (using solve): x = {x_solve}")

# Check
print(f"Check Ax = b: {np.allclose(A @ x, b)}")
```

## 4. Eigenvalues and Eigenvectors

Given a square matrix $$\mathbf{A}$$, if:

$$\mathbf{A}\mathbf{v} = \lambda \mathbf{v}$$

then $$\lambda$$ is an **eigenvalue** and $$\mathbf{v}$$ is the corresponding **eigenvector**.

**Meaning**: The vector $$\mathbf{v}$$ is only scaled (its direction does not change) when multiplied by $$\mathbf{A}$$.

```python
A = np.array([[4, 2],
              [1, 3]])

# Compute eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

print("Eigenvalues:")
print(eigenvalues)

print("\nEigenvectors:")
print(eigenvectors)

# Check
for i in range(len(eigenvalues)):
    lambda_i = eigenvalues[i]
    v_i = eigenvectors[:, i]
    
    Av = A @ v_i
    lambda_v = lambda_i * v_i
    
    print(f"\nEigenvalue {i+1}: λ = {lambda_i:.4f}")
    print(f"Av = {Av}")
    print(f"λv = {lambda_v}")
    print(f"Match? {np.allclose(Av, lambda_v)}")
```

## 5. Applications in Statistics

### 5.1. Covariance Matrix

Given data $$\mathbf{X}$$ ($$n \times p$$), the covariance matrix:

$$\mathbf{\Sigma} = \frac{1}{n-1} \mathbf{X}^T \mathbf{X}$$

(after centering the data)

```python
# Create data
np.random.seed(42)
n = 100
X = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], n)

# Compute the covariance matrix
cov_matrix = np.cov(X.T)
print("Covariance Matrix:")
print(cov_matrix)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Scatter plot
axes[0].scatter(X[:, 0], X[:, 1], alpha=0.6)
axes[0].set_xlabel('X₁')
axes[0].set_ylabel('X₂')
axes[0].set_title('Data')
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

Model: $$\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}$$

**OLS solution** (Ordinary Least Squares):

$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$

```python
# Create data
np.random.seed(42)
n = 100
X = np.random.normal(0, 1, (n, 2))
true_beta = np.array([2, -1])
y = X @ true_beta + np.random.normal(0, 0.5, n)

# Add intercept
X_with_intercept = np.column_stack([np.ones(n), X])

# Compute beta
beta_hat = np.linalg.inv(X_with_intercept.T @ X_with_intercept) @ X_with_intercept.T @ y

print("True beta:", true_beta)
print("Estimated beta:", beta_hat[1:])  # Drop the intercept
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

## 6. Summary of Important Formulas

| Operation | Notation | Formula |
|-----------|---------|-----------|
| Dot product | $$\mathbf{x} \cdot \mathbf{y}$$ | $$\sum_{i=1}^{n} x_i y_i$$ |
| Norm | $$\|\mathbf{x}\|$$ | $$\sqrt{\sum_{i=1}^{n} x_i^2}$$ |
| Matrix multiplication | $$\mathbf{AB}$$ | $$c_{ij} = \sum_{k} a_{ik}b_{kj}$$ |
| Transpose | $$\mathbf{A}^T$$ | $$(\mathbf{A}^T)_{ij} = a_{ji}$$ |
| Inverse | $$\mathbf{A}^{-1}$$ | $$\mathbf{AA}^{-1} = \mathbf{I}$$ |
| Determinant | $$\det(\mathbf{A})$$ | Scalar value |
| Eigenvalue | $$\lambda$$ | $$\mathbf{Av} = \lambda\mathbf{v}$$ |

---

### Worked Numerical Example: Hand-Computing Cholesky & Precision Updating on a $$2	imes 2$$ Covariance Matrix

Suppose a 2-parameter posterior has covariance matrix:

$$\Sigma = egin{pmatrix} 4 & 2 \ 2 & 5 \end{pmatrix}.$$

1. **Check correlation & positive definiteness:**
   - Standard deviations: $$\sigma_1 = \sqrt{4} = 2$$, $$\sigma_2 = \sqrt{5} pprox 2.236$$; correlation $$ho = rac{2}{2\sqrt{5}} pprox 0.447$$.
   - Determinant: $$\det(\Sigma) = 4(5) - 2^2 = 16 > 0$$ and trace $$4+5=9 > 0$$ $$\implies$$ strictly positive definite!
2. **Compute its lower-triangular Cholesky factor $$L$$ ($$\Sigma = L L^T$$) by hand:**
   - $$L_{11} = \sqrt{4} = 2$$.
   - $$L_{21} = rac{2}{L_{11}} = rac{2}{2} = 1$$.
   - $$L_{22} = \sqrt{5 - L_{21}^2} = \sqrt{5 - 1} = 2$$.
   So $$L = egin{pmatrix} 2 & 0 \ 1 & 2 \end{pmatrix}$$! Verify: $$L L^T = egin{pmatrix} 2 & 0 \ 1 & 2 \end{pmatrix}egin{pmatrix} 2 & 1 \ 0 & 2 \end{pmatrix} = egin{pmatrix} 4 & 2 \ 2 & 5 \end{pmatrix}$$—exact!
3. **Generate one correlated draw from $$\mathbf{z} = (1, -1)^T$$:**
   $$L\mathbf{z} = egin{pmatrix} 2(1) + 0 \ 1(1) + 2(-1) \end{pmatrix} = egin{pmatrix} 2 \ -1 \end{pmatrix}.$$

### Deep-Dive Explanation: Four Linear-Algebra Habits for Bayesian Modeling (Read Slowly)

1. **Never invert a matrix explicitly when solving $$A\mathbf{x}=\mathbf{b}$$:** Use `np.linalg.solve(A, b)` or Cholesky solves instead of `np.linalg.inv(A) @ b` for far higher speed and numerical stability.
2. **Watch the condition number of $$\mathbf{X}^T\mathbf{X}$$:** Collinear predictors create tiny eigenvalues in $$\mathbf{X}^T\mathbf{X}$$, stretching the posterior into a razor-thin ridge—standardizing predictors (`(x - mean)/sd`) immediately improves geometry!
3. **Think in precision matrices ($$\Sigma^{-1}$$) for Gaussian Bayes:** Just as 1D precisions add ($$	au_{	ext{post}} = 	au_{	ext{prior}} + 	au_{	ext{data}}$$), in $$d$$ dimensions $$\Sigma_{	ext{post}}^{-1} = \Sigma_{	ext{prior}}^{-1} + rac{1}{\sigma^2}\mathbf{X}^T\mathbf{X}$$!
4. **Use Cholesky for non-centered parameterizations in Stan/PyMC:** Sampling standard Normal $$\mathbf{z}$$ and transforming via $$L\mathbf{z}$$ lets Hamiltonian Monte Carlo explore correlated posteriors effortlessly.

**Quick check.** For the matrix $$\Sigma = egin{pmatrix} 4 & 2 \ 2 & 5 \end{pmatrix}$$ above (with $$\det(\Sigma) = 16$$), what is its inverse—the **precision matrix** $$\Lambda = \Sigma^{-1}$$?

---

## Reference videos

- [Vectors | Chapter 1, Essence of linear algebra](https://www.youtube.com/watch?v=fNk_zzaMoSs) — 3Blue1Brown, English. **watch first**. Watch to see a vector as a geometric object, exactly the part of the lesson that gathers data and parameters into vectors.
- [Matrix multiplication as composition | Chapter 4, Essence of linear algebra](https://www.youtube.com/watch?v=XkY2DOUCWMU) — 3Blue1Brown, English. Watch matrix multiplication as a transformation, supporting the part that writes regression as a linear operator.
- [Eigenvectors and eigenvalues | Chapter 14, Essence of linear algebra](https://www.youtube.com/watch?v=PFDu9oVAE-g) — 3Blue1Brown, English. Watch eigenvalues and eigenvectors, used for the eigenvalues section of the lesson when talking about the structure of a matrix.

## Exercises

1. **Vectors**: Given $$\mathbf{v} = [2, 3, -1]$$ and $$\mathbf{w} = [1, -2, 4]$$. Compute:
   - $$\mathbf{v} + \mathbf{w}$$
   - $$\mathbf{v} \cdot \mathbf{w}$$
   - $$\|\mathbf{v}\|$$
   - The angle between $$\mathbf{v}$$ and $$\mathbf{w}$$

2. **Matrices**: Given $$\mathbf{A} = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$$ and $$\mathbf{B} = \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}$$. Compute:
   - $$\mathbf{A} + \mathbf{B}$$
   - $$\mathbf{AB}$$
   - $$\mathbf{A}^T$$
   - $$\mathbf{A}^{-1}$$
   - $$\det(\mathbf{A})$$

3. **Systems of equations**: Solve the system:
   $$\begin{cases} 3x + 2y = 7 \\ x - y = 1 \end{cases}$$

4. **Eigenvalues**: Find the eigenvalues and eigenvectors of $$\mathbf{A} = \begin{bmatrix} 3 & 1 \\ 1 & 3 \end{bmatrix}$$

5. **Linear Regression**: Generate data $$y = 3x_1 - 2x_2 + \epsilon$$ with 100 samples. Estimate $$\beta$$ using the OLS formula.

## References

1. **Strang, G. (2016).** *Introduction to Linear Algebra*. Wellesley-Cambridge Press.
2. **3Blue1Brown - Essence of Linear Algebra** - https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab
3. **NumPy Linear Algebra** - https://numpy.org/doc/stable/reference/routines.linalg.html

---

*This lesson concludes the basic prerequisite knowledge. You are ready to start the Bayesian Statistics course!*


---

*Next lesson: [0.9 Basic Calculus]({{ site.baseurl }}/contents/en/chapter00/00_06_calculus_basics/)*
