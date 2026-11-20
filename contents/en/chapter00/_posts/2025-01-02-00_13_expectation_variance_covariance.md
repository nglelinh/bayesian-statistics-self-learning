---
layout: post
title: "Lesson 0.15: Expectation, Variance, and Covariance"
chapter: '00'
order: 15
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

## Learning objectives

After this lesson, you will understand expectation as the "long-run average", variance as the "spread around the mean", covariance as the "same-direction or opposite-direction co-movement" between two variables, and know why these three concepts appear constantly in every Bayesian model.

## Introduction: three quantities describing center and uncertainty

In probabilistic inference, we do not always need to know the entire detailed distribution. Many practical decisions start from three basic questions: where the typical value lies, how large the fluctuation is, and whether the variables vary together. Expectation, variance, and covariance are the three quantities that answer those three questions directly.

## 1) Expectation: the mean value under a distribution

For a discrete variable:

$$
\mathbb{E}[X] = \sum_x x\,p(x)
$$

For a continuous variable:

$$
\mathbb{E}[X] = \int x f(x)\,dx
$$

The expectation is not necessarily the value we observe most often directly. It is the "probability center of mass" of the distribution.

![Expectation as the center of mass of a distribution]({{ site.baseurl }}/img/chapter_img/chapter00/expectation_center_histogram.png)

*Figure 1a: The expectation can be seen as the center of mass of the distribution, not necessarily the highest peak of the histogram.*

## 2) Variance: uncertainty around the mean

$$
\mathrm{Var}(X)=\mathbb{E}\big[(X-\mathbb{E}[X])^2\big]
$$

Rewritten in a quick-computation form:

$$
\mathrm{Var}(X)=\mathbb{E}[X^2]-\mathbb{E}[X]^2
$$

The standard deviation is:

$$
\mathrm{SD}(X)=\sqrt{\mathrm{Var}(X)}
$$

Intuitively, a large variance shows that the data is widely spread, while a small variance shows that the data is more concentrated around the mean.

## 3) Covariance: the relationship of co-variation

For two variables $$X, Y$$:

$$
\mathrm{Cov}(X,Y)=\mathbb{E}\big[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])\big]
$$

When $$\mathrm{Cov}>0$$, the two variables tend to increase together; when $$\mathrm{Cov}<0$$, when one variable increases the other usually decreases; and when the covariance is near 0, the linear relationship between them is weak or almost negligible.

![Positive covariance between two variables]({{ site.baseurl }}/img/chapter_img/chapter00/covariance_positive_scatter.png)

*Figure 1b: Positive covariance appears when two variables tend to increase together.*

![Negative covariance between two variables]({{ site.baseurl }}/img/chapter_img/chapter00/covariance_negative_scatter.png)

*Figure 1c: Negative covariance appears when one variable increases and the other tends to decrease.*

Note: covariance depends on the unit of measurement. So in practice we usually use correlation:

$$
\rho_{XY}=\frac{\mathrm{Cov}(X,Y)}{\mathrm{SD}(X)\mathrm{SD}(Y)}
$$

### 3.1) A very short decision example

Suppose there are two bus routes that both have an expected commute time of 30 minutes.

- Route A has typical times around $$28, 30, 32$$ minutes.
- Route B has typical times around $$20, 30, 40$$ minutes.

The two routes can have the same expectation, but route B has a much larger variance, so the risk of being late is also clearly higher. If in addition we see that on heavy-rain days the commute time also rises sharply, we are describing a positive covariance between rainfall and travel time. This example reminds us that looking at the mean alone is not enough; real decisions often depend on both the spread and how the variables co-vary.

## 4) Properties to remember

1. $$\mathbb{E}[aX+b]=a\mathbb{E}[X]+b$$
2. $$\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)$$
3. $$\mathrm{Var}(X+Y)=\mathrm{Var}(X)+\mathrm{Var}(Y)+2\mathrm{Cov}(X,Y)$$
4. If $$X,Y$$ are independent then $$\mathrm{Cov}(X,Y)=0$$

Property (4) goes only one way: zero covariance does not necessarily mean independence.

## 5) Connection to Bayes

In Bayesian inference, the posterior mean is exactly the expectation under the posterior, the uncertainty is usually reported as the posterior SD or posterior variance, and when there are many parameters the covariance matrix tells the degree of dependence between those parameters.

In other words, learning Bayes without being sure of expectation/variance/covariance makes it hard to interpret results.

## Quick summary

1. Expectation is the mean under a distribution.
2. Variance measures the spread around the mean.
3. Covariance measures the same-direction/opposite-direction co-variation of two variables.
4. These three quantities are the basic language for interpreting the posterior.

## Reference videos

- [Expected Values, Main Ideas!!!](https://www.youtube.com/watch?v=KLs_7b7SKi4) — StatQuest with Josh Starmer, English. **watch first**. Watch expectation as the long-run average of a random variable, exactly the opening definition of the lesson.
- [Covariance, Clearly Explained!!!](https://www.youtube.com/watch?v=qtaqvPAeEJY) — StatQuest with Josh Starmer, English. Watch what positive, negative and zero covariance mean, supporting the part on two variables moving in the same or opposite directions.
- [Population and Estimated Parameters, Clearly Explained!!!](https://www.youtube.com/watch?v=vikkiwjQqfU) — StatQuest with Josh Starmer, English. Watch the difference between population parameters and estimates from a sample, used where the lesson connects expectation to sample variance.

## Practice questions

1. Why isn't the expectation always at the peak of the distribution?
2. Give an example of two variables with negative covariance in everyday life.
3. Why is zero covariance not enough to conclude independence?

## References

- Wasserman, L. (2004). *All of Statistics*. Springer.
- McElreath, R. (2020). *Statistical Rethinking* (2nd ed.). CRC Press.

---

*Next lesson: [0.16 The Law of Large Numbers and the Central Limit Theorem]({{ site.baseurl }}/contents/en/chapter00/00_14_law_large_numbers_clt/)*
