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

## 0. A 30-second map before the formulas

If conjugacy feels abstract at first reading, the most useful move is not to memorize formulas immediately, but to keep a compact chain of questions in mind: what the unknown parameter actually is, what form the data take, which likelihood matches that data story, and whether there is a prior with a matching structure such that the posterior remains in the same family after updating.

Once you think in those terms, the standard conjugate pairs become much easier to organize. When the data story is “count the number of successes in $$n$$ trials,” the natural likelihood is Binomial and the natural prior for the success probability is Beta; when the data story is “wait until the first success occurs,” the likelihood becomes Geometric while the prior can still be Beta; when the observations are event counts over time, Poisson is often the right likelihood and Gamma becomes the natural conjugate prior for the rate; and when the goal is to infer the mean of continuous data fluctuating around a central value, the relevant pair is Normal-Normal. You do not need to memorize every pair at once, because it is usually enough at the beginning to recognize whether the problem is about a probability, a waiting-time process, a count rate, or a continuous mean.

## 1. What is a conjugate prior?

A prior $$p(\theta)$$ is conjugate to a likelihood $$p(y \mid \theta)$$ if the posterior $$p(\theta \mid y)$$ stays in the same family as the prior.

Examples:

Beta prior  $$\rightarrow$$ Beta posterior, Gamma prior  $$\rightarrow$$ Gamma posterior, and Normal prior  $$\rightarrow$$ Normal posterior.

The practical importance of this fact is that Bayesian updating becomes a matter of revising a few parameters inside a familiar family rather than inventing a completely new functional form after every observation, which is why conjugate models are so valuable pedagogically and computationally.

## 2. Why does conjugacy happen?

Conjugacy appears when the prior and the likelihood have matching algebraic structure, meaning that once both are written as functions of the parameter, they are built from the same kinds of algebraic pieces. For example, a Binomial likelihood contributes powers of $$\theta$$ and $$1-\theta$$, while a Beta prior is built from exactly those same components; as a result, multiplying them does not change the family of shapes, but only changes the exponents, which is precisely why the posterior remains Beta.

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

To see the algebra directly, keep only the parts that depend on $$\theta$$:

$$
p(\theta)\propto \theta^{\alpha-1}(1-\theta)^{\beta-1}
$$

and:

$$
p(y\mid \theta)\propto \theta^y(1-\theta)^{n-y}.
$$

Therefore:

$$
p(\theta\mid y)\propto p(y\mid \theta)p(\theta)
\propto \theta^{\alpha+y-1}(1-\theta)^{\beta+n-y-1},
$$

so:

$$
\theta\mid y\sim \text{Beta}(\alpha+y,\beta+n-y).
$$

If the data are written as Bernoulli observations $$y_1,\dots,y_n$$ and $$s=\sum_{i=1}^n y_i$$, then the same update becomes:

$$
\theta\mid y_{1:n}\sim \text{Beta}(\alpha+s,\beta+n-s).
$$

The posterior mean is:

$$
E[\theta\mid y]=\frac{\alpha+y}{\alpha+\beta+n}.
$$

If you want a one-line memory rule, read the update this way: the posterior success count equals the prior success count plus the observed successes, and the posterior failure count equals the prior failure count plus the observed failures.

### 3.2. Interpretation

If the prior is Beta$$(2,2)$$ and the data are 31 passes out of 40, the posterior is Beta$$(33,11)$$.

The intuition is simple but important: the prior acts like a small amount of pseudo-data, the real observations are added on top of it, and the posterior is the combined result of both sources of information.

![Beta-Binomial conjugacy]({{ site.baseurl }}/img/chapter_img/chapter02/beta_binomial_conjugacy_visual.png)

### 3.3. Typical applications

Beta-Binomial is natural for settings such as conversion rates, pass rates, treatment success rates, email open rates, and defect proportions, because all of these contexts reduce to the same underlying data story: a count of successes out of a known number of trials, with an unknown success probability.

## 4. Beta-Geometric

### 4.1. Real-world story

Suppose a student keeps taking an exam until passing. We want to infer the pass probability $$\theta$$ on each attempt. If the student passes on the third attempt, the data should not be read as “1 success in 3 trials” in the Binomial sense; rather, the meaningful story is that the first two attempts were failures and the third attempt was the first success, which is exactly the kind of ordered waiting-time structure captured by a Geometric likelihood:

$$
Y \mid \theta \sim \text{Geometric}(\theta),
$$

with:

$$
P(Y=y \mid \theta) = \theta(1-\theta)^{y-1}.
$$

If the prior is still:

$$
\theta \sim \text{Beta}(\alpha,\beta),
$$

then the posterior is:

$$
\theta \mid y \sim \text{Beta}(\alpha+1,\beta+y-1).
$$

For one waiting-time observation $$y$$, the likelihood can be written as:

$$
p(y\mid \theta)=\theta(1-\theta)^{y-1}\propto \theta^1(1-\theta)^{y-1}.
$$

The Beta prior contributes:

$$
p(\theta)\propto \theta^{\alpha-1}(1-\theta)^{\beta-1}.
$$

Multiplying them gives:

$$
p(\theta\mid y)\propto \theta^{\alpha}(1-\theta)^{\beta+y-2},
$$

so:

$$
\theta\mid y\sim \text{Beta}(\alpha+1,\beta+y-1).
$$

If we have $$m$$ independent waiting times $$y_1,\dots,y_m$$, then:

$$
p(y_{1:m}\mid \theta)=\prod_{i=1}^m \theta(1-\theta)^{y_i-1}
=\theta^m(1-\theta)^{\sum_{i=1}^m y_i-m},
$$

which leads to:

$$
\theta\mid y_{1:m}\sim \text{Beta}\left(\alpha+m,\beta+\sum_{i=1}^m y_i-m\right).
$$

The corresponding posterior mean is:

$$
E[\theta\mid y_{1:m}]=\frac{\alpha+m}{\alpha+\beta+\sum_{i=1}^m y_i}.
$$

### 4.2. Interpretation

The logic is that the observation contributes one realized success together with $$y-1$$ realized failures, so the Beta prior still works because the likelihood is still built from powers of $$\theta$$ and $$1-\theta$$.

### 4.3. Do not confuse it with Beta-Binomial

This distinction matters because **Binomial** asks how many successes occurred in a fixed number of trials, whereas **Geometric** asks on which trial the first success occurred. The data stories are therefore different at a structural level, even though both models keep a Beta prior in the same family after updating.

## 5. Gamma-Poisson

### 5.1. Real-world story

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

Under the shape-rate parameterization, the prior kernel is:

$$
p(\lambda)\propto \lambda^{\alpha-1}e^{-\beta\lambda}.
$$

For $$n$$ Poisson observations, the likelihood kernel is:

$$
p(y_{1:n}\mid \lambda)=\prod_{i=1}^n \frac{e^{-\lambda}\lambda^{y_i}}{y_i!}
\propto \lambda^{\sum_{i=1}^n y_i}e^{-n\lambda}.
$$

Therefore:

$$
p(\lambda\mid y_{1:n})\propto p(y_{1:n}\mid \lambda)p(\lambda)
\propto \lambda^{\alpha+\sum_i y_i-1}e^{-(\beta+n)\lambda},
$$

which is why:

$$
\lambda\mid y_{1:n}\sim \text{Gamma}\left(\alpha+\sum_i y_i,\beta+n\right).
$$

The posterior mean is:

$$
E[\lambda\mid y]=\frac{\alpha+\sum_i y_i}{\beta+n}.
$$

If each observation has exposure $$t_i$$ and $$Y_i\mid \lambda\sim \text{Poisson}(t_i\lambda)$$, the same logic gives:

$$
\lambda\mid y_{1:n}\sim \text{Gamma}\left(\alpha+\sum_i y_i,\beta+\sum_i t_i\right).
$$

### 5.2. Interpretation

The observed counts add to the shape parameter, while the number of observation periods adds to the rate parameter, so the update simultaneously reflects how much activity was seen and how long the process was observed.

![Gamma prior and posterior after count data are observed]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_gamma_poisson_prior_posterior.png)

![A compact formula summary for the Gamma-Poisson update]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_gamma_poisson_formula_summary.png)

![Posterior predictive reasoning in the Gamma-Poisson model]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_gamma_poisson_posterior_predictive.png)

![Sequential updating in the Gamma-Poisson model]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_gamma_poisson_sequential_updates.png)

### 5.3. Typical applications

Typical applications include calls per hour, failures per day, hospital arrivals per shift, orders per minute, and absences per week, because these are all examples of event counts attached to some unit of time or exposure.

### 5.4. Quick memory rule

Read the update as bookkeeping: the posterior shape equals the prior shape plus the total number of observed events, while the posterior rate equals the prior rate plus the number of observed time periods.

## 6. Normal-Normal

### 6.1. Real-world story

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

Writing everything as a function of $$\mu$$, the likelihood kernel for $$n$$ observations is:

$$
p(y_{1:n}\mid \mu)\propto \exp\left(-\frac{1}{2\sigma^2}\sum_{i=1}^n (y_i-\mu)^2\right)
\propto \exp\left(-\frac{n}{2\sigma^2}(\mu-\bar y)^2\right),
$$

where:

$$
\bar y=\frac{1}{n}\sum_{i=1}^n y_i.
$$

The Normal prior contributes:

$$
p(\mu)\propto \exp\left(-\frac{(\mu-\mu_0)^2}{2\tau_0^2}\right).
$$

After multiplying the prior and likelihood and completing the square, we get:

$$
\mu\mid y_{1:n}\sim \mathcal{N}(\mu_n,\tau_n^2),
$$

with:

$$
\tau_n^2=\left(\frac{1}{\tau_0^2}+\frac{n}{\sigma^2}\right)^{-1}
$$

and:

$$
\mu_n=\tau_n^2\left(\frac{\mu_0}{\tau_0^2}+\frac{n\bar y}{\sigma^2}\right)
=\frac{\mu_0/\tau_0^2+n\bar y/\sigma^2}{1/\tau_0^2+n/\sigma^2}.
$$

Equivalently:

$$
E[\mu\mid y]=\mu_n,\qquad \mathrm{Var}(\mu\mid y)=\tau_n^2.
$$

### 6.2. Interpretation

The posterior mean becomes a weighted compromise between the prior mean and the sample mean, and the balance between the two depends on the strength of the prior, the size of the sample, and the amount of observation noise.

![Normal prior and posterior after combining with continuous data]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_normal_normal_prior_posterior.png)

![A compact formula summary for the Normal-Normal update]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_normal_normal_formula_summary.png)

![How sample size changes the Normal-Normal posterior]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_normal_normal_sample_size_effect.png)

![Relative prior and data weights in the Normal-Normal model]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_normal_normal_prior_data_weights.png)

### 6.3. Quick memory rule

Even if you forget the exact formula, the right intuition is that the more precise source of information receives more weight, while the posterior variance shrinks as the data become more informative.

## 7. Sequential updating

One of the nicest features of conjugate models is how naturally they support sequential learning. You can update with today's data, use the resulting posterior as tomorrow's prior, and continue the process without having to restart the derivation from scratch each time new data arrive.

![Sequential updating with conjugate priors]({{ site.baseurl }}/img/chapter_img/chapter02/sequential_updating_story.png)

This is useful for dashboards, quality monitoring, and streaming observations.

## 8. Why learn conjugacy if we later use MCMC?

Conjugacy remains worth learning even if we later rely on MCMC, and the reasons go beyond mere computational convenience. First, it builds strong intuition for how Bayesian updating works, because the effect of prior information and observed data can usually be read directly from the updated parameters. Second, it gives exact answers that are extremely useful when we want to check whether numerical methods such as grid approximation or MCMC are behaving sensibly. Third, it remains genuinely practical for many simple one-parameter models, where an exact and interpretable solution is often more valuable than a more elaborate computational approach.

![Conjugacy versus broader computational methods]({{ site.baseurl }}/img/chapter_img/chapter02/conjugacy_vs_mcmc.png)

## 9. Limits of conjugacy

Conjugacy is about convenience, not truth. We should not force a conjugate prior if it is a poor description of prior knowledge, and this becomes especially important when the realistic prior is multimodal, when the model is hierarchical, when the parameter space has complex constraints, or when the dependence structure is richer than a simple one-parameter setup can express.

Support matters too. Sometimes the algebra looks familiar, but the posterior no longer fits a standard family on the correct parameter domain. In those cases the model can still be valid, but it is no longer a clean “same family in, same family out” conjugate case.

![A conjugate prior can poorly represent a truncated or constrained ideal prior]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_conjugate_limit_truncated_prior.png)

![A compact overview of when conjugacy stops being a good fit]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_conjugate_limit_overview.png)

![Mixture priors are a common case where conjugate families become too restrictive]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_conjugate_limit_mixture_prior.png)

![A quick decision tree for staying with conjugacy or moving to MCMC]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_conjugate_limit_decision_tree.png)

In such cases, we turn to grid approximation or MCMC.

## 10. Quick guide to common conjugate pairs

![Table of common conjugate pairs]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_pairs_table.png)

Think in terms of data stories rather than isolated formulas. If the parameter is a probability of success, Beta with Binomial is the natural pair; if the problem is about waiting until the first success, Beta with Geometric is the right mental model; if the target is an event rate, Gamma with Poisson is the standard pair; and if the unknown quantity is the mean of continuous data, Normal with Normal is the natural starting point.

## 11. Common misunderstandings

### 11.1. “A conjugate prior is always the best prior”

No. It is only the most convenient one computationally.

### 11.2. “Memorizing formulas is enough”

No. Without the generative story, the formulas become easy to misuse.

### 11.3. “Conjugacy is obsolete because of MCMC”

No. It is still foundational for intuition and for simple exact solutions.

## Summary

**Conjugate priors are priors that keep the posterior in the same family after updating.** That property makes Bayesian inference easier to compute, easier to explain, and easier to update sequentially, which is why the four basic pairs in this lesson, namely Beta-Binomial, Beta-Geometric, Gamma-Poisson, and Normal-Normal, are worth remembering. Even so, the more important principle is that computational convenience should never replace good modeling judgment. In condensed form, the lesson is this: conjugacy happens when the algebra of the prior and likelihood matches so that the posterior stays in the same family, conjugate pairs are exceptionally useful for building intuition and checking simple exact updates, and a conjugate prior remains only a convenient choice rather than an automatically superior one.

## Practice questions

1. Give one real-world example that fits Beta-Binomial.
2. What is the key data-story difference between Beta-Binomial and Beta-Geometric?
3. Why is Gamma-Poisson so natural for count data over time?
4. In the Normal-Normal model, what makes the posterior mean stay closer to the prior mean or move closer to the sample mean?
5. When would you avoid a conjugate prior even though it is convenient?

## References

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 2.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 6-7.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 2-3.

---

*Next lesson: [2.6 Grid Approximation - Discrete Approximation to the Posterior](/en/chapter02/grid-approximation/)*
