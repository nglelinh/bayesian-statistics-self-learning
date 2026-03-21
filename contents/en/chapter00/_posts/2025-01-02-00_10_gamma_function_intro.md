---
layout: post
title: "Lesson 0.10: Introduction to the Gamma Function"
chapter: '00'
order: 10
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
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

Examples:

- $$\Gamma(1)=1$$
- $$\Gamma(2)=1!=1$$
- $$\Gamma(3)=2!=2$$
- $$\Gamma(6)=5!=120$$

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

- Dirichlet is a multivariate generalization of Beta, with Gamma in its normalization constant.
- Student-t also contains a Gamma ratio in its front coefficient.

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

## Exercises

**Exercise 1.** Use recursion to compute $$\Gamma(4)$$ and $$\Gamma(5)$$, then compare with $$3!$$ and $$4!$$.

**Exercise 2.** Starting from $$\Gamma\!\left(\tfrac{1}{2}\right)=\sqrt{\pi}$$, derive $$\Gamma\!\left(\tfrac{3}{2}\right)$$ and $$\Gamma\!\left(\tfrac{5}{2}\right)$$.

**Exercise 3.** Rewrite the Beta($$a,b$$) normalization constant using Gamma and explain why this constant is needed for the density to integrate to 1.

**Exercise 4.** In Python, compute `gamma(10)` and `gammaln(10)`. Check whether `np.log(gamma(10))` is close to `gammaln(10)`.

## References

- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Kruschke, J. (2015). *Doing Bayesian Data Analysis* (2nd ed.). Academic Press.
- SciPy Special Functions: `gamma`, `gammaln`.
