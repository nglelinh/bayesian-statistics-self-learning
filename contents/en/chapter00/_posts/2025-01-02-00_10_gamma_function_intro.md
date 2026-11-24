---
layout: post
title: "Lesson 0.10b: Introduction to the Gamma Function"
chapter: '00'
order: 23
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

What is $$2.5!$$? You can’t multiply "2.5 integers in a row," yet in 1729 Leonhard Euler discovered a smooth, analytic curve—the **Gamma function $$\Gamma(z)$$**—that passes through every factorial $$(n-1)!$$ and fills in every real and half-integer value in between! Far from being a pure-math curiosity, $$\Gamma(z)$$ is the exact normalizing glue holding together the **Beta**, **Gamma**, **Chi-squared**, **Dirichlet**, and **Student-$$t$$** distributions across all of Bayesian statistics.

This lesson strips the mystery off $$\Gamma(z)$$ with its two core identities—$$\Gamma(z+1) = z\Gamma(z)$$ and $$\Gamma(1/2) = \sqrt{\pi}$$—and shows why Bayesian libraries always compute `lgamma` in log space.

---

## Background Knowledge Map: Where the Gamma Function Appears in Bayesian Models

Four properties turn $$\Gamma(z)$$ from an intimidating integral into an everyday algebraic tool:

1. **Continuous Factorial Extension:** For every positive integer $$n$$, $$\Gamma(n) = (n-1)!$$, and for all $$z > 0$$, the recurrence $$\Gamma(z+1) = z\,\Gamma(z)$$ lets you step any argument down by 1.
2. **Half-Integer Anchor $$\Gamma(1/2) = \sqrt{\pi}$$:** Connects $$\Gamma$$ directly to the Gaussian integral $$\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}$$, explaining why $$\sqrt{\pi}$$ appears inside the Student-$$t$$ and Chi-squared densities!
3. **The Beta Function Normalizer:** $$B(lpha, eta) = \int_0^1 p^{lpha-1}(1-p)^{eta-1}\,dp = rac{\Gamma(lpha)\Gamma(eta)}{\Gamma(lpha+eta)}$$ is the exact normalizing constant of $$\mathrm{Beta}(lpha,eta)$$—and powers the closed-form **Beta–Binomial marginal likelihood**!
4. **Log-Gamma (`gammaln` / `lgamma`) for Numerical Safety:** Because $$\Gamma(200) pprox 3.9	imes 10^{372}$$ overflows `float64` (max $$1.8	imes 10^{308}$$), statistical software computes $$\ln\Gamma(lpha) + \ln\Gamma(eta) - \ln\Gamma(lpha+eta)$$ directly in log space!

---

## Learning objectives

After this lesson, you will understand what the Gamma function is, why it is the natural extension of factorial to non-integer values, and why it appears throughout Bayesian statistics (Beta, Gamma, Dirichlet, Student-t, and more).

## 1) Motivation: From factorial to non-integers

For positive integers, factorial is defined as:

$$n! = 1 \cdot 2 \cdot 3 \cdots n$$

For example, $$5! = 120$$.

But what should $$\left(\frac{1}{2}\right)!$$ mean? The usual factorial definition does not apply. The Gamma function gives a consistent extension.

At an introductory level, this is a correct summary: **the Gamma function extends factorial to positive non-integers**. More generally, for every $$x>0$$, we can write:

$$x! = \Gamma(x+1)$$

## 2) Definition of the Gamma function

For $$z > 0$$, the Gamma function is:

$$\Gamma(z) = \int_0^{\infty} t^{z-1} e^{-t} \, dt$$

This integral is positive and converges for $$z > 0$$. In probability and Bayesian modeling, $$\Gamma(z)$$ often appears as a normalization constant.

## 3) Core relationship with factorial

The key identity is:

$$\Gamma(z+1) = z\,\Gamma(z)$$

Setting $$z=n$$ (a positive integer) gives:

$$\Gamma(n+1) = n!$$

For example, $$\Gamma(1)=1$$, $$\Gamma(2)=1!=1$$, $$\Gamma(3)=2!=2$$, and $$\Gamma(6)=5!=120$$.

So on integer arguments, Gamma exactly matches factorial.

## 4) Special value: $$\Gamma\!\left(\tfrac{1}{2}\right)=\sqrt{\pi}$$

A famous result is:

$$\Gamma\!\left(\frac{1}{2}\right)=\sqrt{\pi}$$

Then:

$$\Gamma\!\left(\frac{3}{2}\right)=\frac{1}{2}\Gamma\!\left(\frac{1}{2}\right)=\frac{\sqrt{\pi}}{2}$$

$$\Gamma\!\left(\frac{5}{2}\right)=\frac{3}{2}\Gamma\!\left(\frac{3}{2}\right)=\frac{3\sqrt{\pi}}{4}$$

This helps explain why $$\pi$$ appears in many continuous-distribution formulas.

## 5) Why Gamma matters in Bayesian statistics

### 5.1 Distribution normalization

Many densities are first written in an unnormalized form, then divided by a constant so the total integral is 1. That constant is often expressed with Gamma.

For example, the Gamma distribution (shape $$\alpha$$, rate $$\beta$$):

$$p(x\mid \alpha,\beta)=\frac{\beta^{\alpha}}{\Gamma(\alpha)}x^{\alpha-1}e^{-\beta x},\quad x>0$$

### 5.2 Beta distribution

The Beta normalization constant is:

$$B(a,b)=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}$$

So:

$$p(\theta\mid a,b)=\frac{1}{B(a,b)}\theta^{a-1}(1-\theta)^{b-1},\quad 0<\theta<1$$

### 5.3 Dirichlet and Student-t

Dirichlet is a multivariate generalization of Beta, and its normalization constant is also written with Gamma. Likewise, the Student-t distribution contains a Gamma ratio in its front coefficient to ensure the density is properly normalized.

In short: if you do Bayesian analysis long enough, you repeatedly use Gamma.

## 6) Practical computation intuition

In numerical work, we usually avoid direct $$\Gamma(z)$$ for large $$z$$ because of overflow. Instead, we use:

$$\log\Gamma(z)$$

Scientific libraries provide this directly (`gammaln` in SciPy), which is much more stable for optimization and MCMC.

Python example:

```python
from scipy.special import gamma, gammaln

print(gamma(6))      # 120.0
print(gamma(0.5))    # ~1.7724538509 = sqrt(pi)
print(gammaln(100))  # log(Gamma(100))
```

## 7) Quick recap

1. $$\Gamma(z)$$ extends factorial from integers to positive real numbers.
2. Recursion: $$\Gamma(z+1)=z\Gamma(z)$$.
3. For $$n\in\mathbb{N}$$: $$\Gamma(n+1)=n!$$.
4. Famous value: $$\Gamma\!\left(\tfrac{1}{2}\right)=\sqrt{\pi}$$.
5. In Bayesian statistics, Gamma frequently appears as a normalization constant.

---

### Worked Numerical Example: Computing $$\Gamma(5/2)$$ and the Exact Normalizer of $$\mathrm{Beta}(2, 3)$$ by Hand

**Part A — Stepping down a half-integer:**
Using $$\Gamma(z+1) = z\Gamma(z)$$ and $$\Gamma(1/2) = \sqrt{\pi} pprox 1.7725$$:
$$\Gamma\!\left(rac{5}{2}ight) = rac{3}{2}\,\Gamma\!\left(rac{3}{2}ight) = rac{3}{2}\cdotrac{1}{2}\,\Gamma\!\left(rac{1}{2}ight) = rac{3}{4}\sqrt{\pi} pprox \mathbf{1.3293}.$$

**Part B — Exact normalizing constant of $$\mathrm{Beta}(lpha=2,\; eta=3)$$:**
$$B(2, 3) = rac{\Gamma(2)\,\Gamma(3)}{\Gamma(2+3)} = rac{1!\cdot 2!}{4!} = rac{1 	imes 2}{24} = rac{1}{12}.$$
Therefore the exact PDF of $$\mathrm{Beta}(2, 3)$$ is $$f(p) = 12\,p(1-p)^2$$ on $$[0,1]$$! Verify by direct integration:
$$\int_0^1 12(p - 2p^2 + p^3)\,dp = 12\!\left(rac{1}{2} - rac{2}{3} + rac{1}{4}ight) = 12\cdotrac{1}{12} = \mathbf{1}$$ — exact!

### Deep-Dive Explanation: Four Practical Takeaways on the Gamma Function (Read Slowly)

1. **Remember the off-by-one shift:** $$\Gamma(n) = (n-1)!$$, so $$\Gamma(1) = 0! = 1$$ and $$\Gamma(5) = 4! = 24$$—never $$\Gamma(5) = 5!$$.
2. **You rarely need to integrate Beta/Gamma kernels by hand:** Whenever you see $$\int_0^1 p^{a-1}(1-p)^{b-1}\,dp$$, immediately recognize it as $$B(a,b) = rac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}$$.
3. **Always use `scipy.special.gammaln` (or `betaln`) in code:** Even for modest datasets ($$n = 200$$), calling `gamma(200)` returns `inf`, whereas `gammaln(200) ≈ 859.66` works effortlessly.
4. **Watch the Dirichlet generalization:** For $$K$$-category probabilities $$(p_1,\dots,p_K)$$, the Dirichlet normalizer is simply $$rac{\prod_{k=1}^K \Gamma(lpha_k)}{\Gamma(\sum_k lpha_k)}$$—the direct multi-category cousin of $$B(lpha,eta)$$.

**Quick check.** Using $$B(lpha,eta) = rac{\Gamma(lpha)\Gamma(eta)}{\Gamma(lpha+eta)}$$, compute the exact normalizing constant $$1/B(3, 3)$$ for the symmetric prior $$\mathrm{Beta}(3, 3)$$.

---

## Reference videos

- [Gamma Function - Explained](https://www.youtube.com/watch?v=UZuszwqW_Qo) — DataMListic, English. **watch first**. Watch for the gamma function as the extension of factorial beyond the positive integers, which is the definition this lesson starts from.
- [Introduction to the Gamma function & the Pi function (extending the factorial!)](https://www.youtube.com/watch?v=L4Trz6pFut4) — blackpenredpen, English. Watch the explicit link between factorial and the gamma integral, supporting the lesson's passage from n! to Γ(z).
- [What is the factorial of -½?](https://www.youtube.com/watch?v=dGnIJFzkLI4) — Stand-up Maths, English. Watch a concrete non-integer factorial, useful when the lesson explains why Beta, Gamma, and t densities need this function.

## Exercises

**Exercise 1.** Use recursion to compute $$\Gamma(4)$$ and $$\Gamma(5)$$, then compare with $$3!$$ and $$4!$$.

**Exercise 2.** Starting from $$\Gamma\!\left(\tfrac{1}{2}\right)=\sqrt{\pi}$$, derive $$\Gamma\!\left(\tfrac{3}{2}\right)$$ and $$\Gamma\!\left(\tfrac{5}{2}\right)$$.

**Exercise 3.** Rewrite the Beta($$a,b$$) normalization constant using Gamma and explain why this constant is needed for the density to integrate to 1.

**Exercise 4.** In Python, compute `gamma(10)` and `gammaln(10)`. Check whether `np.log(gamma(10))` is close to `gammaln(10)`.

## References

- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Kruschke, J. (2015). *Doing Bayesian Data Analysis* (2nd ed.). Academic Press.
- SciPy Special Functions: `gamma`, `gammaln`.
