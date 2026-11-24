---
layout: post
title: "Lesson 5.1: Multiple Regression - From One to Many Predictors"
chapter: '05'
order: 1
owner: Nguyen Le Linh
lang: en
categories:
- chapter05
lesson_type: required
---

Adding a second predictor to a regression can do something that feels like black magic: a variable that looked **positively** correlated with your outcome when analyzed alone can flip to **negative** (or drop to exact zero!) the moment you control for a second variable! Understanding *why* that happens—**partial (conditional) effects**—is the gateway from simple curve fitting to real-world Bayesian multiple regression.

This lesson extends single-predictor Bayesian regression to multiple predictors $$\mu_i = \alpha + \beta_1 x_{1i} + \cdots + \beta_p x_{pi}$$, explains why **standardizing predictors** makes priors and MCMC geometry vastly cleaner, and teaches you to read partial slopes accurately.

---

## Background Knowledge Map: Partial Effects, Standardization, and Posterior Geometry

1. **Conditional ("Holding Other Predictors Constant") Interpretation:** In multiple regression, $$\beta_1$$ answers *"what is the expected change in $$Y$$ for a 1-unit increase in $$X_1$$ among observations with the **exact same** value of $$X_2$$?"*—not the raw marginal correlation!
2. **Why Standardizing Predictors ($$z = (x - \bar{x})/s_x$$) Is a Bayesian Superpower:** Removes arbitrary unit scales (mm vs. km), centers the intercept $$\alpha$$ at the mean outcome (breaking correlation between $$\alpha$$ and slopes $$\beta_j$$), and lets you apply clean weakly informative priors like $$\beta_j \sim \mathcal{N}(0, 1)$$!
3. **Spurious vs. Masked Relationships:** Controlling for a second predictor can *reveal* a spurious correlation (when $$X_2$$ causes both $$X_1$$ and $$Y$$) OR *unmask* a real relationship that was previously hidden by two opposing effects!
4. **Posterior Uncertainty Reflects Shared Information:** When predictors share variance, Bayesian multiple regression automatically widens the marginal posterior intervals of $$\beta_1, \beta_2$$ to honestly reflect what the data cannot separate.

---

## Learning objectives

After this lesson, you need to understand why many real problems cannot use just one predictor. You also need to grasp the most important meaning of multiple regression: each coefficient should be read only as the effect of one variable when the other variables are held fixed. This is the foundation for reading regression results correctly in later lessons.

> **Mini example.** A company wants to predict employees' salaries. If we look only at years of experience, we will miss degree, job position, and region of residence. Multiple regression lets us include many factors at once so that the picture is fairer and closer to reality.
>
> **Quick check.** If two people have the same years of experience but different education, can a model with only one predictor describe the salary difference between them?

## 1. Why is one predictor often not enough?

In Chapter 4, we learned the simple linear regression model:

$$
y = \alpha + \beta x + \epsilon
$$

This model is very useful for building intuition, but the real world is rarely that simple. An exam score, for instance, depends not only on study hours but also on background knowledge, sleep quality, and the difficulty of the exam; a house price depends not only on floor area but also on location, the age of the house, the number of bedrooms, and the surrounding infrastructure; and weight is related not only to height but also to age, sex, activity level, and diet. If we try to force a many-cause problem into a one-variable model, we very easily both miss important information and misinterpret the meaning of the coefficient.

Multiple regression was created to handle exactly this situation.

## 2. What does a model with many predictors look like?

The general model is:

$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_k x_k + \epsilon
$$

Here, $$y$$ is the outcome, $$x_1, x_2, \ldots, x_k$$ are the predictors, $$\alpha$$ is the intercept, and each $$\beta_j$$ is the coefficient of the $$j$$-th predictor. The idea of this model is very natural: we add up the contribution of each predictor and then add a noise term $$\epsilon$$, because real data always fluctuates around the average trend and never lies exactly on a rigid formula.

The three views below show that the same outcome can be seen as several two-dimensional slices or as a multidimensional surface.

![Weight by height, colored by age]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_weight_vs_height_colored_by_age.png)

![Weight by age, colored by height]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_weight_vs_age_colored_by_height.png)

![3D view of weight by height and age]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_weight_height_age_3d.png)

The three figures above help us see that an outcome can change along **many dimensions at once**. When we look at each two-dimensional plot separately, we see only one slice of the problem. Multiple regression tries to stitch those slices together into one joint model.

## 3. The most important meaning: "holding the other variables fixed"

This is the hardest idea but also the most important idea of this whole chapter.

In multiple regression, the coefficient $$\beta_1$$ no longer means:

> whenever $$x_1$$ increases by one unit, $$y$$ increases by $$\beta_1$$ units.

The correct meaning is:

> when the other predictors are held fixed, if $$x_1$$ increases by one unit, then $$y$$ changes on average by about $$\beta_1$$ units.

It may sound like only a few extra words, but the meaning changes a lot.

### Example 1: salary, experience, and education

Suppose we have the model:

$$
\text{Salary} = \alpha + \beta_1 \cdot \text{Experience} + \beta_2 \cdot \text{Education} + \epsilon
$$

Then, $$\beta_1$$ must be read as the expected salary difference between two people with the **same education** who differ by one year of experience, while $$\beta_2$$ is the expected salary difference between two people with the **same years of experience** who differ by one education level. This is a far more realistic reading than mixing all the differences into a single coefficient.

### Example 2: weight, height, and age

If the model is:

$$
\text{Weight} = \alpha + \beta_1 \cdot \text{Height} + \beta_2 \cdot \text{Age} + \epsilon
$$

then $$\beta_1$$ speaks about the effect of height among people of the same age, while $$\beta_2$$ speaks about the effect of age among people of the same height. In short, multiple regression always compares in the style of "**everything else equal, only one variable changes**".

### 3.1. A numerical example for reading coefficients correctly

Suppose we fit a salary model on experience and education as follows:

$$
\text{Salary} = 8 + 0.6 \cdot \text{Experience} + 2.5 \cdot \text{Postgraduate}.
$$

Here:

- `Experience` is measured in years,
- `Postgraduate = 1` if the person has a postgraduate degree, and `= 0` otherwise,
- salary is measured in millions of VND per month.

Then:

- if two people have the **same education**, the person with 1 more year of experience has an expected salary higher by about **0.6 million/month**,
- if two people have the **same years of experience**, the person with a postgraduate degree has an expected salary higher by about **2.5 million/month**.

A concrete example:

- Person A: 5 years of experience, no postgraduate degree  
  $$8 + 0.6 \times 5 + 2.5 \times 0 = 11$$
- Person B: 6 years of experience, no postgraduate degree  
  $$8 + 0.6 \times 6 + 2.5 \times 0 = 11.6$$
- Person C: 5 years of experience, with a postgraduate degree  
  $$8 + 0.6 \times 5 + 2.5 \times 1 = 13.5$$

Comparing A with B gives us the reading of the experience coefficient. Comparing A with C gives us the reading of the education coefficient. This is exactly the "hold the other variables fixed" logic written out as numbers.

## 4. Why can the coefficients in simple regression and multiple regression differ?

This is something that confuses many beginners.

A predictor in simple regression can carry the influence of variables not yet put into the model.

The salary example shows this very clearly: if more educated people usually also have more experience, then a model using only education may "absorb" part of the effect of experience into the education coefficient.

When experience is added to the model, the education coefficient may decrease. This does not mean the new model is worse. On the contrary, it usually means the new model is separating the sources of influence more clearly.

### An intuitive way of thinking

Simple regression answers:

> looking at the whole picture, how does this variable go along with the outcome?

Multiple regression answers:

> if we try to hold the other factors stable, how is this variable still related to the outcome?

Hence these two questions are different, so it is normal for the answers to differ.

## 5. A real example: predicting house prices

Suppose we want to predict house prices from three variables: floor area, number of bedrooms, and distance to the center.

A reasonable model is:

$$
\text{House price} = \alpha + \beta_1 \cdot \text{Area} + \beta_2 \cdot \text{Bedrooms} + \beta_3 \cdot \text{Distance} + \epsilon
$$

The correct interpretation here is: $$\beta_1$$ tells us, between two houses with the same number of bedrooms and the same distance to the center, how much the expected price differs for a house with 1 more square meter; $$\beta_2$$ tells us, between two houses with the same area and location, how the expected price changes when adding 1 bedroom; and $$\beta_3$$ tells us, between two houses with the same area and number of rooms, how much the expected price differs for a house 1 km farther from the center.

If we do not say clearly "holding the other variables fixed", the reader can easily misunderstand the coefficient.

### 5.1. Why doesn't adding 1 bedroom always raise the price by the same amount?

Suppose the estimated model is:

$$
\text{House price} = 1.2 + 0.035 \cdot \text{Area} + 0.18 \cdot \text{Bedrooms} - 0.25 \cdot \text{Distance},
$$

where price is measured in **billions of VND**, area in **m²**, and distance to the center in **km**.

Then, comparing two houses with the same number of bedrooms and the same location, a house 10 m² larger will have an expected price higher by about:

$$
0.035 \times 10 = 0.35\ \text{billion VND}.
$$

If we compare two houses with the same area and the same location, a house with 1 more bedroom will have an expected price higher by about:

$$
0.18\ \text{billion VND}.
$$

But note: this coefficient `0.18` does not mean that "in every circumstance, adding 1 bedroom raises the price by 180 million". It is correct only for comparisons between houses **with area and location held fixed**. In real data, an extra bedroom usually also comes with a larger house, so if we forget this condition we will misread the coefficient very quickly.

## 6. What does multiple regression do for us?

### 6.1. Better prediction

When the outcome truly depends on many factors, adding appropriate predictors usually helps predict more closely. For example, predicting an exam score from study hours alone is usually worse than predicting from study hours combined with the background score and the attendance rate.

### 6.2. Fairer explanation

We can separate the influence of each variable instead of dumping everything on a single predictor. For example, to evaluate the effectiveness of a course, we should consider study time, level of participation, and entry level at the same time instead of looking at one single measure.

### 6.3. Preparing for causal thinking

Multiple regression does not automatically create causation, but it is a first step toward learning how to adjust for related variables, make fairer comparisons between groups, and think seriously about confounding in the next lesson.

## 7. What should we be careful about when using many predictors?

Adding more variables is not always good. There are at least three situations where we need to be especially careful.

### 7.1. Omitting an important variable

If an important variable is left out, the remaining coefficients can be distorted.

### 7.2. Predictors that are too similar

If two variables measure nearly the same thing, the model will have difficulty separating the effect of each. This is the topic of Lesson 5.3 on multicollinearity.

### 7.3. Adding variables without thinking

It is not true that "controlling for everything" is always good. Some variables should be included, but others should not. This is the content of Lesson 5.2 on confounding and DAGs.

## 8. Seeing multiple regression as a data-generating story

A Bayesian way of understanding is to see the model as a story in which each subject has different features, each feature contributes a part to the outcome, and the rest is fluctuation that the model cannot fully explain. For exam scores, this means each student has different study hours, entry scores, and attendance rates; these factors combine to produce an expected score; and the real result still fluctuates further because of health, exam-room psychology, and other random factors.

When we think this way, the formula is no longer dry notation, but a summary of a real process.

## 9. When reporting results, how should we interpret them?

A good interpretation usually has three connected parts: name the predictor clearly, state the condition "holding the other variables fixed", and then tie the result to real units instead of leaving behind an abstract coefficient.

For example:

> Holding education and job position constant, each additional year of experience is associated with an expected salary higher by about X million VND.

This kind of interpretation is much clearer than just saying:

> $$\beta_1 = 0.42$$.

## 10. Connecting to the next lessons

Multiple regression is the doorway to three very practical questions: whether any variable is distorting the relationship we care about, whether the predictors are too similar to each other, and whether the effect of one variable depends on another. Understanding this lesson firmly will help you not feel "overwhelmed" when moving on to confounding, multicollinearity, and interaction in the next three lessons.

> **3 key ideas.** Multiple regression lets us describe an outcome with many predictors at once, so it fits real problems better; each coefficient in multiple regression must always be read together with the condition "holding the other variables fixed"; and when a coefficient changes after adding a new predictor, that is usually a sign that the model is separating the influences better, not a sign that the model is wrong.

---

### Worked Numerical Example: Watching a Partial Slope Flip From Spurious to Zero

Suppose ice-cream sales ($$X_1$$) and shark attacks ($$Y$$) both depend on summer temperature ($$X_2$$, standardized):
- **Bivariate regression** ($$Y \sim X_1$$ alone): yields posterior $$\beta_1 \approx +0.78 \pm 0.12$$ (strong positive association!).
- **Multiple regression** ($$Y \sim X_1 + X_2$$): holding temperature $$X_2$$ constant, suppose the fitted posterior gives:
  $$\mu_i = 5.0 + \underbrace{0.02}_{\beta_1 \text{ (SD } 0.15\text{)}} X_{1i} + \underbrace{0.85}_{\beta_2 \text{ (SD } 0.14\text{)}} X_{2i}.$$
- **95% Credible Interval for $$\beta_1$$:** $$0.02 \pm 1.96(0.15) = [-0.27,\; +0.31]$$ (straddling zero cleanly!), while $$\beta_2$$ sits cleanly at $$[+0.58,\; +1.12]$$! Once you know temperature, knowing ice-cream sales adds **zero** predictive information about shark attacks!

### Deep-Dive Explanation: Four Rules for Bayesian Multiple Regression (Read Slowly)

1. **Always plot counterfactual / predictor-residual plots:** Don’t just stare at a table of 8 regression coefficients—plot predicted $$Y$$ as $$X_1$$ varies while holding $$X_2$$ fixed at its mean.
2. **Adding more predictors is NOT always better:** As the very next lesson (DAGs & Confounding) proves, controlling for the *wrong* variable (a collider or post-treatment mediator!) can actually *create* bias out of thin air!
3. **Check correlation among posterior slopes (`pair_plot`):** A strong negative diagonal band between $$\beta_1$$ and $$\beta_2$$ warns you that the data pins down their *sum* well, even if each individual slope looks wide.
4. **Use posterior predictive plots to verify fit across all predictors:** Plot residuals against every $$X_j$$ to catch missed curvature or interactions.

**Quick check.** In a standardized multiple regression where $$X_1, X_2$$ have mean 0 and SD 1, what is the concrete meaning of the intercept $$\alpha$$?

---

## Reference videos

- [Multiple Regression, Clearly Explained!!!](https://www.youtube.com/watch?v=EkAQAi3a4js) — StatQuest with Josh Starmer, English. **watch first**. Watch each coefficient as a contribution when the other predictors are already in the model, exactly how the lesson reads multiple regression.
- [Statistical Rethinking 2023 - 05 - Elemental Confounds](https://www.youtube.com/watch?v=mBEA7PKDmiY) — Richard McElreath, English. Watch why adding one variable changes the meaning of the other variable's coefficient, supporting the part on conditional effects.
- [Covariance and the regression line | Regression | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=ualmyZiPs9w) — Khan Academy, English. Watch how covariance enters the regression line, used where the lesson explains that a predictor does not stand alone.

## Practice questions

1. In the house price prediction problem, why is using only floor area usually not enough?
2. What does "holding the other variables fixed" mean in the example of salary by experience and education?
3. Think of a real problem in your field that needs at least three predictors.
4. When can a coefficient in simple regression differ quite a lot from the corresponding coefficient in multiple regression?

## References

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

**Gelman, A., Hill, J., & Vehtari, A. (2020).** *Regression and Other Stories*. Cambridge University Press.

---

*Next lesson: [5.2 Confounding and DAGs]({{ site.baseurl }}/contents/en/chapter05/05_02_confounding_dags/)*
