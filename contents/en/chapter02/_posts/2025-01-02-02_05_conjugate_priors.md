---
layout: post
title: "Lesson 2.5: Conjugate Priors and the Algebra of Bayesian Updating"
chapter: '02'
order: 5
owner: Nguyen Le Linh
lang: en
categories:
- chapter02
lesson_type: required
---

## Learning objectives

After this lesson, you should understand conjugate priors not as a memorization trick, but as prior-likelihood pairs that make Bayesian updating especially clean. You should also know when conjugacy is extremely useful and when it is better to move on to more flexible computational methods.

> **Mini example.** If the prior for a pass rate is Beta$$(2,2)$$ and new data are 7 passes out of 10 students, the posterior becomes Beta$$(9,5)$$. We do not need a new family of distributions, only updated parameters.
>
> **Quick check.** What exactly makes a prior “conjugate” to a likelihood?

## Opening idea: why are some Bayesian models so easy to solve by hand?

Bayes' theorem is conceptually simple:

$$
P(\theta \mid D) \propto P(D \mid \theta)P(\theta).
$$

But exact computation is often hard because the posterior must be normalized. Some models are special: after multiplying prior and likelihood, the posterior still belongs to the **same distribution family** as the prior. These are the conjugate cases.

![An introduction to conjugate pairs]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_pairs_intro.png)

## 1. What is a conjugate prior?

A prior $$p(\theta)$$ is conjugate to a likelihood $$p(y \mid \theta)$$ if the posterior $$p(\theta \mid y)$$ stays in the same family as the prior.

Examples:

- Beta prior  $$\rightarrow$$ Beta posterior,
- Gamma prior  $$\rightarrow$$ Gamma posterior,
- Normal prior  $$\rightarrow$$ Normal posterior.

That means updating becomes a matter of adjusting a few parameters rather than inventing a whole new functional form.

## 2. Why does conjugacy happen?

Conjugacy appears when the prior and the likelihood have matching algebraic structure.

For example:

- a Binomial likelihood contributes powers of $$\theta$$ and $$1-\theta$$,
- a Beta prior is built from the same powers.

So multiplying them does not change the shape family. It only changes the exponents.

![Why conjugacy is convenient]({{ site.baseurl }}/img/chapter_img/chapter02/why_conjugacy_convenient.png)

## 3. Beta-Binomial

### 3.1. Real-world story

Suppose a teacher wants to infer the class pass rate $$\theta$$. Out of 40 students, 31 pass.

If:

$$
Y \mid \theta \sim \text{Binomial}(n,\theta)
$$

and:

$$
\theta \sim \text{Beta}(\alpha,\beta),
$$

then:

$$
\theta \mid y \sim \text{Beta}(\alpha+y,\beta+n-y).
$$

### 3.2. Interpretation

If the prior is Beta$$(2,2)$$ and the data are 31 passes out of 40, the posterior is Beta$$(33,11)$$.

The intuition is simple:

- the prior acts like a small amount of pseudo-data,
- the real data are added on top,
- and the posterior combines both.

![Beta-Binomial conjugacy]({{ site.baseurl }}/img/chapter_img/chapter02/beta_binomial_conjugacy_visual.png)

### 3.3. Typical applications

- conversion rates,
- pass rates,
- treatment success rates,
- email open rates,
- defect proportions.

## 4. Gamma-Poisson

### 4.1. Real-world story

Suppose a call center wants to infer the mean call rate $$\lambda$$ per hour.

If:

$$
Y_i \mid \lambda \sim \text{Poisson}(\lambda)
$$

and:

$$
\lambda \sim \text{Gamma}(\alpha,\beta),
$$

then under the shape-rate parameterization:

$$
\lambda \mid y_{1:n} \sim \text{Gamma}\left(\alpha + \sum_i y_i,\beta + n\right).
$$

### 4.2. Interpretation

The observed counts add to the shape parameter, and the number of observation periods adds to the rate parameter.

![Gamma-Poisson conjugacy]({{ site.baseurl }}/img/chapter_img/chapter02/gamma_poisson_conjugacy_detailed.png)

### 4.3. Typical applications

- calls per hour,
- failures per day,
- hospital arrivals per shift,
- orders per minute,
- absences per week.

## 5. Normal-Normal

### 5.1. Real-world story

Suppose you want to infer the mean height $$\mu$$ of a group of students, assuming the observation standard deviation $$\sigma$$ is known.

If:

$$
Y_i \mid \mu \sim \mathcal{N}(\mu,\sigma^2)
$$

and:

$$
\mu \sim \mathcal{N}(\mu_0,\tau_0^2),
$$

then the posterior for $$\mu$$ is also Normal.

### 5.2. Interpretation

The posterior mean becomes a weighted compromise between:

- the prior mean,
- and the sample mean.

The balance depends on prior strength, sample size, and observation noise.

![Normal-Normal conjugacy]({{ site.baseurl }}/img/chapter_img/chapter02/normal_normal_conjugacy_detailed.png)

## 6. Sequential updating

One of the nicest features of conjugate models is how naturally they support sequential learning.

You can:

- update with today's data,
- use the posterior as tomorrow's prior,
- and keep going without restarting from scratch.

![Sequential updating with conjugate priors]({{ site.baseurl }}/img/chapter_img/chapter02/sequential_updating_story.png)

This is useful for dashboards, quality monitoring, and streaming observations.

## 7. Why learn conjugacy if we later use MCMC?

Three reasons:

1. It builds strong intuition for how Bayesian updating works.
2. It gives exact answers that are useful for checking numerical methods.
3. It remains practical for many simple one-parameter models.

![Conjugacy versus broader computational methods]({{ site.baseurl }}/img/chapter_img/chapter02/conjugacy_vs_mcmc.png)

## 8. Limits of conjugacy

Conjugacy is about convenience, not truth. We should not force a conjugate prior if it is a poor description of prior knowledge.

Examples where conjugacy may be too restrictive:

- multimodal priors,
- hierarchical models,
- complex constraints,
- richer dependence structures.

![Limits of conjugate priors]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_prior_limitations.png)

In such cases, we turn to grid approximation or MCMC.

## 9. Quick guide to common conjugate pairs

![Table of common conjugate pairs]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_pairs_table.png)

Think in terms of data stories:

- probability of success  $$\rightarrow$$ Beta + Binomial,
- event rate  $$\rightarrow$$ Gamma + Poisson,
- unknown mean of continuous data  $$\rightarrow$$ Normal + Normal.

## 10. Common misunderstandings

### 10.1. “A conjugate prior is always the best prior”

No. It is only the most convenient one computationally.

### 10.2. “Memorizing formulas is enough”

No. Without the generative story, the formulas become easy to misuse.

### 10.3. “Conjugacy is obsolete because of MCMC”

No. It is still foundational for intuition and for simple exact solutions.

## Summary

**Conjugate priors are priors that keep the posterior in the same family after updating.** They make Bayesian inference easier to compute, easier to explain, and easier to update sequentially. The three basic pairs to remember are:

- Beta-Binomial,
- Gamma-Poisson,
- Normal-Normal.

But convenience should never replace good modeling judgment.

> **3 key takeaways.**
> 1. Conjugacy happens when the algebra of the prior and likelihood matches so that the posterior stays in the same family.
> 2. Conjugate pairs are extremely helpful for building intuition and computing simple exact updates.
> 3. A conjugate prior is convenient, but it should not be forced when it poorly represents real prior knowledge.

## Practice questions

1. Give one real-world example that fits Beta-Binomial.
2. Why is Gamma-Poisson so natural for count data over time?
3. In the Normal-Normal model, what makes the posterior mean stay closer to the prior mean or move closer to the sample mean?
4. When would you avoid a conjugate prior even though it is convenient?

## References

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 2.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 6-7.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 2-3.

---

*Next lesson: [2.6 Grid Approximation - Discrete Approximation to the Posterior](/en/chapter02/grid-approximation/)*
