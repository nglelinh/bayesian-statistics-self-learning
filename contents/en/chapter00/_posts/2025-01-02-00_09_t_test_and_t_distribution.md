---
layout: post
title: "Lesson 0.12: The T-test and the T Distribution"
chapter: '00'
order: 12
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

In 1908, William Sealy Gosset—a chemist working at the Guinness brewery in Dublin—had a practical problem: testing barley yields and yeast batches with **only 4 to 10 samples at a time**. Standard Normal $$z$$-tables kept giving him too many false alarms because he didn’t know the true population standard deviation $$\sigma$$; he had to estimate it from the tiny sample itself! Publishing under the pseudonym **"Student"** (because Guinness forbade employees from publishing trade secrets), Gosset derived the **Student-$$t$$ distribution**.

This lesson explains *why* estimating $$\sigma$$ thickens the tails of the sampling distribution, walks through a hand-verifiable $$t$$-test, and reveals the Student-$$t$$ distribution’s second life in Bayesian statistics: as the **exact marginal posterior** for an unknown Normal mean AND the go-to **robust likelihood** against outliers!

---

## Background Knowledge Map: Student-$$t$$ in Both Frequentist and Bayesian Worlds

Four insights connect Gosset’s 1908 brewery discovery directly to modern Bayesian modeling:

1. **The Price of Unknown $$\sigma$$:** Replacing known $$\sigma$$ with noisy sample $$S$$ in $$T = rac{ar{X}-\mu}{S/\sqrt{n}}$$ injects extra variability into the denominator, producing heavier tails governed by **degrees of freedom $$
u = n - 1$$**.
2. **Convergence to Normal as $$
u 	o \infty$$:** At $$
u = 3$$, the 95% critical value is $$3.182$$ (far wider than $$1.960$$); by $$
u = 30$$ it shrinks to $$2.042$$; as $$
u	o\infty$$, $$t_
u 	o \mathcal{N}(0,1)$$.
3. **Exact Bayesian Appearance (Marginalizing $$\sigma^2$$):** In a Bayesian Normal model with unknown mean $$\mu$$ *and* unknown variance $$\sigma^2$$, integrating out $$\sigma^2$$ yields an exact **Student-$$t$$ posterior** for $$\mu$$!
4. **Heavy-Tailed Robustness:** Because Student-$$t$$ (with small $$
u$, say $$
u = 3	ext{–}5$$) assigns much higher probability to extreme values than a Gaussian, using a Student-$$t$$ likelihood in Bayesian regression makes your posterior nearly immune to wild outliers!

---

## Learning Objectives

After completing this lesson, you will deeply understand the **t-statistic**, the **t distribution**, and the **t-test** - one of the most common statistical tools in scientific research. You will learn why we need the t distribution (instead of the normal distribution), how to compute and interpret the t-value, and the different types of t-tests. More importantly, you will understand the assumptions and limitations of the t-test, preparing a foundation for comparison with Bayesian methods in later chapters.

## Introduction: The Problem with an Unknown Standard Deviation

Imagine you are a researcher who wants to know whether the average height of male students at your university differs from 170 cm. You cannot measure the height of all male students, so you randomly sample 25 students and compute the sample mean height $$\bar{x} = 172.5$$ cm with sample standard deviation $$s = 6.2$$ cm.

You want to know: is the difference between 172.5 cm (sample) and 170 cm (hypothesis) large enough to conclude that the true average height really differs from 170 cm, or could it be just due to chance?

In classical statistics, if we **know the population standard deviation** $$\sigma$$, we can use the **z-statistic**:

$$z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}$$

And this z-statistic follows the standard normal distribution $$N(0, 1)$$.

But in practice, we **rarely know** $$\sigma$$! We only have $$s$$ - the sample standard deviation, an estimate of $$\sigma$$. When we replace $$\sigma$$ with $$s$$, the uncertainty increases, and the distribution of the statistic is no longer normal.

This is exactly why we need the **t distribution** and the **t-statistic**.

## The T-statistic: Definition and Meaning

The **t-statistic** (or t-value) is defined analogously to the z-statistic, but uses the sample standard deviation $$s$$ instead of $$\sigma$$:

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

Here, $$\bar{x}$$ is the sample mean, $$\mu_0$$ is the hypothesized value, usually coming from $$H_0$$, $$s$$ is the sample standard deviation, $$n$$ is the sample size, and $$s / \sqrt{n}$$ is called the **standard error of the mean** (SE), i.e., the uncertainty of the sample mean.

### Interpreting the T-value

The t-value measures the **number of standard errors** by which the sample mean is away from the hypothesized value:

If **$$|t|$$ is large**, the sample mean is a considerable number of standard errors away from $$\mu_0$$, and that creates evidence against $$H_0$$; conversely, if **$$|t|$$ is small**, the sample mean lies close to $$\mu_0$$ so the data has not created much weight against the null hypothesis.

*How to read the figure: The four figures below separate each level of extremeness of the t-value so you can clearly see how the p-value changes.*

![A small t-value with weak evidence against H0]({{ site.baseurl }}/img/chapter_img/chapter00/t_value_small_example.png)

*Figure 1a: With $$t = 0.5$$ and $$df = 15$$, the p-value is large at about 0.62 so the data is fairly consistent with $$H_0$$.*

![A t-value in the middle zone near the 0.05 threshold]({{ site.baseurl }}/img/chapter_img/chapter00/t_value_borderline_example.png)

*Figure 1b: With $$t = 2.0$$, the p-value is about 0.064 so the result is in a borderline state, close to the 0.05 threshold.*

![A large t-value with stronger evidence against H0]({{ site.baseurl }}/img/chapter_img/chapter00/t_value_large_example.png)

*Figure 1c: With $$t = 3.0$$, the p-value is small at about 0.009 so the evidence against $$H_0$$ is markedly stronger.*

![A chocolate example with a t of small magnitude and negative sign]({{ site.baseurl }}/img/chapter_img/chapter00/t_value_chocolate_example.png)

*Figure 1d: In the chocolate example with $$t = -0.70$$, p = 0.495 shows there is not yet enough evidence against the null hypothesis.*

The shaded region in each panel represents the "extreme region" used to compute the p-value (two-tailed test).

**A concrete example:** returning to the height example, we have $$\bar{x} = 172.5$$ cm, $$\mu_0 = 170$$ cm, $$s = 6.2$$ cm, and $$n = 25$$.

$$t = \frac{172.5 - 170}{6.2 / \sqrt{25}} = \frac{2.5}{1.24} = 2.02$$

A t-value = 2.02 means the sample mean is about 2 standard errors away from the hypothesized value. This is a considerable distance, suggesting there is evidence against the null hypothesis.

## The T Distribution: Why Not the Normal Distribution?

When we use $$s$$ instead of $$\sigma$$, the t-statistic does not follow the normal distribution, but follows the **t distribution** (Student's t-distribution).

### Characteristics of the T Distribution

The t distribution has a shape quite similar to the normal distribution but with heavier tails, and this very characteristic reflects the additional uncertainty when we must estimate $$\sigma$$ by $$s$$. The t distribution also depends on a parameter called the **degrees of freedom**, usually equal to $$df = n - 1$$ in the one-sample t-test, and as $$n$$ increases it converges to the normal distribution; so with a large enough sample, for example more than 30 observations, the two distributions are usually very hard to tell apart by eye.

### Why Heavier Tails?

When the sample is small, $$s$$ is an uncertain estimate of $$\sigma$$. Sometimes $$s$$ is smaller than the true $$\sigma$$, making the t-value larger than it should be. The heavier tails of the t distribution "adjust" for this variability, making it harder for us to reject $$H_0$$ when the sample is small - a reasonably cautious approach.

![Comparison of the T Distribution and the Normal Distribution]({{ site.baseurl }}/img/chapter_img/chapter00/t_vs_normal_distribution.png)

*How to read the figure: This figure illustrates the comparison of the t distribution and the normal distribution. Read the axis labels/legend first, then compare the main trend across the lines, bars or groups of points instead of looking only at individual points.*

The figure above compares the t distribution at several different df values. With **df = 2**, corresponding to a very small sample, the tails of the distribution are extremely heavy because the uncertainty in estimating $$\sigma$$ is still very large; with **df = 5** the tails are still clearly heavier than the normal; with **df = 10** the difference has shrunk; and with **df = 30** the curve is almost indistinguishable from the normal distribution, which can be viewed as the limiting case when $$df = \infty$$.

Note how the critical values change: with df = 2 and $$\alpha = 0.05$$ (two-tailed), the critical value is ±4.303, whereas for the normal distribution it is only ±1.96. This makes rejecting $$H_0$$ much harder when the sample is small - a cautious and reasonable property.

### Experiment: the t distribution with a small sample

Simulates the t statistic and compares it with the t and normal densities as n grows.

<div class="interactive-demo" markdown="1">
<div data-demo="pvalue-explainer" data-lang="en" data-tab="tdist"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## Types of T-tests

There are three common types of t-tests, depending on the study design:

![Summary table of the three types of t-tests]({{ site.baseurl }}/img/chapter_img/chapter00/t_test_type_summary_table.png)

*Figure 2: A quick summary table of the purpose, formula and degrees of freedom of the three common types of t-tests.*

### 1. One-sample T-test

**Purpose:** Compare the mean of one sample with a known value.

**Formula:**

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

**Degrees of freedom:** $$df = n - 1$$

**Example:** Check whether the average height of male students differs from 170 cm.

![One-sample t-test comparing one sample with a hypothesized value]({{ site.baseurl }}/img/chapter_img/chapter00/t_test_type_one_sample.png)

*Figure 2a: The one-sample t-test compares the mean of one sample with a known or pre-hypothesized value.*

### 2. Independent Two-sample T-test (Unpaired)

**Purpose:** Compare the means of two independent groups.

**Formula (assuming equal variances):**

$$t = \frac{\bar{x}_1 - \bar{x}_2}{s_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}$$

Here $$s_p$$ is the **pooled standard deviation**:

$$s_p = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1 + n_2 - 2}}$$

**Degrees of freedom:** $$df = n_1 + n_2 - 2$$

**Example:** Compare the average height of male students in department A and department B.

![Independent two-sample t-test comparing two independent groups]({{ site.baseurl }}/img/chapter_img/chapter00/t_test_type_independent.png)

*Figure 2b: The independent two-sample t-test compares two independent groups, for example height between two different departments.*

### 3. Paired T-test (Dependent)

**Purpose:** Compare the means of two measurements on the same group of subjects (before-after, matched pairs).

**Formula:**

$$t = \frac{\bar{d}}{s_d / \sqrt{n}}$$

Where:
Here, $$\bar{d}$$ is the mean of the differences, and $$s_d$$ is the standard deviation of those differences.

**Degrees of freedom:** $$df = n - 1$$

**Example:** Compare the weight of patients before and after taking a weight-loss drug.

![Paired t-test comparing before and after on the same group]({{ site.baseurl }}/img/chapter_img/chapter00/t_test_type_paired.png)

*Figure 2c: The paired t-test tracks the same group at two time points, so the focus is on the difference of each measured pair.*

## Assumptions of the T-test

The t-test relies on several important assumptions. When these assumptions are violated, the results may not be reliable:

### 1. Data follow a normal distribution (or n is large enough)

**Assumption:** The data in each group follow a normal distribution, or the sample size is large enough (n > 30 is a rule of thumb) for the Central Limit Theorem to take effect.

We can check this assumption with a histogram, a Q-Q plot, or the Shapiro-Wilk test, although we must remember that the latter test is usually very sensitive when the sample size is large.

If the violation occurs with a small sample, we should consider non-parametric tests such as Wilcoxon; with a large sample, the t-test is usually still fairly robust thanks to the central limit theorem.

### 2. Independence among observations

**Assumption:** The observations in the sample are independent of each other.

Common violations include repeated measurements on the same subject, hierarchically structured data, or time series data with serial dependence.

### 3. Equal variances (for the two-sample t-test)

**Assumption:** The two groups have the same variance (homogeneity of variance).

We can check using Levene's test or use the rule of thumb that the ratio $$\frac{s_1}{s_2}$$ should not exceed 2 by too much.

If this assumption is violated, Welch's t-test is usually the safer choice because it does not require equal variances.

## Interpreting T-test Results

When we run a t-test, we get two main pieces of information:

### 1. The T-value

The t-value tells the **degree of difference** between the data and the null hypothesis; the larger its absolute value, the farther the data lie from the expectation under $$H_0$$, and therefore the stronger the evidence against $$H_0$$.

### 2. The P-value

The p-value tells the **probability of observing a t-value at least as extreme** if $$H_0$$ is true; a small p, for example below 0.05, is usually interpreted as statistically significant, while a large p only shows that there is not yet enough evidence to reject $$H_0$$.

**IMPORTANT NOTE:** The p-value does **not** tell the probability that $$H_0$$ is true, does **not** tell the practical importance of the result, and therefore should always be reported together with the **effect size** and **confidence intervals** rather than standing alone.

## A Complete Example: One-sample T-test

Let us work through a complete example with real data:

**Context:** A chocolate manufacturer claims their chocolate bars weigh 100g. We doubt this claim and weigh 16 random bars.

**Data (grams):**
```
98, 102, 97, 99, 101, 103, 98, 100, 
99, 101, 97, 102, 100, 98, 101, 99
```

**Step 1: Set up the hypotheses.** We set $$H_0: \mu = 100$$, i.e., the chocolate bar weighs exactly 100g as claimed; $$H_1: \mu \neq 100$$, i.e., the mean weight differs from 100g; and use a significance level $$\alpha = 0.05$$.

**Step 2: Compute the sample statistics.** From the data, we have $$n = 16$$, $$\bar{x} = 99.69$$ g, and $$s = 1.78$$ g.

**Step 3: Compute the t-statistic**

$$t = \frac{99.69 - 100}{1.78 / \sqrt{16}} = \frac{-0.31}{0.445} = -0.70$$

**Step 4: Determine the degrees of freedom**

$$df = n - 1 = 16 - 1 = 15$$

**Step 5: Find the p-value**

With $$t = -0.70$$ and $$df = 15$$, consulting a t table or using software:

$$p = 0.495$$ (two-tailed)

**Step 6: Conclusion**

$$p = 0.495 > 0.05$$, we **fail to reject** $$H_0$$.

**Interpretation:** There is not enough evidence to conclude that the mean weight of the chocolate differs from 100g. The observed difference (99.69g) could easily occur due to random variation.

**95% Confidence Interval:**

$$\bar{x} \pm t_{0.025, 15} \times \frac{s}{\sqrt{n}} = 99.69 \pm 2.131 \times 0.445 = [98.74, 100.64]$$

This confidence interval contains 100g, consistent with the conclusion of not rejecting $$H_0$$.

### An Additional Reading via Effect Size

We can also standardize the mean deviation by the sample standard deviation:

$$
d=\frac{99.69-100}{1.78}\approx -0.17
$$

This is a very small effect size. That means not only is the p-value not small enough to reject $$H_0$$, but even the observed deviation is small in a practical sense. This example reminds us that a statistical result should be read through at least three layers at once: the sign of the effect, the magnitude of the effect, and the uncertainty around it.

## Comparing the T-test with the Z-test

| Feature | Z-test | T-test |
|----------|--------|--------|
| **When to use** | Population $$\sigma$$ known | $$\sigma$$ unknown (use $$s$$) |
| **Distribution** | Normal(0, 1) | t-distribution (df) |
| **Tails** | Thinner | Heavier |
| **Critical values** | Fixed | Depend on df |
| **In practice** | Rarely used | Very common |

**Relationship:** As $$n \to \infty$$, t-distribution $$\to$$ Normal distribution

## Limitations of the T-test and the Bayesian Direction

Although the t-test is very useful, it still carries limitations close to those of the p-value. It gives us $$P(\text{data} \mid H_0)$$ rather than $$P(H_0 \mid \text{data})$$, tends to be pulled toward binary decisions based on arbitrary thresholds, does not integrate prior knowledge about the plausibility of the hypothesis, and can give wrong conclusions if the underlying assumptions are substantially violated.

### The Bayesian Approach

In later chapters, you will see how the Bayesian approach addresses these limitations. **Bayesian estimation** provides the full distribution of the parameter instead of just a single t-value, **credible intervals** have a more direct interpretation than confidence intervals, **Bayes factors** allow comparing evidence between hypotheses, and **priors** allow prior knowledge to be incorporated into inference transparently.

---

### Worked Numerical Example: One-Sample $$t$$-Test on a Small Batch ($$n = 4$$ vs. $$n = 25$$)

Suppose Guinness tests $$n = 4$$ barley batches and measures yield difference from target ($$\mu_0 = 0$$): `[2, 4, 6, 8]`:
1. **Sample mean & SD:** $$ar{x} = 5.0$$; sum of squared deviations $$(-3)^2 + (-1)^2 + 1^2 + 3^2 = 20$$; sample variance $$s^2 = rac{20}{4-1} = 6.667 \implies s pprox 2.582$$.
2. **Standard error & $$t$$-statistic:**
   $$\mathrm{SE} = rac{2.582}{\sqrt{4}} = 1.291, \qquad t = rac{5.0 - 0}{1.291} = \mathbf{3.873} \quad (df = 3).$$
3. **Compare $$t$$ critical value vs. naive Normal $$z$$:**
   - Naive $$z$$-test (WRONG for $$n=4$$!): 95% critical value $$1.960$$ $$\implies$$ CI $$5.0 \pm 2.53 = [2.47, 7.53]$$ (falsely narrow!).
   - Proper $$t$$-test ($$df = 3$$): 95% critical value $$t_{0.025;\,3} = \mathbf{3.182}$$ $$\implies$$ CI $$5.0 \pm 4.11 = [0.89, 9.11]$$ (**62% wider**!).
   Since $$3.873 > 3.182$$ ($$p pprox 0.030 < 0.05$$), we still reject $$H_0$$, but with an *honest* uncertainty interval!

### Deep-Dive Explanation: Four Rules for Using Student-$$t$$ Effectively (Read Slowly)

1. **Always prefer Welch’s two-sample $$t$$-test (unequal variances):** Assuming two groups have identical variance (`equal_var=True`) is rarely justified; Welch’s $$t$$-test adjusts degrees of freedom automatically with virtually zero loss of power.
2. **Use paired $$t$$-tests when measurements share a subject:** Before/after measurements on the same person cancel out individual baseline variation—dramatically boosting power compared to an unpaired test.
3. **Remember Student-$$t$$’s Bayesian upgrade (BEST — Kruschke):** Instead of a two-sample $$t$$-test, Bayesian Estimation Supersedes the $$t$$-test fits a Student-$$t$$ model to both groups and gives you the full posterior distribution over the difference in means *and* difference in variances!
4. **Watch extreme skewness at tiny $$n$$:** When $$n < 10$$ and data is wildly skewed, check residuals or use a non-parametric / Bayesian model matching the true data shape.

**Quick check.** Why does the 95% critical value of the $$t$$-distribution shrink from $$3.182$$ at $$df = 3$$ down toward $$1.960$$ as sample size $$n$$ grows large?

---

## Reference videos

- [Introduction to the t Distribution (non-technical)](https://www.youtube.com/watch?v=Uv6nGIgZMVw) — jbstatistics, English. **watch first**. Watch why we must use the t distribution when the standard deviation is only estimated from the sample, exactly the reason the lesson replaces the Normal with t.
- [Introduction to t statistics | Confidence intervals | AP Statistics | Khan Academy](https://www.youtube.com/watch?v=a2rd4Qy8yNI) — Khan Academy, English. Watch the t statistic and the corresponding confidence interval, supporting the example of comparing a sample mean with a given value.
- [StatQuickie: Which t test to use](https://www.youtube.com/watch?v=nnBJeb_I-q8) — StatQuest with Josh Starmer, English. Watch how to choose the form of t-test according to the sampling design, used for the part of the lesson that distinguishes testing situations.

## Exercises

**Exercise 1: Computing the T-statistic by Hand.** A study measures the test scores of 10 students after learning with a new method. The national average score is 75. Data: 78, 82, 75, 80, 77, 83, 79, 81, 76, 84. (a) Compute $$\bar{x}$$ and $$s$$. (b) Compute the t-statistic to test $$H_0: \mu = 75$$. (c) With $$\alpha = 0.05$$ (two-tailed), consult the t table and decide whether to reject $$H_0$$.

**Exercise 2: Distinguishing Types of T-tests.** For each of the following situations, determine which type of t-test is appropriate: (a) Compare the exam scores of male and female students. (b) Compare blood pressure before and after exercise for the same group of people. (c) Check whether the daily average temperature differs from 25°C. (d) Compare the effectiveness of two drugs on two different groups of patients.

**Exercise 3: Interpreting Results.** A t-test gives the result: $$t(24) = 2.35, p = 0.027$$. (a) What does df = 24 mean? (b) With $$\alpha = 0.05$$, what is the conclusion? (c) If this were a one-tailed test instead of two-tailed, how would the p-value change? (d) Write a correct interpretation of the meaning of this p-value.

**Exercise 4: Checking Assumptions.** You have height data for 15 people with an obvious outlier. (a) Which assumption of the t-test might be violated? (b) How can you check the normality assumption? (c) If the assumption is seriously violated, what should you do? (d) Is there a better option than the t-test in this case?

**Exercise 5: T-test vs Bayesian (Reflection).** Read the chocolate example above. (a) What exactly does the confidence interval [98.74, 100.64] mean from the frequentist perspective? (b) If you were the manufacturer, would you be satisfied with the conclusion "not enough evidence"? (c) What information does the t-test not provide that you would like to know? (d) How do you think the Bayesian approach could address these problems?

## References

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 4: Asymptotics and connections to non-Bayesian approaches

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 11: Null Hypothesis Significance Testing
- Chapter 16: Metric-Predicted Variable on One or Two Groups

### Classic Reference:

**Student (W.S. Gosset). (1908).** The probable error of a mean. *Biometrika*, 6(1), 1-25.
- The original paper introducing the t distribution

### Supplementary Reading:

**Zimmerman, D. W. (1997).** A note on interpretation of the paired-samples t test. *Journal of Educational and Behavioral Statistics*, 22(3), 349-360.

**Delacre, M., Lakens, D., & Leys, C. (2017).** Why psychologists should by default use Welch's t-test instead of Student's t-test. *International Review of Social Psychology*, 30(1), 92-101.

---

*Next lesson: [0.13 Joint Distribution]({{ site.baseurl }}/contents/en/chapter00/00_11_joint_distribution/)*
