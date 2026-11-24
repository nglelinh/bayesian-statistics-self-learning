---
layout: post
title: "Lesson 4.5: Case Study Model Checking & Prediction - A Full Workflow on One Dataset"
chapter: '04'
order: 6
owner: Nguyen Le Linh
lang: en
categories:
- chapter04
lesson_type: required
---

Theory only clicks when you get your hands dirty on a real dataset that misbehaves. Restaurant tipping (`tips`) looks deceptively simple at first glance: larger bills lead to larger tips, so a straight line ought to do the job. Yet the moment we run posterior predictive checks and residual plots on `tips`, a glaring crack opens up: tips on a \$10 lunch barely vary by a dollar, whereas tips on a \$50 dinner swing wildly—and a constant-variance Normal model even predicts **negative tips**! Walking through this full workflow shows how Bayesian diagnostics turn a failed check into a principled model upgrade.

**Lesson Roadmap:** Putting the full workflow on `tips` → Background Knowledge Map (End-to-end Bayesian workflow, Homoscedasticity vs. Heteroscedasticity, Targeted model revision) → Hand-worked comparison of constant-$$\sigma$$ vs. bill-scaled $$\sigma(x)$$ intervals → Full 6-step case study and exercises.

## Learning objectives

After this lesson, you need to be able to carry out a full, in-depth workflow on a concrete dataset: build a Bayesian model, assess the quality of sampling, check the model with posterior predictive checks (PPC), analyze residuals, report predictions with the right kind of uncertainty, and propose model revisions based on evidence.

> **Mini example.** You predict the tip amount from the total bill in restaurant data. A linear model may give a very nice slope, but the practical question is: does that model really generate data that looks like reality and make trustworthy predictions for new customers?
>
> **Quick check.** If the posterior slope is clearly positive but the PPC fails in the large-bill region, what should you trust?

## Background Knowledge Map: Executing the Full Bayesian Workflow on Real Data

### 1. Iterative Model Building (Box's Loop)
- **What it is:** The disciplined cycle: *Specify generative baseline → Check sampler diagnostics → Run PPC & residual plots → Diagnose failure mode → Revise model → Re-check*.
- **What it studies:** Treating every model as a provisional hypothesis to be stress-tested against real data rather than a one-shot fit.

### 2. Homoscedasticity vs. Heteroscedasticity
- **What it is:** Whether observation noise $$\sigma$$ stays constant across all predictor values ($$\sigma_i = \sigma$$) or grows systematically with the predictor ($$\sigma_i = \gamma_0 + \gamma_1 x_i$$ or log-scale modeling).
- **What it studies:** Why fan-shaped residual plots invalidate prediction intervals even when the mean regression line $$\alpha + \beta x$$ looks accurate.

### 3. Domain Constraints on Predictive Distributions
- **What it is:** Checking whether $$p(y^{\text{rep}} \mid y)$$ respects physical boundaries of the outcome (such as tips being strictly non-negative, $$y \ge 0$$).
- **What it studies:** Selecting likelihoods or link/log transforms so predictions remain coherent at both low and high extremes of the covariate.

## Deep-Dive Explanation: Catching Heteroscedasticity by Hand on `tips` (Read Slowly)

Suppose a baseline homoscedastic model on `tips` gives $$\mu(x) = 0.80 + 0.14 x$$ with constant noise $$\sigma = 1.00$$ (in USD). Compare its 95% prediction intervals ($$\mu \pm 1.96\sigma$$) against a heteroscedastic revision where $$\sigma(x) = 0.10 + 0.05 x$$:

| Bill $$x$$ | Mean tip $$\mu(x)$$ | Baseline 95% PI ($$\sigma = 1.00$$) | Revised 95% PI ($$\sigma(x) = 0.10 + 0.05x$$) | What the check reveals |
| :--- | :--- | :--- | :--- | :--- |
| **\$10** | $$\$2.20$$ | $$[0.24,\; 4.16]$$ (at \$5: $$[-0.46,\; 3.46]$$!) | $$\sigma = 0.60 \implies [1.02,\; 3.38]$$ | Baseline leaks negative tips on small bills! |
| **\$50** | $$\$7.80$$ | $$[5.84,\; 9.76]$$ (width $$\$3.92$$) | $$\sigma = 2.60 \implies [2.70,\; 12.90]$$ | Baseline is far too narrow for big-table variance! |

Notice the crisp diagnostic signature: a single constant $$\sigma$$ simultaneously **over-estimates** uncertainty for small bills and **under-estimates** uncertainty for large bills. Letting $$\sigma$$ scale with $$x$$ (or modeling $$\log(\text{tip})$$) fixes both ends in one targeted move.

## 1. The concrete dataset: `tips` (seaborn)

We use the `tips` dataset, in which:

- `total_bill`: the total bill,
- `tip`: the tip amount,
- each row is one table of diners.

Main goal: model and predict `tip` from `total_bill`.

Secondary goal: check whether a baseline Gaussian linear model is good enough, instead of trusting the posterior slope by default.

The reason this dataset suits lesson 4.5 is that it is small enough to read intuitively, yet realistic enough to show model checking problems: possibly mild nonlinearity, variance that grows with the bill level, and tail behavior that is not entirely ideal for a simple Normal.

### 1.1. A quick look at part of the data

The table below shows the first 5 rows of the `tips` dataset so you get an intuitive feel for the data:

| total_bill | tip | sex | smoker | day | time | size |
|---:|---:|---|---|---|---|---:|
| 16.99 | 1.01 | Female | No | Sun | Dinner | 2 |
| 10.34 | 1.66 | Male | No | Sun | Dinner | 3 |
| 21.01 | 3.50 | Male | No | Sun | Dinner | 3 |
| 23.68 | 3.31 | Male | No | Sun | Dinner | 2 |
| 24.59 | 3.61 | Female | No | Sun | Dinner | 4 |

### 1.2. Summarizing the data before modeling

Over all 244 observations:

- `total_bill`: mean about 19.79, standard deviation about 8.90, min 3.07, max 50.81,
- `tip`: mean about 3.00, standard deviation about 1.38, min 1.00, max 10.00,
- the linear correlation between `total_bill` and `tip` is about 0.676 (positive, moderate to fairly strong).

An important point for the later checking step:

- only about 2.9% of observations have `tip > 6`,
- but this is exactly the region that determines tail behavior, where a Gaussian linear model is often prone to error.

Clarifying this argument:

- **Why does 2.9% still matter?** In prediction problems, errors in the tail are often tied to high-impact cases (large bills, large tips). Even though rare, these points determine the quality of prediction in risk or high-value scenarios.
- **Why is a linear Gaussian model prone to error in the tail?** The baseline model assumes symmetric errors and a single common noise $$\sigma$$ for every level of `total_bill`. In reality, service data often has variance that grows with the bill level, so the tail can be thicker than a simple Normal predicts.
- **Consequence of ignoring the tail region:** the model may still fit the mean well but underestimate the probability of very high tips, making the prediction interval in the large-bill region artificially narrow.
- **The right check in PPC:** besides mean/variance, you should also check tail statistics, for example

$$
T(y)=\mathbf 1(y>6),\quad T(y)=\max(y),\quad T(y)=Q_{0.95}(y).
$$

If $$T(y_{obs})$$ lies at the edge of or outside the distribution of $$T(y_{rep})$$, that is a sign the model has not reproduced the tail behavior.

### 1.3. Interpreting the conclusions with formulas

To avoid the "look at a plot and guess" style of conclusion, we write down the formulas behind the important statements.

The sample linear correlation coefficient (Pearson) between `total_bill` and `tip` is computed by:

$$
r_{xy}=\frac{\sum_{i=1}^{n}(x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum_{i=1}^{n}(x_i-\bar x)^2}\sqrt{\sum_{i=1}^{n}(y_i-\bar y)^2}}.
$$

For this dataset, $$r_{xy}\approx 0.676$$, so we have two separate conclusions:

- positive sign: as the bill increases, the tip tends to increase,
- magnitude of about 0.68: the linear relationship is moderate to fairly strong, not weak but not nearly perfect either.

The proportion in the right tail (`tip > 6`) is computed by:

$$
\hat p_{\text{tip}>6}=\frac{1}{n}\sum_{i=1}^{n}\mathbf 1(y_i>6),
$$

and gives a value of about 0.029 (2.9%). Because this proportion is small, every conclusion about the tail must be checked by PPC instead of only looking at the mean.

A quick connection for reading the level of linear explanation is:

$$
R^2 \approx r_{xy}^2.
$$

Therefore, with $$r_{xy}\approx 0.676$$ we get $$R^2\approx 0.46$$, meaning the linear model only explains about 46% of the variation of `tip`. This is the reason we must continue with model checking and residual analysis.

Finally, to quickly detect heteroskedasticity, we look at the correlation between the residual magnitude and the predictor:

$$
\operatorname{corr}(|e_i|,x_i), \quad e_i=y_i-\hat y_i.
$$

If this indicator is clearly positive, the error magnitude tends to grow with `total_bill`, and the assumption of homogeneous errors needs to be reconsidered.

## 2. Step 1 - Write the generative story and fit the baseline model

The baseline model of the case study:

$$
\text{tip}_i \sim \mathcal{N}(\mu_i, \sigma), \quad \mu_i = \alpha + \beta\,x_i,
$$

with $$x_i$$ being the standardized `total_bill`.

Interpreting the generative story:

- each table has an expected tip that depends linearly on the bill level,
- around that expectation, the tip fluctuates with a common noise $$\sigma$$,
- the prior should regularize enough to avoid overfitting in the sparse data region (very large bills).

The linear fit usually gives a clearly positive slope. However, in this lesson we treat that only as a starting point, not the final conclusion.

## 3. Step 2 - Check sampler diagnostics before talking about meaning

Before interpreting the slope/intercept, we need to look at:

- whether the trace plot mixes well,
- whether `r_hat` is close to 1,
- whether ESS is large enough,
- whether there are warnings about divergences or sampling pathologies.

If the diagnostics are not fine, all conclusions about the posterior and predictions are not yet trustworthy.

Practical benchmarks to follow:

- `r_hat` approaching 1.00 for the main parameters,
- ESS large enough to estimate tail quantiles stably,
- no systematic divergences.

The reason to take this step seriously: a good or bad PPC only has meaning once the posterior samples are trustworthy.

## 4. Step 3 - Posterior predictive distribution and PPC

Following lesson 4.4, we use:

$$
p(\tilde y \mid y)=\int p(\tilde y \mid \theta)\,p(\theta\mid y)\,d\theta.
$$

In the context of the `tips` dataset, the PPC question is:

> If the baseline model is correct, does the simulated tip data look like the real tip data in both the central region and the tail region?

### 4.1. Comparing the overall distribution

Compare the observed `y` with `y_rep` from the posterior predictive:

- whether the histogram/density overlap reasonably well,
- whether the right tail (very high tips) is underestimated by the model,
- whether the simulated min/max are reasonable.

![Figure 2 - Comparing observed and posterior predictive over the whole distribution]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_observed_vs_predicted.png)

### 4.2. Comparing mean, variance, and specific statistics

Compute the statistic on the real data and on each simulated sample:

- mean,
- variance,
- the proportion of tips exceeding a threshold (for example `tip > 6`).

If the observed value falls too far at the edge relative to the posterior predictive distribution of the statistic, the model is missing a part of the data structure.

![Figure 3 - Checking the mean with the posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_test_stat_mean.png)

![Figure 4 - Checking the variance with the posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_variance_check.png)

In the `tips` case, the baseline model usually reproduces the mean fairly well but tends to be off in the variance in the large-bill region. This is an early signal of heteroskedasticity.

### 4.3. Comparing the `x -> y` relationship

For regression, the most important thing is the shape of the relationship:

- plot many regression lines/draws from the posterior predictive over the real scatter,
- see whether the model predicts too optimistically in the large `total_bill` region,
- see whether the width of the prediction grows with `x`.

This is usually where nonlinearity or heteroskedasticity is detected earliest.

![Figure 5 - Comparing the predictor-response relationship between real data and posterior predictive samples]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_distribution_at_x5.png)

## 5. Step 4 - Residual analysis to find systematic deviations

Simple standardized residual:

$$
r_i = y_i - \mathbb{E}[y_i \mid y].
$$

You should look at at least three plots:

- residual vs fitted,
- residual vs `total_bill`,
- Q-Q plot of the residuals.

Signs to watch for:

- a curved pattern: suggests a nonlinear relationship,
- a fan shape: suggests changing variance,
- strongly skewed tails on the Q-Q plot: suggests the Normal assumption may be too simple.

In the `tips` case, a common signal is that the residual magnitude grows with `total_bill`. This is why a homoskedastic error model may not be good enough.

![Figure 6 - Residual distribution: observed vs posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_residual_distribution.png)

![Figure 7 - Residuals vs fitted to identify systematic patterns]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_residuals.png)

## 6. Step 5 - Prediction for a specific case

Suppose we predict for a new table with `total_bill = 40`.

You should report **two kinds of uncertainty**:

1. the posterior interval of the mean tip at that bill level,
2. the prediction interval for one specific new table.

Example interpretation:

- the mean tip at a bill of 40 may be around 5.8 to 6.5,
- but one specific table may be wider, for example 3.8 to 8.7.

The second interval is wider because it adds both parameter uncertainty and new individual noise.

An important reporting point for decision-making:

- if the goal is planning average revenue, use the interval of the mean response,
- if the goal is the risk of one specific transaction, use the prediction interval.

## 7. Step 6 - When the checks are not fine: revise the model with a reason

Suppose the PPC and residuals show that:

- the original linear model under-predicts in the right tail,
- the variance grows with `total_bill`.

A reasonable way to revise:

- use a log-transform for the response, for example $$\log(\text{tip})$$,
- or model $$\sigma$$ as a function of `x`,
- or add a mild nonlinear component (spline/low-degree polynomial).

The important message: do not revise the model by gut feeling. Revise it according to the exact deviation signs that the PPC and residuals point out.

### 7.1. A quick comparison of three candidate models

| Candidate | Addresses the main problem | Strength | Risk |
|---|---|---|---|
| Baseline Gaussian linear | Initial reference point | Easy to interpret | Prone to errors in the tail and changing variance |
| Log-tip Gaussian | Shrinks the right tail, stabilizes variance more | Often improves the tail PPC | Back-interpreting to the original units needs care |
| Heteroskedastic Gaussian | Lets $$\sigma$$ change with `total_bill` | More honest prediction intervals at large bills | Increases complexity and checking cost |

In practice, you should compare these candidates using the same set of PPC/residual criteria before concluding which model is most useful.

## 8. Summary of the lesson 4.4 workflow on a real case

On the `tips` dataset, we have gone through the right cycle:

1. state the generative story and fit the model,
2. check the diagnostics,
3. do posterior predictive checks,
4. read the residuals to find patterns,
5. predict for a specific situation with clear uncertainty,
6. propose a model revision based on evidence.

This is the hands-on version of the message of lesson 4.4: Bayesian regression is only complete when you check and revise the model, not stopping at the posterior of the parameters alone.

### 8.1. In-depth analysis checklist (reuse for other problems)

1. check the data structure and tail region before fitting,
2. confirm the sampler meets the minimum standard,
3. run PPC at three levels: overall distribution, target statistic, the `x -> y` relationship,
4. read residuals by pattern, not just by looking at the mean,
5. report predictions with the right kind of uncertainty,
6. revise the model only when there are clear deviation signs from the checks.

## 9. Common mistakes in this case study

### 9.1. Stopping at "the slope is positive"

A positive slope does not guarantee that the model generates reasonable data over the whole domain of the predictor.

### 9.2. Reporting the wrong kind of interval

Using the interval of the mean response to speak about one specific individual/table creates false certainty.

### 9.3. Revising the model without relying on checks

Trying many arbitrary transformations without following the residual/PPC signs makes the workflow lose its scientific character.

### 9.4. Reporting results without stating the scope of applicability

A model may be fine in the central `total_bill` region but weak in the very large region. If this is not stated clearly, users easily misjudge the reliability of the predictions.

## 10. What to keep after this lesson

A mature Bayesian workflow always follows the loop:

**modeling -> checking -> predicting -> revising the model**.

The `tips` case shows that even a small problem needs this full loop to reach a responsible conclusion.

## Reference videos

- [What is a posterior predictive check and why is it useful?](https://www.youtube.com/watch?v=yDPJnV9vcHs) — Ben Lambert, English. **watch first**. Watch the question a posterior predictive check asks before doing the workflow on the tips data.
- [L4: Interpretable Linear Regressions (State of Bayes Lecture Series)](https://www.youtube.com/watch?v=fpS0NjqNHn8) — PyMC Labs, English. Watch a Bayesian regression being fitted and its coefficients interpreted, supporting the model-building half of the case study.
- [Simple Linear Regression:  Checking Assumptions with Residual Plots](https://www.youtube.com/watch?v=iMdtTCX2Q70) — jbstatistics, English. Watch how to read a residual plot when checking assumptions, used for the residual analysis part of the lesson.

## Practice questions

1. For the `tips` dataset, which statistic would you choose for the PPC besides the mean/variance, and why?
2. If the residual vs fitted forms a U shape, which direction would you try to revise the model first?
3. Why is the prediction interval for a new table always wider than the uncertainty interval of the mean tip?
4. If the model predicts the central region well but fails in the right tail, how does this affect business decisions?

## References

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), chapters on model checking.
- Gelman, A. et al. *Regression and Other Stories*.
- McElreath, R. *Statistical Rethinking* (2nd ed.), chapters on posterior predictive checks.

---

*Next lesson: [Lesson 4.6 - Advanced Case Study on a Complex Dataset]({{ site.baseurl }}/contents/en/chapter04/04_06_case_study_complex_dataset/)*
