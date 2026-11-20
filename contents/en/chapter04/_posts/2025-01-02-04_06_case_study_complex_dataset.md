---
layout: post
title: "Lesson 4.6: Advanced Case Study - Model Checking & Prediction on a Complex Dataset"
chapter: '04'
order: 7
owner: Nguyen Le Linh
lang: en
categories:
- chapter04
lesson_type: required
---

## Learning objectives

After this lesson, you need to grasp how to run a full Bayesian workflow on data with complex structure, where "being able to fit the model" is only a necessary condition and never a sufficient one. The focus of the lesson is not on being able to write one more regression equation, but on reasoning ability: from diagnosing a deviation, identifying its form, to proposing model revisions that fix the real cause instead of fixing by technical intuition.

> **Opening example.** In the diamonds data, `carat` and `price` are very highly correlated, but a simple linear model can still fail badly in the tail of the price distribution, that is, right in the "safe" region but wrong in the region of greatest economic value.
>
> **Quick check.** Why is a very nice summary metric such as a correlation of 0.9+ still not enough to conclude that the model is trustworthy for real-world prediction?

## 1. Data context: why `diamonds` is a hard test

We use the `diamonds` dataset (seaborn), with the response variable `price` and many variables describing both geometric size and perceived quality such as `carat`, `cut`, `color`, `clarity`, `depth`, `table`. What gives this dataset high pedagogical value is that it forces us to face three layers of complexity at once: a strong relationship that is not homogeneous across the whole predictor domain, a group structure with real meaning, and the tail behavior of the response that directly affects the quality of decision-making.

### 1.1. Excerpt of the observed data

| carat | cut | color | clarity | depth | table | price | x | y | z |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|
| 0.23 | Ideal | E | SI2 | 61.5 | 55.0 | 326 | 3.95 | 3.98 | 2.43 |
| 0.21 | Premium | E | SI1 | 59.8 | 61.0 | 326 | 3.89 | 3.84 | 2.31 |
| 0.23 | Good | E | VS1 | 56.9 | 65.0 | 327 | 4.05 | 4.07 | 2.31 |
| 0.29 | Premium | I | VS2 | 62.4 | 58.0 | 334 | 4.20 | 4.23 | 2.63 |
| 0.31 | Good | J | SI2 | 63.3 | 58.0 | 335 | 4.34 | 4.35 | 2.75 |

### 1.2. Quantitative summary to lay the groundwork for the argument

With `n = 53,940`, the variable `carat` has a mean of approximately 0.798 and a median of about 0.70, while `price` has a mean of about 3932.8 but a median of only about 2401, showing that the price distribution is considerably right-skewed. The Pearson correlation between `carat` and `price` is about 0.922, i.e. extremely strong at the overall level; yet the proportion of observations falling in the region `price > 15000` is still only about 3.07%, and this small region is exactly where every model deviation becomes the most costly if the problem is used for high-end pricing.

## 2. From numbers to argument: we must prove with formulas

A serious analysis is not allowed to stop at wording like "it seems" or "it looks like". Every key conclusion needs a corresponding statistical object and measurement.

The sample correlation coefficient between `carat` and `price` is defined by

$$
r_{xy}=\frac{\sum_{i=1}^{n}(x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum_{i=1}^{n}(x_i-\bar x)^2}\sqrt{\sum_{i=1}^{n}(y_i-\bar y)^2}},
$$

and gives a value of about 0.922. This number only lets us state that the fluctuations of `carat` and `price` move strongly in phase in the global linear sense; it in no way guarantees that the residuals are random around 0, in no way guarantees homogeneous error variance, and in no way vouches that the model predicts well in the right tail. In other words, a high correlation is evidence of signal, not evidence of the correctness of the structure of the data-generating model.

Similarly, the statement "the right tail is rare" must also have a clear definition:

$$
\hat p_{\text{price}>15000}=\frac{1}{n}\sum_{i=1}^{n}\mathbf 1(y_i>15000)\approx 0.0307.
$$

Although this proportion is only around 3%, the tail region has outsized economic weight in many practical problems; therefore, a model that is right in the center but wrong in the tail is still a high-risk model if the application goal is pricing, premium portfolio control, or evaluating extreme scenarios.

Finally, to check the assumption of homogeneous variance, we can use the directional indicator

$$
\operatorname{corr}(\lvert e_i \rvert,x_i), \qquad e_i=y_i-\hat y_i,
$$

because when the residual magnitude moves together with the predictor, the assumption of "one common noise level for the whole domain" becomes hard to defend empirically.

## 3. The baseline model: necessary as a baseline, but cannot be the destination

We start with the baseline Gaussian linear model

$$
\text{price}_i \sim \mathcal N(\mu_i,\sigma), \qquad \mu_i=\alpha+\beta\,\text{carat}_i,
$$

**not because we believe the real world is that simple, but because every later improvement needs a benchmark to compare against. The baseline is an instrument for measuring progress, not a declaration of truth**. On `diamonds`, the baseline usually reproduces the average trend fairly well, but easily reveals three limitations: the error width grows with `carat`, the right-tail behavior of `price` is squeezed thin, and structural differences by `cut`/`clarity` are not described.

## 4. Multi-level posterior predictive checks: from global to conditional

In complex data, a single PPC is almost always insufficient. We need a structured series of checks, going from broad questions to narrow ones, to know where the model is right and where it is wrong.

At the global level, we compare the observed distribution with the posterior predictive distribution to see whether the model preserves the central location, spread and tail thickness simultaneously; this is the step that quickly eliminates grossly wrong models.

![Comparing observed data and the posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_observed_vs_predicted.png)

At the target-statistic level, instead of vaguely saying "it looks similar", we force the model to answer with specific quantities:

$$
T_1(y)=\bar y,\quad T_2(y)=\operatorname{Var}(y),\quad T_3(y)=Q_{0.95}(y),\quad T_4(y)=\mathbf 1(y>15000).
$$

If the model matches $$T_1$$ well but deviates considerably at $$T_3$$ or $$T_4$$, the valid conclusion cannot be "the model is good", but must be "the model is good in the center, weak in the tail"; this distinction is decisive when the analysis goal directly concerns high-value risk.

![PPC cho mean]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_test_stat_mean.png)

![PPC cho variance]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_variance_check.png)

At the level conditional on the predictor, we check each `carat` band instead of mixing everything into one common distribution. The idea is that the same model can be right in the central region but systematically wrong in the large-`carat` region, where the range of price fluctuation is considerably wider. Quantitatively, we can track

$$
T_{\text{bin},k}(y)=\operatorname{Var}(y\mid x\in B_k),\qquad T^{(0.95)}_{\text{bin},k}(y)=Q_{0.95}(y\mid x\in B_k),
$$

and compare the observed value with the posterior predictive distribution of each bin.

At the quality-group level, data like `diamonds` forces us to check the ability to reproduce differences between the groups `cut`, `clarity`, `color`. If the model only uses `carat`, failing to reproduce the group means

$$
T_g(y)=\bar y_g
$$

is not a "small error", but evidence that the generative story is missing an important structural mechanism.

## 5. Residual analysis: where the model is questioned most severely

If the PPC gives us the picture at the distribution level, residual analysis gives us a microscope at the mechanism level. The central question is not "are the residuals small" but "do the residuals still carry structured information". When the residuals still have structure, the model has not yet learned all of the data-generating law.

![Signs of heteroskedasticity on the scatter plot]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_scatter.png)

![Residuals vs fitted: fan shape]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_residuals.png)

![Q-Q plot when the residual tails deviate]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonnormal_qq.png)

In the `diamonds` case, a fan shape in residual-vs-fitted usually strongly suggests that uncertainty grows with price level or size, while the deviation on the Q-Q plot shows that a simple Normal assumption may not be flexible enough to describe the tail. The direct consequence is that the prediction interval in the high-`carat` region is easily artificially narrow if we insist on keeping the baseline model.

## 6. Prediction for decisions: distinguishing the two kinds of uncertainty correctly

A point often overlooked in practical reports is the difference between the uncertainty of the conditional mean and the uncertainty of a new observation. These two objects are described by

$$
p(\mu_*\mid y,x_*) \quad \text{and} \quad p(\tilde y_*\mid y,x_*),
$$

where the second distribution is always wider because it includes the noise of the new observation. If we use the interval of $$p(\mu_*\mid y,x_*)$$ to make a statement about one specific diamond, we have created false confidence by definition.

For prediction problems, an important operational indicator is out-of-sample coverage:

$$
\text{Coverage}_{90\%}=\frac{1}{m}\sum_{j=1}^{m}\mathbf 1\{y_j^{\text{test}}\in \text{PI}_{90\%}(x_j)\}.
$$

When coverage drops clearly in the large-`carat` region, that is empirical evidence that the model is not yet suitable for real-world use in the high-price segment, regardless of how nice the overall metrics may be.

## 7. Model revision: from symptom to intervention

A mature workflow does not stop at diagnosis; it must turn diagnosis into an intervention with a mechanism. In other words, each model modification is considered valid only when we can answer three questions at once: which symptom of the data is being addressed, which mathematical component of the model is changed to address that symptom, and which post-hoc evidence allows us to conclude that the change truly takes effect rather than merely making the model look better in form.

In the `diamonds` case, three clusters of symptoms usually appear together: the right tail of `price` is thicker than the simple Gaussian predicts, the residual magnitude grows with `carat`, and there is conditional deviation by quality group. From there, the three intervention directions with the clearest theoretical basis are transforming the response scale, loosening the linear structure of the mean function, and bringing group effects into the generative story.

### 7.1. Intervention 1: log transform to handle the right tail and multiplicative noise

When the `price` distribution is strongly right-skewed, the assumption of additive noise on the original scale is often no longer appropriate. A more mechanism-rich way to put it is to view the error as multiplicative, i.e. relative fluctuation is more stable than absolute fluctuation. Then the model

$$
\log(\text{price}_i) \sim \mathcal N(\mu_i,\sigma),
$$

is not just a technical trick, but a statement about the data-generating mechanism: percentage uncertainty is more reasonable than absolute uncertainty across very different price levels. The practical effect expected after this intervention is a more balanced residual distribution, a lower heteroskedasticity indicator, and a prediction interval in the large-`carat` region that is less artificially narrow.

However, the log transform brings the requirement of correct interpretation when returning to the original scale. If the posterior on the log scale has conditional mean $$\mu_*$$ and standard deviation $$\sigma_*$$, the expected value on the price scale is not simply $$\exp(\mu_*)$$ but

$$
\mathbb E[\text{price}_*\mid y,x_*]=\exp\!\left(\mu_*+\frac{\sigma_*^2}{2}\right),
$$

so prediction reports need to be consistent with the transformation to avoid systematic underestimation on the original scale.

![Illustration of intervention 1: the log transform reduces heteroskedasticity and improves coverage in the high-carat region]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_46_intervention_log_transform.png)

### 7.2. Intervention 2: replace rigid linearity with controlled nonlinear structure

If the residuals show leftover curvature, the problem is not in the noise but in the form of the mean function. Then the right change is to loosen the model

$$
\mu_i=\alpha+\beta\,\text{carat}_i
$$

into a more flexible function, for example

$$
\mu_i=\alpha+f(\text{carat}_i), \qquad f(\cdot)=\sum_{k=1}^{K} w_k B_k(\cdot),
$$

where $$B_k$$ are basis functions (spline/piecewise basis) and the prior on $$w_k$$ plays the role of regularization to avoid overfitting. The key point is that "controlled nonlinearity" is fundamentally different from adding arbitrary polynomials: we increase the representational capacity exactly for the curvature the residuals detect, but still maintain Bayesian discipline through the prior to preserve generalization.

The expected result after the intervention is that the posterior mean line hugs the data more closely at both the low and high ends of `carat`, while the conditional PPC in each predictor bin improves in step rather than only in the center.

![Illustration of intervention 2: a nonlinear model captures the curvature of the carat-price relationship better than a linear one]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_46_intervention_nonlinear.png)

### 7.3. Intervention 3: bring group structure into the generative story via partial pooling

When the data contains grouping variables such as `cut`, `color`, `clarity`, a model with one continuous variable can hardly reproduce the structural differences between quality segments. Instead of adding independent dummy variables in a purely technical way, the more natural Bayesian approach is a hierarchical model, for example with group-wise intercepts:

$$
\mu_i=\alpha_{g(i)}+f(\text{carat}_i), \qquad \alpha_g\sim\mathcal N(\alpha_0,\tau_\alpha).
$$

Partial pooling reconciles two extremes: it does not force all groups to be identical (complete pooling), but also does not leave each group excessively free (no pooling). A very important methodological consequence is that groups with little data are "shrunk" toward the center in a principled way, thereby reducing estimation variance and increasing out-of-sample prediction stability.

If, after introducing group effects, the group-wise PPC is still unsatisfactory, that is a signal that the current group structure is not enough: group-specific slopes, interactions between `carat` and quality, or modeling errors that differ by segment may be needed.

![Illustration of intervention 3: adding group structure makes calibration by cut closer to the observed data]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_46_intervention_group_effects.png)

### Experiment: partial pooling shrinks the groups toward the overall mean

Increase τ from complete pooling to no pooling; compare with the posterior distribution of τ.

<div class="interactive-demo" markdown="1">
<div data-demo="pooling-explainer" data-lang="en"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

### 7.4. Evaluation protocol after each intervention: when we may say "it is better"

A modification should only be accepted when it passes post-hoc evaluation under the same set of criteria, including global PPC, tail PPC, PPC conditional on predictor bins, residual diagnostics, and out-of-sample coverage. In principle, the new model needs to satisfy two conditions at once: (i) reduce the deviation in the target symptom, and (ii) not create considerable deterioration in regions that were previously fine. If it only improves one plot but worsens coverage in the decision region, that intervention cannot yet be considered a success.

The recommended intervention order for this case is to go from the least invasive change to the deeper structural change: first stabilize the scale with a log transform, then handle curvature with a regularized nonlinear function, and only finally expand to hierarchical group effects. This order helps us preserve the ability to trace causes, because each step has a clear hypothesis and a corresponding diagnostic signal to verify it.

### 7.5. Concrete illustrative results for the intervention steps

To avoid the feeling of "generic recommendations", we summarize one directional experiment round on this very dataset (80/20 train/test split, using the same set of evaluation criteria) to illustrate the direction in which results move after each intervention.

| Illustrative model | Signal to fix | Observed result | Interpretation |
|---|---|---|---|
| Baseline: `price ~ carat` (Gaussian) | Heteroskedasticity | $$\operatorname{corr}(\lvert e \rvert,\text{carat})\approx 0.579$$ | The error magnitude grows strongly with `carat`, so the homogeneous noise assumption is weak. |
| Baseline: `price ~ carat` (Gaussian) | Interval reliability in the high-value region | Global 90% coverage about 0.921, but in the high `carat` group only about 0.728 | The interval looks "wide enough" globally but seriously lacks coverage exactly in the most important region. |
| Intervention 1: `log(price) ~ carat` | Stabilizing variance across the predictor | $\operatorname{corr}(\lvert e_{\log} \rvert,\text{carat})\approx 0.269$ | The heteroskedasticity indicator drops markedly, consistent with the multiplicative noise hypothesis. |
| Intervention 1: `log(price) ~ carat` | Coverage in the high `carat` region | 90% coverage in the high `carat` region rises to about 0.850 | Prediction in the large segment is considerably improved compared with the baseline. |
| Intervention 1 (tail check) | Tail calibration | The posterior predictive $$Q_{0.95}$$ tends to exceed the observed level | An important lesson: the log transform can fix the lack of coverage in the high region but also risks over-correcting in the tail, so a separate tail PPC is still needed. |
| Intervention 3 in the non-hierarchical style (crude fixed effects) | Differences by quality group | Some rare groups have abnormally jumping mean predictions | This demonstrates why **partial pooling** is needed instead of adding groups in a completely free style. |

The results above show the core message of step 7: each intervention has a measurable effect, but the effect is not monotone in the sense of "the more complex the better". The right intervention is the one that reduces the target symptom without creating new distortion at another level of checking; therefore, the evaluation process after revising the model is mandatory, not an add-on.

## 8. Methodological conclusions from lesson 4.6

The `diamonds` case shows a truth running through Bayesian modeling: a nice metric at the overall level can coexist with a serious deviation at the conditional level, and without structured model checking, we easily confuse "the model has signal" with "the model is trustworthy for decisions". Therefore, the right cycle is never to fit and then conclude, but always to fit, check at multiple levels, interpret deviations in the language of mechanisms, and only then revise the model and evaluate again.

## Reference videos

- [Multiple Regression, Clearly Explained!!!](https://www.youtube.com/watch?v=EkAQAi3a4js) — StatQuest with Josh Starmer, English. **watch first**. Watch that a coefficient in multiple regression only has meaning when the other variables are kept in the model, exactly the kind of many-descriptor data in the case study.
- [What is a posterior predictive check and why is it useful?](https://www.youtube.com/watch?v=yDPJnV9vcHs) — Ben Lambert, English. Watch the posterior predictive check, supporting the lesson's argument that being able to fit a model is not a sufficient condition.
- [Oriol Abril-Pla - Model criticism with ArviZ | Pydata London 26](https://www.youtube.com/watch?v=HHPAzNan7Uw) — PyData, English. Watch model criticism with ArviZ, used for the part of the lesson that turns sampling diagnostics and PPC into a workflow.

## Practice questions

1. If a model reproduces $$\bar y$$ well but fails badly at $$Q_{0.95}(y)$$, what would you conclude about using the model for the high-end segment?
2. In a prediction context, why is an error in the right tail usually more dangerous than an error in the central region?
3. When `cut` has been added but the group-wise PPC is still unsatisfactory, which structural assumption would you check first?
4. Why is out-of-sample coverage per `carat` band more useful than coverage pooled over all the data?

## References

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), chapters on model checking.
- Gelman, A. et al. *Regression and Other Stories*.
- McElreath, R. *Statistical Rethinking* (2nd ed.), chapters on posterior predictive checks.

---

*End of Chapter 4. Next lesson: [Chapter 5 - Multiple Predictors and Causal Thinking]({{ site.baseurl }}/contents/en/chapter05/)*
