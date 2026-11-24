---
layout: post
title: "Lesson 4.7: Modern MCMC — NUTS, HMC and Bayesian Regression in Practice"
chapter: '04'
order: 8
owner: Nguyen Le Linh
lang: en
categories:
- chapter04
lesson_type: optional
---

Why did Bayesian statistics explode from a niche academic corner into the backbone of modern scientific modeling, epidemiology, and probabilistic ML over the past decade? The turning point was not a new theorem—it was a physics-inspired sampler called **Hamiltonian Monte Carlo (HMC)** and its self-tuning heir, **NUTS** (the No-U-Turn Sampler). By treating the negative log-posterior as a frictionless landscape and rolling a marble across it using exact gradients, NUTS turns high-dimensional posteriors that once took weeks into seconds—and even sounds an alarm (**divergent transitions**) whenever the geometry gets treacherous.

**Lesson Roadmap:** How physics revolutionized Bayesian computation → Background Knowledge Map (Hamiltonian dynamics & leapfrog integration, NUTS adaptive trajectory length, Divergences as geometric alarms) → Hand-worked 1-step leapfrog integration conserving energy → Modern applications, limitations, and exercises.

## Learning objectives

After this optional lesson, you understand that Hamiltonian Monte Carlo and NUTS are not decorative algorithms added after Bayesian linear regression, but an inevitable consequence once the posterior no longer has a closed form. You will be able to read a Stan, PyMC or NumPyro chain as a controlled approximation of the same generative model that Chapter 4 wrote in words.

## Background Knowledge Map: Why HMC and NUTS Power Modern Bayesian Practice

### 1. Hamiltonian Dynamics and Symplectic (Leapfrog) Integration
- **What it is:** Augmenting parameter position $$q$$ with an auxiliary momentum $$p \sim \mathrm{Normal}(0, M)$$ and simulating Hamilton's equations for total energy $$H(q, p) = U(q) + K(p)$$, where potential energy $$U(q) = -\log \tilde{\pi}(q)$$.
- **What it studies:** Proposing distant, nearly independent points across a high-dimensional posterior with acceptance rates near $$80\%\text{–}99\%$$ because symplectic leapfrog steps nearly conserve total energy $$H$$.

### 2. The No-U-Turn Sampler (NUTS)
- **What it is:** Hoffman & Gelman's (2014) recursive tree-building extension of HMC that automatically stops integrating the moment the trajectory begins to U-turn back toward its starting point.
- **What it studies:** Eliminating manual tuning of trajectory length $$L$$ (and adapting step size $$\varepsilon$$ + mass matrix $$M$$ during warmup), powering Stan, PyMC, and NumPyro.

### 3. Divergent Transitions as Built-In Geometry Detectors
- **What it is:** Steps where the leapfrog integrator's energy error $$\vert \Delta H \vert$$ blows up because curvature changes faster than step size $$\varepsilon$$ (such as Neal's funnel in hierarchical models).
- **What it studies:** Turning numerical failure into an actionable diagnostic—unlike random-walk MH, which silently misses narrow funnels without warning.

## Deep-Dive Explanation: One Leapfrog Step of HMC by Hand (Read Slowly)

Take the 1D standard normal posterior $$\tilde{\pi}(q) = e^{-q^2/2}$$, so potential energy is $$U(q) = \frac{1}{2}q^2$$ (gradient $$\nabla U(q) = q$$) and kinetic energy is $$K(p) = \frac{1}{2}p^2$$. Start at position $$q_0 = 1.0$$ with momentum $$p_0 = 0.0$$, giving initial energy:
$$ H_0 = U(1.0) + K(0.0) = \frac{1.0^2}{2} + 0 = \mathbf{0.5000}. $$
Now take **one leapfrog step** with a huge step size $$\varepsilon = 0.5$$:

1. **Half-step momentum:** $$p_{1/2} = p_0 - \frac{\varepsilon}{2}\nabla U(q_0) = 0 - 0.25(1.0) = \mathbf{-0.25}.$$
2. **Full-step position:** $$q_1 = q_0 + \varepsilon\,p_{1/2} = 1.0 + 0.5(-0.25) = \mathbf{0.875}.$$
3. **Half-step momentum:** $$p_1 = p_{1/2} - \frac{\varepsilon}{2}\nabla U(q_1) = -0.25 - 0.25(0.875) = \mathbf{-0.46875}.$$
4. **Check energy conservation:**
   $$ H_1 = \frac{0.875^2}{2} + \frac{(-0.46875)^2}{2} = 0.38281 + 0.10986 = \mathbf{0.49268}. $$
   Energy drift is a tiny $$\Delta H = H_1 - H_0 = -0.00732$$, so the Metropolis acceptance probability is $$\min(1, e^{-\Delta H}) = \mathbf{1.000}$$! Even with a coarse step $$\varepsilon = 0.5$$, the leapfrog integrator glides smoothly toward the high-probability region while conserving energy to within $$1.5\%$$.

## Prerequisites

Lessons 4.1–4.6 built linear regression as a generative story, chose priors, and obtained the posterior with PyMC. Lesson 4.2b covered MCMC at the level of classroom theory. This lesson does not rewrite Metropolis. It asks what modern samplers are doing in 2022–2026 systems, and why linear regression is still the most-sampled model.

## Introduction

Once a model has an intercept, a slope, a variance, and a few predictors, the prior–likelihood product can no longer be integrated by hand. The grid of Chapter 2 explodes in the number of cells. Exact theory therefore becomes insufficient, not because the Bayesian idea has weakened, but because the geometry of the posterior has outgrown the paper. The tension of this lesson is: if we cannot draw the posterior, can we still trust the sequence of numbers the machine returns?

## Conceptual development

Hamiltonian Monte Carlo uses the gradient of the log-posterior to propose long moves that are still accepted. NUTS (No-U-Turn Sampler) stops the trajectory when it begins to turn back, so the user does not have to choose the trajectory length by hand. What the sampler approximates is the expectation under the posterior,

$$
\mathbb E[g(\theta)\mid y]\approx\frac{1}{S}\sum_{s=1}^{S}g(\theta^{(s)}),\qquad \theta^{(s)}\sim p(\theta\mid y),
$$

the same object that Bayesian regression uses for coefficients, for predictions, and for posterior intervals. The software does not replace the model; it replaces the scratch paper.

## Models as generative stories

### 1. NUTS in Stan, PyMC and NumPyro for hierarchical regression

The generative story is still: parameters ~ prior, data ~ normal around a plane. The industrial difference is that this plane has an intercept by country, by campaign, or by server. The Stan User’s Guide and the PyMC/NumPyro notebooks all take NUTS as the default because the gradient of the log-density can be obtained by automatic differentiation. When you read a credible interval for an advertising coefficient, you are reading a summary of a NUTS chain, not an OLS formula.

### 2. Pathfinder as a warm start, not a replacement for MCMC

Zhang, Carpenter, Gelman and Vehtari (2022) propose Pathfinder: follow a quasi-Newton optimization path, place Gaussian approximations along the path, and then sample from the approximation with the smallest KL. On many posteriors, those samples are better than ADVI and cheaper than a short HMC chain, so Stan and JAX libraries use Pathfinder to initialize NUTS. The pedagogical meaning fits Chapter 4 exactly. Variational inference appears because MCMC needs a good place to stand, not because the posterior has been replaced by an optimization.

### 3. BlackJAX and composable MCMC on accelerators

Cabezas et al. (2024) describe BlackJAX as a box of statistical atoms—Metropolis steps, Hamiltonian dynamics, Langevin mechanisms—written in JAX to compile onto GPUs and TPUs. Bayesian regression is then no longer "one chain on a laptop", but the same log-density running thousands of chains in parallel. The generative story does not change; the compute budget does.

### 4. MCMC for Bayesian neural networks

Izmailov, Vikram, Hoffman and Wilson (2021) ask what the posterior of a Bayesian neural network looks like if we really run expensive HMC, instead of immediately trusting dropout or a diagonal Gaussian. They find that popular approximations often fail to reproduce the full posterior, but predictions can still be useful. The lesson for linear regression students is humble and sharp: if HMC is already hard to read on a few dozen correlated coefficients, then "MCMC for deep learning" is the same geometric problem, only bigger. Chapter 7 will meet cheaper approximations again.

## Interpretation and insight

A posterior interval from NUTS is only trustworthy if the chain has mixed and the model is not grossly wrong. $$\hat R$$ near 1 does not prove the plane is causal. Pathfinder can sit at a minor mode and make NUTS start in the wrong place. A fast BlackJAX does not make the prior harmless. Read the sampler as a magnifying glass: it magnifies exactly the model you wrote, including the Gaussian assumptions about the residuals.

## Applications

Bayesian linear regression is the backbone of media mix, pricing, and hierarchical models in A/B testing. Modern MCMC is why those models can carry real priors and still produce a usable posterior, instead of stopping at point estimates.

## Limitations and extensions

HMC needs a differentiable log-density; discrete data with discrete parameters must take another route. Large models still need VI, Laplace, or ensembles. This lesson deliberately does not reopen Markov chain theory. Chapter 5 will make the posterior harder by adding many predictors and causal structure.

## Reference videos

- [The intuition behind the Hamiltonian Monte Carlo algorithm](https://www.youtube.com/watch?v=a-wydhEuAm0) — Ben Lambert, English. **watch first**. Watch the HMC intuition before reading NUTS as a way to choose the trajectory length, exactly the step where the lesson moves from Metropolis to modern samplers.
- [Michael Betancourt: Scalable Bayesian Inference with Hamiltonian Monte Carlo](https://www.youtube.com/watch?v=jUSZboSq1zg) — London Machine Learning Meetup, English. Watch Michael Betancourt present large-scale Bayesian inference with Hamiltonian Monte Carlo.
- [#78 Exploring MCMC Sampler Algorithms, with Matt D. Hoffman](https://www.youtube.com/watch?v=KVpAziPblks) — Learning Bayesian Statistics, English. Watch Matt Hoffman, co-author of NUTS, discuss MCMC samplers, supporting the part of the lesson that reads a PyMC or Stan chain as a controlled approximation.

## Exercises

1. A colleague says "PyMC has converged because the trace looks fine". Which two more diagnostics would you ask for, and which geometric assumption is each checking?
2. Explain, without code, why Pathfinder can be both variational inference and part of an MCMC workflow.
3. In a house-price regression with heavy-tailed errors, NUTS still runs. Which model is the posterior approximating, and what will the PPC expose?
4. Read the NUTS page of Stan or NumPyro. Point to one sentence in the documentation about the *target log density*. Which mathematical object of lesson 4.1 does that sentence correspond to?

## References

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 11–12.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 7, 17.
- Zhang, L., Carpenter, B., Gelman, A., & Vehtari, A. (2022). Pathfinder: Parallel quasi-Newton variational inference. *JMLR*, 23(306). [arXiv:2108.03782](https://arxiv.org/abs/2108.03782).
- Cabezas, A., Corenflos, A., Lao, J., Louf, R., et al. (2024). BlackJAX: Composable Bayesian inference in JAX. [arXiv:2402.10797](https://arxiv.org/abs/2402.10797).
- Izmailov, P., Vikram, S., Hoffman, M. D., & Wilson, A. G. (2021). What are Bayesian neural network posteriors really like? *ICML*.
- [Stan HMC/NUTS](https://mc-stan.org/docs/reference-manual/mcmc.html).
- [NumPyro inference](https://num.pyro.ai/en/stable/mcmc.html).
- [PyMC sampling](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html).
