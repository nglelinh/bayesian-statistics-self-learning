---
layout: post
title: "Bài 8.3: Model Comparison Strategies"
chapter: '08'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter08
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu các chiến lược khác nhau cho **model comparison**, bao gồm **model selection** (chọn một mô hình tốt nhất), **model averaging** (trung bình hóa dự báo từ nhiều mô hình), và **model expansion** (mở rộng sang một mô hình lớn hơn bao trùm các lựa chọn nhỏ hơn). Bài học cũng sẽ giải thích cách dùng `az.compare` một cách hiệu quả và cách diễn giải **stacking weights** sao cho đúng tinh thần dự báo Bayesian.

## Giới thiệu: Three Approaches

Khi có nhiều mô hình cạnh tranh, ta không nhất thiết chỉ có một lựa chọn duy nhất là “chọn ra kẻ thắng cuộc”. Trong thực hành, có ba chiến lược lớn. Một là **model selection**, tức chọn mô hình có năng lực dự báo tốt nhất theo tiêu chí đang dùng. Hai là **model averaging**, tức kết hợp dự báo từ nhiều mô hình bằng các trọng số thích hợp để phản ánh bất định mô hình. Ba là **model expansion**, tức xây dựng một mô hình lớn hơn bao quát các lựa chọn con thay vì buộc phải loại trừ lẫn nhau.

## 1. Model Selection

Ý tưởng của model selection là chọn mô hình có LOO hay WAIC tốt nhất, tức mô hình được kỳ vọng dự báo ngoài mẫu tốt nhất trong tập ứng viên. Ưu điểm của cách này là đơn giản và dễ diễn giải. Nhược điểm của nó là thường bỏ qua độ bất định về chính lựa chọn mô hình, đặc biệt khi nhiều mô hình có hiệu năng rất sát nhau.

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az

# Example: Compare 3 models (from Bài 8.2)
# Assume traces = {'Linear': trace1, 'Quadratic': trace2, 'Cubic': trace3}

# Model selection
comp = az.compare(traces, ic='loo')
best_model_name = comp.index[0]

print("=" * 70)
print("MODEL SELECTION")
print("=" * 70)
print(f"\nBest model: {best_model_name}")
print(f"LOO: {comp.loc[best_model_name, 'loo']:.2f}")
print("\n→ Use this model for predictions")
print("=" * 70)
```

## 2. Model Averaging

Model averaging đi theo hướng khác: thay vì cưỡng bức một quyết định chọn duy nhất, nó lấy trung bình có trọng số của các dự báo từ nhiều mô hình.

Các trọng số này thường được xây dựng từ predictive accuracy, chẳng hạn qua **stacking weights**, để mô hình dự báo tốt hơn đóng góp nhiều hơn vào kết quả cuối cùng.

$$
\hat{y} = \sum_{k=1}^K w_k \hat{y}_k
$$

where $$w_k$$ = weight for model $$k$$.

```python
# Model averaging with stacking weights
weights = comp['weight'].values
model_names = comp.index.tolist()

print("\n" + "=" * 70)
print("MODEL AVERAGING (Stacking)")
print("=" * 70)
print("\nWeights:")
for name, weight in zip(model_names, weights):
    print(f"  {name}: {weight:.3f}")

print("\n→ Prediction = weighted average")
print("=" * 70)

# Visualize weights
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(model_names, weights, alpha=0.7, edgecolor='black')
ax.set_xlabel('Stacking Weight', fontsize=12, fontweight='bold')
ax.set_ylabel('Model', fontsize=12, fontweight='bold')
ax.set_title('MODEL AVERAGING WEIGHTS\nHigher weight = Better model',
            fontsize=14, fontweight='bold')
ax.grid(alpha=0.3, axis='x')
plt.tight_layout()
plt.show()
```

## 3. Making Predictions

### 3.1. Model Selection Approach

```python
# Use best model only
best_trace = traces[best_model_name]

# Posterior predictive
with pm.Model() as best_model:
    # ... (redefine model)
    ppc = pm.sample_posterior_predictive(best_trace, random_seed=42)

y_pred_best = ppc.posterior_predictive['y_obs'].values.reshape(-1, len(y_z))
y_pred_mean = y_pred_best.mean(axis=0)

print("\n" + "=" * 70)
print("PREDICTIONS: Model Selection")
print("=" * 70)
print(f"\nUsing: {best_model_name}")
print(f"Prediction shape: {y_pred_best.shape}")
print("=" * 70)
```

### 3.2. Model Averaging Approach

```python
# Combine predictions from all models
all_predictions = []

for name in model_names:
    trace = traces[name]
    # ... generate predictions
    # all_predictions.append(pred)

# Weighted average
y_pred_avg = sum(w * pred for w, pred in zip(weights, all_predictions))

print("\n" + "=" * 70)
print("PREDICTIONS: Model Averaging")
print("=" * 70)
print("\nCombining all models with weights")
print("→ More robust to model uncertainty")
print("=" * 70)
```

## 4. Khi nào Dùng Approach Nào?

| Approach | When to Use | Pros | Cons |
|----------|-------------|------|------|
| **Selection** | Clear best model (Δ LOO > 4) | Simple, interpretable | Ignores uncertainty |
| **Averaging** | Multiple good models (Δ LOO < 4) | Robust, accounts for uncertainty | More complex |
| **Expansion** | Models nested, theory-driven | Single coherent model | Can be complex |

```python
# Decision rule based on LOO difference
comp = az.compare(traces, ic='loo')
d_loo = comp['d_loo'].values

print("\n" + "=" * 70)
print("DECISION RULE")
print("=" * 70)
print(f"\nΔ LOO (best vs 2nd): {d_loo[1]:.2f}")

if d_loo[1] > 4:
    print("\n→ Clear winner! Use MODEL SELECTION")
    print(f"   Best model: {comp.index[0]}")
elif d_loo[1] < 2:
    print("\n→ Models similar! Use MODEL AVERAGING")
    print("   Combine predictions with stacking weights")
else:
    print("\n→ Moderate difference. Either approach OK")
    print("   Consider context and interpretability")
print("=" * 70)
```

## Tóm tắt

Model comparison không phải lúc nào cũng đồng nghĩa với việc chọn ra một mô hình duy nhất. Khi một mô hình thắng rõ ràng, model selection là cách làm tự nhiên và dễ truyền đạt. Khi nhiều mô hình gần ngang nhau, model averaging thường hợp lý hơn vì nó phản ánh đúng bất định về cấu trúc mô hình và thường cho dự báo ổn định hơn. Stacking weights cung cấp một cơ chế thực dụng để hiện thực hóa ý tưởng đó, còn `az.compare` gom hầu hết thông tin cần thiết vào cùng một bảng. Điểm quan trọng nhất là chiến lược so sánh mô hình nên được chọn theo mục tiêu dự báo và mức độ bất định mô hình, chứ không chỉ theo thói quen “chọn hạng nhất”.

Bài tiếp theo: **Decision Analysis** - from inference to action.

## Bài tập

**Bài tập 1**: Fit 3 models. Use az.compare. Should you select or average?

**Bài tập 2**: Implement model averaging manually. Compare with single best model.

**Bài tập 3**: Vary data size. How does Δ LOO change? Selection vs averaging?

**Bài tập 4**: Real data. Compare models. Make predictions using both approaches.

## Tài liệu Tham khảo

**Yao, Y., et al. (2018).** "Using stacking to average Bayesian predictive distributions." *Bayesian Analysis*, 13(3), 917-1007.

---

*Bài học tiếp theo: [8.4 Bayesian Decision Analysis](/vi/chapter08/decision-analysis/)*
