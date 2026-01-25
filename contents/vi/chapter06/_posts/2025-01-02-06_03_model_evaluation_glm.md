---
layout: post
title: "Bài 6.3: Model Evaluation for GLMs"
chapter: '06'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter06
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu cách đánh giá **GLM models** (Logistic, Poisson). Bạn sẽ học về **classification metrics** (accuracy, sensitivity, specificity, ROC curves), **calibration plots**, và **posterior predictive checks** cho GLMs. Đây là kỹ năng quan trọng để đánh giá model performance trong thực tế.

## Giới thiệu: Evaluating GLMs Khác Linear Regression

Với linear regression, chúng ta dùng:
- R², RMSE, residual plots

Với GLMs:
- **Binary outcomes**: Accuracy, ROC, calibration
- **Count outcomes**: Deviance, overdispersion checks
- **All GLMs**: Posterior predictive checks

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

# Confusion matrices với different thresholds
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

### 1.2. ROC Curve

**ROC (Receiver Operating Characteristic)**: Plot Sensitivity vs (1 - Specificity) for all thresholds.

**AUC (Area Under Curve)**: Summary metric (0.5 = random, 1.0 = perfect).

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

**Calibration**: Do predicted probabilities match observed frequencies?

**Perfect calibration**: If model predicts p=0.7, then 70% of cases should be y=1.

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

**Deviance**: Measure of fit cho GLMs (lower = better).

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

## Tóm tắt

Model evaluation cho GLMs:

**Logistic Regression**:
- Confusion matrix, accuracy, sensitivity, specificity
- ROC curve, AUC
- Calibration plots

**Poisson Regression**:
- Deviance
- Overdispersion checks
- Residual plots

**All GLMs**:
- Posterior predictive checks
- Compare observed vs predicted distributions

**Key insight**: Different outcomes require different evaluation metrics. Always use PPC!

**Chapter 06 Complete!** GLMs: Logistic, Poisson, Evaluation.

## Bài tập

**Bài tập 1**: Fit logistic regression. Compute ROC, AUC. Interpret.

**Bài tập 2**: Create calibration plot. Is model well-calibrated?

**Bài tập 3**: Fit Poisson regression. Check for overdispersion. If present, what to do?

**Bài tập 4**: Perform comprehensive PPC for GLM. Check mean, variance, max, distribution.

**Bài tập 5**: Compare two logistic models using ROC curves. Which is better?

## Tài liệu Tham khảo

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 11: Assumptions, diagnostics, and model evaluation

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 7: Ulysses' Compass (Model Comparison)

---

*Chương tiếp theo: [Chapter 07: Regularization](/vi/chapter07/)*
