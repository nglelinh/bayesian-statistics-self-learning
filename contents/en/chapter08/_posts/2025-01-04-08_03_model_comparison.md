---
layout: post
title: "Lesson 8.3: Model Comparison Strategies"
chapter: '08'
order: 3
owner: Nguyen Le Linh
lang: en
categories:
- chapter08
lesson_type: required
---

## Learning objectives

After this lesson, you should clearly distinguish three model comparison strategies in Bayesian statistics: choosing one model (selection), combining several models (averaging), and expanding the model to encompass the others (expansion). The central point is not to treat model comparison as a mechanical ranking procedure, but as a decision problem under model uncertainty, where the choice of strategy depends on how well separated the predictive performance is and on the application goal.

## 1. Comparing models is not always about picking a winner

When several competing models have very similar predictive ability, being forced to choose exactly one model easily creates a false sense of certainty. Conversely, when one model is clearly superior and stable across checks, keeping several models only adds complexity without adding predictive value. So the right question is not "which model ranks first", but "which strategy produces the most useful forecasts with the most honest uncertainty".

## 2. Strategy A - Model selection

Model selection is appropriate when the out-of-sample predictive gap between the best model and the rest is large relative to the estimation uncertainty. In that case, the cognitive cost of maintaining several models usually outweighs the benefit, and a single model allows simpler interpretation, communication, and deployment.

However, the hidden condition of selection is sufficiently strong separation. If the difference in predictive metrics is small and unstable, selection can make the whole pipeline depend on random sampling fluctuation rather than on real structural signal.

### Experiment: the Bayes factor is a ratio of marginal likelihoods

Flip one at a time and watch the cumulative BF₁₀ = m₁(k)/m₀(k); the marginal likelihood penalizes a model that spreads its probability thinly (the Occam effect).

<div class="interactive-demo" markdown="1">
<div data-demo="bf-explainer" data-lang="en" data-tab="seq"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 3. Strategy B - Model averaging

Model averaging follows the principle of "preserving model uncertainty" by combining predictive distributions:

$$
p(\tilde y\mid y)=\sum_{k=1}^{K} w_k\,p_k(\tilde y\mid y),\qquad \sum_k w_k=1,\; w_k\ge 0.
$$

In modern practice, stacking weights are usually preferred because they directly optimize the predictive ability of the combined distribution, instead of trying to assign an absolute "right/wrong" probability to each model.

### Experiment: model averaging with pseudo-BMA weights

Add models to the group one at a time and watch the weights w ∝ exp(elpd_loo) and the averaged prediction change.

<div class="interactive-demo" markdown="1">
<div data-demo="ic-explainer" data-lang="en" data-tab="avg"></div>
</div>

### 3.1. A short quantitative example

Suppose that at a new prediction point, model A gives a mean of 52, model B gives 56, and the stacking weights are 0.58 and 0.42 respectively. The mean prediction of the combined model is then

$$
0.58\times 52 + 0.42\times 56 = 53.68.
$$

This value reflects both the signals of the two models and the structural uncertainty that exists between them, instead of forcing a choice of 52 or 56 as two mutually exclusive scenarios.

![Selection vs Stacking predictive distributions]({{ site.baseurl }}/img/chapter_img/chapter08/chapter08_selection_vs_stacking.png)

### Experiment: the BF depends on the prior width

Change the Beta(c, c) prior of M₁ and watch BF₁₀ change — the reason a sensitivity analysis is needed.

<div class="interactive-demo" markdown="1">
<div data-demo="bf-explainer" data-lang="en" data-tab="prior"></div>
</div>

## 4. Strategy C - Model expansion

Model expansion is appropriate when the candidate models represent different pieces of the same data-generating mechanism and can be merged into one larger model, for example by adding a nonlinear component, hierarchical group effects, or regularized interactions. The advantage of expansion is a single consistent inference framework instead of maintaining several disconnected models; the risk is higher computational complexity and the need for stronger checks to avoid overfitting.

A useful way to read it: selection resolves competition between models; averaging resolves uncertainty between models; expansion resolves the structural deficiency of the existing set of models.

## 5. Rules for choosing a strategy in practice

A working rule can be stated as follows. If the difference in predictive performance is large and stable, prefer selection. If several models are nearly tied, prefer averaging to preserve uncertainty. If all models reveal mechanism misfit in PPC, prefer expansion instead of continuing to argue about who is "least wrong".

The important point is that this rule must always go together with diagnostic checks (for example Pareto $$k$$ in LOO) and the results of model criticism. A nice rank table cannot replace evidence that the model still misses important data structure.

## 6. A combined example: same data, three different decisions

Suppose we have three models M1, M2, M3, and the LOO results show that M1 and M2 are close within the standard error, while M3 is clearly worse. When the goal is stable short-term forecasting, averaging between M1 and M2 is usually more sensible than selection. If the goal is to explain the mechanism and M1 is considerably simpler, selection may still be chosen provided the remaining model uncertainty is clearly reported. Conversely, if PPC shows that both M1 and M2 are wrong in the tail, the best decision is neither to choose nor to mix, but to expand in order to fix the data-generating mechanism properly.

This example shows that model comparison is a multi-objective decision: prediction, interpretation, deployment cost, and honesty about uncertainty.

## 7. Conclusion of Lesson 8.3

There is no single correct model comparison strategy for every context. Selection, averaging, and expansion are three complementary tools in the same Bayesian workflow. An analyst's ability lies not in remembering the names of the tools, but in knowing when to reduce uncertainty by choosing a model, when to keep uncertainty by combining models, and when to redesign the model to fix mechanism misfit.

Next lesson: **Bayesian Decision Analysis**, where model results are turned into the optimal choice of action under a concrete loss.

## Reference videos

- [Statistical Rethinking 2023 - 20 - Horoscopes](https://www.youtube.com/watch?v=qwF-st2NGTU) — Richard McElreath, English. **watch first**. Watch why a model ranking table is not a prophecy, exactly the argument by which the lesson refuses to pick a winner at all costs.
- [16a Prediction and Model Averaging](https://www.youtube.com/watch?v=707hT6qYghw) — Philip Ramsey, English. Watch model averaging when the models all make predictions, supporting the strategy of combining instead of choosing one model.
- [Statistical Rethinking 2026 - Lecture B02 - Multilevel Model Expansion](https://www.youtube.com/watch?v=Nv2rm1s9q6I) — Richard McElreath, English. Watch multilevel model expansion, used for the expansion strategy that the lesson places next to selection and averaging.

## Practice questions

1. When two models differ in LOO by very little relative to the SE, why can selection be less honest than averaging?
2. When is expansion better than both selection and averaging?
3. If the main goal is causal interpretation, how would you change your strategy priorities compared with a purely predictive goal?

## References

- Yao, Y., et al. (2018). "Using stacking to average Bayesian predictive distributions." *Bayesian Analysis*.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd Edition).

---

*Next lesson: [8.4 Bayesian Decision Analysis]({{ site.baseurl }}/contents/en/chapter08/08_04_decision_analysis/)*
