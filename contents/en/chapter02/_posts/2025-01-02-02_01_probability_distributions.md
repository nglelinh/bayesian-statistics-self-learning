---
layout: post
title: "Lesson 2.1: Probability Distributions - The Language of Uncertainty"
chapter: '02'
order: 1
owner: Nguyen Le Linh
lang: en
categories:
- chapter02
lesson_type: required
---

## Learning objectives

After this lesson, you should be able to read a probability distribution as a story about uncertainty, distinguish discrete from continuous settings, and explain why Bayesian analysis keeps the **full distribution** instead of only a single point estimate.

> **Mini example.** Two classes both have a pass rate of $$75\%$$, but one class has 8 students and the other has 800 students. The rate is the same, but the certainty is not.
>
> **Quick check.** If you report only the single number $$75\%$$, what important information are you losing?

## Opening question: why is one number often not enough?

Suppose you are tracking the conversion rate of a new button on a website.

In Week 1, you see 25 purchases out of 100 visits, while in Week 2 you again see 25 purchases, but this time out of 1000 visits.

Both weeks give the same point estimate: $$25\%$$. But they do not give the same level of certainty. In Week 2, we are much more confident that the true rate is close to $$25\%$$. In Week 1, values like $$18\%$$ or $$32\%$$ are still quite plausible.

That is the reason Bayesian statistics does not stop at a single number. It keeps a richer object: a **probability distribution**.

![A distribution as a belief map]({{ site.baseurl }}/img/chapter_img/chapter02/distribution_belief_map.png)

## 1. What is a probability distribution?

A probability distribution is a **map of belief** over possible values.

If a value gets high probability or high density, it means that value is more compatible with what we know, what the data suggest, or both.

In Bayesian work, distributions appear everywhere: for unknown parameters, for observed data, and for future predictions. In practice, when you look at a distribution, it helps to ask where its center is, how wide it is, whether it is skewed, and how much probability still remains in the tails, because those questions together turn a graph into an interpretable summary of uncertainty.

## 2. Discrete and continuous uncertainty

### 2.1. Discrete distributions

Use a discrete distribution when the variable takes countable values.

Examples:

number of absent students, number of spam emails in one hour, or number of heads in 10 coin flips.

Then we work with probabilities of exact outcomes:

$$
P(X = x).
$$

### 2.2. Continuous distributions

Use a continuous distribution when the variable can take any value in an interval.

Examples:

height, delivery time, temperature, or the true conversion rate of an ad.

Then we work with density $$p(x)$$ and probabilities over intervals:

$$
P(a < X < b) = \int_a^b p(x)\,dx.
$$

## 3. Same center, different certainty

Suppose two analysts both say the true conversion rate is around $$0.25$$. One uses Beta$$(3,9)$$ and the other uses Beta$$(30,90)$$.

Both have mean:

$$
\frac{\alpha}{\alpha+\beta} = \frac{1}{4}.
$$

But they say different things.

Beta$$(3,9)$$ is fairly wide, which corresponds to saying, “I think $$0.25$$ is a reasonable center, but I am still quite open to nearby possibilities,” whereas Beta$$(30,90)$$ is much tighter and therefore corresponds to saying, “I think $$0.25$$ is reasonable, and I am fairly confident the true value should stay close to it.”

![A narrow distribution indicating high certainty]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_narrow_distribution.png)

![A wide distribution indicating greater uncertainty]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_wide_distribution.png)

That difference disappears if you keep only the mean. The full distribution keeps it.

## 4. The three roles of distributions in Bayesian inference

### 4.1. Prior

The prior $$P(\theta)$$ describes what we believe about the parameter before seeing the current data.

### 4.2. Likelihood

The likelihood $$P(D \mid \theta)$$ describes how compatible the observed data are with each possible value of $$\theta$$.

### 4.3. Posterior

The posterior $$P(\theta \mid D)$$ is the updated belief after combining prior knowledge and data:

$$
P(\theta \mid D) = \frac{P(D \mid \theta)P(\theta)}{P(D)}.
$$

Read together, these three objects define the basic rhythm of Bayesian inference: the prior states where we begin, the likelihood tells us what the data have to say, and the posterior records what remains after those two sources of information are combined coherently.

## 5. How to read the shape of a distribution

### 5.1. Center

The center tells you the most reasonable region for the quantity of interest.

### 5.2. Width

The width tells you how uncertain you still are.

A narrow distribution means greater certainty, whereas a wide distribution means greater remaining uncertainty.

### 5.3. Skewness

The distribution may lean left or right, especially for probabilities near 0 or 1 and for count data.

### 5.4. Tails

The tails tell you how much extreme risk is still on the table.

## 6. Distribution families you will see often

### 6.1. Beta

Natural for quantities between 0 and 1:

success probabilities, pass rates, defect rates, and click-through rates.

![The Beta family]({{ site.baseurl }}/img/chapter_img/chapter02/beta_distribution_family.png)

### 6.2. Binomial

Natural for counting the number of successes in $$n$$ trials.

### 6.3. Poisson

Natural for counting events over time or space:

calls per hour, orders per minute, and system failures per day.

### 6.4. Normal

Natural for continuous quantities varying around a center:

height, measurement error, test scores, and processing time.

## 7. Why Bayesian analysis keeps the full distribution

Once you keep the full distribution, you can answer practical questions such as:

what the probability is that the conversion rate is above $$5\%$$, what interval is reasonable for the pass rate, and what might happen for the next 100 customers.

A single point estimate cannot answer those questions well.

## 8. Everyday examples

### 8.1. Business

In an A/B test, we care not only about the average lift, but also about uncertainty and downside risk.

### 8.2. Education

A pass rate of $$75\%$$ means something very different in a class of 8 students versus a class of 800 students.

### 8.3. Medicine

With only a handful of patients, a single estimate is often too fragile. A distribution gives a more honest summary.

## 9. Common misunderstandings

### 9.1. “A distribution is just a pretty graph”

No. It stores the whole story about uncertainty.

### 9.2. “The mean is enough”

No. Two distributions can share the same mean but lead to very different decisions.

### 9.3. “If data are large, distributions are unnecessary”

No. Even with lots of data, distributions still matter for risk communication and prediction.

## Summary

**Probability distributions are the core language of Bayesian statistics.** They tell us not only which values are plausible, but also how certain we are, how much risk remains, and how future outcomes might behave.

> **3 key takeaways.** A distribution always carries more information than a point estimate because it keeps uncertainty visible; two distributions can share the same center and still imply very different levels of certainty; and in Bayesian inference, prior, likelihood, and posterior are all distributions playing different roles.

## Practice questions

1. Why does the same pass rate of $$75\%$$ mean different things in a class of 8 students and a class of 800 students?
2. Give three discrete examples and three continuous examples from your own context.
3. Beta$$(4,16)$$ and Beta$$(40,160)$$ have the same mean. How do they differ in interpretation?
4. What business or scientific quantity would you rather describe with a full distribution than with a single number?

## References

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1-2.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 4-5.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 2.

---

*Next lesson: [2.2 Likelihood - The Data's Story Under a Model](/en/chapter02/likelihood/)*
