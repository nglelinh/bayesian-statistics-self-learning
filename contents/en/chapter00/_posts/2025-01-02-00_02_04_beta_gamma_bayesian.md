---
layout: post
title: "Lesson 0.5: Beta and Gamma - Distributions for Probabilities and Positive Parameters"
chapter: '00'
order: 5
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

## Learning objectives

After this lesson, you will understand that the Beta arises from the need to describe quantities lying in the interval $$[0,1]$$, be able to read the meaning of the parameters $$\alpha,\beta$$, and grasp the role of the normalizing constant in forming a valid distribution.

## 1) Starting from a practical problem: describing an unknown proportion

In practice, we often meet quantities in the form of proportions such as:

- the proportion of customers who will click,
- the proportion of defective products,
- the proportion of students who complete a course.

These quantities have one thing in common: they always lie between 0 and 1.

We need a distribution flexible enough to describe many different shapes on that interval: it can lean left, lean right, or concentrate around a central region. That is exactly the role of the Beta distribution.

## 2) The Beta for probabilities

$$
p\sim\text{Beta}(\alpha,\beta), \quad 0<p<1.
$$

Quick interpretation:

$$\alpha-1$$ can be understood as the part leaning toward "success", while $$\beta-1$$ leans toward "failure".

Mean:

$$
\mathbb{E}[p]=\frac{\alpha}{\alpha+\beta}.
$$

When $$\alpha+\beta$$ is large, the distribution is more concentrated; when small, the distribution is more spread out.

The normalizing constant of the Beta is:

$$
B(\alpha,\beta)=\int_0^1 p^{\alpha-1}(1-p)^{\beta-1}\,dp
=\frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}.
$$

Therefore the full density must be written:

$$
f(p)=\frac{1}{B(\alpha,\beta)}p^{\alpha-1}(1-p)^{\beta-1},\quad 0<p<1.
$$

## 3) The Gamma function and the bridge to the Beta function

To understand the normalizing constant of the Beta better, we need the Gamma function:

$$
\Gamma(z)=\int_0^{\infty} t^{z-1}e^{-t}\,dt,\quad z>0.
$$

The Gamma function is an extension of the factorial to positive reals, with the property:

$$
\Gamma(z+1)=z\,\Gamma(z),\qquad \Gamma(n+1)=n!\;(n\in\mathbb{N}).
$$

Thanks to that, the normalizing constant of the Beta can be written compactly:

$$
B(\alpha,\beta)=\frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}.
$$

Practical meaning: we turn a normalizing integral that is hard to compute directly into a ratio of Gammas, for more stable computation and a clearer structure.

## 4) What problem does the Beta solve?

The Beta gives us a systematic way to describe the question: "which region of the interval $$[0,1]$$ does the true proportion tend to lie in, and how strongly or weakly concentrated is it?"

In short:

- $$\alpha$$ and $$\beta$$ control the shape,
- $$\frac{\alpha}{\alpha+\beta}$$ gives the central location,
- $$\alpha+\beta$$ gives the degree of concentration.

Thanks to this, the Beta gives not just a single proportion value, but also the uncertainty around that proportion.

## 5) Example of reading a Beta shape

Suppose $$\alpha=2,\beta=5$$; then the density leans toward the region near 0; if changed to $$\alpha=8,\beta=3$$ then the density leans toward the region near 1.

In other words, the pair $$\alpha,\beta$$ controls both the location and the concentration of the distribution on the interval $$[0,1]$$.

![Comparing Beta shapes with different parameter sets]({{ site.baseurl }}/img/chapter_img/chapter00/beta_binomial_update_vi.png)

*How to read the figure: This figure illustrates how changing the parameters shifts and stretches the shape of the Beta distribution on the interval $$[0,1]$$.*

## 6) The Gamma for positive parameters

A commonly used shape-rate parameterization:

$$
\lambda\sim\text{Gamma}(\alpha,\beta), \quad
f(\lambda)=\frac{\beta^\alpha}{\Gamma(\alpha)}\lambda^{\alpha-1}e^{-\beta\lambda},\; \lambda>0.
$$

Expectation:

$$
\mathbb{E}[\lambda]=\frac{\alpha}{\beta}.
$$

Here $$\frac{\beta^\alpha}{\Gamma(\alpha)}$$ is the normalizing constant so that:

$$
\int_0^{\infty} f(\lambda)\,d\lambda=1.
$$

If this ratio is dropped, we only have the "shape" $$\lambda^{\alpha-1}e^{-\beta\lambda}$$, not yet a valid distribution.

## 7) An intuitive example with the Gamma

With shape-rate:

- if we keep $$\alpha$$ and increase $$\beta$$, the distribution shifts closer to 0,
- if we increase $$\alpha$$, the distribution has a clearer peak and is less skewed.

This is useful when describing positive quantities such as waiting times, event intensity, or variables with a right tail.

## 8) Unnormalized and normalized forms

In practice, we often meet the "kernel" form first, for example:

$$
g(p)=p^{\alpha-1}(1-p)^{\beta-1}.
$$

This is not yet a valid density because the integral over $$[0,1]$$ is not necessarily 1. To become a density, we need to divide by the normalizing constant:

$$
f(p)=\frac{1}{B(\alpha,\beta)}g(p).
$$

A similar idea applies to the Gamma: the exponential and power parts give the shape, while the front coefficient ensures the total probability equals 1.

## 9) Practical tip

When using the Gamma, always state clearly whether the parameterization is shape-rate or shape-scale. When reading documentation, check the notation carefully to avoid confusing the rate $$\beta$$ with the scale $$\theta=1/\beta$$.

## 10) Extending from the factorial to the Gamma

For positive integers, we have the factorial:

$$
n!=1\cdot 2\cdot 3\cdots n.
$$

The Gamma function extends this idea to positive reals. So we can quickly understand:

$$
x!=\Gamma(x+1),\quad x>0.
$$

Example:

$$
\Gamma(1)=1,\quad \Gamma(2)=1!,\quad \Gamma(3)=2!,\quad \Gamma(6)=5!.
$$

## 11) Common special values

A famous value:

$$
\Gamma\!\left(\frac{1}{2}\right)=\sqrt{\pi}.
$$

From the recurrence formula we deduce:

$$
\Gamma\!\left(\frac{3}{2}\right)=\frac{\sqrt{\pi}}{2},
\qquad
\Gamma\!\left(\frac{5}{2}\right)=\frac{3\sqrt{\pi}}{4}.
$$

This is why $$\pi$$ appears in many continuous distribution formulas.

## 12) A short example with the Beta function

With $$a,b>0$$:

$$
B(a,b)=\int_0^1 t^{a-1}(1-t)^{b-1}\,dt
=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}.
$$

Example:

$$
B(2,3)=\frac{\Gamma(2)\Gamma(3)}{\Gamma(5)}=\frac{1!\,2!}{4!}=\frac{1}{12}.
$$

This part shows clearly the role of the Gamma as a tool for computing the normalizing constant of the Beta.

## 13) A numerical example for the Beta shape (7/10)

Suppose we consider the expression in $$\theta$$ on the interval $$[0,1]$$:

$$
g(\theta)=\theta^8(1-\theta)^4.
$$

This is only the unnormalized form. The normalized form is:

$$
f(\theta)=\frac{1}{B(9,5)}\theta^8(1-\theta)^4.
$$

![Beta-Binomial update 7 over 10]({{ site.baseurl }}/img/chapter_img/chapter00/beta_binomial_update_7of10.png)

*How to read the figure: The curve shows that the unnormalized and normalized forms have the same relative shape; the factor $$1/B(9,5)$$ only turns the curve into a valid density (area equal to 1).* 

## 14) Hints for numerically stable computation

When the parameters are large, use log-functions instead of computing directly:

- `gammaln(z)` instead of `log(gamma(z))`
- `betaln(a,b)` instead of `log(beta(a,b))`

In SciPy, these functions are in `scipy.special` and are more stable in computation.

Python example:

```python
from scipy.special import gamma, gammaln, beta, betaln

print(gamma(6))      # 120.0
print(gamma(0.5))    # ~1.7724538509 = sqrt(pi)
print(gammaln(100))  # log(Gamma(100))
print(beta(2, 3))    # 1/12 = 0.08333...
print(betaln(2, 3))  # log(Beta(2,3))
```

## 15) Quick summary

1. The Beta is a flexible distribution for quantities in $$[0,1]$$.
2. The Gamma is a distribution for positive quantities.
3. The Gamma function extends the factorial: $$\Gamma(n+1)=n!$$.
4. The Beta function is directly related to the Gamma via the ratio $$\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}$$.
5. The normalizing constant turns an expression of the "right shape" into a valid density.

## Reference videos

- [The Beta distribution in 12 minutes!](https://www.youtube.com/watch?v=juF3r12nM5A) — Luis Serrano Academy, English. **watch first**. Watch to read α and β as the numbers of successes and failures known beforehand, exactly the Beta on the interval from 0 to 1 part.
- [The Gamma Distribution](https://www.youtube.com/watch?v=9IIcHAJlcWc) — Steve Brunton, English. Watch the Gamma shape for positive quantities, supporting the half of the lesson about rate parameters and waiting times.
- [How to Estimate Rates with a Gamma-Poisson Bayesian Model | Conjugate Priors](https://www.youtube.com/watch?v=m8roQUqmybg) — Drawing Distributions, English. Watch the Gamma–Poisson pair when estimating an event rate, linking the distributions in the lesson to Bayesian updating in the closing connection.

## Exercises

**Exercise 1.** Use the recurrence formula to compute $$\Gamma(4)$$ and $$\Gamma(5)$$, then compare with $$3!$$ and $$4!$$.

**Exercise 2.** From $$\Gamma\!\left(\tfrac{1}{2}\right)=\sqrt{\pi}$$, deduce $$\Gamma\!\left(\tfrac{3}{2}\right)$$ and $$\Gamma\!\left(\tfrac{5}{2}\right)$$.

**Exercise 3.** Rewrite the normalizing constant of Beta($$a,b$$) using the Gamma and explain why this constant is needed for the density to integrate to 1.

**Exercise 4.** In Python, compute `gamma(10)` and `gammaln(10)`. Check whether `np.log(gamma(10))` is close to `gammaln(10)`.

**Exercise 5.** Quickly prove $$B(a,1)=\frac{1}{a}$$ from the integral definition, then compare with the Gamma ratio formula.

## References

- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Kruschke, J. (2015). *Doing Bayesian Data Analysis* (2nd ed.). Academic Press.
- SciPy Special Functions: `gamma`, `gammaln`.

## Summary

Beta and Gamma are two foundational families of distributions in statistics: the Beta for variables in $$[0,1]$$ and the Gamma for positive variables. The most important point of the lesson is knowing how to choose the right domain and understanding the role of the normalizing constant in turning a "shape" into a valid distribution.

---

*Next lesson: [0.6 Descriptive Statistics]({{ site.baseurl }}/contents/en/chapter00/00_03_descriptive_statistics/)*
