---
layout: post
title: "Lesson 8.4: Bayesian Decision Analysis - From Inference to Action"
chapter: '08'
order: 4
owner: Nguyen Le Linh
lang: en
categories:
- chapter08
lesson_type: required
---

## Learning objectives

After this lesson, you should be able to turn Bayesian inference results into concrete actions under uncertainty, through loss functions, expected loss, and the value of information. The focus of the lesson is to understand that the posterior answers the question "what do we believe", while decision theory answers a completely different question: "what should we do" when each choice carries asymmetric costs.

## 1. Inference is not the same as decision

A very sharp posterior does not automatically produce the right decision, because a decision always also depends on the consequences of mistakes. The same posterior probability can lead to two different actions if the damage structure changes. This is why decision analysis is the mandatory final stage of the Bayesian workflow, not a decorative add-on after inference.

The standard framework has four components: the action set $$a\in\mathcal A$$, the state of the world $$\theta$$, the posterior $$p(\theta\mid y)$$ and the loss $$L(a,\theta)$$. The Bayes action rule is to choose

$$
a^*(y)=\arg\min_{a\in\mathcal A} \mathbb E[L(a,\theta)\mid y]
=\arg\min_{a\in\mathcal A}\int L(a,\theta)p(\theta\mid y)\,d\theta.
$$

## 2. A threshold rule from asymmetric costs

Consider a risk-alert problem with two actions: alert ($$a_1$$) and no alert ($$a_0$$). Let $$q=P(H_1\mid y)$$ be the posterior probability of an incident, $$L_{FP}$$ the cost of a false alarm, and $$L_{FN}$$ the cost of missing an incident. Then

$$
R(a_1\mid y)=L_{FP}(1-q),\qquad R(a_0\mid y)=L_{FN}q.
$$

We choose to alert if $$R(a_1\mid y)<R(a_0\mid y)$$, which is equivalent to

$$
q>\frac{L_{FP}}{L_{FP}+L_{FN}}.
$$

With $$L_{FP}=5$$ and $$L_{FN}=40$$, the decision threshold is only $$q^*=5/45\approx 0.111$$. This shows an important methodological point: the optimal decision can be very "sensitive" to costs, even when the posterior does not change.

![Expected loss threshold rule]({{ site.baseurl }}/img/chapter_img/chapter08/chapter08_expected_loss_threshold.png)

### 2.1. A business-meaning example

If missing an incident causes losses many times larger than a false alert, a reasonable organization will alert earlier, that is, use a lower posterior threshold. Conversely, if a false alert is very expensive, the posterior threshold needs to be higher to avoid over-acting. The optimal rule is therefore never a "universal" number; it is a function of the loss structure in the specific context.

### Experiment: the decision threshold in an A/B test

Add batches of 150 users one at a time, track π = P(p > p₀) and compare it with the threshold c_fp/(c_fp + c_fn).

<div class="interactive-demo" markdown="1">
<div data-demo="decision-explainer" data-lang="en" data-tab="threshold"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 3. Loss functions and posterior summaries

In point estimation, the choice of mean, median, or mode is not a presentation preference but is determined by the loss:

- squared loss $$L(\hat\theta,\theta)=(\hat\theta-\theta)^2$$ -> the optimum is the posterior mean,
- absolute loss $$L(\hat\theta,\theta)=|\hat\theta-\theta|$$ -> the optimum is the posterior median,
- 0-1 loss (discrete) -> the optimum is the posterior mode.

The methodological conclusion here is: any report of a "representative point estimate" implicitly contains a view about the cost of error, whether or not we are aware of it.

### Experiment: each loss function gives a different optimal summary

Squared → mean, absolute value → median, 0–1 → mode, asymmetric → quantile.

<div class="interactive-demo" markdown="1">
<div data-demo="decision-explainer" data-lang="en" data-tab="loss"></div>
</div>

## 4. From evidence to action: the role of the Bayes factor

For two hypotheses $$H_0,H_1$$, the Bayes factor is defined as:

$$
BF_{10}=\frac{p(D\mid H_1)}{p(D\mid H_0)}.
$$

It updates the odds through

$$
\frac{P(H_1\mid D)}{P(H_0\mid D)}=BF_{10}\times\frac{P(H_1)}{P(H_0)}.
$$

However, even when $$BF_{10}$$ leans strongly toward $$H_1$$, the final action must still pass through the expected loss. The Bayes factor answers the question "which hypothesis does the data support"; decision analysis answers a different one: "under the current cost structure, which action is optimal".

## 5. Value of Information: when to collect more data

Adding data is not always worth it. The value of information is measured by the reduction in expected loss:

$$
\text{VOI}=\mathbb E[L\mid \text{decide now}] - \mathbb E[L\mid \text{with extra information}].
$$

The action rule is very clear:

$$
\text{Collect more data if } \text{VOI} > \text{collection cost}.
$$

For example, if the current expected loss is 12 and after adding information it could drop to 5, then VOI = 7. If the cost of obtaining the information is 4, the net benefit is positive and we should collect it; if the cost is 10, the net benefit is negative and we should decide now with the information we have.

![Value of information decision curve]({{ site.baseurl }}/img/chapter_img/chapter08/chapter08_voi_decision_curve.png)

### Experiment: EVSI and the optimal sample size

Compare the expected value of an extra sample with its collection cost to choose the sample size.

<div class="interactive-demo" markdown="1">
<div data-demo="decision-explainer" data-lang="en" data-tab="voi"></div>
</div>

## 6. A combined example: an A/B testing decision

Suppose two product versions A and B have posterior conversion rates $$p_A$$ and $$p_B$$. The inference part gives us the probability $$P(p_B>p_A\mid D)$$, but the rollout decision should not rest mechanically on this probability. We need to model the business utility/loss: the value of each conversion, the rollout cost, the risk of loss if we choose wrongly, and the time available to react. The optimal action is then the one with the highest expected utility (or the lowest expected loss), not necessarily the one with the highest posterior probability under a fixed threshold.

This is an important intersection between statistics and management: with the same posterior, businesses with different cost structures will have different optimal decisions.

## 7. A workflow template for decision analysis

A rigorous practical procedure usually goes through four steps: (i) identify the set of actions that can be executed, (ii) define a clear loss/utility that can be defended on business grounds, (iii) compute the expected loss based on the posterior/predictive, and (iv) check the sensitivity of the decision when the loss assumptions change. Step (iv) is especially important because many decisions can flip when costs are re-evaluated.

From a scientific viewpoint, a good Bayesian decision is not one that is "certainly right", but one that is optimal given the current information and a transparently declared loss structure.

## 8. Conclusion of Lesson 8.4

Bayesian decision analysis completes the cycle of Chapter 08: PPC helps detect where the model is wrong, WAIC/LOO helps compare predictive ability, model comparison strategies help handle model uncertainty, and decision theory turns all of that information into concrete action. If inference is the science of belief under uncertainty, then decision analysis is the discipline that turns that belief into a responsible choice.

**Chapter 08 Complete**: model criticism -> model comparison -> decision.

## Reference videos

- [(ML 11.3) Frequentist risk, Bayesian expected loss, and Bayes risk](https://www.youtube.com/watch?v=b1GxZdFN6cY) — mathematicalmonk, English. **watch first**. Watch expected loss and Bayes risk, exactly the step where the lesson goes from the posterior to an action under a loss.
- [Decision Analysis 2: EMV & EVPI - Expected Value & Perfect Information](https://www.youtube.com/watch?v=tbv9E9D2BRQ) — Joshua Emmanuel, English. Watch the expected value of perfect information, supporting the value-of-information part.
- [Decision Theory: Loss Functions & Bayes Criterion (Worked Example 3)](https://www.youtube.com/watch?v=c7_L0-0Bvs8) — StatsResource, English. Watch a decision problem with a concrete loss function, used to see how the same probability can lead to two different actions.

## Practice questions

1. Why can two organizations with the same posterior about a risk arrive at two different optimal actions?
2. If the cost of a false alarm doubles, in which direction does the threshold $$q^*$$ change?
3. When VOI is positive but very close to the collection cost, what should you check before deciding to collect more data?

## References

- Berger, J. O. (1985). *Statistical Decision Theory and Bayesian Analysis*.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd Edition), Chapter 9.

---

*Next chapter: [Chapter 12: Bayesian Hands-on Labs]({{ site.baseurl }}/en/chapter12/)*
