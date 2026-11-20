---
layout: post
title: "Lesson 0.18: Point Estimation, Bias-Variance, Consistency"
chapter: '00'
order: 18
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

## Learning objectives

After this lesson, you will understand the three core criteria for evaluating an estimator: bias, variance, consistency; and also grasp the bias-variance tradeoff as a model design principle rather than a slogan.

## Introduction: evaluating an estimator cannot rely on a single number

A good estimator is not simply one that gives a "roughly right" result in one sample. We need to evaluate its behavior over many possible samples: is there systematic bias, does it fluctuate too much, and does it converge to the true value as data increases. The three criteria bias, variance, consistency were built to answer exactly these questions.

![Bias variance tradeoff]({{ site.baseurl }}/img/chapter_img/chapter00/bias_variance_tradeoff_curve.png)

*How to read the figure: This figure illustrates the bias variance tradeoff. Read the axis labels/legend first, then compare the main trend across the lines, bars or groups of points instead of looking only at individual points.*
*Figure 1: Bias gradually decreases as complexity increases, variance gradually increases, and the MSE has an optimal balance point.*

## 1) What is point estimation?

A point estimate is a function of the data $$\hat\theta=g(x_1,\dots,x_n)$$ used to predict the value of an unknown parameter $$\theta$$.

Example:

We can use $$\bar X$$ to estimate $$\mu$$, use the sample proportion $$\hat p$$ to estimate $$p$$, or use a sample regression coefficient to estimate the true slope.

## 2) Bias

Bias measures systematic deviation:

$$
\mathrm{Bias}(\hat\theta)=\mathbb{E}[\hat\theta]-\theta
$$

When the bias is 0, the estimator is unbiased; when the bias is nonzero, the estimator tends to be systematically off to one side.

## 3) The variance of an estimator

Even an unbiased estimator can still fluctuate strongly between different samples. That fluctuation is measured by $$\mathrm{Var}(\hat\theta)$$.

A good estimator needs not only little bias but also reasonable variance.

## 4) MSE and the bias-variance decomposition

The expected squared error:

$$
\mathrm{MSE}(\hat\theta)=\mathbb{E}[(\hat\theta-\theta)^2]
$$

decomposes into:

$$
\mathrm{MSE}(\hat\theta)=\mathrm{Bias}(\hat\theta)^2+\mathrm{Var}(\hat\theta)
$$

This is the foundation for regularization thinking: accept a little bias to reduce variance and improve the total prediction error.

### 4.1) A very concrete example of the bias-variance trade-off

Suppose we need to estimate a true parameter $$\theta = 10$$, and we have two estimators:

- Estimator A: unbiased, so $$\mathrm{Bias}=0$$, but its variance is $$9$$.
- Estimator B: slightly biased by 1 unit, so $$\mathrm{Bias}=1$$, but its variance is only $$4$$.

Then:

$$
\mathrm{MSE}(A) = 0^2 + 9 = 9,
\qquad
\mathrm{MSE}(B) = 1^2 + 4 = 5.
$$

Even though estimator B has bias, it is still better in MSE because in return it gets a larger reduction in variance. This is the logic behind many shrinkage and regularization techniques: accept a slight bias in exchange for more stable predictions.

## 5) Consistency

An estimator $$\hat\theta_n$$ is called consistent if:

$$
\hat\theta_n \xrightarrow[]{P} \theta \quad \text{as } n\to\infty
$$

Simply put: when there is enough data, the estimator approaches the true value.

## 6) The connection to Bayes

In Bayes, we do not only use a point estimate but use the whole posterior. Still, bias-variance thinking remains very useful:

A strong prior usually reduces variance but may increase bias, while a weak prior usually reduces bias but the variance can be large when data is still scarce.

## Quick summary

1. Bias measures the systematic deviation of an estimator.
2. Variance measures the fluctuation between samples.
3. MSE = bias^2 + variance.
4. Consistency is about behavior when the sample size is large.

## Reference videos

- [Unbiasedness vs consistency of estimators - an example](https://www.youtube.com/watch?v=6i7mqDJICzQ) — Ben Lambert, English. **watch first**. Watch an example separating an unbiased estimator from a consistent one, exactly the two criteria the lesson places side by side.
- [[Proof] MSE = Variance + Bias²](https://www.youtube.com/watch?v=qmVT35gFW-Q) — math et al, English. Watch the decomposition of MSE into squared bias plus variance, supporting the bias–variance tradeoff part of the estimator discussion.
- [Population and Estimated Parameters, Clearly Explained!!!](https://www.youtube.com/watch?v=vikkiwjQqfU) — StatQuest with Josh Starmer, English. Watch estimating parameters from a sample, used for the part of the lesson about the behavior of an estimator as data grows.

## Practice questions

1. Can an estimator have small bias but large MSE? Why?
2. Why can regularization help prediction even though it creates bias?
3. Does consistency guarantee good performance in small samples?

## References

- Casella, G., & Berger, R. (2002). *Statistical Inference*.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*.

---

*Next lesson: [0.19 Log-probability and Numerical Stability]({{ site.baseurl }}/contents/en/chapter00/00_17_log_probability_numerical_stability/)*
