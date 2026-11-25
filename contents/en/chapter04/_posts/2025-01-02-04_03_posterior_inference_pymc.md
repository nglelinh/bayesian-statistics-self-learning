---
layout: post
title: "Lesson 4.3: Posterior Inference with PyMC - From Theory to Practice"
chapter: '04'
order: 4
owner: Nguyen Le Linh
lang: en
categories:
- chapter04
lesson_type: required
---

Writing a Bayesian model on a whiteboard is deeply satisfying—until you actually want to run it on real data. That is where probabilistic programming languages like **PyMC** come in: you write the exact generative story in 6 lines of Python, hit `pm.sample()`, and NUTS automatically differentiates your log-posterior and draws thousands of correlated samples. Yet treating `pm.sample()` as a black box is dangerous: before you interpret a single credible interval, you need to know how to back-transform standardized coefficients, read $$\hat{R}$$ and ESS, and check whether your Monte Carlo standard error is small enough to trust.

**Lesson Roadmap:** Translating math to PyMC code → Key ideas (Probabilistic programming & autodiff, Sampler diagnostics before interpretation, Posterior predictive propagation) → Hand-worked standardization back-transform & MCSE check → Full PyMC workflow, code, and exercises.

## Learning objectives

After this lesson, you need to know how to turn Bayesian regression from a generative story into a model that runs in PyMC. You also need to understand a basic practical workflow: standardizing the data, writing priors, declaring the likelihood, sampling the posterior, reading diagnostics, and interpreting the results.

> **Mini example.** Once you understand the generative story and know how to choose reasonable priors, the next step is to write the real model in PyMC to get the posterior of the intercept, slope and noise. PyMC does not think about the model for you; it helps you implement that model more efficiently.
>
> **Quick check.** If PyMC has already produced the posterior, why do we still have to look at diagnostics before interpreting the results?

## Key ideas: From Mathematical Model to Reliable PyMC Inference

### 1. Probabilistic Programming and Automatic Differentiation
- **What it is:** Expressing random variables (`pm.Normal`, `pm.HalfNormal`) as nodes in a computational graph whose exact log-density gradient $$\nabla \log p(\theta \mid D)$$ is computed automatically via reverse-mode autodiff (PyTensor).
- **What it studies:** Decoupling *model specification* (what you believe about the world) from *inference* (how NUTS explores the posterior).

### 2. Diagnostic Gating: Never Interpret an Unchecked Posterior
- **What it is:** Checking **divergences** (must be 0), **$$\hat{R}$$** ($$\le 1.01$$), **bulk/tail ESS** (ideally $$> 400$$), and **MCSE** (Monte Carlo Standard Error $$\mathrm{SD}/\sqrt{\mathrm{ESS}}$$) before looking at parameter means.
- **What it studies:** Ensuring numerical approximation error from finite MCMC draws is negligible compared to genuine posterior uncertainty.

### 3. Posterior Summaries vs. Posterior Predictive Draws
- **What it is:** Distinguishing `idata.posterior` (distributions over parameters $$\alpha, \beta, \sigma$$) from `pm.sample_posterior_predictive` (distributions over *new data* $$y^*$$).
- **What it studies:** Propagating full joint parameter uncertainty—including correlations between $$\alpha$$ and $$\beta$$—into real-world predictions and intervals.

## Explanation: Back-Transforming Standardized PyMC Output & Checking MCSE

Suppose you standardize height ($$\bar{x} = 170\text{ cm},\, s_x = 10\text{ cm}$$) and weight ($$\bar{y} = 65\text{ kg},\, s_y = 12\text{ kg}$$), fit a PyMC model, and `az.summary()` reports:
- $$\alpha_z \approx 0.02$$, $$\beta_z \approx 0.80$$ (with posterior $$\mathrm{SD}(\beta_z) = 0.12$$ and $$\mathrm{ESS} = 1{,}600$$).

### 1. Convert standardized parameters back to physical units (kg and cm)
Since $$\frac{y - \bar{y}}{s_y} = \alpha_z + \beta_z \frac{x - \bar{x}}{s_x}$$, solving for $$y = \alpha + \beta x$$ gives:
- **Physical slope:** $$\beta = \beta_z \frac{s_y}{s_x} = 0.80 \times \frac{12}{10} = \mathbf{0.96\text{ kg/cm}}.$$
- **Physical intercept:** $$\alpha = \bar{y} + s_y \alpha_z - \beta \bar{x} = 65 + 12(0.02) - 0.96(170) = 65.24 - 163.20 = \mathbf{-97.96\text{ kg}}.$$
(This immediately shows why centering matters: $$-97.96\text{ kg}$$ at height $$0\text{ cm}$$ is meaningless, while $$\alpha_z = 0.02$$ says an average-height person weighs $$65.24\text{ kg}$$!)

### 2. Verify Monte Carlo Standard Error (MCSE)
How noisy is our MCMC estimate of the posterior mean $$0.80$$?
$$ \mathrm{MCSE}(\beta_z) = \frac{\mathrm{SD}(\beta_z)}{\sqrt{\mathrm{ESS}}} = \frac{0.12}{\sqrt{1{,}600}} = \frac{0.12}{40} = \mathbf{0.003}. $$
Because $$0.003$$ is only **$$2.5\%$$** of the posterior SD (well below the $$5\%$$ rule of thumb), the reported mean `0.80` is numerically rock-solid to two decimal places.

## 1. From a model on paper to a model in code

In lessons 4.1 and 4.2, we already have all three ingredients: the generative story, priors for the parameters, and intuition about Bayesian regression.

This lesson mainly performs a very practical translation step: moving from statistical thinking to a model that can run in PyMC.

The minimal workflow here is to prepare the data, standardize if needed, declare the priors, declare the likelihood, run the sampler, check the diagnostics, and only then read the posterior.

## 2. Why do we need MCMC? Because there is no closed-form formula

### 2.1. From conjugacy to non-conjugacy

In Chapter 2, we learned about **conjugate priors**:

- **Beta-Binomial**: Prior Beta + Likelihood Binomial → Posterior Beta
- **Gamma-Poisson**: Prior Gamma + Likelihood Poisson → Posterior Gamma
- **Normal-Normal**: Prior Normal + Likelihood Normal → Posterior Normal

With these conjugate pairs, we have a **closed-form formula** to compute the posterior directly:

$$
\theta \mid D \sim \text{Beta}(\alpha_0 + k, \beta_0 + n - k)
$$

Just plug the numbers into the formula and you are done. **No powerful computer needed, no sampling.**

### 2.2. Bayesian regression: no more simple formula

But with **Bayesian regression**, the situation is more complicated:

$$
\begin{aligned}
\beta_0 &\sim \mathcal{N}(5, 5) \\
\beta_1 &\sim \mathcal{N}(2, 5) \\
\sigma &\sim \text{HalfNormal}(2) \\
y_i &\sim \mathcal{N}(\beta_0 + \beta_1 x_i, \sigma^2)
\end{aligned}
$$

**Problems:**
- Three parameters ($\beta_0, \beta_1, \sigma$) must be updated **simultaneously**
- The priors are Normal + HalfNormal (not conjugate with the likelihood)
- The posterior is a 3-dimensional **joint** distribution, with no simple formula

$$
p(\beta_0, \beta_1, \sigma \mid D) = \frac{p(D \mid \beta_0, \beta_1, \sigma) \cdot p(\beta_0) \cdot p(\beta_1) \cdot p(\sigma)}{p(D)}
$$

With $p(D) = \int\int\int p(D \mid \beta_0, \beta_1, \sigma) \cdot p(\beta_0) \cdot p(\beta_1) \cdot p(\sigma) \, d\beta_0 \, d\beta_1 \, d\sigma$

**This integral cannot be computed by hand!**

### 2.3. MCMC: sample instead of computing a formula

When there is no closed-form formula, we use **MCMC (Markov Chain Monte Carlo)**:

> **Core idea:** Instead of doing complicated mathematical computation, we **sample** from the posterior.
>
> Like an opinion survey: you do not ask all 10 million people, you only need to ask 4000 representative people.

**MCMC works as follows:**

1. **Start** from a random point in the parameter space
2. **Move** to a new point following a smart rule (favoring high-probability regions)
3. **Repeat** thousands of times to create a "chain" of samples
4. **Result:** The set of samples faithfully reflects the posterior distribution

**Illustrative example:**

```python
# Instead of computing a complicated formula:
posterior = complicated_integral(...)  # ❌ Cannot be computed!

# We sample:
with pm.Model() as model:
    # Declare priors
    beta_0 = pm.Normal('beta_0', mu=5, sigma=5)
    beta_1 = pm.Normal('beta_1', mu=2, sigma=5)
    sigma = pm.HalfNormal('sigma', sigma=2)
    
    # Likelihood
    mu = beta_0 + beta_1 * x
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
    
    # MCMC: draw 2000 samples from the posterior
    trace = pm.sample(2000)  # ← THIS IS MCMC!
    
# Result: trace contains 2000 sets (β₀, β₁, σ) from the posterior
# Each set is a "possible world" consistent with the data
```

**MCMC result:**

| Sample | β₀ | β₁ | σ |
|--------|----|----|---|
| 1 | 6.8 | 2.1 | 0.6 |
| 2 | 6.5 | 2.2 | 0.5 |
| ... | ... | ... | ... |
| 2000 | 6.9 | 2.0 | 0.7 |

From these 2000 samples, we can compute:
- **Posterior mean:** The average of the samples
- **95% Credible Interval:** The 2.5% and 97.5% percentiles
- **Probability β₁ > 0:** Count how many samples have β₁ > 0

### 2.4. Comparing conjugacy vs MCMC

| | Conjugate Priors | MCMC (Regression) |
|---|---|---|
| **Prior** | Beta, Gamma, simple Normal | Many complicated priors |
| **Likelihood** | Binomial, Poisson, Normal | Normal with many parameters |
| **Posterior** | Closed-form formula | No formula |
| **Computation** | Plug numbers into the formula | Sampling with MCMC |
| **Result** | Exact distribution | Approximation from samples |
| **Example** | Beta(17, 103) | 2000 samples (β₀, β₁, σ) |
| **Time** | < 1 second | 10-60 seconds |
| **Accuracy** | 100% | ~99% (with enough samples) |

### 2.5. PyMC hides the complexity of MCMC

The great thing about PyMC is that you do not need to understand deeply:
- Metropolis-Hastings algorithm
- Gibbs sampling
- NUTS (No-U-Turn Sampler)
- Hamiltonian Monte Carlo

You only need to:
1. Declare the model (priors + likelihood)
2. Call `pm.sample()`
3. Check diagnostics (R-hat, ESS)
4. Read the results

**PyMC automatically:**
- Chooses the best sampler (usually NUTS)
- Tunes automatically during the warm-up phase
- Parallelizes multiple chains
- Detects problems and warns you

### 2.6. Summary: When to use MCMC?

| Situation | Method |
|------------|-------------|
| Conjugate priors + 1 parameter | ✅ Closed-form formula |
| Non-conjugate or many parameters | ✅ MCMC |
| Regression with >2 parameters | ✅ MCMC (PyMC) |
| Hierarchical models | ✅ MCMC |
| Mixture models | ✅ MCMC |

**Simple rule:**
> If you cannot compute the posterior by hand in 5 minutes → Use MCMC!

## 3. What does a simple Bayesian regression in PyMC look like structurally?

The right way of thinking is always to start from the prior for $$\alpha$$, the prior for $$\beta$$, the prior for $$\sigma$$, and only then reach the likelihood:

$$
y_i \sim \mathcal{N}(\alpha + \beta x_i,\sigma).
$$

In PyMC, you are just rewriting that story as code.

What matters is that the code should reflect the model, not that the model be distorted just to fit a specific API.

### 3.1. A minimal but runnable PyMC example

Suppose you have a very small dataset on height and weight:

```python
import numpy as np
import pymc as pm
import arviz as az

height = np.array([150, 155, 160, 165, 170, 175, 180, 185], dtype=float)
weight = np.array([50, 54, 57, 62, 66, 70, 76, 82], dtype=float)

x_z = (height - height.mean()) / height.std()
y_z = (weight - weight.mean()) / weight.std()

with pm.Model() as reg_model:
    alpha = pm.Normal("alpha", 0, 1)
    beta = pm.Normal("beta", 0, 1)
    sigma = pm.HalfNormal("sigma", 1)

    mu = alpha + beta * x_z
    y_obs = pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y_z)

    idata = pm.sample(
        draws=2000,
        tune=2000,
        chains=4,
        target_accept=0.9,
        random_seed=42,
    )

az.summary(idata, var_names=["alpha", "beta", "sigma"])
```

Notably, each block of code maps directly onto the statistical story:

- `alpha`, `beta`, `sigma` are the three priors for the three core parameters,
- `mu = alpha + beta * x_z` is the mean line of the regression,
- `y_obs = pm.Normal(...)` is the likelihood, i.e. how the data is generated around that mean line,
- `pm.sample(...)` is the step that samples from the posterior instead of finding a single point estimate.

If you can keep the one-to-one link between the model on paper and this block of code, you are on the right track.

## 4. Why standardize the data before fitting?

Bayesian regression usually runs better when variables are well scaled.

The benefits of standardizing are that priors are easier to choose, the intercept is easier to interpret, the sampler usually converges more smoothly, and the posterior is also less "distorted by measurement units".

So in a great many cases, standardizing is a practice step worth having.

## 5. After sampling, what do we read first?

Many beginners jump straight to the posterior mean and interval. But the thing to look at first is actually the diagnostics, meaning whether the trace plot looks fine, whether R-hat is close to 1, whether ESS is sufficient, and whether the sampler emitted any warnings.

If this part is not good, every posterior interpretation afterwards should be considered tentative.

## 6. Interpreting the posterior in regression

When the model runs well, only then do we return to the statistical questions.

### 6.1. Intercept

With data that has been standardized or centered, the intercept is usually easier to read because it describes the mean value of $$y$$ when $$x$$ is at the central level.

### 6.2. Slope

The posterior of the slope tells whether the relationship is positive or negative, strong or weak, and how sure we are about it. The nice thing about Bayes is that you can directly ask what the probability of $$\beta > 0$$ is.

### 6.3. Noise

The posterior of $$\sigma$$ tells how widely the data is spread around the regression line, that is, how much unexplained variation the model still leaves behind.

### 6.4. Example: updating from prior to posterior for regression parameters

Suppose that after fitting a one-variable linear model with PyMC, we obtain the following summary:

- Prior: $$\alpha\sim\mathcal N(60,20),\;\beta\sim\mathcal N(0,2),\;\sigma\sim\text{HalfNormal}(5)$$.
- Posterior summary:
  - $$\alpha\mid D\approx \mathcal N(63.2,\,1.1^2)$$
  - $$\beta\mid D\approx \mathcal N(0.78,\,0.09^2)$$
  - $$\sigma\mid D$$ has a posterior mean of about $$2.4$$.

Quick interpretation:

- the data has pulled the intercept from a prior region around 60 up to about 63.2,
- the slope is clearly positive with small uncertainty (SD 0.09),
- the remaining noise is about 2.4 response units.

If we need an approximate 95% posterior interval for the slope (approximately Normal):

$$
0.78\pm 1.96\times 0.09\Rightarrow [0.604,\;0.956].
$$

This interval does not cross 0, so the posterior evidence supports a fairly clear positive relationship.

## 7. From parameter posteriors to predictions

Bayesian regression is not only for knowing what the slope is. It is also for predicting. For example, for a new value of $$x$$, we want to know where the predicted weight or exam score will be, and how wide the uncertainty that comes with that prediction is.

This is where PyMC is very convenient, because once we have posterior draws, we can move rather naturally into the posterior predictive.

### 7.1. A concrete example: prediction for a person 175 cm tall

With the model above, suppose you want to predict for a person 175 cm tall. We can directly take the posterior draws and propagate them to the prediction:

```python
posterior = az.extract(idata, group="posterior")

alpha_draws = posterior["alpha"].values
beta_draws = posterior["beta"].values
sigma_draws = posterior["sigma"].values

x_new_z = (175 - height.mean()) / height.std()

mu_new_z = alpha_draws + beta_draws * x_new_z
y_new_z = np.random.default_rng(42).normal(mu_new_z, sigma_draws)

mu_new = mu_new_z * weight.std() + weight.mean()
y_new = y_new_z * weight.std() + weight.mean()
```

The two objects here serve two different questions:

- `mu_new` is the distribution for the **predicted mean value**, i.e. the average weight of the group of people 175 cm tall under the model.
- `y_new` is the distribution for **a new observation**, i.e. the weight of one specific individual 175 cm tall.

Suppose that after summarizing these samples, you see:

- the mean of `mu_new` is about 71 kg with an 89% interval from 69 to 73 kg,
- while `y_new` has a wider 89% prediction interval, for example from 63 to 79 kg.

Then you should read the result in proper Bayesian language:

- the model is quite sure about the **average trend** in the region of 175 cm height,
- but still honestly says that **a new individual** can deviate from the average quite a lot.

This is exactly where posterior inference turns into prediction very naturally: we do not change the model, we just continue telling the generative story one step further.

## 8. A minimal healthy workflow when using PyMC for regression

You can remember this workflow as three consecutive stages, each with a central question that must be answered clearly before moving to the next step:

### Before running

Before running, ask whether the variables need standardizing, whether the priors are reasonable on the actual scale of the data, and whether the generative story is truly clear.

### While running

While running, watch whether the sampler issues any warnings and whether the warm-up phase is sufficient.

### After running

After running, look at whether the trace plot looks fine, whether R-hat and ESS are good, what the parameter posteriors are saying, and whether the posterior predictive is reasonable.

### Note on the known/unknown variance setting

In PyMC practice, we usually infer $$\sigma$$ as well, so the interval of the slope already reflects uncertainty about the noise. If you fix $$\sigma$$ in advance (a special problem), the interval for the slope is usually narrower. When reporting results, you should state clearly which scenario you are in.

## 9. Common mistakes of beginners using PyMC for regression

### 9.1. Treating PyMC as a black box

This is the biggest mistake.

If you do not understand the model, you will not know what the prior is saying, what the warnings are reporting, and whether the posterior is really trustworthy.

### 9.2. Reading only the posterior mean

The posterior mean is not enough. You need to look at the interval, the probability of exceeding a threshold, the shape of the posterior, and also the prediction uncertainty.

### 9.3. Forgetting model checking

Finishing the regression fit is not the end. The next lesson will emphasize posterior predictive checks, residual analysis, and prediction quality.

## 10. What this lesson wants you to keep

The goal is not to remember every line of the PyMC API. The goal is to see that Bayesian regression can be implemented very naturally as long as you keep the right thinking workflow. PyMC is just a tool; the most important parts are still the model story, the priors, the diagnostics, and how to interpret the posterior.

> **3 key ideas.** PyMC helps implement Bayesian regression following exactly the prior + likelihood + posterior structure you have learned; after fitting the model, diagnostics must always come before interpreting the posterior; and the real value of posterior inference lies not only in parameter estimation but also in the ability to move on to prediction and model checking.

## Reference videos

- [[114] Getting Started with PyMC (Chris Fonnesbeck)](https://www.youtube.com/watch?v=jrU0UBr2z3k) — Data Umbrella, English. **watch first**. Watch a PyMC model being declared and then sampled, exactly the step where the lesson goes from generative story to code.
- [L4: Interpretable Linear Regressions (State of Bayes Lecture Series)](https://www.youtube.com/watch?v=fpS0NjqNHn8) — PyMC Labs, English. Watch linear regression in PyMC and how to read the coefficients, supporting the lesson's workflow of standardization, priors and likelihood.
- [Chris Fonnesbeck - Probabilistic Python: An Introduction to Bayesian Modeling with PyMC](https://www.youtube.com/watch?v=911d4A1U0BE) — PyData, English. Watch a longer introduction to Bayesian modeling with PyMC, for when you need to see both the priors and the checks after sampling.

## Practice questions

1. List the 5 minimal steps of a Bayesian regression workflow with PyMC.
2. Why does standardizing the data usually help both prior selection and sampling?
3. If the posterior of the slope looks reasonable but R-hat is not good, what should you do?
4. In Bayesian regression, why is prediction just as important a part as estimation?

## References

- PyMC Documentation.
- ArviZ Documentation.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 4-5.

---

*Next lesson: [4.4 Model Checking and Prediction - Ensuring a Good Model]({{ site.baseurl }}/contents/en/chapter04/04_04_model_checking_prediction/)*
