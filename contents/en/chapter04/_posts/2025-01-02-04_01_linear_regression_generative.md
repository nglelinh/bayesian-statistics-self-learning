---
layout: post
title: "Lesson 4.1: Bayesian Linear Regression - A Generative Model"
chapter: '04'
order: 1
owner: Nguyen Le Linh
lang: en
categories:
- chapter04
lesson_type: required
---

In an introductory statistics class, linear regression is often reduced to a geometric chore: drop a single straight line through a cloud of dots by minimizing squared vertical errors. Yet the moment you ask *"How confident should I be in a prediction for someone 195 cm tall?"* or *"Could this data realistically have come from a flat line?"*, a single best-fit line falls silent. Bayesian linear regression flips the script completely: instead of hunting for one line, we write down a **generative story** for how the data came to be, and let Bayes' rule hand us an entire probability distribution of plausible lines.

**Lesson Roadmap:** From one OLS line to a full generative model → Key ideas (Generative likelihoods, Posterior over parameters, Epistemic vs. Aleatoric uncertainty) → Hand-worked exact Bayesian regression on 4 points → Full model specification, real examples, and exercises.

## Learning objectives

After this lesson, you need to see Bayesian linear regression as a **data-generating story**, not just the problem of "fitting a straight line". You also need to understand the roles of the intercept, slope, and noise in the model, and why Bayesian regression always keeps the uncertainty of both the parameters and the predictions.

> **Mini example.** You want to describe the relationship between height and weight. The old view is "find the best straight line". The Bayesian view is "each person's weight is generated around an average trend, and we are not certain about that trend".
>
> **Quick check.** Why shouldn't Bayesian-style regression be understood simply as finding a single straight line?

## Key ideas: The Architecture of Bayesian Linear Regression

### 1. Generative Modeling (Forward Data-Generating Process)
- **What it is:** Specifying a complete probability machine $$y_i \sim \mathrm{Normal}(\mu_i, \sigma)$$, $$\mu_i = \alpha + \beta x_i$$, together with prior distributions on $$(\alpha, \beta, \sigma)$$.
- **What it studies:** How parameters generate synthetic datasets *before* seeing data (prior predictive simulation) and *after* updating (posterior predictive simulation), turning regression from curve-fitting into scientific modeling.

### 2. Joint Posterior Distribution over $$(\alpha, \beta, \sigma)$$
- **What it is:** Applying Bayes' rule $$p(\alpha, \beta, \sigma \mid x, y) \propto \prod_{i=1}^n \mathrm{Normal}(y_i \mid \alpha + \beta x_i, \sigma)\, p(\alpha, \beta, \sigma)$$.
- **What it studies:** Quantifying parameter uncertainty and correlation (for example, why uncentered $$x$$ creates a strong negative correlation between intercept $$\alpha$$ and slope $$\beta$$).

### 3. Two Distinct Sources of Predictive Uncertainty
- **What it is:** Decomposing total predictive variance $$\mathrm{Var}(y^* \mid x^*, D) = \underbrace{\sigma^2}_{\text{aleatoric}} + \underbrace{\mathrm{Var}(\alpha + \beta x^* \mid D)}_{\text{epistemic}}$$.
- **What it studies:** Separating irreducible observation noise ($$\sigma^2$$, which never shrinks even with infinite data) from parameter uncertainty (which shrinks as $$1/n$$ and flares outward as $$x^*$$ moves away from $$\bar{x}$$).

## Explanation: Exact Bayesian Slope & Prediction on 4 Points

Consider 4 centered observations: $$x = [-2, -1, 1, 2]$$ (so $$\sum x_i = 0$$ and $$\sum x_i^2 = 10$$) and $$y = [1, 3, 7, 9]$$ (so $$\bar{y} = 5$$ and $$\sum x_i y_i = -2 - 3 + 7 + 18 = 20$$). Assume known observation noise $$\sigma = 1$$, known intercept $$\alpha = 5$$, and a Gaussian prior on the slope $$\beta \sim \mathrm{Normal}(0, 1^2)$$ (prior precision $$1/\tau_0^2 = 1$$).

1. **OLS slope:** $$\hat{\beta}_{\text{OLS}} = \frac{\sum x_i y_i}{\sum x_i^2} = \frac{20}{10} = \mathbf{2.00}$$.
2. **Bayesian posterior precision & variance:** Precision adds cleanly:
   $$ \frac{1}{\tau_n^2} = \frac{1}{\tau_0^2} + \frac{\sum x_i^2}{\sigma^2} = 1 + \frac{10}{1} = 11 \implies \tau_n^2 = \frac{1}{11} \approx 0.0909 \quad (\tau_n \approx 0.302). $$
3. **Bayesian posterior mean:** Precision-weighted average of prior mean ($$0$$) and OLS estimate ($$2.00$$):
   $$ \mu_n = \frac{1 \cdot 0 + 10 \cdot 2.00}{11} = \frac{20}{11} \approx \mathbf{1.818}. $$
   Notice how the prior gently shrinks $$2.00 \to 1.818$$ (exact Ridge / L2 regularization!).
4. **Predicting a new point at $$x^* = 3$$:**
   - Predictive mean: $$\mathbb{E}[y^* \mid x^* = 3, D] = 5 + 1.818(3) = \mathbf{10.45}$$.
   - Predictive variance: $$\mathrm{Var}(y^*) = \underbrace{1.000}_{\sigma^2 \text{ (noise)}} + \underbrace{3^2 \cdot \frac{1}{11}}_{\text{slope uncertainty}} = 1 + 0.818 = \mathbf{1.818} \implies \text{SD} \approx \mathbf{1.348}. $$
   Far from the center ($$x^* = 3$$), epistemic uncertainty nearly doubles the variance compared to noise alone!

## 1. Regression is not just drawing a straight line

When first learning regression, many people are taught that you just choose a line $$y = \alpha + \beta x$$ and then find the line that minimizes the squared error.

That approach is useful, but it easily makes us think regression is just a geometric fitting technique.

In Bayesian regression, we look deeper and force ourselves to ask where the data comes from, why the points do not lie exactly on a line, and how uncertain we are about the parameters of that line itself.

## 2. The data-generating story of linear regression

Suppose we want to model the relationship between height $$x$$ and weight $$y$$.

The data-generating story can be told as follows.

### Step 1. There is an average trend

Taller people are usually heavier. We describe that trend by:

$$
\mu_i = \alpha + \beta x_i.
$$

Here $$\alpha$$ is the intercept and $$\beta$$ is the slope.

### Step 2. Each individual fluctuates around that trend

Nobody lies exactly on the average line, because there are many other factors such as muscle mass, diet, sex, activity level, or measurement error.

So we write:

$$
y_i \sim \mathcal{N}(\mu_i,\sigma).
$$

Here $$\sigma$$ is the noise around the regression line.

![The data-generating process of regression]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_regression_data_generating_process.png)

![Distribution of weight at a fixed height]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_regression_distribution_fixed_height.png)

### Step 3. We do not know the parameters exactly

We do not really know what the intercept is, what the slope is, and what the noise is.

So we place priors on them, and then use the data to infer the posterior.

![Summary of the regression generative story]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_regression_story_summary.png)

## 3. Three parameters to understand firmly

### 3.1. Intercept $$\alpha$$

The intercept is the mean value of $$y$$ when $$x = 0$$.

Mathematically, it is very convenient. But in practical terms, it is not always easy to interpret.

For example, if $$x$$ is height in cm, then $$x=0$$ has almost no practical meaning.

That is why in Bayesian regression we often center or standardize the input variable so that the intercept has a more readable meaning.

![Intercept after centering the input variable]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_intercept_after_centering.png)

### 3.2. Slope $$\beta$$

The slope tells how much the mean of $$y$$ changes when $$x$$ increases by 1 unit.

For example, if $$\beta = 0.7$$ kg/cm, then each cm of height corresponds to an average increase of 0.7 kg in weight.

![Interpreting the slope in linear regression]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_slope_interpretation.png)

### 3.3. Noise $$\sigma$$

Noise tells how widely the data points are spread around the regression line. If $$\sigma$$ is small, the data hug the line more closely, while if $$\sigma$$ is large, the data are more widely dispersed.

![Interpreting noise around the regression line]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_noise_interpretation.png)

## 4. How does Bayesian regression differ from OLS?

### What OLS usually answers

OLS (ordinary least squares) usually answers the question of what the "best" line is under a certain optimization criterion.

![The OLS point-estimate view]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_frequentist_point_estimate.png)

### What Bayesian regression answers

Bayesian regression answers a much broader question: which lines remain plausible after seeing the data, how large the uncertainty of the slope and intercept is, and how uncertain the prediction for a new observation will be. In other words, OLS gives you a central line, while Bayes gives you a **distribution of possible lines**.

![The uncertainty view of Bayesian regression]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bayesian_uncertainty_quantification.png)

### 4.1. Classical assumptions to state clearly before Bayesian inference

Before moving on to the posterior, we should state clearly the underlying assumptions of linear regression:

- the mean relationship is linear in the parameters,
- the errors have expected value 0,
- the errors are conditionally independent given the input variable,
- the error variance is stable (homoscedastic) in the basic model,
- in the simplest version, the errors are usually assumed Normal.

Bayes does not "erase" these assumptions; Bayes only adds a layer of uncertainty for the parameters and lets us check the assumptions more transparently at the model checking step.

![Residual distribution around the regression line]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_regression_residual_distribution.png)

### Experiment: the regression posterior is a whole bundle of lines

Add data points one at a time and watch the bundle of plausible lines narrow; compare with OLS and the true line.

<div class="interactive-demo" markdown="1">
<div data-demo="regression-explainer" data-lang="en"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 5. Why is "generative" such an important word?

If you view regression as a generative model, you will ask the right questions: what process was the data generated from, is the Normal assumption for the residuals reasonable, is the noise homogeneous across all values of $$x$$, and does this model really produce data that looks like the real data.

This is a very important difference between the attitude of "once it is fitted, we are done" and the attitude of "model it and then check".

## 6. Writing out the full Bayesian model

A minimal Bayesian linear regression has the form:

$$
\alpha \sim p(\alpha)
$$

$$
\beta \sim p(\beta)
$$

$$
\sigma \sim p(\sigma)
$$

$$
y_i \sim \mathcal{N}(\alpha + \beta x_i,\sigma)
$$

From there we derive the posterior:

$$
p(\alpha,\beta,\sigma \mid x,y).
$$

What matters is not memorizing this formula, but understanding what the prior says before the data, where the likelihood says the data comes from, and that the posterior is the answer that appears after the two are combined.

### 6.1. The joint likelihood - prior - posterior framework for regression

With data $$\mathcal D=\{(x_i,y_i)\}_{i=1}^n$$, we have:

$$
p(y\mid X,\alpha,\beta,\sigma)=\prod_{i=1}^n \mathcal N(y_i\mid \alpha+\beta x_i,\sigma).
$$

Joint prior (if we assume prior independence):

$$
p(\alpha,\beta,\sigma)=p(\alpha)p(\beta)p(\sigma).
$$

Hence:

$$
p(\alpha,\beta,\sigma\mid X,y)
\propto p(y\mid X,\alpha,\beta,\sigma)\,p(\alpha,\beta,\sigma).
$$

This is the unified view of this chapter: every inference about regression parameters starts from a clearly stated joint model.

### 6.2. Interval for the slope: known variance and unknown variance

When the noise variance is treated as known, the posterior of the slope is usually close to Normal and the posterior interval for $$\beta$$ reads as:

$$
\mu_{\beta\mid D}\pm z_{0.975}\,\sigma_{\beta\mid D}.
$$

When the variance is unknown and inferred together with the data, the posterior of $$\beta$$ usually has heavier tails (in practice close to Student-t), so the posterior interval is usually wider to reflect the additional uncertainty.

So when reporting "the interval of the slope", you need to state clearly whether you are in the known-variance or unknown-variance setting.

## 7. Another real example beyond height - weight

Bayesian regression appears in many places:

### House price and area

Here $$x$$ may be the area and $$y$$ the house price.

### Exam score and study hours

Here $$x$$ may be the number of revision hours and $$y$$ the exam score.

### Revenue and advertising cost

Here $$x$$ may be the advertising budget and $$y$$ the revenue.

In all of those examples, the generative thinking is still the same: there is an average trend, the real data fluctuates around that trend, and we are still uncertain about the very parameters that control the trend.

## 8. How does Bayesian regression make predictions?

Suppose you want to predict the weight of a person who is 175 cm tall.

Bayesian regression does not give just a single number. It gives a predicted mean value, uncertainty from not being sure about $$\alpha$$ and $$\beta$$, and also the uncertainty from the individual noise $$\sigma$$.

This is a very strong point: we not only predict, but also know how confident we should be in that prediction.

### 8.1. A concrete example: predicting weight at 175 cm

Suppose that after fitting the model on height - weight data, our posterior shows the following typical values:

$$
\alpha \approx -55,\qquad \beta \approx 0.75,\qquad \sigma \approx 6.
$$

We can understand these three numbers in everyday language as follows:

- an intercept of about $$-55$$ helps determine the position of the average line,
- a slope of about $$0.75$$ means that 1 cm taller raises the average weight by about 0.75 kg,
- noise of about $$6$$ kg means that even at the same height, the actual weight of each person still fluctuates quite considerably around the mean.

For a new person with height $$x_{\text{new}}=175$$, the model's predicted mean is:

$$
\mu_{\text{new}} = \alpha + \beta x_{\text{new}}
\approx -55 + 0.75 \times 175 = 76.25.
$$

If we look at only one representative set of parameters, we can say: "for a person 175 cm tall, the reasonable average weight under the model is about 76.25 kg". But Bayesian regression does not stop there, because it does not pretend that $$\alpha$$ and $$\beta$$ are known exactly.

Imagine the posterior gives us a few parameter samples as follows:

| Posterior sample | $$\alpha$$ | $$\beta$$ | $$\sigma$$ | $$\mu_{\text{new}} = \alpha + \beta \cdot 175$$ |
|---|---:|---:|---:|---:|
| 1 | -52 | 0.73 | 5.8 | 75.75 |
| 2 | -58 | 0.77 | 6.1 | 76.75 |
| 3 | -50 | 0.72 | 5.5 | 76.00 |
| 4 | -57 | 0.76 | 6.4 | 76.00 |

This table shows a very important idea: even before accounting for individual noise, merely being uncertain about the intercept and slope already produces a **distribution of the predicted mean value**. In other words, the model does not say "it is certainly 76.25 kg", but "the plausible region for the mean at a height of 175 cm lies around 75 to 77 kg".

This is where we need to separate two different questions very clearly:

**Question 1.** What is the average weight of people who are 175 cm tall?

This question targets $$\mu_{\text{new}}$$. If we draw many samples from the posterior and compute $$\mu_{\text{new}}$$ for each one, we get a posterior distribution for the mean value. Suppose that after this step we obtain an approximate 89% posterior interval:

$$
\mu_{\text{new}} \in [74,\ 78.5]\ \text{kg}.
$$

This interval reflects **parameter uncertainty**: we do not know exactly where the regression line lies.

**Question 2.** How much will one specific individual who is 175 cm tall weigh?

This question is harder, because besides parameter uncertainty there is also individual fluctuation around the average line. We must then use the posterior predictive distribution:

$$
y_{\text{new}} \sim \mathcal{N}(\mu_{\text{new}}, \sigma).
$$

If we keep propagating both the uncertainty of $$\alpha,\beta,\sigma$$ and this new noise, we can obtain a wider 89% prediction interval, for example:

$$
y_{\text{new}} \in [66,\ 87]\ \text{kg}.
$$

This interval is much wider than the one for $$\mu_{\text{new}}$$ because it answers for **one specific person**, not for the average of the whole group of people of the same height.

This is the point that many regression beginners often skip:

- the interval for $$\mu_{\text{new}}$$ answers about the average trend,
- the interval for $$y_{\text{new}}$$ answers about a truly new observation,
- the second interval is always wider because it keeps individual variability too.

In the generative spirit, the Bayesian prediction procedure is essentially:

1. Draw a sample from the posterior of $$\alpha,\beta,\sigma$$.
2. Compute $$\mu_{\text{new}}^{(s)} = \alpha^{(s)} + \beta^{(s)} x_{\text{new}}$$.
3. Generate a new value $$y_{\text{new}}^{(s)} \sim \mathcal{N}(\mu_{\text{new}}^{(s)}, \sigma^{(s)})$$.
4. Repeat many times to build the posterior predictive distribution.

So Bayesian regression makes predictions not by "plugging numbers into a single line", but by producing a whole distribution of plausible new values after having seen the data.

### 8.2. A bridge from one-variable to multi-variable regression (matrix form)

With several explanatory variables, we write:

$$
y=X\mathbf w+\varepsilon,
$$

where $$\mathbf w=(\alpha,\beta_1,\dots,\beta_p)^\top$$ and $$X$$ is the design matrix.

Then, Bayesian inference moves from "one slope" to "a vector of coefficients", but the thinking does not change: a prior on $$\mathbf w$$, a likelihood from the data-generating model, and a posterior for the whole parameter vector.

## 9. An important habit from this lesson

Each time you see a regression problem, force yourself to go through a very concrete series of questions: how the data is being generated, where the average trend is, where the noise part is, which parameters are still unknown, and when producing a new prediction which uncertainties need to be kept. If you can do that, you have started to think like someone doing Bayesian modeling rather than just someone running a regression.

> **3 key ideas.** Bayesian linear regression is a generative model in which data is generated around a noisy average trend; the intercept, slope and noise are all unknown quantities to be inferred rather than estimated by a single point value; and the strength of Bayesian regression lies in the fact that it keeps the uncertainty of both the parameters and the predictions instead of giving only a single straight line.

## Reference videos

- [The Essence of Linear Regression!!!](https://www.youtube.com/watch?v=aFDOzpTeg0s) — StatQuest with Josh Starmer, English. **watch first**. Watch regression as a story about a conditional mean plus noise, exactly how the lesson refuses to start from least squares.
- [Linear Regression, Clearly Explained!!!](https://www.youtube.com/watch?v=7ArmBVF2dCs) — StatQuest with Josh Starmer, English. Watch the intercept, slope and residuals on a straight line, supporting the part that names α, β and σ.
- [Statistical Rethinking 2023 - 03 - Geocentric Models](https://www.youtube.com/watch?v=tNOu-SEacNU) — Richard McElreath, English. Watch a regression model written as a generative model before being estimated, following the same order as the lesson.

## Practice questions

1. Tell the generative story for the relationship between study hours and exam score.
2. Why is $$\sigma$$ a very important parameter and not just an extra "residual"?
3. What is the biggest difference between "fit a line" and "model a process"?
4. In your own work, which regression problem should be viewed in the generative spirit?

## References

- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 4.
- Gelman, A. et al. *Regression and Other Stories*.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapters on regression.

---

*Next lesson: [4.2 Priors for Regression - Choosing Priors in a Principled Way]({{ site.baseurl }}/contents/en/chapter04/04_02_priors_for_regression/)*
