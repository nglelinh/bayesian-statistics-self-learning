---
layout: post
title: "Lesson 0.11: P-values and Hypothesis Testing"
chapter: '00'
order: 11
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

## Learning Objectives

After completing this lesson, you will deeply understand **p-values** and hypothesis testing from the frequentist perspective, not only to apply them correctly, but more importantly to recognize their fundamental limitations. You will understand why **p-values** are often misinterpreted, why they do not answer the questions scientists actually care about, and why **the Bayesian approach offers a more natural and coherent approach to statistical inference**. This lesson is not meant for you to abandon hypothesis testing entirely, but for you to use it critically and know when to look for alternative methods.

## Introduction: Why Do We Need to Talk About P-values?

In a course on Bayesian data analysis, why do we spend time discussing p-values and frequentist hypothesis testing? The answer has three important reasons.

1. First, p-values and hypothesis testing remain the most widely used statistical tools in modern scientific research. Whether you work in medicine, psychology, economics, or any other field, you will meet p-values in most of the scientific papers you read. To be able to read and evaluate research critically, you need to understand what p-values really mean.

2. Second, p-values are one of the most misunderstood statistical concepts, even within the research community. Many scientists use p-values every day without really understanding what they measure. Understanding p-values correctly will help you avoid these common and dangerous mistakes.

3. Third, and most importantly, understanding the limitations of p-values clearly will help you appreciate the power and naturalness of the Bayesian approach. When you see clearly what p-values cannot tell you, you will understand why the Bayesian approach offers a better way to approach many research questions.

This lesson will build a deep understanding of p-values, not so that you become an advocate for them, but so that you can use them responsibly and know when to go beyond them.

## The Hypothesis Testing Framework: An Indirect Approach

Frequentist hypothesis testing is based on a somewhat counterintuitive indirect logic. Instead of directly evaluating the evidence for the hypothesis we care about, we construct a **null hypothesis**, usually denoted $$H_0$$, representing the state of "no effect" or "no difference", and then try to find evidence against it.

For example, suppose we want to know whether a new drug is effective at lowering blood pressure. Instead of directly asking "Is this drug effective?" or "How large is the drug's effect?", the hypothesis testing framework requires us to set up:

The **null hypothesis** $$H_0$$ says that the drug has no effect, i.e., the mean change in blood pressure equals 0, while the **alternative hypothesis** $$H_1$$ says that the drug has an effect, i.e., that mean change is not 0.

The logic of hypothesis testing is: **if the observed data would be very unusual if $$H_0$$ were true, then we have evidence against $$H_0$$ and can "reject" it**. This is a form of proof by contradiction, similar to mathematics, but with an important difference: **in statistics, we can never prove anything with certainty, we can only talk about how unusual the data is**.

This indirect approach has historical roots in the work of Ronald Fisher, Jerzy Neyman, and Egon Pearson in the early 20th century. It was designed to provide an objective procedure for making decisions based on data. However, as we will see, this objectivity comes at a steep price.

## The P-value: The Precise Definition

The p-value is the central concept of hypothesis testing, but also one of the most misunderstood concepts in statistics. Let us start with the precise definition:

**The p-value is the probability of observing data at least as unusual as the actual data (or more unusual), given that the null hypothesis is true.**

Formally, if $$T$$ is a **test statistic** computed from the data, and $$t_{obs}$$ is its observed value, then:

$$p = P(T \geq t_{obs} \mid H_0)$$

(for a one-sided test, or a similar formula for a two-sided test)

Let us analyze this definition carefully, because every part is important:

1. **"Probability"**: The p-value is a probability, lying between 0 and 1.

2. **"Observing data at least as unusual as..."**: We do not compute only the probability of the exact data we observe, but the probability of this data plus all the outcomes that are "more extreme" in a given direction.

3. **"Given that the null hypothesis is true"**: This is the most important part and is often overlooked. The p-value does **not** tell you the probability that the null hypothesis is true. It tells you the probability of the data **if** the null hypothesis is true.

The difference between $$P(\text{data} \mid H_0)$$ and $$P(H_0 \mid \text{data})$$ is fundamental. The p-value gives you the former, but what scientists really want to know is usually the latter. This is one of the main sources of misunderstanding about p-values.

---

### Explaining Each Component

#### (1) "The null hypothesis is true" ($$H_0$$ is true)

This condition is extremely important:

We always **assume in advance** that $$H_0$$ is true, and only then ask: if $$H_0$$ really is true, is data that looks like this rare?

**Example:**

If $$H_0$$ says the drug has no effect but the data gives the impression that the drug seems effective, then the p-value answers the question: if the drug really has no effect, what is the probability of still observing a result at least this extreme?

#### (2) What does "unusual data" mean?

"Unusual" is not a feeling, but is defined by:

"Unusual" here is not a subjective feeling but is defined through a **test statistic** such as the z-score, t-statistic or $$\chi^2$$, i.e., how far the data lies from the expectation under $$H_0$$.

For example, the sample mean may deviate far from the mean expected under $$H_0$$, the difference between two groups may be very large, or the statistic may fall deep into the tail of the distribution; the farther from the center of expectation, the more extreme the data and therefore the more it is regarded as unusual.

#### (3) "At least as unusual as the observed data (or more unusual)"

This is the part that is often missed but very important.

The p-value **does not only** compute the probability of exactly the result you see, but computes:

> The probability of the observed result **and all the more extreme results**.

**Example (two-sided test):** suppose we observe $$z = 2.1$$. Then the p-value is $$P(\mid Z \mid \geq 2.1 \mid H_0 \text{ true})$$. In other words, we do not compute only the probability of exactly 2.1, but also values such as 2.5, 3.0, and every more extreme value on both sides.

---

### What the P-value Does NOT Say

This is a point that is very often misunderstood: the p-value is not the probability that the null hypothesis is false, is not the probability that the result is "due to chance", and is also not a direct measure of effect size.

**Wrong example:**

> "P-value = 0.03 means there is a 97% chance $$H_0$$ is false" ❌

**Correct interpretation:**

> "If $$H_0$$ is true, then the probability of observing data at least this extreme is 3%." ✅

---

### A Brief Intuitive Interpretation

A simple way of putting it that is true to its nature:

**The p-value measures how "hard to believe" the data is, if we believe the null hypothesis is true.**

Put more briefly, a small p shows the data is unlikely if $$H_0$$ is true so we have more reason to doubt $$H_0$$, while a large p only shows the data does not strongly contradict $$H_0$$.
---

## A Concrete Example: The T-test

Let us consider a concrete example to clarify the concepts. Suppose we want to test whether the average height of male students at a university differs from 170 cm. We measure the height of 25 randomly chosen male students and compute the sample mean height $$\bar{x} = 172.5$$ cm with sample standard deviation $$s = 6.2$$ cm.

We set up $$H_0$$ that $$\mu = 170$$, i.e., the population mean height is 170 cm, and $$H_1$$ that $$\mu \neq 170$$, i.e., the population mean height differs from 170 cm.

The t test statistic is computed as:

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}} = \frac{172.5 - 170}{6.2 / \sqrt{25}} = \frac{2.5}{1.24} \approx 2.02$$

With $$n - 1 = 24$$ degrees of freedom, we consult the t distribution table (or use software) to find the probability of observing a value $$\mid t \mid \geq 2.02$$ if $$H_0$$ is true. Suppose we find $$p \approx 0.054$$.

![Illustration of the P-value in a T-test]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_ttest_illustration.png)

*How to read the figure: This figure illustrates the p-value in the t-test. Read the axis labels/legend first, then compare the main trend across the lines, bars or groups of points instead of looking only at individual points.*

What does this mean? It means that **if** the population mean height truly is 170 cm, and we repeat this experiment many times (each time taking 25 random samples), then in about 5.4% of the repetitions we would observe a t value with magnitude at least 2.02.

This p-value does not tell us that the probability $$H_0$$ is true is 5.4%, nor that the probability $$H_1$$ is true is 94.6%; it also does not directly say how large the effect size is or how practically meaningful the study is.

### A More Correct Reading of $$p = 0.054$$

The number $$0.054$$ is often irritating because it sits very close to the 0.05 threshold. A more reasonable reading is not "a complete failure", but: this data creates a moderate level of conflict with $$H_0$$, but not strong enough to reach a definitive conclusion under the traditional convention. If a nearly identical study gave $$p=0.049$$, in terms of practical evidence the two results are barely different.

This is why many statisticians advise against turning the p-value into an on/off binary switch. More important is to also look at the effect size, the confidence interval, the quality of the study design, and the scientific context of the question under consideration.

### Experiment: the p-value under H₀ is uniformly distributed

Repeat the experiment many times: when there is no effect, about 5% of experiments still give p < 0.05.

<div class="interactive-demo" markdown="1">
<div data-demo="pvalue-explainer" data-lang="en" data-tab="pnull"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## Significance Thresholds and Decisions: The $$\alpha = 0.05$$ Convention

In practice, p-values are often compared with a pre-specified **significance level**, usually denoted $$\alpha$$. The most common convention is $$\alpha = 0.05$$, although other values such as 0.01 or 0.10 are also sometimes used.

#### A simple decision rule:

Under the traditional convention, if $$p < \alpha$$ we reject $$H_0$$ and call the result "statistically significant"; and if $$p \geq \alpha$$ we do not reject $$H_0$$ and say that there is not yet enough statistical evidence against it.

In our height example, with $$p = 0.054$$ and $$\alpha = 0.05$$, we would **fail to reject** $$H_0$$. We would conclude that there is not enough evidence to say that the mean height differs from 170 cm.

But let us stop and think about this. The difference between $$p = 0.054$$ and $$p = 0.049$$ is very small, but it leads to two completely different conclusions under this rule. One result is called "statistically significant" and the other "not statistically significant", even though the evidence in the data is nearly identical.

![Two nearby p-values falling on two sides of the alpha threshold]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_misinterpretation_alpha_cutoff.png)

*Illustration: When the p-value sits right at the $$\alpha = 0.05$$ threshold, a very small difference can still be interpreted as two completely different binary conclusions.*

Moreover, the threshold $$\alpha = 0.05$$ is completely arbitrary. Ronald Fisher, who proposed it, said explicitly that it was only a rough guideline, not a rigid rule. In practice, however, it has become a magic threshold that researchers feel they must cross to publish their results.

Relying on this rigid threshold has many negative consequences: it encourages "p-hacking", pushes researchers into binary thinking of the "effect or no effect" kind, and obscures more important information such as the effect size or the uncertainty of the estimate.

### Experiment: the power of a t-test

Power increases with sample size and effect size; at d = 0 it equals α.

<div class="interactive-demo" markdown="1">
<div data-demo="pvalue-explainer" data-lang="en" data-tab="power"></div>
</div>

## Common Misconceptions About P-values

P-values are one of the most misunderstood concepts in science. Let us look at some common misconceptions:

### Misconception 1: The p-value is the probability that the null hypothesis is true

**Wrong:** "$$p = 0.03$$ means there is a 3% chance the null hypothesis is true."

**Correct:** The p-value is the probability of the data (or more extreme data) **if** the null hypothesis is true, not the probability that the null hypothesis is true after seeing the data.

This difference is fundamental. To compute $$P(H_0 \mid \text{data})$$, we need Bayes' theorem and a prior probability for $$H_0$$, which the frequentist framework does not provide.

![The p-value is not the probability of the null hypothesis]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_misinterpretation_h0_probability.png)

*Illustration: The p-value lives in the direction of $$P(\text{data} \mid H_0)$$, not the direction of $$P(H_0 \mid \text{data})$$ that researchers usually actually want to know.*

### Misconception 2: $$1 - p$$ is the probability that the alternative hypothesis is true

**Wrong:** "If $$p = 0.05$$, then there is a 95% chance the alternative hypothesis is true."

**Correct:** The p-value gives you no direct information about the probability of the alternative hypothesis.

### Misconception 3: A small p-value means a large effect

**Wrong:** "$$p < 0.001$$ means the effect is very strong."

**Correct:** A small p-value only means the data would be very unusual if $$H_0$$ were true. This can happen because of a large effect, but it can also happen because of a large sample size with a small effect.

For example, with a large enough sample, you can find a "statistically significant" difference between two groups even when the actual difference is very small and has no practical significance.

![A small p-value does not mean a large effect]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_misinterpretation_small_p_large_effect.png)

*Illustration: A very small p-value can still come from a small effect if the sample size is large enough.*

![Large sample with a small effect]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_large_n_small_effect.png)

*Figure 1a: With a large sample (n = 1000), a very small effect can still give a "statistically significant" p-value.*

![Small sample with a large effect]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_small_n_large_effect.png)

*Figure 1b: With a small sample (n = 20), even a large effect may fail to reach the statistical significance threshold. The p-value therefore does not directly measure effect size.*

### Misconception 4: A large p-value proves the null hypothesis is true

**Wrong:** "$$p = 0.80$$ means the null hypothesis is true."

**Correct:** A large p-value only means the data is not unusual if $$H_0$$ is true. This can happen because $$H_0$$ really is true, or because we do not have enough data to detect a difference.

"Absence of evidence of an effect" is not the same as "evidence of no effect".

![A large p-value does not prove the null hypothesis is true]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_misinterpretation_large_p_h0_true.png)

*Illustration: A large p-value only shows the data does not strongly contradict $$H_0$$; it does not prove $$H_0$$ is true.*

### Misconception 5: The p-value measures reproducibility

**Wrong:** "$$p = 0.05$$ means if I repeat the study, I have a 95% chance of finding a similar result."

**Correct:** The p-value tells you nothing about reproducibility. In fact, research shows that many results with $$p$$ near 0.05 cannot be replicated.

## The Problem with Null Hypothesis Testing

A fundamental problem with the hypothesis testing framework is that the null hypothesis itself is often implausible. In many real situations, we know in advance that the null hypothesis is almost certainly false.

For example, consider the null hypothesis "drug A and drug B have exactly the same effectiveness". In reality, two different drugs will almost certainly have some difference, however small, in their effectiveness. With a large enough sample, we can always reject this null hypothesis, but that tells us nothing useful about whether the difference is large enough to matter.

The real question scientists care about is usually not "Is there any effect?" but "How large is the effect?" and "How sure are we of our estimate?" Hypothesis testing does not answer these questions directly.

![An example of a false positive when testing repeatedly]({{ site.baseurl }}/img/chapter_img/chapter00/multiple_testing_false_positive_example.png)

*Figure 2a: When running many independent tests, chance alone can produce a few results that exceed the statistical significance threshold.*

![The p-value distribution is nearly uniform when H0 is true]({{ site.baseurl }}/img/chapter_img/chapter00/multiple_testing_uniform_pvalues.png)

*Figure 2b: When $$H_0$$ is true, p-values tend to spread nearly uniformly over $$[0,1]$$, so trying enough times almost guarantees a few very small p-values.*

That is the nature of the multiple testing problem (p-hacking): when running 20 independent tests with $$\alpha = 0.05$$, even if $$H_0$$ is true for all of the tests (no real effect), we still expect to find about 1 "statistically significant" result by chance. This is one of the main sources of the replication crisis in science.

## Confidence Intervals: A Better Approach?

An alternative frequentist method to hypothesis testing is the **confidence interval**. A 95% confidence interval for a parameter $$\theta$$ is an interval $$[L, U]$$ constructed from the data such that:

$$P(L \leq \theta \leq U) = 0.95$$

where the probability is computed over all possible samples (with $$\theta$$ fixed).

Confidence intervals seem more attractive than p-values because they provide information about the effect size and the uncertainty. However, they still have a fundamental interpretation problem.

**Correct interpretation:** "If we repeat the experiment many times and compute a 95% confidence interval each time, then 95% of the intervals will contain the true value of $$\theta$$."

![Many confidence intervals across repeated experiments]({{ site.baseurl }}/img/chapter_img/chapter00/confidence_interval_repeated_experiments.png)

*Figure 3a: A confidence interval is a statement about a repeated procedure; looking across many experiments, about 95% of the intervals contain the true value.*

**Wrong (but common) interpretation:** "There is a 95% chance the true value of $$\theta$$ lies in this interval."

The difference is subtle but important. In the frequentist framework, $$\theta$$ is a fixed value (though unknown), not a random variable, so it is meaningless to talk about its "probability". The probability in the definition of a confidence interval is about the intervals, not about the parameter.

However, what scientists really want to know is the second interpretation: given this specific data, how likely is the parameter to lie in this interval? This is exactly what the **Bayesian credible interval** provides.

![A credible interval on the posterior of a specific experiment]({{ site.baseurl }}/img/chapter_img/chapter00/credible_interval_single_posterior.png)

*Figure 3b: A credible interval is a direct statement on the posterior of the current experiment, so we can immediately talk about the probability that the parameter lies in that interval.*

## Why Are P-values Still Widely Used?

With all these problems, why do p-values and hypothesis testing still dominate scientific research? The first reason is history and academic inertia: p-values have been taught and used for decades, so changing the statistical practice of the whole scientific community happens very slowly. The second reason is their superficial simplicity: a single number and a decision rule seem clear, even though that simplicity actually hides many problems. The third reason comes from the publishing mechanism, since many journals still prefer "statistically significant" results with $$p < 0.05$$. Finally, many researchers have not been fully trained in alternative methods such as Bayesian or other modern statistical methods.

However, there are signs that this is changing. Many statistical organizations and scientific journals have issued statements warning about the misuse of p-values and encouraging alternative methods.

### Experiment: confidence intervals and credible intervals

Repeat the experiment many times to see the frequentist meaning of "95%".

<div class="interactive-demo" markdown="1">
<div data-demo="interval-explainer" data-lang="en"></div>
</div>

## The Bayesian Approach: A More Natural Approach

The Bayesian approach offers a more natural and direct approach to the questions that hypothesis testing tries to answer. Instead of asking "How unusual would this data be if the null hypothesis were true?", the Bayesian approach asks "Given this data, what should our belief about the parameter be?"

In the Bayesian framework:

1. **We start with a prior**: Before seeing the data, we encode our initial belief about the parameter in a prior distribution $$P(\theta)$$.

2. **We update with data**: Using Bayes' theorem, we combine the prior with the likelihood of the data to obtain the posterior distribution:

$$P(\theta \mid \text{data}) = \frac{P(\text{data} \mid \theta) \cdot P(\theta)}{P(\text{data})}$$

3. **We interpret the posterior directly**: The posterior distribution tells us directly about the probability of different values of $$\theta$$ given the observed data.

For example, instead of saying "we reject the hypothesis that the drug effect is 0 with $$p = 0.03$$", we can say "given this data, there is a 95% posterior probability that the drug effect lies between 2 and 8 mmHg". The latter answers directly the question scientists care about.

Moreover, the Bayesian approach lets us compute the probabilities of different hypotheses, combine information from many studies naturally, make predictions for future data, and quantify uncertainty in a more direct, more interpretable way.

## When Should We Use P-values?

Despite their many limitations, p-values are not always useless. They can still be useful as a quick screening tool to find data patterns worth investigating further, as a preliminary check of model fit, or in contexts that truly need a clear binary decision, such as some quality-control problems.

However, even in these cases, p-values should be used with a full understanding of their limitations and should be supplemented by other measures such as the effect size and confidence intervals.

## Practical Guidelines

If you must use or interpret p-values, you should not report the p-value alone but accompany it with the effect size, the confidence interval, and the sample size; nor should you use a rigid threshold to turn inference into a simple binary decision. The important thing is to always remember that the p-value is $$P(\text{data} \mid H_0)$$ and not $$P(H_0 \mid \text{data})$$, and also to place the result in the context of effect size, practical significance, and the quality of the study design. In many questions, Bayesian or estimation-based methods will be the more appropriate choice.

## Implications for Bayesian Data Analysis

This lesson on p-values and hypothesis testing is not just an academic exercise. It provides important motivation for learning Bayesian methods.

As you progress through this course, you will see that the Bayesian approach solves many of the problems we have discussed. It lets us speak directly about the probability of hypotheses and parameters, provides more interpretable uncertainty estimates, does not depend on arbitrary decision thresholds, supports incorporating prior knowledge naturally, and shifts the focus from mere testing to estimation and prediction.

However, the Bayesian approach is not a magic solution to all problems. It has its own challenges, especially in computation and the choice of priors. But for many research questions, it provides a more natural and coherent approach than traditional hypothesis testing.

## Reference videos

- [p-values: What they are and how to interpret them](https://www.youtube.com/watch?v=vemZtEM63GY) — StatQuest with Josh Starmer, English. **watch first**. Watch the definition of the p-value as the probability of extreme data under the null hypothesis, exactly the part where the lesson wants p-values read correctly.
- [Hypothesis Testing and The Null Hypothesis, Clearly Explained!!!](https://www.youtube.com/watch?v=0oc49DyA3hU) — StatQuest with Josh Starmer, English. Watch the role of the null hypothesis and the testing procedure, supporting the first half of the lesson on the frequentist framework.
- [Confidence Intervals, Clearly Explained!!!](https://www.youtube.com/watch?v=TqOeMYtOc1w) — StatQuest with Josh Starmer, English. Watch how a frequentist confidence interval is built from repeated samples, to contrast with the part of the lesson on the limits of this interpretation.

## Exercises

**Exercise 1: Interpreting P-values.** A study compares two teaching methods and reports "$$p = 0.04$$". Write three interpretations: (a) a correct interpretation of the meaning of this p-value, (b) a common wrong interpretation, and (c) an explanation of why the wrong interpretation is wrong and why the difference matters.

**Exercise 2: Sample Size and P-values.** Suppose the average height of men in population A is 175.0 cm and in population B is 175.5 cm (a very small difference). The standard deviation in both populations is 7 cm. (a) Using the two-sample t-test formula, estimate the sample size needed to have $$p < 0.05$$ when comparing these two populations. (b) Discuss the meaning of this result: is "statistical significance" equivalent to "practical significance"?

![Sample Size Calculation]({{ site.baseurl }}/img/chapter_img/chapter00/sample_size_calculation.png)

*How to read the figure: This figure illustrates the sample size calculation. Read the axis labels/legend first, then compare the main trend across the lines, bars or groups of points instead of looking only at individual points.*

The figure above shows the relationship between the effect size and the sample size needed to detect that effect with power = 0.80 and α = 0.05. Note that to detect a small effect (0.5 cm), we need a very large sample (more than 1500 people per group), whereas a large effect (2.0 cm) needs only about 100 people per group.

**Exercise 3: P-hacking.** A researcher collects data on 20 different variables and tests whether each variable is correlated with an outcome of interest, using $$\alpha = 0.05$$ for each test. (a) If in reality none of the variables is correlated with the outcome, what is the probability of finding at least one "statistically significant" result? (b) What kind of problem is this an example of? (c) Propose two ways to address this problem.

**Exercise 4: Comparing Confidence Intervals and Credible Intervals.** Suppose you read two reports: (a) "The 95% confidence interval for the drug effect is [2, 8] mmHg" (frequentist), and (b) "The 95% credible interval for the drug effect is [2, 8] mmHg" (Bayesian). Write the precise interpretation for each interval. Which interval answers more directly the question a doctor cares about? Why?

**Exercise 5: Case Study.** Find a scientific paper in a field you are interested in that uses p-values. (a) Do the authors interpret p-values correctly? (b) Do they report effect sizes and confidence intervals? (c) If you were a reviewer, what improvements would you suggest for the statistical analysis? (d) Would a Bayesian approach be more suitable for this research question? Why?

## References

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 4: Asymptotics and connections to non-Bayesian approaches
- Chapter 6: Model checking

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 11: Null Hypothesis Significance Testing
- Chapter 12: Bayesian Approaches to Testing a Point ("Null") Hypothesis

### Critical Papers on P-values:

**Wasserstein, R. L., & Lazar, N. A. (2016).** The ASA's statement on p-values: context, process, and purpose. *The American Statistician*, 70(2), 129-133.

**Ioannidis, J. P. (2005).** Why most published research findings are false. *PLoS Medicine*, 2(8), e124.

**Nuzzo, R. (2014).** Scientific method: statistical errors. *Nature*, 506(7487), 150-152.

### Supplementary Reading:

**McShane, B. B., Gal, D., Gelman, A., Robert, C., & Tackett, J. L. (2019).** Abandon statistical significance. *The American Statistician*, 73(sup1), 235-245.

**Greenland, S., Senn, S. J., Rothman, K. J., Carlin, J. B., Poole, C., Goodman, S. N., & Altman, D. G. (2016).** Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations. *European Journal of Epidemiology*, 31(4), 337-350.

---

*Next lesson: [0.12 T-test and the T Distribution]({{ site.baseurl }}/contents/en/chapter00/00_09_t_test_and_t_distribution/)*
