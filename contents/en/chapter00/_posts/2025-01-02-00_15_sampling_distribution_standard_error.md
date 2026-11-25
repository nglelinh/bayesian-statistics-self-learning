---
layout: post
title: "Lesson 0.17: Sampling Distribution and Standard Error"
chapter: '00'
order: 17
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

Open almost any scientific paper and you will see error bars plotted around a mean—yet half of readers (and plenty of authors!) confuse **Standard Deviation (SD)** with **Standard Error (SE)**. When a nutrition study reports *"mean weight loss = 4 kg, SD = 12 kg, $$n = 144$$"*, individual patients vary wildly ($$\pm 12	ext{ kg}$$), yet the *standard error of the mean* is a razor-thin **$$12 / \sqrt{144} = 1.0	ext{ kg}$$**!

This lesson draws an unbreakable line between **data spread (SD)** and **estimator uncertainty (SE)**, showing how the frequentist sampling distribution compares directly to the Bayesian **posterior standard deviation**.

---

## Key ideas: Data Spread vs. Estimator Uncertainty

Four distinctions clear up every error-bar confusion forever:

1. **Standard Deviation (SD, $$s$$):** Measures how spread out *individual observations* are around the mean. Collecting more data makes $$s$$ estimate $$\sigma$$ more accurately—it does **NOT** shrink $$s$$ toward zero!
2. **Standard Error (SE, $$s/\sqrt{n}$$):** Measures how much the *sample mean* $$ar{X}_n$$ would bounce around if you repeated the entire study from scratch. As $$n 	o \infty$$, $$\mathrm{SE} 	o 0$$!
3. **Sampling Distribution:** The theoretical distribution of a statistic ($$ar{X}_n$$, $$\hat{p}$$, $$\hat{eta}_1$$) across hypothetical repeated samples of size $$n$$.
4. **Bayesian Counterpart (Posterior SD):** Instead of imagining repeated hypothetical samples, Bayesian inference computes the exact spread of your belief about $$\mu$$ given *this* dataset—and for large $$n$$ with a weak prior, the Bayesian posterior SD converges right onto $$\mathrm{SE} = \sigma/\sqrt{n}$$!

---

## Learning objectives

After this lesson, you will clearly distinguish the raw data from the distribution of an estimate, understand that the standard error is the uncertainty of the estimator (not the spread of the data), and use this intuition to read inference results more correctly.

## Introduction: from one data sample to the reliability of an estimate

In practice, we often have only a single data sample, but still need to answer the question "how stable is the current estimate if the sampling procedure were repeated?". The sampling distribution and the standard error are exactly the language for quantifying that question scientifically.

## 1) What is a sampling distribution?

Suppose we repeat the same sampling procedure many times and each time compute an estimate $$\hat\theta$$ (for example the sample mean $$\bar X$$). The collection of $$\hat\theta$$ values across the repetitions forms the **sampling distribution**.

The key point: the sampling distribution is the distribution of the **estimate**, not the distribution of individual data points.

![Sampling distribution of the sample mean with n = 20]({{ site.baseurl }}/img/chapter_img/chapter00/sampling_distribution_n20.png)

*Figure 1a: For the same problem but with a small sample size, the sampling distribution of the sample mean is still fairly wide.*

## 2) Standard Error (SE)

The SE is the standard deviation of the sampling distribution:

$$
\mathrm{SE}(\hat\theta)=\sqrt{\mathrm{Var}(\hat\theta)}
$$

For the sample mean:

$$
\mathrm{SE}(\bar X)=\frac{\sigma}{\sqrt{n}}\approx\frac{s}{\sqrt{n}}
$$

So:

The SD of the data measures the spread among individuals, while the SE measures the uncertainty of the estimate itself.

### Experiment: sampling distribution and standard error

Increase the sample size n and watch the standard deviation of the sample mean decrease as σ/√n.

<div class="interactive-demo" markdown="1">
<div data-demo="clt-explainer" data-lang="en" data-tab="clt"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 3) A common confusion: SD vs SE

Two datasets with the same SD but different sample sizes will have different SEs.

If $$n$$ is larger then the SE is smaller and the estimate is more stable, while if $$n$$ is small then the SE is larger and the conclusion is therefore less certain.

![Sampling distribution of the sample mean with n = 200]({{ site.baseurl }}/img/chapter_img/chapter00/sampling_distribution_n200.png)

*Figure 1b: When the sample size is increased to $$n = 200$$, the sampling distribution narrows markedly, corresponding to a smaller standard error.*

### 3.1) An example where SD and SE are easily confused

Suppose the weight of a group of people has a standard deviation of about 12 kg.

- If we sample $$n=25$$ people, the standard error of the mean is $$12/\sqrt{25}=2.4$$ kg.
- If we sample $$n=100$$ people, the standard error of the mean is $$12/\sqrt{100}=1.2$$ kg.

The important point is that the SD of individual data is still 12 kg in both cases. What changes is the uncertainty of the **estimate of the mean**. This is why SD and SE cannot be used interchangeably, even though many beginners often mix up the two quantities.

## 4) How does the SE relate to confidence/credible intervals?

In normal-approximation thinking, an uncertainty interval usually has the form:

$$
\hat\theta \pm c\cdot \mathrm{SE}(\hat\theta)
$$

The factor $$c$$ depends on the goal (95%, 90%, ...). Regardless of the framework (Frequentist or Bayesian), the intuition that "the width increases when the SE is large" remains the same.

## 5) The connection to the Bayesian workflow

In Bayes, the posterior SD of a parameter plays a role close to the SE: it gives us the uncertainty of the parameter after combining the prior and the data.

If you are used to thinking in terms of sampling distribution + SE, reading posterior intervals will be much easier.

## Quick summary

1. The sampling distribution is the distribution of the estimator.
2. The SE is the standard deviation of the estimator.
3. The data SD and the SE are two different things.
4. Increasing the sample size decreases the SE as $$1/\sqrt{n}$$.

---

### Worked Numerical Example: Watching SD Stay Flat While SE Collapses as $$n$$ Grows

Suppose adult reaction times have population mean $$\mu = 250	ext{ ms}$$ and population SD $$\sigma = 36	ext{ ms}$$. Compare studies of size $$n = 9$$, $$n = 36$$, and $$n = 144$$:

| Sample Size $$n$$ | Individual Spread ($$\sigma$$) | Standard Error ($$\mathrm{SE} = \sigma/\sqrt{n}$$) | 95% Interval for Mean $$\mu$$ ($$\pm 1.96\,\mathrm{SE}$$) |
| :--- | :--- | :--- | :--- |
| $$n = 9$$ | $$36.0	ext{ ms}$$ | $$36 / 3 = \mathbf{12.0	ext{ ms}}$$ | $$ar{x} \pm 23.5	ext{ ms}$$ |
| $$n = 36$$ | $$36.0	ext{ ms}$$ | $$36 / 6 = \mathbf{6.0	ext{ ms}}$$ | $$ar{x} \pm 11.8	ext{ ms}$$ |
| $$n = 144$$ | $$36.0	ext{ ms}$$ | $$36 / 12 = \mathbf{3.0	ext{ ms}}$$ | $$ar{x} \pm 5.9	ext{ ms}$$ |

Every 4× increase in sample size halves the SE while leaving individual human variability ($$36	ext{ ms}$$) completely unchanged!

### Explanation: Four Rules for Reading Error Bars Like a Statistician

1. **Always check the caption: are the error bars SD, SE, or 95% CI?** Plotting `± 1 SE` makes noisy data look artificially tight—always label explicitly!
2. **Use SD to describe people/items; use SE (or posterior SD) to describe uncertainty in an average:** A doctor telling a patient *"your outcome will likely fall within..."* needs SD (or a posterior predictive interval), never SE!
3. **Beware non-independent samples:** If you measure 100 time points from just **5 patients**, your effective sample size for estimating the population mean is closer to 5, not 100—dividing by $$\sqrt{100}$$ severely understates true SE!
4. **Bootstrap when no closed-form SE exists:** For medians, ratios, or AUC scores, resampling your data 2,000 times estimates the sampling distribution directly.

**Quick check.** If a dataset has $$n = 100$$ independent observations with sample SD $$s = 20$$, what is the standard error of the mean—and if you collect $$300$$ *more* observations (reaching $$n = 400$$), what happens to $$s$$ and to $$\mathrm{SE}$$?

---

## Reference videos

- [Standard Deviation vs Standard Error, Clearly Explained!!!](https://www.youtube.com/watch?v=A82brFpdr9g) — StatQuest with Josh Starmer, English. **watch first**. Watch so as not to mix the spread of the data with the uncertainty of the estimate, exactly the distinction between standard deviation and standard error.
- [Introduction to sampling distributions | Sampling distributions | AP Statistics | Khan Academy](https://www.youtube.com/watch?v=z0Ry_3_qhDw) — Khan Academy, English. Watch the sampling distribution of a statistic, supporting the question the lesson poses if the sampling procedure were repeated.
- [Standard error of the mean | Inferential statistics | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=J1twbrHel3o) — Khan Academy, English. Watch the standard error of the sample mean decrease with sample size, used for the part on reading the stability of an estimator.

## Practice questions

1. Explain why a large SD does not mean a large SE in every case.
2. If the sample size is increased from 100 to 400, how does the SE change?
3. Is the sampling distribution of the median the same as that of the mean? Why?

## References

- Rice, J. (2006). *Mathematical Statistics and Data Analysis*.
- Wasserman, L. (2004). *All of Statistics*.

---

*Next lesson: [0.18 Point Estimation, Bias-Variance, Consistency]({{ site.baseurl }}/contents/en/chapter00/00_16_point_estimation_bias_variance_consistency/)*
