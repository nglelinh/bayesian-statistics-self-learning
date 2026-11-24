---
layout: post
title: "Lesson 5.4: Interaction Effects - When Effects Depend on Each Other"
chapter: '05'
order: 4
owner: Nguyen Le Linh
lang: en
categories:
- chapter05
lesson_type: required
---

Does rugged terrain hurt a country’s GDP? Across Europe and Asia, the answer is clearly **yes**—mountains make trade expensive. Yet in Africa, economists found the exact *opposite* slope: rugged terrain was **positively** associated with higher GDP (because mountains historically shielded communities from the slave trade!). An additive regression `GDP ~ ruggedness + continent` is mathematically blind to that sign flip—it forces one single slope everywhere! Only an **interaction term** (`ruggedness × continent`) lets the effect of one predictor depend on the level of another.

This lesson makes **interaction effects** effortless to specify, compute, and visualize in Bayesian regression—showing why **centering predictors** is essential before interpreting main effects.

---

## Background Knowledge Map: Conditional Slopes and Interaction Geometry

1. **Additive vs. Interactive Linear Models:** Adding $$\beta_{12} X_1 X_2$$ to $$\mu = \alpha + \beta_1 X_1 + \beta_2 X_2$$ lets the slope of $$X_1$$ vary linearly with $$X_2$$: $$\frac{\partial \mu}{\partial X_1} = \beta_1 + \beta_{12} X_2$$!
2. **Main Effects Become Conditional Effects:** Once $$\beta_{12} X_1 X_2$$ is in the model, $$\beta_1$$ is **NO LONGER** the overall average effect of $$X_1$$—it is specifically the slope of $$X_1$$ *when $$X_2 = 0$$*! Centering $$X_2$$ at its mean makes $$\beta_1$$ immediately interpretable again.
3. **Symmetry of Interactions:** Algebraically, $$\beta_{12} X_1 X_2$$ equally means the slope of $$X_1$$ depends on $$X_2$$ *and* the slope of $$X_2$$ depends on $$X_1$$—the data alone doesn’t label one as "moderator."
4. **Triptych / Counterfactual Plotting:** Never interpret interactions from a raw coefficient table alone—plot predicted curves of $$Y$$ vs. $$X_1$$ at three slices of $$X_2$$ (low, medium, high) with posterior uncertainty bands!

---

## Learning objectives

After this lesson, you need to understand what an interaction effect is and why many real phenomena cannot be described by a simple additive model. You also need to know how to read an interaction in the style of "the effect of one variable changes with the context of another variable" instead of trying to force every coefficient into a fixed effect.

> **Mini example.** A test-prep program may help decent students improve very quickly, but for students who lack fundamentals, the effect is smaller if no supplementary materials are available. The effect of study hours is then not fixed for everyone, but depends on entry level.
>
> **Quick check.** If the effect of one predictor changes with the level of another predictor, what will a simple additive model miss?

## 1. The real world is rarely just "adding up"

In simple additive regression, we write:

$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \epsilon
$$

This model says that the effect of $$x_1$$ is the same at every level of $$x_2$$, and the effect of $$x_2$$ is also the same at every level of $$x_1$$. But in practice, many phenomena do not work this way: the effectiveness of advertising depends on product quality, the effect of diet depends on activity level, the effect of study hours depends on background knowledge, and the effect of a drug depends on age or underlying conditions.

In that case we need an interaction.

## 2. What is an interaction effect?

An interaction occurs when the effect of one predictor on the outcome **changes with the value of another predictor**.

A model with an interaction between $$x_1$$ and $$x_2$$ is usually written:

$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \beta_3 (x_1 x_2) + \epsilon
$$

The new component $$\beta_3 (x_1 x_2)$$ is the interaction term. If $$\beta_3$$ is significantly different from 0, it suggests that the slope of $$x_1$$ changes when $$x_2$$ changes, or, looking the other way, the slope of $$x_2$$ changes when $$x_1$$ changes.

![No interaction: the lines are nearly parallel]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_no_interaction_parallel_lines.png)

![With interaction: the slope changes by group]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_with_interaction_different_slopes.png)

![Comparison of models with and without interaction]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_interaction_model_comparison.png)

## 3. Seeing it in a picture is easier than seeing it in a formula

![Additive model with nearly parallel lines]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_additive_model_demo.png)

![Interactive model with different slopes]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_interactive_model_demo.png)

Let us compare the two situations:

### Additive model

In the additive model, the lines are nearly parallel. This means that different groups may have different baseline levels, but the effect of $$x_1$$ on $$y$$ is nearly the same across groups.

### Model with interaction

In the model with interaction, the lines have clearly different slopes. This means that for the same one-unit increase in $$x_1$$, the outcome rises strongly or weakly depending on the level of $$x_2$$.

This is the core intuition of interaction.

## 4. Real examples to see interaction more clearly

### Example 1: study time and entry level

The outcome here is the final exam score, while the predictors are weekly study hours and entry level.

If a student already has a good foundation, one more hour of study can raise the score quite noticeably. But for a student who lacks fundamentals, one more hour of study does not necessarily make a big difference if the basic knowledge gaps have not been filled.

The effect of study hours then depends on entry level, so an interaction is reasonable.

### Example 2: advertising and product quality

Advertising can be much more effective when the product is already good. If the product is poor, increasing advertising may only help people learn about it faster without producing lasting conversion.

In other words, the effect of the advertising budget depends on product quality.

### Example 3: treatment and severity of illness

A treatment protocol may be very effective for mild cases but less effective for very severe cases, or the other way around. The effect of the treatment then changes with severity.

### Experiment: from an additive model to a model with interaction

One common line → two parallel lines → two lines with different slopes; watch how the RSS falls.

<div class="interactive-demo" markdown="1">
<div data-demo="confound-explainer" data-lang="en" data-tab="interaction"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 5. How to read an interaction correctly

The most common mistake is to read $$\beta_1$$ as a fixed common effect even though the model already has an interaction.

When there is an interaction:

$$
\frac{\partial y}{\partial x_1} = \beta_1 + \beta_3 x_2
$$

This says that the effect of $$x_1$$ is **no longer a single number**. It depends on $$x_2$$.

### Example with a binary variable

If $$x_2$$ is a group variable, where $$x_2 = 0$$ is the control group and $$x_2 = 1$$ is the intervention group, then in the control group the effect of $$x_1$$ is $$\beta_1$$, while in the intervention group the effect of $$x_1$$ is $$\beta_1 + \beta_3$$.

This means the interaction tells us the extent to which the intervention strengthens or weakens the effect of $$x_1$$.

![Conditional effects of x₁ by each x₂ group]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_conditional_effects_by_group.png)

![Interaction as the difference between two conditional effects]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_interaction_difference_distribution.png)

### 5.1. A numerical example for reading an interaction without getting lost

Suppose we model the final exam score as follows:

$$
\text{Score} = 4 + 0.2 \cdot \text{Study hours} + 1.0 \cdot \text{Good background} + 0.25 \cdot (\text{Study hours} \times \text{Good background}).
$$

Where:

- `Good background = 0` is the group lacking fundamentals,
- `Good background = 1` is the group with solid background knowledge.

Then:

- for the group lacking fundamentals, one more study hour raises the score on average by about **0.2 points**,
- for the group with a good background, one more study hour raises the score on average by about  
  $$0.2 + 0.25 = 0.45$$ points.

We can see this more clearly through a few concrete predictions:

- a student lacking fundamentals studying 2 hours:  
  $$4 + 0.2 \times 2 = 4.4$$
- a student with a good background studying 2 hours:  
  $$4 + 0.2 \times 2 + 1 + 0.25 \times 2 = 5.9$$
- a student lacking fundamentals studying 6 hours:  
  $$4 + 0.2 \times 6 = 5.2$$
- a student with a good background studying 6 hours:  
  $$4 + 0.2 \times 6 + 1 + 0.25 \times 6 = 7.7$$

The key point is that the difference between 2 hours and 6 hours of study is not the same across the two groups. That is exactly the interaction, written as numbers instead of just words.

## 6. Interactions are not only for binary variables

Interactions are also very common between two continuous variables.

For example, temperature and humidity jointly affect electricity consumption, income and age jointly affect spending behavior, and study time and sleep quality jointly affect exam scores.

![Effect lines when both variables are continuous]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_interaction_continuous_lines.png)

![3D view of the interaction between two continuous variables]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_continuous_interaction_3d.png)

![Contour plot of the interaction between two continuous variables]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_continuous_interaction_contour.png)

In the continuous x continuous case, images such as a contour plot or surface plot are usually far more intuitive than a table of coefficients. Interaction is therefore a topic where **visualization is almost mandatory**.

## 7. When should we think of an interaction?

### 7.1. When domain theory suggests it

If domain knowledge says that the effect changes with context, an interaction should be considered. Familiar examples are drug and age, training and background level, or price and customer segment.

### 7.2. When plots suggest different slopes

If you plot the data by group and see that the lines are not parallel, that is a very clear signal.

### 7.3. When a simple additive model leaves structured residuals

Some residual patterns can show that the model is missing dependence between predictors.

## 8. What beginners often misunderstand

### Misconception 1: "The main effect no longer has meaning"

Not exactly. The main effect still has meaning, but its meaning depends on how you code and center the variables. If a continuous variable is centered around its mean, then the main effect is usually the effect of the predictor at the average level of the other variable.

This is why standardizing or centering predictors is often very useful before interpreting an interaction.

### Misconception 2: "If there is an interaction, we must drop the main effects"

Usually we should not do this. An interaction usually goes together with the main effects so that the model keeps its basic interpretive meaning.

### Misconception 3: "Looking at the p-value or interval of the interaction is enough"

Not enough. With interactions, plots and conditional effects are as important as, or more important than, the summary number.

## 9. A familiar example: exercise and diet

Suppose the outcome is the kilograms lost in 8 weeks, while the predictors are the number of workouts per week and the level of diet adherence.

If the diet is very poor, adding 1 more workout may improve things only slightly. But if the diet is kept good, that same extra workout may make a larger difference.

This is the kind of situation where the additive model:

$$
\text{Weight loss} = \alpha + \beta_1 \cdot \text{Exercise} + \beta_2 \cdot \text{Diet} + \epsilon
$$

may miss an important part of the story.

The model with interaction would be more reasonable:

$$
\text{Weight loss} = \alpha + \beta_1 \cdot \text{Exercise} + \beta_2 \cdot \text{Diet} + \beta_3 \cdot (\text{Exercise} \times \text{Diet}) + \epsilon
$$

If $$\beta_3 > 0$$, it means that for the same 1 additional workout, a person who adheres well to the diet benefits more. If $$\beta_3 < 0$$, we would read it the other way: the effect of increasing exercise weakens when the diet is already at a very good level or when the two factors partly substitute for each other. The sign of the interaction therefore helps us understand whether the two factors are **amplifying** or **offsetting** each other.

## 10. How to report an interaction to a non-specialist

Do not start with:

> the interaction coefficient is 0.63.

Start with the language of the situation:

> The effect of study hours is not the same for every student. In the group with a good background, additional study time goes with a clearly larger increase in score than in the group with a weak background.

Only then give the number if needed.

This kind of interpretation helps the reader understand the nature of the phenomenon first, and then look at the quantitative part.

## 11. Chapter 5 closes here

By the end of this chapter, you have a very important toolkit for reading regression correctly, including multiple predictors at once, confounding and causal structure, multicollinearity, and interaction effects. This is the moment when regression stops being "drawing a straight line" and becomes a way of thinking about the mechanism that generates data.

> **3 key ideas.** An interaction occurs when the effect of one predictor changes with the level of another predictor, so the effect cannot always be interpreted as a fixed number for all cases; when a model has an interaction, the best way to read it is through conditional effects and to use plots instead of looking only at the coefficient table; and interactions are very common in real life because the effectiveness of an intervention, behavior, or conditions are rarely the same in every context.

---

### Worked Numerical Example: Computing a Sign-Flipping Conditional Slope by Hand

Suppose crop yield $$\mu$$ depends on **Water ($$x_1$$)**, **Shade ($$x_2 \in \{0=\text{Sun},\; 1=\text{Shade}\}$$)**:

$$\mu = 10 + 3x_1 + 2x_2 - 5(x_1 x_2).$$

Compute the exact effect of adding +1 unit of Water ($$\frac{\partial\mu}{\partial x_1} = 3 - 5x_2$$) in both conditions:
- **In Full Sun ($$x_2 = 0$$):** $$\mu = 10 + 3x_1 \implies$$ slope is **$$+3$$** (more water strongly boosts yield!).
- **In Full Shade ($$x_2 = 1$$):** $$\mu = (10 + 2) + (3 - 5)x_1 = 12 - 2x_1 \implies$$ slope flips to **$$-2$$** (extra water in shade rots the roots!).

Notice that looking only at the main-effect coefficient $$\beta_1 = +3$$ tells you *only* about Full Sun and completely misses the negative slope in Shade!

### Deep-Dive Explanation: Four Rules for Modeling Interactions Safely (Read Slowly)

1. **Always include both lower-order main effects when adding $$X_1 X_2$$:** Dropping $$X_1$$ or $$X_2$$ forces all interaction lines to cross artificially at the origin `(0, 0)`.
2. **Center continuous predictors before multiplying them:** Without centering, $$X_1$$ and $$X_1 X_2$$ become strongly collinear, inflating posterior uncertainty and slowing MCMC.
3. **Use regularizing priors on interaction terms:** With $$p = 10$$ predictors, there are $$\binom{10}{2} = 45$$ possible pairwise interactions—without shrinkage priors (e.g., $$\beta_{12} \sim \mathcal{N}(0, 0.5)$$), interactions overfit noise rapidly!
4. **Always compute posterior uncertainty on the *combined* conditional slope:** Draw $$\beta_1^{(s)} + \beta_{12}^{(s)} x_2$$ across posterior samples rather than testing $$\beta_1$$ and $$\beta_{12}$$ separately.

**Quick check.** In the crop-yield equation $$\mu = 10 + 3x_1 + 2x_2 - 5x_1 x_2$$, what is the predicted yield at $$x_1 = 2, x_2 = 1$$?

---

## Reference videos

- [GLM Part 6: Interaction effects: How to interpret and identify them](https://www.youtube.com/watch?v=3CCkeFShB3U) — Simplistics (QuantPsych), English. **watch first**. Watch the effect of one variable change with the level of the other, exactly the definition of interaction the lesson contrasts with the additive model.
- [How to Interpret a Regression with an Interaction Term](https://www.youtube.com/watch?v=J8IHdu-oM64) — Econometrics, Causality, and Coding with Dr. HK, English. Watch how to read the main coefficients and the interaction coefficient in a regression table.
- [Statistical Rethinking 2023 - 04 - Categories & Curves](https://www.youtube.com/watch?v=F0N4b7K_iYQ) — Richard McElreath, English. Watch curves and group differences written as a model, supporting the part where the interaction is more than just an added term.

## Practice questions

1. Give an example from everyday life where the effect of one variable clearly depends on another variable.
2. Why are non-parallel lines on a group plot a sign of a possible interaction?
3. In the example of study hours and entry level, what does the interaction help describe that the additive model misses?
4. If a continuous variable is not centered, what can be difficult about interpreting the main effects in a model with an interaction?

## References

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

---

*Next chapter: [Chapter 6: Bayesian Generalized Linear Models (GLMs)]({{ site.baseurl }}/contents/en/chapter06/)*
