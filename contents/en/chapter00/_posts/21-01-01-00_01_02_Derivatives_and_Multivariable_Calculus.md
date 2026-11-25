---
layout: post
title: 00-01-02 Derivatives and Multivariable Calculus
chapter: '00'
order: 25
owner: GitHub Copilot
lang: en
categories:
- chapter00
lesson_type: required
---

This lesson covers derivatives and essential multivariable calculus concepts that form the foundation for optimization theory and algorithms.

---

When Hamiltonian Monte Carlo (HMC / NUTS) explores a 50-dimensional Bayesian posterior in Stan or PyMC, how does it know which direction leads uphill toward higher probability without blindly stumbling in 50 dimensions? It follows the **gradient vector $$\nabla_\theta \log p(\theta\mid y)$$**—and uses the **multivariable chain rule** (reverse-mode automatic differentiation) to compute all 50 partial derivatives in a single backward pass!

This mathematical reference sharpens the exact multivariable calculus tools that power modern Bayesian optimization and sampling: partial derivatives, gradients, Hessians, and the multivariable chain rule.

---

## Key ideas: Multivariable Calculus Inside Modern Bayesian Engines

1. **Gradient Vector ($$\nabla f$$):** Points in the direction of steepest ascent of the log-posterior; setting $$\nabla_\theta \log p(\theta\mid y) = \mathbf{0}$$ locates the MAP mode.
2. **Hessian Matrix ($$\mathbf{H}$$):** The matrix of second partial derivatives measures local curvature—its negative inverse $$(-\mathbf{H})^{-1}$$ at the mode gives the **Laplace covariance matrix**!
3. **Multivariable Chain Rule & Reverse-Mode Autodiff:** Composing priors, link functions (logit/exp), and likelihoods creates a computational graph; the chain rule propagates sensitivities backward in $$O(1)$$ passes regardless of parameter count.
4. **Jacobian Determinants for Constrained Parameters:** Transforming $$\sigma > 0$$ via $$\sigma = e^\phi$$ changes volume elements by $$\lvert \frac{d\sigma}{d\phi}\rvert = e^\phi$$—required so HMC samples the true target posterior!

---

## Derivatives and Rate of Change

The derivative of a single variable function represents its instantaneous rate of change, which is fundamental to understanding how functions behave locally.

### Basic Derivative Concepts

**Slope between two points:**

$$\text{Slope} = \frac{y_2 - y_1}{x_2 - x_1}$$

**Derivative (instantaneous rate of change):**

$$f'(x_0) = \lim_{x_1 \to x_0} \frac{f(x_1) - f(x_0)}{x_1 - x_0} = \lim_{\Delta x \to 0} \frac{f(x_0 + \Delta x) - f(x_0)}{\Delta x}$$

The derivative tells us how quickly the function is changing at any given point, which is essential for finding optimal points where the rate of change is zero.

### Level Curves of Functions

Level curves are a fundamental concept in multivariable calculus used to visualize functions of two variables, typically denoted as $$f(x, y)$$. They provide a way to represent a 3D surface in a 2D plane.

A **level curve** of a function $$f(x, y)$$ is the set of all points $$(x, y)$$ in the domain of $$f$$ where the function takes a constant value:

$$f(x, y) = c$$

**Examples:**
- For $$f(x, y) = x^2 + y^2$$, the level curves are circles: $$x^2 + y^2 = c$$
- For $$f(x, y) = x + y$$, the level curves are parallel lines: $$x + y = c$$

Level curves help us understand:
1. The topography of the function
2. Directions of steepest ascent and descent
3. Locations of potential optima

---

## Multivariable Calculus Key Concepts

### Partial Derivatives

For a function $$f(x_1, x_2, \ldots, x_n)$$, the **partial derivative** with respect to $$x_i$$ is:

$$\frac{\partial f}{\partial x_i} = \lim_{h \to 0} \frac{f(x_1, \ldots, x_i + h, \ldots, x_n) - f(x_1, \ldots, x_i, \ldots, x_n)}{h}$$

This measures how $$f$$ changes when only $$x_i$$ varies while all other variables remain fixed.

### Gradient Vector

The **gradient** is a vector composed of all partial derivatives:

$$\nabla f(\mathbf{x}) = \begin{pmatrix} \frac{\partial f}{\partial x_1} \\ \frac{\partial f}{\partial x_2} \\ \vdots \\ \frac{\partial f}{\partial x_n} \end{pmatrix}$$

The gradient points in the direction of steepest increase of the function and is perpendicular to level curves.

### Hessian Matrix

The **Hessian matrix** contains all second-order partial derivatives:

$$\nabla^2 f(\mathbf{x}) = \mathbf{H} = \begin{pmatrix} 
\frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_1 \partial x_n} \\
\frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \cdots & \frac{\partial^2 f}{\partial x_2 \partial x_n} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial^2 f}{\partial x_n \partial x_1} & \frac{\partial^2 f}{\partial x_n \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_n^2}
\end{pmatrix}$$

The Hessian provides information about the curvature of the function and is crucial for:
- Determining the nature of critical points (minimum, maximum, or saddle point)
- Second-order optimization methods like Newton's method

---

## Chain Rule for Multivariable Functions

The chain rule is fundamental for computing derivatives of composite functions, which frequently appear in optimization problems.

### Basic Chain Rule

For a function $$z = f(x, y)$$ where $$x = g(t)$$ and $$y = h(t)$$:

$$ \frac{dz}{dt} = \frac{\partial f}{\partial x} \frac{dx}{dt} + \frac{\partial f}{\partial y} \frac{dy}{dt} $$

### General Chain Rule

For $$z = f(x_1, x_2, \ldots, x_n)$$ where each $$x_i = x_i(t_1, t_2, \ldots, t_m)$$:

$$ \frac{\partial z}{\partial t_j} = \sum_{i=1}^{n} \frac{\partial f}{\partial x_i} \frac{\partial x_i}{\partial t_j} $$

### Applications in Optimization

The chain rule is essential for:

1. **Gradient Computation**: Computing gradients of composite objective functions
2. **Constraint Handling**: Dealing with constraints that are functions of other variables
3. **Algorithm Implementation**: Backpropagation in neural networks and automatic differentiation
4. **Sensitivity Analysis**: Understanding how changes in parameters affect optimal solutions

### Example: Optimization with Constraints

Consider minimizing $$f(x, y) = x^2 + y^2$$ subject to $$g(x, y) = x + y - 1 = 0$$.

Using the constraint to eliminate one variable: $$y = 1 - x$$, so we minimize:
$$h(x) = f(x, 1-x) = x^2 + (1-x)^2$$

Using the chain rule:
$$h'(x) = \frac{\partial f}{\partial x} \cdot 1 + \frac{\partial f}{\partial y} \cdot \frac{d(1-x)}{dx} = 2x + 2(1-x)(-1) = 4x - 2$$

Setting $$h'(x) = 0$$ gives $$x = 1/2$$, so the optimal point is $$(1/2, 1/2)$$.

This demonstrates how multivariable calculus concepts work together to solve optimization problems systematically.

---

### Worked Numerical Example: Computing Gradient and Hessian of a 2D Log-Posterior by Hand

Consider a 2-parameter Gaussian log-posterior $$g(\mu, \beta) = -\frac{1}{2}\!\left(2(\mu - 1)^2 + 4(\beta - 3)^2 + 2(\mu - 1)(\beta - 3)\right)$$:
1. **Partial derivatives (Gradient):**
   $$\frac{\partial g}{\partial \mu} = -2(\mu - 1) - (\beta - 3), \qquad \frac{\partial g}{\partial \beta} = -4(\beta - 3) - (\mu - 1).$$
   At $$(\mu, \beta) = (0, 3)$$, $$\nabla g = (+2, +1)^T$$—pointing straight uphill toward the mode $$(1, 3)$$!
2. **Negative Hessian (Posterior Precision Matrix):**
   $$-\mathbf{H} = \begin{pmatrix} 2 & 1 \\ 1 & 4 \end{pmatrix} \implies \Sigma = (-\mathbf{H})^{-1} = \frac{1}{7}\begin{pmatrix} 4 & -1 \\ -1 & 2 \end{pmatrix}.$$
   The off-diagonal $$+1$$ in $$-\mathbf{H}$$ immediately tells you $$\mu$$ and $$\beta$$ are negatively correlated ($$\mathrm{Cov} = -1/7$$)!

### Explanation: Four Rules for Multivariable Calculus in Bayes

1. **Always check the sign of the Hessian at a mode:** A maximum of $$\log p$$ must have a *negative-definite* Hessian (so $$-\mathbf{H}$$ is positive-definite).
2. **Verify your analytical gradient with finite differences:** Checking $$\frac{g(\theta+\epsilon)-g(\theta-\epsilon)}{2\epsilon}$$ against your coded gradient catches 99% of chain-rule bugs in 5 seconds.
3. **Never forget the Jacobian when reparameterizing:** Sampling $$\log \sigma$$ without adding `+\log\sigma` to the log-posterior silently changes your prior!
4. **Centering predictors makes the Hessian nearly diagonal:** Smaller off-diagonal Hessian entries mean faster optimization and faster HMC mixing.

**Quick check.** For $$g(\mu, \beta)$$ above, verify that $$\nabla g = (0, 0)^T$$ at $$(\mu, \beta) = (1, 3)$$.

---

## Reference videos

- [The paradox of the derivative | Chapter 2, Essence of calculus](https://www.youtube.com/watch?v=9vKqVkMQHKk) — 3Blue1Brown, English. **watch first**. Watch the derivative as a local linear approximation, the rate-of-change idea in the first section of the lesson.
- [Partial derivatives, introduction](https://www.youtube.com/watch?v=AXqhWeUEtQU) — Khan Academy, English. Watch a partial derivative hold every variable but one fixed, supporting the multivariable section.
- [Multivariable chain rule](https://www.youtube.com/watch?v=NO3AqAaAE6o) — Khan Academy, English. Watch the multivariable chain rule, the last section of the lesson on composed functions of several inputs.
