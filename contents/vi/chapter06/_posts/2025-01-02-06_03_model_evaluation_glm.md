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

Trong hồi quy tuyến tính cổ điển, ta quen nhìn $$R^2$$ và biểu đồ phần dư đơn giản. Nhưng khi bước sang mô hình tuyến tính tổng quát (GLM) — nơi đầu ra là 0/1 hay số đếm 0, 1, 2, … — phần dư thô $$y_i - \hat p_i$$ không còn tuân theo phân phối chuẩn hay có phương sai đồng nhất nữa. Thậm chí một mô hình dự đoán luôn luôn "không gian lận" trên tập dữ liệu 99% giao dịch sạch vẫn đạt độ chính xác 99% dù hoàn toàn vô dụng.

Bài học này trang bị bộ công cụ đánh giá chuyên biệt cho GLM Bayes: đường cong ROC/AUC, hiệu chỉnh xác suất (*calibration*), log-loss / Brier score, phần dư Deviance/Pearson và kiểm tra dự báo hậu nghiệm (PPC).

---

## Mục tiêu học tập

Sau khi hoàn thành bài học này, bạn sẽ nắm cách đánh giá các **mô hình GLM** như hồi quy logistic và hồi quy Poisson trong thực tế. Trọng tâm của bài là chọn đúng tiêu chí đánh giá theo bản chất của biến kết quả: từ các **thước đo phân lớp (classification metrics)** như accuracy, sensitivity, specificity và đường cong ROC, đến **đồ thị hiệu chỉnh xác suất (calibration plot)**, **độ lệch mô hình (deviance)** và **kiểm tra dự báo hậu nghiệm (posterior predictive checks)**. Một mô hình chỉ thực sự hữu ích khi ta biết rõ nó làm tốt ở điểm nào, hạn chế ở đâu và còn tồn tại những sai lệch nào.


## Bản đồ kiến thức nền: Phân biệt, Hiệu chỉnh và Phản biện mô hình GLM Bayes

Đánh giá đúng một mô hình GLM đòi hỏi kết hợp ba trụ cột độc lập:

- **Khả năng phân biệt vs. Độ hiệu chỉnh (Discrimination vs. Calibration):** AUC-ROC chỉ đo xem mô hình có xếp hạng ca dương tính cao hơn ca âm tính hay không (bất biến nếu nhân đôi mọi xác suất miễn giữ thứ tự). Trong khi đó, **Calibration** kiểm tra xem nhóm có dự báo $$p = 0.70$$ có thực sự xảy ra khoảng $$70\%$$ hay không — yếu tố sống còn cho ra quyết định dựa trên chi phí.
- **Thước đo xác suất nghiêm ngặt (Proper Scoring Rules):** Brier score $$\frac{1}{n}\sum (y_i - \hat p_i)^2$$ và Log-loss (tương ứng Deviance / ELPD) đánh giá đồng thời cả khả năng phân biệt lẫn độ hiệu chỉnh.
- **Chẩn đoán riêng cho GLM (Deviance Residuals & PPC):** Đối với Poisson/Negative Binomial, phần dư Pearson $$r_i = (y_i - \hat\lambda_i)/\sqrt{\hat\lambda_i}$$ và Posterior Predictive Checks (kiểm tra tỷ lệ số 0, phương sai/trung bình, giá trị cực đại) giúp phát hiện chính xác quá phân tán hoặc thừa số 0 (*zero-inflation*).

---

## Giới thiệu: Đánh giá GLMs khác gì so với hồi quy tuyến tính

Với hồi quy tuyến tính, ta thường dùng các chỉ số như $$R^2$$, RMSE hay biểu đồ phần dư (residual) để kiểm tra mức độ khớp dữ liệu. Khi chuyển sang GLMs, tiêu chí đánh giá phải thay đổi theo loại biến kết quả. Với **biến kết quả nhị phân (binary outcomes)**, ta quan tâm đến khả năng phân biệt lớp và độ hiệu chỉnh xác suất nên thường dùng accuracy, đường cong ROC hay calibration. Với **biến kết quả đếm (count outcomes)**, ta cần kiểm tra mức độ khớp của phân phối, deviance và dấu hiệu **quá phân tán (overdispersion)**. Dù vậy, có một nguyên tắc chung cho mọi GLM: luôn thực hiện **kiểm tra dự báo hậu nghiệm (posterior predictive checks)** để so sánh dữ liệu mô hình sinh ra với dữ liệu thực tế.

## 1. Đánh giá hồi quy logistic

![Model Evaluation for GLM]({{ site.baseurl }}/img/chapter_img/chapter06/model_evaluation_glm.png)

### 1.1. Ma trận nhầm lẫn (Confusion Matrix)

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

### 1.1.1. Đánh giá theo quy tắc quyết định thay vì cố định ngưỡng 0.5

Trong phân lớp Bayes, ngưỡng 0.5 chỉ hợp lý khi chi phí của hai loại sai lầm gần như bằng nhau. Khi chi phí khác nhau, ta nên chọn ngưỡng dựa trên rủi ro kỳ vọng (expected risk).

Xét bài toán hai lớp (dương tính/âm tính) với chi phí của **dương tính giả (false positive)** là $$C_{FP}$$ và chi phí của **âm tính giả (false negative)** là $$C_{FN}$$. Quy tắc tối ưu (khi không có tùy chọn từ chối) là dự đoán dương tính khi:

$$
P(y=1\mid x) > \frac{C_{FP}}{C_{FP}+C_{FN}}.
$$

Nếu bổ sung hành động từ chối (reject) với chi phí $$C_R$$, ta chỉ đưa ra quyết định phân lớp khi rủi ro của quyết định đó nhỏ hơn $$C_R$$. Về mặt thực hành, ma trận nhầm lẫn không phải là một bảng đếm tách rời ngữ cảnh: một ngưỡng chỉ có ý nghĩa khi gắn với chi phí thực tế của từng loại sai lầm, bởi trong nhiều ứng dụng, âm tính giả nghiêm trọng hơn nhiều so với dương tính giả hoặc ngược lại.

### 1.1.2. Ví dụ cụ thể: Ngưỡng 0.5 có thể làm bỏ sót ca quan trọng

Giả sử trong bài toán sàng lọc bệnh hiếm, chi phí bỏ sót một ca bệnh cao gấp 9 lần chi phí báo động giả. Khi đó:

$$
\text{threshold tối ưu}=\frac{C_{FP}}{C_{FP}+C_{FN}}=\frac{1}{1+9}=0.1
$$

Nghĩa là chỉ cần $$P(y=1\mid x)>0.1$$, ta đã nên chọn phương án gửi đi kiểm tra bổ sung. Nếu mô hình trả về ba xác suất $$0.18$$, $$0.32$$ và $$0.65$$ cho ba bệnh nhân, cả ba đều cần được theo dõi tiếp. Nếu áp dụng ngưỡng 0.5 một cách máy móc, hai người đầu sẽ bị xếp là âm tính dù rủi ro bỏ sót rất lớn. Ví dụ này cho thấy hồi quy logistic không chỉ dừng ở việc gán nhãn, mà cần sử dụng xác suất hậu nghiệm gắn với chi phí quyết định của bài toán.

### 1.1.3. Hệ số Bayes (Bayes Factor) như thước đo bằng chứng ở mức mô hình

Bên cạnh các thước đo phân lớp theo nhãn, ta có thể so sánh mức độ ủng hộ của dữ liệu giữa hai mô hình hoặc giả thuyết bằng **hệ số Bayes (Bayes factor)**:

$$
BF_{10}=\frac{p(D\mid M_1)}{p(D\mid M_0)}.
$$

Khi $$BF_{10}>1$$, dữ liệu ủng hộ $$M_1$$ nhiều hơn $$M_0$$; khi $$BF_{10}<1$$, bằng chứng nghiêng về $$M_0$$. Như vậy, Bayes factor bổ sung cho ROC/AUC ở một góc nhìn khác: ROC đánh giá năng lực phân biệt nhãn, còn Bayes factor đo mức bằng chứng tương đối giữa các mô hình hoặc giả thuyết.

### 1.2. Đường cong ROC (ROC Curve)

**Đường cong ROC** biểu diễn **độ nhạy (Sensitivity)** theo $$1-\text{Specificity}$$ khi quét qua toàn bộ các ngưỡng phân lớp có thể. Thay vì cố định sớm ở một ngưỡng, ROC cung cấp cái nhìn tổng thể về sự đánh đổi giữa khả năng phát hiện đúng ca dương tính và tỷ lệ báo động giả. **AUC (Area Under the Curve)** tóm tắt toàn bộ đường cong đó bằng một con số: giá trị gần 0.5 tương ứng với phân lớp gần như ngẫu nhiên, còn giá trị tiến gần 1 cho thấy khả năng phân biệt tốt.

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

### 1.3. Đồ thị hiệu chỉnh xác suất (Calibration Plot)

**Hiệu chỉnh xác suất (calibration)** trả lời một câu hỏi khác với ROC: khi mô hình dự đoán xác suất là 0.7, liệu trong thực tế có khoảng 70% trường hợp như vậy xảy ra hay không? Một mô hình có thể phân biệt lớp khá tốt nhưng vẫn hiệu chỉnh kém, tức các xác suất nó đưa ra bị đẩy quá cao hoặc quá thấp. Đồ thị hiệu chỉnh xác suất giúp đánh giá độ tin cậy của chính các xác suất dự báo, chứ không chỉ nhãn phân lớp cuối cùng.

### 1.3.1. Ví dụ cụ thể: AUC tốt nhưng xác suất vẫn lệch

Giả sử mô hình dự đoán cho 10 bệnh nhân với xác suất quanh mức $$0.8$$, nhưng thực tế chỉ có 5 người dương tính. Mô hình vẫn có thể đạt ROC/AUC khá tốt nếu 5 người mắc bệnh nhận xác suất cao hơn phần lớn người không mắc bệnh. Tuy nhiên, xét về calibration, mô hình đang quá tự tin: dự báo "80%" nhưng tần suất thực tế chỉ khoảng "50%".

Tương tự, nếu một nhóm khác được dự báo quanh mức $$0.2$$ nhưng thực tế có tới $$0.35$$ số ca xảy ra, mô hình lại đang đánh giá thấp rủi ro. Như vậy, ROC trả lời câu hỏi "mô hình có xếp hạng đúng người có rủi ro cao hơn không?", còn calibration trả lời câu hỏi "con số xác suất mô hình đưa ra có phản ánh đúng tần suất thực tế hay không?".

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

## 2. Đánh giá hồi quy Poisson

### 2.1. Độ lệch mô hình (Deviance)

**Deviance** là thước đo mức độ khớp của mô hình trong họ GLM. Theo trực giác, deviance đo khoảng cách giữa mô hình đang xét với một mô hình bão hòa (saturated model) khớp hoàn hảo dữ liệu. Giá trị deviance càng nhỏ thì mô hình càng gần mức khớp lý tưởng đó:

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

### 2.1.1. Ví dụ cụ thể: Trung bình khớp nhưng phương sai báo động

Giả sử số cuộc gọi hỗ trợ trong 7 ngày liên tiếp là: $$2, 3, 4, 2, 3, 4, 18$$. Trung bình của chuỗi này vào khoảng $$5.1$$, nên một mô hình Poisson với $$\lambda$$ quanh mức 5 có vẻ khớp với giá trị trung bình. Tuy nhiên, chuỗi số liệu cho thấy sự bất thường rõ rệt: sáu ngày đầu khá thấp, còn một ngày vọt lên 18.

Trong tình huống này, chỉ nhìn vào trung bình là không đủ để kết luận mô hình tốt. Nếu phân phối dự báo hậu nghiệm sinh ra các tập dữ liệu có trung bình gần 5 nhưng phương sai và giá trị cực đại nhỏ hơn dữ liệu thực rất nhiều, thì deviance, biểu đồ phần dư và PPC sẽ cùng chỉ ra rằng mô hình quá hẹp so với dữ liệu. Đây là dấu hiệu điển hình của hiện tượng quá phân tán (overdispersion) hoặc của một nguồn biến thiên chưa được đưa vào mô hình.

### 2.2. Biểu đồ phần dư (Residual Plots)

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

## 3. Kiểm tra dự báo hậu nghiệm cho GLMs

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

### Thử nghiệm: Kiểm tra dự báo hậu nghiệm cho GLM

Quan sát độ hiệu chuẩn theo nhóm cho hồi quy logistic và thống kê số giá trị 0 cho hồi quy Poisson để so sánh mô hình đặc tả đúng với mô hình đặc tả sai.

<div class="interactive-demo" markdown="1">
<div data-demo="glmppc-explainer" data-lang="vi" data-tab="logistic"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## Tóm tắt

Đánh giá GLM không thể chỉ sử dụng lại bộ công cụ của hồi quy tuyến tính. Với hồi quy logistic, cần xem xét đồng thời ma trận nhầm lẫn, các thước đo phân lớp như sensitivity và specificity, năng lực phân biệt tổng quát qua ROC/AUC, và độ tin cậy của xác suất dự báo qua đồ thị hiệu chỉnh xác suất. Với hồi quy Poisson, trọng tâm chuyển sang deviance, dấu hiệu quá phân tán và biểu đồ phần dư để phát hiện các cấu trúc còn bị bỏ sót. Với mọi GLM, **kiểm tra dự báo hậu nghiệm (posterior predictive checks)** vẫn là bước kiểm chứng quan trọng nhất để xem dữ liệu mô hình sinh ra có tái hiện được các đặc điểm chính của dữ liệu thực hay không.

Mỗi loại biến kết quả đòi hỏi bộ tiêu chí đánh giá tương ứng, và không có một chỉ số đơn lẻ nào đủ để kết luận mô hình tốt hay xấu. Cách làm hợp lý là kết hợp các thước đo chuyên biệt với kiểm tra dự báo hậu nghiệm để đánh giá mô hình từ nhiều góc độ.

Kết thúc Chương 06 về các mô hình tuyến tính tổng quát (GLMs): hồi quy logistic, hồi quy Poisson và đánh giá mô hình.


## Khung giải thích (nên đọc chậm): Đọc Brier Score, Calibration và Phần dư Pearson bằng tay

Để không bao giờ bị đánh lừa bởi một chỉ số đơn lẻ (như accuracy hay AUC), hãy kiểm tra theo 4 bước sau:

1. **Kiểm tra khả năng phân biệt (ROC-AUC / PR-AUC):** Đặc biệt dùng PR-AUC khi lớp dương tính hiếm.
2. **Kiểm tra độ hiệu chỉnh (Calibration):** Chia dự báo thành các nhóm xác suất và so sánh trung bình dự báo với tần suất thật.
3. **Tính thước đo tổng hợp (Brier Score / Log-Loss / LOO):** So sánh khách quan giữa các mô hình GLM cạnh tranh.
4. **Chạy PPC cho đặc trưng miền dữ liệu:** Với Poisson, luôn kiểm tra tỷ lệ quan sát bằng 0 và tỷ số phương sai/trung bình.

### Ví dụ tính toán cầm tay chỉ việc: Brier Score và Độ hiệu chỉnh trên 4 dự báo nhị phân

Xét 4 ca dự báo xác suất của hai mô hình logistic trên cùng tập nhãn thật $$y = (1, 1, 0, 0)$$:
- **Mô hình A (Hiệu chỉnh tốt):** $$\hat p_A = (0.8, 0.7, 0.3, 0.2)$$.
- **Mô hình B (Đoán đúng thứ tự — cùng AUC = 1.0 — nhưng hiệu chỉnh kém):** $$\hat p_B = (0.55, 0.52, 0.48, 0.45)$$.

| Quan sát | Nhãn $$y_i$$ | $$(y_i - \hat p_{A,i})^2$$ | $$(y_i - \hat p_{B,i})^2$$ |
| --- | --- | --- | --- |
| 1 | $$1$$ | $$(1 - 0.8)^2 = 0.04$$ | $$(1 - 0.55)^2 = 0.2025$$ |
| 2 | $$1$$ | $$(1 - 0.7)^2 = 0.09$$ | $$(1 - 0.52)^2 = 0.2304$$ |
| 3 | $$0$$ | $$(0 - 0.3)^2 = 0.09$$ | $$(0 - 0.48)^2 = 0.2304$$ |
| 4 | $$0$$ | $$(0 - 0.2)^2 = 0.04$$ | $$(0 - 0.45)^2 = 0.2025$$ |
| **Brier Score (trung bình)** | — | **$$0.26 / 4 = 0.0650$$** | **$$0.8658 / 4 = 0.2165$$** |

Cả hai mô hình đều đạt $$\text{AUC} = 1.00$$ và $$\text{Accuracy} = 100\%$$ ở ngưỡng $$0.5$$, nhưng Brier Score lập tức vạch rõ Mô hình A vượt trội hơn gấp **3.3 lần** ($$0.0650$$ so với $$0.2165$$) nhờ dự báo xác suất sắc nét và hiệu chỉnh tốt hơn.

**Hiểu lầm cần tránh:** Chỉ nhìn AUC cao (ví dụ $$0.92$$) rồi tin rằng xác suất đầu ra có thể nhân trực tiếp với lợi nhuận kỳ vọng. Nếu mô hình bị lệch calibration, quyết định tài chính dựa trên ngưỡng xác suất vẫn sẽ sai.

**Kiểm tra nhanh:** Trong hồi quy Poisson, nếu quan sát $$y_i = 15$$ khi mô hình dự báo $$\hat\lambda_i = 4$$, phần dư Pearson là $$(15 - 4)/\sqrt{4} = 5.5$$ — vượt rất xa ngưỡng $$\pm 2$$, cảnh báo ngay điểm bất thường hoặc hiện tượng quá phân tán.

---

## Video tham khảo

- [Machine Learning Fundamentals: The Confusion Matrix](https://www.youtube.com/watch?v=Kdsp6soqA7o) — StatQuest with Josh Starmer, English. **Xem trước**. Giới thiệu ma trận nhầm lẫn trước khi tính accuracy, phù hợp với phần đánh giá biến kết quả nhị phân.
- [Probability Calibration : Data Science Concepts](https://www.youtube.com/watch?v=AunotauS5yI) — ritvikmath, English. Giải thích hiệu chỉnh xác suất, minh họa rằng điểm phân lớp cao chưa bảo đảm xác suất dự báo đáng tin cậy.
- [Deviance Residuals](https://www.youtube.com/watch?v=JC56jS2gVUE) — StatQuest with Josh Starmer, English. Trình bày phần dư deviance, hữu ích khi đánh giá mô hình GLM đếm hoặc logistic ngoài các chỉ số phân lớp.

## Bài tập

**Bài tập 1**: Khớp một mô hình hồi quy logistic, tính đường cong ROC và chỉ số AUC, sau đó diễn giải kết quả.

**Bài tập 2**: Vẽ đồ thị hiệu chỉnh xác suất (calibration plot) và đánh giá xem mô hình đã được hiệu chỉnh tốt chưa.

**Bài tập 3**: Khớp một mô hình hồi quy Poisson, kiểm tra hiện tượng quá phân tán (overdispersion) và nêu hướng xử lý nếu hiện tượng này xuất hiện.

**Bài tập 4**: Thực hiện kiểm tra dự báo hậu nghiệm (PPC) đầy đủ cho mô hình GLM trên các thống kê: trung bình, phương sai, giá trị cực đại và phân phối tổng thể.

**Bài tập 5**: So sánh hai mô hình hồi quy logistic bằng đường cong ROC và xác định mô hình nào tốt hơn.

## Tài liệu tham khảo

**Gelman, A., et al. (2020).** *Regression and Other Stories*. Cambridge University Press.
- Chapter 11: Assumptions, diagnostics, and model evaluation

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 7: Ulysses' Compass (Model Comparison)

---

*Chương tiếp theo: [Chapter 07: Regularization]({{ site.baseurl }}/contents/vi/chapter07/)*
