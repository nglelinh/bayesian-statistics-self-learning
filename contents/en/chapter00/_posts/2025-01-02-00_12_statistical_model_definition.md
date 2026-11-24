---
layout: post
title: "Lesson 0.14: What is a Statistical Model?"
chapter: '00'
order: 14
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

What actually *is* a statistical model? It is not a black-box `model.fit()` call—it is a **mathematical story of how your data could have been generated!** In Bayesian statistics, writing down a statistical model means specifying two clean ingredients: a **data-generating process** $$p(y\mid	heta)$$ (how observable measurements emerge given hidden parameters) and a **prior** $$p(	heta)$$ (what parameter values are plausible before seeing data).

This lesson teaches you to read and write generative statistical models fluently, separate **parameters** from **data** and **hyperparameters**, and simulate synthetic data forward before ever fitting real observations.

---

## Background Knowledge Map: The Anatomy of a Generative Statistical Model

Four elements define every Bayesian statistical model you will build in this course:

1. **Data-Generating Story (Likelihood $$p(y\mid	heta)$$):** A family of probability distributions indexed by unknown parameter(s) $$	heta$$ describing how noise and signal combine to produce observations $$y$$.
2. **Prior Distribution $$p(	heta\mid\phi)$$:** Encodes domain constraints and plausible scales for $$	heta$$, controlled by fixed **hyperparameters** $$\phi$$ (or learned hyperpriors in hierarchical models).
3. **Forward Simulation (Prior Predictive):** Because a Bayesian model is fully generative, you can sample $$	heta \sim p(	heta)$$ and then $$y_{	ext{sim}} \sim p(y\mid	heta)$$ *before* touching real data—catching absurd priors immediately (like predicting negative human heights!).
4. **All Models Are Wrong, Some Are Useful (George Box):** A statistical model is a deliberate simplification; its value is judged by how well it explains observed structure, quantifies uncertainty, and predicts new observations.

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

### 6.1) A very short example: same data idea, different model story

Suppose the data are not heights but the number of support calls arriving each hour: $$0, 1, 3, 2, 4, \dots$$. For this kind of data, a Poisson model usually tells a more sensible story because it respects the counting structure and only produces nonnegative predictions. If we force a Normal model onto the same setting, we may still get a mean and a variance, but the model also quietly allows negative predicted counts that make no practical sense.

The key point is that choosing a model is not just choosing a convenient formula. It is choosing a story about how the data are generated, and that story determines which conclusions become reasonable.

## Quick recap

1. A statistical model is a family $$\{p(x\mid\theta)\}$$ for data.
2. It links unknown parameters to observed data via a generative mechanism.
3. Every model carries assumptions; understanding assumptions is central.
4. In Bayes, the model provides the likelihood that updates prior to posterior.

---

### Worked Numerical Example: Checking a Generative Normal Model via Prior Predictive Variance

Suppose you model exam scores $$Y$$ with known measurement noise $$\sigma = 10$$ and an uncertain class mean $$\mu$$:

$$\mu \sim \mathcal{N}(70,\; 5^2), \qquad Y \mid \mu \sim \mathcal{N}(\mu,\; 10^2).$$

What distribution does a single *future* score $$Y$$ follow before seeing any data (**Prior Predictive**)? Write $$Y = \mu + arepsilon$$ where $$\mu \sim \mathcal{N}(70, 25)$$ and $$arepsilon \sim \mathcal{N}(0, 100)$$ are independent:
1. **Prior predictive mean:** $$\mathbb{E}[Y] = 70 + 0 = 70$$.
2. **Prior predictive variance (variances of independent sources add!):**
   $$\mathrm{Var}(Y) = \mathrm{Var}(\mu) + \mathrm{Var}(arepsilon) = 5^2 + 10^2 = 25 + 100 = 125 \implies \mathrm{SD}(Y) = \sqrt{125} pprox \mathbf{11.18}.$$
3. **95% Prior Predictive Range:** $$70 \pm 1.96(11.18) = [48.1,\; 91.9]$$—completely sensible for a 0–100 exam! *(Whereas a lazy "flat" prior $$\mu \sim \mathcal{N}(70, 1000^2)$$ would predict exam scores from $$-1890$$ to $$+2030$$!)*

### Deep-Dive Explanation: Four Rules for Specifying Clean Statistical Models (Read Slowly)

1. **Always write the model in mathematical notation before writing code:** Two lines like $$\mu \sim \mathcal{N}(70, 5^2); \; y_i \mid \mu \sim \mathcal{N}(\mu, 10^2)$$ clarify every assumption in seconds.
2. **Distinguish epistemic uncertainty (about $$	heta$$) from aleatoric noise (about $$Y\mid	heta$$):** Collecting more data shrinks $$\mathrm{Var}(\mu\mid y) 	o 0$$, but never shrinks $$\sigma^2 = 100$$.
3. **Run prior predictive checks on every new model:** Simulating fake datasets from your prior instantly flags scale mistakes before you waste time running MCMC.
4. **Start simple and expand iteratively:** Begin with a minimal baseline model (e.g., Normal or Binomial), check where its predictions fail real data, and only then add hierarchy or heavy tails.

**Quick check.** In the exam model above, if you knew the class mean $$\mu = 70$$ with 100% certainty ($$\mathrm{SD}(\mu) = 0$$), what would the predictive standard deviation of a new student’s score $$Y$$ be?

---

## Reference videos

- [What is a statistical model?](https://www.youtube.com/watch?v=3d5ivs_8amQ) — Very Normal, English. **watch first**. Watch a statistical model defined as a probability story for how data are generated, the practical definition in this lesson.
- [Statistical Rethinking 2023 - 01 - The Golem of Prague](https://www.youtube.com/watch?v=FdnMWdICdRs) — Richard McElreath, English. Watch the argument that a model is a tool that must be supervised, supporting the lesson's focus on assumptions.
- [Regression and Other Stories: Generative models and statistical inference (ros02 4)](https://www.youtube.com/watch?v=kn8fyNzvcPo) — Data Science Learning Community Videos, English. Watch generative models set next to statistical inference, useful for separating observed data from unknown parameters.

## Exercises

1. For the coin example, list three implicit assumptions of the binomial model.
2. Give one context where the independence assumption is likely violated.
3. Explain in your own words: "A model is a map, not the territory."

## References

- McElreath, R. (2020). *Statistical Rethinking* (2nd ed.). CRC Press.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Wasserman, L. (2004). *All of Statistics*. Springer.
