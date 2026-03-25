---
layout: post
title: "Lesson 0.12: What is a Statistical Model?"
chapter: '00'
order: 12
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

## Learning objectives

After this lesson, you will understand a practical definition of a statistical model as a probability description of how data are generated, distinguish observed data from unknown parameters, and see why asking "what assumptions does this model make?" matters more than memorizing formulas.

## 1) Motivation: Data do not speak without a model

From a dataset, we can compute means, standard deviations, and histograms. But those summaries alone do not answer inference questions such as:

What the true population rate is, whether an effect is large enough to matter, or how uncertain future predictions are.

To answer these, we need a bridge from "unknown parameter" to "observable data." That bridge is a statistical model.

## 2) Core definition

A **statistical model** is a family of probability distributions for data $$x$$, indexed by parameter(s) $$\theta$$:

$$
\mathcal{M} = \{p(x\mid \theta): \theta \in \Theta\}
$$

Here, $$x$$ denotes observed data, $$\theta$$ is the unknown quantity governing the data-generating mechanism, and $$\Theta$$ is the parameter space, that is, the set of valid values of $$\theta$$.

In short: a statistical model encodes "if parameters look like this, data tend to look like that."

## 3) Generative-story view

In this course, we use a generative interpretation: first imagine some unknown parameter value $$\theta$$, then generate data $$x$$ from $$p(x\mid\theta)$$, and finally compare the observed data with what the model would expect under plausible values of $$\theta$$.

Coin example:

In the coin example, $$\theta$$ is the probability of heads, each toss produces an observation $$y_i \sim \text{Bernoulli}(\theta)$$, and after $$n$$ tosses the total number of heads $$k=\sum_i y_i$$ follows $$\text{Binomial}(n,\theta)$$.

The model is not only the binomial formula. It also assumes that each trial has the same $$\theta$$, that trials are independent, and that the data are counts arising from repeated trials under a common mechanism.

![Statistical model as bridge from parameters to data]({{ site.baseurl }}/img/chapter_img/chapter00/statistical_model_definition_flow.png)
*Figure 1: A statistical model links unknown parameters $$\theta$$ to observed data $$x$$ through the data-generating mechanism $$p(x\mid\theta)$$, then updates beliefs to posterior $$p(\theta\mid x)$$.*

## 3.1) How are models and simulations different?

These two ideas are easy to mix up, but they play different roles: a model is a probability description of the data-generating mechanism, while a simulation is what happens when we run that description on a computer to generate fake data many times.

Coin example:

The model says each toss satisfies $$y_i\sim\text{Bernoulli}(\theta)$$. A simulation chooses a specific value such as $$\theta=0.6$$ and then generates many repeated datasets to see how the proportion of heads varies.

Short Python simulation example:

```python
import numpy as np

np.random.seed(42)

theta = 0.6
n_tosses = 20
n_simulations = 10_000

heads_counts = np.random.binomial(n_tosses, theta, size=n_simulations)
head_rates = heads_counts / n_tosses

print(heads_counts[:10])
print(head_rates.mean(), head_rates.std())
```

In this code, the model is still $$K \sim \text{Binomial}(20, 0.6)$$. The simulation simply asks: if that model were true, how many heads would we usually see in 20 tosses, and how much variation would appear across repetitions?

After many repetitions, the average of `head_rates` will be close to 0.6, but individual simulated datasets still vary around that value. That is the key point: a model does not imply one fixed outcome, but a distribution of plausible outcomes.

## 4) A model is not "the truth"

A common mistake is to search for a perfectly true model. In practice:

A model is a map rather than the territory, every model necessarily simplifies reality, and its value comes from how well it supports prediction, explanation, and decision-making.

So whenever we model, we ask:

We should therefore ask which assumptions are being imposed, whether those assumptions fit the context, and how our conclusions could fail if those assumptions are wrong.

## 5) Direct link to Bayesian inference

In Bayesian analysis, the model appears through the likelihood:

$$
p(\theta\mid x) \propto p(x\mid\theta)\,p(\theta)
$$

Here:

The term $$p(x\mid\theta)$$ comes from the statistical model, $$p(\theta)$$ is the prior, and the posterior $$p(\theta\mid x)$$ is the updated belief after seeing the data.

If the model is unclear, the likelihood is unclear, and the posterior loses interpretability.

## 6) Mini example: student heights

Suppose $$x_1,\dots,x_n$$ are student heights (cm). A simple model is:

$$
x_i \sim \mathcal{N}(\mu,\sigma^2),\quad i=1,\dots,n
$$

where $$\mu$$ is class-average height and $$\sigma$$ is spread.

This model implicitly assumes approximately normal data, conditional independence given the parameters, and a shared data-generating process across observations.

With this model, we can estimate and interpret $$\mu, \sigma$$, make predictions, and check whether the model is missing important structure.

## Quick recap

1. A statistical model is a family $$\{p(x\mid\theta)\}$$ for data.
2. It links unknown parameters to observed data via a generative mechanism.
3. Every model carries assumptions; understanding assumptions is central.
4. In Bayes, the model provides the likelihood that updates prior to posterior.

## Exercises

1. For the coin example, list three implicit assumptions of the binomial model.
2. Give one context where the independence assumption is likely violated.
3. Explain in your own words: "A model is a map, not the territory."

## References

- McElreath, R. (2020). *Statistical Rethinking* (2nd ed.). CRC Press.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Wasserman, L. (2004). *All of Statistics*. Springer.
