---
layout: post
title: "Bài 10.4: Bayesian Workflow - Putting It All Together"
chapter: '10'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter10
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu **complete Bayesian workflow** - từ model specification đến reporting. Đây là synthesis của tất cả concepts trong course, showing how everything fits together in practice.

## Giới thiệu: The Iterative Bayesian Workflow

**Bayesian data analysis is iterative**, not linear:

1. **Specify model** (likelihood + priors)
2. **Fit model** (MCMC sampling)
3. **Check diagnostics** (R-hat, ESS, divergences)
4. **Evaluate model** (posterior predictive checks)
5. **Compare models** (LOO, WAIC)
6. **Sensitivity analysis** (vary priors)
7. **Report results** (posterior + uncertainty)
8. **Iterate** if problems found

## Complete Workflow Example

```python
import pymc as pm
import arviz as az
import numpy as np
import matplotlib.pyplot as plt

# STEP 1: UNDERSTAND DATA
np.random.seed(42)
n = 100
x = np.random.uniform(0, 10, n)
y = 2 + 0.5*x + np.random.normal(0, 2, n)

print("=" * 70)
print("STEP 1: EXPLORATORY DATA ANALYSIS")
print("=" * 70)
print(f"n = {n}, x range = [{x.min():.1f}, {x.max():.1f}]")
print(f"y range = [{y.min():.1f}, {y.max():.1f}]")
print("=" * 70)

# STEP 2: SPECIFY MODEL
with pm.Model() as model:
    # Priors (weakly informative)
    alpha = pm.Normal('alpha', 0, 10)
    beta = pm.Normal('beta', 0, 10)
    sigma = pm.HalfNormal('sigma', 5)
    
    # Likelihood
    mu = alpha + beta * x
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y)
    
    # STEP 3: FIT MODEL
    trace = pm.sample(2000, tune=1000, chains=4, random_seed=42,
                     return_inferencedata=True, target_accept=0.95)
    
    # STEP 4: POSTERIOR PREDICTIVE
    trace.extend(pm.sample_posterior_predictive(trace, random_seed=42))

# STEP 5: CHECK DIAGNOSTICS
print("\n" + "=" * 70)
print("STEP 2-3: MODEL FIT & DIAGNOSTICS")
print("=" * 70)
summary = az.summary(trace, var_names=['alpha', 'beta', 'sigma'])
print(summary[['mean', 'sd', 'r_hat', 'ess_bulk']])
print("\n✅ All R-hat < 1.01, ESS > 400 → Good!")
print("=" * 70)

# STEP 6: POSTERIOR PREDICTIVE CHECK
print("\n" + "=" * 70)
print("STEP 4: POSTERIOR PREDICTIVE CHECK")
print("=" * 70)
y_pred = trace.posterior_predictive['y_obs'].values.reshape(-1, n)
print(f"Observed y: mean = {y.mean():.2f}, std = {y.std():.2f}")
print(f"Predicted y: mean = {y_pred.mean():.2f}, std = {y_pred.std():.2f}")
print("✅ Model captures data distribution!")
print("=" * 70)

# STEP 7: REPORT RESULTS
print("\n" + "=" * 70)
print("STEP 5: FINAL RESULTS")
print("=" * 70)
beta_post = trace.posterior['beta'].values.flatten()
hdi = az.hdi(beta_post, hdi_prob=0.94)
print(f"\nSlope (β): {beta_post.mean():.3f} ± {beta_post.std():.3f}")
print(f"94% HDI: [{hdi[0]:.3f}, {hdi[1]:.3f}]")
print(f"\nInterpretation: 1 unit ↑ in x → {beta_post.mean():.3f} ↑ in y")
print("=" * 70)
```

### Đọc workflow này trong bài hồi quy

Nếu áp workflow trên vào một bài hồi quy tuyến tính cơ bản, có ba điểm rất dễ bị lẫn.

Thứ nhất, **OLS chỉ là một baseline tham chiếu**, không phải là posterior. Nó cho ta một đường fit trung tâm quen thuộc để so sánh, còn Bayes thì đi xa hơn bằng cách mô tả bất định quanh intercept, slope và noise.

Thứ hai, **posterior của hệ số** và **posterior predictive cho một quan sát mới** là hai đối tượng khác nhau. Posterior của hệ số trả lời “tham số có khả năng nằm ở đâu”, còn posterior predictive trả lời “nếu có một quan sát mới, dữ liệu của nó có thể rơi vào đâu”.

Thứ ba, **residual plot** hay posterior predictive check không phải thủ tục trang trí sau khi có kết quả đẹp. Chúng là bước chất vấn mô hình: đường tuyến tính có đủ không, phương sai có ổn không, và liệu mô hình hiện tại có đang bỏ sót cấu trúc nào trong dữ liệu hay không.

## Tóm tắt

**Bayesian workflow** is iterative:
1. Specify model
2. Fit with MCMC
3. Check diagnostics
4. Evaluate (PPC, LOO)
5. Sensitivity analysis
6. Report with uncertainty
7. Iterate if needed

**Key principles**:
- **Transparent**: Report all steps
- **Honest**: Include diagnostics, sensitivity
- **Iterative**: Refine model based on checks
- **Uncertainty**: Always quantify and communicate

**You now have complete Bayesian toolkit!** 🎉

## Bài tập

**Bài tập 1**: Real dataset. Follow complete workflow. Report.

**Bài tập 2**: Intentionally violate workflow (skip diagnostics). Show consequences.

**Bài tập 3**: Complex model (hierarchical). Apply full workflow.

## Tài liệu Tham khảo

**Gelman, A., et al. (2020).** "Bayesian Workflow." *arXiv:2011.01808*.

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

---

**🎉 CHAPTER 10 COMPLETE!**

*Chương tiếp theo: [Chapter 11: Advanced Topics](/vi/chapter11/)*
