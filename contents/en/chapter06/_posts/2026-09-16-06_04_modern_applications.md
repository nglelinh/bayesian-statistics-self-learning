---
layout: post
title: "Lesson 6.4: Modern Applications of Bayesian GLMs"
chapter: '06'
order: 4
owner: Nguyen Le Linh
lang: en
categories:
- chapter06
lesson_type: optional
---

Why do premier football analytics desks, insurance actuaries, and tech ad-auction teams still bet billions of dollars on **Bayesian Generalized Linear Models (GLMs)** in the era of giant Transformers? Because when you need **calibrated probabilities, interpretable risk factors, and hierarchical partial pooling across thousands of sparse entities** (like pricing insurance for a rare car model or predicting goals for a newly promoted club), hierarchical Bayesian GLMs remain unbeatable!

This optional bridge connects Chapter 6’s Logistic and Poisson GLMs to real-world systems in 2022–2026: click-through-rate (CTR) ad auctions, insurance claim frequency/severity modeling, and hierarchical sports rating models.

---

## Background Knowledge Map: Three High-Stakes Production Uses of Bayesian GLMs

1. **Ad-Auction CTR & Conversion Modeling (Logistic GLMs):** Expected value of showing an ad is $$\text{bid} \times P(\text{click}\mid x)$$; calibrated Bayesian posteriors directly power Thompson Sampling and risk-aware bidding.
2. **Actuarial Pricing (Poisson Frequency $$\times$$ Gamma Severity):** Insurance models separate *how many claims* (Poisson/NegBin GLM with exposure offset) from *how costly each claim is* (Gamma/Log-Normal GLM)—requiring full regulatory interpretability.
3. **Hierarchical Sports & Ranking Models (Baio–Blangiardo Poisson GLM):** Models goals scored as $$\ln\lambda_{ij} = \text{home} + \text{attack}_i - \text{defense}_j$$ with hierarchical priors shrinking small-sample teams smoothly toward the league average!

---

## Learning objectives

After this optional lesson, you can choose a Bayesian GLM because of the *generative story of the outcome*, not out of the habit of calling every problem a linear regression. You will recognize logistic, Poisson, and neighboring families running in credit, epidemiology, and marketing measurement, and know that the posterior of a probability or a count intensity must be read together with the decision cost.

## Prerequisites

Lessons 6.1–6.3 built logistic, Poisson, and GLM evaluation. This lesson does not rewrite the link function. It only connects the same models with 2022–2026 systems.

## Introduction

Chapter 6 was born because the Gaussian assumption of Chapter 4 cannot withstand binary outcomes and counts. In products, that intolerance shows up immediately: a transaction defaults or not, the number of orders in an hour, the number of cases reported late. If we still optimize least squares, we are telling a generative story that the data could never have lived. The tension of this lesson is to choose the right observation family before discussing deep networks or feature stores.

## Conceptual development

A Bayesian GLM keeps a linear structure on a suitable scale,

$$
g(\mathbb E[y_i\mid x_i])=x_i^\top\beta,
$$

then places a prior on $$\beta$$ and takes the posterior. For logistic, $$g$$ is the logit and $$y$$ is Bernoulli. For Poisson, $$g$$ is the log and $$y$$ is a count. The posterior does not return a “predicted class”; it returns a distribution over the probability or over the intensity. A classification threshold appears only later, when a loss function says clearly how much more expensive a false positive is than a false negative.

## Models as generative stories

### 1. Bayesian logistic for credit, fraud, and clinical risk

The generative story: each record has a probability of a rare event, $$\theta(x)=\mathrm{logit}^{-1}(x^\top\beta)$$, and then the label is tossed like a biased coin. The prior on $$\beta$$ keeps the probability from being pushed to 0 or 1 when a combination of features has never appeared—exactly the spirit of regularization that will be emphasized in Chapter 7. What industry needs from the posterior is not maximum accuracy, but a calibrated probability for setting limits, insurance, or approval thresholds. Grinsztajn, Oyallon and Varoquux (2022) show that on many heterogeneous tables, “shallow” models still beat deep networks; a well-specified Bayesian logistic is therefore not a step backward.

### 2. Poisson and Negative Binomial for demand and nowcasting

The number of orders, calls, or cases per day is a count. The Poisson story says that the variance equals the mean; in epidemiology and commerce, reality often requires the Negative Binomial when there is overdispersion. In a pandemic, nowcasting must both estimate the intensity and correct the reporting delay. Hierarchical Bayes over geographic groups is the Chapter 6 GLM written as many intercepts. The posterior predictive of next week is not a point; it is a fan of uncertainty that warehouses and hospitals must pay for.

### 3. Media mix modeling as a causal GLM with priors

Google Meridian (2024) is a Bayesian marketing-mix framework: sales are told as a function of media channels transformed by adstock and diminishing returns, plus non-media factors, with priors that can be calibrated by experiments. Inference uses MCMC/NUTS. The likelihood is close to regression, but the spirit is a GLM opened up to nonlinear transformations of exposure. The Meridian documentation emphasizes that the goal is causal inference about ROI, not minimizing hold-out prediction error—a direct warning from Chapters 5 and 6: the same model family serves two different questions.

### 4. GLM evaluation: calibration before hard labels

Lesson 6.3 already warned that the confusion matrix is not cost-neutral. In credit, missing a default is more expensive than a wrong rejection. In epidemiology, missing a cluster is more expensive than an extra alert. Therefore the posterior of $$\theta(x)$$ must be checked with a reliability diagram, not only with accuracy. A “less sharp” GLM that is straight on the calibration plot can still be the right decision model.

## Interpretation and insight

A logistic coefficient is a change in log-odds, not a constant change in probability. A Poisson coefficient is a change in log-intensity. A posterior interval on media ROI has pooled the uncertainty of the adstock, of the confounder, and of the sampler. No interval becomes a decision until the loss is written.

## Applications

Credit approval, fraud detection, demand forecasting, nowcasting, and advertising budget allocation are four places where Bayesian GLMs are already infrastructure, not textbook examples.

## Limitations and extensions

Meridian warns that a good hold-out does not prove that the media effect is right. Poisson will break with zero-inflation. A linear logistic does not capture deep interactions unless you write them out. Chapter 7 will ask which prior keeps a GLM from overfitting as the number of columns grows.

---

### Worked Numerical Example: Partial Pooling in a Bayesian Poisson Sports/CTR Model

Suppose the league average scoring rate is **1.40 goals/game** (prior $$\mathrm{Gamma}(\alpha=7,\; \beta=5)$$, equivalent to 5 pseudo-games). A newly promoted team scores **4 goals in its very first match** ($$n = 1$$):
- **Unpooled MLE:** $$\hat{\lambda}_{\text{MLE}} = 4 / 1 = \mathbf{4.00}$$ goals/game (absurdly predicting a 152-goal season!).
- **Bayesian Conjugate Posterior:** $$\mathrm{Gamma}(7 + 4,\; 5 + 1) = \mathrm{Gamma}(11,\; 6) \implies \hat{\lambda}_{\text{post}} = \frac{11}{6} \approx \mathbf{1.83}$$ goals/game!
  The Bayesian GLM gives genuine credit for the strong opener (lifting the team from $$1.40 \to 1.83$$) while refusing to overreact to a 1-game fluke!

### Deep-Dive Explanation: Four Reasons Bayesian GLMs Still Thrive Alongside Deep Learning (Read Slowly)

1. **Tabular & sparse-group data favors structured hierarchical priors:** Deep nets struggle with 500 small groups of 3 rows each; hierarchical GLMs borrow strength across groups automatically.
2. **Auditability and regulatory compliance:** Insurance, healthcare, and credit teams must explain *why* a rate changed—log-odds and rate ratios provide transparent audits.
3. **Natural handling of exposure, censoring, and domain offsets:** Putting `log(policy_years)` directly in a Poisson GLM encodes domain physics with zero extra parameters.
4. **Hybrid architectures combine both worlds:** Use a neural embedding for text/images and feed it into a calibrated Bayesian GLM head for final uncertainty-aware decisions!

**Quick check.** In the football example above, after the same team plays **20 matches** and scores **40 total goals** (2.00 goals/game), what is its updated $$\mathrm{Gamma}(7+40,\; 5+20)$$ posterior mean—and how close is it now to the raw sample average?

---

## Reference videos

- [Explaining generalized linear models (GLMs) | VNT #15](https://www.youtube.com/watch?v=1fZeBafD1nw) — Very Normal, English. **watch first**. Watch GLMs chosen by the type of outcome variable, exactly the habit the lesson wants in place of calling every problem a linear regression.
- [GLM Intro - 4 - Link Function](https://www.youtube.com/watch?v=J4zNmGqttVo) — Meerkat Statistics, English. Watch the link function connect the mean of the outcome with the linear part, supporting logistic and Poisson in real systems.
- [Statistical Rethinking 2023 - 19 - Generalized Linear Madness](https://www.youtube.com/watch?v=zffwg0xDOgE) — Richard McElreath, English. Watch GLMs pushed beyond the textbook form, used for the part of the lesson on model families close to logistic and Poisson.

## Exercises

1. A default model reaches 98% accuracy because only 2% of records default. The posterior mean of $$\theta(x)$$ in the high-risk group is 0.15. Why is accuracy hiding exactly the subjects that the Bayesian GLM cares about?
2. Write the generative story for the number of orders per hour at a warehouse. When do you move from Poisson to Negative Binomial, and how will the posterior predictive change shape?
3. Meridian advises against taking hold-out prediction as the main criterion. Connect that statement with the difference between prediction and causal inference in Chapter 5.
4. Choose a logistic threshold when a false negative is ten times as expensive as a false positive. Which additional object of the posterior do you need, not only $$\hat\beta$$?

## References

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 16.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 21–22.
- Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why do tree-based models still outperform deep learning on typical tabular data? *NeurIPS*.
- Google. (2024). *Meridian*: Bayesian marketing mix modeling. [Bayesian inference](https://developers.google.com/meridian/docs/causal-inference/bayesian-inference); [GitHub](https://github.com/google/meridian).
- [Stan User’s Guide, GLM chapters](https://mc-stan.org/docs/stan-users-guide/index.html).
- [PyMC GLM examples](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/GLM_linear.html).
