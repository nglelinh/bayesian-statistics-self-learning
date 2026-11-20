---
layout: post
title: "Lesson 7.4: Modern Applications of Priors, Regularization, and Bayesian Deep Learning"
chapter: '07'
order: 4
owner: Nguyen Le Linh
lang: en
categories:
- chapter07
lesson_type: optional
---

## Learning objectives

After this optional lesson, you will read weight decay, the horseshoe, the Laplace approximation, and deep ensembles as different ways of placing a prior on an overly flexible model. The goal is not to memorize algorithm names, but to see that the overfitting of Chapter 7 is exactly why Bayesian deep learning had to be invented: a network has so many parameters that we need a distribution over functions, not a single optimum.

## Prerequisites

Lessons 7.1–7.3 connected priors with regularization, bias–variance, and variable selection. This lesson does not rewrite the shrinkage theory. It only shows that the same logic is being used on neural networks and high-dimensional tabular models in 2021–2024.

## Introduction

Chapter 7 opened with a tradeoff: a model soft enough will fit the noise, a model rigid enough will drop the signal. In deep learning, that tradeoff is magnified. Millions of weights can interpolate the training set and still generalize, but the confidence a network attaches to a prediction is usually not a probability. The intellectual tension therefore changes shape. It is no longer “should we add variables?”, but “can we keep a posterior, even only on the last layer, honest enough to know when the model does not know?”.

## Conceptual development

A Gaussian prior on the coefficients,

$$
\beta_j\sim\mathcal N(0,\tau^2),
$$

is equivalent to weight decay: the MAP is an optimization with an $$L_2$$ penalty. The horseshoe and spike-and-slab go further: they allow many coefficients near zero and a few large ones, that is, feature selection as a posterior rather than as a pre-filtering step. When $$\beta$$ becomes millions of weights, full MCMC is out of reach. The 2021–2024 approximations—Laplace, last-layer Bayes, ensembles—are different ways of keeping a part of $$p(\theta\mid y)$$.

## Models as generative stories

### 1. Regularization as a prior in GLMs and shallow networks

The generative story does not change: data comes from a simple function plus noise. A narrow prior says “I do not believe the function bends too much”. In credit scoring or tabular ranking, that is often still the right choice, especially since Grinsztajn et al. (2022) show that tree models and regularized linear models remain competitive with deep networks. Chapter 7 is therefore not made obsolete by deep learning; deep learning only makes the prior *more mandatory*.

### 2. Laplace and the last layer: a local posterior at a low price

Daxberger et al. (2021) build Laplace Redux: take a MAP, approximate the posterior with a Gaussian from the Hessian (or proxies), and turn a trained network into a Bayesian model with few code changes. Harrison, Willes and Snoek (2024) turn the Bayesian last layer into a deterministic variational loss, with no sampling needed, at a cost that grows only with the square of the last-layer dimension. The generative story is deliberately shrunk: the features are treated as already learned, and the remaining uncertainty lives in the readout layer. That is regularization in the form of a distribution over the decision hyperplane.

### 3. Do we need a fully stochastic Bayesian network?

Sharma, Farquhar, Nalisnick and Rainforth (2023) ask a very Chapter-7 question: is full stochasticity the only way to avoid overfitting and to have a rich predictive distribution? They prove that networks that are only partly stochastic are still universal approximators for conditional distributions, and experimentally find no systematic benefit from making every weight stochastic. Bias–variance here is the cost of memory and the honesty of inference, not only prediction error. The feature selection of Lesson 7.3 reappears in the form of choosing *which layer* receives a prior.

### 4. Deep ensembles as a practical Bayesian approximation

Deep ensembles—training a few networks from different initializations—remain a strong uncertainty baseline in industry. Wilson and Izmailov have argued that they approximate a mixture over the modes of the posterior. They do not replace the MCMC of Izmailov et al. (2021), but they are how products “buy” posterior diversity when HMC cannot run. Reading an ensemble as several MAPs under an implicit prior, then averaging the predictions, keeps the true spirit of Chapter 7: reduce variance by not trusting a single point.

## Interpretation and insight

A narrow Laplace interval around the MAP can miss other modes. A confident last-layer Bayes remains blind if the features have collapsed. A consensus ensemble does not mean the data has proven the hypothesis; the members may share the same systematic error. The prior has done its job when the model *refuses* to go too far in sparse regions, not when its confidence is always high.

## Applications

Tabular scoring, out-of-distribution detection, and the uncertainty of classification networks are three places where Bayesian regularization has become a deployed technique, no longer a metaphor.

## Limitations and extensions

Laplace is local. VBLL assumes a linear last layer on fixed features. Ensembles multiply the training cost. No method removes the need for model checking in Chapter 8. This lesson deliberately does not open a separate deep learning chapter; it only shows that the prior of Lesson 7.1 has entered modern networks through narrow doors.

## Reference videos

- [The Bayesian interpretation of weight decay 43 Machine Learning](https://www.youtube.com/watch?v=RckG_kNv1Kc) — Professor tutorials, English. **watch first**. Watch weight decay read as a prior on the weights, exactly the bridge the lesson draws from regularization to neural networks.
- [Uncertainty estimation and Bayesian Neural Networks - Marcin Możejko](https://www.youtube.com/watch?v=dj-FKXxy7HQ) — PyData, English. Watch uncertainty estimation with a Bayesian neural network, supporting the part on overly flexible models needing a prior.
- [MIT 6.S191: Uncertainty in Deep Learning](https://www.youtube.com/watch?v=veYq6EWZyVc) — Alexander Amini, English. Watch the ways deep learning reports uncertainty, including the ensemble family, used for the part of the lesson on deep ensembles.

## Exercises

1. Rewrite weight decay as a prior. If you decrease $$\tau$$, what are you declaring about the data-generating function, and what kind of bias do you accept?
2. A team places Bayes only on the last layer because it is “cheap”. Based on Sharma et al. (2023), argue when that is enough and when fixed features will hide uncertainty.
3. Compare a horseshoe on twenty predictors with dropout on a network. What is being shrunk, and what is hidden as an optimization trick?
4. Laplace Redux uses the Hessian at the MAP. Describe in words a two-mode posterior and say what that approximation would miss.

## References

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 14–15.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 17–18.
- Daxberger, E., et al. (2021). Laplace Redux — effortless Bayesian deep learning. *NeurIPS*.
- Harrison, J., Willes, J., & Snoek, J. (2024). Variational Bayesian last layers. *ICLR*. [arXiv:2404.11599](https://arxiv.org/abs/2404.11599).
- Sharma, M., Farquhar, S., Nalisnick, E., & Rainforth, T. (2023). Do Bayesian neural networks need to be fully stochastic? *AISTATS*. [arXiv:2211.06291](https://arxiv.org/abs/2211.06291).
- Izmailov, P., Vikram, S., Hoffman, M. D., & Wilson, A. G. (2021). What are Bayesian neural network posteriors really like? *ICML*.
