---
layout: post
title: "Lesson 0.16: The Law of Large Numbers and the Central Limit Theorem"
chapter: '00'
order: 16
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

When an MCMC sampler generates 4,000 posterior draws and reports that your posterior mean is `0.412`, how do you know that `0.412` is actually close to the true integral $$\int 	heta\,p(	heta\mid y)\,d	heta$$—and how many extra draws would it take to pin down one more decimal digit? Two twin theorems from probability theory answer both questions: the **Law of Large Numbers (LLN)** guarantees your sample average converges to the truth, and the **Central Limit Theorem (CLT)** tells you the exact speed of convergence: **$$O(1/\sqrt{S})$$**!

This lesson builds crystal-clear intuition for LLN and CLT—not just for real-world data collection, but as the exact mathematical warranty behind **Monte Carlo integration and MCMC sampling**.

---

## Key ideas: LLN and CLT as the Engine of Monte Carlo Bayes

Four concepts connect classical limit theorems directly to modern Bayesian computation:

1. **Law of Large Numbers (LLN):** As independent draws $$S 	o \infty$$, the sample mean $$ar{X}_S = rac{1}{S}\sum_{s=1}^S X^{(s)}$$ converges to $$\mu = \mathbb{E}[X]$$—guaranteeing that Monte Carlo expectations are consistent.
2. **Central Limit Theorem (CLT) & Monte Carlo Standard Error (MCSE):** For large $$S$$, $$ar{X}_S pprox \mathcal{N}\!\left(\mu,\; rac{\sigma^2}{S}
ight)$$, so the Monte Carlo standard error is $$\mathrm{MCSE} = rac{\sigma}{\sqrt{S}}$$!
3. **The 100× Cost of One Extra Decimal Digit:** Because error shrinks like $$1/\sqrt{S}$$, cutting MCSE by $$10	imes$$ requires **$$100	imes$$ as many samples**—explaining why efficient HMC/NUTS samplers beat crude random-walk samplers by orders of magnitude.
4. **Effective Sample Size (ESS) for Correlated MCMC Draws:** When draws are positively autocorrelated (as in MCMC), replace raw $$S$$ with the **Effective Sample Size $$S_{	ext{eff}}$$** in $$\mathrm{MCSE} = \sigma / \sqrt{S_{	ext{eff}}}$$!

---

## Learning objectives

After this lesson, you will understand why the sample mean stabilizes as the sample size grows (LLN), why the sum/mean of many random variables tends to be close to normal (CLT), and why these two theorems are the foundation for thinking about simulation, estimation, and testing.

## Introduction: why does randomness still produce stable regularities?

One of the foundational ideas of statistics is: each individual observation can be very noisy, but when we aggregate enough observations, we see a clear structure of regularity. The LLN and CLT are two theorems that describe exactly this phenomenon, and also explain why sample estimates can be used to make inferences about the population.

## 1) The Law of Large Numbers (LLN): the sample mean converges

Let $$X_1,\dots,X_n$$ be independent and identically distributed, with expectation $$\mu$$. The sample mean:

$$
\bar X_n = \frac{1}{n}\sum_{i=1}^n X_i
$$

The LLN says that as $$n\to\infty$$, $$\bar X_n$$ approaches $$\mu$$ (in probability).

Intuition: random noise "gradually cancels out" when averaging over many observations.

![The running mean gradually converges to the expectation]({{ site.baseurl }}/img/chapter_img/chapter00/lln_running_mean_convergence.png)

*Figure 1a: The law of large numbers shows the running mean gradually stabilizing and converging to the expected value as the number of observations increases.*

### Experiment: the law of large numbers

The running means of five simulated sequences converge to μ.

<div class="interactive-demo" markdown="1">
<div data-demo="clt-explainer" data-lang="en" data-tab="lln"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 2) The CLT: the distribution of the sample mean is close to normal

Under mild enough conditions, we have:

$$
\frac{\bar X_n-\mu}{\sigma/\sqrt{n}} \Rightarrow \mathcal N(0,1)
$$

Practical consequence:

$$
\bar X_n \approx \mathcal N\left(\mu,\frac{\sigma^2}{n}\right)
$$

even when the original distribution is not normal (n large enough).

![The distribution of the sample mean is close to normal]({{ site.baseurl }}/img/chapter_img/chapter00/clt_sample_means_histogram.png)

*Figure 1b: The central limit theorem shows that the distribution of the sample mean approaches a normal shape even though the original data is not necessarily normal.*

### Experiment: the central limit theorem

The histogram of the sample mean approaches a normal distribution as n increases, even though the original distribution is skewed.

<div class="interactive-demo" markdown="1">
<div data-demo="clt-explainer" data-lang="en" data-tab="clt"></div>
</div>

## 3) How do the LLN and CLT differ?

The **LLN** answers the question of whether the sample mean converges to the true value, while the **CLT** answers the question of what the rate and shape of the uncertainty around the true value look like. In other words, the LLN is the story of "where it converges to", and the CLT is the story of "how it fluctuates around the truth".

## 4) The connection to the standard error

From the CLT, the magnitude of the fluctuation of $$\bar X_n$$ is proportional to $$1/\sqrt{n}$$. This is why the standard error decreases slowly:

To cut the error by a factor of 2, we usually have to increase the sample size by about 4 times.

This is an important intuition when designing experiments and assessing the reliability of estimates.

### 4.1) A numerical example: what if we increase the sample 4 times?

Suppose we are estimating a true proportion around $$0.6$$. Then the standard error of the sample frequency is approximately:

$$
\mathrm{SE}(\hat p)\approx \sqrt{\frac{0.6\times 0.4}{n}}.
$$

- If $$n=25$$ then $$\mathrm{SE}\approx 0.098$$.
- If $$n=100$$ then $$\mathrm{SE}\approx 0.049$$.
- If $$n=400$$ then $$\mathrm{SE}\approx 0.024$$.

That is, when increasing the sample size from 25 to 100, and then from 100 to 400, the uncertainty falls by about half each time, rather than in the style of "doubling the data halves the error". This is a very direct way to remember why the LLN and CLT lead to the $$1/\sqrt{n}$$ law in practice.

## 5) The connection to Bayes and simulation

In Bayes, Monte Carlo estimates also rely on the idea of the sample mean: the more posterior samples there are, the more stable the estimate becomes, and many diagnostics about uncertainty are actually based on the intuition of the LLN and CLT.

## Quick summary

1. LLN: the sample mean converges to the true expectation when the sample size is large.
2. CLT: the distribution of the sample mean is close to normal with variance $$\sigma^2/n$$.
3. The LLN is about convergence; the CLT is about fluctuation around the point of convergence.
4. Both are foundations for statistical inference and simulation.

---

### Worked Numerical Example: Budgeting Monte Carlo Draws for Exact Posterior Precision

Suppose a posterior distribution for conversion rate $$	heta$$ has standard deviation $$\sigma = 0.10$$, and we estimate its posterior mean by averaging $$S$$ independent Monte Carlo draws:

| Independent Draws $$S$$ | $$\mathrm{MCSE} = 0.10 / \sqrt{S}$$ | 95% Monte Carlo Error Band ($$\pm 1.96\,\mathrm{MCSE}$$) | Reliable Decimal Places |
| :--- | :--- | :--- | :--- |
| $$S = 100$$ | $$0.0100$$ | $$\pm 0.0196$$ | ~1–2 digits (rough!) |
| $$S = 1{,}600$$ | $$0.0025$$ | $$\pm 0.0049$$ | 2 digits |
| $$S = 10{,}000$$ | $$0.0010$$ | $$\pm 0.0020$$ | ~3 digits |
| $$S = 1{,}000{,}000$$ | $$0.0001$$ | $$\pm 0.0002$$ | ~4 digits (100× more compute!) |

Now check what happens if an MCMC chain draws $$S = 10{,}000$$ correlated samples with an Effective Sample Size of only $$S_{	ext{eff}} = 400$$: its true MCSE is $$0.10 / \sqrt{400} = 0.0050$$—five times noisier than 10,000 independent draws!

### Explanation: Four Rules for Using LLN & CLT Wisely

1. **Always check MCSE in your Bayesian summary tables (`arviz.summary`):** A posterior mean of `0.412` with `mcse_mean = 0.001` is rock-solid; with `mcse_mean = 0.04`, you need more draws or a better sampler!
2. **LLN fails when the mean does not exist (Cauchy distribution!):** Averaging 10,000 draws from a Cauchy(0,1) distribution *never* settles down because occasional giant outliers reset the running mean.
3. **Tail quantiles need more draws than the mean:** Estimating the 95% credible interval boundary accurately requires higher tail ESS (`ess_tail`) than estimating the center (`ess_bulk`).
4. **CLT does not make a small-sample *posterior* Gaussian:** With $$n = 5$$ data points, running $$S = 100{,}000$$ MCMC draws makes your *Monte Carlo estimate* of the posterior ultra-precise—it does *not* turn a skewed posterior into a bell curve!

**Quick check.** If your posterior SD is $$\sigma = 0.20$$ and you want your Monte Carlo Standard Error (MCSE) of the posterior mean to be $$\le 0.002$$, how many independent draws $$S$$ do you need?

---

## Reference videos

- [Law of Large Numbers - Explained and Visualized](https://www.youtube.com/watch?v=MntX3zWNWec) — Jeremy Blitz-Jones, English. **watch first**. Watch the sample mean stabilize as the number of observations grows, exactly the law of large numbers in the first half of the lesson.
- [But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo) — 3Blue1Brown, English. Watch the shape of the distribution of the mean approach a bell, supporting the central limit theorem part.
- [Định lý giới hạn trung tâm (Central limit theorem)](https://www.youtube.com/watch?v=Sm2yBx3Jn6c) — Bài Học 10 Phút, Vietnamese. Watch the same theorem again in Vietnamese, to compare with the lesson's argument about estimation and simulation.

## Practice questions

1. Why is the LLN not enough to deduce the uncertainty interval of $$\bar X$$?
2. Explain in words why the standard error decreases as $$1/\sqrt{n}$$.
3. Does the CLT require the original data to be normal?

## References

- Casella, G., & Berger, R. (2002). *Statistical Inference*.
- Wasserman, L. (2004). *All of Statistics*.

---

*Next lesson: [0.17 Sampling Distribution and Standard Error]({{ site.baseurl }}/contents/en/chapter00/00_15_sampling_distribution_standard_error/)*
