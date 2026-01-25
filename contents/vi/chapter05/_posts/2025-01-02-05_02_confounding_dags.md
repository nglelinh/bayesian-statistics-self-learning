---
layout: post
title: "Bài 5.2: Confounding và DAGs - Causal Inference Basics"
chapter: '05'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter05
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu về **confounding** - một trong những vấn đề quan trọng nhất trong data analysis. Bạn sẽ học cách sử dụng **DAGs (Directed Acyclic Graphs)** để suy nghĩ về causal relationships và quyết định **khi nào nên** và **khi nào không nên** control for variables. Đây là bước đầu quan trọng vào causal inference - một kỹ năng thiết yếu cho data scientists.

## Giới thiệu: Correlation ≠ Causation

Câu nói kinh điển: **"Correlation does not imply causation"**

Nhưng làm sao chúng ta biết khi nào correlation phản ánh causation? Và quan trọng hơn, **khi nào nên control for variables và khi nào không nên**?

Hãy xem một ví dụ gây sốc:

**Quan sát**: Số lượng ice cream bán ra correlate với số vụ đuối nước.

**Kết luận sai**: Ice cream gây đuối nước? Hay đuối nước khiến người ta mua ice cream?

**Sự thật**: Cả hai đều tăng vào mùa hè. **Temperature** là **confounder** - biến ảnh hưởng đến cả hai.

Đây là lý do tại sao chúng ta cần **causal thinking** và **DAGs**.

## 1. Confounding: Vấn đề và Ví dụ

![Confounding và DAGs]({{ site.baseurl }}/img/chapter_img/chapter05/confounding_dags.png)

### 1.1. Simpson's Paradox - Khi Tổng thể và Nhóm Ngược nhau

Một trong những ví dụ kinh điển về confounding là **Simpson's Paradox**.

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns

# Simpson's Paradox: Kidney stone treatment
np.random.seed(42)

# Generate data
n = 50

# Group A (severe cases): High treatment intensity, but worse outcomes
treatment_A = np.random.uniform(7, 10, n)
success_A = 40 + 2*treatment_A + np.random.normal(0, 3, n)

# Group B (mild cases): Low treatment intensity, better outcomes  
treatment_B = np.random.uniform(0, 3, n)
success_B = 80 + 2*treatment_B + np.random.normal(0, 3, n)

# Combine
treatment_all = np.concatenate([treatment_A, treatment_B])
success_all = np.concatenate([success_A, success_B])
severity = np.array(['Severe']*n + ['Mild']*n)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Overall (ignoring severity)
lr_overall = LinearRegression().fit(treatment_all.reshape(-1, 1), success_all)
x_line = np.linspace(0, 10, 100)

axes[0].scatter(treatment_all, success_all, s=80, alpha=0.6, edgecolors='black')
axes[0].plot(x_line, lr_overall.predict(x_line.reshape(-1, 1)), 
            'r-', linewidth=3, label=f'β = {lr_overall.coef_[0]:.2f}')
axes[0].set_xlabel('Treatment Intensity', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
axes[0].set_title('IGNORING Severity\n' +
                 f'β = {lr_overall.coef_[0]:.2f} (NEGATIVE!)\n' +
                 'More treatment → Worse outcome?',
                 fontsize=14, fontweight='bold', color='red')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# By severity group
colors = {'Severe': 'red', 'Mild': 'blue'}
for sev in ['Severe', 'Mild']:
    mask = severity == sev
    axes[1].scatter(treatment_all[mask], success_all[mask], 
                   s=80, alpha=0.6, label=sev, 
                   color=colors[sev], edgecolors='black')
    
    # Fit within group
    lr_group = LinearRegression().fit(
        treatment_all[mask].reshape(-1, 1), 
        success_all[mask]
    )
    axes[1].plot(x_line, lr_group.predict(x_line.reshape(-1, 1)),
                '-', linewidth=2, color=colors[sev],
                label=f'{sev}: β = {lr_group.coef_[0]:.2f}')

axes[1].set_xlabel('Treatment Intensity', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
axes[1].set_title('CONTROLLING for Severity\n' +
                 'β = +2 (POSITIVE!) for both groups\n' +
                 'More treatment → Better outcome!',
                 fontsize=14, fontweight='bold', color='green')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("=" * 70)
print("SIMPSON'S PARADOX")
print("=" * 70)
print("\nIgnoring Severity:")
print(f"  β = {lr_overall.coef_[0]:.2f} (NEGATIVE)")
print("  → More treatment seems BAD!")
print("\nControlling for Severity:")
print(f"  β = +2.00 (POSITIVE) for both groups")
print("  → More treatment is actually GOOD!")
print("\n→ Severity is a CONFOUNDER!")
print("=" * 70)
```

### 1.2. Định nghĩa Confounder

**Confounder** là biến:
1. Ảnh hưởng đến **treatment/predictor** (X)
2. Ảnh hưởng đến **outcome** (Y)
3. Không nằm trên causal path từ X → Y

**Hậu quả**: Nếu không control for confounder, chúng ta sẽ ước lượng sai effect của X lên Y.

## 2. DAGs: Công cụ Suy nghĩ về Causation

**DAG (Directed Acyclic Graph)** là một công cụ đơn giản nhưng mạnh mẽ để visualize causal relationships.

### 2.1. DAG Basics

**Components**:
- **Nodes** (nút): Variables
- **Arrows** (mũi tên): Causal effects
- **Directed**: Arrows có hướng (A → B)
- **Acyclic**: Không có cycles (A → B → C → A)

```python
# Visualize DAGs
import matplotlib.pyplot as plt
import networkx as nx

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# 1. Simple causation: X → Y
G1 = nx.DiGraph()
G1.add_edge('X', 'Y')
pos1 = {'X': (0, 0), 'Y': (1, 0)}
axes[0, 0].set_title('Simple Causation\nX → Y', fontsize=13, fontweight='bold')
nx.draw(G1, pos1, ax=axes[0, 0], with_labels=True, node_size=2000,
        node_color='lightblue', font_size=14, font_weight='bold',
        arrows=True, arrowsize=20, arrowstyle='->')
axes[0, 0].text(0.5, -0.3, 'X causes Y\nNo confounding',
               ha='center', fontsize=11, transform=axes[0, 0].transAxes)

# 2. Confounding: Z → X, Z → Y
G2 = nx.DiGraph()
G2.add_edges_from([('Z', 'X'), ('Z', 'Y')])
pos2 = {'Z': (0.5, 1), 'X': (0, 0), 'Y': (1, 0)}
axes[0, 1].set_title('Confounding\nZ → X, Z → Y', fontsize=13, fontweight='bold')
nx.draw(G2, pos2, ax=axes[0, 1], with_labels=True, node_size=2000,
        node_color='lightcoral', font_size=14, font_weight='bold',
        arrows=True, arrowsize=20, arrowstyle='->')
axes[0, 1].text(0.5, -0.3, 'Z confounds X-Y relationship\nMUST control for Z',
               ha='center', fontsize=11, transform=axes[0, 1].transAxes)

# 3. Mediation: X → M → Y
G3 = nx.DiGraph()
G3.add_edges_from([('X', 'M'), ('M', 'Y')])
pos3 = {'X': (0, 0), 'M': (0.5, 0), 'Y': (1, 0)}
axes[0, 2].set_title('Mediation\nX → M → Y', fontsize=13, fontweight='bold')
nx.draw(G3, pos3, ax=axes[0, 2], with_labels=True, node_size=2000,
        node_color='lightgreen', font_size=14, font_weight='bold',
        arrows=True, arrowsize=20, arrowstyle='->')
axes[0, 2].text(0.5, -0.3, 'M is mediator\nDO NOT control for M\n(blocks causal path)',
               ha='center', fontsize=11, transform=axes[0, 2].transAxes)

# 4. Collider: X → C ← Y
G4 = nx.DiGraph()
G4.add_edges_from([('X', 'C'), ('Y', 'C')])
pos4 = {'X': (0, 1), 'Y': (1, 1), 'C': (0.5, 0)}
axes[1, 0].set_title('Collider\nX → C ← Y', fontsize=13, fontweight='bold')
nx.draw(G4, pos4, ax=axes[1, 0], with_labels=True, node_size=2000,
        node_color='lightyellow', font_size=14, font_weight='bold',
        arrows=True, arrowsize=20, arrowstyle='->')
axes[1, 0].text(0.5, -0.3, 'C is collider\nDO NOT control for C\n(creates spurious correlation)',
               ha='center', fontsize=11, transform=axes[1, 0].transAxes)

# 5. Full example: Treatment effect
G5 = nx.DiGraph()
G5.add_edges_from([('Severity', 'Treatment'), ('Severity', 'Outcome'),
                   ('Treatment', 'Outcome')])
pos5 = {'Severity': (0.5, 1), 'Treatment': (0, 0), 'Outcome': (1, 0)}
axes[1, 1].set_title('Simpson\'s Paradox\nSeverity confounds', 
                    fontsize=13, fontweight='bold')
nx.draw(G5, pos5, ax=axes[1, 1], with_labels=True, node_size=2000,
        node_color='lightcoral', font_size=12, font_weight='bold',
        arrows=True, arrowsize=20, arrowstyle='->')
axes[1, 1].text(0.5, -0.3, 'Must control for Severity\nto get true Treatment effect',
               ha='center', fontsize=11, transform=axes[1, 1].transAxes)

# 6. Summary
axes[1, 2].axis('off')
summary = """
╔═══════════════════════════════════════════════╗
║           DAG RULES                           ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  1. CONFOUNDER (Z → X, Z → Y):                ║
║     → MUST control for Z                      ║
║                                               ║
║  2. MEDIATOR (X → M → Y):                     ║
║     → DO NOT control for M                    ║
║     (blocks causal path)                      ║
║                                               ║
║  3. COLLIDER (X → C ← Y):                     ║
║     → DO NOT control for C                    ║
║     (creates spurious correlation)            ║
║                                               ║
║  4. DESCENDANT of collider:                   ║
║     → DO NOT control                          ║
║                                               ║
╚═══════════════════════════════════════════════╝
"""
axes[1, 2].text(0.5, 0.5, summary, fontsize=10, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9))

plt.tight_layout()
plt.show()
```

## 3. Khi nào Control, Khi nào Không?

### 3.1. Quy tắc Quyết định

**CONTROL FOR** (include in regression):
- ✅ **Confounders**: Z → X và Z → Y
- ✅ **Precision variables**: Giảm variance (nếu không phải collider)

**DO NOT CONTROL FOR**:
- ❌ **Mediators**: X → M → Y (blocks causal path)
- ❌ **Colliders**: X → C ← Y (creates spurious correlation)
- ❌ **Descendants of colliders**

### 3.2. Ví dụ Thực tế

```python
# Example: Education → Income
# với Age là confounder

# Generate data
np.random.seed(42)
n = 200

# Age affects both Education and Income
age = np.random.uniform(25, 65, n)
education = 12 + 0.1 * age + np.random.normal(0, 2, n)  # Age → Education
income = 20 + 3 * education + 0.5 * age + np.random.normal(0, 10, n)  # Age → Income, Education → Income

# Standardize
age_z = (age - age.mean()) / age.std()
education_z = (education - education.mean()) / education.std()
income_z = (income - income.mean()) / income.std()

# Model 1: WITHOUT controlling for Age
import pymc as pm
import arviz as az

with pm.Model() as model_no_control:
    alpha = pm.Normal('alpha', 0, 1)
    beta_edu = pm.Normal('beta_edu', 0, 1)
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + beta_edu * education_z
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=income_z)
    
    trace_no = pm.sample(1000, tune=500, chains=2, random_seed=42,
                        return_inferencedata=True, progressbar=False)

# Model 2: WITH controlling for Age
with pm.Model() as model_with_control:
    alpha = pm.Normal('alpha', 0, 1)
    beta_edu = pm.Normal('beta_edu', 0, 1)
    beta_age = pm.Normal('beta_age', 0, 1)
    sigma = pm.HalfNormal('sigma', 1)
    
    mu = alpha + beta_edu * education_z + beta_age * age_z
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=income_z)
    
    trace_with = pm.sample(1000, tune=500, chains=2, random_seed=42,
                          return_inferencedata=True, progressbar=False)

# Compare
print("\n" + "=" * 70)
print("EFFECT OF EDUCATION ON INCOME")
print("=" * 70)

beta_no = trace_no.posterior['beta_edu'].values.flatten()
beta_with = trace_with.posterior['beta_edu'].values.flatten()

print(f"\nWITHOUT controlling for Age:")
print(f"  β_education = {beta_no.mean():.3f} ± {beta_no.std():.3f}")
print(f"  (Biased - includes indirect effect through Age)")

print(f"\nWITH controlling for Age:")
print(f"  β_education = {beta_with.mean():.3f} ± {beta_with.std():.3f}")
print(f"  (Unbiased - direct effect only)")

print(f"\n→ Controlling for confounder gives TRUE causal effect!")
print("=" * 70)
```

## Tóm tắt và Kết nối

Confounding và DAGs là cốt lõi của causal inference:

- **Confounder**: Biến ảnh hưởng đến cả X và Y
- **DAGs**: Công cụ visualize causal relationships
- **Control rules**:
  - ✅ Control for confounders
  - ❌ Don't control for mediators
  - ❌ Don't control for colliders

**Key insight**: Không phải lúc nào cũng nên "control for everything". Phải suy nghĩ về causal structure!

Trong bài tiếp theo, chúng ta sẽ học về **multicollinearity** - vấn đề khi predictors correlate với nhau.

## Bài tập

**Bài tập 1: Draw DAGs**
Vẽ DAGs cho các scenarios:
(a) Smoking → Lung Cancer, với Age là confounder
(b) Exercise → Weight Loss → Health, với Diet là confounder
(c) Identify confounders, mediators, colliders

**Bài tập 2: Simpson's Paradox**
Generate data với Simpson's Paradox.
(a) Show overall negative correlation
(b) Show within-group positive correlation
(c) Explain using DAG

**Bài tập 3: Control or Not?**
Cho DAG: X → Y, Z → X, Z → Y, X → M → Y
(a) Should control for Z? Why?
(b) Should control for M? Why not?
(c) Fit models và compare

**Bài tập 4: Real Example**
Scenario: Study effect of Exercise on Weight.
Variables: Exercise, Weight, Age, Diet, Genetics.
(a) Draw plausible DAG
(b) Which variables to control for?
(c) Explain reasoning

**Bài tập 5: Collider Bias**
(a) Generate data với collider: X → C ← Y, no X-Y correlation
(b) Show that controlling for C creates spurious correlation
(c) Explain why this happens

## Tài liệu Tham khảo

### Primary References:

**Pearl, J. (2009).** *Causality: Models, Reasoning, and Inference* (2nd Edition). Cambridge University Press.
- The definitive book on causal inference

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.
- Chapter 6: The Haunted DAG & The Causal Terror

**Hernán, M. A., & Robins, J. M. (2020).** *Causal Inference: What If*. Chapman & Hall/CRC.
- Free online: https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/

---

*Bài học tiếp theo: [5.3 Multicollinearity](/vi/chapter05/multicollinearity/)*
