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

- what is the true population rate,
- whether an effect is large enough to matter,
- how uncertain future predictions are.

To answer these, we need a bridge from "unknown parameter" to "observable data." That bridge is a statistical model.

## 2) Core definition

A **statistical model** is a family of probability distributions for data $$x$$, indexed by parameter(s) $$\theta$$:

$$
\mathcal{M} = \{p(x\mid \theta): \theta \in \Theta\}
$$

Where:

- $$x$$: observed data,
- $$\theta$$: unknown quantity controlling the data-generating mechanism,
- $$\Theta$$: parameter space (valid values of $$\theta$$).

In short: a statistical model encodes "if parameters look like this, data tend to look like that."

## 3) Generative-story view

In this course, we use a generative interpretation:

1. Choose parameter(s) $$\theta$$ (unknown).
2. Generate data $$x$$ from $$p(x\mid\theta)$$.
3. Compare observed data with what the model expects.

Coin example:

- $$\theta$$ is the probability of heads,
- each toss: $$y_i \sim \text{Bernoulli}(\theta)$$,
- after $$n$$ tosses: $$k=\sum_i y_i \sim \text{Binomial}(n,\theta)$$.

The model is not only the binomial formula. It also assumes:

- each trial has the same $$\theta$$,
- trials are independent,
- the data are counts from repeated trials.

![Statistical model as bridge from parameters to data]({{ site.baseurl }}/img/chapter_img/chapter00/statistical_model_definition_flow.png)
*Figure 1: A statistical model links unknown parameters $$\theta$$ to observed data $$x$$ through the data-generating mechanism $$p(x\mid\theta)$$, then updates beliefs to posterior $$p(\theta\mid x)$$.*

## 4) A model is not "the truth"

A common mistake is to search for a perfectly true model. In practice:

- a model is a map, not the territory,
- every model simplifies reality,
- model value comes from prediction, explanation, and decision support.

So whenever we model, we ask:

- which assumptions are being imposed,
- whether those assumptions fit the context,
- how conclusions could fail if assumptions are wrong.

## 5) Direct link to Bayesian inference

In Bayesian analysis, the model appears through the likelihood:

$$
p(\theta\mid x) \propto p(x\mid\theta)\,p(\theta)
$$

Here:

- $$p(x\mid\theta)$$ comes from the statistical model,
- $$p(\theta)$$ is the prior,
- posterior $$p(\theta\mid x)$$ is the updated belief.

If the model is unclear, the likelihood is unclear, and the posterior loses interpretability.

## 6) Mini example: student heights

Suppose $$x_1,\dots,x_n$$ are student heights (cm). A simple model is:

$$
x_i \sim \mathcal{N}(\mu,\sigma^2),\quad i=1,\dots,n
$$

where $$\mu$$ is class-average height and $$\sigma$$ is spread.

This model implicitly assumes:

- approximately normal data,
- conditional independence given parameters,
- a shared data-generating process across observations.

With this model, we can:

- estimate and interpret $$\mu, \sigma$$,
- make predictions,
- check model mismatch.

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
