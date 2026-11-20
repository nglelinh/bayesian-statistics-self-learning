---
layout: post
title: "Lesson 8.5: Modern Applications of Model Checking and Bayesian Decision-Making"
chapter: '08'
order: 5
owner: Nguyen Le Linh
lang: en
categories:
- chapter08
lesson_type: optional
---

## Learning objectives

After this optional lesson, you will see PPC, LOO/WAIC and decision analysis as a production workflow, not as an "appendix chapter after the fit". You will connect posterior checks with simulation-based calibration, model comparison with the uncertainty of the LOO difference itself, and the Bayes action rule with Bayesian optimization and bandits.

## Prerequisites

Lessons 8.1–8.4 built PPC, information criteria, model comparison, and decisions under loss. This lesson does not redefine ELPD. It shows how those objects are being tightened in 2022–2025 research and in optimization libraries.

## Introduction

Chapter 8 was written because of a bad habit: watching the MCMC chains converge and stopping. In computer science, that habit turns into a green dashboard. A sampler can draw the right samples from the wrong model, or the wrong samples from the right model. A difference $$\Delta\mathrm{ELPD}$$ can change sign once you recompute its error. The tension of this lesson is to separate three questions that products tend to mix: can the model generate data of this kind, which model predicts better under the uncertainty of the comparison itself, and what should we *do*?

## Conceptual development

PPC asks whether $$y^{\mathrm{rep}}$$ generated from $$p(y\mid\theta)$$ with $$\theta\sim p(\theta\mid y)$$ reproduces the structure of $$y$$. LOO estimates the expected log predictive density at a new point. Decision theory chooses

$$
a^*(y)=\arg\min_a\int L(a,\theta)\,p(\theta\mid y)\,d\theta.
$$

These three objects do not replace each other. A model that wins on LOO can still fail PPC in the tail. An optimal action can choose a model that is *worse in log score* if the loss is asymmetric.

## Models as generative stories

### 1. Simulation-based calibration as a check of software and inference

Modrák et al. (2025) tighten simulation-based calibration: draw $$\theta$$ from the prior, generate $$y$$, refit, then look at the rank of the test quantity in the posterior. They show that ranking only the parameters misses a whole class of errors—including the case where the posterior equals the prior—and that the likelihood is a sensitive test quantity as well. In industry, this is a unit test for a PyMC/Stan model before it enters an A/B test or pricing. The PPC of Lesson 8.1 checks the model on real data; SBC checks the *inference tool* on data generated from the model itself.

### 2. The uncertainty of the LOO comparison itself

Sivula, Magnusson, Matamoros and Vehtari (2025) show that the normal approximation of the LOO difference is often biased when two models predict similarly, when the model is misspecified, or when the sample is small. The skewness of the error may not vanish as $$n\to\infty$$ in some situations. The product consequence is very concrete: a model leaderboard must not be published as a hard ranking if the error of $$\Delta\mathrm{ELPD}$$ swallows the difference. Lesson 8.3 already said that comparison is a decision under model uncertainty; this paper measures that very uncertainty.

### 3. Bayesian optimization as decision theory on an expensive function

When $$\theta$$ is a hyperparameter configuration or a lab experiment, each evaluation $$f(\theta)$$ is very expensive. Bayesian optimization places a posterior—usually a Gaussian process—on $$f$$, then chooses the next point by minimizing expected loss, for example expected improvement. That is Lesson 8.4 written for a continuous action space. BoTorch (Balandat et al., 2020; the 2022–2026 ecosystem) turns this rule into Monte Carlo over the posterior, enough to optimize multiple objectives and constraints. AutoML is an application, not a new theory: choosing models and hyperparameters by Bayes action, not by a blind grid.

### 4. Bandits and adaptive experiments

Thompson sampling, which already appeared as a conjugate application in Chapter 2, is now read in its proper place: a sequential approximation of the Bayes action when the loss is regret. Content platforms, advertising, and adaptive clinical trials all update $$p(\theta\mid y)$$ and then choose an arm. The decision is not “reject $$H_0$$”; the decision is to continue, stop, or change the allocation ratio. PPC is still needed: if the model gets the tail of conversions wrong, the bandit will exploit a mirage.

## Interpretation and insight

A beautiful PPC does not grant a causal license. A LOO difference larger than two standard errors can still be a comparison between two models that are both misspecified. A high expected improvement does not mean the next point will be good; it means that *under the current posterior* the value of information exceeds the cost. Keep three layers of interpretation separate: criticism of the data generation, predictive comparison, and action.

## Applications

Testing models before production, choosing forecasting models for tables and for time series, tuning hyperparameters, and allocating experiments are the four faces of Chapter 8 in CS/DS today.

## Limitations and extensions

SBC requires many model fits. LOO assumes that the observations contribute in a nearly factorizable way. Bayesian optimization depends strongly on the prior over $$f$$ and will be naive if the noise is misunderstood. The course has no dedicated Gaussian process chapter, so this lesson uses the GP only as a posterior that serves decisions. If a later chapter opens up nonparametrics, you will see that the kernel of BO is exactly that model.

## Reference videos

- [#164 Bayesian Workflow, with Andrew Gelman, Aki Vehtari & Richard McElreath](https://www.youtube.com/watch?v=ysITaNRUQUU) — Learning Bayesian Statistics, English. **watch first**. Watch Andrew Gelman, Aki Vehtari and Richard McElreath discuss the Bayesian workflow, exactly how the lesson joins model checking with comparison and decision.
- [BITESIZE | Understanding Simulation-Based Calibration, with Teemu Säilynoja](https://www.youtube.com/watch?v=EC1bvP65rjs) — Learning Bayesian Statistics, English. Watch simulation-based calibration, supporting the part of the lesson that connects posterior predictive checks with checking the inference algorithm itself.
- [Uncertainty in Bayesian leave-one-out cross-validation based model comparison](https://www.youtube.com/watch?v=vLx6lUlZ0fc) — Aki Vehtari, English. Watch the uncertainty of LOO model comparison, used for the part of the lesson that does not read an ELPD difference as a hard ranking.

## Exercises

1. On a pricing model, distinguish a right-tail PPC failure from an SBC failure. Which one forces you to fix the *inference code*, and which one forces you to fix the *generative story*?
2. Two models have $$\Delta\mathrm{ELPD}=1.2$$ and an error of 1.5. Based on Sivula et al. (2025), what would you write on a slide for the product director?
3. Write the loss of a Bayesian optimization round when each experiment costs a fixed budget and you have five evaluations left. What is the action, and what is the state of the world?
4. A content bandit exploits a clickbait headline early. Which PPC would expose the reward model, and which decision rule would be more cautious than pure Thompson sampling?

## References

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 6–7, 9.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 10, 13.
- Modrák, M., et al. (2025). Simulation-based calibration checking for Bayesian computation. *Bayesian Analysis*, 20(2), 461–488. [arXiv:2211.02383](https://arxiv.org/abs/2211.02383).
- Sivula, T., Magnusson, M., Matamoros, A. A., & Vehtari, A. (2025). Uncertainty in Bayesian leave-one-out cross-validation based model comparison. *Bayesian Analysis*. [arXiv:2008.10296](https://arxiv.org/abs/2008.10296).
- Balandat, M., et al. (2020). BoTorch: A framework for efficient Monte-Carlo Bayesian optimization. *NeurIPS*. [arXiv:1910.06403](https://arxiv.org/abs/1910.06403).
- Russo, D., et al. (2018). A tutorial on Thompson sampling. *Foundations and Trends in Machine Learning*.
- [ArviZ posterior predictive checks](https://python.arviz.org/en/stable/api/generated/arviz.plot_ppc.html).
- [Stan Workflow / SBC notes](https://mc-stan.org/docs/stan-users-guide/posterior-predictive-checks.html).
