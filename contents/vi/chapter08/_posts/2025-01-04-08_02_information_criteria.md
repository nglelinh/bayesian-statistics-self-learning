---
layout: post
title: "Bài 8.2: Information Criteria - WAIC và LOO"
chapter: '08'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter08
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **information criteria** như những thước đo dùng để so sánh mô hình dựa trên năng lực dự báo ngoài mẫu, chứ không phải chỉ dựa trên độ khớp với dữ liệu huấn luyện. Bài học sẽ giải thích WAIC, LOO-CV, cách tính chúng với ArviZ, và quan trọng hơn là cách diễn giải kết quả sao cho không rơi vào lối dùng chỉ số một cách máy móc. Đây là công cụ then chốt cho **model selection** (chọn mô hình) trong Bayesian workflow.

## Giới thiệu: The Problem of Model Selection

Giả sử bạn có ba mô hình ứng viên, từ một mô hình tuyến tính đơn giản đến một mô hình đa thức phức tạp hơn nhiều. Câu hỏi “mô hình nào là tốt nhất?” thoạt nhìn có vẻ dễ trả lời bằng cách chọn mô hình có training error nhỏ nhất, nhưng đó chính là câu trả lời sai cổ điển vì nó mở đường cho overfitting. Câu trả lời đúng phải xoay quanh **out-of-sample predictive accuracy** (độ chính xác dự báo ngoài mẫu), tức khả năng dự đoán dữ liệu mới mà mô hình chưa từng nhìn thấy.

## 1. Predictive Accuracy: The Gold Standard

Mục tiêu thật sự của model comparison là ước lượng xem mô hình dự đoán **new data** tốt đến mức nào. Vì vậy, predictive accuracy mới là “gold standard”, còn training fit chỉ là một tín hiệu phụ rất dễ gây hiểu lầm nếu đứng một mình.

**Log Pointwise Predictive Density (lppd)**:
$$
\text{lppd} = \sum_{i=1}^n \log p(y_i | y_{-i})
$$

where $$y_{-i}$$ = all data except $$i$$.

Vấn đề là nếu làm điều này một cách ngây thơ bằng leave-one-out thực thụ, ta phải fit lại mô hình tới $$n$$ lần, thường là quá tốn kém. Information criteria xuất hiện như những xấp xỉ có cơ sở lý thuyết cho bài toán đó.

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az

# Generate data
np.random.seed(42)
n = 50
x = np.random.uniform(0, 10, n)
y_true = 2 + 0.5*x + 0.1*x**2 + np.random.normal(0, 1, n)

# Standardize
x_z = (x - x.mean()) / x.std()
y_z = (y_true - y_true.mean()) / y_true.std()

print("=" * 70)
print("MODEL SELECTION PROBLEM")
print("=" * 70)
print("\nWe have data generated from: y = 2 + 0.5x + 0.1x²")
print("\nWhich model fits best?")
print("  Model 1: Linear (y ~ x)")
print("  Model 2: Quadratic (y ~ x + x²)")
print("  Model 3: Cubic (y ~ x + x² + x³)")
print("=" * 70)
```

## 2. WAIC: Watanabe-Akaike Information Criterion

**WAIC** có thể được xem như phiên bản Bayesian của AIC, nhưng cần hiểu nó không đơn thuần là một công thức thay tên đổi họ. Nó cố gắng cân bằng giữa mức độ khớp của mô hình với dữ liệu và độ phức tạp hiệu dụng của mô hình.

$$
\text{WAIC} = -2(\text{lppd} - p_{\text{WAIC}})
$$

where $$p_{\text{WAIC}}$$ = effective number of parameters (penalty).

Giá trị WAIC càng thấp thì predictive accuracy ước lượng càng tốt.

```python
# Fit 3 models
models = {}
traces = {}

# Model 1: Linear
with pm.Model() as model_linear:
    alpha = pm.Normal('alpha', 0, 1)
    beta1 = pm.Normal('beta1', 0, 1)
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + beta1 * x_z
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    traces['Linear'] = pm.sample(1000, tune=500, chains=2, random_seed=42,
                                 return_inferencedata=True, progressbar=False)

# Model 2: Quadratic
with pm.Model() as model_quad:
    alpha = pm.Normal('alpha', 0, 1)
    beta1 = pm.Normal('beta1', 0, 1)
    beta2 = pm.Normal('beta2', 0, 1)
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + beta1 * x_z + beta2 * x_z**2
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    traces['Quadratic'] = pm.sample(1000, tune=500, chains=2, random_seed=42,
                                    return_inferencedata=True, progressbar=False)

# Model 3: Cubic
with pm.Model() as model_cubic:
    alpha = pm.Normal('alpha', 0, 1)
    beta1 = pm.Normal('beta1', 0, 1)
    beta2 = pm.Normal('beta2', 0, 1)
    beta3 = pm.Normal('beta3', 0, 1)
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + beta1 * x_z + beta2 * x_z**2 + beta3 * x_z**3
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_z)
    
    traces['Cubic'] = pm.sample(1000, tune=500, chains=2, random_seed=42,
                                return_inferencedata=True, progressbar=False)

# Compute WAIC
print("\n" + "=" * 70)
print("WAIC COMPARISON")
print("=" * 70)

for name, trace in traces.items():
    waic = az.waic(trace)
    print(f"\n{name}:")
    print(f"  WAIC: {waic.waic:.2f}")
    print(f"  pWAIC: {waic.p_waic:.2f} (effective parameters)")
    print(f"  SE: {waic.waic_se:.2f}")

print("\n→ Lower WAIC = Better!")
print("=" * 70)
```

## 3. LOO-CV: Leave-One-Out Cross-Validation

**LOO-CV** thường được xem là chuẩn tham chiếu cho predictive accuracy vì nó trực tiếp hỏi: nếu bỏ một điểm dữ liệu ra ngoài, mô hình còn lại dự đoán điểm đó tốt đến mức nào. Về nguyên tắc, ta phải lần lượt bỏ từng quan sát $$y_i$$, fit mô hình trên $$n-1$$ điểm còn lại, rồi đánh giá log probability của chính điểm bị bỏ ra. Cách làm này rất thuyết phục về mặt khái niệm nhưng lại quá đắt về mặt tính toán. Vì vậy, trong thực hành Bayesian, người ta thường dùng **PSIS-LOO** để xấp xỉ LOO mà không cần refit mô hình nhiều lần.

```python
# Compute LOO
print("\n" + "=" * 70)
print("LOO-CV COMPARISON")
print("=" * 70)

for name, trace in traces.items():
    loo = az.loo(trace)
    print(f"\n{name}:")
    print(f"  LOO: {loo.loo:.2f}")
    print(f"  pLOO: {loo.p_loo:.2f} (effective parameters)")
    print(f"  SE: {loo.loo_se:.2f}")
    
    # Check Pareto k diagnostic
    if hasattr(loo, 'pareto_k'):
        bad_k = np.sum(loo.pareto_k > 0.7)
        if bad_k > 0:
            print(f"  ⚠️  Warning: {bad_k} observations with high Pareto k")

print("\n→ Lower LOO = Better!")
print("=" * 70)
```

## 4. Model Comparison with az.compare

Trong thực hành, cách gọn và đáng tin cậy nhất là dùng `az.compare` để so sánh tất cả các mô hình cùng lúc, thay vì đọc WAIC hay LOO của từng mô hình một cách rời rạc.

```python
# Compare all models
comp = az.compare(traces, ic='loo')

print("\n" + "=" * 70)
print("MODEL COMPARISON TABLE")
print("=" * 70)
print(comp)
print("=" * 70)

# Visualize
az.plot_compare(comp, figsize=(10, 4))
plt.title('Model Comparison (LOO)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("INTERPRETING RESULTS")
print("=" * 70)
print("\nColumns:")
print("  rank: 0 = best model")
print("  loo: LOO score (higher = better)")
print("  p_loo: Effective number of parameters")
print("  d_loo: Difference from best model")
print("  weight: Stacking weights for model averaging")
print("  se: Standard error")
print("  dse: SE of difference")

best_model = comp.index[0]
print(f"\n→ Best model: {best_model}")
print("=" * 70)
```

## 5. Pareto k Diagnostic

**Pareto k** là diagnostic dùng để kiểm tra xem xấp xỉ PSIS-LOO có đáng tin hay không. Khi $$k<0.5$$, ta thường có thể yên tâm rằng xấp xỉ hoạt động tốt; khi $$k$$ nằm giữa 0.5 và 0.7, kết quả vẫn có thể chấp nhận được nhưng cần cẩn trọng hơn; còn khi $$k>0.7$$, dấu hiệu cảnh báo đã đủ mạnh để nghi ngờ rằng LOO hiện tại không còn ổn định và có thể cần những biện pháp khác.

```python
# Plot Pareto k
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, (name, trace) in enumerate(traces.items()):
    loo = az.loo(trace, pointwise=True)
    k_values = loo.pareto_k.values
    
    axes[idx].scatter(range(len(k_values)), k_values, s=50, alpha=0.6,
                     edgecolors='black')
    axes[idx].axhline(0.5, color='orange', linestyle='--', linewidth=2,
                     label='Threshold 0.5')
    axes[idx].axhline(0.7, color='red', linestyle='--', linewidth=2,
                     label='Threshold 0.7')
    axes[idx].set_xlabel('Data Point', fontsize=12, fontweight='bold')
    axes[idx].set_ylabel('Pareto k', fontsize=12, fontweight='bold')
    axes[idx].set_title(f'{name}\nMax k = {k_values.max():.3f}',
                       fontsize=13, fontweight='bold')
    axes[idx].legend(fontsize=10)
    axes[idx].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

## Tóm tắt

Information criteria cho ta một ngôn ngữ nhất quán để so sánh mô hình theo mục tiêu dự báo ngoài mẫu. WAIC cung cấp một xấp xỉ nhanh và hoàn toàn Bayesian cho năng lực dự báo, còn LOO-CV gần với chuẩn tham chiếu hơn và trong thực hành thường được tính qua PSIS-LOO. Khi dùng các chỉ số này, điều quan trọng không phải là thuộc lòng tên viết tắt, mà là luôn nhớ rằng mô hình nên được chọn theo **predictive accuracy**, không phải theo training fit. Diagnostic Pareto k đóng vai trò nhắc ta rằng ngay cả một tiêu chí tốt cũng cần được kiểm tra độ tin cậy trước khi ra quyết định.

Bài tiếp theo: **Model Comparison** strategies.

## Bài tập

**Bài tập 1**: Fit 4 polynomial models (degree 1-4). Compute WAIC and LOO. Which is best?

**Bài tập 2**: Check Pareto k. If k > 0.7, what does it mean? How to fix?

**Bài tập 3**: Use `az.compare`. Interpret all columns. What is "weight"?

**Bài tập 4**: Compare GLMs (Logistic, Poisson) using LOO. Which fits better?

**Bài tập 5**: Real data. Fit multiple models. Use information criteria to select best.

## Tài liệu Tham khảo

**Vehtari, A., Gelman, A., & Gabry, J. (2017).** "Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC." *Statistics and Computing*, 27(5), 1413-1432.

**Gelman, A., et al. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 7: Evaluating, comparing, and expanding models

---

*Bài học tiếp theo: [8.3 Model Comparison Strategies](/vi/chapter08/model-comparison/)*
