---
layout: post
title: "Lesson 5.3: Multicollinearity - When Predictors Are Correlated"
chapter: '05'
order: 3
owner: Nguyen Le Linh
lang: en
categories:
- chapter05
lesson_type: required
---

Try predicting a person’s height from **both** their left leg length and their right leg length in the same regression. Individually, each leg is an extraordinary predictor of height (slope $$\approx 2.0$$). Put *both* legs into the same model, and suddenly the posterior intervals for both slopes explode to `[-3.0, +7.0]`—making it look as if *neither* leg predicts height! Nothing is broken in Bayes’ theorem; the model is honestly telling you: **because left and right legs are 99% correlated, infinitely many pairs $$(\beta_L, \beta_R)$$ with $$\beta_L + \beta_R \approx 2.0$$ explain the data equally well!**

This lesson demystifies **multicollinearity** from a Bayesian perspective: why predictions stay accurate while individual slopes become non-identifiable, how posterior pair plots reveal the exact diagonal ridge, and how weakly informative priors stabilize inference.

---

## Background Knowledge Map: Non-Identifiability Ridges Under Multicollinearity

1. **The Posterior Ridge Geometry:** When $$X_1 \approx X_2$$, the linear predictor $$\beta_1 X_1 + \beta_2 X_2 \approx (\beta_1 + \beta_2)X_1$$ depends only on the **sum** $$\beta_1 + \beta_2$$. The joint posterior stretches into a long, narrow diagonal ridge with strong negative correlation $$\rho(\beta_1, \beta_2) \approx -0.99$$!
2. **Individual Slopes Fail, Predictions Succeed:** Even when marginal CIs for $$\beta_1$$ and $$\beta_2$$ look wildly uncertain, their sum $$\beta_1 + \beta_2$$—and therefore out-of-sample predictions $$\hat{y}$$—remain razor-sharp!
3. **Weakly Informative Priors Break Exact Flatness:** While OLS explodes to $$\pm\infty$$ under perfect collinearity, a Bayesian prior $$\beta_j \sim \mathcal{N}(0, 1)$$ smoothly anchors the ridge around balanced weights $$(\beta_1 \approx \beta_2 \approx 1.0)$$.
4. **Detection (VIF & Posterior Pair Plots):** Variance Inflation Factor $$\mathrm{VIF}_j = \frac{1}{1 - R_j^2}$$ and inspecting `az.plot_pair` immediately expose collinear parameter pairs.

---

## Learning objectives

After this lesson, you need to understand what multicollinearity is, why it makes interpreting coefficients difficult, and when it is truly worrying. You also need to clearly distinguish two different goals of regression: **prediction** and **interpretation**.

> **Mini example.** You predict house prices using floor area and the number of bedrooms. These two variables usually go together: larger houses usually also have more rooms. The model can then predict price quite well, but becomes awkward when it must answer exactly "holding everything else fixed, how much does one more bedroom raise the price?".
>
> **Quick check.** If two predictors measure nearly the same thing, what difficulty will the model have in separating the effect of each variable?

## 1. What is multicollinearity?

Multicollinearity occurs when two or more predictors in the same model are highly correlated with each other. Put more simply, they usually move together, carry substantially overlapping information, and so the model has difficulty knowing which variable to "give credit" to. Very typical examples are height in centimeters and height in inches, house area and number of bedrooms in an apartment complex with fairly similar designs, or study hours and the number of completed assignments in a highly disciplined class.

The problem is not wrong data. The problem is that the predictors are too similar in terms of information.

The three views below summarize the most basic intuition of multicollinearity.

![Very high correlation between two predictors]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_multicollinearity_predictor_correlation.png)

![Both predictors are strongly related to the outcome]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_multicollinearity_both_predict_y.png)

![Summary of why multicollinearity makes interpretation hard]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_multicollinearity_problem_summary.png)

The figures above show a very typical situation: both predictors are related to the outcome, but they are also so similar that the model has difficulty separating who contributes how much.

## 2. Why does multicollinearity make coefficients hard to read?

Let us return to the principle of multiple regression:

> each coefficient is understood as the effect of one variable when the other variables are held fixed.

The problem is that if two variables usually rise and fall together, the condition "hold the other variable fixed" becomes rather foreign to the real data.

### Example: floor area and number of bedrooms

In practice, a house with a large area usually has more bedrooms, while a small house usually has fewer bedrooms.

If we ask:

> between two houses with the same area but differing by 1 bedroom, how much does the price differ?

that is a reasonable question. But if your data rarely contains such pairs of houses, the model will not have much information to answer with confidence.

The result is usually wider credible intervals for the coefficients, coefficient signs that can unexpectedly flip, and coefficients that become very sensitive to adding or removing just a few observations.

The comparison below shows the difference between a context with weakly correlated predictors and one with nearly duplicated predictors.

![Case where predictors are only slightly correlated]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_low_predictor_correlation.png)

![Case where predictors are very highly correlated]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_high_predictor_correlation.png)

![Posterior when predictors are weakly correlated]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_low_correlation_posterior.png)

![Posterior when predictors are highly correlated]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_high_correlation_posterior.png)

### 2.1. A numerical example: the overall model is fine but the individual coefficients are awkward

Suppose we predict house prices using `area` and `number of bedrooms`, and these two variables are very highly correlated, say about $$0.92$$.

If we fit each simple model separately, we may see:

- the model with only `area`: 1 more m² goes with an increase of about **35 million VND**,
- the model with only `number of bedrooms`: 1 more bedroom goes with an increase of about **700 million VND**.

Both results sound reasonable because each variable represents nearly the same package of information about the "size of the house".

But when both are put into the same model, the result may turn into:

- `area`: about **32 million VND/m²** with a fairly stable interval,
- `number of bedrooms`: about **40 million VND/bedroom** but with a very wide interval, for example from **-180** to **260 million**.

Here the model does not necessarily predict badly. What it is saying is: "I still know that bigger houses are usually more expensive, but this data is not enough to clearly separate the individual value of the number of bedrooms once the area has been held fixed".

This is a very typical multicollinearity situation: the overall information about the group of variables is still useful, but splitting the credit among individual variables becomes unstable.

## 3. Signs to recognize it in practice

When working with data, you can suspect multicollinearity if you see predictors that are highly correlated on a scatter plot or in the correlation matrix, if the coefficient of each variable "jumps around" when a new predictor is added, if the intervals of the coefficients are wide even though the overall model still fits fairly well, or if the sign of a coefficient contradicts domain intuition. For instance, in a revenue prediction model, advertising budgets for Facebook and Instagram can be very similar because a company usually raises and lowers them at the same time; the consequence is that the model has difficulty saying which channel is more effective, even though the total advertising budget still predicts revenue well overall.

## 4. Is multicollinearity always bad?

No.

This is a very important point.

### 4.1. If the goal is prediction

If the main goal is prediction, multicollinearity is often not too frightening, because the model can still predict the outcome well, the total information from that group of predictors is still useful, and what you mainly need is accurate forecasting rather than explaining each coefficient individually. For example, a credit risk model can use many fairly similar financial indicators and still give acceptable forecasts.

### 4.2. If the goal is interpretation

If the goal is interpretation, multicollinearity becomes a much bigger problem, because now you really care about which variable is important, how large the individual effect of each variable is, and whether the sign and size of the coefficients are stable. When the predictors overlap too much, all of that interpretive power weakens markedly.

## 5. An everyday example: salary and education

Suppose you want to explain salary using years of schooling, highest degree, and a tested professional skill.

These three variables are quite strongly related to each other.

What can happen is that the overall model still predicts salary fairly well, but it is very hard to say exactly how much the degree alone contributes if skills and years of schooling also rise along with it.

In that case, the more honest answer would be:

> The set of variables on academic and professional background is strongly related to salary, but the current data is not enough to clearly separate the individual contribution of each component.

This is a more mature kind of interpretation than trying to force each coefficient into a "certain truth".

### 5.1. A very common Bayesian sign: posteriors stretched into a diagonal band

If you plot the joint posterior of `years of schooling` and `professional skill score`, you may see that the samples do not form a neat round cloud but a diagonal band sloping downward.

This usually means:

- when the posterior assigns a larger effect to education, it will assign a smaller effect to skill,
- and conversely, many different combinations still explain the data about equally well.

So what should be read first is not only the posterior mean of each coefficient, but also the **dependence structure between the coefficients** in the joint posterior.

## 6. Why are the posteriors of the coefficients often tightly stuck together?

In a Bayesian setting, multicollinearity often shows up in the joint posterior of the coefficients: when one coefficient increases, the other tends to decrease, because many different combinations can still produce nearly the same predictions.

We can imagine the model saying:

> I know the total contribution of this group of variables is quite important, but I am not really sure how to split the credit among the individual variables.

This is why we often see the posterior of the coefficients stretched along a diagonal direction instead of being round and neat.

### Experiment: raise the correlation and the posterior becomes a diagonal band

Raise ρ between the two predictors: sd(b₁) grows with √VIF, b₁ and b₂ are negatively correlated, but the sum b₁ + b₂ stays stable.

<div class="interactive-demo" markdown="1">
<div data-demo="collinear-explainer" data-lang="en"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 7. How should we handle multicollinearity?

There is no single answer for every case. We choose the way to handle it according to the goal of the analysis.

### 7.1. Keep one representative variable

If two variables measure nearly the same thing, sometimes the simplest approach is to keep only one. For example, we can keep area and drop the number of bedrooms if in the current dataset they nearly repeat the same information.

### 7.2. Combine into a composite index

If several variables describe the same concept, we can create a composite score. For example, many variables on household economic conditions can be combined into a socioeconomic index.

### 7.3. Collect more diverse data

This is a very effective approach but often forgotten.

If the data comes from only a too-homogeneous context, predictors will easily go together. Broadening the range of the data can help separate the signals better.

### 7.4. Use a regularizing prior

In Bayesian statistics, a reasonable prior can help stabilize estimation when the data is not strong enough to separate each effect. The later chapters will return to regularization in more detail.

### 7.5. Accept the limits of interpretation

Sometimes the most correct thing is to admit:

> this data is better suited for prediction than for interpreting each coefficient individually.

That is not a failure. It is an honest scientific conclusion.

## 8. A very practical checklist

When you suspect multicollinearity, you can ask yourself a series of very practical questions: is my goal prediction or interpretation, which predictors are overlapping in information, if I drop one variable does predictive ability fall much, if I keep both can I still interpret the coefficients with confidence, and should I combine them into a broader concept.

## 9. What learners often misunderstand

### Misconception 1: "If a coefficient has the wrong sign, the model must be wrong"

Not necessarily. The model may be trying to split credit between predictors that are too similar.

### Misconception 2: "Correlation between predictors is forbidden"

Not true. Real-world data very often has correlated predictors. What matters is understanding the consequences.

### Misconception 3: "Adding variables is always good"

If a new variable only repeats old information, you can make the model harder to interpret without gaining much value.

## 10. Connecting to interaction effects

Multicollinearity asks:

> are the predictors too similar?

Interaction effects in the next lesson ask:

> does the effect of one predictor change with another predictor?

One is a problem of **overlapping information**, the other a problem of **mutual dependence of effects**. Being able to tell these two apart will help you read multiple regression much more accurately.

> **3 key ideas.** Multicollinearity occurs when predictors carry information that is too similar, making it hard for the model to separate the effect of each variable; this is an especially serious problem when the goal is interpreting coefficients, but may be less serious if the goal is only prediction; and the way to handle it always depends on the goal, from dropping variables, combining variables, using a more stabilizing prior, collecting more diverse data, to accepting the limits of interpretation.

---

### Worked Numerical Example: Left Leg + Right Leg Posterior Ridge

Suppose true height is $$H_i = 2.0 \cdot \text{Leg}_i + \varepsilon_i$$ and left/right leg lengths correlate at $$r = 0.99$$ ($$\mathrm{VIF} = \frac{1}{1 - 0.99^2} \approx \mathbf{50.3}$$!). Compare the posterior summaries of a two-leg Bayesian regression:

| Quantity | Posterior Mean | Posterior SD | 95% Credible Interval | Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| **$$\beta_{\text{left}}$$ alone** | $$+1.10$$ | $$2.45$$ | $$[-3.70,\; +5.90]$$ | Looks "uncertain" marginally! |
| **$$\beta_{\text{right}}$$ alone** | $$+0.90$$ | $$2.45$$ | $$[-3.90,\; +5.70]$$ | Looks "uncertain" marginally! |
| **Sum $$\beta_{\text{left}} + \beta_{\text{right}}$$** | **$$+2.00$$** | **$$0.08$$** | **$$[+1.84,\; +2.16]$$** | **Pinned down with 30× higher precision!** |

### Deep-Dive Explanation: Four Rules for Handling Multicollinearity in Bayes (Read Slowly)

1. **Always check posterior correlation before declaring a predictor "unimportant":** A wide marginal CI straddling zero may simply mean another predictor in the model is measuring the exact same underlying construct!
2. **Distinguish prediction goals from causal goals:** For pure prediction, collinearity rarely hurts (especially with regularizing priors); for causal estimation, consult your DAG before dropping or combining predictors.
3. **Combine redundant measurements cleanly:** Averaging `(left_leg + right_leg)/2` or using a latent factor model eliminates redundancy and cuts measurement noise in half.
4. **Watch HMC sampling speed:** Extreme posterior ridges force tiny HMC step sizes; standardizing or dropping exact duplicates speeds up NUTS by 5–10×.

**Quick check.** If predictor $$X_1$$ has $$R_1^2 = 0.95$$ when regressed on the other predictors in your model, what is its Variance Inflation Factor $$\mathrm{VIF}_1 = \frac{1}{1 - R_1^2}$$?

---

## Reference videos

- [Multicollinearity (in Regression Analysis)](https://www.youtube.com/watch?v=G1WX5GiFSWQ) — numiqo, English. **watch first**. Watch multicollinearity make it hard to separate each variable's share of the signal, exactly the phenomenon the lesson defines.
- [Multicollinearity](https://www.youtube.com/watch?v=O4jDva9B3fw) — Ben Lambert, English. Watch multicollinearity in regression interpretation, supporting the part that distinguishes prediction from reading coefficients.
- [Variance Inflation Factors: testing for multicollinearity](https://www.youtube.com/watch?v=0SBIXgPVex8) — Ben Lambert, English. Watch variance inflation factors, used where the lesson needs a diagnostic sign that predictors go together.

## Practice questions

1. Why do floor area and number of bedrooms easily create multicollinearity?
2. Give an example from your own work where prediction is still fine even though the coefficients are hard to interpret.
3. If two variables nearly duplicate information, would you consider keeping one variable or combining the two? Why?
4. In a salary study, why can education and professional skill make it difficult to interpret each coefficient individually?

## References

**Gelman, A., Hill, J., & Vehtari, A. (2020).** *Regression and Other Stories*. Cambridge University Press.

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

---

*Next lesson: [5.4 Interaction Effects]({{ site.baseurl }}/contents/en/chapter05/05_04_interaction_effects/)*
