---
layout: post
title: "Lesson 2.7: Modern Applications of Conjugate Updating and Empirical Bayes"
chapter: '02'
order: 7
owner: Nguyen Le Linh
lang: en
categories:
- chapter02
lesson_type: optional
---

## Learning objectives

After this optional lesson you should see conjugate priors and grid approximation as industrial design choices, not classroom tricks. You will be able to point to a live product—ads, ranking, or rate monitoring—and say which likelihood is being assumed, which prior family keeps the update cheap, and when the algebra must be abandoned for simulation.

## Prerequisites

Lessons 2.1–2.6 already built the four-part skeleton: distribution, likelihood, prior, posterior. This lesson does not re-derive Beta–Binomial or Gamma–Poisson conjugacy. It asks why those pairs still appear inside large CS systems, and why empirical Bayes is the usual way the prior gets a number.

## Introduction

Once you can update a Beta by counting successes, a natural doubt appears. Why would a company with millions of users still care about a closed-form posterior? The answer is latency and multiplicity. An ads or ranking stack may need a conversion probability for every item, every minute. A full MCMC draw for each item is often too slow; a conjugate update that adds counts to $$(\alpha,\beta)$$ is not. The intellectual tension is therefore economic as well as statistical. Exact algebra survives where it is *fast enough to be honest at scale*.

## Conceptual development

A conjugate prior is a family that stays inside itself after multiplication by the likelihood. For a conversion probability $$\theta$$ with binomial data, the Beta prior yields

$$
\theta\mid y \sim \mathrm{Beta}(\alpha+y,\ \beta+n-y).
$$

The same addition of counts is what a dashboard calls “smoothing.” Empirical Bayes chooses $$\alpha$$ and $$\beta$$ from the ensemble of items rather than from a single expert guess, so a rare item borrows strength from the marketplace. When the likelihood leaves the exponential family, or the prior must be hierarchical in a way that breaks conjugacy, the grid you met in Lesson 2.6 becomes the last exact picture before Hamiltonian Monte Carlo.

## Models as generative stories

### 1. Beta–Binomial rates in advertising and ranking

Imagine each creative, query–item pair, or recommended pin as having an unknown click or conversion probability $$\theta_i$$. The data story is brutally simple: $$n_i$$ opportunities, $$y_i$$ successes. A shared Beta prior, with hyperparameters fit by empirical Bayes, shrinks noisy items toward the marketplace mean. That is why a new item with one click in two impressions is not treated as a 50% converter. The posterior mean

$$
\hat\theta_i=\frac{\alpha+y_i}{\alpha+\beta+n_i}
$$

is the ranking score that can be refreshed with integer additions. Pinterest’s PinnerFormer (Pancha et al., 2022) is a sequence model for user representations, but the serving layer still needs well-behaved item rates; conjugate smoothing remains the inexpensive first Bayesian move beneath more elaborate rankers.

### 2. Thompson sampling as posterior sampling for decisions

Russo et al. (2018) organized a fact that platforms still implement daily: if you can sample from $$p(\theta\mid y)$$, you can choose an action by pretending the sample is true. For a Beta–Binomial bandit that sample is one line of code. The generative story is sequential. Today’s posterior becomes tomorrow’s prior; exploration is not a heuristic but a consequence of remaining posterior width. Modern contextual bandits replace the Beta with a regression posterior, yet the decision rule—sample, then act—is the same update you have already performed on a grid.

### 3. Gamma–Poisson monitoring of counts

Infrastructure events, streaming-quality drops, and incident counts are often modeled as Poisson with a Gamma prior on the rate. The posterior remains Gamma after a night of counts, so an on-call system can report a posterior predictive interval without a sampler. When overdispersion appears, the story must change to Negative Binomial and conjugacy is no longer a free lunch. That is the moment Lesson 2.6 was preparing: draw a grid, see the posterior warp, and admit that a closed form has ended.

### 4. When conjugacy fails: from the grid to probabilistic programming

Stan, PyMC, and NumPyro all document conjugate models as the cases you should *not* waste a sampler on, and nonconjugate models as the reason NUTS exists. The grid is still the right mental picture. It shows the unnormalized product $$p(y\mid\theta)p(\theta)$$ as a landscape. Hamiltonian Monte Carlo, introduced in Chapter 4, is what you do when that landscape has too many coordinates for a grid. Pathfinder (Zhang, Carpenter, Gelman, and Vehtari, 2022) later uses a quasi-Newton path to place a cheap Gaussian near the same landscape, often as a warm start. The Chapter 2 objects have not been replaced; they have been given compilers.

## Interpretation and insight

A shrunk rate is not “the true CTR.” It is a posterior mean under a hierarchical story that may be wrong if items are not exchangeable—creatives in different countries, or queries with incompatible intents. Thompson sampling does not remove regret; it spends posterior uncertainty. A Gamma interval that ignores a change-point will look precise and be late. Read every closed form as an assumption that the next observation is still of the same kind.

## Applications

Ads, ranking, site reliability, and sequential experiments are four places where Chapter 2 is already in production. They also show the boundary: conjugacy for the inner loop, simulation for the model that no longer fits on a whiteboard.

## Limitations and extensions

Empirical Bayes point-estimates the hyperparameters and therefore understates uncertainty about the prior itself. Fully hierarchical Bayes, which Chapter 5’s multilevel thinking begins to motivate, puts a posterior on $$(\alpha,\beta)$$. Grid approximation dies in more than a few dimensions. The honest next tool is not a fancier conjugate table but a sampler, which Chapter 4 develops.

## Exercises

1. Two items have click data $$(y,n)=(1,2)$$ and $$(40,100)$$. Under a $$\mathrm{Beta}(2,98)$$ prior, which posterior mean moves more, and what product decision does that justify?
2. Write the generative story for Thompson sampling on three email subject lines. What is observed, what is latent, and when should you stop exploring?
3. A Poisson–Gamma monitor reports a tight rate after a quiet weekend. Traffic is ten times higher on Monday. Which assumption broke?
4. Open the PyMC or Stan getting-started page and find one example that is conjugate and one that is not. For the second, say why a grid would fail.

## References

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 2–3.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 6.
- Russo, D., Van Roy, B., Kazerouni, A., Osband, I., & Wen, Z. (2018). A tutorial on Thompson sampling. *Foundations and Trends in Machine Learning*, 11(1), 1–96.
- Pancha, N., Zhai, A., Leskovec, J., & Rosenberg, C. (2022). PinnerFormer: Sequence modeling for user representation at Pinterest. *KDD*. [arXiv:2205.04507](https://arxiv.org/abs/2205.04507).
- Zhang, L., Carpenter, B., Gelman, A., & Vehtari, A. (2022). Pathfinder: Parallel quasi-Newton variational inference. *JMLR*, 23(306), 1–49. [arXiv:2108.03782](https://arxiv.org/abs/2108.03782).
- [Stan User’s Guide](https://mc-stan.org/docs/stan-users-guide/index.html).
- [PyMC overview](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html).
- [NumPyro getting started](https://num.pyro.ai/en/stable/getting_started.html).
