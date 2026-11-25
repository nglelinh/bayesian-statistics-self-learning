---
layout: post
title: "Lesson 1.1: The Scientific Crisis and the Limits of P-values"
chapter: '01'
order: 1
owner: Nguyen Le Linh
lang: en
categories:
- chapter01
lesson_type: required
---

In 2015, the Open Science Collaboration attempted to replicate 100 landmark psychology experiments published in top peer-reviewed journals—and **more than 60% failed to replicate!** In medicine, economics, and online A/B testing, the exact same shock hit: hundreds of "statistically significant" results with $$p < 0.05$$ vanished upon re-testing. How could so many peer-reviewed findings be false when the significance threshold was supposed to limit errors to 5%?

The culprit wasn’t bad arithmetic—it was **base-rate neglect, low statistical power, and researcher degrees of freedom (p-hacking)** colliding with a binary `p < 0.05` ritual. This opening Chapter 1 lesson diagnoses the replication crisis mathematically and shows why **Bayesian updating** provides the missing vaccine.

---

## Key ideas: Why `p < 0.05` Fails Without Base Rates and Power

1. **Positive Predictive Value (PPV) vs. p-value:** Even when $$\alpha = 0.05$$ is obeyed honestly, if only 10% of tested hypotheses are actually true (low base rate) and power is 50%, **almost half of all `p < 0.05` discoveries are false positives!**
2. **The Garden of Forking Paths (p-hacking & Optional Stopping):** Testing multiple subgroups, dropping outliers after seeing results, or peeking early inflates effective $$\alpha$$ from 5% to 30%+.
3. **Publication Bias (File-Drawer Effect):** Journals publish the 5% of noisy studies that cross `p < 0.05` and bury the 95% null studies—exaggerating reported effect sizes (*Type M error*).
4. **The Bayesian Remedy:** Explicitly incorporates prior plausibility, updates continuously without optional-stopping penalties on the likelihood, and reports full posterior distributions rather than binary pass/fail cliffs.

---

## Learning objectives

After this lesson, you need to understand three things. First, why many published studies cannot be replicated. Second, why the p-value is often misunderstood and easily misused. Third, why those problems push the scientific community to look for other ways of inference, including Bayesian statistics.

> **Mini example.** A study reports p-value < 0.05, showing that a new drug is effective, but when another group repeats the exact same design, the effect is no longer seen. This is exactly the kind of situation that gives rise to the replication crisis.
>
> **Quick check.** Does a small p-value really mean the research hypothesis is true?

## 1. What is the replication crisis?

In science, a trustworthy result does not only need to look "nice" in one paper. It needs to be **repeatable** when another group redoes the experiment with a similar procedure.

But in many fields such as psychology, preclinical medicine, or the social sciences, many prominent results have failed to replicate.

![Replication crisis statistics]({{ site.baseurl }}/img/chapter_img/chapter01/replication_crisis_stats.png)

This does not mean every scientist is cheating. Most of the problem lies in the fact that data is often noisy, sample sizes are sometimes small, and the publishing system rewards very strongly the results labeled "statistically significant".

## 2. A very everyday story behind this crisis

Imagine 20 independent research groups all test a hypothesis that is actually false. If each group uses the threshold $$p < 0.05$$, then by chance alone, we still expect about 1 group to find a "significant result".

If exactly the group that finds that "nice" result gets published, while the other 19 groups publish nothing, then the whole scientific literature will look as if the hypothesis had just been supported.

That is one of the most dangerous mechanisms behind the replication crisis.

![Publication bias and the file drawer problem]({{ site.baseurl }}/img/chapter_img/chapter01/publication_bias.png)

## 3. What is a p-value, really?

Here is the standard definition:

> **The p-value is the probability of observing data at least as extreme as the data at hand, assuming the null hypothesis $$H_0$$ is true.**

Put more briefly, the p-value answers the question:

**If the null hypothesis $$H_0$$ is true, is this data unusual?**

For example, if $$H_0$$ says the drug has no effect, and the data show the drug group improved more than the control group, then a small p-value only means that data like this is quite unusual if the null hypothesis is really true.

The problem starts here: that is **not** the question the researcher really wants to know.

Researchers usually want to know how likely the hypothesis is to be true, how strong the evidence is, whether the effect is large, and how trustworthy the result itself is. The p-value does not directly answer those questions.

## 4. An easier way to read the p-value

Suppose a trial gives $$p = 0.03$$. That does **not** mean "the probability that the null hypothesis is true is 3%", nor does it mean "the probability that the drug is effective is 97%".

It only means that if there truly is no effect, the probability of seeing this data or something more extreme is only about 3%.

The difference sounds small, but is actually a large gap in logic.

![The p-value is not the probability that H0 is true]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_h0_probability.png)

*Illustration: the p-value lies in the direction $$P(\\text{data} \\mid H_0)$$, not in the direction $$P(H_0 \\mid \\text{data})$$.*

![1 - p is also not the probability that the research hypothesis is true]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_one_minus_p.png)

*Illustration: taking `1 - p` and treating it as the probability that the research hypothesis is true is a wrong logical leap.*

## 5. The most common misconceptions about the p-value

These are very common misconceptions, even in scientific papers.

### Misconception 1. The p-value is the probability that the null hypothesis is true

Wrong. The p-value is:

$$
P(\text{data or more extreme} \mid H_0),
$$

not:

$$
P(H_0 \mid \text{data}).
$$

![Misconception 1 about the p-value]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_h0_probability.png)

### Misconception 2. A small p-value means a large effect

Wrong. The p-value also depends strongly on sample size: with a very large sample, a very small effect can still give a small p-value; while with a small sample, a relatively large effect may still not be small enough to pass the 0.05 threshold.

![Misconception 2: a small p does not mean a large effect]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_effect_size.png)

### Misconception 3. P-value > 0.05 means there is no effect

Wrong. It may only say that the current data is not strong enough to detect the effect.

![Misconception 3: a large p does not mean there is surely no effect]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_large_p_no_effect.png)

### Misconception 4. 0.049 and 0.051 differ in nature

In fact, they almost do not. But when 0.05 is turned into a rigid pass/fail line, people usually interpret them as two completely different worlds.

![Misconception 4: the 0.05 threshold as a magic boundary]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_alpha_threshold.png)

![Summary of the major misconceptions about the p-value]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_summary.png)

## 6. Why is the p-value easily misused?

When the publishing system rewards "statistically significant" results, researchers are easily pulled into behaviors such as trying many different outcome variables, trying many ways of filtering data, selectively removing outliers, stopping data collection as soon as the threshold is reached, or reporting only the nicest analysis.

Those behaviors do not always stem from cheating. Often they stem from publication pressure and from researchers convincing themselves that they are only "exploring the data".

But the consequence is the same: the false discovery rate rises sharply.

![P-hacking techniques]({{ site.baseurl }}/img/chapter_img/chapter01/phacking_techniques.png)

## 7. Optional stopping: a very common example

Suppose you start with 20 participants and do not yet see a small enough p-value. You recruit 10 more people, then 10 more again, and stop when p < 0.05.

It sounds harmless, but this is a quiet way of raising the probability of finding a "significant result" purely by luck.

In Bayes, sequential updating is much more natural, whereas in classical frequentist testing, stopping when looking at the data can break the original interpretation of the p-value.

### 7.1. A numerical example: keep looking until p < 0.05

Suppose a study starts with 20 participants and gives $$p=0.18$$. The researcher is not satisfied, so recruits 10 more people, and now $$p=0.09$$. Still not "nice" enough, so they recruit 10 more and see $$p=0.047$$, then stop immediately and publish the result as statistically significant.

The problem is not in the number $$0.047$$ alone, but in the fact that the stopping rule depended on the very data being observed. If from the start the plan had been to collect 60 people and only then test, the final p-value could well bounce back to a level like $$0.11$$. Optional stopping therefore increases the chance of "luckily" hitting the threshold, even though the true effect may be very weak or nonexistent.

## 8. Publication bias: what distorts the scientific picture

Even when each individual study does everything right, science can still be distorted if "positive" results are published while "negative" results are left in the drawer.

Then readers only see "successful" studies, and easily think that the evidence for a hypothesis is stronger than it really is.

This is why we cannot evaluate a finding from a single paper alone.

## 9. A famous example: extrasensory perception and extraordinary findings

An example often mentioned is the studies claiming to have evidence for extrasensory perception. Looking only at p-values, some results look "noteworthy". But scientific intuition says that the more extraordinary a claim is, the much stronger the evidence needed.

The p-value cannot distinguish between a very ordinary claim like "aspirin reduces headaches" and an extremely extraordinary claim like "people can see the future". It only scores how "unusual the data is under the null hypothesis".

Bayesian analysis is different in that it allows us to bring in **prior plausibility**. A hypothesis that is very hard to believe from the start will need a much stronger amount of evidence for the posterior to become convincing.

![The Frequentist view: the p-value measures how unusual the data is]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_vs_posterior_frequentist.png)

![The Bayesian view: the posterior speaks directly about the probability we care about]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_vs_posterior_bayesian.png)

## 10. The deeper problem: the p-value answers the wrong question

This is the most important point of the lesson.

Scientists usually want to know which hypothesis is more credible, where the parameter may lie, how strongly the data support this hypothesis, and how much uncertainty remains.

The p-value asks a different question: if the null hypothesis $$H_0$$ is true, is this data unusual or not.

It can be useful in some testing contexts, but it is not the direct answer to the core scientific concern.

## 11. Why does this lesson pave the way for Bayes?

Bayesian statistics is attractive not because it "hates p-values", but because it tries to answer more directly the things we truly care about: the probability of a hypothesis after seeing data, the distribution of unknown parameters, the current level of uncertainty, and how to update beliefs when new information arrives.

Chapter 1 will gradually lead you to exactly that point. This lesson only plays the role of a warm-up: pointing out why so many people have felt that the old way of inference is not enough.

> **3 key ideas.** The replication crisis is not only the fault of individual researchers but also a problem of the whole system of inference and publication incentives; the p-value is easily misunderstood because it answers a different question from the scientific question we truly care about; and when p-values become a target to hit, p-hacking and publication bias appear almost inevitably.

---

### Worked Numerical Example: Computing the True False-Discovery Rate Behind `p < 0.05`

Suppose a lab tests **1,000 hypotheses**, of which only **10%** (100) are truly non-null and **90%** (900) are truly null, using $$\alpha = 0.05$$ and typical statistical power $$1 - \beta = 0.50$$:

| Hypothesis Reality | Count | Significant (`p < 0.05`) | Not Significant |
| :--- | :--- | :--- | :--- |
| **True Effect ($$H_1$$)** | $$100$$ | $$100 \times 0.50 = \mathbf{50}$$ (True Positives) | $$50$$ |
| **No Effect ($$H_0$$)** | $$900$$ | $$900 \times 0.05 = \mathbf{45}$$ (False Positives) | $$855$$ |
| **Total Published (`p < 0.05`)** | $$1{,}000$$ | **$$95$$** | $$905$$ |

Compute the probability that a published `p < 0.05` finding is actually a **false alarm**:
$$\mathrm{FDR} = \frac{45}{50 + 45} = \frac{45}{95} \approx \mathbf{47.4\%}!$$
Nearly **half** of all "statistically significant" findings are false—even with zero cheating!

### Explanation: Four Scientific Habits That Prevent False Discoveries

1. **Always ask "what was the prior base rate?"** Extraordinary claims (e.g., 1% base rate) require far stronger evidence than `p = 0.04` to become credible.
2. **Pre-register hypotheses and report effect sizes with uncertainty:** Replacing binary `p < 0.05` headlines with posterior intervals prevents cliff-chasing.
3. **Shrink small-sample discoveries toward zero:** Hierarchical Bayesian models automatically guard against inflated Type M effect sizes.
4. **Value replication as sequential Bayesian updating:** Yesterday’s posterior becomes today’s prior—science accumulates evidence continuously instead of resetting to zero on every paper.

**Quick check.** In the 1,000-hypothesis table above, if researchers boost statistical power from $$50\%$$ to $$80\%$$ (keeping base rate 10% and $$\alpha = 0.05$$), how many True Positives do they find, and what does the False Discovery Rate drop to?

---

## Reference videos

- [p-values: What they are and how to interpret them](https://www.youtube.com/watch?v=vemZtEM63GY) — StatQuest with Josh Starmer, English. **watch first**. Watch which question the p-value really answers, exactly the part of the lesson that points out the common misreadings.
- [p-hacking: What it is and how to avoid it!](https://www.youtube.com/watch?v=HDCOUXE3HMM) — StatQuest with Josh Starmer, English. Watch p-hacking arise from flexible analysis choices, supporting the argument for why many results do not replicate.
- [The reproducibility crisis and other problems in science | John Ioannidis](https://www.youtube.com/watch?v=vY9mGJQFdyE) — The Institute of Art and Ideas, English. Watch John Ioannidis discuss the replication crisis, used for the part of the lesson linking test misuse to belief in publications.

## Practice questions

1. Why can a study with a small p-value still fail to replicate?
2. Explain in words the difference between $$P(\text{data} \mid H_0)$$ and $$P(H_0 \mid \text{data})$$.
3. Why can a large sample size make an effect that is small and practically meaningless still give a very small p-value?
4. Give an everyday example of publication bias outside science.

## References

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 11.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 1.
- Wasserstein, R. L., & Lazar, N. A. (2016). The ASA Statement on p-Values.

---

*Next lesson: [1.2 Probability as Plausibility - The Bayesian View]({{ site.baseurl }}/contents/en/chapter01/01_02_probability_as_plausibility/)*
