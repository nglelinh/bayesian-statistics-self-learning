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
