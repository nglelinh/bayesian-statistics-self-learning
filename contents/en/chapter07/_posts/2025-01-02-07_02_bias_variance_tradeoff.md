---
layout: post
title: "Lesson 7.2: Bias-Variance Tradeoff - The Core of Model Selection"
chapter: '07'
order: 2
owner: Nguyen Le Linh
lang: en
categories:
- chapter07
lesson_type: required
---

Give a polynomial regression enough flexibility (degree 9 on 10 data points), and it will wiggle cleanly through **every single training point** with 0.00 training error—yet predict catastrophic nonsense one millimeter outside the training points! That classic tension between **underfitting** (too rigid, high bias) and **overfitting** (memorizing noise, high variance) is the **Bias–Variance Trade-off**—the compass of all model selection.

This lesson reframes the Bias–Variance Trade-off in Bayesian terms: showing how **regularizing priors** and **posterior averaging** tame variance automatically, and why **out-of-sample predictive accuracy** is the only honest judge of model complexity.

---

## Background Knowledge Map: Complexity, Generalization, and Bayesian Averaging

1. **Underfitting (High Bias) vs. Overfitting (High Variance):** Too few parameters miss real curvature (both train and test error stay high); too many unregularized parameters chase random sample noise (train error $$\to 0$$, test error explodes!).
2. **In-Sample Deviance Always Improves With Complexity:** Adding any extra parameter never worsens training fit—which is why comparing models on training $$R^2$$ or training log-likelihood guarantees overfitting!
3. **Regularizing Priors Shift the Sweet Spot:** Tightening the prior on higher-order terms adds tiny bias while slashing variance dramatically, letting richer models generalize cleanly.
4. **Posterior Averaging Reduces Variance Further:** Integrating predictions over all posterior draws $$\theta^{(s)}$$ (instead of plugging in one MLE/MAP point!) acts like an automatic ensemble, softening overconfident out-of-sample predictions.

---

## Learning objectives

After completing this lesson, you will have a deep understanding of the **bias-variance tradeoff**, one of the most fundamental ideas in machine learning and statistics. The lesson explains why a model that is too simple usually has **high bias**, why a model that is too complex usually has **high variance**, and why the real goal of model selection is not to push one component as low as possible, but to find the balance point that makes the overall error smallest. This is the direct basis for understanding regularization, overfitting, and even the logic of choosing models.

## Introduction: Two Kinds of Error

When a model predicts wrongly, the error usually does not come from a single cause. Part of the error may come from the model being too simple and therefore missing the true structure of the data; that is **bias**. Another part may come from the model being too sensitive to the training data, so that changing the sample slightly makes the predictions fluctuate strongly; that is **variance**. The core point is that these two components usually pull in opposite directions: reducing bias usually increases variance, while pushing variance down too hard usually increases bias.

## 1. Bias and Variance: Definitions

### 1.1. Mathematical Definitions

Suppose we train the model many times on different datasets from the same distribution.

**Bias**: The deviation between the **average prediction** and the **true value**
$$
\text{Bias}[\hat{f}(x)] = \mathbb{E}[\hat{f}(x)] - f(x)
$$

**Variance**: Variability of predictions across datasets
$$
\text{Variance}[\hat{f}(x)] = \mathbb{E}[(\hat{f}(x) - \mathbb{E}[\hat{f}(x)])^2]
$$

**Total Error**:
$$
\mathbb{E}[(y - \hat{f}(x))^2] = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}
$$

### 1.2. Intuitive Understanding

![Bias-Variance Demonstration]({{ site.baseurl }}/img/chapter_img/chapter07/bias_variance_demonstration.png)

The figure illustrates this intuition very clearly. With a degree-1 model, the fitted lines from many different datasets are fairly close to each other, meaning low variance, but most of them are far off the true pattern, meaning high bias; this is the typical underfitting state. With a degree-3 model, the flexibility is just enough to follow the true pattern more closely without fluctuating too much between samples, so bias decreases while variance is still under control; that is the best balance region of the trade-off. With a degree-10 model, the average curve may already be closer to the true pattern, meaning lower bias, but each individual model fluctuates strongly from one training sample to the next, meaning variance shoots up. Therefore, looking at 50 different training sets as 50 different versions of the same problem is the most intuitive way to understand variance: it measures how much the predictions “shake” when the data changes.

## 2. Decomposition: MSE = Bias² + Variance + Noise

![MSE Decomposition]({{ site.baseurl }}/img/chapter_img/chapter07/mse_decomposition.png)

Looking at the decomposition of the MSE, we see immediately why model choice cannot rest on a single criterion. In the low-complexity region, for example degree 1 or 2, the $$\text{Bias}^2$$ component is still large because the model is too simple to describe the data, even though the variance is fairly low then. As complexity increases into the intermediate region, the two components begin to balance better and the total MSE reaches its minimum; that is the true “sweet spot” of the model. But as complexity keeps increasing, bias may decrease a little more while variance rises very sharply, making the MSE rise again. The stacked chart on the right is especially useful because it shows visually that the goal is not to minimize bias alone or variance alone, but to minimize the total prediction error.

### Experiment: bias, variance and total error by complexity

Repeat 100 datasets for each polynomial degree; bias² falls, variance rises, the total error is U-shaped; a tight prior (ridge) compresses the variance.

<div class="interactive-demo" markdown="1">
<div data-demo="biasvar-explainer" data-lang="en"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 3. Regularization and Bias-Variance

Regularization is precisely the knob that controls this trade-off. When regularization is weak, that is $$\lambda$$ is small, the model is allowed to be more flexible, so bias tends to be low but variance is high. When regularization is strong, that is $$\lambda$$ is large, the model is forced to be simpler, so variance decreases, but bias increases.

![Regularization Bias-Variance]({{ site.baseurl }}/img/chapter_img/chapter07/regularization_bias_variance.png)

The example with a degree-10 polynomial shows this point very clearly. When $$\lambda=0.001$$, regularization is too weak so the model fluctuates strongly, shown by a very large variance and clear overfitting. As it increases gradually to $$0.1$$ and then $$1$$, variance drops considerably and the model enters a better balance region. If it keeps increasing to $$10$$ or $$100$$, the model starts to be constrained too strongly, the predictions become almost flat, variance is low but bias is high, meaning a return to the underfitting region. The lesson here is that $$\lambda$$ is not a parameter where “bigger is safer”; it must be chosen so that bias and variance reach the best balance for the prediction goal.

## 4. Bayesian Perspective

In Bayesian statistics, the role of regularization is translated into the role of **prior strength**. Weak priors let the data decide more, so the model is more flexible but also fluctuates more; strong priors constrain the model more, so variance decreases, but in return bias may increase if the prior is too rigid.

```python
import pymc as pm
import arviz as az

# Generate data
np.random.seed(42)
n = 30
x_data = np.random.uniform(0, 10, n)
y_data = true_function(x_data) + np.random.normal(0, 1, n)

x_data_z = (x_data - x_data.mean()) / x_data.std()
y_data_z = (y_data - y_data.mean()) / y_data.std()

# Different prior strengths
prior_sds = [0.1, 0.5, 2, 10]

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.ravel()

for idx, prior_sd in enumerate(prior_sds):
    with pm.Model() as model:
        alpha = pm.Normal('alpha', 0, 1)
        beta = pm.Normal('beta', 0, prior_sd)  # Varying prior strength
        sigma = pm.HalfNormal('sigma', 1)
        
        mu = alpha + beta * x_data_z
        y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_data_z)
        
        trace = pm.sample(500, tune=200, chains=2, random_seed=42,
                         return_inferencedata=True, progressbar=False)
    
    # Posterior predictions
    alpha_samples = trace.posterior['alpha'].values.flatten()
    beta_samples = trace.posterior['beta'].values.flatten()
    
    # Plot
    x_plot_z = (x_test - x_data.mean()) / x_data.std()
    for i in range(min(100, len(alpha_samples))):
        y_plot_z = alpha_samples[i] + beta_samples[i] * x_plot_z
        y_plot = y_plot_z * y_data.std() + y_data.mean()
        axes[idx].plot(x_test, y_plot, '-', alpha=0.05, color='orange')
    
    axes[idx].scatter(x_data, y_data, s=60, alpha=0.7, edgecolors='black',
                     label='Data', zorder=5)
    axes[idx].plot(x_test, y_true, 'b-', linewidth=3, label='True', zorder=4)
    axes[idx].set_xlabel('x', fontsize=11, fontweight='bold')
    axes[idx].set_ylabel('y', fontsize=11, fontweight='bold')
    
    if prior_sd < 1:
        title_color = 'red'
        subtitle = '(High Bias)'
    elif prior_sd > 5:
        title_color = 'orange'
        subtitle = '(High Variance)'
    else:
        title_color = 'green'
        subtitle = '(Balanced)'
    
    axes[idx].set_title(f'Prior SD = {prior_sd} {subtitle}',
                       fontsize=13, fontweight='bold', color=title_color)
    axes[idx].legend(fontsize=10)
    axes[idx].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## 5. Validation Strategy and Learning Curves in Practice

The bias-variance tradeoff becomes a decision-making tool only when we measure it on out-of-sample data.

- **Train score** helps monitor the ability to learn from data already seen.
- **Validation score** tells the degree of generalization, for tuning complexity/prior scale.
- **Test score** is the final report, used only once after the model choice has been locked.

A quick way to read learning curves:

1. Good train, poor validation and a large gap -> **high variance** (needs stronger regularization or more data).
2. Poor train and validation both -> **high bias** (needs a more flexible model, add reasonable features).
3. Validation stable around the best point as regularization increases -> this is the appropriate balance region.

## 6. Applied Case Study (Part 2): tune complexity with validation

Continuing the data setup from Lesson 7.1, we use closed-form ridge to sweep regularization strengths and choose the bias-variance balance using validation RMSE.

```python
import numpy as np

def ridge_fit(X, y, lam):
    p = X.shape[1]
    eye = np.eye(p)
    return np.linalg.solve(X.T @ X + lam * eye, X.T @ y)

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

lambdas = np.logspace(-3, 2, 30)
val_scores = []
train_scores = []
coefs = []

for lam in lambdas:
    beta_hat = ridge_fit(X_train_z, y_train_z, lam)
    coefs.append(beta_hat)
    train_scores.append(rmse(y_train_z, X_train_z @ beta_hat))
    val_scores.append(rmse(y_val_z, X_val_z @ beta_hat))

best_idx = int(np.argmin(val_scores))
best_lambda = float(lambdas[best_idx])
best_beta = coefs[best_idx]

test_rmse = rmse(y_test_z, X_test_z @ best_beta)

print(f"Best lambda (validation): {best_lambda:.4f}")
print(f"Train RMSE (z-scale): {train_scores[best_idx]:.3f}")
print(f"Validation RMSE (z-scale): {val_scores[best_idx]:.3f}")
print(f"Test RMSE (z-scale): {test_rmse:.3f}")
```

![Applied ML Workflow Tradeoffs]({{ site.baseurl }}/img/chapter_img/chapter07/applied_ml_workflow_tradeoffs.png)

The figure above summarizes three main decisions in the applied workflow: (1) choose regularization by validation RMSE, (2) check the size of the coefficients after shrinkage, and (3) assess the stability of variable selection through bootstrap frequencies.

**Decision checkpoint 2**:
- If you optimize only the train RMSE, the result usually pushes the model into the overfit region.
- If you optimize the validation RMSE and keep the test for the final step, you have a trustworthy basis for assessing generalization.

## 7. Tuning checklist: from tradeoff to action

When choosing model complexity in regression/classification problems:

1. Choose a metric appropriate to the business/problem goal (do not use a metric just to go through the motions).
2. Use a reasonable grid for regularization/prior scale instead of sweeping too wide.
3. Track both the train-validation gap and the stability across folds.
4. Combine out-of-sample performance with posterior predictive checks to detect model misspecification.
5. Settle on a model with reasons that can be explained (not just "the highest score").

## Summary

The bias-variance tradeoff shows that prediction error cannot be understood by a single simple measure of “fit”. **Bias** reflects the price of using a model that is too simple, while **variance** reflects the price of using a model that is too sensitive to the training data. The formula $$\text{MSE}=\text{Bias}^2+\text{Variance}+\text{Irreducible Error}$$ reminds us that a good model is one that balances these two opposing forces. Regularization is the practical tool for adjusting that balance point, and in Bayesian statistics, the strength of the prior plays exactly that role.

The point to remember most is that a model that fits the training data beautifully is not necessarily a good model; a good model is one that generalizes well to new data.

Next lesson: **Feature Selection** (completing the case study with stability selection and uncertainty-aware interpretation).

---

### Worked Numerical Example: Watching Train vs. Test Deviance Diverge Across Polynomial Degrees

Fit polynomial models of degree 1, 2, 5, and 9 (with flat priors) to $$n = 15$$ noisy points from a true quadratic curve:

| Model Complexity | Parameters $$p$$ | In-Sample Train Deviance | Out-of-Sample Test Deviance | Diagnosis |
| :--- | :--- | :--- | :--- | :--- |
| **Degree 1 (Line)** | $$2$$ | $$24.5$$ | $$26.1$$ | **Underfit** (high bias — misses curve) |
| **Degree 2 (Quadratic)** | $$3$$ | $$8.4$$ | **$$9.6$$** | **Sweet spot!** (lowest test error) |
| **Degree 5** | $$6$$ | $$6.1$$ | $$15.8$$ | Starting to chase sample noise |
| **Degree 9 (Flat Prior)** | $$10$$ | **$$1.2$$** | **$$64.0$$** | **Severe Overfit!** (huge variance!) |
| **Degree 9 ($$\mathcal{N}(0, 0.3)$$ Prior)** | $$10$$ | $$8.9$$ | **$$10.2$$** | **Regularizing prior rescues generalization!** |

Look at the bottom two rows: the exact same 10-parameter architecture drops out-of-sample deviance from **64.0 down to 10.2** simply by adding a skeptical Bayesian prior!

### Deep-Dive Explanation: Four Rules for Navigating the Bias–Variance Trade-Off (Read Slowly)

1. **Never pick a model by training fit alone:** Always evaluate via cross-validation (LOO-CV / k-fold) or a locked held-out test set.
2. **Plot the *gap* between train and test deviance:** A tiny train error paired with a huge test error is the unmistakable fingerprint of overfitting; both high signals underfitting.
3. **Prefer regularizing priors over crude manual dropping of variables:** Smoothly shrinking weak effects toward zero avoids the abrupt variance spikes of all-or-nothing variable deletion.
4. **More data cures variance, not structural bias:** Collecting 10× more samples won’t make a straight line fit a parabola—you must fix underfitting by enriching the model family!

**Quick check.** In the polynomial table above, why did adding a $$\mathcal{N}(0, 0.3)$$ prior to the Degree-9 model make its *in-sample training deviance* slightly worse (`1.2` $$\to$$ `8.9`) while cutting its *out-of-sample test deviance* by more than 6× (`64.0` $$\to$$ `10.2`)?

---

## Reference videos

- [Machine Learning Fundamentals: Bias and Variance](https://www.youtube.com/watch?v=EuBBz3bI-aA) — StatQuest with Josh Starmer, English. **watch first**. Watch a model that is too simple being systematically off and a model that is too flexible fluctuating with the sample, exactly the two kinds of error in the lesson.
- [[Proof] MSE = Variance + Bias²](https://www.youtube.com/watch?v=qmVT35gFW-Q) — math et al, English. Watch the identity MSE equals squared bias plus variance, supporting the error decomposition part.
- [Machine Learning Fundamentals: Cross Validation](https://www.youtube.com/watch?v=fSytzGwwBVw) — StatQuest with Josh Starmer, English. Watch cross-validation as a way of looking at out-of-sample error, used for the learning curve and choosing complexity sections.

## Exercises

**Exercise 1**: Implement bias-variance decomposition from scratch. Verify MSE = Bias² + Variance.

**Exercise 2**: Generate data. Compute bias-variance for models with different complexities. Find optimal.

**Exercise 3**: Use Ridge with different λ. Plot bias-variance curve. Find optimal λ.

**Exercise 4**: Bayesian models with different prior SDs. Compute posterior variance. Relate to bias-variance.

**Exercise 5**: Real data. Split train/test. Show overfitting with high-degree polynomial. Fix with regularization.

## References

**Hastie, T., Tibshirani, R., & Friedman, J. (2009).** *The Elements of Statistical Learning* (2nd Edition). Springer.
- Chapter 7: Model Assessment and Selection

**James, G., et al. (2013).** *An Introduction to Statistical Learning*. Springer.
- Chapter 2: Statistical Learning

---

*Next lesson: [7.3 Feature Selection]({{ site.baseurl }}/contents/en/chapter07/07_03_feature_selection/)*
