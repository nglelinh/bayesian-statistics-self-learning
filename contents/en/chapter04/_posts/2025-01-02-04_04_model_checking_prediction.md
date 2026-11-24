---
layout: post
title: "Lesson 4.4: Model Checking and Prediction - Making Sure the Model Is Good"
chapter: '04'
order: 5
owner: Nguyen Le Linh
lang: en
categories:
- chapter04
lesson_type: required
---

Your MCMC chains converged cleanly with $$\hat{R} = 1.00$$, zero divergences, and 4,000 effective samples. Time to celebrate and ship the model? Not yet! Convergence only proves that your sampler accurately explored the posterior of *the model you wrote down*—it says nothing about whether that model is a decent description of reality. A perfectly converged linear model fit to curved or heavy-tailed data will produce confidently wrong predictions. That is why every serious Bayesian workflow pivots from inference to **model criticism**: Posterior Predictive Checks (PPC) and residual diagnostics.

**Lesson Roadmap:** Why convergence $$\neq$$ a good model → Background Knowledge Map (Posterior predictive distribution, Bayesian p-values & test statistics, Mean vs. Prediction intervals) → Hand-worked Bayesian p-value & predictive interval width comparison → Residual analysis, uncertainty, and exercises.

## Learning objectives

After this lesson, you need to understand that fitting the model is only the first half of Bayesian regression. The other half is checking whether the model describes the data reasonably, and using the posterior to predict new data honestly. You also need to grasp posterior predictive checks as the central tool of this step.

> **Mini example.** A regression line can look very nice on a scatter plot, but if it does not generate data that looks like the real data, the model still has a problem. Model checking is the way to interrogate the model instead of trusting it just because it has finished running.
>
> **Quick check.** Why is a posterior that "looks fine" not enough to conclude that the model is good?

## Background Knowledge Map: Criticizing and Predicting with Bayesian Models

### 1. Posterior Predictive Distribution ($$p(y^{\text{rep}} \mid y)$$)
- **What it is:** Averaging the data likelihood over the entire posterior $$p(y^{\text{rep}} \mid y) = \int p(y^{\text{rep}} \mid \theta) p(\theta \mid y)\,d\theta$$—implemented by drawing $$\theta^{(s)}$$ from the posterior and then simulating synthetic data $$y^{\text{rep},(s)} \sim p(y \mid \theta^{(s)})$$.
- **What it studies:** Answering the acid test of generative modeling: *"If my fitted model were truly the data-generating machine, would its simulated worlds look like the real dataset I actually observed?"*

### 2. Posterior Predictive Checks (PPC) and Tail-Area Diagnostics
- **What it is:** Comparing observed summary statistics $$T(y)$$ (mean, spread, max, skewness, fraction of zeros) against the distribution of $$T(y^{\text{rep},(s)})$$, summarized by the Bayesian $$p$$-value $$p_B = P(T(y^{\text{rep}}) \ge T(y) \mid y)$$.
- **What it studies:** Pinpointing *exactly how* a model fails—for instance, matching the mean perfectly while missing skewness, heteroscedasticity, or extreme outliers.

### 3. Credible Interval for the Mean vs. Prediction Interval for New Data
- **What it is:** Separating uncertainty about the regression line $$\mu(x^*)$$ from uncertainty about a brand-new observation $$y^* = \mu(x^*) + \varepsilon$$.
- **What it studies:** Preventing dangerously overconfident forecasts by always adding observation noise $$\sigma^2$$ when predicting individual future outcomes.

## Deep-Dive Explanation: Bayesian p-Value & Prediction Interval Width by Hand (Read Slowly)

### Part 1: Reading a Posterior Predictive Check via $$p_B$$
Suppose you fit a Normal linear model and check whether it captures extreme observations using the test statistic $$T(y) = \max_i \vert r_i \vert$$ (largest standardized residual). In your real dataset, $$T(y) = 4.2$$. Across $$S = 1{,}000$$ posterior predictive replications $$y^{\text{rep},(s)}$$, only **12** simulations produce a max residual $$\ge 4.2$$:
$$ p_B = \frac{12}{1{,}000} = \mathbf{0.012}. $$
A value near $$0.5$$ means the model reproduces that feature effortlessly; $$p_B = 0.012$$ (close to 0 or 1) flags a concrete mismatch—here, heavier tails than a Normal likelihood, pointing directly toward a Student-$$t$$ revision!

### Part 2: Why a 95% Prediction Interval Is Much Wider Than a 95% Mean Interval
Suppose at $$x^* = 3$$, your posterior gives $$\mathrm{Var}(\alpha \mid D) = 0.25$$, $$\mathrm{Var}(\beta \mid D) = 0.16$$ (uncorrelated), and noise variance $$\sigma^2 = 4.00$$:
- **Uncertainty of the regression line $$\mu(3)$$:**
  $$ \mathrm{Var}(\mu(3)) = 0.25 + 3^2(0.16) = 1.69 \implies \mathrm{SD} = \mathbf{1.30} \quad (\text{95\% half-width } \approx \pm 2.55). $$
- **Uncertainty of a single new observation $$y^*(3)$$:**
  $$ \mathrm{Var}(y^*(3)) = 4.00 + 1.69 = 5.69 \implies \mathrm{SD} = \mathbf{2.385} \quad (\text{95\% half-width } \approx \pm 4.67). $$
The prediction interval is **$$1.83\times$$ wider**—because knowing the average line accurately still cannot eliminate individual observation noise $$\sigma$$.

## 1. A good fit is not necessarily a good model

This is an important shift in thinking.

Many people learning regression stop at estimating the slope, looking at the interval, and then concluding as if the job were done.

But a mature Bayesian workflow asks harder questions: can this model reproduce the observed data, do the residuals still show suspicious patterns, and are the predictions for new data really reasonable?

George Box has a very famous saying:

> “All models are wrong, but some are useful.”

The goal is not to find an "absolutely correct" model, but a model that is useful enough, honest enough, and does not miss the important structures of the data.

## 2. What is the posterior predictive distribution?

Suppose you already have the posterior of the parameters. Then you can generate new data $$\tilde y$$ from the model:

$$
p(\tilde y \mid y) = \int p(\tilde y \mid \theta)\,p(\theta \mid y)\,d\theta.
$$

The meaning of the posterior predictive distribution is that we infer not only about the parameters, but also about future data or data replicated from the model itself.

This is the bridge between estimation and prediction.

*Reading the formula above*:

- $$\tilde y$$ is the new data (or simulated data) that we want to predict,
- $$\theta$$ is the model parameter,
- $$p(\theta \mid y)$$ is how much we believe in each parameter value after seeing the data,
- $$p(\tilde y \mid \theta)$$ is how the model generates new data if the parameter is fixed at $$\theta$$.

So the integral is a "weighted average" over all possibilities of the parameters. The weight here is the posterior $$p(\theta \mid y)$$: **the parameters that the posterior deems more plausible contribute more to the final prediction**.

In short, the posterior predictive does not use a single set of parameters, but combines the predictions of many sets of parameters according to their credibility.

In MCMC practice, we usually approximate the integral by a sum:

$$
p(\tilde y \mid y) \approx \frac{1}{S}\sum_{s=1}^{S} p(\tilde y \mid \theta^{(s)}), \quad \theta^{(s)} \sim p(\theta \mid y).
$$

The computation is very intuitive: draw many samples $$\theta^{(s)}$$ from the posterior, generate $$\tilde y^{(s)}$$ from each sample, and then combine them all into the posterior predictive distribution.

## 3. What is a posterior predictive check (PPC)?

The PPC asks a very practical question:

> If my model is correct, does the simulated data generated from the model look like the real data?

The basic PPC procedure is to draw many parameter samples from the posterior, generate fake data from each sample, and then compare the fake data with the observed data.

If the fake data has a similar shape, spread, and patterns to the real data, the model has more grounds to be considered fine.

![Summary of the posterior predictive check workflow]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_summary.png)

### 3.1. A concrete example: the slope looks great but the model is still wrong

Suppose you model the relationship between study hours and exam score with a straight line. The posterior of the slope comes out very nice: clearly positive, a narrow interval, and the probability $$\beta > 0$$ is almost 1.

If we stop here, many people would conclude that the model is good. But imagine the true relationship in the data is: more study hours make the score rise quickly at first, after which the effect gradually saturates when studying too much. Then a straight line will typically produce three warning signs:

- the PPC generates too many unrealistically high predicted points in the region of very many study hours,
- the residuals in the middle region tend to be negative while the residuals at the two ends tend to be positive, creating a curved pattern,
- the mean prediction looks fine overall but is systematically wrong in the important regions of $$x$$.

The meaning of this example is: the posterior of the parameters can be "nice" because the model has fitted very firmly to a wrong structure. PPC and residual analysis exist precisely to expose that kind of error.

## 4. What should a PPC look at?

There is no single check suitable for every problem. You should look from many angles:

### 4.1. Overall distribution

Does the histogram or density of the fake data look like the real data?

![Comparing the posterior predictive distribution at a representative value of x]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_distribution_at_x5.png)

### 4.2. Mean and spread

Does the model reproduce the mean, variance, reasonable min/max, or tail behavior of the real data?

![Checking the mean of the observed data within the posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_test_stat_mean.png)

![Checking the variance of the observed data within the posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_variance_check.png)

### 4.3. The relationship between predictor and response

For regression, it is very important whether the model reproduces the right pattern between the predictor $$x$$ and the response $$y$$.

![Comparing observed data with posterior predictive samples]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_observed_vs_predicted.png)

### 4.4. Problem-specific statistics

For example, the number of outliers, skewness, asymmetry, or the rate of exceeding a threshold.

## 5. Residual analysis is still very important

Even in Bayesian regression, residuals are still a good mirror for the model.

We usually look at residual vs fitted, residual vs predictor, the residual distribution, signs of heteroskedasticity, and signs of nonlinearity.

Residual analysis is easiest to understand when placed beside typical situations: a good model, a model that misses nonlinearity, a model with heteroskedasticity, and a model with heavy-tailed residuals.

![Residual distribution: observed vs posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_residual_distribution.png)

At the level of the raw scatter plot, the four figures below show what the data can look like in each situation.

![Scatter plot of a good model]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_good_model_scatter.png)

![Scatter plot when the true relationship is nonlinear]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonlinearity_scatter.png)

![Scatter plot when the variance grows with x]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_scatter.png)

![Scatter plot when the residuals have heavy tails]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonnormal_scatter.png)

When moving to residual vs fitted, we want to see the residuals scattered randomly around 0 instead of forming a systematic pattern.

![Residuals vs fitted of a good model]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_good_model_residuals.png)

![Residuals vs fitted showing signs of nonlinearity]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonlinearity_residuals.png)

![Residuals vs fitted showing signs of heteroskedasticity]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_residuals.png)

![Residuals vs fitted with heavy-tailed residuals]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonnormal_residuals.png)

The Q-Q plot helps check whether the residuals are still close to Normal or are deviating from this assumption.

![Q-Q plot of the residuals in a good model]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_good_model_qq.png)

![Q-Q plot when the model misses nonlinearity]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonlinearity_qq.png)

![Q-Q plot when there is heteroskedasticity]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_qq.png)

![Q-Q plot when the residuals have heavy tails]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonnormal_qq.png)

If the residuals show a systematic pattern, the model may be missing nonlinearity, an interaction, heteroskedasticity, or some important variable that has not been included.

## 6. How does prediction in Bayes differ from point prediction?

In classical regression, many people are used to only a single mean predicted value.

Bayesian prediction goes further in that it keeps the uncertainty of the parameters, and also the uncertainty due to the noise of a new observation.

This lets you say not only "the prediction is 72", but also "where the plausible region of the prediction lies, and how sure we are".

That is a much more useful kind of forecast for decision-making.

## 7. Prediction interval and uncertainty

There are two main sources of uncertainty:

### 7.1. Parameter uncertainty

We do not know exactly $$\alpha,\beta,\sigma$$.

### 7.2. Uncertainty of a new observation

Even if we knew the parameters perfectly, a new observation would still fluctuate around the mean line.

A prediction interval is therefore always wider than the uncertainty of the mean response alone.

This is very important when reporting predictions to end users.

### 7.3. A short example to avoid confusing the two kinds of interval

Suppose that for a student who studies 6 hours, the model gives:

- a posterior interval for the mean score from 7.4 to 8.2,
- a prediction interval for a new student from 6.0 to 9.3.

The first interval answers the question: "if we take very many students who all study 6 hours, where does their average score lie?"

The second interval answers the question: "in which region might the score of one specific student who studies 6 hours fall?"

If you accidentally use the first interval to communicate about a specific individual, you will create an excessive sense of certainty. This is a very common interpretation error in prediction.

## 8. Model checking is not for "catching a perfect model"

Do not understand model checking as a binary game of either a perfect model or one to be thrown away.

It is a process of asking where the model is wrong, how wrong it is, and whether that deviation affects the practical question we care about.

For example, if the model is slightly off in the tail but still predicts the mean very well, it may still be acceptable; but if you care about extreme risk, then the error in the tail becomes a very serious problem.

## 9. When the checks are not fine, what should we do?

Do not react mechanically with "run the sampler more".

Instead, think in the following three broad directions:

### 9.1. Is the generative story missing something?

Ask whether there is nonlinearity, an interaction, or some group/hierarchical structure being overlooked.

### 9.2. Is there a problem with the prior?

Look at whether the prior is too wide, too narrow, or whether its prior predictive is really reasonable.

### 9.3. Is there anything special about the data?

Check whether the data has outliers, measurement error, missing variables, or any noteworthy heteroskedasticity.

Good model checking is what paves the way for good model revision.

## 10. A closed-loop workflow for Bayesian regression

Chapter 4 is actually teaching a complete workflow: tell the generative story, choose priors in a principled way, fit the posterior, check the sampler diagnostics, check the model with PPC and residuals, use the posterior to predict, and then go back and fix the model if needed.

If you do all of these seven steps, regression is no longer "running a function", but a real modeling process.

## 11. Common mistakes

### 11.1. Trusting the posterior without checking the model

The posterior is only trustworthy if the model that generated that posterior is still reasonable.

### 11.2. Looking only at the fit on old data

Prediction for new data is where the model reveals its real value.

### 11.3. Doing only a single PPC

A model can pass one criterion but fail another. Check from many perspectives.

## 12. What to keep after this lesson

Bayesian regression does not end at the posterior. It really lives in whether the model explains the data reasonably, and whether the predictions it produces are truly useful.

Without the checking and prediction steps, Bayesian regression has only gone halfway.

> **3 key ideas.** The posterior predictive check is the way to ask whether the model generates data that looks like the real data; residual analysis and prediction are two important parts of evaluating whether the model is truly useful; and fitting the model is only the first step, because a complete Bayesian workflow always includes checking, prediction, and revision if needed.

## Reference videos

- [What is a posterior predictive check and why is it useful?](https://www.youtube.com/watch?v=yDPJnV9vcHs) — Ben Lambert, English. **watch first**. Watch the posterior predictive check ask whether the model reproduces the features of the data, exactly the second half of regression that the lesson emphasizes.
- [Quantile-Quantile Plots (QQ plots), Clearly Explained!!!](https://www.youtube.com/watch?v=okjYjClSjOg) — StatQuest with Josh Starmer, English. Watch the Q–Q plot, supporting the part that compares the residual distribution with the Normal assumption.
- [Residual plots | Exploring bivariate numerical data | AP Statistics | Khan Academy](https://www.youtube.com/watch?v=VamMrPZ-8fc) — Khan Academy, English. Watch a residual plot detect leftover structure, used for the part of the lesson that does not stop at the sampler having converged.

## Practice questions

1. Why should a model that has been fitted but has not passed a PPC not yet be fully trusted?
2. What is the difference between the uncertainty of the mean prediction and the uncertainty of a new observation?
3. Name three things you can compare between the real data and the posterior predictive data.
4. If the residuals show a clearly curved pattern, what would you suspect about the model?

## References

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), chapters on model checking.
- Gelman, A. et al. *Regression and Other Stories*.
- McElreath, R. *Statistical Rethinking* (2nd ed.), chapters on posterior predictive checks.

---

*Next lesson: [Lesson 4.5 - Case Study: Model Checking & Prediction]({{ site.baseurl }}/contents/en/chapter04/04_05_case_study_model_checking_prediction/)*
