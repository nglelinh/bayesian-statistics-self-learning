---
layout: post
title: "Lesson 0.9: Basic Calculus"
chapter: '00'
order: 9
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

Every continuous Bayesian inference problem quietly runs on two engines from calculus: **integration** (summing area under the prior $$	imes$$ likelihood curve to compute the normalizing evidence $$P(D) = \int P(D\mid	heta)P(	heta)\,d	heta$$) and **differentiation** (finding the peak MAP estimate where $$
abla_	heta \log p(	heta\mid D) = 0$$ and steering **Hamiltonian Monte Carlo / NUTS** along the gradient of the log-posterior!).

This lesson refreshes single- and multi-variable calculus directly through a Bayesian lens: derivatives, gradients, Hessians (curvature = precision!), and integrals as expectations.

---

## Background Knowledge Map: Where Calculus Shows Up Inside Bayesian Inference

Four calculus tools power almost every algorithm in this course:

1. **Derivatives & Optimization (MLE / MAP):** Setting the first derivative of the log-posterior $$rac{d}{d	heta}\log p(	heta\mid D) = 0$$ locates the **Maximum A Posteriori (MAP)** mode cleanly without ever needing to compute the normalizing integral!
2. **Second Derivative / Hessian = Curvature = Posterior Precision:** The negative second derivative $$-rac{d^2}{d	heta^2}\log p(	heta\mid D)$$ at the mode measures how sharply peaked the posterior is—giving the **Laplace approximation** variance $$\sigma_{	ext{post}}^2 pprox \left(-\ell''(\hat{	heta})ight)^{-1}$$!
3. **Gradients & Automatic Differentiation (HMC / NUTS):** Modern Bayesian samplers (Stan, PyMC) treat $$-\log p(	heta\mid D)$$ as a gravitational potential energy landscape and use exact gradients $$
abla_	heta \log p(	heta\mid D)$$ to glide efficiently across high-dimensional posteriors.
4. **Integrals as Expectations & Marginalization:** Posterior means $$\mathbb{E}[	heta\mid D] = \int 	heta\,p(	heta\mid D)\,d	heta$$ and posterior predictive distributions are integrals—computed analytically for conjugate models or approximated by Monte Carlo averages $$rac{1}{S}\sum 	heta^{(s)}$$.

---

## Learning objectives

After this lesson, you will grasp the roles of derivatives, integrals, and optimization in Bayesian statistical inference. Specifically, you will understand the derivative as a tool for sensitivity analysis and finding extrema, the integral as normalization and computing probabilities over continuous domains, and optimization as the step of finding approximate solutions (for example the MAP) before or alongside sampling the posterior.

## Introduction: why is calculus at the core of continuous Bayes?

Many Bayesian models work with continuous parameters. In that case, three mathematical operations appear again and again: taking derivatives to optimize the log-posterior function, taking integrals to normalize distributions and marginalize latent variables, and using gradients to design efficient computational algorithms. So calculus is not an auxiliary part; it is the core that turns a probability model into computable inference.

In this lesson, every formula will be read on two levels: the formal level (mathematical notation) and the statistical meaning level (which question it answers in data analysis). This two-level reading is an important skill for the MCMC, Bayesian regression, and model checking chapters.

## A framework connecting to the Bayesian workflow

A typical workflow can be written briefly:

$$
\text{prior} \times \text{likelihood} \propto \text{posterior (unnormalized)}.
$$

From here, calculus takes part at two points:

1. **Derivatives**: find the extrema of the log-posterior (MAP, Laplace approximation).
2. **Integrals**: normalize the posterior or compute probabilities/expectations over a continuous domain.

## 1. Derivatives

### 1.1. Definition

The **derivative** measures the rate of change of a function:

$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

**Geometric meaning**: The slope of the tangent line at the point $$x$$.

```python
import numpy as np
import matplotlib.pyplot as plt

# Function
def f(x):
    return x**2

# Derivative (analytical)
def f_prime(x):
    return 2*x

# Numerical derivative
def numerical_derivative(f, x, h=1e-5):
    return (f(x + h) - f(x)) / h

# Plot the function and the tangent line
x = np.linspace(-3, 3, 100)
y = f(x)

x0 = 1.5
y0 = f(x0)
slope = f_prime(x0)

# Tangent line: y - y0 = slope * (x - x0)
tangent_y = y0 + slope * (x - x0)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2, label='f(x) = x²')
plt.plot(x, tangent_y, 'r--', linewidth=2, label=f'Tangent at x={x0}')
plt.scatter([x0], [y0], color='red', s=100, zorder=5)
plt.xlabel('x')
plt.ylabel('y')
plt.title('The Derivative is the Slope of the Tangent')
plt.legend()
plt.grid(alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.axvline(x=0, color='k', linewidth=0.5)
plt.show()

# Compare analytical vs numerical derivative
x_test = 2.0
analytical = f_prime(x_test)
numerical = numerical_derivative(f, x_test)
print(f"Derivative at x={x_test}:")
print(f"  Analytical: {analytical}")
print(f"  Numerical: {numerical:.10f}")
```

### 1.2. Basic Derivative Rules

| Function | Derivative |
|-----|---------|
| $$c$$ (constant) | $$0$$ |
| $$x^n$$ | $$nx^{n-1}$$ |
| $$e^x$$ | $$e^x$$ |
| $$\ln(x)$$ | $$\frac{1}{x}$$ |
| $$\sin(x)$$ | $$\cos(x)$$ |
| $$\cos(x)$$ | $$-\sin(x)$$ |

**Sum rule**: $$(f + g)' = f' + g'$$

**Product rule**: $$(fg)' = f'g + fg'$$

**Quotient rule**: $$\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}$$

**Chain rule**: $$(f(g(x)))' = f'(g(x)) \cdot g'(x)$$

```python
# Example: f(x) = (x² + 1)³
def f(x):
    return (x**2 + 1)**3

# Derivative by the chain rule:
# f'(x) = 3(x² + 1)² · 2x = 6x(x² + 1)²
def f_prime(x):
    return 6*x * (x**2 + 1)**2

# Check
x_test = 1.0
analytical = f_prime(x_test)
numerical = numerical_derivative(f, x_test)
print(f"\nf(x) = (x² + 1)³ at x={x_test}:")
print(f"  Analytical: {analytical}")
print(f"  Numerical: {numerical:.10f}")
```

### 1.3. Partial Derivatives

Given a function of several variables $$f(x, y)$$, the partial derivative with respect to $$x$$:

$$\frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x+h, y) - f(x, y)}{h}$$

(holding $$y$$ fixed)

```python
# Function of 2 variables: f(x, y) = x²y + y³
def f(x, y):
    return x**2 * y + y**3

# Partial derivatives
def df_dx(x, y):
    return 2*x*y

def df_dy(x, y):
    return x**2 + 3*y**2

# Plot the 3D function
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

# Contour plot with gradient
ax2 = fig.add_subplot(122)
contour = ax2.contour(X, Y, Z, levels=15, cmap='viridis')
ax2.clabel(contour, inline=True, fontsize=8)

# Plot the gradient at some points
x_points = np.linspace(-1.5, 1.5, 8)
y_points = np.linspace(-1.5, 1.5, 8)
for xi in x_points:
    for yi in y_points:
        dx = df_dx(xi, yi)
        dy = df_dy(xi, yi)
        ax2.quiver(xi, yi, dx, dy, color='red', scale=50, width=0.003)

ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_title('Contour and Gradient')
ax2.set_aspect('equal')

plt.tight_layout()
plt.show()

# Compute at a specific point
x0, y0 = 1, 2
print(f"\nAt (x, y) = ({x0}, {y0}):")
print(f"  f = {f(x0, y0)}")
print(f"  ∂f/∂x = {df_dx(x0, y0)}")
print(f"  ∂f/∂y = {df_dy(x0, y0)}")
```

### 1.4. Gradient

The **gradient** is the vector of all partial derivatives:

$$\nabla f = \begin{bmatrix} \frac{\partial f}{\partial x_1} \\ \frac{\partial f}{\partial x_2} \\ \vdots \\ \frac{\partial f}{\partial x_n} \end{bmatrix}$$

**Meaning**: The direction in which the function increases fastest.

```python
def gradient_f(x, y):
    return np.array([df_dx(x, y), df_dy(x, y)])

x0, y0 = 1, 1
grad = gradient_f(x0, y0)
print(f"\nGradient at ({x0}, {y0}): {grad}")
print(f"Magnitude: {np.linalg.norm(grad):.4f}")
```

## 2. Integrals

### 2.1. Definite Integrals

**Meaning**: The area under a curve.

$$\int_a^b f(x) dx$$

```python
# Function
def f(x):
    return x**2

# Analytical integral: ∫x² dx = x³/3
def F(x):
    return x**3 / 3

# Integral from 0 to 2
a, b = 0, 2
integral_analytical = F(b) - F(a)

# Numerical integral
from scipy import integrate
integral_numerical, error = integrate.quad(f, a, b)

print(f"Integral ∫₀² x² dx:")
print(f"  Analytical: {integral_analytical:.6f}")
print(f"  Numerical: {integral_numerical:.6f}")

# Plot
x = np.linspace(0, 3, 100)
y = f(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2, label='f(x) = x²')

# Shade the region of integration
x_fill = np.linspace(a, b, 100)
y_fill = f(x_fill)
plt.fill_between(x_fill, y_fill, alpha=0.3, color='blue', 
                label=f'Area = {integral_analytical:.2f}')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Integral = Area under the Curve')
plt.legend()
plt.grid(alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.axvline(x=0, color='k', linewidth=0.5)
plt.show()
```

### 2.2. Integrals in Probability

A **PDF** (Probability Density Function) must satisfy:

$$\int_{-\infty}^{\infty} f(x) dx = 1$$

**Probability**:

$$P(a \leq X \leq b) = \int_a^b f(x) dx$$

```python
from scipy import stats

# Normal distribution
mu, sigma = 0, 1
x = np.linspace(-4, 4, 1000)
pdf = stats.norm.pdf(x, mu, sigma)

# Compute P(-1 ≤ X ≤ 1)
a, b = -1, 1
prob, _ = integrate.quad(lambda x: stats.norm.pdf(x, mu, sigma), a, b)

plt.figure(figsize=(10, 6))
plt.plot(x, pdf, 'b-', linewidth=2, label='N(0, 1)')

# Shade the probability region
x_fill = np.linspace(a, b, 100)
pdf_fill = stats.norm.pdf(x_fill, mu, sigma)
plt.fill_between(x_fill, pdf_fill, alpha=0.3, color='blue',
                label=f'P(-1 ≤ X ≤ 1) = {prob:.4f}')

plt.xlabel('x')
plt.ylabel('Density')
plt.title('Probability = Area under the PDF')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# Compare with the CDF
prob_cdf = stats.norm.cdf(b, mu, sigma) - stats.norm.cdf(a, mu, sigma)
print(f"\nP(-1 ≤ X ≤ 1):")
print(f"  Integral: {prob:.6f}")
print(f"  CDF: {prob_cdf:.6f}")
```

### 2.3. Multivariable Integrals

$$\int \int f(x, y) \, dx \, dy$$

```python
# Function of 2 variables
def f(x, y):
    return x * y

# Integral over [0,1] × [0,2]
result, error = integrate.dblquad(f, 0, 2, 0, 1)
print(f"\n∫₀¹ ∫₀² xy dy dx = {result:.6f}")

# Analytical: ∫₀¹ x dx · ∫₀² y dy = [x²/2]₀¹ · [y²/2]₀² = 0.5 · 2 = 1
analytical = 0.5 * 2
print(f"Analytical: {analytical}")
```

## 3. Optimization

### 3.1. Extrema

**Necessary condition**:

$$f'(x) = 0$$

**Sufficient condition**:
- $$f''(x) > 0$$: Minimum
- $$f''(x) < 0$$: Maximum

```python
# Function: f(x) = x³ - 6x² + 9x + 1
def f(x):
    return x**3 - 6*x**2 + 9*x + 1

def f_prime(x):
    return 3*x**2 - 12*x + 9

def f_double_prime(x):
    return 6*x - 12

# Find the critical points: f'(x) = 0
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
        label = f'Min at x={xc}'
        color = 'green'
    else:
        marker = '^'  # Maximum
        label = f'Max at x={xc}'
        color = 'red'
    
    plt.scatter([xc], [yc], s=200, marker=marker, color=color, 
               label=label, zorder=5, edgecolor='black', linewidth=2)
    
    print(f"\nx = {xc}:")
    print(f"  f(x) = {yc:.4f}")
    print(f"  f'(x) = {f_prime(xc):.4f}")
    print(f"  f''(x) = {f2:.4f}")
    print(f"  → {'Minimum' if f2 > 0 else 'Maximum'}")

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Finding Extrema')
plt.legend()
plt.grid(alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.show()
```

### 3.2. Gradient Descent

**Algorithm** for finding the minimum:

$$x_{n+1} = x_n - \alpha \nabla f(x_n)$$

where $$\alpha$$ is the learning rate.

```python
# Function of 2 variables: f(x, y) = x² + y²
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

# Run from the starting point
x0, y0 = 3, 2
path = gradient_descent(x0, y0, alpha=0.1, n_iter=20)

# Plot
x = np.linspace(-4, 4, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

plt.figure(figsize=(10, 8))
contour = plt.contour(X, Y, Z, levels=20, cmap='viridis')
plt.clabel(contour, inline=True, fontsize=8)

# Plot the path
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
print(f"Start: ({x0}, {y0}), f = {f(x0, y0):.4f}")
print(f"End: ({path[-1, 0]:.6f}, {path[-1, 1]:.6f}), f = {f(path[-1, 0], path[-1, 1]):.6f}")
```

### 3.3. Maximum Likelihood Estimation (MLE)

**Example**: Estimate the parameter $$\mu$$ of a Normal distribution.

**Likelihood**:

$$L(\mu) = \prod_{i=1}^{n} \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x_i - \mu)^2}{2\sigma^2}\right)$$

**Log-likelihood**:

$$\ell(\mu) = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^{n}(x_i - \mu)^2$$

**Find the maximum**: $$\frac{d\ell}{d\mu} = 0$$

$$\Rightarrow \hat{\mu} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

```python
# Data
np.random.seed(42)
true_mu = 5
sigma = 2
data = np.random.normal(true_mu, sigma, 100)

# Log-likelihood function
def log_likelihood(mu, data, sigma):
    n = len(data)
    return -n/2 * np.log(2*np.pi*sigma**2) - 1/(2*sigma**2) * np.sum((data - mu)**2)

# Plot the log-likelihood
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

## 4. Applications in Bayesian Statistics

### 4.1. Posterior Mode (MAP)

**Maximum A Posteriori** (MAP): Find the mode of the posterior.

$$\hat{\theta}_{MAP} = \arg\max_\theta p(\theta \mid \mathbf{x})$$

Equivalently:

$$\hat{\theta}_{MAP} = \arg\max_\theta [\log p(\mathbf{x} \mid \theta) + \log p(\theta)]$$

### 4.2. Laplace Approximation

Approximate the posterior by a Normal distribution at the mode:

$$p(\theta \mid \mathbf{x}) \approx \mathcal{N}\left(\hat{\theta}, \left[-\frac{d^2 \log p(\theta \mid \mathbf{x})}{d\theta^2}\bigg|_{\hat{\theta}}\right]^{-1}\right)$$

```python
# Example: Beta posterior
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
# Compute the second derivative
def log_posterior_second_deriv(theta):
    return -(alpha_post - 1) / theta**2 - (beta_post - 1) / (1 - theta)**2

variance_laplace = -1 / log_posterior_second_deriv(theta_map)
std_laplace = np.sqrt(variance_laplace)

# Plot
theta = np.linspace(0.01, 0.99, 200)
posterior = stats.beta.pdf(theta, alpha_post, beta_post)
laplace_approx = stats.norm.pdf(theta, theta_map, std_laplace)

plt.figure(figsize=(10, 6))
plt.plot(theta, posterior, 'b-', linewidth=2, label='True Posterior (Beta)')
plt.plot(theta, laplace_approx, 'r--', linewidth=2, label='Laplace Approximation (Normal)')
plt.axvline(theta_map, color='green', linestyle='--', 
           label=f'MAP: θ̂ = {theta_map:.3f}')
plt.xlabel('θ')
plt.ylabel('Density')
plt.title('Laplace Approximation')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

print(f"\nMAP: {theta_map:.4f}")
print(f"Laplace std: {std_laplace:.4f}")
print(f"True std: {np.sqrt(alpha_post * beta_post / ((alpha_post + beta_post)**2 * (alpha_post + beta_post + 1))):.4f}")
```

---

### Worked Numerical Example: Finding the MAP Mode and Laplace Variance of $$\mathrm{Beta}(8, 12)$$ by Hand

Take the unnormalized log-posterior of $$\mathrm{Beta}(lpha=8, eta=12)$$:

$$g(p) = \ln\!igl(p^{8-1}(1-p)^{12-1}igr) = 7\ln p + 11\ln(1-p).$$

1. **First derivative $$	o$$ exact MAP mode:**
   $$g'(p) = rac{7}{p} - rac{11}{1-p} = 0 \implies 7(1-p) = 11p \implies 18p = 7 \implies \hat{p}_{	ext{MAP}} = rac{7}{18} pprox \mathbf{0.3889}.$$
2. **Second derivative at the mode $$	o$$ Laplace curvature & SD:**
   $$g''(p) = -rac{7}{p^2} - rac{11}{(1-p)^2}.$$
   Evaluate at $$\hat{p} = 7/18$$ (so $$1-\hat{p} = 11/18$$):
   $$-g''(\hat{p}) = rac{7}{(7/18)^2} + rac{11}{(11/18)^2} = rac{18^2}{7} + rac{18^2}{11} = 324\!\left(rac{18}{77}ight) pprox 75.74.$$
   Invert to get the Laplace approximate variance and SD:
   $$\sigma_{	ext{Laplace}} = rac{1}{\sqrt{75.74}} pprox \mathbf{0.1149}$$
   *(remarkably close to the exact $$\mathrm{Beta}(8,12)$$ standard deviation $$0.1069$$!)*

### Deep-Dive Explanation: Four Calculus Insights That Make Bayesian Algorithms Click (Read Slowly)

1. **Always differentiate the *log*-posterior, never the raw posterior:** Taking logs turns products of $$n$$ likelihood terms into sums, makes derivatives linear, and guarantees concavity for exponential families.
2. **Higher curvature means *less* uncertainty:** A sharp, narrow log-posterior peak has a large negative second derivative $$-g''(\hat{	heta})$$, which translates directly into a small posterior variance!
3. **Never confuse an integral over *data* with an integral over *parameters*:** Normalization integrates over $$	heta$$ ($$\int p(D\mid	heta)p(	heta)\,d	heta$$), which is why a likelihood function $$L(	heta)$$ by itself does *not* integrate to 1 over $$	heta$$!
4. **Change-of-variables requires a Jacobian:** If you transform a parameter (e.g., $$\phi = \log \sigma$$ for unconstrained HMC sampling), you must multiply the density by $$\lvert rac{d\sigma}{d\phi}vert$$ so total probability mass is conserved.

**Quick check.** For $$\mathrm{Beta}(8, 12)$$, the exact posterior mean is $$8/20 = 0.400$$ while the MAP mode we just found is $$7/18 pprox 0.389$$. Why is the mode slightly smaller than the mean? *(Hint: check which direction $$\mathrm{Beta}(8,12)$$ is skewed!)*

---

## Reference videos

- [The paradox of the derivative | Chapter 2, Essence of calculus](https://www.youtube.com/watch?v=9vKqVkMQHKk) — 3Blue1Brown, English. **watch first**. Watch the derivative as sensitivity when the input is nudged a little, exactly the part of the lesson that uses derivatives to read the log-posterior.
- [Integration and the fundamental theorem of calculus | Chapter 8, Essence of calculus](https://www.youtube.com/watch?v=rfG8ce4nNh0) — 3Blue1Brown, English. Watch the integral as the accumulation of small changes, supporting the part on normalizing distributions and computing probabilities over a continuous domain.
- [Gradient descent, how neural networks learn | Deep Learning Chapter 2](https://www.youtube.com/watch?v=IHZwWFHWa-w) — 3Blue1Brown, English. Watch gradient descent as walking against the steepest slope; the context is neural networks, but the mechanism matches the optimization part of the lesson.

## Exercises

1. **Derivatives**: Compute the derivative of:
   - $$f(x) = 3x^4 - 2x^2 + 5$$
   - $$g(x) = e^{x^2}$$
   - $$h(x) = \ln(x^2 + 1)$$

2. **Partial derivatives**: Given $$f(x, y) = x^2y + xy^2$$. Compute $$\frac{\partial f}{\partial x}$$ and $$\frac{\partial f}{\partial y}$$.

3. **Integrals**: Compute:
   - $$\int_0^1 x^2 dx$$
   - $$\int_1^e \frac{1}{x} dx$$
   - $$\int_{-\infty}^{\infty} e^{-x^2} dx$$ (hint: $$\sqrt{\pi}$$)

4. **Optimization**: Find the extrema of $$f(x) = x^3 - 3x + 1$$.

5. **MLE**: Given data from Exponential($$\lambda$$). Find the MLE of $$\lambda$$.
   - Likelihood: $$L(\lambda) = \prod_{i=1}^{n} \lambda e^{-\lambda x_i}$$
   - Hint: $$\hat{\lambda} = \frac{n}{\sum x_i}$$

## References

1. **Stewart, J. (2015).** *Calculus: Early Transcendentals*. Cengage Learning.
2. **3Blue1Brown - Essence of Calculus** - https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr
3. **SciPy Integrate** - https://docs.scipy.org/doc/scipy/reference/integrate.html

---

*This lesson completes the basic prerequisite knowledge. You are ready for Bayesian Statistics!*


---

*Next lesson: [0.10 Probability Density Functions (PDF)]({{ site.baseurl }}/contents/en/chapter00/00_07_probability_density_functions/)*
