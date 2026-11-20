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
