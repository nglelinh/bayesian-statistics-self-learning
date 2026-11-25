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

You run `az.compare({"M1": idata1, "M2": idata2})` and see `M2` beat `M1` by `elpd_diff = 1.8`. Should you throw `M1` in the trash and declare `M2` the winner? Look one column to the right: `dse = 2.9`! The difference is *smaller than its own standard error*—picking one "winner" here is pure coin-flipping!

This lesson teaches mature **Bayesian Model Comparison**: reading `elpd_diff` alongside its paired standard error `dse`, understanding **Bayes Factors** (and why they depend strongly on prior width!), and combining competing models cleanly via **Bayesian Stacking / Model Averaging** instead of forcing a brittle winner-take-all choice.

---

## Key ideas: Three Complementary Lenses for Model Comparison

1. **Predictive Comparison (LOO-CV `elpd_diff` vs. `dse`):** Compares *pointwise* predictive differences $$d_i = \mathrm{elpd}_{i, M_2} - \mathrm{elpd}_{i, M_1}$$. Because both models are evaluated on the exact same observations, pairing cancels out shared noise—giving a clean paired SE (`dse`). Rule of thumb: $$\lvert\Delta\mathrm{elpd}\rvert > 2\text{–}4 \times \mathrm{dse}$$ signals a clear predictive win!
2. **Marginal Likelihood & Bayes Factors ($$\mathrm{BF}_{12} = \frac{p(y\mid M_1)}{p(y\mid M_2)}$$):** Measures relative evidence under prior predictive distributions. Powerful for nested scientific hypotheses, yet **highly sensitive to prior width** (making a prior 10× wider penalizes that model’s Bayes Factor by 10×!).
3. **Bayesian Model Averaging & Stacking (Yao et al.):** When two models are neck-and-neck (`elpd_diff < 2 * dse`), don’t discard one! **Stacking** finds optimal non-negative weights $$w_1 + w_2 = 1$$ maximizing combined LOO predictive density—preserving model uncertainty in predictions!
4. **Causal Goal ≠ Predictive Goal:** Use DAGs to choose causal models; use LOO/Stacking to optimize predictive accuracy.

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

---

### Worked Numerical Example: Reading Two Real `az.compare` Tables Side by Side

**Scenario 1 — Clear Winner:**
- Model A (`Simple Linear`): `elpd_loo = -142.0`
- Model B (`Hierarchical Spline`): `elpd_loo = -129.6`
- Difference: $$\Delta\mathrm{elpd} = \mathbf{+12.4}$$, paired $$\mathrm{dse} = \mathbf{3.1}$$ $$\implies z = 12.4 / 3.1 = \mathbf{4.0}$$ (decisive predictive superiority for Model B!).

**Scenario 2 — Too Close to Call (Use Stacking!):**
- Model C (`Poisson`): `elpd_loo = -210.4`
- Model D (`NegBin`): `elpd_loo = -208.6`
- Difference: $$\Delta\mathrm{elpd} = \mathbf{+1.8}$$, paired $$\mathrm{dse} = \mathbf{2.9}$$ $$\implies z = 1.8 / 2.9 = \mathbf{0.62}$$!
- Rather than betting 100% on one model, **Stacking** might assign weights $$w_D = 0.65,\; w_C = 0.35$$, combining their posterior predictive draws cleanly!

### Explanation: Four Rules for Wise Bayesian Model Comparison

1. **Always check `dse` (difference SE), never the individual models’ `se`:** Individual `se` includes observation-to-observation difficulty; paired `dse` measures the true uncertainty in *Model B minus Model A*.
2. **Never use flat/uninformative priors when computing Bayes Factors:** Under improper or arbitrarily wide priors, Bayes Factors automatically favor the simpler model (Lindley’s Paradox) regardless of the data!
3. **When models tie on LOO, prefer the simpler, better-regularized, or causally grounded model—or stack them.**
4. **Always run PPCs on the winning model too:** Being the "best" of three bad models still leaves you with a bad model!

**Quick check.** If Model 2 beats Model 1 by `elpd_diff = 3.0` with a paired `dse = 4.5`, do you have strong evidence that Model 2 predicts better out of sample—and what should you do instead of discarding Model 1?

---

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
