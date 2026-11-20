---
layout: post
title: "Lesson 6.1: Logistic Regression - Binary Outcomes"
chapter: '06'
order: 1
owner: Nguyen Le Linh
lang: en
categories:
- chapter06
lesson_type: required
---

## Learning objectives

After completing this lesson, you will understand **Logistic Regression** as a foundational model for **binary outcomes** such as yes/no, success/failure, or 0/1. The focus of the lesson is not merely to swap in another regression formula, but to understand why linear regression is not suitable for binary data, why we need a **link function**, and why the model's coefficients must be interpreted through the **odds ratio** rather than with ordinary linear intuition. This is also the first doorway into the family of **Generalized Linear Models (GLMs)**.

## Introduction: The Problem of Linear Regression for Binary Data

Suppose we want to predict whether a person will buy a product, pass an exam, or have a disease. In all of these examples, the **outcome** takes only two values, that is $$y \in \{0,1\}$$. The natural question is whether we can simply use the familiar linear regression.

$$
y = \alpha + \beta x + \epsilon
$$

The problem appears immediately: linear regression can predict any value on the real line, from negative infinity to positive infinity, while a probability must lie in the interval $$[0,1]$$. This shows that we need a model that keeps a linear predictive part inside, but has a mechanism for transforming the final result into a valid probability.

## 1. Why Linear Regression Does Not Work

![Logistic Regression Basics]({{ site.baseurl }}/img/chapter_img/chapter06/logistic_regression_basics.png)

For binary data, the core difficulty of linear regression is that the model does not know that our output must be a probability. In the left panel, the linear regression line can produce predictions below 0 or above 1, which are meaningless values if we interpret them as probabilities. In the right panel, logistic regression fixes this by using the **logistic function** to turn a **linear predictor** into a valid probability, so that every prediction always lies within $$[0,1]$$.

## 2. Logistic Regression: Generative Model

![Link Functions Comparison]({{ site.baseurl }}/img/chapter_img/chapter06/link_functions_comparison.png)

### 2.1. Link Function

The central idea of logistic regression is still to build a linear expression at the inner level, but then pass it through a **link function** to ensure the final output is a probability.

**Logit link function**:
$$
\text{logit}(p) = \log\left(\frac{p}{1-p}\right) = \alpha + \beta x
$$

**Inverse** (logistic function):
$$
p = \frac{1}{1 + e^{-(\alpha + \beta x)}} = \frac{e^{\alpha + \beta x}}{1 + e^{\alpha + \beta x}}
$$

### 2.2. Generative Story

We can read the model in the spirit of a **generative story** as follows. First, from the predictor $$x$$ we create a linear quantity $$\eta=\alpha+\beta x$$. Next, this quantity is transformed through the logistic function to produce the probability $$p=\text{logistic}(\eta)$$. Finally, the binary observation is generated from a Bernoulli distribution, that is $$y\sim\text{Bernoulli}(p)$$. Writing it this way helps us see that logistic regression is not a “formula-transformation trick”, but a complete probabilistic model.

### 2.3. The Bayes classification rule from prior-likelihood-posterior

For class $$c_i$$ and feature $$x$$, the class posterior probability has the form:

$$
P(c_i\mid x)=\frac{P(x\mid c_i)P(c_i)}{\sum_j P(x\mid c_j)P(c_j)}
\propto P(x\mid c_i)P(c_i).
$$

With 0-1 loss, the optimal classification rule is to choose the class with the largest posterior:

$$
\hat c(x)=\arg\max_i\;P(c_i\mid x).
$$

This point is a direct bridge from Bayes theorem (Chapters 1-2) to the classification problem of Session 8.

### 2.4. Session 8 example: prior shift in fruit classification

Suppose there are 2 classes: Apple ($$c_1$$) and Orange ($$c_2$$). The same feature $$x$$ gives the likelihood ratio:

$$
\frac{P(x\mid c_1)}{P(x\mid c_2)}=2.
$$

**Context A** (a temperate-zone supermarket): $$P(c_1)=0.8,\;P(c_2)=0.2$$.

Then the posterior odds:

$$
\frac{P(c_1\mid x)}{P(c_2\mid x)}=2\times\frac{0.8}{0.2}=8.
$$

**Context B** (a tropical-zone market): $$P(c_1)=0.2,\;P(c_2)=0.8$$.

Then:

$$
\frac{P(c_1\mid x)}{P(c_2\mid x)}=2\times\frac{0.2}{0.8}=0.5.
$$

Conclusion: with the same sensor evidence $$x$$, changing the class prior can reverse the classification decision.

### 2.5. From posterior to a minimum-risk decision rule

When the costs of errors differ, a fixed threshold of 0.5 should not be used. With the action set $$a$$, choose:

$$
a^*(x)=\arg\min_a\sum_i L(a,c_i)P(c_i\mid x).
$$

#### Example: two classes, three actions (with reject)

Two true states: $$c_1, c_2$$. Three actions: choose $$c_1$$, choose $$c_2$$, or **reject** (defer to measure more).

In this illustrative example, we assume the **loss matrix** is chosen in a very simple way: a correct prediction costs 0, a wrong prediction costs 10, and the decision to **reject** costs 3 because we must measure more or wait for more information.

Suppose the posterior at a point $$x$$ is $$P(c_1\mid x)=0.55,\;P(c_2\mid x)=0.45$$.

Then:

$$
R(a=c_1\mid x)=10\cdot 0.45=4.5,
$$

$$
R(a=c_2\mid x)=10\cdot 0.55=5.5,
$$

$$
R(a=\text{reject}\mid x)=3.
$$

So the optimal action is to reject because it has the lowest expected risk. This is the standard "two-class/three-action" example of Session 8.

### 2.6. The discriminant and log-discriminant forms

In practice, we often compare the discriminants directly:

$$
g_i(x)=\log P(x\mid c_i)+\log P(c_i),
$$

and choose the class with the largest $$g_i(x)$$.

Because the log is a monotonic transformation, maximizing the posterior is equivalent to maximizing the log-discriminant, and it is also numerically more stable when probabilities are very small.

### 2.7. The Gaussian case: linear or quadratic boundary

If $$P(x\mid c_i)$$ is multivariate Gaussian, then the shape of the decision boundary depends on the covariance structure. When the classes use a **shared covariance** with $$\Sigma_i=\Sigma$$, the decision boundary is linear, close to the intuition of LDA. Conversely, when each class has its own covariance, that is $$\Sigma_i$$ differs, the decision boundary usually becomes quadratic, close to the intuition of QDA. This view is especially useful because it connects the posterior rule at the probability level with the geometry of the classification boundary in feature space.

![Logistic Function Parameters]({{ site.baseurl }}/img/chapter_img/chapter06/logistic_function_parameters.png)

This figure helps us read the logistic function more intuitively. In the left panel, the function $$p=\frac{1}{1+e^{-\eta}}$$ has the familiar S shape, passing through $$p=0.5$$ when $$\eta=0$$ and asymptotically approaching 0 and 1 at the two ends. In the middle panel, changing $$\alpha$$, the **intercept**, mainly shifts the curve to the left or right, so it can be understood as changing the baseline probability level. In the right panel, changing $$\beta$$, the **slope**, makes the curve flatter or steeper, thereby reflecting the strength of the relationship between the predictor and the probability of the outcome.

## 3. Bayesian Logistic Regression in PyMC

```python
import pymc as pm
import arviz as az

# Generate data
np.random.seed(42)
n = 200
x = np.random.uniform(-3, 3, n)
p_true = 1 / (1 + np.exp(-(1 + 0.8*x)))
y = np.random.binomial(1, p_true)

# Standardize
x_z = (x - x.mean()) / x.std()

# Bayesian logistic regression
with pm.Model() as logistic_model:
    # Priors
    alpha = pm.Normal('alpha', 0, 1.5)  # Weakly informative
    beta = pm.Normal('beta', 0, 1)
    
    # Linear predictor
    eta = alpha + beta * x_z
    
    # Logistic transformation
    p = pm.Deterministic('p', pm.math.invlogit(eta))
    
    # Likelihood
    y_obs = pm.Bernoulli('y_obs', p=p, observed=y)
    
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
                 figsize=(14, 5), ref_val=[1, 0.8])
plt.suptitle('Posterior Distributions\n(True: α=1, β=0.8)',
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

### Experiment: the logistic regression posterior is a whole family of curves

Add data points one at a time; the posterior is computed exactly on the (a, b) grid, from which we read the odds ratio exp(b) with its 95% interval.

<div class="interactive-demo" markdown="1">
<div data-demo="glm-explainer" data-lang="en" data-tab="logistic"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 4. Interpretation: Odds Ratios

### 4.1. Odds vs Probability

To interpret logistic regression correctly, we need to distinguish **probability** from **odds**. Probability is written $$p=P(y=1)$$, while odds is defined by $$\text{odds}=\frac{p}{1-p}$$. When $$p=0.5$$ the odds equal 1, meaning the two possibilities are balanced; when $$p=0.8$$ the odds equal 4, meaning the event is four times as likely to occur as not; and when $$p=0.2$$ the odds are only 0.25, meaning it is much more likely that the event does not occur.

![Odds vs Probability]({{ site.baseurl }}/img/chapter_img/chapter06/odds_probability_relationship.png)

The figure shows the relationship between probability, odds, and **log-odds** (the log of the odds). In the left panel, as the probability rises from 0.2 to 0.5 and then 0.8, the odds change nonlinearly from 0.25 to 1 and then 4. This reminds us that odds below 1 correspond to an event that is less likely to occur, while odds above 1 correspond to an event that is more likely to occur. In the right panel, when we take the log of the odds, the point $$p=0.5$$ becomes 0, probabilities below 0.5 give negative log-odds, and probabilities above 0.5 give positive log-odds. It is on this log-odds scale that logistic regression returns to the familiar linear form: $$\text{logit}(p)=\alpha+\beta x$$.

### 4.2. Interpreting β

**On log-odds scale**:
$$
\log\left(\frac{p}{1-p}\right) = \alpha + \beta x
$$

Therefore, on the log-odds scale, each time $$x$$ increases by 1 unit, the log-odds increases by $$\beta$$ units.

**On odds scale**:
$$
\text{odds} = e^{\alpha + \beta x}
$$

Going back to the odds scale, we see that each time $$x$$ increases by 1 unit, the odds are multiplied by $$e^\beta$$. This is the **odds ratio**, and it is also the most practical way to interpret the coefficient of logistic regression.

### 4.3. A concrete example: from log-odds to predicted probability

Suppose the posterior mean of the model gives us the equation:

$$
\log\left(\frac{p}{1-p}\right) = -0.4 + 1.1x
$$

where $$x$$ is a standardized rating score. We can read the model step by step:

- If $$x=0$$ then the log-odds equals $$-0.4$$, so the odds are $$e^{-0.4}\approx 0.67$$, and the probability is $$p=\frac{0.67}{1+0.67}\approx 0.40$$.
- If $$x=1$$ then the log-odds equals $$0.7$$, so the odds are $$e^{0.7}\approx 2.01$$, and the probability rises to about $$0.67$$.
- If $$x=2$$ then the log-odds equals $$1.8$$, so the odds are $$e^{1.8}\approx 6.05$$, and the probability rises to about $$0.86$$.

A very commonly misread point is that the coefficient $$\beta=1.1$$ does not mean that the probability rises by a fixed 1.1 units or by 110 percentage points. The correct meaning is: each time $$x$$ increases by 1 unit, the **odds** are multiplied by $$e^{1.1}\approx 3$$. Because logistic regression is linear on the log-odds scale but nonlinear on the probability scale, the same 1-unit increase in $$x$$ can make the probability jump by different amounts depending on the starting point: from $$0.40$$ to $$0.67$$ is an increase of about 27 percentage points, while from $$0.67$$ to $$0.86$$ is an increase of about 19 percentage points.

```python
# Compute odds ratios
beta_samples = trace.posterior['beta'].values.flatten()
odds_ratio = np.exp(beta_samples)

print("\n" + "=" * 70)
print("ODDS RATIO INTERPRETATION")
print("=" * 70)
print(f"\nβ (log-odds scale): {beta_samples.mean():.3f}")
print(f"Odds Ratio (e^β): {odds_ratio.mean():.3f}")
print(f"95% CI: [{np.percentile(odds_ratio, 2.5):.3f}, " +
      f"{np.percentile(odds_ratio, 97.5):.3f}]")

print("\nInterpretation:")
print(f"  1 SD increase in x → odds multiply by {odds_ratio.mean():.2f}")
if odds_ratio.mean() > 1:
    print(f"  → {(odds_ratio.mean()-1)*100:.1f}% increase in odds")
else:
    print(f"  → {(1-odds_ratio.mean())*100:.1f}% decrease in odds")
print("=" * 70)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Beta (log-odds scale)
axes[0].hist(beta_samples, bins=50, density=True, alpha=0.7,
            color='skyblue', edgecolor='black')
axes[0].axvline(beta_samples.mean(), color='red', linewidth=3,
               label=f'Mean = {beta_samples.mean():.3f}')
axes[0].axvline(0, color='black', linestyle='--', linewidth=2)
axes[0].set_xlabel('β (log-odds scale)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0].set_title('COEFFICIENT β\n(Log-Odds Scale)',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3, axis='y')

# Odds ratio
axes[1].hist(odds_ratio, bins=50, density=True, alpha=0.7,
            color='lightgreen', edgecolor='black')
axes[1].axvline(odds_ratio.mean(), color='red', linewidth=3,
               label=f'Mean = {odds_ratio.mean():.3f}')
axes[1].axvline(1, color='black', linestyle='--', linewidth=2)
axes[1].set_xlabel('Odds Ratio (e^β)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1].set_title('ODDS RATIO\n(Multiplicative Effect)',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

## 5. Posterior Predictive Checks

```python
# Posterior predictive
with logistic_model:
    ppc = pm.sample_posterior_predictive(trace, random_seed=42)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Predicted probabilities
p_samples = trace.posterior['p'].values.reshape(-1, n)
p_mean = p_samples.mean(axis=0)
p_lower = np.percentile(p_samples, 2.5, axis=0)
p_upper = np.percentile(p_samples, 97.5, axis=0)

# Sort by x for plotting
sort_idx = np.argsort(x)
axes[0].scatter(x, y, alpha=0.3, s=30, label='Observed', edgecolors='black')
axes[0].plot(x[sort_idx], p_mean[sort_idx], 'r-', linewidth=3, label='Posterior mean')
axes[0].fill_between(x[sort_idx], p_lower[sort_idx], p_upper[sort_idx],
                     alpha=0.3, color='red', label='95% CI')
axes[0].set_xlabel('x', fontsize=12, fontweight='bold')
axes[0].set_ylabel('P(y=1)', fontsize=12, fontweight='bold')
axes[0].set_title('PREDICTED PROBABILITIES\nwith Uncertainty',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# PPC: Compare observed vs predicted
y_pred = ppc.posterior_predictive['y_obs'].values.reshape(-1, n)
y_pred_mean = y_pred.mean(axis=0)

axes[1].scatter(y, y_pred_mean, alpha=0.5, s=50, edgecolors='black')
axes[1].plot([0, 1], [0, 1], 'r--', linewidth=2, label='Perfect prediction')
axes[1].set_xlabel('Observed y', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Predicted P(y=1)', fontsize=12, fontweight='bold')
axes[1].set_title('POSTERIOR PREDICTIVE CHECK\nObserved vs Predicted',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## Summary

Logistic regression is the natural answer when the outcome has only two states. The problem it solves is that linear regression cannot guarantee predictions lying in $$[0,1]$$, and its solution is to use the **logit link** to connect an inner linear structure with a valid probability at the output. The core model has the form $$\log\left(\frac{p}{1-p}\right)=\alpha+\beta x$$, and the coefficient should be read through the **odds ratio** $$e^\beta$$ rather than with the intuition of “how many units $$y$$ increases” as in linear regression. In PyMC, this is implemented very directly with the `pm.Bernoulli` distribution combined with `pm.math.invlogit`.

The most important point to keep is the GLM way of thinking: we still start with a linear part, but use an appropriate link function to handle outcomes that no longer follow the familiar Gaussian model.

Next lesson: **Poisson Regression** for count data.

## Reference videos

- [StatQuest: Logistic Regression](https://www.youtube.com/watch?v=yIYKR4sgzI8) — StatQuest with Josh Starmer, English. **watch first**. Watch logistic regression predict the probability of a binary outcome, exactly the 0/1 output variable of the lesson.
- [Odds and Log(Odds), Clearly Explained!!!](https://www.youtube.com/watch?v=ARfXDSkQf1Y) — StatQuest with Josh Starmer, English. Watch odds and log-odds, supporting the part on reading coefficients on the logit scale rather than the probability scale.
- [Statistical Rethinking 2023 - 04 - Categories & Curves](https://www.youtube.com/watch?v=F0N4b7K_iYQ) — Richard McElreath, English. Watch the logistic curve placed inside a Bayesian model, connecting the lesson's formula with the generative story.

## Exercises

**Exercise 1**: Generate binary data. Fit logistic regression. Interpret odds ratio.

**Exercise 2**: Compare predictions of linear vs logistic regression. Visualize differences.

**Exercise 3**: Multiple predictors logistic regression. Interpret each coefficient.

**Exercise 4**: Real data - predict customer churn (0/1) from usage features.

**Exercise 5**: Posterior predictive checks. Compare accuracy, sensitivity, specificity.

## References

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.
- Chapter 5: Logistic regression

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 10: Big Entropy and the Generalized Linear Model

---

*Next lesson: [6.2 Poisson Regression]({{ site.baseurl }}/contents/en/chapter06/06_02_poisson_regression/)*
