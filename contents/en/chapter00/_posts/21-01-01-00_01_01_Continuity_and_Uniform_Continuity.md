---
layout: post
title: 00-01-01 Continuity and Uniform Continuity
chapter: '00'
order: 24
owner: GitHub Copilot
lang: en
categories:
- chapter00
lesson_type: required
---

This lesson introduces the fundamental concepts of continuity and uniform continuity, which are essential for understanding the behavior of functions in optimization.

---

When you approximate a continuous Bayesian posterior integral $$\int_0^1 p(	heta\mid y)\,d	heta$$ on a finite grid of step size $$\Delta	heta = 0.01$$, what mathematical guarantee ensures that making the grid finer actually converges to the exact integral everywhere at once? The answer is **uniform continuity**—the stronger cousin of ordinary continuity where a single step size $$\delta$$ controls the function’s wobble simultaneously across the *entire* domain!

This mathematical reference sharpens the distinction between **pointwise continuity** and **uniform continuity**, highlights the **Heine–Cantor theorem** (every continuous function on a closed bounded interval $$[a,b]$$ is automatically uniformly continuous!), and shows why steep singularities on unbounded domains break naive grid approximations.

---

## Background Knowledge Map: Continuity, Compactness, and Numerical Integration

Four analysis concepts connect real analysis directly to Bayesian grid approximation and density theory:

1. **Pointwise Continuity:** At a *fixed* point $$x_0$$, you can keep $$\lvert f(x)-f(x_0)vert < arepsilon$$ by choosing $$\delta(arepsilon, x_0)$$—allowing $$\delta$$ to shrink arbitrarily tiny in steeper regions of the graph.
2. **Uniform Continuity:** One single $$\delta(arepsilon)$$ works for **every** pair $$x, y$$ across the entire domain simultaneously—guaranteeing controlled variation everywhere.
3. **Heine–Cantor Theorem:** Any continuous function on a compact (closed and bounded) interval $$[a,b]$$ is automatically uniformly continuous—explaining why smooth posteriors on $$[0,1]$$ (like $$\mathrm{Beta}(lpha,eta)$$ with $$lpha,eta \ge 1$$) integrate cleanly on uniform grids!
4. **Failure Modes on Open/Unbounded Domains:** Functions like $$1/x$$ on $$(0,1]$$ (blowing up near 0, like $$\mathrm{Beta}(0.5, 0.5)$$!) or $$x^2$$ on $$(0,\infty)$$ are continuous everywhere yet **not** uniformly continuous—requiring adaptive quadrature or log-transformations.

---

## Continuity and Uniform Continuity

**Continuity** and **Uniform Continuity** are fundamental concepts that describe the behavior of functions, particularly concerning their "smoothness" or "predictability." While closely related, they capture distinct properties, with uniform continuity being a stronger condition than mere continuity.

### Definition of Continuity

A function $$f: A \to \mathbb{R}$$ is said to be **continuous at a point** $$c \in A$$ if, for every positive real number $$\varepsilon > 0$$, there exists a positive real number $$\delta > 0$$ such that for all $$x \in A$$, if 

$$\lvert x - c \rvert < \delta$$

then 

$$\lvert f(x) - f(c) \rvert < \varepsilon$$ 

Intuitively, it means that for any desired level of precision $$\varepsilon$$ in the output $$f(x)$$, we can find a sufficiently small interval around $$c$$ (of width $$2\delta$$) such that all $$x$$ values within this interval map to $$f(x)$$ values within an $$\varepsilon$$-interval around $$f(c)$$. The crucial aspect here is that the choice of $$\delta$$ generally depends not only on $$\varepsilon$$ but also on the specific point $$c$$.

A function is **continuous on a set** $$A$$ if it is continuous at every point $$c \in A$$.

**Examples of continuous functions** include all polynomials (e.g., $$f(x) = x^2 + 3x - 1$$), trigonometric functions like $$\sin(x)$$ and $$\cos(x)$$, and exponential functions $$e^x$$ on their respective domains. 

### Definition of Uniform Continuity

**Uniform Continuity**, on the other hand, imposes a more stringent condition. A function $$f: A \to \mathbb{R}$$ is said to be **uniformly continuous on a set** $$A$$ if, for every positive real number $$\varepsilon > 0$$, there exists a positive real number $$\delta > 0$$ such that for all $$x, y \in A$$, if 

$$\lvert x - y \rvert < \delta$$

then 

$$\lvert f(x) - f(y) \rvert < \varepsilon$$

The **key distinction** from point-wise continuity lies in the order of quantifiers: for **uniform** continuity, the $$\delta$$ depends *only* on $$\varepsilon$$ and is independent of the specific points $$x$$ and $$y$$ in the domain.

### Definition of Lipschitz Continuity

**Lipschitz Continuity** provides an even more specific and quantitative notion of continuity. A function $$f: A \to \mathbb{R}$$ is said to be **Lipschitz continuous** (or **L-Lipschitz**) on a set $$A$$ if there exists a constant $$L \geq 0$$ such that for all $$x, y \in A$$:

$$\lvert f(x) - f(y) \rvert \leq L \lvert x - y \rvert$$

The smallest such constant $$L$$ is called the **Lipschitz constant** or **Lipschitz modulus** of $$f$$.

**Key Properties of Lipschitz Continuity:**

1. **Bounded Rate of Change**: The Lipschitz condition ensures that the function cannot change faster than a linear rate determined by $$L$$.

2. **Uniform Continuity**: Every Lipschitz continuous function is uniformly continuous (choose $$\delta = \varepsilon/L$$ for $$L > 0$$).

3. **Almost Everywhere Differentiability**: Lipschitz continuous functions are differentiable almost everywhere, and where the derivative exists, $$\lvert f'(x) \rvert \leq L$$.

**Examples:**
- $$f(x) = \lvert x \rvert$$ is 1-Lipschitz on $$\mathbb{R}$$
- $$f(x) = \sin(x)$$ is 1-Lipschitz on $$\mathbb{R}$$ (since $$\lvert \cos(x) \rvert \leq 1$$)
- $$f(x) = x^2$$ is not Lipschitz on $$\mathbb{R}$$ but is Lipschitz on any bounded interval

### Key Differences and Hierarchy

The three types of continuity form a hierarchy of increasingly strong conditions:

**Continuity ⊆ Uniform Continuity ⊆ Lipschitz Continuity**

1. **Point-wise vs Global**: 
   - **Continuity**: Local property (checked at each point)
   - **Uniform Continuity**: Global property of the entire function
   - **Lipschitz Continuity**: Global property with quantitative bounds

2. **Choice of $$\delta$$**: 
   - **Continuity**: $$\delta$$ can depend on both $$\varepsilon$$ and the specific point $$c$$
   - **Uniform Continuity**: $$\delta$$ depends only on $$\varepsilon$$, working for all points simultaneously
   - **Lipschitz Continuity**: $$\delta = \varepsilon/L$$ provides explicit relationship

3. **Rate of Change Control**:
   - **Continuity**: No control over rate of change
   - **Uniform Continuity**: Ensures bounded variation over small intervals
   - **Lipschitz Continuity**: Provides explicit linear bound on rate of change

4. **Strength Relationships**: 
   - Every Lipschitz continuous function is uniformly continuous
   - Every uniformly continuous function is continuous
   - The converses are not generally true

### Detailed Examples and Comparisons

**Example 1: $$f(x) = x^2$$**
- **On $$\mathbb{R}$$**: Continuous but not uniformly continuous (rate of change $$\lvert f'(x) \rvert = 2\lvert x \rvert$$ is unbounded)
- **On $$[0,1]$$**: Continuous, uniformly continuous, and Lipschitz with $$L = 2$$

**Example 2: $$f(x) = \sin(x)$$**
- **On $$\mathbb{R}$$**: Continuous, uniformly continuous, and 1-Lipschitz (since $$\lvert \cos(x) \rvert \leq 1$$)

**Example 3: $$f(x) = \lvert x \rvert$$**
- **On $$\mathbb{R}$$**: Continuous, uniformly continuous, and 1-Lipschitz
- **Note**: Not differentiable at $$x = 0$$, but still Lipschitz

**Example 4: $$f(x) = \sqrt{x}$$**
- **On $$[0,1]$$**: Continuous and uniformly continuous, but not Lipschitz (derivative unbounded near $$x = 0$$)
- **On $$[a,1]$$ for $$a > 0$$**: Lipschitz with $$L = 1/(2\sqrt{a})$$

---

### Worked Numerical Example: Proving $$f(x) = x^2$$ Is Continuous Yet NOT Uniformly Continuous on $$[0, \infty)$$

Test whether a single step size $$\delta$$ can keep $$\lvert f(y) - f(x)vert < 1$$ everywhere on $$[0, \infty)$$:
Pick the sequence of pairs $$x_n = n$$ and $$y_n = n + rac{1}{n}$$ for $$n = 1, 10, 100, \dots$$:

| $$n$$ | $$x_n$$ | $$y_n = n + 1/n$$ | Input Gap $$\lvert y_n - x_nvert$$ | Output Jump $$\lvert y_n^2 - x_n^2vert = 2 + 1/n^2$$ |
| :--- | :--- | :--- | :--- | :--- |
| $$1$$ | $$1$$ | $$2.00$$ | $$1.00$$ | $$3.00$$ |
| $$10$$ | $$10$$ | $$10.10$$ | $$0.10$$ | $$2.01$$ |
| $$100$$ | $$100$$ | $$100.01$$ | $$0.01$$ | $$2.0001$$ |

Even as the input gap $$1/n 	o 0$$ becomes smaller than *any* proposed $$\delta > 0$$, the output jump stays strictly above **$$2$$**! Yet restrict $$f(x) = x^2$$ to the compact interval $$[0, 10]$$, and $$\lvert y^2 - x^2vert = \lvert y+xvert\lvert y-xvert \le 20\lvert y-xvert$$—so $$\delta = arepsilon / 20$$ works uniformly everywhere!

### Deep-Dive Explanation: Four Takeaways Connecting Continuity to Bayesian Computing (Read Slowly)

1. **Bounded slope implies Lipschitz $$\implies$$ uniform continuity:** Whenever $$\lvert f'(x)vert \le M$$ on an interval, $$\lvert f(y)-f(x)vert \le M\lvert y-xvert$$ gives an instant, explicit uniform step size $$\delta = arepsilon/M$$.
2. **Watch boundary singularities in Beta/Gamma densities:** $$\mathrm{Beta}(0.5, 0.5)$$ shoots to $$\infty$$ at $$p = 0$$ and $$p = 1$$—evaluating it on a naive grid starting at `p = 0.0` produces `inf`!
3. **Log-posterior smoothness matters for HMC/NUTS:** Hamiltonian Monte Carlo uses fixed leapfrog step sizes $$\epsilon$$; when log-posterior curvature varies wildly (failing uniform Lipschitz gradients, like Neal’s Funnel!), HMC produces **divergences** until you reparameterize.
4. **Compact domains are friendly; infinite tails need care:** Always verify tail decay before truncating a numerical grid on $$(-\infty, \infty)$$.

**Quick check.** Is $$f(x) = rac{1}{x}$$ uniformly continuous on the closed interval $$[1, 10]$$? What about on the open interval $$(0, 1]$$?

---

## Reference videos

- [Continuity at a point | Limits and continuity | AP Calculus AB | Khan Academy](https://www.youtube.com/watch?v=3KMqU5j7irw) — Khan Academy, English. **watch first**. Watch continuity at a point through nearby inputs giving nearby outputs, the local idea this lesson starts from.
- [Uniform Continuity Explained | Real Analysis](https://www.youtube.com/watch?v=MmxtJwr3Kws) — Wrath of Math, English. Watch uniform continuity as a single modulus of continuity for the whole domain, the distinction the lesson exists to draw.
