---
layout: post
title: "Lesson 4.2: Priors for Regression - Choosing Priors in a Principled Way"
chapter: '04'
order: 2
owner: Nguyen Le Linh
lang: en
categories:
- chapter04
lesson_type: required
---

Nothing makes a newcomer to Bayesian regression freeze up faster than the blank line next to `beta ~ Normal(?, ?)`. Choose a prior that is too tight and you risk steamrolling your own data; choose a "safe, uninformative" flat prior like `Normal(0, 100)` and—as we are about to verify by hand—you have accidentally told the model that a 7 cm taller human might weigh as much as a sedan! Choosing priors is not guesswork; it is a disciplined engineering loop anchored by standardization and **prior predictive checks**.

**Lesson Roadmap:** Why "flat" priors are secretly absurd → Background Knowledge Map (Standardization, Weakly informative priors, Prior predictive simulation) → Hand-check of `Normal(0, 100)` vs. `Normal(0, 1)` on standardized variables → Choosing priors for $$\alpha$$, $$\beta$$, $$\sigma$$, and exercises.

## Learning objectives

After this lesson, you need to know how to choose priors for regression in a principled way. You also need to understand why standardization is so important, why weakly informative priors are usually a good starting point, and why the prior predictive check is an almost mandatory step before fitting a model.

> **Mini example.** If you set the prior for the slope too wide, the model may implicitly allow crazy regression lines that domain knowledge immediately calls absurd. A prior for regression is not "fill in anything to complete the model", but a way to keep the model grounded.
>
> **Quick check.** Why can the same prior look reasonable on one scale but absurd on another?

## Background Knowledge Map: Principled Prior Specification for Regression

### 1. Standardization (Z-Scoring) as a Universal Scale
- **What it is:** Transforming predictors and outcomes via $$x_z = (x - \bar{x})/s_x$$ and $$y_z = (y - \bar{y})/s_y$$ before specifying priors.
- **What it studies:** Making parameters dimensionless ($$\beta_z$$ is now "SDs of $$y$$ per 1 SD of $$x$$"), decoupling the intercept from the slope, and dramatically improving MCMC geometry.

### 2. Weakly Informative Priors (Regularizing Without Dogma)
- **What it is:** Priors broad enough to accommodate every scientifically plausible effect (e.g., $$\beta_z \sim \mathrm{Normal}(0, 1)$$) yet tight enough to rule out physically impossible nonsense.
- **What it studies:** Stabilizing inference on small or noisy datasets while letting moderate-to-large datasets speak freely.

### 3. Prior Predictive Checks (Simulating Before Seeing Data)
- **What it is:** Drawing parameters $$(\alpha^{(s)}, \beta^{(s)}, \sigma^{(s)})$$ from the prior *alone* and plotting the implied regression lines $$\mu^{(s)}(x)$$ in observable data units.
- **What it studies:** Translating abstract parameter numbers into concrete observable consequences so domain knowledge can immediately catch absurd priors.

## Deep-Dive Explanation: Why `Normal(0, 100)` Is Not "Uninformative" (Read Slowly)

Suppose you model adult weight ($$\bar{y} = 65\text{ kg},\, s_y = 10\text{ kg}$$) from height ($$\bar{x} = 170\text{ cm},\, s_x = 7\text{ cm}$$) on standardized scales $$x_z, y_z$$. Compare two candidate priors on the standardized slope $$\beta_z$$:

| Prior on $$\beta_z$$ | 95% Prior Interval for $$\beta_z$$ | Implied weight shift per $$+1\text{ SD}$$ ($$+7\text{ cm}$$) height | Scientific verdict |
| :--- | :--- | :--- | :--- |
| **"Flat" $$\mathrm{Normal}(0, 100^2)$$** | $$[-196,\; +196]$$ | $$\pm 196 \times 10 = \mathbf{\pm 1{,}960\text{ kg}}$$ | Predicts humans weighing as much as a car—wildly implausible! |
| **Weakly informative $$\mathrm{Normal}(0, 1^2)$$** | $$[-1.96,\; +1.96]$$ | $$\pm 1.96 \times 10 = \mathbf{\pm 19.6\text{ kg}}$$ | Covers flat, strong positive, and even negative slopes within physical reality |

Even more striking: under $$\mathrm{Normal}(0, 100^2)$$, the probability that $$\vert \beta_z \vert > 5$$ (meaning a $$7\text{ cm}$$ height difference shifts weight by more than $$50\text{ kg}$$) is $$2\Phi(-5/100) \approx \mathbf{96\%}$$! Far from being "neutral," a flat prior puts 96% of its mass on impossible relationships.

## 1. What makes choosing priors for regression hard?

In regression, we usually have at least three kinds of parameters: the intercept $$\alpha$$, the slope $$\beta$$, and the noise $$\sigma$$. If we are not careful, a prior can be too wide and allow absurd values, too narrow and distort the posterior, or simply make the sampler run harder than necessary.

This is why choosing priors for regression is both a statistical matter and a matter of understanding the scale and context of the data.

## 2. Standardization: a step well worth doing before thinking about priors

One of the simplest ways to make prior selection easier is to standardize the data. For example, we can write:

$$
x_{std} = \frac{x-\bar{x}}{\mathrm{SD}(x)}, \qquad
y_{std} = \frac{y-\bar{y}}{\mathrm{SD}(y)}.
$$

After this step, the variable has a mean close to 0 and a standard deviation close to 1, and therefore "standard" priors also become much easier to choose.

![Data on the original scale before standardizing]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_standardization_raw_data.png)

![Data after standardizing to mean 0 and SD 1]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_standardization_standardized_data.png)

### Why does standardization help so much?

#### 1. The intercept is easier to interpret

After centering or standardizing, the intercept is usually close to the mean of $$y$$ at the central level of $$x$$, so interpreting it becomes more natural.

#### 2. The prior no longer depends too strongly on the measurement unit

For example, cm versus m, or kg versus pounds, can make a prior that "reads the same" mean something completely different if you do not standardize.

#### 3. The sampler usually runs more smoothly

When the variables are on relatively similar scales, the posterior is usually friendlier to HMC/NUTS, the Hamiltonian sampling algorithms commonly used in modern Bayes.

### 2.1. A concrete example: the same prior before and after standardizing

Suppose $$x$$ is height in cm, mostly in the range 150 to 190, and $$y$$ is weight in kg, around 45 to 90.

If you have not standardized and set directly:

$$
\alpha \sim \mathcal{N}(0,1), \qquad \beta \sim \mathcal{N}(0,1),
$$

then these two priors sound "nice" but are actually hard to accept semantically.

- The prior $$\alpha \sim \mathcal{N}(0,1)$$ implicitly says that when $$x=0$$ cm, the average weight will be around 0 kg, which is clearly meaningless in the height - weight context.
- The prior $$\beta \sim \mathcal{N}(0,1)$$ has an approximate 95% range from $$-2$$ to $$2$$ kg/cm. That means that with just a 20 cm difference in height, the model is already ready to accept an average difference from $$-40$$ to $$40$$ kg, which is usually too wide for many practical problems.

But if you standardize both $$x$$ and $$y$$ into $$x_{std}, y_{std}$$ and only then set:

$$
\alpha \sim \mathcal{N}(0,1), \qquad \beta \sim \mathcal{N}(0,1),
$$

then the meaning changes completely:

- $$\alpha$$ around 0 now means that the mean value of $$y$$ at the central level of $$x$$ also lies around the data mean, which is very natural.
- $$\beta$$ around 0 with standard deviation 1 now means that when $$x$$ increases by 1 standard deviation, $$y$$ typically changes within a region of a few standard deviations, i.e. still flexible enough but no longer "flying off the ground".

This is why standardization is not just a technical trick. It turns a prior from something hard to understand into a statement that can be read intuitively.

## 3. Prior for the intercept $$\alpha$$

After standardizing, the intercept should usually lie around 0 with moderate uncertainty. So a prior such as:

$$
\alpha \sim \mathcal{N}(0,1)
$$

or

$$
\alpha \sim \mathcal{N}(0,2)
$$

is usually a reasonable start.

The three contrasting situations below show that the prior for the intercept can be too wide, moderate, or too narrow.

![A prior that is too wide for the intercept]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_intercept_too_wide.png)

![Prior weakly informative cho intercept]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_intercept_weakly_informative.png)

![A prior that is too narrow for the intercept]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_intercept_too_narrow.png)

The intuition here is fairly simple: a prior that is too wide allows unrealistic values, a prior that is too narrow forces the model too hard, while a moderate prior keeps regularization yet remains flexible enough to let the data speak.

## 4. Prior for the slope $$\beta$$

After standardization, the slope has a very clear meaning: when $$x$$ increases by 1 standard deviation, by how many standard deviations does $$y$$ change on average.

Then a prior such as:

$$
\beta \sim \mathcal{N}(0,1)
$$

is usually quite reasonable for many problems.

This prior says that we expect the slope not to be too extreme, but still leave it open to both positive and negative effects.

If you have no strong prior knowledge, this is a very good weakly informative choice.

The three choices below help you see clearly the difference between a prior that is too wide, weakly informative, and too narrow for the slope.

![A prior that is too wide for the slope]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_slope_too_wide.png)

![Prior weakly informative cho slope]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_slope_weakly_informative.png)

![A prior that is too narrow for the slope]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_slope_too_narrow.png)

## 5. Prior for the noise $$\sigma$$

Because $$\sigma > 0$$, we usually use positive priors such as HalfNormal, Exponential, or sometimes HalfStudentT.

A common choice after standardization is:

$$
\sigma \sim \mathrm{HalfNormal}(1).
$$

![HalfNormal prior curve for the noise sigma]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_noise_halfnormal_curve.png)

The intuition here is that we expect the noise to be moderate, but still want to leave the model enough room to accept noisier data if that is actually observed.

![Summary of how to read the prior for the noise sigma]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_noise_halfnormal_summary.png)

## 6. What are weakly informative priors, and why should we usually start there?

A weakly informative prior does not mean "I know nothing". What it really means is that I do not want to impose a very strong belief, but I still want to remove absurd values that domain knowledge can reject right from the start.

In regression, this is a very useful way to regularize the model, making the posterior more stable and keeping the sampler from being pulled into meaningless regions of parameter space.

## 7. Prior predictive check: the most important step of this lesson

If you only look at the prior on the parameters, it is often hard to know whether it is reasonable. But if you use that prior to generate simulated data, everything becomes very clear.

The idea is to draw $$\alpha,\beta,\sigma$$ from the prior, generate many fake regression lines from those draws, and then see whether those lines produce data that is realistic in practical terms.

![Prior predictive with a weakly informative slope]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_predictive_weakly_informative.png)

For example, if the prior for the slope yields absurdly steep lines, or generates predictions such as negative weight, exam scores of 300 points, or absurdly explosive revenue growth, then the prior has a problem, even though mathematically it is "valid".

![Prior predictive with a slope that is too wide]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_predictive_too_wide.png)

## 8. An intuitive example: advertising and revenue

Suppose you model $$x$$ as advertising cost and $$y$$ as revenue. If the prior for the slope is too wide, the model may implicitly accept that a tiny increase in budget makes revenue explode absurdly, or conversely, that a slight increase in advertising makes revenue collapse very sharply.

Before looking at the data, you already know that many of those scenarios are unrealistic. The prior needs to reflect that.

### 8.1. How is the prior predictive read in numbers?

Suppose you have standardized the advertising and revenue data, and you are deciding between two priors for the slope:

$$
\beta \sim \mathcal{N}(0,3)
$$

or

$$
\beta \sim \mathcal{N}(0,0.5).
$$

With the first prior, the 95% interval for $$\beta$$ is approximately $$[-6,6]$$. If a new campaign sits at $$x_{std}=2$$, i.e. 2 standard deviations above the mean, then the predicted mean alone:

$$
\mu = \alpha + \beta x_{std}
$$

can already be pulled into a region of about $$-12$$ to $$12$$ standard deviations of $$y$$, before even adding noise. For many business problems, this is a sign of being so wide as to be unrealistic.

By contrast, with

$$
\beta \sim \mathcal{N}(0,0.5),
$$

the 95% interval for the slope is only about $$[-1,1]$$. At the same level $$x_{std}=2$$, the model mainly allows the predicted mean to lie in a region of about $$-2$$ to $$2$$ standard deviations around the center. That is still a sufficiently open space, but much closer to practical intuition.

This example shows why the prior predictive check is stronger than just looking at the prior plot over the parameters: it forces us to read the prior in the language of the data the model will generate.

## 9. Prior sensitivity analysis

After fitting the model, a very worthwhile question to ask is: **If I change to another reasonable prior a little, does the posterior change a lot?** If the posterior changes strongly, that may signal that the data is not strong enough, the prior is influencing the result considerably, and so you need to be more transparent when reporting conclusions.

![Posterior when changing different reasonable priors]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_sensitivity_posterior_overlay.png)

Sensitivity analysis is not meant to find an "absolutely correct" prior. Its goal is to understand how much your conclusions depend on the prior.

![Summary of how to read prior sensitivity analysis]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_sensitivity_summary.png)

## 10. A very practical set of starting priors

With standardized data, a good set of starting priors for simple linear regression is usually:

$$
\alpha \sim \mathcal{N}(0,1)
$$

$$
\beta \sim \mathcal{N}(0,1)
$$

$$
\sigma \sim \mathrm{HalfNormal}(1)
$$

This is not a fixed truth for every problem, but it is a very healthy default to start from.

## 11. Common mistakes when choosing priors for regression

### 11.1. Choosing a prior without looking at the data scale

This is a very common error.

### 11.2. Using an extremely wide prior and calling it "non-informative"

A prior that is too wide often has bad consequences such as difficult sampling, absurd prior predictives, and a posterior that is harder to read.

### 11.3. Not doing a prior predictive check

This throws away an extremely powerful check.

### 11.4. Not checking sensitivity

A prior that looks reasonable should still be challenged with a few neighboring choices.

> **3 key ideas.** Standardization is usually the best step to make priors for regression easier to choose and interpret; weakly informative priors help remove absurd values while still letting the data speak strongly; and the prior predictive check together with sensitivity analysis are two important tools for evaluating priors in regression.

## Reference videos

- [Bayesian Priors Explained | Prior Modelling & Prior Predictive Checks](https://www.youtube.com/watch?v=G3ludfAUAng) — stats 4 good, English. **watch first**. Watch how a prior is stated and then checked with a prior predictive, exactly the habit the lesson wants when choosing priors for regression.
- [Keynote 2: Weakly Informative Priors -- Andrew Gelman](https://www.youtube.com/watch?v=UH6-9FU6bRg) — AISTATS 2014, English. Watch the argument for weakly informative priors, supporting the part of the lesson that takes a weakly informative prior as the starting point.
- [Standardized variables in a simple regression](https://www.youtube.com/watch?v=RTFnrK5ZZ8E) — Jos Dornschneider-Elkink, English. Watch how the coefficient changes meaning after standardizing variables, used for the part that explains why standardization comes before setting a prior.

## Practice questions

1. Why does standardization make prior selection easier?
2. Explain in words what a weakly informative prior for the slope is saying.
3. What does the prior predictive check test that looking at the prior over the parameters may not show us?
4. In one of your own regression problems, which parameter is where the prior needs the most careful choice?

## References

- Gelman, A., Simpson, D., & Betancourt, M. (2017). The prior can often only be understood in the context of the likelihood.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 4.
- Gelman, A. et al. *Regression and Other Stories*.

---

*Next lesson: [4.3 Posterior Inference with PyMC - From Theory to Practice]({{ site.baseurl }}/contents/en/chapter04/04_03_posterior_inference_pymc/)*
