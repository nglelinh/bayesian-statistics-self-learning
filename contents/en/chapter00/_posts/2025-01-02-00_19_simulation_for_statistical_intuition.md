---
layout: post
title: "Lesson 0.21: Simulation to Test Statistical Intuition"
chapter: '00'
order: 21
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

Whenever a probability puzzle or Bayesian model makes your head spin, stop staring at integrals and **simulate it 10,000 times in 5 lines of Python!** Simulation is the ultimate truth serum of modern statistics: it lets you verify algebraic formulas in seconds, test whether an estimator actually recovers ground-truth parameters (*Simulation-Based Calibration*), and see how prior choices behave before you ever touch real data.

This lesson turns forward simulation into an everyday Bayesian habit—showing how to generate synthetic worlds from a known truth, test your inference code on them, and build unshakable intuition.

---

## Key ideas: Four Ways Simulation Supercharges Bayesian Workflow

In modern Bayesian data analysis (Gelman’s Bayesian Workflow), simulation is not a toy—it is a core validation tool:

1. **Prior Predictive Simulation:** Sample $$	heta^{(s)} \sim p(	heta)$$, then $$y^{(s)} \sim p(y\mid	heta^{(s)})$$. Instantly reveals whether your prior implies physically plausible data!
2. **Parameter Recovery Testing:** Fix a known ground truth $$	heta_{	ext{true}}$$, simulate fake data $$y_{	ext{sim}}$$, fit your Bayesian model to $$y_{	ext{sim}}$$, and verify that the 95% credible interval recovers $$	heta_{	ext{true}}$$—catching coding bugs *before* analyzing real data!
3. **Empirical Verification of Coverage & Power:** Repeat simulation 1,000 times to measure true Type I error, credible interval coverage, or sample size needed to achieve desired posterior precision.
4. **Posterior Predictive Checks (PPC):** Draw $$y^{	ext{rep}} \sim p(y\mid	heta^{(s)})$$ from posterior draws $$	heta^{(s)}$$ and compare simulated datasets against your real observed dataset.

---

## Learning objectives

After this lesson, you will see simulation as an inference tool and not just an illustration, know how to use simulation to check formulas, detect misunderstood intuitions, and prepare well for a Bayesian workflow based on the generative story.

## Introduction: simulation as the laboratory of inference

In many probability problems, verbal intuition easily leads to wrong conclusions, while closed-form formulas are sometimes hard to check quickly in a real context. Simulation provides an intermediate "laboratory": we state an assumption, generate data according to that assumption, and then compare the consequences with what we believe to be true. This approach helps learning go deeper because it forces us to tie the theoretical model closely to the behavior of observed data.

![Quy trinh mo phong thong ke]({{ site.baseurl }}/img/chapter_img/chapter00/simulation_statistical_intuition_workflow.png)

*How to read the figure: This figure illustrates the statistical simulation workflow. Read the axis labels/legend first, then compare the main trend across the lines, bars or groups of points instead of looking only at individual points.*
*Figure 1: The 4-step simulation workflow: model assumptions -> set parameters -> generate data -> compare and update.*

## 1) Why do we need simulation?

Many statistical problems are hard because intuition is easily wrong:

We may confuse conditional probabilities, misjudge the level of uncertainty, or believe a "nice" result without checking the data-generating mechanism behind it.

Simulation lets us look directly at the consequences of assumptions.

## 2) The 4-step simulation workflow

1. State the data-generating mechanism clearly (generative story).
2. Choose reasonable input parameters.
3. Generate data repeatedly.
4. Summarize the results and compare with the theoretical expectation.

If the simulation result contradicts intuition, it is usually our intuition that needs correcting.

## 3) When should we simulate?

Simulation is especially useful when a formula is too complicated or hard to check by hand, when we want to check sensitivity to parameters, when we need to teach or learn a probability concept visually, or when we need a sanity check for Bayesian inference code.

## 4) A short example

To understand the uncertainty interval of a proportion $$p$$ when $$n$$ is small:

We can assume the true value $$p=0.2$$, simulate many Binomial samples with $$n=20$$ and $$n=200$$, and then compare the fluctuation of $$\hat p$$ between those two settings.

You will see right away why small data fluctuates a lot and why the prior can matter in settings with little data.

### 4.1) If we look at 5 concrete simulation runs, what will we see?

With the same true value $$p=0.2$$, a typical simulation result might look as follows:

- If $$n=20$$: $$\hat p = 0.10, 0.15, 0.20, 0.30, 0.35$$
- If $$n=200$$: $$\hat p = 0.17, 0.19, 0.20, 0.22, 0.24$$

Both groups revolve around the true value 0.2, but the $$n=20$$ group fluctuates much more widely. Just by looking at a few such simulation runs, we already have a very clear intuition for why little data usually makes conclusions less stable.

## 5) Direct connection to Bayes

Simulation is the "laboratory" of the Bayesian workflow:

It lets us check the prior predictive, the posterior predictive, and also the stability of decisions when the input assumptions change.

In other words, simulation helps us learn the "model implies data" way of thinking.

## Quick summary

1. Simulation is an inference tool, not just an illustration.
2. The standard workflow: assumptions -> generate data -> repeat -> summarize.
3. Simulation is especially useful for sanity checking Bayesian models.
4. When intuition and simulation conflict, trust the simulated data first and then re-examine the assumptions.

---

### Worked Numerical Example: Tracing a 5-Draw Prior Predictive Check by Hand

Suppose your model for 10 user visits is $$	heta \sim \mathrm{Beta}(2, 8)$$ (prior mean $$0.20$$) and $$y \mid 	heta \sim \mathrm{Binomial}(10, 	heta)$$. Trace 5 simulated worlds step by step:

| Simulation $$s$$ | Drawn Prior $$	heta^{(s)} \sim \mathrm{Beta}(2,8)$$ | Simulated Clicks $$y^{(s)} \sim \mathrm{Bin}(10, 	heta^{(s)})$$ |
| :--- | :--- | :--- |
| 1 | $$0.12$$ | $$1$$ |
| 2 | $$0.28$$ | $$3$$ |
| 3 | $$0.09$$ | $$0$$ |
| 4 | $$0.35$$ | $$4$$ |
| 5 | $$0.18$$ | $$2$$ |

From these simulated worlds, average simulated clicks $$pprox 2.0$$ (matching $$\mathbb{E}[y] = 10 	imes 0.20 = 2.0$$), and typical counts sit in $$[0, 5]$$. If your real domain routinely sees 8–9 clicks out of 10, this 5-second simulation immediately warns you that $$\mathrm{Beta}(2,8)$$ is far too pessimistic!

### Explanation: Four Rules for Reliable Statistical Simulations

1. **Always test your inference code on simulated data with known $$	heta_{	ext{true}}$$ first:** If your sampler cannot recover $$	heta_{	ext{true}} = 0.65$$ from 500 clean simulated coin flips, never trust it on messy real-world data!
2. **Check Monte Carlo error of your simulation itself:** Running only 50 repetitions has $$\mathrm{SE} pprox 7\%$$ for a coverage rate; use $$1{,}000	ext{–}10{,}000$$ vectorized repetitions for crisp answers.
3. **Simulate the *exact* messy features of your real data:** Include missing values, rounding, outliers, or group clustering in your simulator to see whether your model breaks gracefully or catastrophically.
4. **Set explicit random seeds (`default_rng(123)`):** Reproducible simulations make debugging effortless.

**Quick check.** If you run 1,000 independent parameter-recovery simulations of a well-calibrated 95% credible interval (drawing $$	heta_{	ext{true}}$$ from the prior each time), roughly how many of the 1,000 intervals should contain $$	heta_{	ext{true}}$$?

---

## Reference videos

- [What is Monte Carlo Simulation?](https://www.youtube.com/watch?v=7TqhmX92P6U) — IBM Technology, English. **watch first**. Watch Monte Carlo simulation as a way of stating an assumption and then generating data under that assumption, exactly the role the lesson assigns to simulation.
- [Law of Large Numbers - Explained and Visualized](https://www.youtube.com/watch?v=MntX3zWNWec) — Jeremy Blitz-Jones, English. Watch a theorem being checked with a simulated plot, supporting the part about using simulation to detect wrong intuition.
- [But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo) — 3Blue1Brown, English. Watch many samples generated to see the distribution of the mean, used as a template for the data-generating workflow in the lesson.

## Practice questions

1. Name a probability concept that you often misunderstand and propose a simulation to check it.
2. Why is simulation a good bridge between math and code?
3. When a simulation gives a surprising result, what should you check first?

## References

- Downey, A. (2014). *Think Bayes*.
- McElreath, R. (2020). *Statistical Rethinking*.

---

*Next lesson: [Chapter 1: Fundamentals of Bayesian Inference]({{ site.baseurl }}/contents/en/chapter01/)*
