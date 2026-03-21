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

## Learning objectives

After this lesson, you should understand grid approximation as the bridge from hand-calculated Bayes to computational Bayes. You should know how to discretize a parameter space, compute a posterior on a grid, and explain why this method is excellent for learning but limited for high-dimensional models.

> **Mini example.** You want to infer $$\theta$$ after seeing 6 heads in 9 tosses, but instead of working over the entire interval $$[0,1]$$, you only test candidate values like $$0, 0.25, 0.5, 0.75, 1$$. That is the basic idea of grid approximation.
>
> **Quick check.** If you increase the grid from 5 points to 100 or 1000 points, what do you expect to improve?

## Opening idea: what if the posterior has no clean closed form?

Conjugate models are elegant, but real problems are not always so cooperative.

Examples:

- the prior may be a mixture of competing beliefs,
- the prior and likelihood may not combine into a closed-form posterior,
- or we may simply want a very transparent computational approach.

Grid approximation is the simplest way to start.

![A visual introduction to grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/grid_approximation_intro.png)

## 1. Core idea: replace a continuum with a finite set of points

Suppose $$\theta$$ lies in $$[0,1]$$. Instead of considering every possible value continuously, choose grid points:

$$
\theta_1,\theta_2,\dots,\theta_G.
$$

At each point, compute:

- the prior,
- the likelihood,
- the unnormalized posterior.

Then normalize the weights. The result is a discrete approximation to the posterior.

## 2. A tiny hand-worked example

Suppose:

- the prior is uniform on $$[0,1]$$,
- the data are 6 heads in 9 tosses,
- the grid is:

$$
\theta \in \{0,\ 0.25,\ 0.5,\ 0.75,\ 1\}.
$$

The likelihood is proportional to:

$$
\theta^6(1-\theta)^3.
$$

Evaluate that expression at each grid point, multiply by the prior, and normalize.

The main lesson is not the exact numbers. It is the workflow:

- score candidate values,
- compare them,
- normalize them.

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

## 4. Finer grids improve the approximation

Using 5 points gives a rough picture. Using 20, 100, or 1000 points gives a smoother and more accurate approximation.

![Grid approximation with different resolutions]({{ site.baseurl }}/img/chapter_img/chapter02/grid_approximation_basics.png)

![Effect of grid size]({{ site.baseurl }}/img/chapter_img/chapter02/grid_size_comparison.png)

This gives a clear trade-off:

- coarse grid  $$\rightarrow$$ faster but rougher,
- fine grid  $$\rightarrow$$ more accurate but more expensive.

## 5. A useful case: non-conjugate priors

Suppose analysts have two competing prior beliefs about a return rate:

- one mode near $$0.3$$,
- another mode near $$0.7$$.

That gives a mixture prior with two peaks. Closed-form algebra may no longer be convenient, but grid approximation still works naturally:

1. evaluate the mixture prior on the grid,
2. evaluate the likelihood,
3. normalize.

![Grid approximation with a mixture prior]({{ site.baseurl }}/img/chapter_img/chapter02/grid_mixture_prior_example.png)

## 6. What can we do with a grid posterior?

Quite a lot.

### 6.1. Posterior mean

$$
E[\theta \mid D] \approx \sum_i \theta_i p(\theta_i \mid D).
$$

### 6.2. Interval probabilities

Add posterior weights over the relevant grid points.

### 6.3. Credible intervals

Use the cumulative posterior mass on the grid.

### 6.4. Posterior sampling

Draw grid points according to their posterior weights.

![Statistics from a grid posterior]({{ site.baseurl }}/img/chapter_img/chapter02/grid_statistics_computation.png)

## 7. Posterior predictive with a grid

Once the posterior is available on a grid, future-data prediction becomes easy:

$$
P(y_{\text{new}} \mid D) = \sum_i P(y_{\text{new}} \mid \theta_i)p(\theta_i \mid D).
$$

![Posterior predictive from grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/grid_posterior_predictive.png)

This is where the method starts to feel practically useful, not just pedagogically useful.

## 8. When is grid approximation especially useful?

### 8.1. When learning Bayesian inference

It makes every part of Bayes visible.

### 8.2. For one-parameter problems

It is often simple, fast, and easy to visualize.

### 8.3. As a small-model check

Even if you later use MCMC, grid approximation can be a useful sanity check in tiny problems.

![When to use grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/when_to_use_grid.png)

## 9. The main limitation: curse of dimensionality

If each parameter uses 100 grid points:

- 1 parameter  $$\rightarrow$$ 100 points,
- 2 parameters  $$\rightarrow$$ 10,000 points,
- 3 parameters  $$\rightarrow$$ 1,000,000 points,
- 4 parameters  $$\rightarrow$$ 100,000,000 points.

![Curse of dimensionality]({{ site.baseurl }}/img/chapter_img/chapter02/curse_of_dimensionality.png)

So grid approximation is excellent for very small models and quickly becomes impractical as dimension grows.

## 10. Where does grid approximation fit in the bigger picture?

You can think of the main approaches this way:

- conjugate priors for exact closed-form updates,
- grid approximation for small transparent computational updates,
- MCMC for general high-dimensional models.

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

**Grid approximation computes a posterior by discretizing the parameter space into a finite grid.** It is intuitive, flexible, and excellent for learning or for very small models. Its main weakness is dimensionality, which is why more advanced methods such as MCMC are needed later.

> **3 key takeaways.**
> 1. Grid approximation turns a continuous posterior problem into a discrete weighted comparison over candidate values.
> 2. It is especially useful for small models and for cases where conjugacy is unavailable.
> 3. Its main limitation is the curse of dimensionality, so it does not scale to many parameters.

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

*End of Chapter 02. Next chapter: [Chapter 03 - Sampling, Monte Carlo, and MCMC](/en/chapter03/)*
