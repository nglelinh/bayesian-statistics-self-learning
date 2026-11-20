---
layout: post
title: "Lesson 1.2: Probability as Plausibility - The Philosophical Foundation of Bayesian Statistics"
chapter: '01'
order: 2
owner: Nguyen Le Linh
lang: en
categories:
- chapter01
lesson_type: required
---

## Learning objectives

After this lesson, you need to understand why Bayesian statistics sees probability as the **degree of plausibility of a belief** and not just as long-run frequency. You also need to see the strength of this view on real problems, where we must talk about events that happen only once, about hypotheses, and about unknown parameters.

> **Mini example.** When you hear "70% chance of rain tomorrow", you understand it as the current level of confidence used to decide whether to bring an umbrella, not as a frequency observed from countless repetitions of "tomorrow".
>
> **Quick check.** Why is the sentence "the probability of rain tomorrow is 70%" hard to interpret in the frequentist sense but very natural in the Bayesian sense?

## 1. A seemingly simple question: what is probability, really?

In many traditional statistics courses, probability is usually introduced as the frequency with which an event occurs over very many repetitions. This definition works fairly well for examples such as tossing a coin, rolling dice, or drawing a card from a deck. But it begins to struggle when we ask very everyday questions such as what the probability of rain tomorrow is, what the probability is that this patient has disease A or B, or what the probability is that this model is better than that one.

Those events are not easily understood as "infinitely repeated" in the mechanical sense.

## 2. The frequentist view: probability is long-run frequency

According to the frequentist view, the probability of an event is its relative frequency as the number of repetitions goes to a very large number.

For example, if a coin is fair, then when tossed very many times, the proportion of heads will approach 0.5.

This is a beautiful and important idea. But it has two big limitations.

### 2.1. It is hard to apply to events that happen only once

For example, whether it rains tomorrow, whether this surgery succeeds, or whether the market goes up or down next week.

You cannot "repeat infinitely many times" exactly the same tomorrow to define probability in the purely frequency sense.

### 2.2. It is uncomfortable when talking about unknown parameters

In frequentist statistics, the parameter $$\theta$$ is considered fixed but unknown, while the data is random. So they do not like the sentence "the probability that $$\theta$$ lies between 0.4 and 0.6 is 95%".

For them, $$\theta$$ is not random, so there is nothing to assign a probability to.

## 3. The Bayesian view: probability is plausibility

Bayesian statistics takes a more natural direction for many practical problems.

Probability is not only long-run frequency. It is also a degree of belief, a degree of plausibility, or the degree to which we should bet on a proposition, based on the available information. So the sentence "70% chance of rain tomorrow" can be understood very naturally as: given the current information, the proposition "it rains tomorrow" is credible at the 70% level.

This is not a loose way of speaking. It is the very foundation of Bayesian reasoning.

![The story of Linh and the umbrella]({{ site.baseurl }}/img/chapter_img/chapter01/linh_umbrella_story.png)

## 4. Why is the Bayesian view closer to everyday life?

Because people think this way almost every day.

### 4.1. Weather forecasts

When you hear "70% chance of rain", you do not think about countless parallel worlds, but simply think that it is quite likely to rain so it is better to bring an umbrella.

### 4.2. Medical diagnosis

A doctor does not only look at the current symptoms. They also use the frequency of the disease in the community, age and medical history, as well as previous test results. That is exactly the thinking of updating beliefs based on information.

### 4.3. Business

A startup sees its first 3 customers all make a purchase. No one immediately concludes that the true purchase rate is 100%. We keep a reasonable level of uncertainty, and then continue updating as more data arrives.

![Hearing a strange noise and then updating the hypothesis about its cause]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayesian_daily_life_night_noise.png)

![Reading restaurant reviews and then updating the rating]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayesian_daily_life_restaurant.png)

![Weather forecasting as a belief-updating process]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayesian_daily_life_weather.png)

![Medical diagnosis as a belief-updating process]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayesian_daily_life_medical.png)

## 5. An intuitive example: a friend's coin

Suppose your friend hands you a coin and says: "I just tossed it 10 times and got 8 heads." The question you really want to answer is what the probability of heads for this coin could be.

### What would a frequentist say?

They would say something like: the true parameter is a fixed constant, and we can only estimate it and then build a confidence interval.

### What would a Bayesian say?

A Bayesian would say that before the data, I have a prior about $$\theta$$; after the data of 8/10, I update that prior into a posterior; and the posterior tells which region of $$\theta$$ is currently more plausible.

![How a frequentist statistician views the coin problem]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_coin_flip_frequentist.png)

![How a Bayesian statistician views the coin problem]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_coin_flip_bayesian.png)

The strength here is that Bayes lets us speak directly about the unknown parameter, the current level of belief, and how that belief changes with data.

### Reading it in numbers

If we start with a uniform prior Beta$$(1,1)$$ and observe 8 heads in 10 tosses, the posterior will be Beta$$(9,3)$$. The posterior mean is then:

$$
\frac{9}{9+3}=0.75.
$$

We can even directly ask questions like "what is the probability that the coin is biased toward heads rather than fair?", i.e. $$P(\theta>0.5\mid D)$$, and that value is then about $$0.97$$. This is exactly the spirit of "probability is plausibility": it lets us say outright how plausible the parameter values are after having looked at the data.

## 6. Is "subjective" a weakness?

Many people hear "degree of belief" and worry that Bayes is too subjective. But we need to distinguish between **principled subjectivity** and arbitrariness. In Bayes, you are not allowed to assign probabilities absurdly; the probabilities must still be coherent, obey the rules of probability, and can be corrected by data. In other words, Bayes allows personal belief to appear, but forces that belief to have logical structure and to be accountable to the data.

## 7. The Dutch book intuition: why must beliefs be coherent?

A very nice way to think about it is this: if your system of probabilities is not coherent, others can arrange bets that make you lose for sure.

This idea is called the Dutch book argument.

You do not need to dig into this philosophy right away. Just remember one thing:

**Bayesian probability is not "believe whatever you want". It is disciplined belief.**

![Dutch book cartoon]({{ site.baseurl }}/img/chapter_img/chapter01/dutch_book_cartoon.png)

## 8. Cox and the idea of "probability as extended logic"

A very beautiful way to put it is that classical logic handles what is certainly true or certainly false, while probability handles what is not completely certain.

In that spirit, Bayesian probability can be seen as a form of **extended logic for an uncertain world**.

This explains why Bayes feels natural: when there is no data, we keep an initial level of belief; when new data arrives, we update it.

## 9. Who is random? Who is fixed?

This is the core difference between Frequentist and Bayesian.

### Frequentist

For a frequentist, the parameter is fixed but unknown, while the data is random.

### Bayesian

For a Bayesian, the observed data is already fixed, while the unknown parameter is described by a probability distribution.

This leads to a very big difference in how results are interpreted.

![Frequentist views probability through repeated data]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_philosophy_frequentist.png)

![Bayesian views probability as uncertainty about the parameter]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_philosophy_bayesian.png)

## 10. Why is this chapter so important for what follows?

If you cannot accept that probability can describe reasonable belief, then all of the Bayes that follows will look very strange. But once you see this, concepts such as prior, posterior, credible interval, or the probability of a hypothesis will become very natural.

## 11. A short way to remember

If we had to sum it up in just two sentences, the Frequentist ties probability to the long-run frequency of repeatable data, while the Bayesian ties probability to the degree of plausibility of what we believe given the available information.

Neither side is completely wrong and the other completely right in every situation. But Bayes is much more flexible for real scientific questions.

> **3 key ideas.** Frequentist and Bayesian differ first of all in how they define probability, not only in computational technique; the Bayesian view treats probability as plausibility, so it applies naturally to hypotheses, parameters and events that happen only once; and "subjective" in Bayes does not mean arbitrary, because beliefs must still obey the coherent rules of probability.

## Reference videos

- [The Bayesian Trap](https://www.youtube.com/watch?v=R13BD8qKeTg) — Veritasium, English. **watch first**. Watch probability used as a degree of belief in a hypothesis, exactly the shift in meaning from long-run frequency to plausibility.
- [Bayes' Theorem (with Example!)](https://www.youtube.com/watch?v=akClB1J6b28) — Steve Brunton, English. Watch Bayes' theorem as an inverse problem from symptoms back to causes, supporting the one-off situations in the lesson.
- [Bayes theorem, the geometry of changing beliefs](https://www.youtube.com/watch?v=HZGCoVF3YvM) — 3Blue1Brown, English. Watch belief updated by area, used when the lesson needs a picture for probability as plausibility.

## Practice questions

1. Why is the forecast "70% chance of rain tomorrow" a very natural example for the Bayesian understanding of probability?
2. In the coin problem with 8/10 heads, what is the most important way in which a Frequentist and a Bayesian differ?
3. Give an example from work or life where understanding probability as plausibility is more useful than understanding it as frequency.
4. Why does Bayes still have logical discipline even though it allows initial beliefs to be brought into the model?

## References

- Jaynes, E. T. *Probability Theory: The Logic of Science*.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 1.

---

*Next lesson: [1.3 Bayes' Theorem - A Tool for Updating Beliefs]({{ site.baseurl }}/contents/en/chapter01/01_03_bayes_theorem_posterior/)*
