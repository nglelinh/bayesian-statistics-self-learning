---
layout: post
title: "Bài 8.4: Bayesian Decision Analysis - From Inference to Action"
chapter: '08'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter08
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu cách connect Bayesian inference với **decision-making**. Bạn sẽ học về loss functions, utility functions, expected loss, và cách choose optimal actions under uncertainty. Đây là bước cuối cùng trong Bayesian workflow - từ data → inference → decision → action.

## Giới thiệu: Inference ≠ Decision

**Bayesian inference** cho chúng ta:
- Posterior distributions: $$p(\theta \mid y)$$
- Predictions: $$p(\tilde{y} \mid y)$$
- Uncertainty quantification

**Nhưng**: Trong thực tế, chúng ta cần **làm gì đó** (take action)!

**Bayesian decision theory**: Framework để choose optimal action given uncertainty.

## 1. Decision Theory Framework

### 1.1. Components

1. **Actions** ($$a$$): Possible choices
2. **States** ($$\theta$$): Unknown parameters
3. **Loss function** $$L(a, \theta)$$: Cost of action $$a$$ when truth is $$\theta$$
4. **Posterior** $$p(\theta \mid y)$$: Belief about $$\theta$$

**Goal**: Choose action $$a$$ that minimizes **expected loss**:
$$
\mathbb{E}[L(a, \theta) | y] = \int L(a, \theta) p(\theta \mid y) d\theta
$$

### 1.2. Example: Medical Decision

```python
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az

# Scenario: Disease diagnosis
# Posterior: P(disease \mid test) = 0.7

# Actions:
# a1: No treatment
# a2: Treatment
# a3: More tests

# Loss function (in "utility units")
# Rows: True state (disease=1, healthy=0)
# Cols: Actions (no_treat, treat, more_tests)

loss_matrix = np.array([
    [0, 10, 5],      # Healthy: no harm, treatment cost, test cost
    [100, 5, 20]     # Disease: death, cure, delay+test
])

# Posterior probabilities
p_disease = 0.7
p_healthy = 0.3
posterior = np.array([p_healthy, p_disease])

# Expected loss for each action
expected_losses = loss_matrix.T @ posterior

actions = ['No Treatment', 'Treatment', 'More Tests']

print("=" * 70)
print("MEDICAL DECISION ANALYSIS")
print("=" * 70)
print(f"\nPosterior: P(disease \mid test) = {p_disease}")
print("\nExpected Loss:")
for action, exp_loss in zip(actions, expected_losses):
    print(f"  {action}: {exp_loss:.1f}")

optimal_action = actions[np.argmin(expected_losses)]
print(f"\n→ Optimal action: {optimal_action}")
print("=" * 70)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Loss matrix
im = axes[0].imshow(loss_matrix, cmap='RdYlGn_r', aspect='auto')
axes[0].set_xticks(range(3))
axes[0].set_xticklabels(actions, rotation=45, ha='right')
axes[0].set_yticks(range(2))
axes[0].set_yticklabels(['Healthy', 'Disease'])
axes[0].set_title('LOSS MATRIX\nL(action, state)',
                 fontsize=14, fontweight='bold')

for i in range(2):
    for j in range(3):
        axes[0].text(j, i, f'{loss_matrix[i, j]}',
                    ha='center', va='center', fontsize=14, fontweight='bold')

plt.colorbar(im, ax=axes[0])

# Expected losses
axes[1].barh(actions, expected_losses, alpha=0.7, edgecolor='black')
axes[1].axvline(expected_losses.min(), color='red', linestyle='--',
               linewidth=2, label='Minimum')
axes[1].set_xlabel('Expected Loss', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Action', fontsize=12, fontweight='bold')
axes[1].set_title('EXPECTED LOSS\nChoose minimum',
                 fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3, axis='x')

plt.tight_layout()
plt.show()
```

## 2. Common Loss Functions

### 2.1. Point Estimation

**Squared error loss**: $$L(\hat{\theta}, \theta) = (\hat{\theta} - \theta)^2$$
- Optimal estimate: **Posterior mean**

**Absolute error loss**: $$L(\hat{\theta}, \theta) = |\hat{\theta} - \theta|$$
- Optimal estimate: **Posterior median**

**0-1 loss**: $$L(\hat{\theta}, \theta) = \mathbb{1}(\hat{\theta} \neq \theta)$$
- Optimal estimate: **Posterior mode**

```python
# Example: Estimate parameter with different loss functions
np.random.seed(42)

# Generate skewed posterior (Beta distribution)
from scipy import stats
alpha, beta = 2, 5
theta_samples = stats.beta.rvs(alpha, beta, size=10000)

# Optimal estimates under different losses
mean_est = theta_samples.mean()  # Squared loss
median_est = np.median(theta_samples)  # Absolute loss
mode_est = stats.beta.mode(alpha, beta)[0]  # 0-1 loss

# Visualize
fig, ax = plt.subplots(figsize=(12, 6))

ax.hist(theta_samples, bins=50, density=True, alpha=0.6,
       edgecolor='black', label='Posterior')
ax.axvline(mean_est, color='blue', linewidth=3, label=f'Mean = {mean_est:.3f}')
ax.axvline(median_est, color='green', linewidth=3, label=f'Median = {median_est:.3f}')
ax.axvline(mode_est, color='red', linewidth=3, label=f'Mode = {mode_est:.3f}')
ax.set_xlabel('θ', fontsize=12, fontweight='bold')
ax.set_ylabel('Density', fontsize=12, fontweight='bold')
ax.set_title('OPTIMAL ESTIMATES\nDepend on loss function!',
            fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("OPTIMAL ESTIMATES UNDER DIFFERENT LOSSES")
print("=" * 70)
print(f"\nSquared loss → Mean: {mean_est:.3f}")
print(f"Absolute loss → Median: {median_est:.3f}")
print(f"0-1 loss → Mode: {mode_est:.3f}")
print("\n→ Different losses → different optimal actions!")
print("=" * 70)
```

### 2.2. Ví dụ Session 6: MAP detection nhị phân

Giả sử ta cần quyết định giữa hai trạng thái $$H_0$$ (an toàn) và $$H_1$$ (sự cố), với quan sát nhiễu $$x$$. Quy tắc MAP:

$$
\text{chọn }H_1 \text{ nếu } p(H_1\mid x)>p(H_0\mid x)
\iff p(x\mid H_1)P(H_1)>p(x\mid H_0)P(H_0).
$$

Ví dụ số:

- $$P(H_1)=0.2,\;P(H_0)=0.8$$
- $$p(x\mid H_1)=0.30,\;p(x\mid H_0)=0.05$$

So sánh:

$$
0.30\times0.2=0.06 \;>\; 0.05\times0.8=0.04.
$$

Nên MAP chọn $$H_1$$. Đây là dạng quyết định nhị phân xuất hiện trong phát hiện tín hiệu/cảnh báo lỗi.

### 2.3. Ví dụ Session 6: quyết định cảnh báo với chi phí bất đối xứng

Xét hai hành động: cảnh báo ($$a_1$$) hoặc không cảnh báo ($$a_0$$). Gọi $$q=P(H_1\mid x)$$ là xác suất hậu nghiệm có sự cố.

Loss:

- Báo động giả (chọn $$a_1$$ khi $$H_0$$ đúng): $$L_{FP}=5$$
- Bỏ sót sự cố (chọn $$a_0$$ khi $$H_1$$ đúng): $$L_{FN}=40$$

Expected loss:

$$
R(a_1\mid x)=L_{FP}(1-q),\qquad R(a_0\mid x)=L_{FN}q.
$$

Chọn cảnh báo khi $$R(a_1\mid x)<R(a_0\mid x)$$, tương đương:

$$
q>\frac{L_{FP}}{L_{FP}+L_{FN}}=\frac{5}{45}\approx 0.111.
$$

Nghĩa là chỉ cần posterior vượt 11.1% đã nên cảnh báo, vì chi phí bỏ sót lớn hơn nhiều chi phí báo động giả.

### 2.4. Cầu nối với prior hỗn hợp từ Chapter 2

Nếu prior là hỗn hợp kịch bản $$M_k$$:

$$
p(\theta)=\sum_k w_k p_k(\theta),
$$

thì sau dữ liệu:

$$
p(\theta\mid D)=\sum_k \tilde w_k p_k(\theta\mid D),
\quad
\tilde w_k\propto w_k p(D\mid M_k).
$$

Các trọng số hậu nghiệm $$\tilde w_k$$ chính là đầu vào cho expected loss ở bước quyết định. Tức là dữ liệu không chỉ cập nhật tham số mà còn cập nhật "độ tin" vào từng kịch bản prior.

## 3. Bayesian hypothesis testing và Bayes factor

### 3.1. Bayes factor là gì?

Với hai giả thuyết $$H_0$$ và $$H_1$$:

$$
BF_{10}=\frac{p(D\mid H_1)}{p(D\mid H_0)}.
$$

- $$BF_{10}>1$$: dữ liệu nghiêng về $$H_1$$.
- $$BF_{10}<1$$: dữ liệu nghiêng về $$H_0$$.

Kết hợp với prior odds:

$$
\frac{P(H_1\mid D)}{P(H_0\mid D)}=BF_{10}\times\frac{P(H_1)}{P(H_0)}.
$$

### 3.2. One-sided vs two-sided trong Bayes

- **One-sided**: ví dụ $$H_1: \theta>\theta_0$$, $$H_0: \theta\le\theta_0$$.
- **Two-sided**: ví dụ $$H_1: \theta\neq\theta_0$$, $$H_0: \theta=\theta_0$$ (hoặc vùng lân cận thực dụng quanh $$\theta_0$$).

Trong thực hành quyết định, one-sided thường gắn với câu hỏi hành động cụ thể ("có vượt chuẩn tối thiểu không?"). Two-sided phù hợp khi mục tiêu là phát hiện mọi sai khác theo cả hai hướng.

### 3.3. Ví dụ tích hợp: posterior inference + loss + Bayes factor

Giả sử từ phân tích posterior ta có:

- $$P(H_1\mid D)=0.7,\;P(H_0\mid D)=0.3$$
- Bayes factor tính được $$BF_{10}=3$$

Quyết định hành động với loss bất đối xứng như mục 2.3. Nếu $$q=0.7$$ thì:

$$
R(a_1\mid D)=5(1-0.7)=1.5,
\quad
R(a_0\mid D)=40(0.7)=28.
$$

Nên chọn hành động cảnh báo $$a_1$$.

Đây là workflow đầy đủ của Buổi 6: dữ liệu -> posterior/Bayes factor -> expected loss -> hành động.

## 4. Value of Information

**Question**: Should we collect more data before deciding?

**Value of Information (VOI)**: Expected reduction in loss from additional data.

$$
\text{VOI} = \mathbb{E}[\text{Loss without data}] - \mathbb{E}[\text{Loss with data}]
$$

**Decision rule**: Collect data if VOI > Cost of data collection.

```python
# Example: Value of additional test
# Current posterior: P(disease) = 0.7
# Test cost: 20 units

# Expected loss with current information
current_exp_loss = expected_losses.min()

# If we do test, posterior will update
# Simulate: If test positive, P(disease) = 0.95
# If test negative, P(disease) = 0.3

p_positive = 0.6  # P(test positive)
p_negative = 0.4

# Expected loss after test
posterior_if_pos = np.array([0.05, 0.95])
posterior_if_neg = np.array([0.7, 0.3])

exp_loss_if_pos = (loss_matrix.T @ posterior_if_pos).min()
exp_loss_if_neg = (loss_matrix.T @ posterior_if_neg).min()

exp_loss_with_test = (p_positive * exp_loss_if_pos + 
                      p_negative * exp_loss_if_neg)

# Value of information
test_cost = 20
voi = current_exp_loss - exp_loss_with_test
net_benefit = voi - test_cost

print("\n" + "=" * 70)
print("VALUE OF INFORMATION")
print("=" * 70)
print(f"\nCurrent expected loss: {current_exp_loss:.1f}")
print(f"Expected loss with test: {exp_loss_with_test:.1f}")
print(f"Value of information: {voi:.1f}")
print(f"Test cost: {test_cost}")
print(f"Net benefit: {net_benefit:.1f}")

if net_benefit > 0:
    print("\n→ DO the test! (VOI > cost)")
else:
    print("\n→ DON'T do the test (VOI < cost)")
print("=" * 70)
```

## 5. Practical Example: A/B Testing

```python
# A/B test: Which version better?
# Version A: 120/1000 conversions
# Version B: 140/1000 conversions

# Bayesian analysis
with pm.Model() as ab_model:
    # Priors
    p_A = pm.Beta('p_A', 1, 1)
    p_B = pm.Beta('p_B', 1, 1)
    
    # Likelihoods
    y_A = pm.Binomial('y_A', n=1000, p=p_A, observed=120)
    y_B = pm.Binomial('y_B', n=1000, p=p_B, observed=140)
    
    # Sample
    trace = pm.sample(2000, tune=500, chains=2, random_seed=42,
                     return_inferencedata=True, progressbar=False)

# Extract posteriors
p_A_samples = trace.posterior['p_A'].values.flatten()
p_B_samples = trace.posterior['p_B'].values.flatten()

# Decision: Choose B if P(p_B > p_A) > threshold
prob_B_better = np.mean(p_B_samples > p_A_samples)

# Loss function: Cost of wrong choice
# If choose A but B better: lose (p_B - p_A) * future_users
# If choose B but A better: lose (p_A - p_B) * future_users

future_users = 100000
expected_gain_B = future_users * (p_B_samples - p_A_samples).mean()

print("\n" + "=" * 70)
print("A/B TESTING DECISION")
print("=" * 70)
print(f"\nP(B better than A): {prob_B_better:.3f}")
print(f"Expected gain from choosing B: {expected_gain_B:.0f} conversions")

if prob_B_better > 0.95:
    print("\n→ Choose B (high confidence)")
elif prob_B_better < 0.05:
    print("\n→ Choose A")
else:
    print("\n→ Uncertain! Consider collecting more data")
print("=" * 70)
```

## Tóm tắt

Bayesian Decision Analysis:

- **Framework**: Actions + States + Loss function + Posterior
- **Optimal action**: Minimize expected loss
- **Bayes testing**: One-sided/two-sided framing + Bayes factor as evidence ratio
- **Loss functions**: Squared, absolute, 0-1, custom
- **Value of Information**: Should we collect more data?
- **Applications**: MAP detection, alarm decisions with asymmetric costs, A/B testing, business

**Key insight**: Bayesian inference provides beliefs (posteriors). Decision theory tells us what to do with those beliefs!

**Chapter 08 Complete!** PPC, Information Criteria, Model Comparison, Decision Analysis.

## Bài tập

**Bài tập 1**: Define custom loss function. Compute optimal action.

**Bài tập 2**: Medical decision với different loss matrices. How does optimal action change?

**Bài tập 3**: Compute VOI for additional data. When is it worth collecting?

**Bài tập 4**: A/B testing. Compute expected gain. Make decision.

**Bài tập 5**: Real business problem. Define losses. Use Bayesian decision theory.

## Tài liệu Tham khảo

**Berger, J. O. (1985).** *Statistical Decision Theory and Bayesian Analysis* (2nd Edition). Springer.

**Gelman, A., et al. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 9: Decision analysis

---

*Chương tiếp theo: [Chapter 12: Labs Thực Hành Bayesian](/vi/chapter12/)*
