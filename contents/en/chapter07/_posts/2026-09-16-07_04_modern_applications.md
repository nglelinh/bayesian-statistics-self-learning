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

A standard deep neural network classifying chest X-rays can be **99.8% confident** even when you accidentally feed it a blurry photo of a golden retriever! Why? Because ordinary neural nets fit a single point estimate (MAP via weight decay = Gaussian prior!) and throw away the entire posterior distribution over weights. **Bayesian Deep Learning (BDL)** restores honest epistemic uncertainty to modern neural networks—using scalable approximations like **Deep Ensembles**, **MC Dropout**, **Last-Layer Laplace**, and **SWAG**!

This optional bridge links Chapter 7’s priors and regularization directly to 2022–2026 production deep learning: showing how weight decay *is* a Gaussian prior, and how ensembling turns neural nets into uncertainty-aware systems that know when to say *"I don’t know—escalate to a human!"*

---

## Key ideas: Four Practical Approximations to Bayesian Deep Learning

1. **Weight Decay = Gaussian Prior MAP:** Standard `AdamW` weight decay is literally placing $$\mathbf{w} \sim \mathcal{N}(\mathbf{0}, \tau^2 I)$$ and keeping only the single peak—fast, yet blind to posterior width!
2. **Last-Layer Laplace Approximation:** Freezes the deep feature backbone and computes the exact Hessian covariance $$(-\mathbf{H})^{-1}$$ only on the final linear layer—adding calibrated Bayesian uncertainty in seconds with zero retraining!
3. **MC Dropout (Gal & Ghahramani):** Leaves dropout masks *active* at test time and runs $$M$$ stochastic forward passes—approximating variational Bayesian inference cheaply.
4. **Deep Ensembles (Lakshminarayanan et al.):** Trains $$M = 5$$ independent networks from different random initializations; their disagreement across predictions is one of the strongest empirical detectors of **Out-of-Distribution (OOD)** inputs!

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

---

### Worked Numerical Example: Detecting an Out-of-Distribution Input With a 4-Model Deep Ensemble

Suppose 4 independently trained ensemble networks predict the probability of pneumonia on two test images:
- **In-Distribution Chest X-Ray:** `[0.82, 0.85, 0.79, 0.86]`
  - Mean prediction: $$\bar{p} = \mathbf{0.830}$$; Ensemble SD (epistemic disagreement): $$\mathbf{0.032}$$ (tight consensus $$\implies$$ trust!).
- **Out-of-Distribution Blurry Non-X-Ray Image:** `[0.91, 0.12, 0.65, 0.30]`
  - Mean prediction: $$\bar{p} = \mathbf{0.495}$$; Ensemble SD: **$$0.354$$** (**11× wider epistemic disagreement** $$\implies$$ flag for human doctor review!).

### Explanation: Four Takeaways on Bayesian Deep Learning in Practice

1. **You don’t need full HMC over 100 million weights to get Bayesian benefits:** A 5-model Deep Ensemble or a Last-Layer Laplace head captures 90% of practical OOD detection and calibration gains at tiny cost.
2. **Separate *epistemic* (model disagreement) from *aleatoric* (inherent data noise):** High epistemic variance means *"show this to a human and label it for the next training round"* (Active Learning!).
3. **Check Expected Calibration Error (ECE) on shifted test sets:** Standard nets look calibrated on i.i.d. validation sets and fall apart under real-world distribution shift—where Bayesian methods shine brightest.
4. **Pair BDL uncertainty with abstention thresholds:** Allowing a medical or autonomous system to abstain on the top 5% most uncertain inputs often cuts real-world errors by 50%+!

**Quick check.** In the 4-model ensemble example above, why does a single network with `p = 0.91` fail to warn the hospital about the blurry OOD image, whereas the 4-model ensemble catches it immediately?

---

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
