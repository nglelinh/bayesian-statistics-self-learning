---
layout: post
title: "Lesson 6.3: Model Evaluation for GLMs"
chapter: '06'
order: 3
owner: Nguyen Le Linh
lang: en
categories:
- chapter06
lesson_type: required
---

Once you step outside Normal linear regression into Logistic or Poisson GLMs, familiar metrics like ordinary $$R^2$$ and raw residual plots stop working—binary outcomes only ever equal `0` or `1`, so `y - p` is never bell-shaped! Evaluating a Bayesian GLM honestly requires **proper probabilistic scoring rules** (Log-Loss / Deviance, Brier score), **calibration curves**, **binned/randomized quantile residuals**, and **Posterior Predictive Checks**!

This lesson builds a complete GLM diagnostic workflow so you know when a classifier is well-calibrated versus overconfident, and when a count model is missing overdispersion.

---

## Background Knowledge Map: Four Diagnostic Tools for Bayesian GLMs

1. **Log-Pointwise Predictive Score & Deviance ($$D = -2\sum \log p(y_i\mid\hat{\theta})$$):** Generalizes RSS to *any* likelihood family (Bernoulli, Poisson, Negative Binomial)—strictly proper and directly connects to WAIC/LOO!
2. **Calibration vs. Discrimination (ROC-AUC vs. Calibration Plot):** ROC-AUC measures *ranking* (does a true 1 score higher than a true 0?); **calibration** measures whether predicted 70% probabilities actually happen 70% of the time!
3. **Binned & Pearson Residuals:** For binary GLMs, raw residuals $$y_i - p_i$$ lie on two curved stripes; grouping observations into bins of predicted $$p_i$$ reveals hidden nonlinearity immediately.
4. **GLM Posterior Predictive Checks:** Simulate $$y^{\text{rep}} \sim \mathrm{Bernoulli}(p^{(s)})$$ or $$\mathrm{Poisson}(\lambda^{(s)})$$ and check group calibration, max counts, variance/mean ratio, and zero proportions.

---

## Learning objectives

After completing this lesson, you will understand how to evaluate **GLM models** such as logistic regression and Poisson regression in real-world settings. The focus of the lesson is learning to choose the right evaluation criteria for the right type of outcome, from **classification metrics** such as accuracy, sensitivity, specificity, and ROC curves, to the **calibration plot**, **deviance**, and **posterior predictive checks**. This is a very important step, because a model has real value only when we clearly understand what it does well, what it does not yet do well, and what deviations remain.

## Introduction: How Evaluating GLMs Differs from Linear Regression

With linear regression, we are usually used to metrics such as $$R^2$$, RMSE, or residual plots to see how well the model fits the data. However, when we move to GLMs, the evaluation criteria must change with the nature of the outcome. For **binary outcomes**, we care about the ability to discriminate between classes and the calibration of probabilities, so we commonly use accuracy, ROC, or calibration. For **count outcomes**, we must check how well the distribution fits, the deviance, and signs of **overdispersion**. Even so, there is one principle common to every GLM: we always need to use **posterior predictive checks** to compare the data the model generates with the real data.

## 1. Evaluating Logistic Regression

![Model Evaluation for GLM]({{ site.baseurl }}/img/chapter_img/chapter06/model_evaluation_glm.png)

### 1.1. Confusion Matrix

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
from sklearn.metrics import confusion_matrix, roc_curve, auc

# Generate binary data
np.random.seed(42)
n = 200
x = np.random.uniform(-3, 3, n)
p_true = 1 / (1 + np.exp(-(1 + 0.8*x)))
y = np.random.binomial(1, p_true)

# Fit logistic model
x_z = (x - x.mean()) / x.std()

with pm.Model() as logistic_model:
    alpha = pm.Normal('alpha', 0, 1.5)
    beta = pm.Normal('beta', 0, 1)
    eta = alpha + beta * x_z
    p = pm.Deterministic('p', pm.math.invlogit(eta))
    y_obs = pm.Bernoulli('y_obs', p=p, observed=y)
    trace = pm.sample(1000, tune=500, chains=2, random_seed=42,
                     return_inferencedata=True, progressbar=False)

# Posterior predictions
p_samples = trace.posterior['p'].values.reshape(-1, n)
p_mean = p_samples.mean(axis=0)

# Confusion matrices with different thresholds
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

thresholds = [0.3, 0.5, 0.7]
for idx, thresh in enumerate(thresholds):
    # Predict
    y_pred = (p_mean >= thresh).astype(int)
    
    # Confusion matrix
    cm = confusion_matrix(y, y_pred)
    
    # Visualize
    im = axes[0, idx].imshow(cm, cmap='Blues', vmin=0, vmax=max(cm.flatten()))
    axes[0, idx].set_xticks([0, 1])
    axes[0, idx].set_yticks([0, 1])
    axes[0, idx].set_xticklabels(['Pred 0', 'Pred 1'], fontsize=11)
    axes[0, idx].set_yticklabels(['True 0', 'True 1'], fontsize=11)
    axes[0, idx].set_title(f'Threshold = {thresh}\nConfusion Matrix',
                          fontsize=13, fontweight='bold')
    
    # Add text
    for i in range(2):
        for j in range(2):
            axes[0, idx].text(j, i, str(cm[i, j]), ha='center', va='center',
                            fontsize=20, fontweight='bold',
                            color='white' if cm[i, j] > cm.max()/2 else 'black')
    
    # Compute metrics
    tn, fp, fn, tp = cm.ravel()
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0  # Recall, TPR
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0  # TNR
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    
    # Metrics text
    metrics_text = f"""
    Accuracy: {accuracy:.3f}
    Sensitivity: {sensitivity:.3f}
    Specificity: {specificity:.3f}
    Precision: {precision:.3f}
    """
    axes[1, idx].axis('off')
    axes[1, idx].text(0.5, 0.5, metrics_text, ha='center', va='center',
                     fontsize=12, family='monospace',
                     bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

plt.tight_layout()
plt.show()

print("=" * 70)
print("CLASSIFICATION METRICS")
print("=" * 70)
print("\nConfusion Matrix Components:")
print("  TN (True Negative): Correctly predicted 0")
print("  FP (False Positive): Incorrectly predicted 1 (Type I error)")
print("  FN (False Negative): Incorrectly predicted 0 (Type II error)")
print("  TP (True Positive): Correctly predicted 1")
print("\nMetrics:")
print("  Accuracy = (TP + TN) / Total")
print("  Sensitivity (Recall) = TP / (TP + FN)")
print("  Specificity = TN / (TN + FP)")
print("  Precision = TP / (TP + FP)")
print("=" * 70)
```

### 1.1.1. Evaluating by decision rule instead of only by the 0.5 threshold

In Bayesian classification, the 0.5 threshold is reasonable only when the costs of the two kinds of error are nearly symmetric. If the costs differ, we should choose the threshold according to the expected risk.

Example with two classes (positive/negative):

We denote the cost of a **false positive** as $$C_{FP}$$ and the cost of a **false negative** as $$C_{FN}$$.

The optimal rule (without reject) is to predict positive when:

$$
P(y=1\mid x) > \frac{C_{FP}}{C_{FP}+C_{FN}}.
$$

If we add a reject action with cost $$C_R$$, we classify only when the risk of the decision is less than $$C_R$$.

An important practical point is that the confusion matrix should not be presented as a context-neutral table of counts. A threshold only has meaning when tied to the cost of each kind of mistake, because in many applied problems, a false negative can be far more serious than a false positive, or vice versa.

### 1.1.2. A concrete example: the 0.5 threshold can make us miss important cases

Suppose this is a rare-disease screening problem, in which missing a case is about 9 times worse than a false alarm. Then:

$$
\text{optimal threshold}=\frac{C_{FP}}{C_{FP}+C_{FN}}=\frac{1}{1+9}=0.1
$$

This means that as soon as $$P(y=1\mid x)>0.1$$, we should lean toward the decision "send for further testing". If the model returns three probabilities $$0.18$$, $$0.32$$ and $$0.65$$ for three patients, then all three should be placed in the group needing further follow-up. If we mechanically keep the 0.5 threshold, the first two would be classified as negative even though the risk of missing them is very large. This example shows that logistic regression is not only about predicting labels, but also about using the posterior probability in line with the decision costs of the problem.

### 1.1.3. The Bayes factor as a measure of evidence at the model level

Besides label-based classification metrics, we can compare the evidence between two models/hypotheses with the Bayes factor:

$$
BF_{10}=\frac{p(D\mid M_1)}{p(D\mid M_0)}.
$$

When $$BF_{10}>1$$, the data supports $$M_1$$ more than $$M_0$$; when $$BF_{10}<1$$, the evidence leans toward $$M_0$$. Bayes factor therefore complements ROC/AUC in a very different way: ROC speaks about the ability to discriminate labels, while the Bayes factor speaks about the level of relative evidence for a model or hypothesis.

### 1.2. ROC Curve

The **ROC curve** is a plot of **Sensitivity** against $$1-\text{Specificity}$$ as we sweep through every possible classification threshold. Instead of settling early on a specific threshold, the ROC gives us a global view of the tradeoff between catching true positive cases and avoiding false alarms. The **AUC** (Area Under the Curve) is a summary of that entire curve; a value near 0.5 suggests the model is nearly random, while a value approaching 1 shows very strong discriminating ability.

```python
# Compute ROC curve
fpr, tpr, thresholds_roc = roc_curve(y, p_mean)
roc_auc = auc(fpr, tpr)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# ROC curve
axes[0].plot(fpr, tpr, 'b-', linewidth=3, label=f'ROC (AUC = {roc_auc:.3f})')
axes[0].plot([0, 1], [0, 1], 'r--', linewidth=2, label='Random (AUC = 0.5)')
axes[0].fill_between(fpr, tpr, alpha=0.3, color='blue')
axes[0].set_xlabel('False Positive Rate (1 - Specificity)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('True Positive Rate (Sensitivity)', fontsize=12, fontweight='bold')
axes[0].set_title('ROC CURVE\nHigher AUC = Better Model',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11, loc='lower right')
axes[0].grid(alpha=0.3)

# Threshold selection
axes[1].plot(thresholds_roc, tpr, 'b-', linewidth=2, label='Sensitivity (TPR)')
axes[1].plot(thresholds_roc, 1-fpr, 'r-', linewidth=2, label='Specificity (TNR)')
axes[1].axvline(0.5, color='green', linestyle='--', linewidth=2, alpha=0.7)
axes[1].set_xlabel('Threshold', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Rate', fontsize=12, fontweight='bold')
axes[1].set_title('THRESHOLD SELECTION\nTrade-off between Sensitivity & Specificity',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("ROC CURVE INTERPRETATION")
print("=" * 70)
print(f"\nAUC = {roc_auc:.3f}")
if roc_auc > 0.9:
    print("  → Excellent discrimination")
elif roc_auc > 0.8:
    print("  → Good discrimination")
elif roc_auc > 0.7:
    print("  → Acceptable discrimination")
else:
    print("  → Poor discrimination")
print("=" * 70)
```

### 1.3. Calibration Plot

**Calibration** answers a different question from the ROC: when the model says the probability is 0.7, do about 70% of such cases really occur in practice? A model can discriminate classes quite well and still be poorly calibrated, meaning the probabilities it reports are too optimistic or too cautious. The calibration plot therefore helps us assess the quality of the predicted probabilities themselves, not only the quality of the final classification decision.

### 1.3.1. A concrete example: a good AUC but still skewed probabilities

Imagine a model that predicts for 10 patients with probabilities around $$0.8$$, but in the end only 5 are truly positive. The model can still have a fairly good ROC/AUC if the 5 patients with the disease receive higher probabilities than most of those without it. However, in terms of calibration the model is overconfident: it says "80%" but in reality it happens only about "50%" of the time.

Similarly, if another group is predicted around $$0.2$$ but in reality as many as $$0.35$$ of the cases occur, the model is underestimating the risk. The core point is that ROC answers the question "does the model rank higher-risk people correctly?", while calibration answers the question "is the probability number the model gives trustworthy as a real probability?".

```python
# Calibration plot
n_bins = 10
bins = np.linspace(0, 1, n_bins + 1)
bin_centers = (bins[:-1] + bins[1:]) / 2

observed_freq = []
predicted_prob = []

for i in range(n_bins):
    mask = (p_mean >= bins[i]) & (p_mean < bins[i+1])
    if mask.sum() > 0:
        observed_freq.append(y[mask].mean())
        predicted_prob.append(p_mean[mask].mean())

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Calibration plot
axes[0].scatter(predicted_prob, observed_freq, s=150, alpha=0.7,
               edgecolors='black', label='Binned data')
axes[0].plot([0, 1], [0, 1], 'r--', linewidth=2, label='Perfect calibration')
axes[0].set_xlabel('Predicted Probability', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Observed Frequency', fontsize=12, fontweight='bold')
axes[0].set_title('CALIBRATION PLOT\nDo predictions match reality?',
                 fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)
axes[0].set_xlim(0, 1)
axes[0].set_ylim(0, 1)

# Histogram of predicted probabilities
axes[1].hist(p_mean, bins=30, alpha=0.7, edgecolor='black')
axes[1].set_xlabel('Predicted Probability', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Frequency', fontsize=12, fontweight='bold')
axes[1].set_title('DISTRIBUTION OF PREDICTIONS\nWell-spread or concentrated?',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

## 2. Evaluating Poisson Regression

### 2.1. Deviance

**Deviance** is a measure of model fit within the GLM family, and intuitively it can be understood as the distance between the model under consideration and a saturated model that can fit the data perfectly. The smaller the deviance, the closer the model is to that ideal fit.

$$
D = -2 \log \frac{L(\text{model})}{L(\text{saturated})}
$$

```python
# Generate count data
np.random.seed(42)
n = 150
x_count = np.random.uniform(0, 5, n)
lambda_true = np.exp(0.5 + 0.4*x_count)
y_count = np.random.poisson(lambda_true)

# Fit Poisson model
x_count_z = (x_count - x_count.mean()) / x_count.std()

with pm.Model() as poisson_model:
    alpha = pm.Normal('alpha', 2, 1)
    beta = pm.Normal('beta', 0, 1)
    eta = alpha + beta * x_count_z
    lambda_ = pm.Deterministic('lambda', pm.math.exp(eta))
    y_obs = pm.Poisson('y_obs', mu=lambda_, observed=y_count)
    trace_poisson = pm.sample(1000, tune=500, chains=2, random_seed=42,
                             return_inferencedata=True, progressbar=False)

# Posterior predictions
lambda_samples = trace_poisson.posterior['lambda'].values.reshape(-1, n)
lambda_mean = lambda_samples.mean(axis=0)

# Compute deviance
from scipy.stats import poisson as poisson_dist

log_lik_model = poisson_dist.logpmf(y_count, lambda_mean).sum()
log_lik_saturated = poisson_dist.logpmf(y_count, y_count + 1e-10).sum()  # Perfect fit
deviance = -2 * (log_lik_model - log_lik_saturated)

print("\n" + "=" * 70)
print("POISSON REGRESSION EVALUATION")
print("=" * 70)
print(f"\nDeviance: {deviance:.2f}")
print(f"  (Lower = better fit)")

# Check overdispersion
print(f"\nOverdispersion check:")
print(f"  Observed mean: {y_count.mean():.2f}")
print(f"  Observed variance: {y_count.var():.2f}")
print(f"  Variance/Mean ratio: {y_count.var()/y_count.mean():.2f}")

if y_count.var() / y_count.mean() > 1.5:
    print("  → Overdispersion detected!")
else:
    print("  → Poisson assumption reasonable")
print("=" * 70)
```

### 2.1.1. A concrete example: the mean fits but the variance still raises an alarm

Suppose the number of support calls over 7 consecutive days is: $$2, 3, 4, 2, 3, 4, 18$$. The average of this series is about $$5.1$$, so a Poisson model with $$\lambda$$ around 5 might look "not bad" at a glance. But intuition already shows that something is unusual: the first six days are fairly low, and one day jumps to 18.

In such a situation, the mean alone is not enough to conclude that the model is good. If the posterior predictive distribution produces datasets with a mean near 5 but with a variance and maximum value much smaller than the real data, then the deviance, residual plots, and PPC will all point in the same direction: the model is too narrow relative to the data. This is a very typical sign of overdispersion or of an unmodeled source of variation.

### 2.2. Residual Plots

```python
# Residuals
residuals = y_count - lambda_mean
pearson_residuals = residuals / np.sqrt(lambda_mean)

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Raw residuals
axes[0, 0].scatter(lambda_mean, residuals, alpha=0.6, s=50, edgecolors='black')
axes[0, 0].axhline(0, color='red', linestyle='--', linewidth=2)
axes[0, 0].set_xlabel('Predicted λ', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Raw Residuals', fontsize=12, fontweight='bold')
axes[0, 0].set_title('RAW RESIDUALS\nShould be random around 0',
                    fontsize=14, fontweight='bold')
axes[0, 0].grid(alpha=0.3)

# Pearson residuals
axes[0, 1].scatter(lambda_mean, pearson_residuals, alpha=0.6, s=50, edgecolors='black')
axes[0, 1].axhline(0, color='red', linestyle='--', linewidth=2)
axes[0, 1].axhline(2, color='orange', linestyle='--', linewidth=1, alpha=0.7)
axes[0, 1].axhline(-2, color='orange', linestyle='--', linewidth=1, alpha=0.7)
axes[0, 1].set_xlabel('Predicted λ', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Pearson Residuals', fontsize=12, fontweight='bold')
axes[0, 1].set_title('PEARSON RESIDUALS\nStandardized (should be in [-2, 2])',
                    fontsize=14, fontweight='bold')
axes[0, 1].grid(alpha=0.3)

# QQ plot
from scipy import stats as scipy_stats
scipy_stats.probplot(pearson_residuals, dist="norm", plot=axes[1, 0])
axes[1, 0].set_title('Q-Q PLOT\nCheck normality of residuals',
                    fontsize=14, fontweight='bold')
axes[1, 0].grid(alpha=0.3)

# Histogram of residuals
axes[1, 1].hist(pearson_residuals, bins=30, alpha=0.7, edgecolor='black', density=True)
x_norm = np.linspace(pearson_residuals.min(), pearson_residuals.max(), 100)
axes[1, 1].plot(x_norm, scipy_stats.norm.pdf(x_norm, 0, 1), 'r-', linewidth=3,
               label='Standard Normal')
axes[1, 1].set_xlabel('Pearson Residuals', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1, 1].set_title('RESIDUAL DISTRIBUTION\nCompare to Normal',
                    fontsize=14, fontweight='bold')
axes[1, 1].legend(fontsize=11)
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

## 3. Posterior Predictive Checks for GLMs

```python
# PPC for Poisson
with poisson_model:
    ppc_poisson = pm.sample_posterior_predictive(trace_poisson, random_seed=42)

y_pred_poisson = ppc_poisson.posterior_predictive['y_obs'].values.reshape(-1, n)

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Distribution comparison
axes[0, 0].hist(y_count, bins=range(0, max(y_count)+2), alpha=0.6,
               density=True, label='Observed', edgecolor='black')
for i in range(min(50, y_pred_poisson.shape[0])):
    axes[0, 0].hist(y_pred_poisson[i], bins=range(0, max(y_count)+2),
                   alpha=0.02, density=True, color='red')
axes[0, 0].set_xlabel('Count', fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0, 0].set_title('PPC: DISTRIBUTION\nObserved vs Predicted',
                    fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=11)
axes[0, 0].grid(alpha=0.3, axis='y')

# Mean check
obs_mean = y_count.mean()
pred_means = y_pred_poisson.mean(axis=1)
axes[0, 1].hist(pred_means, bins=30, alpha=0.7, edgecolor='black', density=True)
axes[0, 1].axvline(obs_mean, color='red', linewidth=3, label=f'Observed = {obs_mean:.2f}')
axes[0, 1].set_xlabel('Mean of Predicted Data', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[0, 1].set_title('PPC: MEAN\nDoes model capture mean?',
                    fontsize=14, fontweight='bold')
axes[0, 1].legend(fontsize=11)
axes[0, 1].grid(alpha=0.3, axis='y')

# Variance check
obs_var = y_count.var()
pred_vars = y_pred_poisson.var(axis=1)
axes[1, 0].hist(pred_vars, bins=30, alpha=0.7, edgecolor='black', density=True)
axes[1, 0].axvline(obs_var, color='red', linewidth=3, label=f'Observed = {obs_var:.2f}')
axes[1, 0].set_xlabel('Variance of Predicted Data', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1, 0].set_title('PPC: VARIANCE\nDoes model capture variance?',
                    fontsize=14, fontweight='bold')
axes[1, 0].legend(fontsize=11)
axes[1, 0].grid(alpha=0.3, axis='y')

# Max check
obs_max = y_count.max()
pred_maxs = y_pred_poisson.max(axis=1)
axes[1, 1].hist(pred_maxs, bins=30, alpha=0.7, edgecolor='black', density=True)
axes[1, 1].axvline(obs_max, color='red', linewidth=3, label=f'Observed = {obs_max}')
axes[1, 1].set_xlabel('Max of Predicted Data', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Density', fontsize=12, fontweight='bold')
axes[1, 1].set_title('PPC: MAXIMUM\nDoes model capture extremes?',
                    fontsize=14, fontweight='bold')
axes[1, 1].legend(fontsize=11)
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()
```

### Experiment: posterior predictive check for GLMs

Group calibration for logistic and the zero-share statistic for Poisson; compare a correct model with a misspecified one.

<div class="interactive-demo" markdown="1">
<div data-demo="glmppc-explainer" data-lang="en" data-tab="logistic"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## Summary

GLM evaluation cannot simply reuse the whole toolkit of linear regression. For logistic regression, we need to think at the same time about the confusion matrix, classification measures such as sensitivity or specificity, overall discriminating ability through ROC/AUC, and the quality of predicted probabilities through the calibration plot. For Poisson regression, the focus shifts to deviance, signs of overdispersion, and residual plots to see whether the model is missing some structure in the data. And for every GLM, **posterior predictive checks** remain the final and most important layer of checking, because they let us ask directly whether the data the model generates resembles the real data in the important features.

The point to keep is that each type of outcome requires its own evaluation standard, and no single metric is enough to conclude that a model is “good” or “bad”. The right habit is to always combine specialized metrics with posterior checks to look at the model from several angles.

**Chapter 06 Complete!** GLMs: Logistic, Poisson, Evaluation.

---

### Worked Numerical Example: Computing Exact Bernoulli Log-Loss & Deviance on 3 Observations

Compare Model A vs. Model B predicting 3 binary outcomes $$y = [1,\; 0,\; 1]$$:
- **Model A:** $$p_A = [0.80,\; 0.20,\; 0.70]$$
- **Model B:** $$p_B = [0.95,\; 0.80,\; 0.90]$$ (confidently wrong on observation 2!)

| Obs $$i$$ | Truth $$y_i$$ | Model A $$-\ln p(y_i)$$ | Model B $$-\ln p(y_i)$$ |
| :--- | :--- | :--- | :--- |
| 1 | $$1$$ | $$-\ln(0.80) = 0.223$$ | $$-\ln(0.95) = 0.051$$ |
| 2 | $$0$$ | $$-\ln(0.80) = 0.223$$ | $$-\ln(0.20) = \mathbf{1.609}$$ |
| 3 | $$1$$ | $$-\ln(0.70) = 0.357$$ | $$-\ln(0.90) = 0.105$$ |
| **Total NLL** | — | **$$0.803$$** (Deviance $$= 1.606$$) | **$$1.765$$** (Deviance $$= 3.530$$) |

Model A achieves **less than half the deviance** of Model B because proper log scoring heavily punishes confident mistakes!

### Deep-Dive Explanation: Four Rules for Evaluating Bayesian GLMs (Read Slowly)

1. **Never rely on 0.5-threshold accuracy for imbalanced binary data:** Use Log-Loss, Brier score, calibration plots, and PR-AUC.
2. **Check dispersion (Pearson $$\chi^2 / df$$) on every Poisson GLM:** A ratio near $$1.0$$ supports Poisson; a ratio $$> 1.5\text{–}2.0$$ screams overdispersion $$\to$$ switch to Negative Binomial!
3. **Evaluate out-of-sample (LOO-CV / held-out test set), not just in-sample deviance:** Adding predictors always lowers in-sample deviance even when hurting real predictions.
4. **Inspect subgroup calibration:** A model calibrated globally at 50% can still overpredict Group A by +15% and underpredict Group B by -15%—a sure sign of a missing group intercept or interaction!

**Quick check.** In the 3-observation table above, if a model assigns probability `p = 0.00` to an event that actually happens ($$y = 1$$), what happens to its Log-Loss $$-\ln(p)$$?

---

## Reference videos

- [Machine Learning Fundamentals: The Confusion Matrix](https://www.youtube.com/watch?v=Kdsp6soqA7o) — StatQuest with Josh Starmer, English. **watch first**. Watch the confusion matrix before computing accuracy, exactly the part of the lesson that changes the criteria when the outcome is binary.
- [Probability Calibration : Data Science Concepts](https://www.youtube.com/watch?v=AunotauS5yI) — ritvikmath, English. Watch probability calibration, supporting the argument that a correct classification score does not yet tell whether the probability is trustworthy.
- [Deviance Residuals](https://www.youtube.com/watch?v=JC56jS2gVUE) — StatQuest with Josh Starmer, English. Watch deviance residuals, used when the lesson evaluates count or logistic GLMs beyond the classification metrics.

## Exercises

**Exercise 1**: Fit logistic regression. Compute ROC, AUC. Interpret.

**Exercise 2**: Create calibration plot. Is model well-calibrated?

**Exercise 3**: Fit Poisson regression. Check for overdispersion. If present, what to do?

**Exercise 4**: Perform comprehensive PPC for GLM. Check mean, variance, max, distribution.

**Exercise 5**: Compare two logistic models using ROC curves. Which is better?

## References

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 11: Assumptions, diagnostics, and model evaluation

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 7: Ulysses' Compass (Model Comparison)

---

*Next chapter: [Chapter 07: Regularization]({{ site.baseurl }}/contents/en/chapter07/)*
