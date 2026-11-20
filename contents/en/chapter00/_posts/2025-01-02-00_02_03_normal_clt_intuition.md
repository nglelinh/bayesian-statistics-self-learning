---
layout: post
title: "Lesson 0.4: Normal and CLT Intuition - When Does Data Look Bell-Shaped?"
chapter: '00'
order: 4
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

## Learning objectives

After this lesson, you will understand the role of the Normal distribution, interpret the parameters $$\mu,\sigma$$ correctly, and know how to use the intuition of the central limit theorem (CLT) to explain why many aggregate quantities are approximately normal.

## 1) What is the Normal distribution?

For a continuous variable $$X$$:

$$
X\sim\mathcal{N}(\mu,\sigma^2),
$$

the density function is:

$$
f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).
$$

Here, $$\mu$$ gives the central location of the distribution, while $$\sigma$$ measures the spread around that center. A quick rule of thumb is that the interval $$\mu\pm\sigma$$ contains approximately 68% of the probability mass, the interval $$\mu\pm 2\sigma$$ contains about 95%, and the interval $$\mu\pm 3\sigma$$ contains about 99.7%.

![The 68-95-99.7 rule of the Normal distribution]({{ site.baseurl }}/img/chapter_img/chapter00/normal_distribution_rule.png)

*How to read the figure: This figure illustrates the 68-95-99.7 rule of the normal distribution. Read the axis labels/legend first, then compare the main trend across the lines, bars or groups of points instead of looking only at individual points.*

## 2) Why does the Normal appear so often?

The CLT says: when adding up (or averaging) many independent noise components, the aggregate usually approaches a normal shape, even if each initial component is not normal.

So quantities such as measurement error, average scores, and the total influence of many small factors are usually close to Normal.

![The CLT makes the distribution of the sample mean gradually rounder and narrower]({{ site.baseurl }}/img/chapter_img/chapter00/clt_sample_means_overlay.png)

*How to read the figure: This figure illustrates that the CLT makes the distribution of the sample mean gradually rounder and narrower. Read the axis labels/legend first, then compare the main trend across the lines, bars or groups of points instead of looking only at individual points.*

## 3) Where does the normalizing constant of the Normal come from?

The Normal density has the form:

$$
f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).
$$

The factor $$\frac{1}{\sigma\sqrt{2\pi}}$$ is the normalizing constant that ensures:

$$
\int_{-\infty}^{\infty} f(x)\,dx=1.
$$

Setting the standardized variable $$z=\frac{x-\mu}{\sigma}$$, we get:

$$
\int_{-\infty}^{\infty} f(x)\,dx
=\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}e^{-z^2/2}\,dz
=1.
$$

That is, the whole "probability mass" of the bell curve equals exactly 1, which is why it is a valid density.

## 4) An intuitive example

Suppose the final exam score is influenced by many small factors:

For example sleep quality, level of revision, the difficulty of each question, and psychological state during the exam.

Each factor varies a little, but their combination usually gives a score distribution close to a bell shape. This is why using a Normal model for errors or for total scores is reasonable in many contexts.

### 4.1) A quick reading using the standard deviation

Suppose the heights of a group of people can be approximated by:

$$
X \sim \mathcal{N}(170, 6^2).
$$

Then we can read very quickly:

- The range $$164$$ to $$176$$ cm is $$\mu \pm 1\sigma$$, usually containing approximately 68% of observations.
- The range $$158$$ to $$182$$ cm is $$\mu \pm 2\sigma$$, usually containing approximately 95% of observations.

So, a person who is $$182$$ cm tall is not "so unusual as to be impossible", but is just sitting near the upper edge of the roughly 95% region. This is an intuitive way to read the Normal without needing to look up a table or compute an integral.

## 5) When should the Normal not be used?

The Normal is no longer a good choice when the data is bounded in its domain, such as a probability lying only in $$[0,1]$$ or a waiting time that is always positive, when the data is non-negative integer counts, or when the distribution is strongly skewed, heavy-tailed, or contains many outliers. In these cases, the Normal assumption can distort the uncertainty intervals considerably.

## 6) The Bayesian connection

In Bayesian modeling, the Normal distribution appears at many different levels: it can serve as the likelihood for continuous data, as the prior for regression coefficients, or appear as a convenient approximation of the posterior when the sample size is large enough. Still, the Bayesian workflow always requires careful model checking, instead of assuming by default that any continuous data can unconditionally be given a Normal.

## Reference videos

- [The Normal Distribution, Clearly Explained!!!](https://www.youtube.com/watch?v=rzFX5NWojp0) — StatQuest with Josh Starmer, English. **watch first**. Watch to read μ and σ on the bell curve, exactly the part of the lesson that interprets the parameters of the Normal distribution.
- [But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo) — 3Blue1Brown, English. Watch the intuition for why the average of many independent variables is close to normal, supporting the central limit theorem part.
- [Định lý giới hạn trung tâm (Central limit theorem)](https://www.youtube.com/watch?v=Sm2yBx3Jn6c) — Bài Học 10 Phút, Vietnamese. Watch a short Vietnamese version on the same theorem, to compare with the lesson's argument about when aggregate data looks bell-shaped.

## Practice questions

1. Name a continuous quantity for which the Normal should be used and explain why.
2. Name a continuous quantity for which the Normal should not be used and propose a replacement distribution.
3. How does the CLT help the intuition about the distribution of the sample mean?

---

*Next lesson: [0.5 Beta and Gamma]({{ site.baseurl }}/contents/en/chapter00/00_02_04_beta_gamma_bayesian/)*
