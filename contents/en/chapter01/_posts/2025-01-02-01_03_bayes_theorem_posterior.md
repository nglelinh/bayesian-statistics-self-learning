---
layout: post
title: "Lesson 1.3: Bayes' Theorem - A Tool for Updating Beliefs"
chapter: '01'
order: 3
owner: Nguyen Le Linh
lang: en
categories:
- chapter01
lesson_type: required
---

## Learning objectives

After this lesson, you need to understand Bayes' theorem as a rule for updating beliefs and not just a memorized formula. You must be able to read the roles of the prior, likelihood and posterior in a real example, and know why Bayes becomes natural in diagnosis, forecasting and learning from data.

> **Mini example.** A doctor knows that flu is common this season, but when a patient shows up with a set of symptoms very characteristic of COVID-19, the initial belief needs to be updated. Bayes' theorem is exactly the tool for doing that in a principled way.
>
> **Quick check.** If the prior is what you believe before the data, and the likelihood is how well the data fits each hypothesis, how should the posterior be understood?

## 1. Bayes starts from a very everyday question

Every day, we do something very Bayesian: we first believe something at a moderate level, then see new information, and then adjust the belief. This appears when we hear a weather forecast and update plans, when we look at test results to update a diagnosis, or when we look at first-week sales to adjust beliefs about market demand. Bayes' theorem simply turns this seemingly intuitive process into a clear mathematical rule.

## 2. An easy example: a doctor diagnosing a disease

Suppose a doctor is weighing three possibilities: flu, COVID-19, and bacterial pneumonia. Before looking closely at the patient's specific symptoms, the doctor already has an initial belief based on which disease is circulating this season, the regional epidemiology, and prior experience; that is the **prior**. Then, the doctor looks at new data such as fever, cough, loss of taste, X-ray images, or test results; that is the information that goes into the **likelihood**. Combining these two parts, the doctor has an updated belief about the most plausible diagnosis; that is the **posterior**.

![The patient's initial symptoms]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_doctor_diagnosis_symptoms.png)

![The diagnostic prior before strong evidence]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_doctor_diagnosis_prior.png)

![New data changes the plausibility of each hypothesis]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_doctor_diagnosis_new_data.png)

![The posterior after updating with evidence]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_doctor_diagnosis_posterior.png)

## 3. The Bayes formula

Bayes' theorem is written as follows:

$$
P(\theta \mid D) = \frac{P(D \mid \theta)\,P(\theta)}{P(D)}.
$$

Here, $$P(\theta \mid D)$$ is the **posterior**, $$P(D \mid \theta)$$ is the **likelihood**, $$P(\theta)$$ is the **prior**, and $$P(D)$$ is the **evidence** or normalizing constant.

If we only need to look at the structure, we usually remember the short form:

$$
\text{posterior} \propto \text{likelihood} \times \text{prior}.
$$

### 3.1. Quick review of conditional probability and total probability

Before using Bayes, we need two very short pieces:

$$
P(A\mid B)=\frac{P(A\cap B)}{P(B)}
$$

and

$$
P(B)=\sum_i P(B\mid A_i)P(A_i)
$$

where $$\{A_i\}$$ are mutually exclusive cases that cover all possibilities.

For a binary problem (disease/no disease), the total probability formula is usually written:

$$
P(B)=P(B\mid A)P(A)+P(B\mid A')P(A').
$$

This is exactly the normalizing denominator in Bayes' theorem.

## 4. Reading the formula in words

Don't rush to see Bayes as a scary formula. Read it in plain English:

> My new belief about a hypothesis is proportional to how strongly the data supports that hypothesis, multiplied by how strongly I believed that hypothesis beforehand.

This is an extremely natural idea.

If a hypothesis has a high prior and the data also fits it, its posterior will be high. Conversely, if the prior is already low and the data does not support it either, the posterior will be low.

## 5. A classic example: the biased coin

Suppose we want to know what the probability $$\theta$$ of heads for a coin is.

### Before the data

We think the coin may be nearly balanced, but are not sure; that is the prior.

### The data

We toss 10 times and see 7 heads.

### The update

Bayes combines the initial prior with the 7/10 data to produce the posterior for $$\theta$$.

![Bayes with the coin example]({{ site.baseurl }}/img/chapter_img/chapter01/coin_bayes_visualization.png)

The important point is that the posterior is not simply equal to the prior, nor just equal to the observed proportion 0.7. It is a compromise between what we believed before and what the data is saying.

## 6. What are the prior, likelihood and posterior, really?

### 6.1. Prior

The prior is what we believe before the current data. For example, we may know that the pass rate of a course has usually been around 70%, that a similar drug is usually only moderately effective, or that a coin bought from a shop is usually nearly balanced.

### 6.2. Likelihood

The likelihood measures how well the current data fits each parameter value. For example, if the coin is truly balanced how plausible is the data of 7/10 heads, or if the true pass rate is 0.9 is the current data still plausible.

### 6.3. Posterior

The posterior is the belief after updating. It is the central object of Bayesian inference because from the posterior we can answer where the parameter is likely to lie, what the probability is that it exceeds a threshold, or what its most plausible range of values is.

![The prior before looking at the data]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayes_theorem_prior.png)

![The likelihood shows which parameter values the data supports]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayes_theorem_likelihood.png)

![The posterior after updating with data]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayes_theorem_posterior.png)

![Comparing the prior and posterior to see where the data has pulled belief]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayes_theorem_prior_vs_posterior.png)

### Experiment: count people instead of multiplying probabilities

Drag the base rate, sensitivity and specificity; press Next step to see 1000 people split into sick/healthy, positive/negative and why a positive result is not necessarily a disease.

<div class="interactive-demo" markdown="1">
<div data-demo="bayesrule-explainer" data-lang="en" data-tab="tree"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 7. A very famous example: a medical test

This is an example that helps learners see where Bayes is strong.

Suppose there is a rare disease that only 1% of the population has, a test with high sensitivity and high specificity, and a person receives a positive result. The question the patient really cares about is: "So what is the probability that I really have the disease?"

Many people mistakenly think that a positive result is almost synonymous with surely having the disease. But Bayes shows that if the disease is very rare then the initial prior is very low, so even a fairly good test does not necessarily push the posterior to an extremely high level.

![The medical test paradox]({{ site.baseurl }}/img/chapter_img/chapter01/medical_test_paradox.png)

Here is one of the places where Bayes gives a much more natural answer than gut intuition.

### 7.1. Computing concrete numbers for the rare-disease test problem (Example 1)

Suppose $$P(D)=0.001$$ is the initial disease rate, $$P(+\mid D)=0.9$$ is the sensitivity, and $$P(+\mid D')=0.01$$ is the false positive rate.

We need:

$$
P(D\mid +)=\frac{P(+\mid D)P(D)}{P(+)}.
$$

With total probability:

$$
P(+)=P(+\mid D)P(D)+P(+\mid D')P(D')
$$

$$
=0.9\times 0.001+0.01\times 0.999=0.01089.
$$

Suy ra:

$$
P(D\mid +)=\frac{0.9\times 0.001}{0.01089}\approx 0.0826.
$$

Even though the test is fairly good, the posterior is still only about $$8.26\%$$ because the disease is too rare (low base rate).

### 7.2. Reading the problem through the confusion matrix

In a binary diagnostic problem, the **confusion matrix** helps read the meaning of the quantities correctly: **True Positive (TP)** is having the disease and testing positive, **False Positive (FP)** is not having the disease but testing positive, **False Negative (FN)** is having the disease but testing negative, and **True Negative (TN)** is not having the disease and testing negative. Then, the sensitivity is $$P(+\mid D)=\frac{TP}{TP+FN}$$, the specificity is $$P(-\mid D')=\frac{TN}{TN+FP}$$, and the false positive rate is $$P(+\mid D')=1-\text{specificity}$$.

What the patient cares about is $$P(D\mid +)$$, i.e. the PPV. This is the reason Bayes must be used: from the quantities along the rows/columns of the confusion matrix to infer the posterior probability truly needed for decisions.

### 7.3. A context-conditioning example (Example 2)

Suppose $$P(\text{Icy})=0.7$$ and $$P(\text{Not Icy})=0.3$$, and also $$P(\text{One crashes}\mid \text{Icy})=0.8$$ while $$P(\text{One crashes}\mid \text{Not Icy})=0.1$$.

First, use total probability:

$$
P(\text{One crashes})=0.8\times 0.7+0.1\times 0.3=0.59.
$$

Suppose we have observed that Watson crashed. Then:

$$
P(\text{Icy}\mid \text{Watson crashes})=\frac{0.8\times 0.7}{0.59}\approx 0.95.
$$

The probability that Holmes crashes after knowing Watson crashed:

$$
P(\text{Holmes crashes}\mid \text{Watson crashes})=0.8\times 0.95+0.1\times 0.05=0.765.
$$

The important point: we update the belief about the environmental condition (the runway), and then infer the probability of the event of interest.

## 8. What role does the evidence play?

In the formula:

$$
P(D)
$$

is the probability of observing the data under all possible values of the parameter.

You can think of the evidence as a normalizing constant to ensure the posterior is a valid probability distribution.

In practice, we usually remember:

$$
P(\theta \mid D) \propto P(D \mid \theta)P(\theta)
$$

and leave the normalization for the next step.

## 9. Bayes is not used just once

A big beauty of Bayes is its **sequential updating**.

For example, today you have week 1 data, tomorrow add week 2 data, and next week add week 3 data. You do not need to think of "starting over" in a completely separate way; the current posterior can become the prior for the next update.

![The starting step: the initial prior]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_sequential_updating_prior.png)

![After the first batch of data]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_sequential_updating_step1.png)

![After the second batch of data]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_sequential_updating_step2.png)

![Comparing sequential updating with a one-shot update]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_sequential_updating_batch_comparison.png)

This is extremely natural for business dashboards, operational monitoring, and every situation of continually learning from data arriving over time.

### 9.1. Sequential updating example with two tests (Example 3)

Suppose:

$$
P(\theta=1)=0.7,\quad P(\theta=0)=0.3,
$$

with $$\theta=1$$ meaning having the disease.

The first test $$Y$$ satisfies $$P(Y=1\mid \theta=1)=0.95$$ and $$P(Y=1\mid \theta=0)=0.40$$, and we observe $$Y=1$$.

Then:

$$
P(\theta=1\mid Y=1)=\frac{0.95\times 0.7}{0.95\times 0.7+0.40\times 0.3}
=\frac{0.665}{0.785}\approx 0.847.
$$

Next, there is a second test $$W$$ conditionally independent given $$\theta$$, with $$P(W=1\mid \theta=1)=0.99$$ so $$P(W=0\mid \theta=1)=0.01$$, and $$P(W=1\mid \theta=0)=0.04$$ so $$P(W=0\mid \theta=0)=0.96$$, and we observe $$W=0$$.

Update 2:

$$
P(\theta=1\mid Y=1,W=0)=
\frac{P(W=0\mid \theta=1)P(\theta=1\mid Y=1)}{P(W=0\mid Y=1)}
\approx 0.052.
$$

That is, the posterior changes strongly with new evidence: from $$0.7 \to 0.847 \to 0.052$$.

### Experiment: sequential updating toss by toss

Three kinds of coins; at each toss, multiply the prior by the likelihood and then normalize; change the prior to see the data gradually dominate.

<div class="interactive-demo" markdown="1">
<div data-demo="bayesrule-explainer" data-lang="en" data-tab="sequential"></div>
</div>

## 10. What about a strong or weak prior?

If the prior is very strong, little data may not change the posterior much. If the prior is weak, the data will have a larger influence. This is not a flaw of Bayes but exactly what we want: when prior knowledge is very solid, we should not throw it away too easily; and when the prior is vague, the data should speak more strongly.

### 10.1. A concrete example: same data, different priors

Suppose we observe 6 positive cases out of 10.

- If the weak prior is Beta$$(1,1)$$, the posterior will be Beta$$(7,5)$$ with a posterior mean of about $$0.583$$.
- If the prior is stronger and already leans toward a high rate, for example Beta$$(20,5)$$, the posterior will be Beta$$(26,9)$$ with a posterior mean of about $$0.743$$.

The same data but different posteriors because the prior brings real information into the problem. This is not "whimsical Bayes", but Bayes's way of stating clearly something that always exists in practice: new data is always read in the context of what we already knew.

![Weak prior: the initial belief is still fairly open]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_prior_strength_weak_prior.png)

![Strong prior: the initial belief is much more concentrated]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_prior_strength_strong_prior.png)

![When the prior is weak, the posterior is pulled harder by the data]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_prior_strength_weak_posterior.png)

![When the prior is strong, the posterior changes less]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_prior_strength_strong_posterior.png)

## 11. What Bayes really teaches us

Bayes does not only teach a formula. It teaches a way of thinking, in which data does not speak for itself without a model, initial belief is not taboo, new data must have the right to correct old belief, and the whole updating process needs to be presented transparently.

Once you accept this, you will see the prior and posterior are no longer "strange", but extremely natural.

> **3 key ideas.** Bayes' theorem is the rule for updating beliefs when new evidence arrives; the prior, likelihood and posterior are not three separate concepts but three parts of the same inference process; and the power of Bayes lies in the fact that it lets us combine old knowledge with new data transparently.

## Reference videos

- [P01.007 — Định lý Bayes cập nhật niềm tin của mô hình ra sao?](https://www.youtube.com/watch?v=zXtcZ-2adK0) — Phạm Thông, Vietnamese. **watch first**. Watch, in Vietnamese, how the prior and the data together rewrite belief, exactly the way the lesson wants Bayes' theorem to be read.
- [Bayes theorem, the geometry of changing beliefs](https://www.youtube.com/watch?v=HZGCoVF3YvM) — 3Blue1Brown, English. Watch each component—prior, likelihood and normalizing constant—on a diagram, supporting the part that names their roles.
- [Statistical Rethinking 2023 - 02 - The Garden of Forking Data](https://www.youtube.com/watch?v=R1vcdhPBlXA) — Richard McElreath, English. Watch the globe water-and-land example, where Bayes' theorem becomes counting the ways the data could have been generated.

## Practice questions

1. In the doctor diagnosis example, where does the prior come from and where does the likelihood come from?
2. Why does a positive result on a test not necessarily mean a very high probability of having the disease?
3. Give an example from your own work where today's posterior can become tomorrow's prior.
4. Why does the posterior not necessarily coincide with the proportion observed directly from the data?

## References

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 5.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 1-2.

---

*Next lesson: [1.4 Bayesian vs Frequentist - Comparison and Choice]({{ site.baseurl }}/contents/en/chapter01/01_04_bayesian_vs_frequentist/)*
