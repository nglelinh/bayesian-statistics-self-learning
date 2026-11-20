---
layout: post
title: "Lesson 8.2: Information Criteria - WAIC and LOO"
chapter: '08'
order: 2
owner: Nguyen Le Linh
lang: en
categories:
- chapter08
lesson_type: required
---

## Learning objectives

After this lesson, you should understand WAIC and LOO as tools for approximating the out-of-sample predictive ability of Bayesian models, and know how to read results in terms of estimation uncertainty rather than with a "hard ranking" mindset. The focus of the lesson is methodological reasoning: why out-of-sample predictive criteria should be preferred, when the difference between models is large enough to conclude, and when to move from model selection to model averaging.

## 1. From training fit to out-of-sample prediction

The classic problem of model comparison is that the more flexible a model is, the more easily it achieves a good training fit, yet that same flexibility can reduce predictive ability on new data. Therefore, the quantity of interest is not the in-sample error but the out-of-sample log predictive density. In pointwise language, we care about the sum

$$
\text{elpd} = \sum_{i=1}^n \log p(y_i\mid y_{-i}),
$$

where each observation is evaluated as a never-before-seen point, with the model having learned from the remaining data.

This idea is very powerful conceptually but computationally expensive if the model must be refit many times; WAIC and PSIS-LOO appear as two practical routes to approximate the same target.

## 2. WAIC: a fully Bayesian approximation of predictive accuracy

WAIC can be written as

$$
\text{WAIC}=-2\,(\text{lppd}-p_{\text{WAIC}}),
$$

where lppd reflects pointwise predictive fit, and $$p_{\text{WAIC}}$$ plays the role of effective complexity that penalizes overfitting. When comparing several models on the same data, a lower WAIC corresponds to better predictive performance (or, equivalently, a larger elpd).

It must be emphasized that WAIC is not an "absolute score" of a model; it only has meaning relative to competing models and must be accompanied by the standard error of the difference.

## 3. PSIS-LOO: closer to the reference standard in practice

Ideal LOO-CV requires leaving out each observation and refitting the model, while PSIS-LOO uses Pareto-smoothed importance sampling to approximate that procedure without refitting the whole model. Because it is closer to the direct out-of-sample definition, LOO is usually preferred in modern workflows, provided the Pareto $$k$$ diagnostic shows that the approximation is reliable enough.

A short reading that still captures the essence: WAIC is usually fast and convenient; PSIS-LOO is usually more trustworthy; both must be interpreted together with estimation uncertainty.

![WAIC and LOO comparison with uncertainty]({{ site.baseurl }}/img/chapter_img/chapter08/chapter08_waic_loo_comparison.png)

### Experiment: WAIC and LOO estimate out-of-sample predictive quality

Increase the polynomial degree step by step: the in-sample lppd always rises, while the elpd by WAIC and LOO (which tracks the elpd on new data closely) peaks and then falls. The table gives p_waic, Δelpd and the standard error.

<div class="interactive-demo" markdown="1">
<div data-demo="ic-explainer" data-lang="en" data-tab="waic"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 4. Reading the model comparison table: differences and uncertainty

Suppose three models give the following results on the elpd scale (higher is better):

- Model A: elpd = -221, SE = 5
- Model B: elpd = -220, SE = 5.5
- Model C: elpd = -229, SE = 6

The reasonable conclusion is that C is clearly worse than A and B, but A and B are almost tied because a difference of 1 point is considerably smaller than the accompanying uncertainty. In this situation, declaring "B wins" is an over-reading; the more mature choice is to treat A and B as a set of nearly equally competitive models, then consider averaging or prefer the more interpretable model if communication goals matter.

## 5. Pareto k: the reliability condition of PSIS-LOO

For PSIS-LOO, the Pareto $$k$$ index answers the question: are the importance sampling weights stable? A commonly used practical threshold is:

- $$k<0.5$$: very stable,
- $$0.5\le k\le 0.7$$: usable but needs care,
- $$k>0.7$$: the approximation may be unreliable; check carefully and consider alternative measures.

The important point is that Pareto $$k$$ is not a minor detail. If the diagnostic fails, the LOO ranking table may look nice but no longer has a solid enough foundation for decisions.

## 6. A methodological example: when is there "enough evidence" to choose a model

Suppose the best model has an elpd 6 points higher than the second-best model, while the standard error of the difference is about 2. Then we can regard the gap as convincing enough to choose the best model for the predictive goal. Conversely, if the difference is only 1.5 with a standard error of 2.2, the scientific conclusion should be "not clearly distinguishable yet", and the more sensible strategy is usually averaging or keeping several models for different goals.

In other words, model comparison in Bayesian statistics is an inference problem under uncertainty, not a scoring contest with a single number.

## 7. Good practice when using WAIC/LOO

Good practice can be summarized in three principles. First, always compare on the same data and the same target variable so that the difference has meaning. Second, read the estimate and the SE together instead of looking only at the rank. Third, if several models are close, move from "winner-takes-all" logic to combining predictions.

From the workflow perspective, WAIC/LOO does not replace PPC: a model with a better predictive score can still be wrong in mechanism in regions the problem cares about especially, so model criticism and model comparison must be used as complements, not substitutes.

## 8. Conclusion of Lesson 8.2

WAIC and LOO provide a quantitative language for comparing models by out-of-sample predictive ability, but their greatest value lies in disciplined interpretation: always read differences together with uncertainty, always check the diagnostics of the approximation, and always tie the model-choice decision to a concrete predictive goal rather than to the habit of choosing the top rank.

Next lesson: **Model Comparison Strategies**, where we go deeper into the choice between selection, averaging, and expansion.

## Reference videos

- [Evaluating model fit through AIC, DIC, WAIC and LOO-CV](https://www.youtube.com/watch?v=xS4jDHQfP2o) — Ben Lambert, English. **watch first**. Watch AIC, DIC, WAIC and LOO-CV placed side by side as ways of estimating out-of-sample predictive ability.
- [BDA 2019 Lecture 9.1 PSIS-LOO and K-fold cross-validation](https://www.youtube.com/watch?v=D0kVMie93Yk) — Aki Vehtari, English. Watch Aki Vehtari present PSIS-LOO and K-fold, supporting the part where the lesson prefers LOO over in-sample fit.
- [31- Pareto k diagnostics in R](https://www.youtube.com/watch?v=h4g5KUWRzyg) — Horizon 2 Reach, English. Watch the Pareto k diagnostic, exactly the condition the lesson requires before trusting a PSIS-LOO estimate.

## Practice questions

1. Why is a WAIC/LOO difference smaller than the standard error of the difference not enough to declare a model the winner?
2. If a model ranks first but has many points with Pareto $$k>0.7$$, how would you handle that result?
3. When do you prefer model averaging over choosing a single model?

## References

- Vehtari, A., Gelman, A., & Gabry, J. (2017). "Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC." *Statistics and Computing*.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd Edition), Chapter 7.

---

*Next lesson: [8.3 Model Comparison Strategies]({{ site.baseurl }}/contents/en/chapter08/08_03_model_comparison/)*
