---
layout: post
title: "Lesson 6.2: Poisson Regression - Count Data"
chapter: '06'
order: 2
owner: Nguyen Le Linh
lang: en
categories:
- chapter06
lesson_type: required
---

Counts—hospital ER visits, daily bug reports, species sightings, website clicks—are strictly non-negative integers whose variance naturally grows with their mean. **Bayesian Poisson Regression** handles count data cleanly via the **log link** $$\ln \lambda_i = \alpha + \beta x_i \iff \lambda_i = e^{\alpha + \beta x_i}$$, guaranteeing positive rates everywhere and turning additive linear effects into **multiplicative rate ratios**!

This lesson builds complete mastery over log-link Poisson GLMs, **exposure offsets** (`+ log(exposure)`), and diagnosing **overdispersion** (when you must upgrade from Poisson to Negative Binomial).

---

## Key ideas: Log Links, Exposure Offsets, and Overdispersion

1. **Log Link Guarantees $$\lambda_i > 0$$:** Writing $$\lambda_i = \exp(\alpha + \beta x_i)$$ makes +1 unit of $$x$$ multiply the expected count by $$e^\beta$$ (Incidence Rate Ratio — IRR).
2. **Why Priors Must Be Tight on the Log Scale:** Because $$e^{10} \approx 22{,}026$$ and $$e^{20} \approx 4.85\times 10^8$$, a careless $$\beta \sim \mathcal{N}(0, 10^2)$$ prior predicts billions of events per second! Weakly informative priors like $$\beta \sim \mathcal{N}(0, 0.5)$$ keep prior predictive counts realistic.
3. **Exposure Offsets (`ln(T_i)`):** When observations cover different time spans or populations (e.g., 7 days vs. 30 days), model the *rate* $$\lambda_i / T_i = e^{\alpha + \beta x_i} \iff \ln\lambda_i = \ln(T_i) + \alpha + \beta x_i$$—adding $$\ln(T_i)$$ with a fixed coefficient of `1`!
4. **Overdispersion $$\to$$ Gamma–Poisson (Negative Binomial):** Poisson enforces $$\mathrm{Var}(Y_i) = \lambda_i$$; if real counts show extra variance, switch to Negative Binomial ($$\mathrm{Var} = \lambda + \lambda^2/\phi$$) so credible intervals aren’t falsely narrow!

---

## Learning objectives

After completing this lesson, you will understand **Poisson Regression** as the standard model for **count data**, that is, data recording the number of times an event occurs. You will see why linear regression is not suitable when the outcome takes only non-negative integers, why the **log link function** helps the model produce valid predictions, and why the model's coefficients should be interpreted through the **rate ratio** rather than a simple additive difference. This is the second important GLM after logistic regression.

## Introduction: Count Data Everywhere

**Count data** appears in many real-world settings, such as the number of customers arriving at a store per hour, the number of emails received per day, the number of accidents on a highway per month, the number of goals in a football match, or the number of mutations in a DNA segment. What these variables have in common is $$y \in \{0,1,2,3,\ldots\}$$, that is, they are non-negative integers, usually with no clear upper bound, and their variance usually grows as the mean grows. This leads to the familiar question: can we use linear regression for this kind of data?

## 1. The Problem of Linear Regression for Count Data

![Poisson Regression Basics]({{ site.baseurl }}/img/chapter_img/chapter06/poisson_regression_basics.png)

The basic difficulty of linear regression in this setting is that a linear model can produce negative predictions, while the number of occurrences of an event cannot be less than 0. The figure shows that in the left panel, the linear regression line can enter the region of negative values, while in the right panel, Poisson regression uses the **log link** to ensure that the intensity parameter $$\lambda$$ is always positive. In other words, instead of predicting the count directly, we model the log of the expected rate, so the output is always consistent with the nature of the data.

## 2. Poisson Regression: Generative Model

### 2.1. Log Link Function

The core idea of Poisson regression is to keep the linear part inside, but use the **log link function** to ensure that the final quantity, the expected rate $$\lambda$$, is always greater than 0.

**Log link**:
$$
\log(\lambda) = \alpha + \beta x
$$

**Inverse** (exponential):
$$
\lambda = e^{\alpha + \beta x}
$$

### 2.2. Generative Story

In the language of the **generative story**, the model is read as follows. From the predictor $$x$$, we create a linear quantity $$\eta=\alpha+\beta x$$. This quantity is then passed through the exponential function to produce the expected rate $$\lambda=\exp(\eta)$$. Finally, the observed count is generated from a Poisson distribution, that is $$y\sim\text{Poisson}(\lambda)$$. Separating these three steps clearly helps us see that the model both keeps the linear part that is convenient for inference and respects the specific probabilistic structure of count data.

The Poisson distribution has the form:
$$
P(y = k \mid \lambda) = \frac{\lambda^k e^{-\lambda}}{k!}
$$

A distinctive feature of this distribution is that the mean and the variance are both equal to $$\lambda$$; this property is often called **equidispersion** (meaning the mean equals the variance).

![Exponential Function Parameters]({{ site.baseurl }}/img/chapter_img/chapter06/exponential_function_parameters.png)

The figure helps us read the exponential function more intuitively. In the left panel, the basic function $$\lambda=e^\eta$$ is always positive and passes through the point $$\lambda=1$$ when $$\eta=0$$, so it can be seen as the baseline rate level. In the middle panel, changing $$\alpha$$, the **intercept**, mainly shifts the whole curve up or down, thereby changing the baseline level of the rate. In the right panel, changing $$\beta$$, the **slope**, makes the rate increase faster or slower with $$x$$, so it reflects the strength of the relationship between the predictor and the intensity of the event.

## 3. Bayesian Poisson Regression in PyMC

```python
import pymc as pm
import arviz as az

# Generate data
np.random.seed(42)
n = 150
x = np.random.uniform(0, 5, n)
lambda_true = np.exp(0.5 + 0.4*x)
y = np.random.poisson(lambda_true)

# Standardize predictor
x_z = (x - x.mean()) / x.std()

# Bayesian Poisson regression
with pm.Model() as poisson_model:
    # Priors
    alpha = pm.Normal('alpha', 2, 1)  # log(λ) ~ 2 → λ ~ 7
    beta = pm.Normal('beta', 0, 1)
    
    # Linear predictor
    eta = alpha + beta * x_z
    
    # Exponential transformation
    lambda_ = pm.Deterministic('lambda', pm.math.exp(eta))
    
    # Likelihood
    y_obs = pm.Poisson('y_obs', mu=lambda_, observed=y)
    
    # Sample
    trace = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                     return_inferencedata=True)

# Summary
print("\n" + "=" * 70)
print("POSTERIOR SUMMARY")
print("=" * 70)
summary = az.summary(trace, var_names=['alpha', 'beta'])
print(summary)
print("=" * 70)

# Visualize posteriors
az.plot_posterior(trace, var_names=['alpha', 'beta'],
                 figsize=(14, 5))
plt.suptitle('Posterior Distributions',
            fontsize=14, fontweight='bold', y=1.05)
plt.tight_layout()
plt.show()

# Trace plots
az.plot_trace(trace, var_names=['alpha', 'beta'], compact=True,
             figsize=(14, 6))
plt.suptitle('Trace Plots (Check Convergence)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### Experiment: the Poisson regression posterior and the rate ratio

Add count data points one at a time; the bundle of λ(x) curves and the rate ratio exp(b) gradually narrow.

<div class="interactive-demo" markdown="1">
<div data-demo="glm-explainer" data-lang="en" data-tab="poisson"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 4. Interpretation: Rate Ratios

### 4.1. Rate Ratio

**On log scale**:
$$
\log(\lambda) = \alpha + \beta x
$$

On the log scale, each time $$x$$ increases by 1 unit, the log of the expected rate increases by $$\beta$$ units.

**On rate scale**:
$$
\lambda = e^{\alpha + \beta x}
$$

When returning to the original scale, this means the expected rate is multiplied by $$e^\beta$$. This quantity $$e^\beta$$ is the **rate ratio**, and it is the most natural way to interpret a coefficient of Poisson regression.

### 4.2. A concrete example: how visits to a shop increase

Suppose the posterior mean of the model is:

$$
\log(\lambda)=2.30 + 0.25x
$$

where $$x$$ is the number of advertising campaigns running in the week. Then:

- If $$x=0$$ then $$\lambda=e^{2.30}\approx 10$$, meaning the shop expects about 10 visits per day.
- If $$x=1$$ then $$\lambda=e^{2.55}\approx 12.8$$.
- If $$x=2$$ then $$\lambda=e^{2.80}\approx 16.4$$.

Here $$e^{0.25}\approx 1.28$$, so each time one more advertising campaign is added, the expected number of visits is multiplied by about 1.28, that is, an increase of nearly 28%. This does not mean it always increases by a fixed 0.25 visits or always by exactly 2.8 visits. Because the effect in Poisson regression is **multiplicative** rather than **additive**, the absolute increase depends on the starting baseline: from 10 to 12.8 is an increase of about 2.8 visits, while from 12.8 to 16.4 is an increase of about 3.6 visits.

```python
# Compute rate ratios
beta_samples = trace.posterior['beta'].values.flatten()
rate_ratio = np.exp(beta_samples)

print("\n" + "=" * 70)
print("RATE RATIO INTERPRETATION")
print("=" * 70)
print(f"\nβ (log scale): {beta_samples.mean():.3f}")
print(f"Rate Ratio (e^β): {rate_ratio.mean():.3f}")
print(f"95% CI: [{np.percentile(rate_ratio, 2.5):.3f}, " +
      f"{np.percentile(rate_ratio, 97.5):.3f}]")

print("\nInterpretation:")
print(f"  1 SD increase in x → rate multiply by {rate_ratio.mean():.2f}")
if rate_ratio.mean() > 1:
    print(f"  → {(rate_ratio.mean()-1)*100:.1f}% increase in rate")
else:
    print(f"  → {(1-rate_ratio.mean())*100:.1f}% decrease in rate")
print("=" * 70)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Beta (log scale)
axes[0].hist(beta_samples, bins=50, density=True, alpha=0.7,
            color='skyblue', edgecolor='black')
axes[0].axvline(beta_samples.mean(), color='red', linewidth=3,
               label=f'Mean = {beta_samples.mean():.3f}')
axes[0].axvline(0, color='black', linestyle='--', linewidth=2)
axes[0].set_xlabel('β (log scale)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('COEFFICIENT β\n(Log Scale)',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')

# Rate ratio
axes[1].hist(rate_ratio, bins=50, density=True, alpha=0.7,
            color='lightgreen', edgecolor='black')
axes[1].axvline(rate_ratio.mean(), color='red', linewidth=3,
               label=f'Mean = {rate_ratio.mean():.3f}')
axes[1].axvline(1, color='black', linestyle='--', linewidth=2)
axes[1].set_xlabel('Rate Ratio (e^β)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('RATE RATIO\n(Multiplicative Effect)',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

## 5. Posterior Predictive Checks

```python
# Posterior predictive
with poisson_model:
    ppc = pm.sample_posterior_predictive(trace, random_seed=42)

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Predicted rates
lambda_samples = trace.posterior['lambda'].values.reshape(-1, n)
lambda_mean = lambda_samples.mean(axis=0)
lambda_lower = np.percentile(lambda_samples, 2.5, axis=0)
lambda_upper = np.percentile(lambda_samples, 97.5, axis=0)

sort_idx = np.argsort(x)
axes[0, 0].scatter(x, y, alpha=0.4, s=40, label='Observed', edgecolors='black')
axes[0, 0].plot(x[sort_idx], lambda_mean[sort_idx], 'r-', linewidth=3,
               label='Posterior mean λ')
axes[0, 0].fill_between(x[sort_idx], lambda_lower[sort_idx], lambda_upper[sort_idx],
                        alpha=0.3, color='red', label='95% CI')
axes[0, 0].set_xlabel('x', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('y (counts)', fontsize=12, fontweight='bold')
axes[0, 0].set_title('PREDICTED RATES\nwith Uncertainty',
                    fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=11)
axes[0, 0].grid(alpha=0.3)

# Observed vs Predicted
y_pred = ppc.posterior_predictive['y_obs'].values.reshape(-1, n)
y_pred_mean = y_pred.mean(axis=0)

axes[0, 1].scatter(y, y_pred_mean, alpha=0.5, s=50, edgecolors='black')
axes[0, 1].plot([0, max(y)], [0, max(y)], 'r--', linewidth=2,
               label='Perfect prediction')
axes[0, 1].set_xlabel('Observed y', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Predicted E[y]', fontsize=12, fontweight='bold')
axes[0, 1].set_title('POSTERIOR PREDICTIVE CHECK\nObserved vs Predicted',
                    fontsize=14, fontweight='bold')
axes[0, 1].legend(fontsize=11)
axes[0, 1].grid(alpha=0.3)

# Distribution comparison
axes[1, 0].hist(y, bins=range(0, max(y)+2), alpha=0.6, density=True,
               label='Observed', edgecolor='black')
for i in range(min(100, y_pred.shape[0])):
    axes[1, 0].hist(y_pred[i], bins=range(0, max(y)+2), alpha=0.01,
                   density=True, color='red')
axes[1, 0].set_xlabel('y (counts)', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1, 0].set_title('DISTRIBUTION CHECK\nObserved vs PPC samples',
                    fontsize=14, fontweight='bold')
axes[1, 0].legend(fontsize=11)
axes[1, 0].grid(alpha=0.3, axis='y')

# Residuals
residuals = y - lambda_mean
axes[1, 1].scatter(lambda_mean, residuals, alpha=0.5, s=50, edgecolors='black')
axes[1, 1].axhline(0, color='red', linestyle='--', linewidth=2)
axes[1, 1].set_xlabel('Predicted λ', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Residuals (y - λ)', fontsize=12, fontweight='bold')
axes[1, 1].set_title('RESIDUAL PLOT\nCheck for patterns',
                    fontsize=14, fontweight='bold')
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## 6. Overdispersion: When Variance > Mean

A central assumption of Poisson regression is that the variance equals the mean. In real data, this assumption is often broken because the variance is larger than the mean, a phenomenon called **overdispersion**. When that happens, the Poisson model tends to be overconfident and underestimate uncertainty. Two common remedies are to use **Negative Binomial regression** when we need to let the variance exceed the mean flexibly, or to use **Zero-Inflated Poisson** if the data has more zeros than ordinary Poisson can explain.

```python
# Check overdispersion
print("\n" + "=" * 70)
print("OVERDISPERSION CHECK")
print("=" * 70)
print(f"\nObserved data:")
print(f"  Mean: {y.mean():.2f}")
print(f"  Variance: {y.var():.2f}")
print(f"  Variance/Mean ratio: {y.var()/y.mean():.2f}")

if y.var() / y.mean() > 1.5:
    print("\n→ Overdispersion detected!")
    print("  Consider Negative Binomial or Zero-Inflated models")
else:
    print("\n→ Poisson assumption reasonable")
print("=" * 70)
```

### Experiment: Poisson or Negative Binomial?

From var/mean to the posterior predictive check: Poisson is rejected, and Negative Binomial can describe the dispersion.

<div class="interactive-demo" markdown="1">
<div data-demo="overdisp-explainer" data-lang="en" data-data="nb"></div>
</div>

## Summary

Poisson regression is the natural model for count data because it addresses exactly the weakness of linear regression: the prediction of a linear model can be negative, while count data cannot. By using the **log link**, modeling $$\log(\lambda)=\alpha+\beta x$$ and then deriving $$\lambda$$ on the original scale, Poisson regression ensures that the expected rate is always positive. The model's coefficients are best understood through the **rate ratio** $$e^\beta$$, and the most important assumption that always needs checking is whether the variance is approximately equal to the mean. If the data is overdispersed, we must think of more flexible models.

The core point to remember is that the log link function is not just a mathematical trick, but the mechanism that makes the linear part of the model compatible with the nature of count data and rate data.

Next lesson: **Model Evaluation for GLMs**.

---

### Worked Numerical Example: Computing Multiplicative Rates & Exposure Offsets by Hand

Suppose a website’s daily bug count follows $$\ln\lambda = 1.0 + 0.5 x + \ln(T)$$ where $$x$$ is code-complexity score and $$T$$ is observation window in days:
1. **For $$T = 1$$ day ($$\ln 1 = 0$$):**
   - At $$x = 0$$: $$\lambda = e^{1.0} \approx \mathbf{2.72}$$ bugs/day.
   - At $$x = 1$$: $$\lambda = e^{1.5} \approx \mathbf{4.48}$$ bugs/day (multiplied by $$e^{0.5} \approx \mathbf{1.649\times}$$, i.e., **+64.9%**!).
   - At $$x = 2$$: $$\lambda = e^{2.0} \approx \mathbf{7.39}$$ bugs/day (multiplied by $$1.649\times$$ again!).
2. **For $$T = 7$$ days at $$x = 0$$:** Adding offset $$\ln(7)$$ gives $$\lambda = e^{1.0 + \ln 7} = 7 \times 2.72 = \mathbf{19.03}$$ bugs/week—scaling linearly with exposure time!

### Explanation: Four Rules for Bayesian Count Regression

1. **Always check prior predictive counts *before* running MCMC:** An exponential link explodes fast—verify your prior doesn’t simulate $$10^{12}$$ events!
2. **Never divide counts by exposure and feed the ratio into Poisson:** Poisson requires *integer* counts; keep raw integer $$y_i$$ as the outcome and put `np.log(exposure)` on the right-hand side as an offset!
3. **Always check for overdispersion and excess zeros via PPC:** Compare observed variance-to-mean ratio and observed zero fraction against replicated Poisson draws—upgrade to Negative Binomial or Zero-Inflated Poisson if Poisson fails!
4. **Watch extreme leverage points:** Because $$\exp(\beta x)$$ curves steeply upward, a single high-$$x$$ observation carries huge influence in Poisson GLMs.

**Quick check.** In a Poisson regression with log link, if a predictor has slope $$\beta = -0.20$$, by roughly what percentage does the expected count *decrease* for each +1 unit increase in that predictor? *(Hint: compute $$e^{-0.20} \approx 0.819$$.)*

---

## Reference videos

- [Poisson regression - clearly explained](https://www.youtube.com/watch?v=Obpz_Uvo2rQ) — TileStats, English. **watch first**. Watch Poisson regression for count data and why a straight line cannot keep counts non-negative.
- [Regression with Count Data: Poisson and Negative Binomial](https://www.youtube.com/watch?v=uGKnoAw-PFQ) — Matthew E. Clapham, English. Watch the Poisson count model next to the Negative Binomial, supporting the part of the lesson where the variance exceeds the mean.
- [Statistical Rethinking 2023 - 10 - Counts & Hidden Confounds](https://www.youtube.com/watch?v=jokxu18egu0) — Richard McElreath, English. Watch count models together with hidden confounds, used for the passage that writes Poisson as a Bayesian GLM.

## Exercises

**Exercise 1**: Generate count data. Fit Poisson regression. Interpret rate ratio.

**Exercise 2**: Compare linear vs Poisson predictions. Visualize differences.

**Exercise 3**: Multiple predictors Poisson regression. Interpret each coefficient.

**Exercise 4**: Real data - predict number of customer visits from time/weather features.

**Exercise 5**: Check for overdispersion. If present, try Negative Binomial model.

## References

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.
- Chapter 6: Generalized linear models

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 11: God Spiked the Integers

---

*Next lesson: [6.3 Model Evaluation for GLMs]({{ site.baseurl }}/contents/en/chapter06/06_03_model_evaluation_glm/)*
