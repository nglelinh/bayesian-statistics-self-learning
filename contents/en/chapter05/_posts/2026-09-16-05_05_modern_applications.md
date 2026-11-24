---
layout: post
title: "Lesson 5.5: Modern Applications of Multiple Regression and Causal Thinking"
chapter: '05'
order: 5
owner: Nguyen Le Linh
lang: en
categories:
- chapter05
lesson_type: optional
---

When a streaming service launches a $20 million Super Bowl ad campaign, they can’t run a clean user-level A/B test—everybody in the broadcast region sees the ad! How do modern tech and economics teams measure the true causal lift without a randomized trial? They combine Chapter 5’s **Bayesian multiple regression + DAG causal thinking** into **Bayesian Structural Time Series (`CausalImpact`)**, **Geo-Lift Difference-in-Differences**, and **Uplift Modeling**—delivering full posterior distributions over incremental revenue!

This optional bridge shows how causal DAGs and Bayesian regression power real-world industry decisions in 2022–2026.

---

## Background Knowledge Map: Three Production Causal-Bayesian Frameworks

1. **Bayesian Difference-in-Differences & Geo-Lift:** Compares a treated city’s pre-to-post jump against a synthetic control of untreated cities, yielding $$P(\text{ROI} > 1 \mid \text{data})$$ directly.
2. **Bayesian Structural Time Series (CausalImpact):** Predicts the counterfactual trajectory *"what sales would have been without the campaign"* using correlated control markets, then subtracts counterfactual draws from observed sales to get a full posterior over cumulative lift!
3. **Heterogeneous Treatment Effects (Interactions / Uplift):** Models `outcome ~ treatment * user_segment` with shrinkage priors to identify *which* customers actually respond positively vs. which ones are unaffected or annoyed.

---

## Learning objectives

After this optional lesson, you can read a coefficient in a multi-predictor model as a conditional causal claim, not as a coefficient that is “more important” just because the software printed it. You will see that confounding, multicollinearity and interactions are not regression bugs, but the shape of product data: A/B tests on marketplaces, recommender systems, and medical records over time.

## Prerequisites

Lessons 5.1–5.4 laid out multiple regression, DAGs, multicollinearity and interactions. This lesson does not redraw the definition of the back-door. It only brings those same diagrams into 2022–2026 papers and systems.

## Introduction

Chapter 5 begins with a familiar disappointment: adding variables raises $$R^2$$, but the story about “impact” falls apart. In applied computer science, that disappointment is more expensive. A platform can add hundreds of features to a ranking model and then claim to have “controlled for everything”. If one of those features is a mediator or a collider, the coefficient of the treatment is no longer the effect we want. The tension of this lesson is: the more columns the data has, the more a DAG is needed, not the less.

## Conceptual development

A coefficient $$\beta_j$$ in

$$
y_i=\alpha+\sum_j\beta_j x_{ij}+\varepsilon_i
$$

has a causal meaning only after the set of controls has blocked the back-door paths and has not opened new ones. Cinelli, Forney and Pearl (2022) name exactly this problem good and bad controls: not every “related” covariate should enter the equation. Interaction says something else, namely that $$\beta_j$$ itself can be a function of another variable. Multicollinearity is not causal bias; it is posterior uncertainty swelling when the columns tell the same story.

## Models as generative stories

### 1. Good and bad controls in product experiments

The generative story of an A/B test on a marketplace often comes with built-in confounding: users are active, supply and demand move together, and an intervention on one side changes the other side. Adding the variable “number of clicks after seeing the variant” can be a bad control if the click lies on the path from treatment to revenue. Cinelli et al. (2022) give a catalog of small DAGs where the intuition “the more you control, the cleaner” fails. An honest experimentation team draws the DAG before opening the feature store, and only then asks which variables the Bayesian regression should condition on.

### 2. Learning DAGs and the limits of optimization

Bello, Aragam and Ravikumar (2022) reduce DAG learning to a log-det acyclicity characterization on an M-matrix, then optimize continuously (DAGMA). This is a clear computer science development: instead of assuming the graph, we try to learn it. But the generative story still needs assumptions—usually an additive structural equation model with independent noise. A DAG learned from click logs is not automatically the business DAG. The multiple regression of Chapter 5 still needs an analyst who takes responsibility for the unobserved arrows.

### 3. Causal transformers for outcomes over time

Melnychuk, Frauen and Feuerriegel (2022) build the Causal Transformer to estimate counterfactual outcomes on longitudinal data, for example treatment protocols in MIMIC. The generative story is: covariates over time, treatment, and outcome depend on one another over a long horizon; confounding changes over time. The transformer architecture does not remove confounding. It tries to learn a representation that predicts the outcome but does *not* predict the current treatment assignment, through an adversarial loss. This is the deep learning version of the same Chapter 5 idea: to make the treatment's $$\beta$$ readable, you must block the confounding path, not add layers to the network.

### 4. Interactions and multicollinearity in personalization

A recommender that writes “the effect of a discount depends on how new the user is” is exactly an interaction. Two nearly collinear embeddings will give a wide posterior on each coefficient even though the forecast is still good—exactly the phenomenon of Lesson 5.3. In products, this means: do not interpret each embedding coordinate as a mechanism; interpret the predictions and the named interactions.

## Interpretation and insight

A narrow posterior interval on $$\beta_{\text{treatment}}$$ after stuffing in twenty controls is not causal evidence. It may be a bad control that has blocked the path or a collider that has opened a path. Conversely, a wide interval after conditioning on exactly the minimal set can still be an honest estimate. Chapter 5 teaches the right order: DAG first, narrowness second.

## Applications

Marketplace experiments, controlled ranking, personalized treatment, and embedding interpretation are all multiple regression plus a causal question. Bayes adds something that OLS often hides: the uncertainty that remains after the structure has been declared.

## Limitations and extensions

Learning a DAG from observations does not solve non-identifiability when assumptions are missing. The Causal Transformer needs assumptions about temporal ordering and about the ability to balance the representation. This lesson does not replace a course on causal inference. Chapter 6 will change the likelihood family when $$y$$ is no longer Gaussian, but the confounding problem still follows.

---

### Worked Numerical Example: Bayesian Geo-Lift Difference-in-Differences Calculation

A retailer runs a TV campaign in **City A (Treated)** while holding **City B (Control)** unchanged. Weekly sales ($K):

| Region | Pre-Campaign Avg | Post-Campaign Avg | Pre $$\to$$ Post Change |
| :--- | :--- | :--- | :--- |
| **City A (Treated)** | $$100$$ | $$114$$ | $$+14$$ |
| **City B (Control)** | $$100$$ | $$104$$ | $$+4$$ (seasonal trend!) |

1. **Naive before/after estimate (WRONG — confounded by seasonality!):** $$114 - 100 = +14\text{K}$$.
2. **Difference-in-Differences causal lift:** $$(114 - 100) - (104 - 100) = \mathbf{+10\text{K}}$$!
3. **Bayesian decision check:** Suppose the posterior for causal lift is $$\Delta \sim \mathcal{N}(+10\text{K},\; 3\text{K}^2)$$ and the campaign cost $$C = \$7\text{K}$$. Then the posterior probability the campaign was profitable is $$P(\Delta > 7) = P(Z > -1.0) \approx \mathbf{84.1\%}$$!

### Deep-Dive Explanation: Four Rules for Applied Causal Bayes in Industry (Read Slowly)

1. **Always check the parallel-trends assumption before trusting DiD:** Verify that Treatment and Control tracked closely *before* launch; if they were already diverging, your counterfactual is biased.
2. **Separate marketing spend *correlation* from incremental *causality*:** Ad platforms naturally target users who were already about to buy (confounding!); geo-experiments break that confounding cleanly.
3. **Report probability of beating the break-even cost, not just `lift > 0`:** A +$2K lift that costs $7K to run is a losing campaign even if $$P(\text{lift} > 0) = 99\%$$!
4. **Use regularizing priors on segment interactions:** Without shrinkage, slicing a geo-lift test into 20 regions will always make 2 lucky regions look like "miracle markets."

**Quick check.** In the Geo-Lift example above, if the campaign cost were **$$\$10\text{K}$$** (equal to the posterior mean lift), what is $$P(\Delta > 10\text{K})$$?

---

## Reference videos

- [A Crash Course in Good and Bad Controls with Carlos Cinelli](https://www.youtube.com/watch?v=IFgHw_E521U) — Spark: a centre for social research innovation, English. **watch first**. Watch a short course on good and bad controls, exactly how the lesson reads a coefficient as a conditional causal claim.
- [Statistical Rethinking 2023 - 06 - Good & Bad Controls](https://www.youtube.com/watch?v=uanZZLlzKHw) — Richard McElreath, English. Watch the good and bad control graphs, supporting the part that says confounding is not a bug of regression software.
- [Causality: Closing Back Doors](https://www.youtube.com/watch?v=IajzIKW518M) — Econometrics, Causality, and Coding with Dr. HK, English. Watch closing backdoors on a DAG, used where the lesson connects multicollinearity and interactions with the causal question.

## Exercises

1. Draw a three-node DAG for “ad display → click → purchase”. If the goal is the effect of display on purchase, is conditioning on click in the regression a good or bad control, and why?
2. A personalization model has two features correlated at 0.97. The hold-out forecast is good but the two coefficients flip sign when you drop one percent of the data. Which coefficient would you interpret, if any?
3. The Causal Transformer minimizes the ability to predict treatment from the representation. Which confounding of Lesson 5.2 is that aiming at?
4. DAGMA returns a graph from a product log. List two arrows that you do *not* allow the model to draw by itself unless there is domain knowledge.

## References

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 5, 14.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 18.
- Cinelli, C., Forney, A., & Pearl, J. (2022). A crash course in good and bad controls. *Sociological Methods & Research*. [doi:10.1177/00491241221099552](https://doi.org/10.1177/00491241221099552).
- Bello, K., Aragam, B., & Ravikumar, P. (2022). DAGMA: Learning DAGs via M-matrices and a log-determinant acyclicity characterization. *NeurIPS*. [arXiv:2209.08011](https://arxiv.org/abs/2209.08011).
- Melnychuk, V., Frauen, D., & Feuerriegel, S. (2022). Causal Transformer for estimating counterfactual outcomes. *ICML*. [arXiv:2204.07258](https://arxiv.org/abs/2204.07258).
