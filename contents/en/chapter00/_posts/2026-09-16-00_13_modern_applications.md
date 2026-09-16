---
layout: post
title: "Lesson 0.13: Modern Applications of Foundational Probability in Data Science"
chapter: '00'
order: 13
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: optional
---

## Learning objectives

By the end of this optional lesson you should be able to recognize the Chapter 0 toolkit—probability, joint distributions, expectation, log-probability, and simulation—not as a waiting room before Bayes, but as the same language that modern computer science and data science use when they ask whether a model is calibrated, numerically stable, and generative. The aim is a change of stance: foundational objects become design questions rather than review items.

## Prerequisites

This lesson assumes the required Chapter 0 sequence. It does not introduce new probability theory. It only asks what happens when those ideas leave the classroom and enter classifiers, language models, and probabilistic programs.

## Introduction

A student who has just finished Chapter 0 can compute a mean, write a density, and simulate a sampling distribution. Industry problems look larger, but they often fail for the same small reasons: a reported probability is not a long-run frequency, a product of tiny likelihoods underflows, or a joint model is written as if dependence did not exist. The tension of this lesson is therefore modest and useful. If the foundations are already in place, why do modern systems still misread uncertainty? Because scale does not replace the meaning of a probability statement.

## Conceptual development

A probability $$p$$ attached to a prediction is a claim about a data-generating process. If a model says $$p=0.9$$ on one hundred cases, about ninety of those cases should be correct if the number is calibrated. That is the same idea as a sampling distribution, now applied to machine-learning scores rather than to a sample mean. Joint structure matters for the same reason: once two events are dependent, the product of marginals is no longer a story about the world. Simulation remains the cheapest way to see whether the story is even possible.

## Models as generative stories

### 1. Calibration of classifiers and language models

Spam filters, fraud scores, and medical alerts all output a number that looks like a probability. The generative question is not “did the model rank cases well?” but “if the model claims $$P(\text{positive}\mid x)=0.8$$, do eight in ten such cases really occur?” Kadavath et al. (2022) showed that large language models can be surprisingly well calibrated on formatted true/false and multiple-choice tasks, and that a model can be asked for $$P(\text{True})$$ after it proposes an answer. Tian et al. (2023) then showed that models fine-tuned with human feedback often give better-calibrated *verbalized* confidences than their raw token probabilities. The Chapter 0 moral is exact: a number in $$[0,1]$$ is not automatically a probability until it survives a frequency check.

### 2. Log-probability and numerical stability in large models

Training and inference in modern networks repeatedly evaluate products of probabilities. In log space the product becomes a sum,

$$
\log p(x_{1:n})=\sum_{i=1}^{n}\log p(x_i\mid x_{<i}),
$$

which is why Chapter 0 insisted on log-probability. The same identity is what keeps language-model likelihoods from underflowing and what makes the log-sum-exp trick a standard primitive. The model believes that tokens are generated sequentially; the computer can only believe that story if the arithmetic does not collapse to zero.

### 3. Joint distributions in probabilistic programming

A PyMC or NumPyro program is a joint distribution written as a generative recipe: first sample parameters, then sample data given parameters. That is precisely the Chapter 0 definition of a statistical model, now compiled so that later chapters can condition it. When tabular predictors are strongly dependent, the joint—not a pile of one-dimensional summaries—is the object that later Bayesian models must respect. Grinsztajn, Oyallon, and Varoquaux (2022) remind us that on many ordinary tabular tasks, tree ensembles still beat deep nets, in part because the relevant joint structure is discrete, heterogeneous, and not well served by a generic continuous density.

### 4. Simulation as a check on intuition

Chapter 0 treated simulation as a way to see sampling variability. The same habit now appears as posterior predictive checking and as simulation-based calibration: draw parameters from a prior, draw data, refit, and ask whether the recovered uncertainties are honest (Modrák et al., 2025). Before you meet Markov chain Monte Carlo, you already have the right question. Does the computational story reproduce the probabilistic story?

## Interpretation and insight

In each application the posterior or the score is easy to over-read. A calibrated $$P(\text{True})$$ is still not a proof that the model “knows.” A stable log-likelihood is still not a correct likelihood. A joint program is still only as honest as the conditional independence it assumes. The useful habit is to ask what frequency, what dependence, and what simulation would embarrass the claim.

## Applications

These four settings already cover ranking, language, tabular modeling, and software for Bayesian computation. They are not extra topics. They are Chapter 0 spoken in the dialect of current CS/DS practice.

## Limitations and extensions

This lesson does not replace a course on deep learning or probabilistic programming. Calibration can fail after a distribution shift; log-space arithmetic does not fix a misspecified likelihood; and simulation-based checks only test the computation you actually ran. The next chapters begin the Bayesian update itself.

## Exercises

1. A fraud model outputs $$0.99$$ on ten transactions, three of which are later confirmed as fraud. In one paragraph, say what “miscalibrated” means here and which Chapter 0 object you would plot.
2. Explain why a language model’s next-token probabilities can look confident in token space and still be uncertain in meaning space. What extra invariance would you need?
3. Write a four-line generative story (in words, not code) for a Beta–Binomial conversion rate. Identify the joint, the observed, and the unobserved.
4. A colleague says simulation is only for teaching. Using the idea of simulation-based calibration, argue for one industrial use.

## References

- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. *Bayesian Data Analysis* (3rd ed.), Ch. 1.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 4–5.
- Kadavath, S., et al. (2022). Language models (mostly) know what they know. [arXiv:2207.05221](https://arxiv.org/abs/2207.05221).
- Tian, K., et al. (2023). Just ask for calibration. [arXiv:2305.14975](https://arxiv.org/abs/2305.14975).
- Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why do tree-based models still outperform deep learning on typical tabular data? *NeurIPS*.
- Modrák, M., et al. (2025). Simulation-based calibration checking for Bayesian computation. *Bayesian Analysis*, 20(2), 461–488. [arXiv:2211.02383](https://arxiv.org/abs/2211.02383).
- [PyMC conceptual overview](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html).
