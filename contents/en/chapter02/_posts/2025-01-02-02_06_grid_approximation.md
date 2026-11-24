---
layout: post
title: "Lesson 2.6: Grid Approximation - Discrete Approximation to the Posterior"
chapter: '02'
order: 6
owner: Nguyen Le Linh
lang: en
categories:
- chapter02
lesson_type: required
---

Conjugate priors feel like magic—until the first time your real-world problem refuses to cooperate. The moment you impose a truncated prior, a multimodal prior, or a non-standard likelihood, the neat algebraic shortcut vanishes and you are staring at an integral in the denominator of Bayes' rule that has no closed-form antiderivative. Before we ever touch fancy MCMC samplers, there is a disarmingly simple, transparent weapon that lets you compute *any* 1D or 2D posterior with nothing more than arithmetic: **grid approximation**.

**Lesson Roadmap:** Why closed-form conjugacy breaks → Background Knowledge Map (Riemann sums, non-conjugate inference, curse of dimensionality) → Hand-worked 5-point grid check → Finer grids, non-conjugate priors, posterior summaries, and exercises.

## Learning objectives

After this lesson, you should understand grid approximation as the bridge from hand-calculated Bayes to computational Bayes. You should know how to discretize a parameter space, compute a posterior on a grid, and explain why this method is excellent for learning but limited for high-dimensional models.

> **Mini example.** You want to infer $$\theta$$ after seeing 6 heads in 9 tosses, but instead of working over the entire interval $$[0,1]$$, you only test candidate values like $$0, 0.25, 0.5, 0.75, 1$$. That is the basic idea of grid approximation.
>
> **Quick check.** If you increase the grid from 5 points to 100 or 1000 points, what do you expect to improve?

## Background Knowledge Map: What Grid Approximation Really Is

### 1. Discrete Quadrature for Bayes' Denominator
- **What it is:** Replacing the continuous marginal-likelihood integral $$P(D) = \int p(D \mid \theta)p(\theta)\,d\theta$$ with a finite Riemann sum over $$M$$ evenly spaced grid points $$\theta_1, \dots, \theta_M$$.
- **What it studies:** How accurately a finite probability vector $$\mathbf{w}$$ approximates a continuous posterior density $$p(\theta \mid D)$$, and how posterior expectations $$\mathbb{E}[g(\theta) \mid D] \approx \sum_{j=1}^M w_j g(\theta_j)$$ turn into simple weighted averages.

### 2. Breaking Free from Conjugacy
- **What it is:** A model-agnostic numerical procedure that evaluates $$p(\theta_j) \cdot p(D \mid \theta_j)$$ pointwise—requiring zero algebraic matching between prior and likelihood.
- **What it studies:** Arbitrary priors (step functions, truncated intervals, mixture priors) and non-standard likelihoods, proving that Bayesian updating is fundamentally *multiply prior by likelihood, then normalize*.

### 3. The Curse of Dimensionality (Why We Eventually Need MCMC)
- **What it is:** The exponential explosion of grid size $$M^d$$ as the number of parameters $$d$$ grows.
- **What it studies:** The exact boundary where grid approximation shines ($$d \le 2$$, teaching, sanity-checking MCMC) versus where it collapses ($$d \ge 4$$), motivating Hamiltonian Monte Carlo and NUTS in Chapter 4.

## Deep-Dive Explanation: A 5-Point Grid Posterior Checked by Hand (Read Slowly)

Suppose you flip a coin $$n = 3$$ times and observe $$k = 2$$ heads, with a flat uniform prior over $$\theta \in [0, 1]$$. Analytically, we know the exact posterior is $$\mathrm{Beta}(3, 2)$$ with mean $$\frac{3}{3+2} = 0.600$$. Now pretend you forgot the Beta formula and evaluate only 5 evenly spaced grid points $$\theta \in \{0.1, 0.3, 0.5, 0.7, 0.9\}$$ (each with prior weight $$1/5$$). Ignoring the constant $$\binom{3}{2} = 3$$ (which cancels on normalization), the unnormalized likelihood is $$L(\theta) = \theta^2(1 - \theta)$$:

| Grid point $$\theta_j$$ | Unnormalized $$\theta_j^2(1-\theta_j)$$ | Normalized weight $$w_j$$ | Contribution $$\theta_j w_j$$ |
| :--- | :--- | :--- | :--- |
| $$0.1$$ | $$0.01 \times 0.9 = 0.009$$ | $$0.009 / 0.425 = 0.0212$$ | $$0.0021$$ |
| $$0.3$$ | $$0.09 \times 0.7 = 0.063$$ | $$0.063 / 0.425 = 0.1482$$ | $$0.0445$$ |
| $$0.5$$ | $$0.25 \times 0.5 = 0.125$$ | $$0.125 / 0.425 = 0.2941$$ | $$0.1471$$ |
| $$0.7$$ | $$0.49 \times 0.3 = 0.147$$ | $$0.147 / 0.425 = 0.3459$$ | $$0.2421$$ |
| $$0.9$$ | $$0.81 \times 0.1 = 0.081$$ | $$0.081 / 0.425 = 0.1906$$ | $$0.1715$$ |
| **Total** | **$$0.425$$** | **$$1.0000$$** | **$$0.6073$$** |

Even with a crude 5-point grid, the posterior mean $$0.6073$$ lands within $$0.007$$ of the exact $$0.6000$$! Yet notice the scaling wall: with $$M = 100$$ points per axis, $$d = 1$$ takes $$100$$ evaluations, $$d = 3$$ takes $$10^6$$, and a modest 10-parameter regression requires $$100^{10} = 10^{20}$$ evaluations—longer than the age of the universe.

## Opening idea: what if the posterior has no clean closed form?

Conjugate models are elegant, but real problems are not always so cooperative.

For example, the prior may be a mixture of competing beliefs, the prior and likelihood may fail to combine into a convenient closed-form posterior, or we may simply want a computational approach transparent enough that every step can still be inspected directly.

Grid approximation is the simplest way to start.

![A visual introduction to grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/grid_approximation_intro.png)

## 1. Core idea: replace a continuum with a finite set of points

Suppose $$\theta$$ lies in $$[0,1]$$. Instead of considering every possible value continuously, choose grid points:

$$
\theta_1,\theta_2,\dots,\theta_G.
$$

At each point, compute:

the prior, the likelihood, and the unnormalized posterior.

Then normalize the weights. The result is a discrete approximation to the posterior.

## 2. A tiny hand-worked example

Suppose the prior is uniform on $$[0,1]$$, the data are 6 heads in 9 tosses, and the grid is:

$$
\theta \in \{0,\ 0.25,\ 0.5,\ 0.75,\ 1\}.
$$

The likelihood is proportional to:

$$
\theta^6(1-\theta)^3.
$$

Evaluate that expression at each grid point, multiply by the prior, and normalize.

The main lesson is not the exact numbers themselves, but the workflow: we score candidate values, compare them, and then normalize the resulting weights into a proper posterior approximation.

### 2.1. Reading the grid posterior numerically

The sum of the three nonzero weights above is approximately:

$$
0.000103 + 0.001953 + 0.002781 = 0.004837.
$$

After normalization, the discrete posterior on this grid is approximately:

- $$P(\theta=0.25 \mid D) \approx 0.021$$
- $$P(\theta=0.50 \mid D) \approx 0.404$$
- $$P(\theta=0.75 \mid D) \approx 0.575$$

So even on a very coarse grid, we can already answer questions like:

$$
P(\theta \ge 0.5 \mid D) \approx 0.404 + 0.575 = 0.979.
$$

This is one of the nicest things about grid approximation: it turns the posterior into concrete probabilities that we can add, compare, and interpret directly.

## 3. The grid algorithm

![Grid approximation algorithm steps]({{ site.baseurl }}/img/chapter_img/chapter02/grid_algorithm_steps.png)

### Step 1. Build the grid

For example:

$$
\theta_{\text{grid}} = \text{linspace}(0,1,G).
$$

### Step 2. Compute the prior on the grid

### Step 3. Compute the likelihood on the grid

### Step 4. Multiply prior and likelihood

$$
p(\theta_i \mid D) \propto p(D \mid \theta_i)p(\theta_i).
$$

### Step 5. Normalize

Divide by the total weight.

### Try it: grid approximation step by step

Lay a grid, compute prior and likelihood, multiply and normalise; add points to watch the error shrink.

<div class="interactive-demo" markdown="1">
<div data-demo="grid-explainer" data-lang="en" data-prior="flat" data-k="6" data-n="9" data-points="10"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 4. Finer grids improve the approximation

Using 5 points gives a rough picture. Using 20, 100, or 1000 points gives a smoother and more accurate approximation.

![A very coarse 5-point grid]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_resolution_5.png)

![A medium 20-point grid]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_resolution_20.png)

![A finer 100-point grid]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_resolution_100.png)

![Comparing a 5-point grid with the exact posterior]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_vs_exact_5.png)

![Comparing a 20-point grid with the exact posterior]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_vs_exact_20.png)

![Comparing a 100-point grid with the exact posterior]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_vs_exact_100.png)

![Effect of grid size]({{ site.baseurl }}/img/chapter_img/chapter02/grid_size_comparison.png)

This creates a clear trade-off: a coarse grid is faster but rougher, while a fine grid is more accurate but also more computationally expensive.

## 5. A useful case: non-conjugate priors

Suppose analysts have two competing prior beliefs about a return rate, with one mode near $$0.3$$ and another mode near $$0.7$$.

That gives a mixture prior with two peaks. Closed-form algebra may no longer be convenient, but grid approximation still works naturally, because we only need to evaluate the mixture prior on the grid, evaluate the likelihood at the same points, and then normalize the resulting weights.

![Grid approximation with a mixture prior]({{ site.baseurl }}/img/chapter_img/chapter02/grid_mixture_prior_example.png)

### Try it: a non-conjugate prior (skewed triangle)

With no closed form the grid still gives an accurate posterior when fine enough.

<div class="interactive-demo" markdown="1">
<div data-demo="grid-explainer" data-lang="en" data-prior="tri" data-k="8" data-n="12" data-points="100"></div>
</div>

## 6. What can we do with a grid posterior?

Quite a lot, and that is precisely why grid approximation is more than a toy example.

### 6.1. Posterior mean

$$
E[\theta \mid D] \approx \sum_i \theta_i p(\theta_i \mid D).
$$

![Posterior mean, median, and mode on the grid]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_stat_mean_median_mode.png)

### 6.2. Interval probabilities

Add posterior weights over the relevant grid points.

![An interval probability computed from the grid posterior]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_stat_interval_probability.png)

### 6.3. Credible intervals

Use the cumulative posterior mass on the grid.

![A credible interval extracted from the discrete posterior]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_stat_credible_interval.png)

### 6.4. Posterior sampling

Draw grid points according to their posterior weights.

![Sampling directly from the grid posterior]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_stat_sampling.png)

## 7. Posterior predictive with a grid

Once the posterior is available on a grid, future-data prediction becomes easy, because prediction can be obtained by averaging conditional predictive distributions over the posterior weights on the grid:

$$
P(y_{\text{new}} \mid D) = \sum_i P(y_{\text{new}} \mid \theta_i)p(\theta_i \mid D).
$$

![Posterior predictive distribution obtained from the grid posterior]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_predictive_distribution.png)

![Grid posterior predictive compared with the exact solution]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_predictive_vs_exact.png)

This is where the method starts to feel practically useful, not just pedagogically useful.

## 8. When is grid approximation especially useful?

### 8.1. When learning Bayesian inference

It makes every part of Bayes visible, because prior, likelihood, posterior, normalization, and prediction all appear as explicit computations on a finite set of candidate values.

### 8.2. For one-parameter problems

It is often simple, fast enough, and easy to visualize, which makes it especially attractive as a first computational method.

### 8.3. As a small-model check

Even if you later use MCMC, grid approximation can still serve as a useful sanity check in tiny problems where an explicit approximation is cheap and easy to inspect.

![When to use grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/when_to_use_grid.png)

## 9. The main limitation: curse of dimensionality

If each parameter uses 100 grid points, then 1 parameter requires 100 points, 2 parameters require 10,000 points, 3 parameters require 1,000,000 points, and 4 parameters require 100,000,000 points; this explosive growth is exactly what the phrase curse of dimensionality is meant to capture.

![Grid size grows explosively with parameter dimension]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_dimensionality_growth.png)

![A table view of the dimensionality explosion in grid methods]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_dimensionality_table.png)

So grid approximation is excellent for very small models and quickly becomes impractical as dimension grows.

## 10. Where does grid approximation fit in the bigger picture?

You can think of the main approaches this way: conjugate priors are ideal for exact closed-form updates in sufficiently simple problems, grid approximation is useful for small and transparent computational updates, and MCMC is the more general tool for complex high-dimensional models.

![From grid approximation to MCMC]({{ site.baseurl }}/img/chapter_img/chapter02/grid_to_mcmc_bridge.png)

Grid approximation is the conceptual bridge to later computational methods.

## 11. Common misunderstandings

### 11.1. “Grid approximation is always accurate”

No. It is only an approximation, and accuracy depends on resolution and parameter dimension.

### 11.2. “Just increase the grid size and everything is solved”

No. In higher dimensions, the number of grid points explodes.

### 11.3. “Grid approximation is too simple to matter”

No. It is one of the best tools for building Bayesian intuition.

## Summary

**Grid approximation computes a posterior by discretizing the parameter space into a finite grid.** It is intuitive, flexible, and excellent for learning or for very small models, especially when conjugacy is unavailable but the parameter space is still simple enough to explore directly. Its main weakness is dimensionality, which is why more advanced methods such as MCMC are needed later. The main lesson to keep is that grid approximation turns a continuous posterior problem into a discrete weighted comparison over candidate values, works especially well for small models and non-conjugate examples, and fails to scale once the number of parameters becomes even moderately large.

## Reference videos

- [Introduction to the elements of Bayesian statistics. Week 3. Video 2. Grid approx. & probability.](https://www.youtube.com/watch?v=w4fKaBCX02Q) — Peter Blenis, English. **xem trước**. Watch a posterior computed on a grid and normalized by a sum, the algorithm this lesson wants you to implement.
- [Bayes Week 2, Lecture 1: Grid Approximation](https://www.youtube.com/watch?v=2BhfFLATx8c) — Kevin James, English. Watch a second pass over building the grid, multiplying prior by likelihood, and reading the discrete posterior.
- [Statistical Rethinking 2023 - 02 - The Garden of Forking Data](https://www.youtube.com/watch?v=R1vcdhPBlXA) — Richard McElreath, English. Watch Bayesian updating as counting, the idea a grid only discretizes.

## Practice questions

1. Why does a 5-point grid only give a rough approximation?
2. Why is grid approximation such a good teaching tool for one-parameter models?
3. Why does the method break down so quickly in 4 or 5 dimensions?
4. Give one example of a non-conjugate prior where grid approximation is easier than exact algebra.

## References

- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 2-3.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 6.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 3.

---

*End of Chapter 02. Next chapter: [Chapter 04 - Bayesian Linear Regression]({{ site.baseurl }}/contents/en/chapter04/)*
